import numpy as np
import pytest
from nabu.testutils import compare_arrays, get_data, generate_tests_scenarios, __do_long_tests__
from nabu.reconstruction.rings import MunchDeringer, SinoMeanDeringer, VoDeringer
from nabu.thirdparty.pore3d_deringer_munch import munchetal_filter
from nabu.cuda.utils import __has_cupy__

if __has_cupy__:
    import cupy
    from nabu.reconstruction.rings_cuda import CudaSinoMeanDeringer
    from nabu.processing.fft_cuda import get_available_fft_implems
    from nabu.thirdparty.tomocupy_remove_stripe import __have_tomocupy_deringer__

    from nabu.reconstruction.rings_cuda import (
        CudaMunchDeringer,
        can_use_cuda_deringer,
        CudaVoDeringer,
    )

    __has_cuda_deringer__ = can_use_cuda_deringer()
else:
    __has_cuda_deringer__ = False
    __have_tomocupy_deringer__ = False

try:
    from algotom.prep.removal import remove_all_stripe

    __has_algotom__ = True
except ImportError:
    __has_algotom__ = False


fw_scenarios = generate_tests_scenarios(
    {
        "levels": [4],
        "sigma": [1.0],
        "wname": ["db15"],
        "padding": [(100, 100)],
        "fft_implem": ["vkfft"],
    }
)
if __do_long_tests__:
    fw_scenarios = generate_tests_scenarios(
        {
            "levels": [4, 2],
            "sigma": [1.0, 2.0],
            "wname": ["db15", "haar", "rbio4.4"],
            "padding": [None, (100, 100), (50, 71)],
            "fft_implem": ["vkfft"],
        }
    )


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.sino = get_data("mri_sino500.npz")["data"]
    cls.sino2 = get_data("sino_bamboo_hercules.npz")["data"]
    cls.tol = 5e-3
    cls.rings = {150: 0.5, -150: 0.5}
    if __has_cupy__:
        cls._available_fft_implems = get_available_fft_implems()
    yield
    if __has_cupy__:
        ...


@pytest.mark.usefixtures("bootstrap")
class TestDeringer:
    @staticmethod
    def add_stripes_to_sino(sino, rings_desc):
        """
        Create a new sinogram by adding synthetic stripes to an existing one.

        Parameters
        ----------
        sino: array-like
            Sinogram.
        rings_desc: dict
            Dictionary describing the stripes locations and intensity.
            The location is an integer in [0, N[ where N is the number of columns.
            The intensity is a float: percentage of the current column mean value.
        """
        sino_out = np.copy(sino)
        for loc, intensity in rings_desc.items():
            sino_out[:, loc] += sino[:, loc].mean() * intensity
        return sino_out

    @staticmethod
    def get_fourier_wavelets_reference_result(sino, config):
        # Reference destriping with pore3d "munchetal_filter"
        padding = config.get("padding", None)
        if padding is not None:
            sino = np.pad(sino, ((0, 0), padding), mode="edge")
        ref = munchetal_filter(sino, config["levels"], config["sigma"], wname=config["wname"])
        if config["padding"] is not None:
            ref = ref[:, padding[0] : -padding[1]]
        return ref

    @pytest.mark.skipif(munchetal_filter is None, reason="Need PyWavelets for this test")
    @pytest.mark.parametrize("config", fw_scenarios)
    def test_munch_deringer(self, config):
        deringer = MunchDeringer(
            config["sigma"], self.sino.shape, levels=config["levels"], wname=config["wname"], padding=config["padding"]
        )
        sino = self.add_stripes_to_sino(self.sino, self.rings)
        ref = self.get_fourier_wavelets_reference_result(sino, config)
        # Wrapping with DeRinger
        res = np.zeros((1,) + sino.shape, dtype=np.float32)
        deringer.remove_rings(sino, output=res)

        err_max = np.max(np.abs(res[0] - ref))
        assert err_max < self.tol, "Max error is too high"

    @pytest.mark.skipif(
        not (__has_cuda_deringer__) or munchetal_filter is None,
        reason="Need cupy and pyvkfft for this test",
    )
    @pytest.mark.parametrize("config", fw_scenarios)
    def test_cuda_munch_deringer(self, config):
        fft_implem = config["fft_implem"]
        if fft_implem not in self._available_fft_implems:
            pytest.skip("FFT implementation %s is not available" % fft_implem)
        sino = self.add_stripes_to_sino(self.sino, self.rings)
        deringer = CudaMunchDeringer(
            config["sigma"],
            self.sino.shape,
            levels=config["levels"],
            wname=config["wname"],
            padding=config["padding"],
            fft_backend=fft_implem,
            # cuda_options={"ctx": self.ctx},
        )
        d_sino = deringer.cuda_processing.to_device("d_sino", sino)
        deringer.remove_rings(d_sino)
        res = d_sino.get()

        ref = self.get_fourier_wavelets_reference_result(sino, config)

        err_max = np.max(np.abs(res - ref))
        assert err_max < 1e-1, "Max error is too high with configuration %s" % (str(config))

    @pytest.mark.skipif(
        not (__has_algotom__),
        reason="Need algotom for this test",
    )
    def test_vo_deringer(self):
        deringer = VoDeringer(self.sino.shape)
        sino_deringed = deringer.remove_rings_sinogram(self.sino)  # noqa: F841
        sinos = np.tile(self.sino, (10, 1, 1))
        sinos_deringed = deringer.remove_rings_sinograms(sinos)  # noqa: F841
        # TODO check result. The generated test sinogram is "too synthetic" for this kind of deringer

    @pytest.mark.skipif(
        not (__have_tomocupy_deringer__ and __has_algotom__),
        reason="Need algotom and cupy for this test",
    )
    def test_cuda_vo_deringer(self):
        # Beware, this deringer seems to be buggy for "too-small" sinograms
        # (NaNs on the edges and in some regions). To be investigated

        deringer = CudaVoDeringer(self.sino2.shape)
        d_sino = cupy.array(self.sino2)
        deringer.remove_rings_sinogram(d_sino)
        sino = d_sino.get()

        if __has_algotom__:
            vo_deringer = VoDeringer(self.sino2.shape)
            sino_deringed = vo_deringer.remove_rings_sinogram(self.sino2)

            assert (
                np.max(np.abs(sino - sino_deringed)) < 2e-3
            ), "Cuda implementation of Vo deringer does not yield the same results as base implementation"

    def test_mean_deringer(self):
        deringer_no_filtering = SinoMeanDeringer(self.sino.shape, mode="subtract")

        sino = self.sino.copy()
        deringer_no_filtering.remove_rings_sinogram(sino)

        sino = self.sino.copy()
        deringer_with_filtering = SinoMeanDeringer(self.sino.shape, mode="subtract", filter_cutoff=(0, 30))
        deringer_with_filtering.remove_rings_sinogram(sino)
        # TODO check results

    @pytest.mark.skipif(not (__has_cupy__), reason="Need cupy for this test")
    def test_cuda_mean_deringer(self):
        cuda_deringer = CudaSinoMeanDeringer(
            self.sino.shape,
            mode="subtract",
            filter_cutoff=(
                0,
                10,
            ),
            # ctx=self.ctx,
        )
        deringer = SinoMeanDeringer(
            self.sino.shape,
            mode="subtract",
            filter_cutoff=(
                0,
                10,
            ),
        )

        d_sino = cuda_deringer.processing.to_device("sino", self.sino)
        cuda_deringer.remove_rings_sinogram(d_sino)

        sino = self.sino.copy()
        sino_d = deringer.remove_rings_sinogram(sino)

        dirac = np.zeros(self.sino.shape[-1], "f")
        dirac[dirac.size // 2] = 1
        deringer_filter_response = deringer._apply_filter(dirac)

        d_dirac = cuda_deringer.processing.to_device("dirac", dirac)
        cuda_deringer_filter_response = cuda_deringer._apply_filter(d_dirac)

        is_close, residual = compare_arrays(
            deringer_filter_response, cuda_deringer_filter_response.get(), 1e-7, return_residual=True
        )
        assert is_close, "Cuda deringer does not have the correct filter response: max_error=%.2e" % residual

        # There is a rather large discrepancy between the vertical_mean kernel and numpy.mean(). Not sure who is right
        is_close, residual = compare_arrays(sino_d, d_sino.get(), 1e-1, return_residual=True)
        assert is_close, (
            "Cuda deringer does not yield the same result as base implementation: max_error=%.2e" % residual
        )
