import pytest
import numpy as np
from scipy.ndimage import shift as ndshift
from nabu.preproc.shift import VerticalShift
from nabu.cuda.utils import __has_cupy__

if __has_cupy__:
    from nabu.preproc.shift_cuda import CudaVerticalShift


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    data = np.zeros([13, 11], "f")
    slope = 100 + np.arange(13)
    data[:] = slope[:, None]
    cls.radios = np.array([data] * 17)
    cls.shifts = 0.3 + np.arange(17)
    cls.indexes = range(17)
    # given the shifts and the radios we build the golden reference
    golden = []
    for iradio in range(17):
        projection_number = cls.indexes[iradio]
        my_shift = cls.shifts[projection_number]
        padded_radio = np.concatenate(
            [cls.radios[iradio], np.zeros([1, 11], "f")], axis=0
        )  # needs padding because ndshifs does not work as expected
        shifted_padded_radio = ndshift(padded_radio, [-my_shift, 0], mode="constant", cval=0.0, order=1).astype("f")
        shifted_radio = shifted_padded_radio[:-1]
        golden.append(shifted_radio)
    cls.golden = np.array(golden)
    cls.tol = 1e-5
    if __has_cupy__:
        ...


@pytest.mark.usefixtures("bootstrap")
class TestVerticalShift:
    def test_vshift(self):
        radios = self.radios.copy()
        new_radios = np.zeros_like(radios)

        Shifter = VerticalShift(radios.shape, self.shifts)

        Shifter.apply_vertical_shifts(radios, self.indexes, output=new_radios)
        assert abs(new_radios - self.golden).max() < self.tol

        Shifter.apply_vertical_shifts(radios, self.indexes)
        assert abs(radios - self.golden).max() < self.tol

    @pytest.mark.skipif(not (__has_cupy__), reason="Need cupy for this test")
    def test_cuda_vshift(self):
        Shifter = CudaVerticalShift(self.radios.shape, self.shifts)

        d_radios = Shifter.cuda_processing.to_device("d_radios", self.radios)
        d_radios2 = d_radios.copy()
        d_out = Shifter.cuda_processing.allocate_array("d_out", d_radios.shape, dtype=d_radios.dtype)

        Shifter.apply_vertical_shifts(d_radios, self.indexes, output=d_out)
        assert abs(d_out.get() - self.golden).max() < self.tol

        Shifter.apply_vertical_shifts(d_radios, self.indexes)
        assert abs(d_radios.get() - self.golden).max() < self.tol

        # Test with negative shifts
        radios2 = self.radios.copy()
        Shifter_neg = VerticalShift(self.radios.shape, -self.shifts)
        Shifter_neg.apply_vertical_shifts(radios2, self.indexes)

        Shifter_neg_cuda = CudaVerticalShift(d_radios.shape, -self.shifts)
        Shifter_neg_cuda.apply_vertical_shifts(d_radios2, self.indexes)
        err_max = np.max(np.abs(d_radios2.get() - radios2))
        #
        # FIXME tolerance was downgraded from 1e-6 to 8e-6 when switching to numpy 2
        #
        assert err_max < 8e-6, "Something wrong for negative translations: max error = %.2e" % err_max
