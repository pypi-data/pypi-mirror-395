from itertools import product
import numpy as np
import pytest
from nabu.processing.unsharp import UnsharpMask
from nabu.processing.unsharp_opencl import OpenclUnsharpMask, __have_opencl__ as __has_pyopencl__
from nabu.cuda.utils import __has_cupy__
from nabu.testutils import get_data

if __has_pyopencl__:
    from pyopencl import CommandQueue
    import pyopencl.array as parray
    from silx.opencl.common import ocl
if __has_cupy__:
    import cupy
    from nabu.processing.unsharp_cuda import CudaUnsharpMask

try:
    from skimage.filters import unsharp_mask

    __has_skimage__ = True
except ImportError:
    __has_skimage__ = False


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.data = get_data("brain_phantom.npz")["data"]
    cls.imagej_results = get_data("dirac_unsharp_imagej.npz")
    cls.tol = 1e-4
    cls.sigma = 1.6
    cls.coeff = 0.5
    if __has_cupy__:
        ...
    if __has_pyopencl__:
        cls.cl_ctx = ocl.create_context()
    yield


@pytest.mark.usefixtures("bootstrap")
class TestUnsharp:
    def get_reference_result(self, method, data=None):
        if data is None:
            data = self.data
        unsharp_mask = UnsharpMask(data.shape, self.sigma, self.coeff, method=method)
        return unsharp_mask.unsharp(data)

    def check_result(self, result, method, data=None, error_msg_prefix=None):
        reference = self.get_reference_result(method, data=data)
        mae = np.max(np.abs(result - reference))
        err_msg = str(
            "%s: max error is too high with method=%s: %.2e > %.2e" % (error_msg_prefix or "", method, mae, self.tol)
        )
        assert mae < self.tol, err_msg

    @pytest.mark.skipif(not (__has_skimage__), reason="Need scikit-image for this test")
    def test_mode_gaussian(self):
        dirac = np.zeros((43, 43), "f")
        dirac[dirac.shape[0] // 2, dirac.shape[1] // 2] = 1
        sigma_list = [0.2, 0.5, 1.0, 2.0, 3.0]
        coeff_list = [0.5, 1.0, 3.0]
        for sigma, coeff in product(sigma_list, coeff_list):
            res = UnsharpMask(dirac.shape, sigma, coeff, method="gaussian").unsharp(dirac)
            ref = unsharp_mask(dirac, radius=sigma, amount=coeff, preserve_range=True)
            assert np.max(np.abs(res - ref)) < 1e-6, "Something wrong with mode='gaussian', sigma=%.2f, coeff=%.2f" % (
                sigma,
                coeff,
            )

    def test_mode_imagej(self):
        dirac = np.zeros(self.imagej_results["images"][0].shape, dtype="f")
        dirac[dirac.shape[0] // 2, dirac.shape[1] // 2] = 1
        for sigma, coeff, ref in zip(
            self.imagej_results["sigma"], self.imagej_results["amount"], self.imagej_results["images"]
        ):
            res = UnsharpMask(dirac.shape, sigma, coeff, method="imagej").unsharp(dirac)
            assert np.max(np.abs(res - ref)) < 1e-3, "Something wrong with mode='imagej', sigma=%.2f, coeff=%.2f" % (
                sigma,
                coeff,
            )

    @pytest.mark.skipif(not (__has_pyopencl__), reason="Need pyopencl for this test")
    def test_opencl_unsharp(self):
        cl_queue = CommandQueue(self.cl_ctx)
        d_image = parray.to_device(cl_queue, self.data)
        d_out = parray.zeros_like(d_image)
        for method in OpenclUnsharpMask.avail_methods:
            d_image = parray.to_device(cl_queue, self.data)
            d_out = parray.zeros_like(d_image)

            opencl_unsharp = OpenclUnsharpMask(self.data.shape, self.sigma, self.coeff, method=method, ctx=self.cl_ctx)
            opencl_unsharp.unsharp(d_image, output=d_out)
            res = d_out.get()
            self.check_result(res, method, error_msg_prefix="OpenclUnsharpMask")

    @pytest.mark.skipif(not (__has_cupy__), reason="Need cuda/cupy for this test")
    def test_cuda_unsharp(self):
        d_image = cupy.array(self.data)
        d_out = cupy.array(d_image)
        for method in CudaUnsharpMask.avail_methods:
            cuda_unsharp = CudaUnsharpMask(self.data.shape, self.sigma, self.coeff, method=method)  # , ctx=self.ctx)
            cuda_unsharp.unsharp(d_image, output=d_out)
            res = d_out.get()
            self.check_result(res, method, error_msg_prefix="CudaUnsharpMask")
