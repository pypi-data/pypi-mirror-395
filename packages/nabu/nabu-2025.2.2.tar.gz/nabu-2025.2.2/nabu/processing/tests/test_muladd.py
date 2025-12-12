import pytest
import numpy as np
from nabu.processing.muladd import MulAdd
from nabu.testutils import get_data
from nabu.cuda.utils import __has_cupy__

if __has_cupy__:
    from nabu.processing.muladd_cuda import CudaMulAdd


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.data = get_data("chelsea.npz")["data"].astype("f")  # (300, 451)
    cls.tol = 1e-7
    if __has_cupy__:
        ...
    yield


@pytest.mark.usefixtures("bootstrap")
class TestMulad:
    def test_muladd(self):
        dst = self.data.copy()
        other = self.data.copy()
        mul_add = MulAdd()

        # Test with no subregion
        mul_add(dst, other, 1, 2)
        assert np.allclose(dst, self.data * 1 + other * 2)

        # Test with x-y subregion
        dst = self.data.copy()
        mul_add(dst, other, 0.5, 1.7, (slice(10, 200), slice(15, 124)), (slice(100, 290), slice(200, 309)))
        assert np.allclose(dst[10:200, 15:124], self.data[10:200, 15:124] * 0.5 + self.data[100:290, 200:309] * 1.7)

    @pytest.mark.skipif(not (__has_cupy__), reason="Need Cuda/cupy for this test")
    def test_cuda_muladd(self):
        mul_add = CudaMulAdd()
        dst = mul_add.processing.to_device("dst", self.data)
        other = mul_add.processing.to_device("other", (self.data / 2).astype("f"))

        # Test with no subregion
        mul_add(dst, other, 3, 5)
        assert np.allclose(dst.get(), self.data * 3 + (self.data / 2) * 5)

        # Test with x-y subregion
        dst.set(self.data)
        mul_add(dst, other, 0.5, 1.7, (slice(10, 200), slice(15, 124)), (slice(100, 290), slice(200, 309)))
        assert np.allclose(
            dst.get()[10:200, 15:124], self.data[10:200, 15:124] * 0.5 + (self.data / 2)[100:290, 200:309] * 1.7
        )
