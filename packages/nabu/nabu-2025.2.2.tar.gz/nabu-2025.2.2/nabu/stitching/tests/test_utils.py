from nabu.stitching.utils.utils import has_itk, find_shift_with_itk
from scipy.ndimage import shift as shift_scipy
import numpy
import pytest
from nabu.testutils import get_data


@pytest.mark.parametrize("data_type", (numpy.float32, numpy.uint16))
@pytest.mark.skipif(not has_itk, reason="itk not installed")
def test_find_shift_with_itk(data_type):
    shift = (5, 2)
    img1 = get_data("chelsea.npz")["data"].astype(data_type)
    img2 = shift_scipy(
        img1.copy(),
        shift=shift,
        order=1,
    )

    img1 = img1[10:-10, 10:-10]
    img2 = img2[10:-10, 10:-10]
    assert find_shift_with_itk(img1=img1, img2=img2) == shift
