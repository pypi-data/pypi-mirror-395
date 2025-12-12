import numpy as np
import pytest
from nabu.processing.fft_cuda import get_available_fft_implems
from nabu.testutils import get_data, generate_tests_scenarios, compare_shifted_images
from nabu.cuda.utils import __has_cupy__, get_cuda_stream
from nabu.opencl.utils import get_opencl_context, __has_pyopencl__
from nabu.thirdparty.algotom_convert_sino import extend_sinogram

__has_cufft__ = False
if __has_cupy__:
    avail_fft = get_available_fft_implems()
    __has_cufft__ = len(avail_fft) > 0
__has_cupy__ = __has_cupy__ and __has_cufft__  # need both for using Cuda backprojector


if __has_cupy__:
    from nabu.reconstruction.fbp import CudaBackprojector
    from nabu.reconstruction.hbp import HierarchicalBackprojector
if __has_pyopencl__:
    from nabu.reconstruction.fbp_opencl import OpenCLBackprojector


scenarios = generate_tests_scenarios({"backend": ["cuda", "opencl"]})


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    file_desc = get_data("sino_halftomo.npz")
    cls.sino = file_desc["sinogram"] * 1e4
    cls.rot_center = file_desc["rot_center"]
    cls.tol = 5e-3
    if __has_cupy__:
        cls._cuda_stream = get_cuda_stream(force_create=True)
    if __has_pyopencl__:
        cls.opencl_ctx = get_opencl_context("all")


@pytest.mark.usefixtures("bootstrap")
@pytest.mark.parametrize("config", scenarios)
class TestHalftomo:
    def _get_backprojector(self, config, *bp_args, **bp_kwargs):
        if config["backend"] == "cuda":
            if not (__has_cupy__):
                pytest.skip("Need cupy and vkfft")
            Backprojector = CudaBackprojector
            ctx = None
        else:
            if not (__has_pyopencl__):
                pytest.skip("Need pyopencl")
            Backprojector = OpenCLBackprojector
            ctx = self.opencl_ctx
            if config.get("opencl_use_textures", True) is False:
                # patch "extra_options"
                extra_options = bp_kwargs.pop("extra_options", {})
                extra_options["use_textures"] = False
                bp_kwargs["extra_options"] = extra_options
        return Backprojector(*bp_args, **bp_kwargs, backend_options={"ctx": ctx})

    # ruff: noqa: PT028
    def test_halftomo_right_side(self, config, sino=None, rot_center=None):
        if sino is None:
            sino = self.sino
        if rot_center is None:
            rot_center = self.rot_center

        sino_extended, rot_center_ext = extend_sinogram(sino, rot_center, apply_log=False)
        sino_extended *= 2  # compat. with nabu normalization

        backprojector_extended = self._get_backprojector(
            config,
            sino_extended.shape,
            rot_center=rot_center_ext,
            halftomo=False,
            padding_mode="edges",
            angles=np.linspace(0, 2 * np.pi, sino.shape[0], True),
            extra_options={"centered_axis": True},
        )
        ref = backprojector_extended.fbp(sino_extended)

        backprojector = self._get_backprojector(
            config,
            sino.shape,
            rot_center=rot_center,
            halftomo=True,
            padding_mode="edges",
            extra_options={"centered_axis": True},
        )
        res = backprojector.fbp(sino)

        # The approach in algotom (used as reference) slightly differers:
        #   - altogom extends the sinogram with padding, so that it's ready-to-use for FBP
        #   - nabu filters the sinogram first, and then does the "half-tomo preparation".
        #     Filtering the sinogram first is better to avoid artefacts due to sharp transition in the borders
        metric, upper_bound = compare_shifted_images(res, ref, return_upper_bound=True)
        assert metric < 5, "Something wrong for halftomo with backend %s" % (config["backend"])

    def test_halftomo_left_side(self, config):
        sino = np.ascontiguousarray(self.sino[:, ::-1])
        rot_center = sino.shape[-1] - 1 - self.rot_center
        return self.test_halftomo_right_side(config, sino=sino, rot_center=rot_center)

    def test_halftomo_plain_backprojection(self, config):
        backprojector = self._get_backprojector(
            config,
            self.sino.shape,
            rot_center=self.rot_center,
            halftomo=True,
            padding_mode="edges",
            extra_options={"centered_axis": True},
        )
        d_sino_filtered = backprojector.sino_filter.filter_sino(self.sino)  # device array
        h_sino_filtered = d_sino_filtered.get()
        reference_fbp = backprojector.fbp(self.sino)

        def _check(rec, array_type):
            assert (
                np.max(np.abs(rec - reference_fbp)) < 1e-7
            ), "Something wrong with halftomo backproj using %s array and configuration %s" % (array_type, str(config))

        # Test with device array
        rec_from_already_filtered_sino = backprojector.backproj(d_sino_filtered)
        _check(rec_from_already_filtered_sino, "device")

        # Test with numpy array
        rec_from_already_filtered_sino = backprojector.backproj(h_sino_filtered)
        _check(rec_from_already_filtered_sino, "numpy")

    def test_halftomo_cor_outside_fov(self, config):
        sino = np.ascontiguousarray(self.sino[:, : self.sino.shape[-1] // 2])
        backprojector = self._get_backprojector(config, sino.shape, rot_center=self.rot_center, halftomo=True)
        res = backprojector.fbp(sino)  # noqa: F841
        # Just check that it runs, but no reference results. Who does this anyway ?!

    @pytest.mark.skipif(not (__has_cupy__), reason="Need cupy")
    def test_hbp_halftomo(self, config):
        if config["backend"] == "opencl":
            pytest.skip("No HBP available in OpenCL")
        B = HierarchicalBackprojector(self.sino.shape, halftomo=True, rot_center=self.rot_center, padding_mode="edge")
        res = B.fbp(self.sino)

        sino_extended, rot_center_ext = extend_sinogram(self.sino, self.rot_center, apply_log=False)
        sino_extended *= 2  # compat. with nabu normalization
        B_extended = HierarchicalBackprojector(
            sino_extended.shape,
            rot_center=rot_center_ext,
            padding_mode="edge",
            angles=np.linspace(0, 2 * np.pi, self.sino.shape[0], True),
        )
        res_e = B_extended.fbp(sino_extended)

        # see notes in test_halftomo_right_side()
        metric, upper_bound = compare_shifted_images(res, res_e, return_upper_bound=True)
        assert metric < 5, "Something wrong for halftomo with HBP"
