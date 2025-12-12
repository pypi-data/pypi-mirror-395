from os.path import join, isfile, dirname
from math import ceil
from time import time
import numpy as np
import copy

from nabu.utils import first_generator_item
from ...resources.logger import LoggerOrPrint
from ...io.writer import merge_hdf5_files
from ...cuda.utils import collect_cuda_gpus

try:
    import nabuxx

    SpanStrategy = nabuxx.span_strategy.SpanStrategy
except:
    logger_tmp = LoggerOrPrint(None)
    logger_tmp.info("Nabuxx not available. Loading python implementation for SpanStrategy")
    from .span_strategy import SpanStrategy

from .helical_chunked_regridded_cuda import CudaHelicalChunkedRegriddedPipeline

from ..fullfield.reconstruction import FullFieldReconstructor

avail_gpus = collect_cuda_gpus() or {}


class HelicalReconstructorRegridded:
    """
    A class for obtaining a full-volume reconstructions from helical-scan datasets.
    """

    _pipeline_cls = CudaHelicalChunkedRegriddedPipeline
    _process_name = "reconstruction"
    _pipeline_mode = "helical"

    reading_granularity = 100
    """ The data angular span which needs to be read for a reconstruction is read step by step,
        reading each time a maximum of reading_granularity radios, and doing the preprocessing
        till phase retrieval for each of these  angular groups
    """

    def __init__(self, process_config, logger=None, extra_options=None, cuda_options=None):
        """
        Initialize a LocalReconstruction object.
        This class is used for managing pipelines

        Parameters
        ----------
        process_config: ProcessConfig object
            Data structure with process configuration
        logger: Logger, optional
            logging object
        extra_options: dict, optional
            Dictionary with advanced options. Please see 'Other parameters' below
        cuda_options: dict, optional
            Dictionary with cuda options passed to `nabu.cuda.processing.CudaProcessing`

        Other Parameters
        -----------------
        Advanced options can be passed in the 'extra_options' dictionary. These can be:

           - "gpu_mem_fraction": 0.9,
           - "cpu_mem_fraction": 0.9,
           - "use_phase_margin": True,
           - "max_chunk_size": None,
           - "phase_margin": None,
           - "dry_run": 0,
           - "diag_zpro_run": 0,
        """
        self.logger = LoggerOrPrint(logger)
        self.process_config = process_config
        self._set_extra_options(extra_options)
        self._get_resources()

        ### intrication problem: this is used in fullfield's compute_margin to clamp the margin but not used by the present pipeline
        ### Set it to a big number that will never clamp
        self.n_z = 10000000  # a big number
        self.n_x = 10000000  # a big number
        ###
        self._compute_margin()
        # self._margin_v, self._margin_h = self._compute_phase_margin()

        self._setup_span_info()
        self._compute_max_chunk_size()
        self._get_reconstruction_range()

        self._build_tasks()
        self.pipeline = None
        self.cuda_options = cuda_options

    def _set_extra_options(self, extra_options):
        if extra_options is None:
            extra_options = {}
        advanced_options = {
            "gpu_mem_fraction": 0.9,
            "cpu_mem_fraction": 0.9,
            "use_phase_margin": True,
            "max_chunk_size": None,
            "phase_margin": None,
            "dry_run": 0,
            "diag_zpro_run": 0,
        }
        advanced_options.update(extra_options)
        self.extra_options = advanced_options
        self.gpu_mem_fraction = self.extra_options["gpu_mem_fraction"]
        self.cpu_mem_fraction = self.extra_options["cpu_mem_fraction"]
        self.use_phase_margin = self.extra_options["use_phase_margin"]

        self.dry_run = self.extra_options["dry_run"]
        self.diag_zpro_run = self.extra_options["diag_zpro_run"]

        self._do_histograms = self.process_config.nabu_config["postproc"]["output_histogram"]

        if self.diag_zpro_run:
            self.process_config.processing_options.get("phase", None)
            self._do_histograms = False
            self.reading_granularity = 10

        self._histogram_merged = False
        self._span_info = None

    def _get_reconstruction_range(self):
        rec_cfg = self.process_config.nabu_config["reconstruction"]
        self.z_min = rec_cfg["start_z"]
        self.z_max = rec_cfg["end_z"] + 1
        z_fract_min = rec_cfg["start_z_fract"]
        z_fract_max = rec_cfg["end_z_fract"]
        z_min_mm = rec_cfg["start_z_mm"]
        z_max_mm = rec_cfg["end_z_mm"]

        if z_min_mm != 0.0 or z_max_mm != 0.0:
            z_min_mm += self.z_offset_mm
            z_max_mm += self.z_offset_mm

            d_v, d_h = self.process_config.dataset_info.radio_dims[::-1]

            z_start, z_end = (self._span_info.get_doable_span()).view_heights_minmax
            z_end += 1

            h_s = np.arange(z_start, z_end)
            fact_mm = self.process_config.dataset_info.pixel_size * 1.0e-3
            z_mm_s = fact_mm * (-self._span_info.z_pix_per_proj[0] + (d_v - 1) / 2 - h_s)

            self.z_min = 0
            self.z_max = len(z_mm_s)

            if z_mm_s[-1] > z_mm_s[0]:
                for i in range(len(z_mm_s) - 1):
                    if (z_min_mm - z_mm_s[i]) * (z_min_mm - z_mm_s[i + 1]) <= 0:
                        self.z_min = i
                        break
                for i in range(len(z_mm_s) - 1):
                    if (z_max_mm - z_mm_s[i]) * (z_max_mm - z_mm_s[i]) <= 0:
                        self.z_max = i + 1
                        break
            else:
                for i in range(len(z_mm_s) - 1):
                    if (z_max_mm - z_mm_s[i]) * (z_max_mm - z_mm_s[i + 1]) <= 0:
                        self.z_max = len(z_mm_s) - 2 - i
                        break
                for i in range(len(z_mm_s) - 1):
                    if (z_min_mm - z_mm_s[i]) * (z_min_mm - z_mm_s[i + 1]) <= 0:
                        self.z_min = len(z_mm_s) - 1 - i
                        break
        elif z_fract_min != 0.0 or z_fract_max != 0.0:
            z_start, z_max = (self._span_info.get_doable_span()).view_heights_minmax

            # the meaming of z_min and z_max is: position in slices units from the
            # first available slice and in the direction of the scan
            self.z_min = round(z_start * (0 - z_fract_min) + z_max * z_fract_min)
            self.z_max = round(z_start * (0 - z_fract_max) + z_max * z_fract_max) + 1

    def _compute_translations_margin(self):
        return 0, 0

    def _compute_cone_overlap(self):
        return 0, 0

    _get_resources = FullFieldReconstructor._get_resources
    _get_memory = FullFieldReconstructor._get_memory
    _get_gpu = FullFieldReconstructor._get_gpu
    _compute_phase_margin = FullFieldReconstructor._compute_phase_margin
    _compute_margin = FullFieldReconstructor._compute_margin
    _compute_unsharp_margin = FullFieldReconstructor._compute_unsharp_margin
    _print_tasks = FullFieldReconstructor._print_tasks
    _instantiate_pipeline_if_necessary = FullFieldReconstructor._instantiate_pipeline_if_necessary
    _destroy_pipeline = FullFieldReconstructor._destroy_pipeline

    _give_progress_info = FullFieldReconstructor._give_progress_info
    get_relative_files = FullFieldReconstructor.get_relative_files
    merge_histograms = FullFieldReconstructor.merge_histograms
    merge_data_dumps = FullFieldReconstructor.merge_data_dumps
    _get_chunk_length = FullFieldReconstructor._get_chunk_length

    # redefined here, and with self, otherwise @static and inheritance gives "takes 1 positional argument but 2 were given"
    # when called from inside the inherite class
    def _get_delta_z(self, task):
        return task["sub_region"][1] - task["sub_region"][0]

    def _get_task_key(self):
        """
        Get the 'key' (number) associated to the current task/pipeline
        """
        return self.pipeline.sub_region[-2:]

    # Gpu required memory size does not depend on the number of slices
    def _compute_max_chunk_size(self):
        cpu_mem = self.resources["mem_avail_GB"] * self.cpu_mem_fraction

        user_max_chunk_size = self.extra_options["max_chunk_size"]

        if self.diag_zpro_run:
            if user_max_chunk_size is not None:
                user_max_chunk_size = min(
                    user_max_chunk_size, max(self.process_config.dataset_info.radio_dims[1] // 4, 10)
                )
            else:
                user_max_chunk_size = max(self.process_config.dataset_info.radio_dims[1] // 4, 10)

        self.cpu_max_chunk_size = self.estimate_chunk_size(
            cpu_mem, self.process_config, chunk_step=1, user_max_chunk_size=user_max_chunk_size
        )

        if user_max_chunk_size is not None:
            self.cpu_max_chunk_size = min(self.cpu_max_chunk_size, user_max_chunk_size)

        self.user_slices_at_once = self.cpu_max_chunk_size

    # cannot use the estimate_chunk_size from computations.py beacause it has the  estimate_required_memory hard-coded
    def estimate_chunk_size(self, available_memory_GB, process_config, chunk_step=1, user_max_chunk_size=None):
        """
        Estimate the maximum chunk size given an available amount of memory.

        Parameters
        -----------
        available_memory_GB: float
            available memory in Giga Bytes (GB - not GiB !).
        process_config: ProcessConfig
            ProcessConfig object
        """
        chunk_size = chunk_step
        radios_and_sinos = False
        if (
            "reconstruction" in process_config.processing_steps
            and process_config.processing_options["reconstruction"]["enable_halftomo"]
        ):
            radios_and_sinos = True  # noqa: F841

        # max_dz = process_config.dataset_info.radio_dims[1]
        chunk_size = chunk_step
        last_good_chunk_size = chunk_size
        while True:
            required_mem = self._pipeline_cls.estimate_required_memory(
                process_config,
                chunk_size=chunk_size,
                reading_granularity=self.reading_granularity,
                margin_v=self._margin_v,
                span_info=self._span_info,
                diag_zpro_run=self.diag_zpro_run,
            )

            required_mem_GB = required_mem / 1e9
            if required_mem_GB > available_memory_GB:
                break
            last_good_chunk_size = chunk_size

            if user_max_chunk_size is not None and chunk_size > user_max_chunk_size:
                last_good_chunk_size = user_max_chunk_size
                break
            chunk_size += chunk_step

        return last_good_chunk_size

    # different because of dry_run
    def _build_tasks(self):
        if self.dry_run:
            self.tasks = []
        else:
            self._compute_volume_chunks()

    # this is very different
    def _compute_volume_chunks(self):
        margin_v = self._margin_v
        # self._margin_far_up = min(margin_v, self.z_min)
        # self._margin_far_down = min(margin_v, n_z - (self.z_max + 1))

        ## It will be the reading process which pads
        self._margin_far_up = margin_v
        self._margin_far_down = margin_v

        # | margin_up |     n_slices    |  margin_down |
        # |-----------|-----------------|--------------|
        # |----------------------------------------------------|
        #                    delta_z

        n_slices = self.user_slices_at_once

        z_start, z_end = (self._span_info.get_doable_span()).view_heights_minmax
        z_end += 1

        if (self.z_min, self.z_max) == (0, 0):
            self.z_min, self.z_max = z_start, z_end
            my_z_min = z_start
            my_z_end = z_end
        else:
            if self.z_max <= self.z_min:
                message = f"""" The input file provide start_z end_z {self.z_min,self.z_max}
                but it is necessary that  start_z < end_z
                """
                raise ValueError(message)

            if self._span_info.z_pix_per_proj[-1] >= self._span_info.z_pix_per_proj[0]:
                my_z_min = z_start + self.z_min
                my_z_end = z_start + self.z_max
            else:
                my_z_min = z_end - self.z_max
                my_z_end = z_end - self.z_min

        my_z_min = max(z_start, my_z_min)
        my_z_end = min(z_end, my_z_end)

        print("my_z_min my_z_end ", my_z_min, my_z_end)
        if my_z_min >= my_z_end:
            message = f""" The requested vertical span, after translation to absolute doable heights would be {my_z_min, my_z_end}
            is not  doable (start>=end).
            Scans are often shorter than expected ThereFore :  CONSIDER TO INCREASE angular_tolerance_steps
            """
            raise ValueError(message)

        # if my_z_min != self.z_min or my_z_end != self.z_max:
        #     message = f""" The requested vertical span given by self.z_min, self.z_max+1 ={self.z_min, self.z_max}
        #     is not withing the doable span which is {z_start, z_end}
        #     """
        #     raise ValueError(message)

        tasks = []
        n_stages = ceil((my_z_end - my_z_min) / n_slices)

        curr_z_min = my_z_min
        curr_z_max = my_z_min + n_slices

        for i in range(n_stages):
            if curr_z_max >= my_z_end:
                curr_z_max = my_z_end
            margin_down = margin_v
            margin_up = margin_v

            tasks.append(
                {
                    "sub_region": (curr_z_min - margin_up, curr_z_max + margin_down),
                    "phase_margin": ((margin_up, margin_down), (0, 0)),
                }
            )
            if curr_z_max == my_z_end:
                # No need for further tasks
                break

            curr_z_min += n_slices
            curr_z_max += n_slices

        ##
        ##
        ###########################################################################################

        self.tasks = tasks
        self.n_slices = n_slices
        self._print_tasks()

    def _setup_span_info(self):
        """We create here an instance of SpanStrategy class for helical scans.
        This class do all the accounting for the doable slices, giving for each the useful angle, the  shifts ..
        """

        # projections_subsampling = self.process_config.dataset_info.projections_subsampling
        projections_subsampling = self.process_config.nabu_config["dataset"]["projections_subsampling"]

        radio_shape = self.process_config.dataset_info.radio_dims[::-1]
        dz_per_proj = self.process_config.nabu_config["reconstruction"]["dz_per_proj"]
        z_per_proj = self.process_config.dataset_info.z_per_proj
        dx_per_proj = self.process_config.nabu_config["reconstruction"]["dx_per_proj"]
        x_per_proj = self.process_config.dataset_info.x_per_proj

        tot_num_images = len(self.process_config.processing_options["read_chunk"]["files"]) // projections_subsampling

        if z_per_proj is not None:
            z_per_proj = np.array(z_per_proj)
            self.logger.info(" z_per_proj has been explicitely provided")

            if len(z_per_proj) != tot_num_images:
                message = f""" The provided array z_per_proj, which has length {len(z_per_proj)} must
                match in lenght the number of radios which is {tot_num_images}
                """
                raise ValueError(message)
        else:
            z_per_proj = self.process_config.dataset_info.z_translation
            if dz_per_proj is not None:
                self.logger.info("correcting  vertical displacement by provided screw rate dz_per_proj")
                z_per_proj += np.arange(tot_num_images) * dz_per_proj

        if x_per_proj is not None:
            x_per_proj = np.array(x_per_proj)
            self.logger.info(" x_per_proj has been explicitely provided")

            if len(x_per_proj) != tot_num_images:
                message = f""" The provided array x_per_proj, which has length {len(x_per_proj)} must
                match in lenght the number of radios which is {tot_num_images}
                """
                raise ValueError(message)
        else:
            x_per_proj = self.process_config.dataset_info.x_translation
            if dx_per_proj is not None:
                self.logger.info("correcting  vertical displacement by provided screw rate dx_per_proj")
                x_per_proj += np.arange(tot_num_images) * dx_per_proj

        x_per_proj = x_per_proj - x_per_proj[0]
        self.z_offset_mm = z_per_proj[0] * self.process_config.dataset_info.pixel_size * 1.0e-3  # micron to mm
        z_per_proj = z_per_proj - z_per_proj[0]

        binning = self.process_config.nabu_config["dataset"]["binning"]
        if binning is not None:
            if np.isscalar(binning):
                binning = (binning, binning)
            binning_x, binning_z = binning

            x_per_proj = x_per_proj / binning_x
            z_per_proj = z_per_proj / binning_z

        x_per_proj = projections_subsampling * x_per_proj
        z_per_proj = projections_subsampling * z_per_proj

        angles_rad = self.process_config.processing_options["reconstruction"]["angles"]
        angles_rad = np.unwrap(angles_rad)
        angles_deg = np.rad2deg(angles_rad)

        redundancy_angle_deg = self.process_config.nabu_config["reconstruction"]["redundancy_angle_deg"]
        # do_helical_half_tomo = self.process_config.nabu_config["reconstruction"]["helical_halftomo"]

        self.logger.info("Creating SpanStrategy object for helical ")
        t0 = time()

        self._span_info = SpanStrategy(
            z_offset_mm=self.z_offset_mm,
            z_pix_per_proj=z_per_proj,
            x_pix_per_proj=x_per_proj,
            detector_shape_vh=radio_shape,
            phase_margin_pix=self._margin_v,
            projection_angles_deg=angles_deg,
            pixel_size_mm=self.process_config.dataset_info.pixel_size * 1.0e-3,  # micron to mm
            require_redundancy=(redundancy_angle_deg > 0),
            angular_tolerance_steps=self.process_config.nabu_config["reconstruction"]["angular_tolerance_steps"],
        )

        duration = time() - t0
        self.logger.info(f"Creating SpanStrategy object for helical in {duration} seconds")
        if self.dry_run:
            info_string = self._span_info.get_informative_string()
            print(" Informations about the doable vertical span")
            print(info_string)
            return

    def _instantiate_pipeline(self, task):
        self.logger.debug("Creating a new pipeline object")
        args = [self.process_config, task["sub_region"]]

        # dz = self._get_delta_z(task)

        pipeline = self._pipeline_cls(
            *args,
            logger=self.logger,
            phase_margin=task["phase_margin"],
            reading_granularity=self.reading_granularity,
            span_info=self._span_info,
            diag_zpro_run=self.diag_zpro_run,
            # cuda_options=self.cuda_options
        )

        self.pipeline = pipeline

    # kept  to save diagnostic
    def _process_task(self, task):
        self.pipeline.process_chunk(sub_region=task["sub_region"])

        key = len(list(self.diagnostic_per_chunk.keys()))

        self.diagnostic_per_chunk[key] = copy.deepcopy(self.pipeline.diagnostic)

    # kept for diagnostic and dry run
    def reconstruct(self):
        self._print_tasks()
        self.diagnostic_per_chunk = {}
        tasks = self.tasks
        self.results = {}
        self._histograms = {}
        self._data_dumps = {}
        prev_task = None
        for task in tasks:
            if prev_task is None:
                prev_task = task
            self._give_progress_info(task)
            self._instantiate_pipeline_if_necessary(task, prev_task)

            if self.dry_run:
                info_string = self._span_info.get_informative_string()
                print(" SPAN_INFO informations ")
                print(info_string)
                return

            self._process_task(task)
            if self.pipeline.writer is not None:
                task_key = self._get_task_key()
                self.results[task_key] = self.pipeline.writer.fname
                if self.pipeline.histogram_writer is not None:  # self._do_histograms
                    self._histograms[task_key] = self.pipeline.histogram_writer.fname
                if len(self.pipeline._data_dump) > 0:
                    self._data_dumps[task_key] = {}
                    for step_name, writer in self.pipeline._data_dump.items():
                        self._data_dumps[task_key][step_name] = writer.fname
            prev_task = task

    ## kept in order to speed it up by omitting the super  slow python writing
    ## of thousand of unused urls
    def merge_hdf5_reconstructions(
        self,
        output_file=None,
        prefix=None,
        files=None,
        process_name=None,
        axis=0,
        merge_histograms=True,
        output_dir=None,
    ):
        """
        Merge existing hdf5 files by creating a HDF5 virtual dataset.

        Parameters
        ----------
        output_file: str, optional
            Output file name. If not given, the file prefix in section "output"
            of nabu config will be taken.
        """
        out_cfg = self.process_config.nabu_config["output"]
        out_dir = output_dir or out_cfg["location"]
        prefix = prefix or ""
        # Prevent issue when out_dir is empty, which happens only if dataset/location is a relative path.
        # TODO this should be prevented earlier
        if out_dir is None or len(out_dir.strip()) == 0:
            out_dir = dirname(dirname(self.results[first_generator_item(self.results.keys())]))
        #
        if output_file is None:
            output_file = join(out_dir, prefix + out_cfg["file_prefix"]) + ".hdf5"
        if isfile(output_file):
            msg = str("File %s already exists" % output_file)
            if out_cfg["overwrite_results"]:
                msg += ". Overwriting as requested in configuration file"
                self.logger.warning(msg)
            else:
                msg += ". Set overwrite_results to True in [output] to overwrite existing files."
                self.logger.fatal(msg)
                raise ValueError(msg)

        local_files = files
        if local_files is None:
            local_files = self.get_relative_files()
        if local_files == []:
            self.logger.error("No files to merge")
            return
        entry = getattr(self.process_config.dataset_info.dataset_scanner, "entry", "entry")
        process_name = process_name or self._process_name
        h5_path = join(entry, *[process_name, "results", "data"])
        #
        self.logger.info("Merging %ss to %s" % (process_name, output_file))

        print("omitting config in call to merge_hdf5_files because export2dict too slow")

        merge_hdf5_files(
            local_files,
            h5_path,
            output_file,
            process_name,
            output_entry=entry,
            output_filemode="a",
            processing_index=0,
            config={
                self._process_name + "_stages": {str(k): v for k, v in zip(self.results.keys(), local_files)},
                "diagnostics": self.diagnostic_per_chunk,
            },
            # config={
            #     self._process_name + "_stages": {str(k): v for k, v in zip(self.results.keys(), local_files)},
            #     "nabu_config": self.process_config.nabu_config,
            #     "processing_options": self.process_config.processing_options,
            # },
            base_dir=out_dir,
            axis=axis,
            overwrite=out_cfg["overwrite_results"],
        )
        if merge_histograms:
            self.merge_histograms(output_file=output_file)
        return output_file

    merge_hdf5_files = merge_hdf5_reconstructions
