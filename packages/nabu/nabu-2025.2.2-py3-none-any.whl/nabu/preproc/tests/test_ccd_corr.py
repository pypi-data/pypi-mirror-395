import pytest
import numpy as np
from nabu.utils import median2 as nabu_median_filter
from nabu.testutils import get_data
from nabu.cuda.utils import __has_cupy__
from nabu.preproc.ccd import CCDFilter

if __has_cupy__:
    from nabu.preproc.ccd_cuda import CudaCCDFilter


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls

    cls.data = get_data("mri_proj_astra.npz")["data"]
    cls.data /= cls.data.max()
    cls.put_hotspots_in_data()
    if __has_cupy__:
        ...


@pytest.mark.usefixtures("bootstrap")
class TestCCDFilter:
    @classmethod
    def put_hotspots_in_data(cls):
        # Put 5 hot spots in the data
        # (row, column, deviation from median)
        cls.hotspots = [(50, 51, 0.04), (151, 150, 0.08), (202, 303, 0.12), (322, 203, 0.14)]
        cls.threshold = 0.1  # parameterize ?
        data_medfilt = nabu_median_filter(cls.data)
        for r, c, deviation_from_median in cls.hotspots:
            cls.data[r, c] = data_medfilt[r, c] + deviation_from_median

    def check_detected_hotspots_locations(self, res):
        diff = self.data - res
        rows, cols = np.where(diff > 0)
        hotspots_arr = np.array(self.hotspots)
        M = hotspots_arr[:, -1] > self.threshold
        hotspots_rows = hotspots_arr[M, 0]
        hotspots_cols = hotspots_arr[M, 1]
        assert np.allclose(hotspots_rows, rows)
        assert np.allclose(hotspots_cols, cols)

    def test_median_clip(self):
        ccd_filter = CCDFilter(self.data.shape, median_clip_thresh=self.threshold)
        res = np.zeros_like(self.data)
        res = ccd_filter.median_clip_correction(self.data, output=res)
        self.check_detected_hotspots_locations(res)

    @pytest.mark.skipif(not (__has_cupy__), reason="Need cupy for this test")
    def test_cuda_median_clip(self):
        cuda_ccd_correction = CudaCCDFilter(self.data.shape, median_clip_thresh=self.threshold)

        cuda_proc = cuda_ccd_correction.cuda_median_filter.cuda_processing
        d_radios = cuda_proc.to_device("d_radios", self.data)
        d_out = cuda_proc.allocate_array("d_out", d_radios.shape, dtype=d_radios.dtype)
        cuda_ccd_correction.median_clip_correction(d_radios, output=d_out)
        res = d_out.get()
        self.check_detected_hotspots_locations(res)
