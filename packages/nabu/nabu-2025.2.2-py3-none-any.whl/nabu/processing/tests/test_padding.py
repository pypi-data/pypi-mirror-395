import numpy as np
import pytest
from nabu.cuda.utils import __has_cupy__
from nabu.opencl.utils import __has_pyopencl__, get_opencl_context
from nabu.processing.padding_cuda import CudaPadding
from nabu.processing.padding_opencl import OpenCLPadding
from nabu.testutils import __do_long_tests__
from nabu.testutils import get_data, generate_tests_scenarios

scenarios = {
    "shape": [(511, 512), (512, 511)],
    "pad_width": [((256, 255), (128, 127))],
    "mode_cuda": CudaPadding.supported_modes[:2] if __has_cupy__ else [],
    "mode_opencl": OpenCLPadding.supported_modes[:2] if __has_pyopencl__ else [],
    "constant_values": [0, ((1.0, 2.0), (3.0, 4.0))],
    "output_is_none": [True, False],
    "backend": ["cuda", "opencl"],
}


if __do_long_tests__:
    scenarios["mode_cuda"] = CudaPadding.supported_modes if __has_cupy__ else []
    scenarios["mode_opencl"] = OpenCLPadding.supported_modes if __has_pyopencl__ else []
    scenarios["pad_width"].extend([((0, 0), (6, 7))])

scenarios = generate_tests_scenarios(scenarios)


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.data = get_data("brain_phantom.npz")["data"]
    cls.tol = 1e-7
    if __has_cupy__:
        ...
    if __has_pyopencl__:
        cls.cl_ctx = get_opencl_context(device_type="all")
    yield
    if __has_cupy__:
        ...


@pytest.mark.usefixtures("bootstrap")
class TestPadding:
    @pytest.mark.parametrize("config", scenarios)
    def test_padding(self, config):
        backend = config["backend"]
        shape = config["shape"]
        padding_mode = config["mode_%s" % backend]
        data = self.data[: shape[0], : shape[1]]
        kwargs = {}
        if padding_mode == "constant":
            kwargs["constant_values"] = config["constant_values"]
        ref = np.pad(data, config["pad_width"], mode=padding_mode, **kwargs)

        PaddingCls = CudaPadding if backend == "cuda" else OpenCLPadding
        if backend == "cuda":
            backend_options = {}  # "cuda_options": {"ctx": self.cu_ctx}}
        else:
            backend_options = {"opencl_options": {"ctx": self.cl_ctx}}

        padding = PaddingCls(
            config["shape"],
            config["pad_width"],
            mode=padding_mode,
            constant_values=config["constant_values"],
            **backend_options,
        )
        if config["output_is_none"]:
            output = None
        else:
            output = padding.processing.allocate_array("output", ref.shape, dtype="f")

        d_img = padding.processing.allocate_array("d_img", data.shape, dtype="f")
        d_img.set(np.ascontiguousarray(data, dtype="f"))
        res = padding.pad(d_img, output=output)

        err_max = np.max(np.abs(res.get() - ref))
        assert err_max < self.tol, str("Something wrong with padding for configuration %s" % (str(config)))

    @pytest.mark.skipif(not (__has_cupy__) and not (__has_pyopencl__), reason="need cupy or pyopencl")
    def test_custom_coordinate_transform(self):
        data = self.data
        R, C = np.indices(data.shape, dtype=np.int32)

        pad_width = ((256, 255), (254, 251))
        mode = "reflect"

        coords_R = np.pad(R, pad_width[0], mode=mode)[:, 0]
        coords_C = np.pad(C, pad_width[1], mode=mode)[0, :]

        # Further transform of coordinates - here FFT layout
        coords_R = np.roll(coords_R, -pad_width[0][0])
        coords_C = np.roll(coords_C, -pad_width[1][0])

        padding_classes_to_test = []
        if __has_cupy__:
            padding_classes_to_test.append(CudaPadding)
        if __has_pyopencl__:
            padding_classes_to_test.append(OpenCLPadding)

        for padding_cls in padding_classes_to_test:
            ctx = self.cl_ctx if padding_cls.backend == "opencl" else None  # self.cu_ctx
            padding = padding_cls(data.shape, (coords_R, coords_C), mode=mode, ctx=ctx)

            d_img = padding.processing.allocate_array("d_img", data.shape, dtype="f")
            d_img.set(data)
            d_out = padding.processing.allocate_array("d_out", padding.padded_shape, dtype="f")

            padding.pad(d_img, output=d_out)

            ref = np.roll(np.pad(data, pad_width, mode=mode), (-pad_width[0][0], -pad_width[1][0]), axis=(0, 1))

            err_max = np.max(np.abs(d_out.get() - ref))
            assert err_max < self.tol, "Something wrong with custom padding"
