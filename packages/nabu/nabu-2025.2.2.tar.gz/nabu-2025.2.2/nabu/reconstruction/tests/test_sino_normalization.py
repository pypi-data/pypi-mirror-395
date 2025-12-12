import numpy as np
import pytest
from nabu.testutils import get_data
from nabu.cuda.utils import __has_cupy__
from nabu.reconstruction.sinogram import SinoNormalization

if __has_cupy__:
    from nabu.reconstruction.sinogram_cuda import CudaSinoNormalization


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.sino = get_data("sino_refill.npy")
    cls.tol = 1e-7
    cls.norm_array_1D = np.arange(cls.sino.shape[-1]) + 1
    cls.norm_array_2D = np.arange(cls.sino.size).reshape(cls.sino.shape) + 1


@pytest.mark.usefixtures("bootstrap")
class TestSinoNormalization:
    def test_sino_normalization(self):
        sino_proc = SinoNormalization(kind="chebyshev", sinos_shape=self.sino.shape)
        sino = self.sino.copy()
        sino_proc.normalize(sino)

    @pytest.mark.skipif(not (__has_cupy__), reason="Need cupy for sinogram normalization with cuda backend")
    def test_sino_normalization_cuda(self):
        sino_proc = SinoNormalization(kind="chebyshev", sinos_shape=self.sino.shape)
        sino = self.sino.copy()
        ref = sino_proc.normalize(sino)

        cuda_sino_proc = CudaSinoNormalization(kind="chebyshev", sinos_shape=self.sino.shape)
        d_sino = cuda_sino_proc.cuda_processing.to_device("d_sino", self.sino)
        cuda_sino_proc.normalize(d_sino)
        res = d_sino.get()

        assert np.max(np.abs(res - ref)) < self.tol

    def get_normalization_reference_result(self, op, normalization_arr):
        # Perform explicit operations to compare with numpy.divide, numpy.subtract, etc
        if op == "subtraction":
            ref = self.sino - normalization_arr
        elif op == "division":
            ref = self.sino / normalization_arr
        return ref

    def test_sino_array_subtraction_and_division(self):
        with pytest.raises(ValueError):
            SinoNormalization(kind="subtraction", sinos_shape=self.sino.shape)

        def compare_normalizations(normalization_arr, op):
            sino_normalization = SinoNormalization(
                kind=op, sinos_shape=self.sino.shape, normalization_array=normalization_arr
            )
            sino = self.sino.copy()
            sino_normalization.normalize(sino)
            ref = self.get_normalization_reference_result(op, normalization_arr)
            assert np.allclose(sino, ref), "operation=%s, normalization_array dims=%d" % (op, normalization_arr.ndim)

        compare_normalizations(self.norm_array_1D, "subtraction")
        compare_normalizations(self.norm_array_1D, "division")
        compare_normalizations(self.norm_array_2D, "subtraction")
        compare_normalizations(self.norm_array_2D, "division")

    @pytest.mark.skipif(not (__has_cupy__), reason="Need cupy for sinogram normalization with cuda backend")
    def test_sino_array_subtraction_cuda(self):
        with pytest.raises(ValueError):
            CudaSinoNormalization(kind="subtraction", sinos_shape=self.sino.shape)

        def compare_normalizations(normalization_arr, op):
            sino_normalization = CudaSinoNormalization(
                kind=op, sinos_shape=self.sino.shape, normalization_array=normalization_arr
            )
            sino = sino_normalization.cuda_processing.to_device("sino", self.sino)
            sino_normalization.normalize(sino)
            ref = self.get_normalization_reference_result(op, normalization_arr)
            assert np.allclose(sino.get(), ref)

        compare_normalizations(self.norm_array_1D, "subtraction")
        compare_normalizations(self.norm_array_2D, "subtraction")
        compare_normalizations(self.norm_array_1D, "division")
        compare_normalizations(self.norm_array_2D, "division")
