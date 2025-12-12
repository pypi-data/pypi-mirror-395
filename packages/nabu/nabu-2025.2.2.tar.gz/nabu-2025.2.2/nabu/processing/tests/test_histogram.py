import pytest
import numpy as np
from nabu.testutils import get_data
from nabu.processing.histogram import PartialHistogram
from nabu.cuda.utils import __has_cupy__

if __has_cupy__:
    from nabu.processing.histogram_cuda import CudaPartialHistogram


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.data = get_data("mri_rec_astra.npz")["data"]
    cls.data /= 10
    cls.data[:100] *= 10
    cls.data_part_1 = cls.data[:100]
    cls.data_part_2 = cls.data[100:]
    cls.data0 = cls.data.ravel()
    cls.bin_tol = 1e-5 * (cls.data0.max() - cls.data0.min())
    cls.hist_rtol = 1.5e-3
    if __has_cupy__:
        ...
    yield
    if __has_cupy__:
        ...


def add_nans_in_data(data_part1, data_part2, data_ref):
    data_part1.ravel()[0] = np.nan
    data_part2.ravel()[-1] = np.nan
    data_ref.ravel()[0] = np.nan
    data_ref.ravel()[-1] = np.nan


@pytest.mark.usefixtures("bootstrap")
class TestPartialHistogram:
    def compare_histograms(self, hist1, hist2):
        errmax_bins = np.max(np.abs(hist1[1] - hist2[1]))
        assert errmax_bins < self.bin_tol
        errmax_hist = np.max(np.abs(hist1[0] - hist2[0]) / hist2[0].max())
        assert errmax_hist / hist2[0].max() < self.hist_rtol

    def test_fixed_nbins(self):
        partial_hist = PartialHistogram(method="fixed_bins_number", num_bins=1e6)
        hist1 = partial_hist.compute_histogram(self.data_part_1.ravel())
        hist2 = partial_hist.compute_histogram(self.data_part_2.ravel())
        hist = partial_hist.merge_histograms([hist1, hist2])
        ref = np.histogram(self.data0, bins=partial_hist.num_bins)
        self.compare_histograms(hist, ref)

    def test_nans(self):
        partial_hist = PartialHistogram(method="fixed_bins_number", num_bins=1e6)
        data_part1 = self.data_part_1.copy()
        data_part2 = self.data_part_2.copy()
        data_ref = self.data0.copy()
        add_nans_in_data(data_part1, data_part2, data_ref)

        hist1 = partial_hist.compute_histogram(data_part1.ravel())
        hist2 = partial_hist.compute_histogram(data_part2.ravel())
        hist = partial_hist.merge_histograms([hist1, hist2])
        ref = np.histogram(data_ref, bins=partial_hist.num_bins, range=(np.nanmin(data_ref), np.nanmax(data_ref)))
        self.compare_histograms(hist, ref)

    @pytest.mark.skipif(not (__has_cupy__), reason="Need cuda/cupy for this test")
    def test_fixed_nbins_cuda(self):
        partial_hist = CudaPartialHistogram(method="fixed_bins_number", num_bins=1e6)
        data_part_1 = partial_hist.cuda_processing.to_device("data_part_1", np.tile(self.data_part_1, (1, 1, 1)))
        data_part_2 = partial_hist.cuda_processing.to_device("data_part_2", np.tile(self.data_part_2, (1, 1, 1)))
        hist1 = partial_hist.compute_histogram(data_part_1)
        hist2 = partial_hist.compute_histogram(data_part_2)
        hist = partial_hist.merge_histograms([hist1, hist2])
        ref = np.histogram(self.data0, bins=partial_hist.num_bins)
        self.compare_histograms(hist, ref)

    @pytest.mark.skipif(not (__has_cupy__), reason="Need cuda/cupy for this test")
    def test_nans_cuda(self):
        partial_hist = CudaPartialHistogram(method="fixed_bins_number", num_bins=1e6)
        data_part1 = self.data_part_1.copy()
        data_part2 = self.data_part_2.copy()
        data_ref = self.data0.copy()
        add_nans_in_data(data_part1, data_part2, data_ref)
        d_data_part1 = partial_hist.cuda_processing.to_device("data_part1", data_part1)
        d_data_part2 = partial_hist.cuda_processing.to_device("data_part2", data_part2)

        hist1 = partial_hist.compute_histogram(d_data_part1.reshape((1,) + d_data_part1.shape))
        hist2 = partial_hist.compute_histogram(d_data_part2.reshape((1,) + d_data_part2.shape))
        hist = partial_hist.merge_histograms([hist1, hist2])
        ref = np.histogram(data_ref, bins=partial_hist.num_bins, range=(np.nanmin(data_ref), np.nanmax(data_ref)))
        self.compare_histograms(hist, ref)
