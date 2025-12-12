import numpy as np
import pytest
from nabu.cuda.utils import __has_cupy__
from nabu.opencl.utils import __has_pyopencl__, get_opencl_context
from nabu.testutils import get_data, generate_tests_scenarios

if __has_pyopencl__:
    from nabu.processing.fftshift import OpenCLFFTshift

configs = {
    "shape": [(300, 451), (300, 300), (255, 300)],
    "axes": [(1,)],
    "dtype_in_out": [(np.float32, np.complex64), (np.complex64, np.float32)],
    "inplace": [True, False],
}

scenarios = generate_tests_scenarios(configs)


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.data = get_data("chelsea.npz")["data"]
    cls.tol = 1e-7
    if __has_cupy__:
        ...
    if __has_pyopencl__:
        cls.cl_ctx = get_opencl_context(device_type="all")
    yield
    if __has_cupy__:
        ...


@pytest.mark.skip(reason="OpenCL fftshift is a prototype")
@pytest.mark.usefixtures("bootstrap")
class TestFFTshift:
    def _do_test_fftshift(self, config, fftshift_cls):
        shape = config["shape"]
        dtype = config["dtype_in_out"][0]
        dst_dtype = config["dtype_in_out"][1]
        axes = config["axes"]
        inplace = config["inplace"]
        if inplace and shape[-1] & 1:
            pytest.skip("Not Implemented")
        data = np.ascontiguousarray(self.data[: shape[0], : shape[1]], dtype=dtype)

        backend = fftshift_cls.backend
        ctx = self.cu_ctx if backend == "cuda" else self.cl_ctx
        backend_options = {"ctx": ctx}
        if not (inplace):
            fftshift = fftshift_cls(data.shape, dtype, dst_dtype=dst_dtype, axes=axes, **backend_options)
        else:
            fftshift = fftshift_cls(data.shape, dtype, axes=axes, **backend_options)

        d_data = fftshift.processing.allocate_array("data", shape, dtype)
        d_data.set(data)

        d_res = fftshift.fftshift(d_data)

        assert (
            np.max(np.abs(d_res.get() - np.fft.fftshift(data, axes=axes))) == 0
        ), "something wrong with fftshift_%s(%s)" % (backend, str(config))

    # @pytest.mark.skipif(not (__has_pycuda__), reason="Need pycuda for this test")
    # @pytest.mark.parametrize("config", scenarios)
    # def test_cuda_transpose(self, config):
    # self._do_test_transpose(config, CudaTranspose)

    @pytest.mark.skipif(not (__has_pyopencl__), reason="Need pyopencl for this test")
    @pytest.mark.parametrize("config", scenarios)
    def test_opencl_fftshift(self, config):
        self._do_test_fftshift(config, OpenCLFFTshift)
