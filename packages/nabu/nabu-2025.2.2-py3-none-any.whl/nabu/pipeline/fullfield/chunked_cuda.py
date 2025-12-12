from ...preproc.ccd_cuda import CudaLog, CudaCCDFilter
from ...preproc.flatfield_cuda import CudaFlatField
from ...preproc.shift_cuda import CudaVerticalShift
from ...preproc.double_flatfield_cuda import CudaDoubleFlatField
from ...preproc.phase_cuda import CudaPaganinPhaseRetrieval
from ...preproc.ctf_cuda import CudaCTFPhaseRetrieval
from ...reconstruction.sinogram_cuda import CudaSinoBuilder, CudaSinoNormalization
from ...reconstruction.filtering_cuda import CudaSinoFilter
from ...reconstruction.rings_cuda import CudaMunchDeringer, CudaSinoMeanDeringer, CudaVoDeringer
from ...processing.unsharp_cuda import CudaUnsharpMask
from ...processing.rotation_cuda import CudaRotation
from ...processing.histogram_cuda import CudaPartialHistogram
from ...reconstruction.fbp import Backprojector
from ...reconstruction.hbp import HierarchicalBackprojector
from ...cuda.utils import __has_cupy__
from ..utils import pipeline_step
from .chunked import ChunkedPipeline

if __has_cupy__:
    import cupy


class CudaChunkedPipeline(ChunkedPipeline):
    """
    Cuda backend of ChunkedPipeline
    """

    backend = "cuda"
    FlatFieldClass = CudaFlatField
    DoubleFlatFieldClass = CudaDoubleFlatField
    CCDCorrectionClass = CudaCCDFilter
    PaganinPhaseRetrievalClass = CudaPaganinPhaseRetrieval
    CTFPhaseRetrievalClass = CudaCTFPhaseRetrieval
    UnsharpMaskClass = CudaUnsharpMask
    ImageRotationClass = CudaRotation
    VerticalShiftClass = CudaVerticalShift
    MunchDeringerClass = CudaMunchDeringer
    SinoMeanDeringerClass = CudaSinoMeanDeringer
    VoDeringerClass = CudaVoDeringer
    MLogClass = CudaLog
    SinoBuilderClass = CudaSinoBuilder
    SinoNormalizationClass = CudaSinoNormalization
    SinoFilterClass = CudaSinoFilter
    FBPClass = Backprojector
    HBPClass = HierarchicalBackprojector
    HistogramClass = CudaPartialHistogram

    def __init__(
        self,
        process_config,
        chunk_shape,
        logger=None,
        extra_options=None,
        margin=None,
        use_grouped_mode=False,
        cuda_options=None,
    ):
        self._init_cuda(cuda_options)
        super().__init__(
            process_config,
            chunk_shape,
            logger=logger,
            extra_options=extra_options,
            use_grouped_mode=use_grouped_mode,
            margin=margin,
        )
        self._allocate_array(self.radios.shape, "f", name="radios")
        self._determine_when_to_transfer_data_on_gpu()

    def _determine_when_to_transfer_data_on_gpu(self):
        # Decide when to transfer data to GPU. Normally it's right after reading the data,
        # But sometimes a part of the processing is done on CPU.
        self._when_to_transfer_radios_on_gpu = "read_data"
        if self.flatfield is not None:
            use_flats_distortion = getattr(self.flatfield, "distortion_correction", None) is not None
            use_pca_flats = self.processing_options["flatfield"]["method"].lower() == "pca"
            if use_flats_distortion or use_pca_flats:
                self._when_to_transfer_radios_on_gpu = "flatfield"

    def _init_cuda(self, cuda_options):
        if not (__has_cupy__):
            raise ImportError("Could not import cupy. Cannot use CudaChunkedPipeline")
        cuda_options = cuda_options or {}
        self._device_id = cuda_options.get("device_id", 0)
        cupy.cuda.Device(self._device_id).use()
        self._d_radios = None
        self._d_sinos = None
        self._d_recs = None

    def _allocate_array(self, shape, dtype, name=None):
        name = name or "tmp"  # should be mandatory
        d_name = "_d_" + name
        d_arr = getattr(self, d_name, None)
        if d_arr is None:
            self.logger.debug("Allocating %s: %s" % (name, str(shape)))
            d_arr = cupy.zeros(shape, dtype)  # pylint: disable=E0606
            setattr(self, d_name, d_arr)
        return d_arr

    def _transfer_radios_to_gpu(self):
        self.logger.debug("Transfering radios to GPU")
        self._d_radios.set(self.radios)
        self._h_radios = self.radios
        self.radios = self._d_radios

    def _process_finalize(self):
        self.radios = self._h_radios

    #
    # Pipeline execution (class specialization)
    #

    def _read_data(self):
        super()._read_data()
        if self._when_to_transfer_radios_on_gpu == "read_data":
            self._transfer_radios_to_gpu()

    def _flatfield(self):
        super()._flatfield()
        if self._when_to_transfer_radios_on_gpu == "flatfield":
            self._transfer_radios_to_gpu()

    def _reconstruct(self):
        super()._reconstruct()
        if "reconstruction" not in self.processing_steps:
            return
        rec_method = self.processing_options["reconstruction"]["method"]
        if rec_method == "cone":
            ((U, D), (L, R)) = self.margin
            U, D = U or None, -D or None
            # not sure why slicing can't be done before get()
            self.recs = self.recs.get()[U:D, ...]
        elif rec_method == "mlem" and self.processing_options["reconstruction"]["implementation"] == "corrct":
            pass  # already a numpy array
        else:
            self.recs = self.recs.get()

    def _write_data(self, data=None):
        super()._write_data(data=data)
        if "reconstruction" in self.processing_steps:
            self.recs = self._d_recs
        self.radios = self._h_radios

    @pipeline_step("histogram", "Computing histogram")
    def _compute_histogram(self, data=None):
        if data is None:
            data = self._d_recs
        self.recs_histogram = self.histogram.compute_histogram(data)

    def _dump_data_to_file(self, step_name, data=None):
        if data is None:
            data = self.radios
        if step_name not in self.datadump_manager.data_dump:
            return
        if isinstance(data, cupy.ndarray):
            data = data.get()
        self.datadump_manager.dump_data_to_file(step_name, data=data)
