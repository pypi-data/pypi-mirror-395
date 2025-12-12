import numpy as np
import pytest
from nabu.cuda.utils import __has_cupy__
from nabu.opencl.utils import __has_pyopencl__, get_opencl_context
from nabu.testutils import get_data, generate_tests_scenarios
from nabu.processing.roll_opencl import OpenCLRoll

configs_roll = {
    "shape": [(300, 451), (300, 300), (255, 300)],
    "offset_x": [0, 10, 155],
    "dtype": [np.float32],  # , np.complex64],
}


scenarios_roll = generate_tests_scenarios(configs_roll)


@pytest.fixture(scope="class")
def bootstrap_roll(request):
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


@pytest.mark.usefixtures("bootstrap_roll")
class TestRoll:
    @staticmethod
    def _compute_ref(data, direction, offset):
        ref = data.copy()
        ref[:, offset:] = np.roll(data[:, offset:], direction, axis=1)
        return ref

    @pytest.mark.skipif(not (__has_pyopencl__), reason="Need pyopencl for this test")
    @pytest.mark.parametrize("config", scenarios_roll)
    def test_opencl_roll(self, config):
        shape = config["shape"]
        dtype = config["dtype"]
        offset_x = config["offset_x"]
        data = np.ascontiguousarray(self.data[: shape[0], : shape[1]], dtype=dtype)

        ref_forward = self._compute_ref(data, 1, offset_x)
        ref_backward = self._compute_ref(data, -1, offset_x)

        roll_forward = OpenCLRoll(dtype, direction=1, offset=offset_x, ctx=self.cl_ctx)
        d_data = roll_forward.processing.allocate_array("data", data.shape, dtype=dtype)
        d_data.set(data)
        roll_backward = OpenCLRoll(dtype, direction=-1, offset=offset_x, queue=roll_forward.processing.queue)

        roll_forward(d_data)
        # from spire.utils import ims
        # ims([d_data.get(), ref_forward, d_data.get() - ref_forward])
        assert np.allclose(d_data.get(), ref_forward), "roll_forward: something wrong with config=%s" % (str(config))

        d_data.set(data)
        roll_backward(d_data)
        assert np.allclose(d_data.get(), ref_backward), "roll_backward: something wrong with config=%s" % (str(config))
