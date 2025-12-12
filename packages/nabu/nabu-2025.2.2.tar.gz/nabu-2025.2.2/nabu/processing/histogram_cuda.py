import numpy as np
from ..utils import get_cuda_srcfile, updiv
from ..cuda.utils import __has_cupy__
from .histogram import PartialHistogram, VolumeHistogram

if __has_cupy__:
    import cupy
    from ..cuda.processing import CudaProcessing


class CudaPartialHistogram(PartialHistogram):
    def __init__(
        self,
        method="fixed_bins_number",
        bin_width="uint16",
        num_bins=None,
        min_bins=None,
        cuda_options=None,
    ):
        if method == "fixed_bins_width":
            raise NotImplementedError("Histogram with fixed bins width is not implemented with the Cuda backend")
        super().__init__(
            method=method,
            bin_width=bin_width,
            num_bins=num_bins,
            min_bins=min_bins,
        )
        self.cuda_processing = CudaProcessing(**(cuda_options or {}))  # pylint: disable=E0606
        self._init_cuda_histogram()

    def _init_cuda_histogram(self):
        self.cuda_hist = self.cuda_processing.kernel(
            "histogram",
            filename=get_cuda_srcfile("histogram.cu"),
        )
        self.d_hist = self.cuda_processing.allocate_array("d_hist", self.num_bins, dtype=np.uint32)

    def _compute_histogram_fixed_nbins(self, data, data_range=None):
        if isinstance(data, np.ndarray):
            data = self.cuda_processing.to_device("data", data)
        if data_range is None:
            # Should be possible to do both in one single pass with ReductionKernel,
            # But not sure how to use native vector types "float2" with these kernels.
            # Probably the simplest would be a RawKernel with explicit reduction ?
            # pylint: disable=E0606
            data_min = cupy.nanmin(data).get()[()]
            data_max = cupy.nanmax(data).get()[()]
        else:
            data_min, data_max = data_range
        Nz, Ny, Nx = data.shape
        block = (16, 16, 4)
        grid = (
            updiv(Nx, block[0]),
            updiv(Ny, block[1]),
            updiv(Nz, block[2]),
        )
        self.d_hist.fill(0)
        self.cuda_hist(
            data,
            Nx,
            Ny,
            Nz,
            data_min,
            data_max,
            self.d_hist,
            self.num_bins,
            grid=grid,
            block=block,
        )
        # Return a result in the same format as numpy.histogram
        res_hist = self.d_hist.get()
        res_bins = np.linspace(data_min, data_max, num=self.num_bins + 1, endpoint=True)
        return res_hist, res_bins


class CudaVolumeHistogram(VolumeHistogram):
    def __init__(
        self,
        data_url,
        chunk_size_slices=100,
        chunk_size_GB=None,
        nbins=1e6,
        logger=None,
        cuda_options=None,
    ):
        self.cuda_options = cuda_options
        super().__init__(
            data_url,
            chunk_size_slices=chunk_size_slices,
            chunk_size_GB=chunk_size_GB,
            nbins=nbins,
            logger=logger,
        )

    def _init_histogrammer(self):
        self.histogrammer = CudaPartialHistogram(
            method="fixed_bins_number",
            num_bins=self.nbins,
            cuda_options=self.cuda_options,
        )

    def _compute_histogram(self, data):
        return self.histogrammer.compute_histogram(data)  # 3D
