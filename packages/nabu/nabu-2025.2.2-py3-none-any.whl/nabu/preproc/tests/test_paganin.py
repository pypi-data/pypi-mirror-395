import pytest
import numpy as np
from nabu.preproc.phase import PaganinPhaseRetrieval
from nabu.processing.fft_cuda import get_available_fft_implems
from nabu.testutils import generate_tests_scenarios, get_data
from nabu.thirdparty.tomopy_phase import retrieve_phase
from nabu.cuda.utils import __has_cupy__

__has_cufft__ = False
if __has_cupy__:
    from nabu.preproc.phase_cuda import CudaPaganinPhaseRetrieval

    avail_fft = get_available_fft_implems()
    __has_cufft__ = len(avail_fft) > 0

scenarios = {
    "distance": [1],
    "energy": [35],
    "delta_beta": [1e1],
    "margin": [((50, 50), (0, 0)), None],
}

scenarios = generate_tests_scenarios(scenarios)


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls

    cls.data = get_data("mri_proj_astra.npz")["data"]
    cls.rtol = 1.2e-6
    cls.rtol_pag = 5e-3


@pytest.mark.usefixtures("bootstrap")
class TestPaganin:
    """
    Test the Paganin phase retrieval.
    The reference implementation is tomopy.
    """

    @staticmethod
    def get_paganin_instance_and_data(cfg, data):
        pag_kwargs = cfg.copy()
        margin = pag_kwargs.pop("margin")
        if margin is not None:
            data = np.pad(data, margin, mode="edge")
        paganin = PaganinPhaseRetrieval(data.shape, **pag_kwargs)
        return paganin, data, pag_kwargs

    @staticmethod
    def crop_to_margin(data, margin):
        if margin is None:
            return data
        ((U, D), (L, R)) = margin
        D = None if D == 0 else -D
        R = None if R == 0 else -R
        return data[U:D, L:R]

    @pytest.mark.parametrize("config", scenarios)
    def test_paganin(self, config):
        paganin, data, _ = self.get_paganin_instance_and_data(config, self.data)
        res = paganin.apply_filter(data)

        data_tomopy = np.atleast_3d(np.copy(data)).T
        res_tomopy = retrieve_phase(
            data_tomopy,
            pixel_size=paganin.pixel_size_xy_micron[0] * 1e-4,
            dist=paganin.distance_cm,
            energy=paganin.energy_kev,
            alpha=1.0 / (4 * 3.141592**2 * paganin.delta_beta),
        )

        res_tomopy = self.crop_to_margin(res_tomopy[0].T, config["margin"])
        res = self.crop_to_margin(res, config["margin"])

        errmax = np.max(np.abs(res - res_tomopy) / np.max(res_tomopy))
        assert errmax < self.rtol_pag, "Max error is too high"

    @pytest.mark.skipif(not (__has_cupy__ and __has_cufft__), reason="Need cupy and vkfft for this test")
    @pytest.mark.parametrize("config", scenarios)
    def test_gpu_paganin(self, config):
        paganin, data, pag_kwargs = self.get_paganin_instance_and_data(config, self.data)

        gpu_paganin = CudaPaganinPhaseRetrieval(data.shape, **pag_kwargs)
        ref = paganin.apply_filter(data)
        res = gpu_paganin.apply_filter(data)
        errmax = np.max(np.abs((res - ref) / np.max(ref)))
        assert errmax < self.rtol, "Max error is too high"
