# ruff: noqa
# pylint: skip-file

from os import path
import numpy as np
import math
from silx.image.tomography import get_next_power
from scipy import ndimage as nd
import h5py
import silx.io
import copy
from silx.io.url import DataUrl
from ...resources.logger import LoggerOrPrint
from ...resources.utils import is_hdf5_extension
from ...io.reader_helical import ChunkReaderHelical, get_hdf5_dataset_shape
from ...preproc.flatfield_variable_region import FlatFieldDataVariableRegionUrls as FlatFieldDataHelicalUrls
from ...preproc.distortion import DistortionCorrection
from ...preproc.shift import VerticalShift
from ...preproc.double_flatfield_variable_region import DoubleFlatFieldVariableRegion as DoubleFlatFieldHelical
from ...preproc.phase import PaganinPhaseRetrieval
from ...reconstruction.sinogram import SinoBuilder
from ...processing.unsharp import UnsharpMask
from ...processing.histogram import PartialHistogram, hist_as_2Darray
from ..utils import use_options, pipeline_step

from ..detector_distortion_provider import DetectorDistortionProvider

from .utils import (
    WriterConfiguratorHelical as WriterConfigurator,
)  # .utils is the same as ..utils but internally we retouch the key associated to "tiffwriter" of Writers to

# point to our class which can write tiff with names indexed by the z height above the sample stage in millimiters

from numpy.lib.stride_tricks import sliding_window_view
from ...misc.binning import get_binning_function
from .helical_utils import find_mirror_indexes


try:
    import nabuxx

    GriddedAccumulator = nabuxx.gridded_accumulator.GriddedAccumulator
    CCDFilter = nabuxx.ccd.CCDFilter
    Log = nabuxx.ccd.LogFilter
    cxx_paganin = nabuxx.paganin
except:
    logger_tmp = LoggerOrPrint(None)
    logger_tmp.info(
        "Nabuxx not available. Loading python implementation for gridded_accumulator, Log, CCDFilter, paganin"
    )
    from . import gridded_accumulator

    GriddedAccumulator = gridded_accumulator.GriddedAccumulator
    from ...preproc.ccd import Log, CCDFilter

    cxx_paganin = None


# For now we don't have a plain python/numpy backend for reconstruction
Backprojector = None


class HelicalChunkedRegriddedPipeline:
    """
    Pipeline for "helical" full or half field tomography.
    Data is processed by chunks. A chunk consists in K+-1 contiguous lines of all the radios
    which are read at variable height following the translations
    """

    extra_marge_granularity = 4
    """ This offers extra reading space to be able to read the redundant part 
    which might be sligtly larger and or require extra border for interpolation
    """

    FlatFieldClass = FlatFieldDataHelicalUrls
    DoubleFlatFieldClass = DoubleFlatFieldHelical

    CCDFilterClass = CCDFilter
    MLogClass = Log

    PaganinPhaseRetrievalClass = PaganinPhaseRetrieval
    UnsharpMaskClass = UnsharpMask
    VerticalShiftClass = VerticalShift
    SinoBuilderClass = SinoBuilder

    FBPClass = Backprojector
    HBPClass = None
    HistogramClass = PartialHistogram
    regular_accumulator = None

    def __init__(
        self,
        process_config,
        sub_region,
        logger=None,
        extra_options=None,
        phase_margin=None,
        reading_granularity=10,
        span_info=None,
        diag_zpro_run=0,
    ):
        """
        Initialize a "HelicalChunked" pipeline.

        Parameters
        ----------
        process_config: `nabu.resources.processcinfig.ProcessConfig`
            Process configuration.
        sub_region: tuple
            Sub-region to process in the volume for this worker, in the format
            `(start_x, end_x, start_z, end_z)`.
        logger: `nabu.app.logger.Logger`, optional
            Logger class
        extra_options: dict, optional
            Advanced extra options.
        phase_margin: tuple, optional
            Margin to use when performing phase retrieval, in the form ((up, down), (left, right)).
            See also the documentation of PaganinPhaseRetrieval.
            If not provided, no margin is applied.
        reading_granularity: int
            The data angular span which needs to be read for a reconstruction is read step by step,
            reading each time a maximum of reading_granularity radios, and doing the preprocessing
            till phase retrieval for each of these  angular groups

        Notes
        ------
        Using a `phase_margin` results in a lesser number of reconstructed slices.
        More specifically, if `phase_margin = (V, H)`, then there will be `chunk_size - 2*V`
        reconstructed slices (if the sub-region is in the middle of the volume)
        or `chunk_size - V` reconstructed slices (if the sub-region is on top or bottom
        of the volume).
        """

        self.span_info = span_info
        self.reading_granularity = reading_granularity

        self.logger = LoggerOrPrint(logger)

        self._set_params(process_config, sub_region, extra_options, phase_margin, diag_zpro_run)

        self._init_pipeline()

    def _set_params(self, process_config, sub_region, extra_options, phase_margin, diag_zpro_run):
        self.diag_zpro_run = diag_zpro_run
        self.process_config = process_config
        self.dataset_info = self.process_config.dataset_info

        self.processing_steps = self.process_config.processing_steps.copy()
        self.processing_options = self.process_config.processing_options

        sub_region = self._check_subregion(sub_region)

        self.chunk_size = sub_region[-1] - sub_region[-2]
        self.radios_buffer = None

        self._set_detector_distortion_correction()

        self.set_subregion(sub_region)

        self._set_phase_margin(phase_margin)
        self._set_extra_options(extra_options)
        self._callbacks = {}
        self._steps_name2component = {}
        self._steps_component2name = {}
        self._data_dump = {}
        self._resume_from_step = None

    @staticmethod
    def _check_subregion(sub_region):
        if len(sub_region) < 4:
            assert len(sub_region) == 2, " at least start_z and end_z are required in subregion"
            sub_region = (None, None) + sub_region
        if None in sub_region[-2:]:
            raise ValueError("Cannot set z_min or z_max to None")
        return sub_region

    def _set_extra_options(self, extra_options):
        if extra_options is None:
            extra_options = {}
        advanced_options = {}
        advanced_options.update(extra_options)
        self.extra_options = advanced_options

    def _set_phase_margin(self, phase_margin):
        if phase_margin is None:
            phase_margin = ((0, 0), (0, 0))
        self._phase_margin_up = phase_margin[0][0]
        self._phase_margin_down = phase_margin[0][1]
        self._phase_margin_left = phase_margin[1][0]
        self._phase_margin_right = phase_margin[1][1]

    def set_subregion(self, sub_region):
        """
        Set a sub-region to process.

        Parameters
        ----------
        sub_region: tuple
            Sub-region to process in the volume, in the format
            `(start_x, end_x, start_z, end_z)` or `(start_z, end_z)`.
        """
        sub_region = self._check_subregion(sub_region)
        dz = sub_region[-1] - sub_region[-2]
        if dz != self.chunk_size:
            raise ValueError(
                "Class was initialized for chunk_size = %d but provided sub_region has chunk_size = %d"
                % (self.chunk_size, dz)
            )
        self.sub_region = sub_region
        self.z_min = sub_region[-2]
        self.z_max = sub_region[-1]

    def _compute_phase_kernel_margin(self):
        """
        Get the "margin" to pass to classes like PaganinPhaseRetrieval.
        In order to have a good accuracy for filter-based phase retrieval methods,
        we need to load extra data around the edges of each image. Otherwise,
        a default padding type is applied.
        """
        if not (self.use_radio_processing_margin):
            self._phase_margin = None
            return
        up_margin = self._phase_margin_up
        down_margin = self._phase_margin_down
        # Horizontal margin is not implemented
        left_margin, right_margin = (0, 0)
        self._phase_margin = ((up_margin, down_margin), (left_margin, right_margin))

    @property
    def use_radio_processing_margin(self):
        return ("phase" in self.processing_steps) or ("unsharp_mask" in self.processing_steps)

    def _get_phase_margin(self):
        if not (self.use_radio_processing_margin):
            return ((0, 0), (0, 0))
        return self._phase_margin

    @property
    def phase_margin(self):
        """
        Return the margin for phase retrieval in the form ((up, down), (left, right))
        """
        return self._get_phase_margin()

    def _get_process_name(self, kind="reconstruction"):
        # In the future, might be something like "reconstruction-<ID>"
        if kind == "reconstruction":
            return "reconstruction"
        elif kind == "histogram":
            return "histogram"
        return kind

    def _configure_dump(self, step_name):
        if step_name not in self.processing_steps:
            if step_name == "sinogram" and self.process_config._dump_sinogram:
                fname_full = self.process_config._dump_sinogram_file
            else:
                return
        else:
            if not self.processing_options[step_name].get("save", False):
                return
            fname_full = self.processing_options[step_name]["save_steps_file"]

        fname, ext = path.splitext(fname_full)
        dirname, file_prefix = path.split(fname)
        output_dir = path.join(dirname, file_prefix)
        file_prefix += str("_%06d" % self._get_image_start_index())

        self.logger.info("omitting config in  data_dump because of too slow nexus writer ")

        self._data_dump[step_name] = WriterConfigurator(
            output_dir,
            file_prefix,
            file_format="hdf5",
            overwrite=True,
            logger=self.logger,
            nx_info={
                "process_name": step_name,
                "processing_index": 0,  # TODO
                #                "config": {"processing_options": self.processing_options, "nabu_config": self.process_config.nabu_config},
                "config": None,
                "entry": getattr(self.dataset_info.dataset_scanner, "entry", None),
            },
        )

    def _configure_data_dumps(self):
        self.process_config._configure_save_steps()
        for step_name in self.processing_steps:
            self._configure_dump(step_name)
        # sinogram is a special keyword: not in processing_steps, but guaranteed to be before sinogram generation

        if self.process_config._dump_sinogram:
            self._configure_dump("sinogram")

    #
    # Callbacks
    #

    def register_callback(self, step_name, callback):
        """
        Register a callback for a pipeline processing step.

        Parameters
        ----------
        step_name: str
            processing step name
        callback: callable
            A function. It will be executed once the processing step `step_name`
            is finished. The function takes only one argument: the class instance.
        """
        if step_name not in self.processing_steps:
            raise ValueError("'%s' is not in processing steps %s" % (step_name, self.processing_steps))
        if step_name in self._callbacks:
            self._callbacks[step_name].append(callback)
        else:
            self._callbacks[step_name] = [callback]

    #
    # Overwritten in inheriting classes
    #

    def _get_shape(self, step_name):
        """
        Get the shape to provide to the class corresponding to step_name.
        """
        if step_name == "flatfield":
            shape = self.radios_subset.shape
        elif step_name == "double_flatfield":
            shape = self.radios_subset.shape
        elif step_name == "phase":
            shape = self.radios_subset.shape[1:]
        elif step_name == "ccd_correction":
            shape = self.gridded_radios.shape[1:]
        elif step_name == "unsharp_mask":
            shape = self.radios_subset.shape[1:]
        elif step_name == "take_log":
            shape = self.radios.shape
        elif step_name == "radios_movements":
            shape = self.radios.shape
        elif step_name == "sino_normalization":
            shape = self.radios.shape
        elif step_name == "sino_normalization_slim":
            shape = self.radios.shape[:1] + (1,) + self.radios.shape[2:]
        elif step_name == "one_sino_slim":
            shape = self.radios.shape[:1] + self.radios.shape[2:]
        elif step_name == "build_sino":
            shape = self.radios.shape[:1] + (1,) + self.radios.shape[2:]
        elif step_name == "reconstruction":
            shape = self.sino_builder.output_shape[1:]
        else:
            raise ValueError("Unknown processing step %s" % step_name)
        self.logger.debug("Data shape for %s is %s" % (step_name, str(shape)))
        return shape

    def _allocate_array(self, shape, dtype, name=None):
        """this function can be redefined in the  derived class which is dedicated to gpu
        and will return gpu garrays
        """
        return _cpu_allocate_array(shape, dtype, name=name)

    def _cpu_allocate_array(self, shape, dtype, name=None):
        """For objects used in the pre-gpu part. They will be always on CPU even in the derived class"""
        result = np.zeros(shape, dtype=dtype)
        return result

    def _allocate_sinobuilder_output(self):
        return self._cpu_allocate_array(self.sino_builder.output_shape, "f", name="sinos")

    def _allocate_recs(self, ny, nx):
        self.n_slices = self.gridded_radios.shape[1]
        if self.use_radio_processing_margin:
            self.n_slices -= sum(self.phase_margin[0])
        self.recs = self._allocate_array((1, ny, nx), "f", name="recs")
        self.recs_stack = self._cpu_allocate_array((self.n_slices, ny, nx), "f", name="recs_stack")

    def _reset_memory(self):
        pass

    def _get_read_dump_subregion(self):
        read_opts = self.processing_options["read_chunk"]
        if read_opts.get("process_file", None) is None:
            return None
        dump_start_z, dump_end_z = read_opts["dump_start_z"], read_opts["dump_end_z"]
        relative_start_z = self.z_min - dump_start_z
        relative_end_z = relative_start_z + self.chunk_size
        # (n_angles, n_z, n_x)
        subregion = (None, None, relative_start_z, relative_end_z, None, None)
        return subregion

    def _check_resume_from_step(self):
        if self._resume_from_step is None:
            return
        read_opts = self.processing_options["read_chunk"]
        expected_radios_shape = get_hdf5_dataset_shape(
            read_opts["process_file"],
            read_opts["process_h5_path"],
            sub_region=self._get_read_dump_subregion(),
        )
        # TODO check

    def _init_reader_finalize(self):
        """
        Method called after _init_reader
        """
        self._check_resume_from_step()

        self._compute_phase_kernel_margin()

        self._allocate_reduced_gridded_and_subset_radios()

    def _allocate_reduced_gridded_and_subset_radios(self):
        shp_h = self.chunk_reader.data.shape[-1]

        sliding_window_size = self.chunk_size
        if sliding_window_size % 2 == 0:
            sliding_window_size += 1
        sliding_window_radius = (sliding_window_size - 1) // 2

        if sliding_window_radius == 0:
            n_projs_max = (self.span_info.sunshine_ends - self.span_info.sunshine_starts).max()
        else:
            padded_starts = self.span_info.sunshine_starts
            padded_ends = self.span_info.sunshine_ends

            padded_starts = np.concatenate(
                [[padded_starts[0]] * sliding_window_radius, padded_starts, [padded_starts[-1]] * sliding_window_radius]
            )
            starts = sliding_window_view(padded_starts, sliding_window_size).min(axis=-1)

            padded_ends = np.concatenate(
                [[padded_ends[0]] * sliding_window_radius, padded_ends, [padded_ends[-1]] * sliding_window_radius]
            )

            ends = sliding_window_view(padded_ends, sliding_window_size).max(axis=-1)

            n_projs_max = (ends - starts).max()

        ((up_margin, down_margin), (left_margin, right_margin)) = self.phase_margin

        (start_x, end_x, start_z, end_z) = self.sub_region

        ## and now the gridded ones

        my_angle_step = abs(np.diff(self.span_info.projection_angles_deg).mean())
        self.n_gridded_angles = int(round(360.0 / my_angle_step))

        self.my_angles_rad = np.arange(self.n_gridded_angles) * 2 * np.pi / self.n_gridded_angles

        my_angles_deg = np.rad2deg(self.my_angles_rad)

        self.mirror_angle_relative_indexes = find_mirror_indexes(my_angles_deg)

        if "read_chunk" not in self.processing_steps:
            raise ValueError("Cannot proceed without reading data")

        r_shp_v, r_shp_h = self.whole_radio_shape

        (subr_start_x, subr_end_x, subr_start_z, subr_end_z) = self.sub_region

        subradio_shape = subr_end_z - subr_start_z, r_shp_h

        ### these radios are for diagnostic of the translations ( they will be optionally written, for being further used
        ##  by correlation techniques ). Two radios for the first two pass over the first gridded angles
        if self.diag_zpro_run:
            # 2 for the redundancy, 2 for +180 mirror
            ndiag = 2 * 2 * self.diag_zpro_run
        else:
            ndiag = 2 * 2

        self.diagnostic_searched_angles_rad_clipped = (
            (0.5 + np.arange(ndiag // 2)) * (2 * np.pi / (ndiag // 2))
        ).astype("f")

        self.diagnostic_radios = np.zeros((ndiag,) + subradio_shape, np.float32)
        self.diagnostic_weights = np.zeros((ndiag,) + subradio_shape, np.float32)
        self.diagnostic_proj_angle = np.zeros([ndiag], "f")
        self.diagnostic_zpix_transl = np.zeros([ndiag], "f")
        self.diagnostic_zmm_transl = np.zeros([ndiag], "f")

        self.diagnostic = {
            "radios": self.diagnostic_radios,
            "weights": self.diagnostic_weights,
            "angles": self.diagnostic_proj_angle,
            "zpix_transl": self.diagnostic_zpix_transl,
            "zmm_trans": self.diagnostic_zmm_transl,
            "pixel_size_mm": self.span_info.pix_size_mm,
            "searched_rad": self.diagnostic_searched_angles_rad_clipped,
        }
        ## -------
        if self.diag_zpro_run == 0:
            self.gridded_radios = np.zeros((self.n_gridded_angles,) + subradio_shape, np.float32)
            self.gridded_cumulated_weights = np.zeros((self.n_gridded_angles,) + subradio_shape, np.float32)
        else:
            # only diagnostic will be cumulated. No need to keep the full size for diagnostic runs.
            # The gridder is initialised passing also the two buffer below,
            # and the two first dimensions are used to allocate auxiliaries,
            # so we shorten only the last dimension, but this is already a good cut
            self.gridded_radios = np.zeros((self.n_gridded_angles,) + (subradio_shape[0], 2), np.float32)
            self.gridded_cumulated_weights = np.zeros((self.n_gridded_angles,) + (subradio_shape[0], 2), np.float32)

        self.radios_subset = np.zeros((self.reading_granularity,) + subradio_shape, np.float32)
        self.radios_weights_subset = np.zeros((self.reading_granularity,) + subradio_shape, np.float32)

        if not self.diag_zpro_run:
            self.radios = np.zeros(
                (self.n_gridded_angles,) + ((end_z - down_margin) - (start_z + up_margin), shp_h), np.float32
            )
        else:
            # place holder
            self.radios = np.zeros((self.n_gridded_angles,) + (1, 1), np.float32)

        self.radios_weights = np.zeros_like(self.radios)

        self.radios_slim = self._allocate_array(self._get_shape("one_sino_slim"), "f", name="radios_slim")

    def _process_finalize(self):
        """
        Method called once the pipeline has been executed
        """
        pass

    def _get_slice_start_index(self):
        return self.z_min + self._phase_margin_up

    _get_image_start_index = _get_slice_start_index

    #
    # Pipeline initialization
    #

    def _reset_diagnostics(self):
        self.diagnostic_radios[:] = 0
        self.diagnostic_weights[:] = 0
        self.diagnostic_zpix_transl[:] = 0
        self.diagnostic_zmm_transl[:] = 0
        self.diagnostic_proj_angle[:] = np.nan

    def _init_pipeline(self):
        self._get_size_of_a_raw_radio()

        self._init_reader()

        self._init_flatfield()

        self._init_double_flatfield()
        self._init_weights_field()

        self._init_ccd_corrections()
        self._init_phase()
        self._init_unsharp()
        self._init_mlog()
        self._init_sino_normalization()
        self._init_sino_builder()
        self._prepare_reconstruction()
        self._init_reconstruction()
        self._init_histogram()
        self._init_writer()
        self._configure_data_dumps()

        self._configure_regular_accumulator()

    def _set_detector_distortion_correction(self):
        if self.process_config.nabu_config["preproc"]["detector_distortion_correction"] is None:
            self.detector_corrector = None
        else:
            self.detector_corrector = DetectorDistortionProvider(
                detector_full_shape_vh=self.process_config.dataset_info.radio_dims[::-1],
                correction_type=self.process_config.nabu_config["preproc"]["detector_distortion_correction"],
                options=self.process_config.nabu_config["preproc"]["detector_distortion_correction_options"],
            )

    def _configure_regular_accumulator(self):
        ##
        # keeping these freshly numpyed objects referenced by self
        # ensures that their buffer info, conserved by c++ implementation of  GriddedAccumulator
        # will always point to existing data, which could otherwise be garbage collected by python
        #

        if self.process_config.nabu_config["preproc"]["normalize_srcurrent"]:
            self.radios_srcurrent = np.array(self.dataset_info.projections_srcurrent, "f")
            self.flats_srcurrent = np.array(self.dataset_info.flats_srcurrent, "f")
        else:
            self.radios_srcurrent = None
            self.flats_srcurrent = None

        self.regular_accumulator = GriddedAccumulator(
            gridded_radios=self.gridded_radios,
            gridded_weights=self.gridded_cumulated_weights,
            diagnostic_radios=self.diagnostic_radios,
            diagnostic_weights=self.diagnostic_weights,
            diagnostic_angles=self.diagnostic_proj_angle,
            diagnostic_zpix_transl=self.diagnostic_zpix_transl,
            diagnostic_searched_angles_rad_clipped=self.diagnostic_searched_angles_rad_clipped,
            dark=self.flatfield.get_dark(),
            flat_indexes=self.flatfield._sorted_flat_indices,
            flats=self.flatfield.flats_stack,
            weights=self.weights_field.data,
            double_flat=self.double_flatfield.data,
            diag_zpro_run=self.diag_zpro_run,
            radios_srcurrent=self.radios_srcurrent,
            flats_srcurrent=self.flats_srcurrent,
        )

        return

    def _get_size_of_a_raw_radio(self):
        """Once for all we find the shape of a radio.
        This information will be used in other parts of the code when allocating
        bunch of data holders
        """
        if "read_chunk" not in self.processing_steps:
            raise ValueError("Cannot proceed without reading data")

        options = self.processing_options["read_chunk"]

        here_a_file = next(iter(options["files"].values()))
        here_a_radio = silx.io.get_data(here_a_file)

        binning_x, binning_z = self._get_binning()
        if (binning_z, binning_x) != (1, 1):
            binning_function = get_binning_function((binning_z, binning_x))
            here_a_radio = binning_function(here_a_radio)

        self.whole_radio_shape = here_a_radio.shape
        return self.whole_radio_shape

    @use_options("read_chunk", "chunk_reader")
    def _init_reader(self):
        if "read_chunk" not in self.processing_steps:
            raise ValueError("Cannot proceed without reading data")
        options = self.processing_options["read_chunk"]

        assert options.get("process_file", None) is None, "Resume not yet implemented in helical pipeline"

        # dummy initialisation, it will be _set_subregion'ed and set_data_buffer'ed in the loops
        self.chunk_reader = ChunkReaderHelical(
            options["files"],
            sub_region=None,  # setting of subregion will be already done by calls to set_subregion
            detector_corrector=self.detector_corrector,
            convert_float=True,
            binning=options["binning"],
            dataset_subsampling=options["dataset_subsampling"],
            data_buffer=None,
            pre_allocate=True,
        )

        self._init_reader_finalize()

    @use_options("flatfield", "flatfield")
    def _init_flatfield(self, shape=None):
        if shape is None:
            shape = self._get_shape("flatfield")
        options = self.processing_options["flatfield"]

        distortion_correction = None
        if options["do_flat_distortion"]:
            self.logger.info("Flats distortion correction will be applied")
            estimation_kwargs = {}
            estimation_kwargs.update(options["flat_distortion_params"])
            estimation_kwargs["logger"] = self.logger
            distortion_correction = DistortionCorrection(
                estimation_method="fft-correlation", estimation_kwargs=estimation_kwargs, correction_method="interpn"
            )

        self.flatfield = self.FlatFieldClass(
            shape,
            flats=self.dataset_info.flats,
            darks=self.dataset_info.darks,
            radios_indices=options["projs_indices"],
            interpolation="linear",
            distortion_correction=distortion_correction,
            radios_srcurrent=options["radios_srcurrent"],
            flats_srcurrent=options["flats_srcurrent"],
            detector_corrector=self.detector_corrector,
            ## every flat will be read at a different heigth
            ### sub_region=self.sub_region,
            binning=options["binning"],
            convert_float=True,
        )

    def _get_binning(self):
        options = self.processing_options["read_chunk"]
        binning = options["binning"]
        if binning is None:
            return 1, 1
        else:
            return binning

    def _init_double_flatfield(self):
        options = self.processing_options["double_flatfield"]

        binning_x, binning_z = self._get_binning()

        result_url = None

        self.double_flatfield = None

        if options["processes_file"] not in (None, ""):
            file_path = options["processes_file"]
            data_path = (self.dataset_info.hdf5_entry or "entry") + "/double_flatfield/results/data"

            if path.exists(file_path) and (data_path in h5py.File(file_path, "r")):
                result_url = DataUrl(file_path=file_path, data_path=data_path)
                self.logger.info("Loading double flatfield from %s" % result_url.file_path())

                self.double_flatfield = self.DoubleFlatFieldClass(
                    self._get_shape("double_flatfield"),
                    result_url=result_url,
                    binning_x=binning_x,
                    binning_z=binning_z,
                    detector_corrector=self.detector_corrector,
                )

    def _init_weights_field(self):
        options = self.processing_options["double_flatfield"]
        result_url = None

        binning_x, binning_z = self.chunk_reader.get_binning()

        self.weights_field = None

        if options["processes_file"] not in (None, ""):
            file_path = options["processes_file"]
            data_path = (self.dataset_info.hdf5_entry or "entry") + "/weights_field/results/data"

            if path.exists(file_path) and (data_path in h5py.File(file_path, "r")):
                result_url = DataUrl(file_path=file_path, data_path=data_path)
                self.logger.info("Loading weights_field from %s" % result_url.file_path())

                self.weights_field = self.DoubleFlatFieldClass(
                    self._get_shape("double_flatfield"), result_url=result_url, binning_x=binning_x, binning_z=binning_z
                )

    def _init_ccd_corrections(self):
        if "ccd_correction" not in self.processing_steps:
            return

        options = self.processing_options["ccd_correction"]

        median_clip_thresh = options["median_clip_thresh"]

        self.ccd_correction = self.CCDFilterClass(
            self._get_shape("ccd_correction"), median_clip_thresh=median_clip_thresh
        )

    @use_options("phase", "phase_retrieval")
    def _init_phase(self):
        options = self.processing_options["phase"]
        # If unsharp mask follows phase retrieval, then it should be done
        # before cropping to the "inner part".
        # Otherwise, crop the data just after phase retrieval.
        if "unsharp_mask" in self.processing_steps:
            margin = None
        else:
            margin = self._phase_margin
        self.phase_retrieval = self.PaganinPhaseRetrievalClass(
            self._get_shape("phase"),
            distance=options["distance_m"],
            energy=options["energy_kev"],
            delta_beta=options["delta_beta"],
            pixel_size=options["pixel_size_m"],
            padding=options["padding_type"],
            margin=margin,
            fft_num_threads=True,  # TODO tune in advanced params of nabu config file
        )
        if self.phase_retrieval.use_fftw:
            self.logger.debug(
                "PaganinPhaseRetrieval using FFTW with %d threads" % self.phase_retrieval.fftw.num_threads
            )

    ##@use_options("unsharp_mask", "unsharp_mask")

    def _init_unsharp(self):
        if "unsharp_mask" not in self.processing_steps:
            self.unsharp_mask = None
            self.unsharp_sigma = 0.0
            self.unsharp_coeff = 0.0
            self.unsharp_method = "log"
        else:
            options = self.processing_options["unsharp_mask"]
            self.unsharp_sigma = options["unsharp_sigma"]
            self.unsharp_coeff = options["unsharp_coeff"]
            self.unsharp_method = options["unsharp_method"]

            self.unsharp_mask = self.UnsharpMaskClass(
                self._get_shape("unsharp_mask"),
                options["unsharp_sigma"],
                options["unsharp_coeff"],
                mode="reflect",
                method=options["unsharp_method"],
            )

    def _init_mlog(self):
        options = self.processing_options["take_log"]

        self.mlog = self.MLogClass(
            self._get_shape("take_log"), clip_min=options["log_min_clip"], clip_max=options["log_max_clip"]
        )

    @use_options("sino_normalization", "sino_normalization")
    def _init_sino_normalization(self):
        options = self.processing_options["sino_normalization"]
        self.sino_normalization = self.SinoNormalizationClass(
            kind=options["method"],
            radios_shape=self._get_shape("sino_normalization_slim"),
        )

    def _init_sino_builder(self):
        options = self.processing_options["reconstruction"]  ## build_sino class disappeared disappeared

        self.sino_builder = self.SinoBuilderClass(
            radios_shape=self._get_shape("build_sino"),
            rot_center=options["rotation_axis_position"],
            halftomo=False,
        )
        self._sinobuilder_copy = False
        self._sinobuilder_output = None
        self.sinos = None

    # this should be renamed, as it could be confused with _init_reconstruction. What about _get_reconstruction_array ?
    @use_options("reconstruction", "reconstruction")
    def _prepare_reconstruction(self):
        options = self.processing_options["reconstruction"]
        x_s, x_e = options["start_x"], options["end_x"]
        y_s, y_e = options["start_y"], options["end_y"]

        if not self.diag_zpro_run:
            self._rec_roi = (x_s, x_e + 1, y_s, y_e + 1)
            self._allocate_recs(y_e - y_s + 1, x_e - x_s + 1)
        else:
            ## Dummy 1x1 place holder
            self._rec_roi = (x_s, x_s + 1, y_s, y_s + 1)
            self._allocate_recs(y_s - y_s + 1, x_s - x_s + 1)

    @use_options("reconstruction", "reconstruction")
    def _init_reconstruction(self):
        options = self.processing_options["reconstruction"]

        if self.sino_builder is None:
            raise ValueError("Reconstruction cannot be done without build_sino")

        if self.FBPClass is None:
            raise ValueError("No usable FBP  module was found")

        rot_center = options["rotation_axis_position"]

        start_y, end_y, start_x, end_x = self._rec_roi

        if self.HBPClass is not None and self.process_config.nabu_config["reconstruction"]["use_hbp"]:
            fan_source_distance_meters = self.process_config.nabu_config["reconstruction"]["fan_source_distance_meters"]

            self.reconstruction_hbp = self.HBPClass(
                self._get_shape("one_sino_slim"),
                slice_shape=(end_y - start_y, end_x - start_x),
                angles=self.my_angles_rad,
                rot_center=rot_center,
                extra_options={"axis_correction": np.zeros(self.radios.shape[0], "f")},
                axis_source_meters=fan_source_distance_meters,
                voxel_size_microns=options["voxel_size_cm"][0] * 1.0e4,
                scale_factor=2.0 / options["voxel_size_cm"][0],
                clip_outer_circle=options["clip_outer_circle"],
            )

        else:
            self.reconstruction_hbp = None

        self.reconstruction = self.FBPClass(
            self._get_shape("reconstruction"),
            angles=np.zeros(self.radios.shape[0], "f"),
            rot_center=rot_center,
            filter_name=options["fbp_filter_type"],
            slice_roi=self._rec_roi,
            # slice_shape =   ( end_y-start_y,  end_x- start_x ),
            scale_factor=2.0 / options["voxel_size_cm"][0],
            padding_mode=options["padding_type"],
            extra_options={
                "scale_factor": 2.0 / options["voxel_size_cm"][0],
                "axis_correction": np.zeros(self.radios.shape[0], "f"),
                "clip_outer_circle": options["clip_outer_circle"],
            },  #  "padding_mode": options["padding_type"],         },
        )

        my_options = self.process_config.nabu_config["reconstruction"]
        if my_options["axis_to_the_center"]:
            x_s, x_ep1, y_s, y_ep1 = self._rec_roi
            off_x = -int(round((x_s + x_ep1 - 1) / 2.0 - rot_center))
            off_y = -int(round((y_s + y_ep1 - 1) / 2.0 - rot_center))
            self.reconstruction.offsets = {"x": off_x, "y": off_y}

        if options["fbp_filter_type"] is None:
            self.reconstruction.fbp = self.reconstruction.backproj

    @use_options("histogram", "histogram")
    def _init_histogram(self):
        options = self.processing_options["histogram"]
        self.histogram = self.HistogramClass(method="fixed_bins_number", num_bins=options["histogram_bins"])
        self.histo_stack = []

    @use_options("save", "writer")
    def _init_writer(self, chunk_info=None):
        options = self.processing_options["save"]
        file_prefix = options["file_prefix"]
        output_dir = path.join(options["location"], file_prefix)
        nx_info = None
        self._hdf5_output = is_hdf5_extension(options["file_format"])

        if chunk_info is not None:
            d_v, d_h = self.process_config.dataset_info.radio_dims[::-1]
            h_rels = self._get_slice_start_index() + np.arange(chunk_info.span_v[1] - chunk_info.span_v[0])
            fact_mm = self.process_config.dataset_info.pixel_size * 1.0e-3
            heights_mm = (
                fact_mm * (-self.span_info.z_pix_per_proj[0] + (d_v - 1) / 2 - h_rels) - self.span_info.z_offset_mm
            )
        else:
            heights_mm = None

        if self._hdf5_output:
            fname_start_index = None
            file_prefix += str("_%06d" % self._get_slice_start_index())
            entry = getattr(self.dataset_info.dataset_scanner, "entry", None)
            nx_info = {
                "process_name": self._get_process_name(),
                "processing_index": 0,
                "config": {
                    "processing_options": self.processing_options,
                    "nabu_config": self.process_config.nabu_config,
                },
                "entry": entry,
            }
            self._histogram_processing_index = nx_info["processing_index"] + 1
        elif options["file_format"] in ["tif", "tiff", "edf"]:
            fname_start_index = self._get_slice_start_index()
            self._histogram_processing_index = 1

        self._writer_configurator = WriterConfigurator(
            output_dir,
            file_prefix,
            file_format=options["file_format"],
            overwrite=options["overwrite"],
            start_index=fname_start_index,
            heights_above_stage_mm=heights_mm,
            logger=self.logger,
            nx_info=nx_info,
            write_histogram=("histogram" in self.processing_steps),
            histogram_entry=getattr(self.dataset_info.dataset_scanner, "entry", "entry"),
        )
        self.writer = self._writer_configurator.writer
        self._writer_exec_args = self._writer_configurator._writer_exec_args
        self._writer_exec_kwargs = self._writer_configurator._writer_exec_kwargs
        self.histogram_writer = self._writer_configurator.get_histogram_writer()

    def _apply_expand_fact(self, t):
        if t is not None:
            t = t * self.chunk_reader.dataset_subsampling
        return t

    def _expand_slice(self, subchunk_slice):
        start, stop, step = subchunk_slice.start, subchunk_slice.stop, subchunk_slice.step
        if step is None:
            step = 1

        start, stop, step = list(map(self._apply_expand_fact, [start, stop, step]))
        result_slice = slice(start, stop, step)
        return result_slice

    def _read_data_and_apply_flats(self, sub_total_prange_slice, subchunk_slice, chunk_info):
        my_integer_shifts_v = chunk_info.integer_shift_v[subchunk_slice]
        fract_complement_shifts_v = chunk_info.fract_complement_to_integer_shift_v[subchunk_slice]
        x_shifts_list = chunk_info.x_pix_per_proj[subchunk_slice]
        (subr_start_x, subr_end_x, subr_start_z, subr_end_z) = self.sub_region
        subr_start_z_list = subr_start_z - my_integer_shifts_v
        subr_end_z_list = subr_end_z - my_integer_shifts_v + 1

        self._reset_reader_subregion((None, None, subr_start_z_list.min(), subr_end_z_list.max()))

        dtasrc_start_x, dtasrc_end_x, dtasrc_start_z, dtasrc_end_z = self.trimmed_floating_subregion

        if self.diag_zpro_run:
            searched_angles = self.diagnostic_searched_angles_rad_clipped

            these_angles = chunk_info.angles_rad[subchunk_slice]
            if len(these_angles) > 1:
                # these_angles are the projection angles
                # if no diagnostic angle falls close to them we skip to the next angular subchunk
                # (here slice refers to angular slicing)
                # We like hdf5 but we that is not a reason to read them all the time, so we spare time

                a_step = abs(these_angles[1:] - these_angles[:-1]).mean()
                distance = abs(np.mod(these_angles, np.pi * 2) - searched_angles[:, None]).min()
                distance_l = abs(np.mod(these_angles, np.pi * 2) - searched_angles[:, None] - a_step).min()
                distance_h = abs(np.mod(these_angles, np.pi * 2) - searched_angles[:, None] + a_step).min()
                distance = np.array([distance, distance_h, distance_l]).min()

                if distance > 2 * a_step:
                    return

        self.chunk_reader.load_data(overwrite=True, sub_total_prange_slice=sub_total_prange_slice)
        if self.chunk_reader.dataset_subsampling > 1:
            radios_angular_range_slicing = self._expand_slice(sub_total_prange_slice)
        else:
            radios_angular_range_slicing = sub_total_prange_slice
        my_subsampled_indexes = self.chunk_reader._sorted_files_indices[radios_angular_range_slicing]
        data_raw = self.chunk_reader.data[: len(my_subsampled_indexes)]

        self.regular_accumulator.extract_preprocess_with_flats(
            subchunk_slice,
            my_subsampled_indexes,  # these are indexes pointing within the global domain sequence which is composed of darks flats radios
            chunk_info,
            np.array((subr_start_z, subr_end_z), "i"),
            np.array((dtasrc_start_z, dtasrc_end_z), "i"),
            data_raw,
            radios_angular_range_slicing,  # my_subsampled_indexes  is important in order to compare the
            # radios positions with respect to the flat position, and these position
            # are given as the sequential acquisition number which counts everything ( flats, darks, radios )
            # Insteqd, in order to access array which spans only the radios, we need to have an idea of where we are.
            # this is provided by radios_angular_range_slicing which addresses the radios domain
        )

    def binning_expanded(self, region):
        binning_x, binning_z = self.chunk_reader.get_binning()
        binnings = [binning_x] * 2 + [binning_z] * 2
        res = [None if tok is None else tok * fact for tok, fact in zip(region, binnings)]
        return res

    def _reset_reader_subregion(self, floating_subregion):
        if self._resume_from_step is None:
            binning_x, binning_z = self.chunk_reader.get_binning()

            start_x, end_x, start_z, end_z = floating_subregion
            trimmed_start_z = max(0, start_z)
            trimmed_end_z = min(self.whole_radio_shape[0], end_z)

            my_buffer_height = trimmed_end_z - trimmed_start_z

            if self.radios_buffer is None or my_buffer_height > self.safe_buffer_height:
                self.safe_buffer_height = end_z - start_z
                assert (
                    self.safe_buffer_height >= my_buffer_height
                ), "This should always be true, if not contact the developer"
                self.radios_buffer = None
                self.radios_buffer = np.zeros(
                    (self.reading_granularity + self.extra_marge_granularity,)
                    + (self.safe_buffer_height, self.whole_radio_shape[1]),
                    np.float32,
                )

            self.trimmed_floating_subregion = start_x, end_x, trimmed_start_z, trimmed_end_z

            self.chunk_reader._set_subregion(self.binning_expanded(self.trimmed_floating_subregion))
            self.chunk_reader._init_reader()
            self.chunk_reader._loaded = False

            self.chunk_reader.set_data_buffer(self.radios_buffer[:, :my_buffer_height, :], pre_allocate=False)

        else:
            message = "Resume not yet implemented in helical pipeline"
            raise RuntimeError(message)

    def _ccd_corrections(self, radios=None):
        if radios is None:
            radios = self.gridded_radios
        if hasattr(self.ccd_correction, "median_clip_correction_multiple_images"):
            self.ccd_correction.median_clip_correction_multiple_images(radios)
        else:
            _tmp_radio = self._cpu_allocate_array(radios.shape[1:], "f", name="tmp_ccdcorr_radio")
            for i in range(radios.shape[0]):
                self.ccd_correction.median_clip_correction(radios[i], output=_tmp_radio)
                radios[i][:] = _tmp_radio[:]

    def _retrieve_phase(self):
        if "unsharp_mask" in self.processing_steps:
            for i in range(self.gridded_radios.shape[0]):
                self.gridded_radios[i] = self.phase_retrieval.apply_filter(self.gridded_radios[i])
        else:
            for i in range(self.gridded_radios.shape[0]):
                self.radios[i] = self.phase_retrieval.apply_filter(self.gridded_radios[i])

    def _nophase_put_to_radios(self, target, source):
        ((up_margin, down_margin), (left_margin, right_margin)) = self.phase_margin

        zslice = slice(up_margin or None, -down_margin or None)
        xslice = slice(left_margin or None, -right_margin or None)

        for i in range(target.shape[0]):
            target[i] = source[i][zslice, xslice]

    def _apply_unsharp():
        ((up_margin, down_margin), (left_margin, right_margin)) = self._phase_margin

        zslice = slice(up_margin or None, -down_margin or None)
        xslice = slice(left_margin or None, -right_margin or None)

        for i in range(self.radios.shape[0]):
            self.radios[i] = self.unsharp_mask.unsharp(self.gridded_radios[i])[zslice, xslice]

    def _take_log(self):
        self.mlog.take_logarithm(self.radios)

    @pipeline_step("sino_normalization", "Normalizing sinograms")
    def _normalize_sinos(self, radios=None):
        if radios is None:
            radios = self.radios
        sinos = radios.transpose((1, 0, 2))
        self.sino_normalization.normalize(sinos)

    def _dump_sinogram(self, radios=None):
        if radios is None:
            radios = self.radios
        self._dump_data_to_file("sinogram", data=radios)

    @pipeline_step("sino_builder", "Building sinograms")
    def _build_sino(self):
        self.sinos = self.radios_slim

    def _filter(self):
        rot_center = self.processing_options["reconstruction"]["rotation_axis_position"]
        self.reconstruction.sino_filter.filter_sino(
            self.radios_slim,
            mirror_indexes=self.mirror_angle_relative_indexes,
            rot_center=rot_center,
            output=self.radios_slim,
        )

    def _build_sino(self):
        self.sinos = self.radios_slim

    def _reconstruct(self, sinos=None, chunk_info=None, i_slice=0):
        if sinos is None:
            sinos = self.sinos

        use_hbp = self.process_config.nabu_config["reconstruction"]["use_hbp"]

        if not use_hbp:
            if i_slice == 0:
                self.reconstruction.set_custom_angles_and_axis_corrections(
                    self.my_angles_rad, np.zeros_like(self.my_angles_rad)
                )

            self.reconstruction.backprojection(sinos, output=self.recs[0])

            self.recs[0].get(self.recs_stack[i_slice])
        else:
            if self.reconstruction_hbp is None:
                raise ValueError("You requested the hierchical backprojector but the module could not be imported")
            self.reconstruction_hbp.backprojection(sinos, output=self.recs_stack[i_slice])

    def _compute_histogram(self, data=None, i_slice=None, num_slices=None):
        if self.histogram is None:
            return

        if data is None:
            data = self.recs

        my_histo = self.histogram.compute_histogram(data.ravel())
        self.histo_stack.append(my_histo)

        if i_slice == num_slices - 1:
            self.recs_histogram = self.histogram.merge_histograms(self.histo_stack)
            self.histo_stack.clear()

    def _write_data(self, data=None):
        if data is None:
            data = self.recs_stack
        my_kw_args = copy.copy(self._writer_exec_kwargs)
        if "config" in my_kw_args:
            self.logger.info(
                "omitting config in  writer because of too slow nexus writer. Just writing the diagnostics, if any "
            )

        # diagnostic are saved here, with the Nabu mechanism for config
        self.diagnostic_zpix_transl[:] = np.interp(
            self.diagnostic_proj_angle,
            np.deg2rad(self.span_info.projection_angles_deg_internally),
            self.span_info.z_pix_per_proj,
        )
        self.diagnostic_zmm_transl[:] = self.diagnostic_zpix_transl * self.span_info.pix_size_mm

        my_kw_args["config"] = self.diagnostic

        self.writer.write(data, *self._writer_exec_args, **my_kw_args)
        self.logger.info("Wrote %s" % self.writer.get_filename())
        self._write_histogram()

    def _write_histogram(self):
        if "histogram" not in self.processing_steps:
            return
        self.logger.info("Saving histogram")
        self.histogram_writer.write(
            hist_as_2Darray(self.recs_histogram),
            self._get_process_name(kind="histogram"),
            processing_index=self._histogram_processing_index,
            config={
                "file": path.basename(self.writer.get_filename()),
                "bins": self.processing_options["histogram"]["histogram_bins"],
            },
        )

    def _dump_data_to_file(self, step_name, data=None):
        if step_name not in self._data_dump:
            return
        self.logger.info(f"DUMP step_name={step_name}")
        if data is None:
            data = self.radios
        writer = self._data_dump[step_name]
        self.logger.info("Dumping data to %s" % writer.fname)
        writer.write_data(data)

    def balance_weights(self):
        options = self.processing_options["reconstruction"]

        rot_center = options["rotation_axis_position"]

        self.radios_weights[:] = rebalance(self.radios_weights, self.my_angles_rad, rot_center)

        # When standard scans are incomplete, due to motors errors, some angular range
        #  is missing short of 360 degrees.
        # The weight accounting correctly deal with it, but still the padding
        # procedure with theta+180 data may fall on empty data
        # and this may cause problems, coming from the ramp filter,
        # in half tomo.
        # To correct this we complete with what we have at hand from the nearest
        # non empty data
        #
        to_be_filled = []
        for i in range(len(self.radios_weights) - 1, 0, -1):
            if self.radios_weights[i].sum():
                break
            to_be_filled.append(i)
        for i in to_be_filled:
            self.radios[i] = self.radios[to_be_filled[-1] - 1]

    def _post_primary_data_reduction(self, i_slice):
        """This will be used in the derived class to transfer data to gpu"""
        self.radios_slim[:] = self.radios[:, i_slice, :]

    def process_chunk(self, sub_region=None):
        self._private_process_chunk(sub_region=sub_region)
        self._process_finalize()

    def _private_process_chunk(self, sub_region=None):
        assert sub_region is not None, "sub_region argument is mandatory in helical pipeline"

        # Every chunk has its diagnostic, that is good to follow the trends in helical scans
        # or zstages
        self._reset_diagnostics()

        self.set_subregion(sub_region)

        (subr_start_x, subr_end_x, subr_start_z, subr_end_z) = self.sub_region

        span_v = subr_start_z + self._phase_margin_up, subr_end_z - self._phase_margin_down

        chunk_info = self.span_info.get_chunk_info(span_v)

        self._reset_memory()
        self._init_writer(chunk_info)

        self._configure_data_dumps()
        proj_num_start, proj_num_end = chunk_info.angle_index_span

        n_granularity = self.reading_granularity
        pnum_start_list = list(np.arange(proj_num_start, proj_num_end, n_granularity))
        pnum_end_list = pnum_start_list[1:] + [proj_num_end]

        my_first_pnum = proj_num_start

        if self.diag_zpro_run == 0:
            # It may seem anodine, but setting a huge vector to zero
            # takes time.
            # In diagnostic collection mode we can spare it. On the other hand nothing has would be allocated for the data
            # in such case
            self.gridded_cumulated_weights[:] = 0
            self.gridded_radios[:] = 0

        for pnum_start, pnum_end in zip(pnum_start_list, pnum_end_list):
            start_in_chunk = pnum_start - my_first_pnum
            end_in_chunk = pnum_end - my_first_pnum

            self._read_data_and_apply_flats(
                slice(pnum_start, pnum_end), slice(start_in_chunk, end_in_chunk), chunk_info
            )

        if not self.diag_zpro_run:
            # when we collect diagnostics  we dont collect all the data
            # so there would be nothing to process here

            self.gridded_radios[:] /= self.gridded_cumulated_weights

            self.correct_for_missing_angles()

            linea = self.gridded_cumulated_weights.sum(axis=(1, 2))
            i_zero_list = np.where(linea == 0)[0]
            for i_zero in i_zero_list:
                if i_zero > linea.shape[0] // 2:
                    direction = -1
                else:
                    direction = 1
                i = i_zero
                while ((i >= 0 and direction == -1) or ((i < linea.shape[0] - 1) and direction == 1)) and linea[i] == 0:
                    i += direction
                if linea[i]:
                    self.gridded_radios[i_zero] = self.gridded_radios[i]
                    self.gridded_cumulated_weights[i_zero] = self.gridded_cumulated_weights[i]

            if "flatfield" in self._data_dump:
                paganin_margin = self._phase_margin_up
                if paganin_margin:
                    data_to_dump = self.gridded_radios[:, paganin_margin:-paganin_margin, :]
                else:
                    data_to_dump = self.gridded_radios
                self._dump_data_to_file("flatfield", data_to_dump)
                if self.process_config.nabu_config["pipeline"]["skip_after_flatfield_dump"]:
                    return

            if "ccd_correction" in self.processing_steps:
                self._ccd_corrections()

            if cxx_paganin is None:
                if ("phase" in self.processing_steps) or ("unsharp_mask" in self.processing_steps):
                    self._retrieve_phase()
                    if "unsharp_mask" in self.processing_steps:
                        self._apply_unsharp()
                else:
                    self._nophase_put_to_radios(self.radios, self.gridded_radios)
            else:
                if "phase" in self.processing_steps:
                    pr = self.phase_retrieval
                    paganin_l_micron = math.sqrt(pr.wavelength_micron * pr.distance_micron * pr.delta_beta * math.pi)
                    cxx_paganin.paganin_pyhst(
                        data_raw=self.gridded_radios,
                        output=self.radios,
                        num_of_threads=-1,
                        paganin_marge=self._phase_margin_up,
                        paganin_l_micron=paganin_l_micron / pr.pixel_size_micron,
                        image_pixel_size_y=1.0,
                        image_pixel_size_x=1.0,
                        unsharp_sigma=self.unsharp_sigma,
                        unsharp_coeff=self.unsharp_coeff,
                        unsharp_LoG=int((self.unsharp_method == "log")),
                    )
                else:
                    self._nophase_put_to_radios(self.radios, self.gridded_radios)

            self.logger.info(" LOG ")
            self._nophase_put_to_radios(self.radios_weights, self.gridded_cumulated_weights)

            # print( " processing steps ", self.processing_steps )
            # ['read_chunk', 'flatfield', 'double_flatfield', 'take_log', 'reconstruction', 'save']

            if "take_log" in self.processing_steps:
                self._take_log()

            self.logger.info(" BALANCE ")

            self.balance_weights()

            num_slices = self.radios.shape[1]

            self.logger.info(" NORMALIZE")
            self._normalize_sinos()
            self._dump_sinogram()

        if "reconstruction" in self.processing_steps:
            if not self.diag_zpro_run:
                # otherwise, when collecting diagnostic, we are not interested in the remaining steps
                # on the other hand there would be nothing to process because only diagnostics have been collected
                for i_slice in range(num_slices):
                    self._post_primary_data_reduction(i_slice)  # charge on self.radios_slim

                    self._filter()

                    self.apply_weights(i_slice)

                    self._build_sino()

                    self._reconstruct(chunk_info=chunk_info, i_slice=i_slice)

                    self._compute_histogram(i_slice=i_slice, num_slices=num_slices)

            self._write_data()

    def apply_weights(self, i_slice):
        """radios_slim is on gpu"""
        n_provided_angles = self.radios_slim.shape[0]

        for first_angle_index in range(0, n_provided_angles, self.num_weight_radios_per_app):
            end_angle_index = min(n_provided_angles, first_angle_index + self.num_weight_radios_per_app)
            self._d_radios_weights[: end_angle_index - first_angle_index].set(
                self.radios_weights[first_angle_index:end_angle_index, i_slice]
            )
            self.radios_slim[first_angle_index:end_angle_index] *= self._d_radios_weights[
                : end_angle_index - first_angle_index
            ]

    def correct_for_missing_angles(self):
        """For non helical scan, the rotation is often incomplete ( < 360)
        here we complement the missing angles
        """
        linea = self.gridded_cumulated_weights.sum(axis=(1, 2))
        i_zero_list = np.where(linea == 0)[0]
        for i_zero in i_zero_list:
            if i_zero > linea.shape[0] // 2:
                direction = -1
            else:
                direction = 1
            i = i_zero
            while ((i >= 0 and direction == -1) or ((i < linea.shape[0] - 1) and direction == 1)) and linea[i] == 0:
                i += direction
            if linea[i]:
                self.gridded_radios[i_zero] = self.gridded_radios[i]
                self.gridded_cumulated_weights[i_zero] = self.gridded_cumulated_weights[i]

    @classmethod
    def estimate_required_memory(
        cls, process_config, reading_granularity=None, chunk_size=None, margin_v=0, span_info=None, diag_zpro_run=0
    ):
        """
        Estimate the memory (RAM) needed for a reconstruction.

        Parameters
        -----------
        process_config: `ProcessConfig` object
            Data structure with the processing configuration
        chunk_size: int, optional
            Size of a "radios chunk", i.e "delta z". A radios chunk is a 3D array of shape (n_angles, chunk_size, n_x)
            If set to None, then chunk_size = n_z

        Notes
        -----
        It seems that Cuda does not allow allocating and/or transferring more than 16384 MiB (17.18 GB).
        If warn_from_GB is not None, then the result is in the form (estimated_memory_GB, warning)
        where warning is a boolean indicating whether memory allocation/transfer might be problematic.
        """
        dataset = process_config.dataset_info
        nabu_config = process_config.nabu_config
        processing_steps = process_config.processing_steps
        Nx, Ny = dataset.radio_dims

        total_memory_needed = 0

        # Read data
        # ----------

        # gridded part
        tmp_angles_deg = np.rad2deg(process_config.processing_options["reconstruction"]["angles"])
        tmp_my_angle_step = abs(np.diff(tmp_angles_deg).mean())

        my_angle_step = abs(np.diff(span_info.projection_angles_deg).mean())
        n_gridded_angles = int(round(360.0 / my_angle_step))

        binning_z = nabu_config["dataset"]["binning_z"]
        projections_subsampling = nabu_config["dataset"]["projections_subsampling"]

        if not diag_zpro_run:
            # the gridded target
            total_memory_needed += Nx * (2 * margin_v + chunk_size) * n_gridded_angles * 4

            # the gridded weights
            total_memory_needed += Nx * (2 * margin_v + chunk_size) * n_gridded_angles * 4

        # the read grain
        total_memory_needed += (
            (reading_granularity + cls.extra_marge_granularity) * (2 * margin_v + chunk_size + 2) * Nx * 4
        )

        total_memory_needed += (
            (reading_granularity + cls.extra_marge_granularity) * (2 * margin_v + chunk_size + 2) * Nx * 4
        )

        # the preprocessed radios, their weigth and the buffer used for balancing ( total of three buffer of the same size plus mask plus temporary)
        total_memory_needed += 5 * (Nx * (chunk_size) * n_gridded_angles) * 4

        if "flatfield" in processing_steps:
            # Flat-field is done in-place, but still need to load darks/flats
            n_darks = len(dataset.darks)
            n_flats = len(dataset.flats)
            darks_size = n_darks * Nx * (2 * margin_v + chunk_size) * 2  # uint16
            flats_size = n_flats * Nx * (2 * margin_v + chunk_size) * 4  # f32
            total_memory_needed += darks_size + flats_size

        if "ccd_correction" in processing_steps:
            total_memory_needed += Nx * (2 * margin_v + chunk_size) * 4

        # Phase retrieval
        # ---------------
        if "phase" in processing_steps:
            # Phase retrieval is done image-wise, so near in-place, but needs to
            # allocate some images, fft plans, and so on
            Nx_p = get_next_power(2 * Nx)
            Ny_p = get_next_power(2 * (2 * margin_v + chunk_size))
            img_size_real = 2 * 4 * Nx_p * Ny_p
            img_size_cplx = 2 * 8 * ((Nx_p * Ny_p) // 2 + 1)
            total_memory_needed += 2 * img_size_real + 3 * img_size_cplx

        # Reconstruction
        # ---------------
        reconstructed_volume_size = 0
        if "reconstruction" in processing_steps and not diag_zpro_run:
            ##  radios_slim is used to process one slice at once, It will be on the gpu
            ##  and cannot be reduced further, therefore no need to estimate it.
            ##  Either it passes or it does not.
            #### if radios_and_sinos:
            ####     togtal_memory_needed += data_volume_size  # radios + sinos

            rec_config = process_config.processing_options["reconstruction"]

            Nx_rec = rec_config["end_x"] - rec_config["start_x"] + 1
            Ny_rec = rec_config["end_y"] - rec_config["start_y"] + 1

            Nz_rec = chunk_size // binning_z

            ## the volume is used to reconstruct for each chunk
            reconstructed_volume_size = Nx_rec * Ny_rec * Nz_rec * 4  # float32
            total_memory_needed += reconstructed_volume_size

        return total_memory_needed


# target_central_slicer, source_central_slicer = overlap_logic(   subr_start_z, subr_end_z, dtasrc_start_z, dtasrcs_end_z  )
def overlap_logic(subr_start_z, subr_end_z, dtasrc_start_z, dtasrc_end_z):
    """determines the useful lines which can be transferred from the dtasrc_start_z:dtasrc_end_z
    range targeting the range  subr_start_z: subr_end_z ..................

    """

    t_h = subr_end_z - subr_start_z
    s_h = dtasrc_end_z - dtasrc_start_z

    my_start = max(0, dtasrc_start_z - subr_start_z)
    my_end = min(t_h, dtasrc_end_z - subr_start_z)

    if my_start >= my_end:
        return None, None

    target_central_slicer = slice(my_start, my_end)

    my_start = max(0, subr_start_z - dtasrc_start_z)
    my_end = min(s_h, subr_end_z - dtasrc_start_z)

    assert my_start < my_end, "Overlap_logic logic error"

    dtasrc_central_slicer = slice(my_start, my_end)

    return target_central_slicer, dtasrc_central_slicer


def padding_logic(subr_start_z, subr_end_z, dtasrc_start_z, dtasrc_end_z):
    """.......... and the missing ranges which possibly could be obtained by extension padding"""
    t_h = subr_end_z - subr_start_z
    s_h = dtasrc_end_z - dtasrc_start_z

    if dtasrc_start_z <= subr_start_z:
        target_lower_padding = None
    else:
        target_lower_padding = slice(0, dtasrc_start_z - subr_start_z)

    if dtasrc_end_z >= subr_end_z:
        target_upper_padding = None
    else:
        target_upper_padding = slice(dtasrc_end_z - subr_end_z, None)

    return target_lower_padding, target_upper_padding


def _fill_in_chunk_by_shift_crop_data(
    data_target,
    data_read,
    fract_shit,
    my_subr_start_z,
    my_subr_end_z,
    dtasrc_start_z,
    dtasrc_end_z,
    x_shift=0.0,
    extension_padding=True,
):
    """given a freshly read cube of data, it dispatches every slice to its proper vertical  position and proper radio by shifting, cropping, and extending if necessary"""
    data_read_precisely_shifted = nd.interpolation.shift(data_read, (-fract_shit, x_shift), order=1, mode="nearest")[
        :-1
    ]

    target_central_slicer, dtasrc_central_slicer = overlap_logic(
        my_subr_start_z, my_subr_end_z - 1, dtasrc_start_z, dtasrc_end_z - 1
    )

    if None not in [target_central_slicer, dtasrc_central_slicer]:
        data_target[target_central_slicer] = data_read_precisely_shifted[dtasrc_central_slicer]

    target_lower_slicer, target_upper_slicer = padding_logic(
        my_subr_start_z, my_subr_end_z - 1, dtasrc_start_z, dtasrc_end_z - 1
    )

    if extension_padding:
        if target_lower_slicer is not None:
            data_target[target_lower_slicer] = data_read_precisely_shifted[0]
        if target_upper_slicer is not None:
            data_target[target_upper_slicer] = data_read_precisely_shifted[-1]
    else:
        if target_lower_slicer is not None:
            data_target[target_lower_slicer] = 1.0e-6
        if target_upper_slicer is not None:
            data_target[target_upper_slicer] = 1.0e-6


def shift(arr, shift, fill_value=0.0):
    """trivial horizontal shift.
    Contrarily to scipy.ndimage.interpolation.shift, this shift does not cut the tails abruptly, but by interpolation
    """
    result = np.zeros_like(arr)

    num1 = int(math.floor(shift))
    num2 = num1 + 1
    partition = shift - num1

    for num, factor in zip([num1, num2], [(1 - partition), partition]):
        if num > 0:
            result[:, :num] += fill_value * factor
            result[:, num:] += arr[:, :-num] * factor
        elif num < 0:
            result[:, num:] += fill_value * factor
            result[:, :num] += arr[:, -num:] * factor
        else:
            result[:] += arr * factor

    return result


def rebalance(radios_weights, angles, ax_pos):
    """rebalance the  weights,  within groups of equivalent (up to multiple of 180), data pixels"""
    balanced = np.zeros_like(radios_weights)
    n_span = int(math.ceil(angles[-1] - angles[0]) / np.pi)
    center = (radios_weights.shape[-1] - 1) / 2
    nloop = balanced.shape[0]

    for i in range(nloop):
        w_res = balanced[i]
        angle = angles[i]

        for i_half_turn in range(-n_span - 1, n_span + 2):
            if i_half_turn == 0:
                w_res[:] += radios_weights[i]
                continue

            shifted_angle = angle + i_half_turn * np.pi

            insertion_index = np.searchsorted(angles, shifted_angle)

            if insertion_index in [0, angles.shape[0]]:
                if insertion_index == 0:
                    continue
                else:
                    if shifted_angle > 2 * np.pi:
                        continue
                    myimage = radios_weights[-1]
            else:
                partition = (shifted_angle - angles[insertion_index - 1]) / (
                    angles[insertion_index] - angles[insertion_index - 1]
                )
                myimage = (1.0 - partition) * radios_weights[insertion_index - 1] + partition * radios_weights[
                    insertion_index
                ]

            if i_half_turn % 2 == 0:
                w_res[:] += myimage
            else:
                myimage = np.fliplr(myimage)
                w_res[:] += shift(myimage, (2 * ax_pos - 2 * center))

    mask = np.equal(0, radios_weights)
    balanced[:] = radios_weights / balanced
    balanced[mask] = 0
    return balanced
