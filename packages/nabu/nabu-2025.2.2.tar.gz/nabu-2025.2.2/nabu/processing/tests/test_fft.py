from itertools import permutations
import pytest
import numpy as np
from scipy.fft import fftn, ifftn, rfftn, irfftn
from nabu.testutils import generate_tests_scenarios, get_data, get_array_of_given_shape, __do_long_tests__
from nabu.cuda.utils import __has_cupy__, get_cuda_stream
from nabu.cuda.processing import CudaProcessing
from nabu.opencl.processing import OpenCLProcessing
from nabu.opencl.utils import __has_pyopencl__
from nabu.processing.fft_base import is_fast_axes
from nabu.processing.fft_cuda import VKCUFFT, CupyCUFFT, get_available_fft_implems
from nabu.processing.fft_opencl import VKCLFFT, has_vkfft as has_cl_vkfft

available_cuda_fft = get_available_fft_implems()
__has_vkfft__ = "vkfft" in available_cuda_fft
__has_cupyfft__ = "cupy" in available_cuda_fft

scenarios = {
    "shape": [(256,), (300,), (300, 301), (300, 302)],
    "r2c": [True, False],
    "precision": ["simple"],
    "backend": ["cuda-vkfft", "cuda-cupy", "opencl-vkfft"],
}

if __do_long_tests__:
    scenarios["shape"].extend([(307,), (125, 126, 260)])
    scenarios["precision"].append("double")

scenarios = generate_tests_scenarios(scenarios)


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls

    cls.data = get_data("chelsea.npz")["data"]
    cls.abs_tol = {
        "simple": {
            1: 5e-3,
            2: 1.0e0,
            3: 5e2,  # !
        },
        "double": {
            1: 1e-10,
            2: 1e-9,
            3: 1e-7,
        },
    }
    if __has_cupy__:
        stream = get_cuda_stream(force_create=True)
        cls.cuda_processing = CudaProcessing(stream=stream)
    if __has_pyopencl__:
        cls.opencl_processing = OpenCLProcessing(device_type="all")
    yield
    if __has_cupy__:
        ...


def _get_fft_cls(backend):
    fft_cls = None
    if backend == "cuda-vkfft":
        if not (__has_vkfft__ and __has_cupy__):
            pytest.skip("Need vkfft and cupy to use VKCUFFT")
        fft_cls = VKCUFFT
    if backend == "cuda-cupy":
        if not (__has_cupyfft__ and __has_cupy__):
            pytest.skip("Need cupy to use CupyCUFFT")
        fft_cls = CupyCUFFT
    if backend == "opencl-vkfft":
        if not (has_cl_vkfft() and __has_pyopencl__):
            pytest.skip("Need vkfft and pyopencl to use VKCLFFT")
        fft_cls = VKCLFFT
    return fft_cls


@pytest.mark.usefixtures("bootstrap")
class TestFFT:
    def _get_data_array(self, config):
        r2c = config["r2c"]
        shape = config["shape"]
        precision = config["precision"]
        dtype = {
            True: {"simple": np.float32, "double": np.float64},
            False: {"simple": np.complex64, "double": np.complex128},
        }[r2c][precision]
        data = get_array_of_given_shape(self.data, shape, dtype)
        return data

    @staticmethod
    def check_result(res, ref, config, tol, name=""):
        err_max = np.max(np.abs(res - ref))
        err_msg = "%s FFT(%s, r2c=%s): tol=%.2e, but max error = %.2e" % (
            name,
            str(config["shape"]),
            str(config["r2c"]),
            tol,
            err_max,
        )
        assert np.allclose(res, ref, atol=tol), err_msg

    def _do_fft(self, data, r2c, axes=None, return_fft_obj=False, fft_cls=None):
        backend_kwargs = {}
        if fft_cls.backend == "cuda":
            backend_kwargs["stream"] = self.cuda_processing.stream
        elif fft_cls.backend == "opencl":
            backend_kwargs["queue"] = self.opencl_processing.queue
        fft = fft_cls(data.shape, data.dtype, r2c=r2c, axes=axes, **backend_kwargs)

        d_data = fft.processing.allocate_array("_data", data.shape, dtype=data.dtype)
        d_data.set(data)
        d_out = fft.fft(d_data)
        return (d_out, fft) if return_fft_obj else d_out

    @staticmethod
    def _do_reference_fft(data, r2c, axes=None):
        ref_fft_func = rfftn if r2c else fftn
        ref = ref_fft_func(data, axes=axes)
        return ref

    @staticmethod
    def _do_reference_ifft(data, r2c, axes=None):
        ref_ifft_func = irfftn if r2c else ifftn
        ref = ref_ifft_func(data, axes=axes)
        return ref

    @pytest.mark.parametrize("config", scenarios)
    def test_fft(self, config):
        backend = config["backend"]
        fft_cls = _get_fft_cls(backend)

        r2c = config["r2c"]
        shape = config["shape"]
        precision = config["precision"]
        ndim = len(shape)
        if ndim == 3 and not (__do_long_tests__):
            pytest.skip("3D FFTs are done only for long tests - use NABU_LONG_TESTS=1")

        if "vkfft" in backend and ndim >= 2 and r2c and shape[-1] & 1:
            pytest.skip("R2C with odd-sized fast dimension is not supported in VKFFT")

        # FIXME - vkfft + POCL fail for R2C in one dimension
        if config["backend"] == "opencl-vkfft" and r2c and ndim == 1:  # noqa: SIM102
            if self.opencl_processing.ctx.devices[0].platform.name.strip().lower() == "portable computing language":
                pytest.skip("Something wrong with vkfft + pocl for R2C 1D")
        # ---

        data = self._get_data_array(config)

        d_res, fft_obj = self._do_fft(data, r2c, return_fft_obj=True, fft_cls=fft_cls)
        res = d_res.get()
        ref = self._do_reference_fft(data, r2c)

        tol = self.abs_tol[precision][ndim]
        self.check_result(res, ref, config, tol, name="fft_%s" % backend)

        # Complex-to-complex can also be performed on real data (as in numpy.fft.fft(real_data))
        if not (r2c):
            d_res = self._do_fft(data, False, fft_cls=fft_cls)
            res = d_res.get()
            ref = self._do_reference_fft(data, False)
            self.check_result(res, ref, config, tol, name="fft_%s" % backend)

        # IFFT
        res = fft_obj.ifft(d_res).get()
        self.check_result(res, data, config, tol, name="fft_%s" % backend)

    @pytest.mark.parametrize("config", scenarios)
    def test_fft_batched(self, config):
        backend = config["backend"]
        fft_cls = _get_fft_cls(backend)
        shape = config["shape"]
        if len(shape) == 1:
            return
        elif len(shape) == 3 and not (__do_long_tests__):
            pytest.skip("3D FFTs are done only for long tests - use NABU_LONG_TESTS=1")
        r2c = config["r2c"]
        tol = self.abs_tol[config["precision"]][len(shape)]

        data = self._get_data_array(config)

        if data.ndim >= 2 and r2c and shape[-1] & 1:
            pytest.skip("R2C with odd-sized fast dimension is not supported in VKFFT")

        # For R2C, only fastest axes are supported by vkfft
        if data.ndim == 2:
            if "vkfft" in backend:
                axes_to_test = [(1,)]
            else:
                axes_to_test = [(1,), (0,)]
        elif data.ndim == 3:
            if "vkfft" in backend:
                axes_to_test = [(1, 2), (2,)]
            else:
                axes_to_test = [(1, 2), (0, 1), (0, 2), (2,), (1,), (0,)]

        for axes in axes_to_test:
            d_res, cufft = self._do_fft(data, r2c, axes=axes, return_fft_obj=True, fft_cls=fft_cls)
            res = d_res.get()
            ref = self._do_reference_fft(data, r2c, axes=axes)
            self.check_result(res, ref, config, tol, name="fft_%s batched axes=%s" % (backend, str(axes)))
            # IFFT
            res = cufft.ifft(d_res).get()
            self.check_result(res, data, config, tol, name="fft_%s" % backend)

    @pytest.mark.skipif(not (__do_long_tests__), reason="Use NABU_LONG_TESTS=1 for this test")
    def test_fast_axes_utility_function(self):
        axes_to_test = {
            2: {
                (0, 1): True,
                (1,): True,
                (-1,): True,
                (-2,): False,
                (0,): False,
            },
            3: {
                (0, 1, 2): True,
                (0, 1): False,
                (1, 2): True,
                (2, 1): True,
                (-2, -1): True,
                (2,): True,
                (-1,): True,
            },
        }
        for ndim, axes_ in axes_to_test.items():
            for axes, is_fast in axes_.items():
                possible_axes = [axes]
                if len(axes) > 1:
                    possible_axes = list(permutations(axes, len(axes)))
                for ax in possible_axes:
                    assert is_fast_axes(ndim, ax) is is_fast
