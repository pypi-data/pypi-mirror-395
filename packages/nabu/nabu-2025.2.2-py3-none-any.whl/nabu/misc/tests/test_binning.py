from itertools import product
import numpy as np
import pytest
from nabu.misc.binning import binning


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.data = np.arange(100 * 99, dtype=np.uint16).reshape(100, 99)
    cls.tol = 1e-5


@pytest.mark.usefixtures("bootstrap")
class TestBinning:
    def testBinning(self):
        """
        Test the general-purpose binning function with an image defined by its indices.
        The test "image" is an array where entry [i, j] equals i * Nx + j (where Nx = array.shape[1]).
        Let (b_i, b_j) be the binning factor along each dimension,
        then the binned array at position [p_i, p_j] is equal to
           1/(b_i*b_j) * Sum(Sum(Nx*i + j, (j, p_j, p_j+b_j-1)), (i, p_i, p_i+b_i-1))
        which happens to be equal to
           (Nx * b_i + 2*Nx * p_i - Nx + b_j + 2*p_j - 1) /2
        """

        def get_reference_binned_image(img_shape, bin_factor):
            # reference[p_i, p_j] = 0.5 * (Nx * b_i + 2*Nx * p_i - Nx + b_j + 2*p_j - 1)
            Ny, Nx = img_shape
            img_shape_reduced = tuple(s - (s % b) for s, b in zip(img_shape, bin_factor))
            b_i, b_j = bin_factor
            inds_i, inds_j = np.indices(img_shape_reduced)
            p_i = inds_i[::b0, ::b1]
            p_j = inds_j[::b0, ::b1]
            return 0.5 * (Nx * b_i + 2 * Nx * p_i - Nx + b_j + 2 * p_j - 1)

        # Various test settings
        binning_factors = [2, 3, 4, 5, 6, 8, 10]
        n_items = [63, 64, 65, 66, 125, 128, 130]

        # Yep, that's 2401 tests...
        params = product(n_items, n_items, binning_factors, binning_factors)
        for s0, s1, b0, b1 in params:
            img = np.arange(s0 * s1).reshape((s0, s1))
            ref = get_reference_binned_image(img.shape, (b0, b1))
            res = binning(img, (b0, b1))

            assert np.allclose(res, ref)
