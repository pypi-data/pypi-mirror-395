import numpy as np
import pytest
from scipy.ndimage import shift
from nabu.pipeline.params import fbp_filters
from nabu.utils import clip_circle
from nabu.testutils import get_data, generate_tests_scenarios, __do_long_tests__
from nabu.cuda.utils import __has_cupy__, get_cuda_stream
from nabu.opencl.utils import get_opencl_context, __has_pyopencl__

from nabu.processing.fft_cuda import has_vkfft as has_vkfft_cu
from nabu.processing.fft_opencl import has_vkfft as has_vkfft_cl

__has_cupy__ = __has_cupy__ and has_vkfft_cu()
__has_pyopencl__ = __has_pyopencl__ and has_vkfft_cl()

if __has_cupy__:
    from nabu.reconstruction.fbp import CudaBackprojector
    from nabu.reconstruction.hbp import HierarchicalBackprojector
if __has_pyopencl__:
    from nabu.reconstruction.fbp_opencl import OpenCLBackprojector


scenarios = generate_tests_scenarios({"backend": ["cuda", "opencl"]})
if __do_long_tests__:
    scenarios = generate_tests_scenarios(
        {
            "backend": ["cuda", "opencl"],
            "input_on_gpu": [False, True],
            "output_on_gpu": [False, True],
            "use_textures": [True, False],
        }
    )


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.sino_512 = get_data("mri_sino500.npz")["data"]
    cls.ref_512 = get_data("mri_rec_astra.npz")["data"]
    # always use contiguous arrays
    cls.sino_511 = np.ascontiguousarray(cls.sino_512[:, :-1])
    # Could be set to 5.0e-2 when using textures. When not using textures, interpolation slightly differs
    cls.tol = 2e-2  # 5.1e-2

    if __has_cupy__:
        stream = get_cuda_stream(force_create=True)
    if __has_pyopencl__:
        cls.opencl_ctx = get_opencl_context("all")
    yield
    if __has_cupy__:
        del stream  # ?


def clip_to_inner_circle(img, radius_factor=0.99, out_value=0):
    radius = int(radius_factor * max(img.shape) / 2)
    return clip_circle(img, radius=radius, out_value=out_value)


@pytest.mark.usefixtures("bootstrap")
class TestFBP:

    def _get_backprojector(self, config, *bp_args, **bp_kwargs):
        if config["backend"] == "cuda":
            if not (__has_cupy__):
                pytest.skip("Need cupy and pyvkfft")
            Backprojector = CudaBackprojector
            ctx = None  # self.cuda_ctx
        else:
            if not (__has_pyopencl__):
                pytest.skip("Need pyopencl + pyvkfft")
            Backprojector = OpenCLBackprojector
            ctx = self.opencl_ctx
        if config.get("use_textures", True) is False:
            # patch "extra_options"
            extra_options = bp_kwargs.pop("extra_options", {})
            extra_options["use_textures"] = False
            bp_kwargs["extra_options"] = extra_options
        return Backprojector(*bp_args, **bp_kwargs, backend_options={"ctx": ctx})

    @staticmethod
    def apply_fbp(config, backprojector, sinogram):
        if config.get("input_on_gpu", False):
            sinogram = backprojector._processing.set_array("sinogram", sinogram)
        if config.get("output_on_gpu", False):
            output = backprojector._processing.allocate_array("output", backprojector.slice_shape, dtype="f")
        else:
            output = None
        res = backprojector.fbp(sinogram, output=output)
        if config.get("output_on_gpu", False):
            res = res.get()
        return res

    @pytest.mark.parametrize("config", scenarios)
    def test_fbp_512(self, config):
        """
        Simple test of a FBP on a 512x512 slice
        """
        B = self._get_backprojector(config, (500, 512))
        res = self.apply_fbp(config, B, self.sino_512)

        diff = res - self.ref_512
        tol = self.tol
        if not (B._use_textures):
            diff = clip_to_inner_circle(diff)
            tol = 5.1e-2
        err_max = np.max(np.abs(diff))

        assert err_max < tol, "Something wrong with config=%s" % (str(config))

    @pytest.mark.parametrize("config", scenarios)
    def test_fbp_511(self, config):
        """
        Test FBP of a 511x511 slice where the rotation axis is at (512-1)/2.0
        """
        B = self._get_backprojector(config, (500, 511), rot_center=255.5)
        res = self.apply_fbp(config, B, self.sino_511)
        ref = self.ref_512[:-1, :-1]

        diff = clip_to_inner_circle(res - ref)
        err_max = np.max(np.abs(diff))
        tol = self.tol
        if not (B._use_textures):
            tol = 5.1e-2

        assert err_max < tol, "Something wrong with config=%s" % (str(config))

        # Cropping the singoram to sino[:, :-1]  gives a reconstruction
        # that is not fully equivalent to rec512[:-1, :-1]  in the upper half of the image, outside FoV.
        # However, nabu Backprojector gives the same results as astra
        # Probably we should check this instead:

        # B = self._get_backprojector(config, (500, 511), rot_center=255.5, extra_options={"centered_axis": True})
        # res = self.apply_fbp(config, B, self.sino_511)
        # import astra
        # proj_geom = astra.create_proj_geom('parallel', 1, 511, B.angles)
        # proj_geom = astra.geom_postalignment(proj_geom, - 0.5)
        # vol_geom = astra.create_vol_geom(511, 511)
        # proj_id = astra.create_projector("cuda", proj_geom, vol_geom)
        # ref = astra.create_reconstruction("FBP_CUDA", proj_id, self.sino_511, proj_id)[1]
        # err_max = np.max(np.abs(res - ref))
        # assert err_max < self.tol, "Something wrong with config=%s" % (str(config))

    @pytest.mark.parametrize("config", scenarios)
    def test_fbp_roi(self, config):
        """
        Test FBP in region of interest
        """
        sino = self.sino_511

        B0 = self._get_backprojector(config, sino.shape, rot_center=255.5)
        ref = B0.fbp(sino)

        def backproject_roi(roi, reference):
            B = self._get_backprojector(config, sino.shape, rot_center=255.5, slice_roi=roi)
            res = self.apply_fbp(config, B, sino)
            err_max = np.max(np.abs(res - reference))
            return err_max

        cases = {
            # Test 1: use slice_roi=(0, -1, 0, -1), i.e plain FBP of whole slice
            1: [(0, None, 0, None), ref],
            # Test 2: horizontal strip
            2: [(0, None, 50, 55), ref[50:55, :]],
            # Test 3: vertical strip
            3: [(60, 65, 0, None), ref[:, 60:65]],
            # Test 4: rectangular inner ROI
            4: [(157, 162, 260, -10), ref[260:-10, 157:162]],
        }
        for roi, ref in cases.values():
            err_max = backproject_roi(roi, ref)
            assert err_max < self.tol, "Something wrong with ROI = %s for config=%s" % (
                str(roi),
                str(config),
            )

    @pytest.mark.parametrize("config", scenarios)
    def test_fbp_axis_corr(self, config):
        """
        Test the "axis correction" feature
        """
        sino = self.sino_512

        # Create a sinogram with a drift in the rotation axis
        def create_drifted_sino(sino, drifts):
            out = np.zeros_like(sino)
            for i in range(sino.shape[0]):
                out[i] = shift(sino[i], drifts[i])
            return out

        drifts = np.linspace(0, 20, sino.shape[0])
        sino = create_drifted_sino(sino, drifts)

        B = self._get_backprojector(config, sino.shape, extra_options={"axis_correction": drifts})
        res = self.apply_fbp(config, B, sino)

        delta_clipped = clip_circle(res - self.ref_512, radius=200)
        err_max = np.max(np.abs(delta_clipped))
        # Max error is relatively high, migh be due to interpolation of scipy shift in sinogram
        assert err_max < 10.0, "Max error is too high"

    @pytest.mark.parametrize("config", scenarios)
    def test_fbp_clip_circle(self, config):
        """
        Test the "clip outer circle" parameter in (extra options)
        """
        sino = self.sino_512
        tol = 1e-5

        for rot_center in [None, sino.shape[1] / 2.0 - 10, sino.shape[1] / 2.0 + 15]:
            B = self._get_backprojector(
                config, sino.shape, rot_center=rot_center, extra_options={"clip_outer_circle": True}
            )
            res = self.apply_fbp(config, B, sino)

            B0 = self._get_backprojector(
                config, sino.shape, rot_center=rot_center, extra_options={"clip_outer_circle": False}
            )
            res_noclip = B0.fbp(sino)
            ref = clip_to_inner_circle(res_noclip, radius_factor=1)
            err_max = np.max(np.abs(res - ref))
            assert err_max < tol, "Max error is too high for rot_center=%s ; %s" % (str(rot_center), str(config))

            # Test with custom outer circle value
            B1 = self._get_backprojector(
                config,
                sino.shape,
                rot_center=rot_center,
                extra_options={"clip_outer_circle": True, "outer_circle_value": np.nan},
            )
            res1 = self.apply_fbp(config, B1, sino)
            ref1 = clip_to_inner_circle(res_noclip, radius_factor=1, out_value=np.nan)
            abs_diff1 = np.abs(res1 - ref1)
            err_max1 = np.nanmax(abs_diff1)
            assert err_max1 < tol, "Max error is too high for rot_center=%s ; %s" % (str(rot_center), str(config))

    @pytest.mark.parametrize("config", scenarios)
    def test_fbp_centered_axis(self, config):
        """
        Test the "centered_axis" parameter (in extra options)
        """
        sino = np.pad(self.sino_512, ((0, 0), (100, 0)))
        rot_center = (self.sino_512.shape[1] - 1) / 2.0 + 100

        B0 = self._get_backprojector(config, self.sino_512.shape)
        ref = B0.fbp(self.sino_512)

        # Check that "centered_axis" worked
        B = self._get_backprojector(config, sino.shape, rot_center=rot_center, extra_options={"centered_axis": True})
        res = self.apply_fbp(config, B, sino)
        # The outside region (outer circle) is different as "res" is a wider slice
        diff = clip_to_inner_circle(res[50:-50, 50:-50] - ref)
        err_max = np.max(np.abs(diff))
        assert err_max < 5e-2, "centered_axis without clip_circle: something wrong"

        # Check that "clip_outer_circle" works when used jointly with "centered_axis"
        B = self._get_backprojector(
            config,
            sino.shape,
            rot_center=rot_center,
            extra_options={
                "centered_axis": True,
                "clip_outer_circle": True,
            },
        )
        res2 = self.apply_fbp(config, B, sino)
        diff = res2 - clip_to_inner_circle(res, radius_factor=1)
        err_max = np.max(np.abs(diff))
        assert err_max < 1e-5, "centered_axis with clip_circle: something wrong"

    @pytest.mark.parametrize("config", scenarios)
    def test_fbp_filters(self, config):
        for filter_name in set(fbp_filters.values()):
            if filter_name in [None, "ramlak"]:
                continue
            B = self._get_backprojector(config, self.sino_512.shape, filter_name=filter_name)
            self.apply_fbp(config, B, self.sino_512)
            # not sure what to check in this case

    @pytest.mark.parametrize("config", scenarios)
    def test_differentiated_backprojection(self, config):
        # test Hilbert + DBP
        sino_diff = np.diff(self.sino_512, axis=1, prepend=0).astype("f")
        # Need to translate the axis a little bit, because of non-centered differentiation.
        # prepend -> +0.5 ; append -> -0.5
        B = self._get_backprojector(config, sino_diff.shape, filter_name="hilbert", rot_center=255.5 + 0.5)
        rec = self.apply_fbp(config, B, sino_diff)  # noqa: F841
        # Looks good, but all frequencies are not recovered. Use a metric like SSIM or FRC ?


@pytest.mark.skipif(not (__has_cupy__), reason="Need cupy for using HBP")
@pytest.mark.usefixtures("bootstrap")
class TestHBP:

    def _compare_to_reference(self, res, ref, err_msg="", radius_factor=0.9, rel_tol=0.02):
        delta_clipped = clip_to_inner_circle(res - ref, radius_factor=radius_factor)
        err_max = np.max(np.abs(delta_clipped))
        err_max_rel = err_max / ref.max()
        assert err_max_rel < rel_tol, err_msg

    def test_hbp_simple(self):
        B = HierarchicalBackprojector(self.sino_512.shape)
        res = B.fbp(self.sino_512)
        self._compare_to_reference(res, self.ref_512)

    def test_hbp_input_output(self):
        B = HierarchicalBackprojector(self.sino_512.shape)

        d_sino = B._processing.to_device("d_sino2", self.sino_512)
        d_slice = B._processing.allocate_array("d_slice2", self.ref_512.shape)
        h_slice = np.zeros_like(self.ref_512)

        # in: host, out: host (not provided)
        # see test above

        # in: host, out: host (provided)
        res = B.fbp(self.sino_512, output=h_slice)
        self._compare_to_reference(h_slice, self.ref_512, err_msg="in: host, out: host (provided)")
        h_slice.fill(0)

        # in: host, out: device
        res = B.fbp(self.sino_512, output=d_slice)
        self._compare_to_reference(d_slice.get(), self.ref_512, err_msg="in: host, out: device")
        d_slice.fill(0)

        # in: device, out: host (not provided)
        res = B.fbp(d_sino)
        self._compare_to_reference(res, self.ref_512, err_msg="in: device, out: host (not provided)")

        # in: device, out: host (provided)
        res = B.fbp(d_sino, output=h_slice)
        self._compare_to_reference(h_slice, self.ref_512, err_msg="in: device, out: host (provided)")
        h_slice.fill(0)

        # in: device, out: device
        res = B.fbp(d_sino, output=d_slice)
        self._compare_to_reference(d_slice.get(), self.ref_512, err_msg="in: device, out: device")
        d_slice.fill(0)

    def test_hbp_cor(self):
        """
        Test HBP with various sinogram shapes, obtained by truncating horizontally the original sinogram.
        The Center of rotation is always 255.5 (the one of original sinogram), so it also tests reconstruction with a shifted CoR.
        """
        for crop in [1, 2, 5, 10]:
            sino = np.ascontiguousarray(self.sino_512[:, :-crop])
            B = HierarchicalBackprojector(sino.shape, rot_center=255.5)
            res = B.fbp(sino)

            # HBP always uses "centered_axis=1", so we cannot compare non-integer shifts
            if crop % 2 == 0:
                ref = self.ref_512[crop // 2 : -crop // 2, crop // 2 : -crop // 2]
                self._compare_to_reference(res, ref, radius_factor=0.95, rel_tol=0.02)

    def test_hbp_clip_circle(self):
        B_clip = HierarchicalBackprojector(self.sino_512.shape, extra_options={"clip_outer_circle": True})
        B_noclip = HierarchicalBackprojector(self.sino_512.shape, extra_options={"clip_outer_circle": False})
        res_clip = B_clip.fbp(self.sino_512)
        res_noclip = B_noclip.fbp(self.sino_512)
        self._compare_to_reference(res_clip, clip_to_inner_circle(res_noclip, radius_factor=1), "clip_circle")

    def test_hbp_axis_corr(self):
        sino = self.sino_512

        # Create a sinogram with a drift in the rotation axis
        def create_drifted_sino(sino, drifts):
            out = np.zeros_like(sino)
            for i in range(sino.shape[0]):
                out[i] = shift(sino[i], drifts[i])
            return out

        drifts = np.linspace(0, 20, sino.shape[0])
        sino = create_drifted_sino(sino, drifts)

        B = HierarchicalBackprojector(sino.shape, extra_options={"axis_correction": drifts})
        res = B.fbp(sino)

        # Max error is relatively high, migh be due to interpolation of scipy shift in sinogram
        self._compare_to_reference(res, self.ref_512, radius_factor=0.95, rel_tol=0.04, err_msg="axis_corr")

    @pytest.mark.skipif(not (__do_long_tests__), reason="need NABU_LONG_TESTS=1 for this test")
    def test_hbp_scale_factor(self):
        scale_factor = 0.03125
        B_scaled = HierarchicalBackprojector(self.sino_512.shape, extra_options={"scale_factor": scale_factor})
        B_unscaled = HierarchicalBackprojector(self.sino_512.shape)
        res_scaled = B_scaled.fbp(self.sino_512)
        res_unscaled = B_unscaled.fbp(self.sino_512)
        self._compare_to_reference(res_scaled, res_unscaled * scale_factor, rel_tol=1e-7, err_msg="scale_factor")
