from os import environ
from os.path import join, isfile, basename, dirname
from time import sleep
from multiprocessing.pool import Pool, get_context
from math import ceil
import gc
from silx.io import get_data
from silx.io.url import DataUrl
from tomoscan.esrf.volume.singleframebase import VolumeSingleFrameBase
from ... import version as nabu_version
from ...utils import check_supported, first_generator_item, subdivide_into_overlapping_segment, split_list
from ...resources.logger import LoggerOrPrint, PrinterLogger, Logger
from ...resources.utils import is_hdf5_extension, get_available_ram_GB
from ...io.writer import merge_hdf5_files, NXProcessWriter
from ...preproc.phase import compute_paganin_margin
from ...processing.histogram import PartialHistogram, add_last_bin, hist_as_2Darray
from .chunked import ChunkedPipeline
from .computations import estimate_max_chunk_size
from ..tasks import FakeTaskProcessor, TaskProcessor


def variable_idxlen_sort(fname):
    return int(fname.split("_")[-1].split(".")[0])


def _proc_collect_cuda_gpus(x):
    from nabu.cuda.utils import collect_cuda_gpus

    return collect_cuda_gpus()


def _collect_cuda_gpus(safe=True):
    if not safe:
        return _proc_collect_cuda_gpus(None)
    try:
        ctx = get_context("spawn")
        with Pool(1, context=ctx) as p:
            v = p.map(_proc_collect_cuda_gpus, [1])[0]
    except AssertionError:
        # Can get AssertionError: daemonic processes are not allowed to have children
        # if the calling code is already a subprocess
        return _proc_collect_cuda_gpus(None)
    return v


class NannyPipeline:
    """
    A "nanny" pipeline that runs in a separate process
    """

    def __init__(
        self, process_config, backend="numpy", pipeline_mode="chunked", logging_options=None, **pipeline_kwargs
    ):
        self.process_config = process_config
        self.previous_task = None
        self.pipeline = None
        self.worker_id = 0  # placeholder
        self._get_pipeline_class(backend, pipeline_mode)
        self.pipeline_kwargs = pipeline_kwargs
        self._create_logger(logging_options)

    def _create_logger(self, logging_options):
        if logging_options is None:
            self.logger = PrinterLogger()
            return
        my_logging_options = logging_options.copy()
        logname = logging_options.pop("logname", "nabu")
        self.logger = Logger(logname, **my_logging_options)

    def _get_pipeline_class(self, backend, pipeline_mode):
        self.backend = backend
        # Check were done before
        if backend == "cuda":
            # Don't initialize cuda before creating a new process (with fork) !
            from .chunked_cuda import CudaChunkedPipeline

            self._pipeline_cls = CudaChunkedPipeline
        else:
            self._pipeline_cls = ChunkedPipeline
        self._pipeline_mode = pipeline_mode

    def _get_chunk_length(self, task):
        # normally not supported
        if self._pipeline_mode == "helical":
            (start_z, end_z) = task["sub_region"]
            return end_z - start_z
        #
        (start_angle, end_angle), (start_z, end_z), _ = task["sub_region"]
        if self._pipeline_mode == "chunked":
            return end_z - start_z
        else:
            return end_angle - start_angle

    def _instantiate_pipeline(self, task):
        self.logger.set_prefix("  " * (self.worker_id) + f"[{self.worker_id}] ")
        self.logger.debug("Creating a new pipeline object")
        chunk_shape = tuple(s[1] - s[0] for s in task["sub_region"])
        args = [self.process_config, chunk_shape]
        pipeline_init_kwargs = self.pipeline_kwargs.copy()
        if self.backend == "cuda":
            pipeline_init_kwargs["cuda_options"] = {"device_id": self.worker_id}
        pipeline_init_kwargs["use_grouped_mode"] = self._pipeline_mode == "grouped"
        pipeline = self._pipeline_cls(*args, logger=self.logger, margin=task["margin"], **pipeline_init_kwargs)
        self.pipeline = pipeline

    def _instantiate_pipeline_if_necessary(self, current_task, other_task):
        """
        Instantiate a pipeline only if current_task has a different "delta z" than other_task
        """
        if self.pipeline is None:
            self._instantiate_pipeline(current_task)
            return
        length_cur = self._get_chunk_length(current_task)
        length_other = self._get_chunk_length(other_task)
        if length_cur != length_other or current_task["margin"] != other_task["margin"]:
            self.logger.debug("Destroying pipeline instance and releasing memory")
            self._destroy_pipeline()
            self._instantiate_pipeline(current_task)

    def _destroy_pipeline(self):
        self.pipeline = None

        gc.collect()
        # Not elegant, but for now the only way to release Cuda memory
        import cupy

        cupy.get_default_memory_pool().free_all_blocks()
        cupy.get_default_pinned_memory_pool().free_all_blocks()
        gc.collect()

    def process_task(self, task):
        """
        'task' is in the form {"sub_region": ((a0, a1), (z0, z1), (x0, x1)), "margin": (m_v, m_h)}
        """
        prev_task = self.previous_task
        self.logger.info("Processing sub-volume %s" % (str(task["sub_region"])))
        self._instantiate_pipeline_if_necessary(task, prev_task)
        self.pipeline.process_chunk(task["sub_region"], output_start_z=task.get("output_start_z", None))

        if self._pipeline_mode == "grouped":
            task_result = self.pipeline.datadump_manager.data_dump["sinogram"].fname
        else:
            task_result = self.pipeline.writer.fname if self.pipeline.writer is not None else None

        task_result = {
            "sub_region": task["sub_region"],
            "result": task_result,
            "histogram": None,
            "data_dumps": {},
        }
        if self.pipeline.writer is not None and self.pipeline.writer.histogram:
            task_result["histogram"] = self.pipeline.writer.histogram_writer.fname
        if len(self.pipeline.datadump_manager.data_dump) > 0:
            for step_name, writer in self.pipeline.datadump_manager.data_dump.items():
                task_result["data_dumps"][step_name] = writer.fname

        self.previous_task = task
        return task_result


class FullFieldReconstructor:
    """
    A reconstructor spawns and manages Pipeline objects, depending on the current chunk/group size.
    """

    _available_backends = ["cuda", "numpy"]

    _process_name = "reconstruction"

    default_advanced_options = {
        "gpu_mem_fraction": 0.9,
        "cpu_mem_fraction": 0.9,
        "chunk_size": None,
        "margin": None,
        "force_grouped_mode": False,
        "disable_multiprocessing_if_possible": True,
    }

    def __init__(self, process_config, logger=None, backend="cuda", extra_options=None, cuda_options=None):
        """
        Initialize a Reconstructor object.
        This class is used for managing pipelines.

        Parameters
        ----------
        process_config: ProcessConfig object
            Data structure with process configuration
        logger: Logger, optional
            logging object
        backend: str, optional
            Which backend to use. Available are: "cuda", "numpy".
        extra_options: dict, optional
            Dictionary with advanced options. Please see 'Other parameters' below
        cuda_options: dict, optional
            Dictionary with cuda options passed to `nabu.cuda.processing.CudaProcessing`


        Other Parameters
        -----------------
        Advanced options can be passed in the 'extra_options' dictionary. These can be:

           - cpu_mem_fraction: 0.9,
           - gpu_mem_fraction: 0.9,
           - chunk_size: None,
           - margin: None,
           - force_grouped_mode: False
        """
        self.logger = LoggerOrPrint(logger)
        self.process_config = process_config
        self._set_extra_options(extra_options)
        self._get_reconstruction_range()
        self._get_resources()
        self._get_backend(backend, cuda_options)
        self._compute_margin()
        self._compute_max_chunk_size()
        self._get_pipeline_mode()
        self._build_tasks()

        self._do_histograms = self.process_config.nabu_config["postproc"]["output_histogram"]
        self._reconstruction_output_format_is_hdf5 = is_hdf5_extension(
            self.process_config.nabu_config["output"]["file_format"]
        )
        self._histogram_merged = False
        self._histogram_merged = False

    #
    # Initialization
    #

    def _set_extra_options(self, extra_options):
        self.extra_options = self.default_advanced_options.copy()
        self.extra_options.update(extra_options or {})
        self.gpu_mem_fraction = self.extra_options["gpu_mem_fraction"]
        self.cpu_mem_fraction = self.extra_options["cpu_mem_fraction"]

    def _get_reconstruction_range(self):
        rec_region = self.process_config.rec_region  # without binning
        self.z_min = rec_region["start_z"]
        # In the user configuration, the upper bound is included: [start_z, end_z].
        # In python syntax, the upper bound is not: [start_z, end_z[
        self.z_max = rec_region["end_z"] + 1
        self.delta_z = self.z_max - self.z_min
        # Cache some volume info
        self.n_angles = self.process_config.n_angles(subsampling=False)
        self.n_z, self.n_x = self.process_config.radio_shape(binning=False)

    def _get_resources(self):
        self.resources = {}
        self._get_gpu()
        self._get_memory()

    def _get_memory(self):
        self.resources["mem_avail_GB"] = get_available_ram_GB()
        self.cpu_mem = self.resources["mem_avail_GB"] * self.cpu_mem_fraction

    def _get_gpu(self):
        resources_config = self.process_config.nabu_config.get("resources", {})

        # Number of workers
        self.n_workers = resources_config.get("workers", 1)
        n_gpus = resources_config.get("gpus", 1)
        gpu_ids = resources_config.get("gpu_id", [])
        if gpu_ids != [] and len(gpu_ids) != n_gpus:
            self.logger.warning(
                "Found a discrepancy between 'gpus' and 'gpu_id' in config file. The parameter 'gpu_id' takes precedence."
            )
            n_gpus = len(gpu_ids)
        if gpu_ids == []:
            gpu_ids = list(range(n_gpus))  # list(avail_gpus.keys())[:n_gpus] ?

        self._use_multiprocessing = True
        if (self.n_workers == 1 or n_gpus == 1) and self.extra_options.get("disable_multiprocessing_if_possible", True):
            self.logger.debug("Disabling multi-processing for single-worker reconstruction")
            self._use_multiprocessing = False

        # GPUS / gpu id
        avail_gpus = _collect_cuda_gpus(safe=not (self.extra_options.get("disable_multiprocessing", False))) or {}
        self.resources["gpus"] = avail_gpus
        if len(avail_gpus) == 0:
            self._has_cupy = False
            return
        self._has_cupy = True

        if len(gpu_ids) > len(avail_gpus):
            self.logger.error(f"Requested {len(gpu_ids)} GPUs which is more than the {len(avail_gpus)} available GPUs")
            gpu_ids = gpu_ids[: len(avail_gpus)]
        self.resources["gpu_id"] = gpu_ids

        if len(gpu_ids) != self.n_workers:
            self.logger.warning(
                f"Requested n_workers={self.n_workers} and gpu_id={gpu_ids}. For now nabu can only use one worker per gpu. Resetting n_workers={len(gpu_ids)}"
            )
            self.n_workers = len(gpu_ids)

    def _get_backend(self, backend, cuda_options):
        # self._pipeline_cls = ChunkedPipeline
        check_supported(backend, self._available_backends, "backend")
        if backend == "cuda":
            self.cuda_options = cuda_options
            if len(self.resources["gpus"]) == 0:
                # Not sure if an error should be raised in this case
                self.logger.error("Could not find any cuda device. Falling back on numpy/CPU backend.")
                backend = "numpy"
            else:
                for gpu_id in self.resources["gpu_id"]:
                    gpu_desc = self.resources["gpus"][gpu_id]
                    gpu_mem_tot = gpu_desc["memory_total_GB"]
                    gpu_mem_avail = gpu_desc["memory_avail_GB"]
                    if gpu_mem_avail / gpu_mem_tot < 0.5:
                        self.logger.warning(
                            f"It looks like the target GPU number {gpu_id} ({gpu_desc['name']}) is in use (less than half memory available)"
                        )
                # Assume all GPU have the same amount of memory # FIXME
                self.gpu_mem = gpu_mem_avail * self.gpu_mem_fraction
        if backend == "cuda" and not (self._has_cupy):
            raise RuntimeError("cupy is not avilable")

        # In the special case where we use astra for cone-beam (FDK) reconstruction,
        # astra can do the data split automatically better than nabu
        # In this case, do all the preprocessing CPU, and only FDK on GPU
        rec_config = self.process_config.nabu_config["reconstruction"]
        if rec_config["method"] == "cone" and rec_config.get("implementation") == "astra":
            self.logger.info(
                "Using reconstruction method='cone' and implementation='astra'. All pre-processing will be done on CPU, and final reconstruction with astra"
            )
            backend = "numpy"
        # ---

        self.backend = backend

    def _compute_max_chunk_size(self):
        """
        Compute the maximum number of (partial) radios that can be processed in memory.
        Ideally, the processing is done by reading N lines of all the projections.
        This function estimates max_chunk_size = N_max, the maximum number of lines that can be read
        in all the projections while still fitting the memory.
        On the other hand, if a "processing margin" is needed (eg. phase retrieval), then we need to read
        at least N_min = 2 * margin_v + n_slices lines of each image.
        For large datasets, we have N_min > max_chunk_size, so we can't read lines from all the projections.
        """
        user_chunk_size = self.extra_options["chunk_size"]
        if user_chunk_size is not None:
            self.chunk_size = user_chunk_size
        else:
            self.cpu_max_chunk_size = estimate_max_chunk_size(
                self.cpu_mem, self.process_config, pipeline_part="all", step=5
            )
            self.chunk_size = self.cpu_max_chunk_size
            if self.backend == "cuda":
                self.gpu_max_chunk_size = estimate_max_chunk_size(
                    self.gpu_mem,
                    self.process_config,
                    pipeline_part="all",
                    step=5,
                )
                self.chunk_size = min(self.gpu_max_chunk_size, self.cpu_max_chunk_size)
        self.chunk_size = min(self.chunk_size, self.n_z)

    def _compute_max_group_size(self):
        """
        Compute the maximum number of (partial) images that can be processed in memory
        """

        #
        # "Group size" (i.e, how many radios can be processed in one pass for the first part of the pipeline)
        #
        user_group_size = self.extra_options.get("chunk_size", None)
        if user_group_size is not None:
            self.group_size = user_group_size
        else:
            self.cpu_max_group_size = estimate_max_chunk_size(
                self.cpu_mem,
                self.process_config,
                pipeline_part="radios",
                n_rows=min(2 * self._margin_v + self.delta_z, self.n_z),
                step=10,
            )
            self.group_size = self.cpu_max_group_size
            if self.backend == "cuda":
                self.gpu_max_group_size = estimate_max_chunk_size(
                    self.gpu_mem,
                    self.process_config,
                    pipeline_part="radios",
                    n_rows=min(2 * self._margin_v + self.delta_z, self.n_z),
                    step=10,
                )
                self.group_size = min(self.gpu_max_group_size, self.cpu_max_group_size)
        self.group_size = min(self.group_size, self.n_angles)

        #
        # "sinos chunk size" (i.e, how many sinograms can be processed in one pass for the second part of the pipeline)
        #
        self.cpu_max_chunk_size_sinos = estimate_max_chunk_size(
            self.cpu_mem,
            self.process_config,
            pipeline_part="sinos",
            step=10,
        )
        self.chunk_size_sinos = self.cpu_max_chunk_size_sinos
        if self.backend == "cuda":
            self.gpu_max_chunk_size_sinos = estimate_max_chunk_size(
                self.gpu_mem,
                self.process_config,
                pipeline_part="sinos",
                step=5,
            )
            self.chunk_size_sinos = min(self.gpu_max_chunk_size_sinos, self.cpu_max_chunk_size_sinos)
        self.chunk_size_sinos = min(self.chunk_size_sinos, self.delta_z)

    def _get_pipeline_mode(self):
        # "Pipeline mode" means we either process data chunks of type [:, delta_z, :] or [delta_theta, :, :].
        # The first case is better in terms of performances and should be preferred.
        # However, in some cases, it's not possible to use it (eg. high "delta_z" because of margin)
        chunk_size_for_one_slice = 1 + 2 * self._margin_v  # TODO ignore margin when resuming from sinogram ?
        chunk_is_too_small = False
        if chunk_size_for_one_slice > self.chunk_size:
            msg = str(
                "Margin is %d, so we need to process at least %d detector rows. However, the available memory enables to process only %d rows at once"
                % (self._margin_v, chunk_size_for_one_slice, self.chunk_size)
            )
            chunk_is_too_small = True
        if self._margin_v > self.chunk_size // 3:
            n_slices = max(1, self.chunk_size - (2 * self._margin_v))
            n_stages = ceil(self.delta_z / n_slices)
            if n_stages > 1:
                msg = str("Margin (%d) is too big for chunk size (%d)" % (self._margin_v, self.chunk_size))
                chunk_is_too_small = True
        force_grouped_mode = self.extra_options.get("force_grouped_mode", False)
        if force_grouped_mode:
            msg = "Forcing grouped mode"
        if self.process_config.processing_options.get("phase", {}).get("method", None) == "CTF":
            force_grouped_mode = True
            msg = "CTF phase retrieval needs to process full radios"
        if (self.process_config.dataset_info.detector_tilt or 0) > 15:
            force_grouped_mode = True
            msg = "Radios rotation with a large angle needs to process full radios"
        if self.process_config.processing_options.get("flatfield", {}).get("method", "default") == "pca":
            force_grouped_mode = True
            msg = "PCA-Flatfield normalization needs to process full radios"
        if self.process_config.resume_from_step == "sinogram" and force_grouped_mode:
            self.logger.warning("Cannot use grouped-radios processing when resuming from sinogram")
            force_grouped_mode = False
        if not (chunk_is_too_small or force_grouped_mode):
            # Default case (preferred)
            self._pipeline_mode = "chunked"
            self.chunk_shape = (self.n_angles, self.chunk_size, self.n_x)
        else:
            # Fall-back mode (slower)
            self.logger.warning(msg)  # pylint: disable=E0606
            self._pipeline_mode = "grouped"
            self._compute_max_group_size()
            self.chunk_shape = (self.group_size, self.delta_z, self.n_x)
            self.logger.info("Using 'grouped' pipeline mode")

    #
    # "Margin"
    #

    def _compute_margin(self):
        user_margin = self.extra_options.get("margin", None) or self.process_config.nabu_config["pipeline"].get(
            "processing_margin", None
        )
        if self.process_config.resume_from_step == "sinogram":
            self.logger.debug("Margin not needed when resuming from sinogram")
            margin_v, margin_h = 0, 0
        elif user_margin is not None and user_margin > 0:
            margin_v, margin_h = user_margin, user_margin
            self.logger.info("Using user-defined margin: %d" % user_margin)
        else:
            unsharp_margin = self._compute_unsharp_margin()
            phase_margin = self._compute_phase_margin()
            translations_margin = self._compute_translations_margin()
            cone_margin = self._compute_cone_overlap()
            rot_margin = self._compute_rotation_margin()
            margin_v = max(unsharp_margin[0], phase_margin[0], translations_margin[0], cone_margin[0], rot_margin[0])
            margin_h = max(unsharp_margin[1], phase_margin[1], translations_margin[1], cone_margin[1], rot_margin[1])
            if margin_v > 0:
                self.logger.info("Estimated margin: %d pixels" % margin_v)

        margin_v = min(margin_v, self.n_z)
        margin_h = min(margin_h, self.n_x)
        self._margin = margin_v, margin_h
        self._margin_v = margin_v

    def _compute_unsharp_margin(self):
        if "unsharp_mask" not in self.process_config.processing_steps:
            return (0, 0)
        opts = self.process_config.processing_options["unsharp_mask"]
        sigma = opts["unsharp_sigma"]
        # nabu uses cutoff = 4
        cutoff = 4
        gaussian_kernel_size = ceil(2 * cutoff * sigma + 1)
        self.logger.debug("Unsharp mask margin: %d pixels" % gaussian_kernel_size)
        return (gaussian_kernel_size, gaussian_kernel_size)

    def _compute_phase_margin(self):
        phase_options = self.process_config.processing_options.get("phase", None)
        if phase_options is None:
            margin_v, margin_h = (0, 0)
        elif phase_options["method"] == "paganin":
            radio_shape = self.process_config.dataset_info.radio_dims[::-1]
            margin_v, margin_h = compute_paganin_margin(
                radio_shape,
                distance=phase_options["distance_m"],
                energy=phase_options["energy_kev"],
                delta_beta=phase_options["delta_beta"],
                pixel_size=phase_options["pixel_size_m"],
                padding=phase_options["padding_type"],
            )
        elif phase_options["method"] == "CTF":
            # The whole projection has to be processed!
            margin_v = ceil(
                (self.n_z - self.delta_z) / 2
            )  # not so elegant. Use a dedicated flag eg. _process_whole_image ?
            margin_h = 0  # unused for now
        else:
            margin_v, margin_h = (0, 0)
        return (margin_v, margin_h)

    def _compute_translations_margin(self):
        translations = self.process_config.dataset_info.translations
        if translations is None:
            return (0, 0)
        margin_h_v = []
        for i in range(2):
            transl = translations[:, i]
            margin_h_v.append(ceil(max([transl.max(), (-transl).max()])))
        self.logger.debug("Maximum vertical displacement: %d pixels" % margin_h_v[1])
        return tuple(margin_h_v[::-1])

    def _compute_cone_overlap(self):
        rec_cfg = self.process_config.processing_options.get("reconstruction", {})
        rec_method = rec_cfg.get("method", None)
        if rec_method != "cone":
            return (0, 0)
        d1 = rec_cfg["source_sample_dist"]
        d2 = rec_cfg["sample_detector_dist"]
        n_z, _ = self.process_config.radio_shape(binning=True)

        # delta_z = self.process_config.rec_delta_z  # accounts_for_binning
        # overlap = ceil(delta_z * d2 / (d1 + d2))  # sqrt(2) missing ?

        max_overlap = ceil(n_z * d2 / (d1 + d2))  # sqrt(2) missing ?
        max_overlap = max(max_overlap, 10)  # use at least 10 pixels

        return (max_overlap, 0)

    def _compute_rotation_margin(self):
        if "tilt_correction" in self.process_config.processing_steps:
            # Partial radios rotation yields too much error in single-slice mode
            # Forcing a big margin circumvents the problem
            # This is likely to trigger the 'grouped mode', but perhaps grouped mode should always be used when rotating radios
            nz, nx = self.process_config.radio_shape(binning=True)
            return nz // 3, nx // 3
        else:
            return 0, 0

    def _ensure_good_chunk_size_and_margin(self):
        """
        Check that "chunk_size" and "margin" (if any) are a multiple of binning factor.
        See nabu:!208
        After that, all subregion lengths of _build_tasks_chunked() should be multiple of the binning factor,
        because "delta_z" itself was checked to be a multiple in DatasetValidator._handle_binning()
        """
        bin_z = self.process_config.binning_z
        if bin_z <= 1:
            return
        self.chunk_size -= self.chunk_size % bin_z
        if self._margin_v > 0 and (self._margin_v % bin_z) > 0:
            self._margin_v += bin_z - (self._margin_v % bin_z)  # i.e margin = ((margin % bin_z) + 1) * bin_z

    #
    # Tasks management
    #

    def _modify_processconfig_stage_1(self):
        # Modify the "process_config" object to dump sinograms
        proc = self.process_config
        self._old_steps_to_save = proc.steps_to_save.copy()
        if "sinogram" in proc.steps_to_save:
            return
        proc._configure_save_steps(self._old_steps_to_save + ["sinogram"])

    def _undo_modify_processconfig_stage_1(self):
        self.process_config.steps_to_save = self._old_steps_to_save
        if "sinogram" not in self._old_steps_to_save:
            self.process_config.dump_sinogram = False

    def _modify_processconfig_stage_2(self):
        # Modify the "process_config" object to resume from sinograms
        proc = self.process_config
        self._old_resume_from = proc.resume_from_step
        self._old_proc_steps = proc.processing_steps.copy()
        self._old_proc_options = proc.processing_options.copy()
        proc._configure_resume(resume_from="sinogram")

    def _undo_modify_processconfig_stage_2(self):
        self.process_config.resume_from_step = self._old_resume_from
        self.process_config.processing_steps = self._old_proc_steps
        self.process_config.processing_options = self._old_proc_options

    def _build_tasks_grouped(self):
        tasks = []
        segments = subdivide_into_overlapping_segment(self.n_angles, self.group_size, 0)
        for segment in segments:
            _, start_angle, end_angle, _ = segment
            z_min = max(self.z_min - self._margin_v, 0)
            z_max = min(self.z_max + self._margin_v, self.n_z)
            sub_region = ((start_angle, end_angle), (z_min, z_max), (0, self.chunk_shape[-1]))
            tasks.append({"sub_region": sub_region, "margin": (self.z_min - z_min, z_max - self.z_max)})
        self.tasks = tasks
        # Build tasks for stage 2 (sinogram processing + reconstruction)
        segments = subdivide_into_overlapping_segment(self.delta_z, self.chunk_size_sinos, 0)
        self._sino_tasks = []
        for segment in segments:
            _, start_z, end_z, _ = segment
            z_min = self.z_min + start_z
            z_max = min(self.z_min + end_z, self.n_z)
            sub_region = ((0, self.n_angles), (z_min, z_max), (0, self.chunk_shape[-1]))
            task = {"sub_region": sub_region, "margin": None}
            if self.process_config.dataset_info.flip_frame_ud:
                task["output_start_z"] = (
                    self.z_max - 1 - task["sub_region"][1][0] - self._get_task_vertical_margin(task)[0]
                )
            self._sino_tasks.append(task)

    def _build_tasks_chunked(self):
        margin_v = self._margin_v
        if self.chunk_size >= self.delta_z and self.z_min == 0 and self.z_max == self.n_z:
            # In this case we can do everything in a single stage, without margin
            self.tasks = [
                {
                    "sub_region": ((0, self.n_angles), (self.z_min, self.z_max), (0, self.chunk_shape[-1])),
                    "margin": None,
                }
            ]
            return
        if self.chunk_size - (2 * margin_v) >= self.delta_z:
            # In this case we can do everything in a single stage
            n_slices = self.delta_z
            (margin_up, margin_down) = (min(margin_v, self.z_min), min(margin_v, self.n_z - self.z_max))
            self.tasks = [
                {
                    "sub_region": (
                        (0, self.n_angles),
                        (self.z_min - margin_up, self.z_max + margin_down),
                        (0, self.chunk_shape[-1]),
                    ),
                    "margin": ((margin_up, margin_down), (0, 0)),
                }
            ]
            return
        # In this case there are at least two stages
        n_slices = self.chunk_size - (2 * margin_v)
        n_stages = ceil(self.delta_z / n_slices)
        self.tasks = []
        curr_z_min = self.z_min
        curr_z_max = self.z_min + n_slices
        for i in range(n_stages):
            margin_up = min(margin_v, curr_z_min)
            margin_down = min(margin_v, max(self.n_z - curr_z_max, 0))
            if curr_z_max + margin_down >= self.z_max:
                curr_z_max -= curr_z_max - (self.z_max + 0)
                margin_down = min(margin_v, max(self.n_z - 1 - curr_z_max, 0))
            self.tasks.append(
                {
                    "sub_region": (
                        (0, self.n_angles),
                        (int(curr_z_min - margin_up), int(curr_z_max + margin_down)),
                        (0, self.chunk_shape[-1]),
                    ),
                    "margin": ((margin_up, margin_down), (0, 0)),
                }
            )
            if curr_z_max == self.z_max:
                # No need for further tasks
                break
            curr_z_min += n_slices
            curr_z_max += n_slices

    def _build_tasks(self):
        if self._pipeline_mode == "grouped":
            self._build_tasks_grouped()
        else:
            self._ensure_good_chunk_size_and_margin()
            self._build_tasks_chunked()
        if self.process_config.dataset_info.flip_frame_ud:
            for task in self.tasks:
                # when applying up-down flip we will have a decreasing z index. Indices will be in [start_z, ..., end_z[
                task["output_start_z"] = (
                    self.z_max - 1 - task["sub_region"][1][0] - self._get_task_vertical_margin(task)[0]
                )

    def _get_task_vertical_margin(self, task):
        margin = task.get("margin", None)
        if margin is None:
            return (0, 0)
        if self._pipeline_mode == "grouped":
            # margin is in the form (up, down)
            # TODO this is not consistent
            return margin
        else:
            # margin is in the form ((up, down), (left, right))
            return margin[0]

    def _print_tasks_chunked(self):
        for task in self.tasks:
            margin_up, margin_down = task["margin"][0]
            s_u, s_d = task["sub_region"][1]
            print(
                "Top Margin: [%04d, %04d[  |  Slices: [%04d, %04d[  |  Bottom Margin: [%04d, %04d["
                % (s_u, s_u + margin_up, s_u + margin_up, s_d - margin_down, s_d - margin_down, s_d)
            )

    def _print_tasks(self):
        for task in self.tasks:
            margin_up, margin_down = task["margin"][0]
            s_u, s_d = task["sub_region"][1]
            print(
                "Top Margin: [%04d, %04d[  |  Slices: [%04d, %04d[  |  Bottom Margin: [%04d, %04d["  # pylint: disable=E1307
                % (s_u, s_u + margin_up, s_u + margin_up, s_d - margin_down, s_d - margin_down, s_d)
            )

    def _get_chunk_length(self, task):
        if self._pipeline_mode == "helical":
            (start_z, end_z) = task["sub_region"]
            return end_z - start_z

        else:
            (start_angle, end_angle), (start_z, end_z), _ = task["sub_region"]

            if self._pipeline_mode == "chunked":
                return end_z - start_z
            else:
                return end_angle - start_angle

    def _give_progress_info(self, task):
        self.logger.info("Processing sub-volume %s" % (str(task["sub_region"][:-1])))

    #
    # Reconstruction
    #

    def _reconstruct_chunked(self, tasks=None):
        self.results = {}
        self._histograms = {}
        self._data_dumps = {}
        tasks = tasks or self.tasks

        pipeline_kwargs = {}
        if self.backend == "cuda":
            pipeline_kwargs["cuda_options"] = self.cuda_options

        # Handle frames vertical flip
        if self.process_config.dataset_info.flip_frame_ud:
            self.logger.warning("Using 'flip_ud' setting. Reconstructed volume will be flipped upside down!")
            pipeline_kwargs["extra_options"] = {"write_in_reverse_order": True}

        # subdivide tasks into workers
        workers_tasks = split_list(tasks, self.n_workers)

        _log_options = None
        if isinstance(self.logger, Logger):
            _log_options = {"level": self.logger.level, "logfile": self.logger.logfile}

        if self._use_multiprocessing:
            tasks_processor_class = TaskProcessor
        else:
            tasks_processor_class = FakeTaskProcessor

        self.tasks_processor = tasks_processor_class(
            NannyPipeline,
            n_processes=self.n_workers,
            worker_init_args=(self.process_config,),
            worker_init_kwargs={
                "backend": self.backend,
                "pipeline_mode": self._pipeline_mode,
                "logging_options": _log_options,
            }
            | pipeline_kwargs,
        )

        def _result_callback(future):
            result = future.result()
            if "error" in result:
                return
            task_key = result["sub_region"]
            self.results[task_key] = result["result"]
            if result["histogram"] is not None:
                self._histograms[task_key] = result["histogram"]
            if len(result["data_dumps"]) > 0:
                self._data_dumps[task_key] = result["data_dumps"]

        self.tasks_processor.start_workers()
        try:
            # Submit tasks
            future_results = {}
            for worker_id in range(self.n_workers):
                current_worker_tasks = workers_tasks[worker_id]
                for task_id, task in enumerate(current_worker_tasks):
                    fut = self.tasks_processor.submit(worker_id, task)
                    fut.add_done_callback(_result_callback)
                    future_results[task_id] = fut
            self.tasks_processor.start_work()
            # Wait for all results. See also the above callback '_result_callback'
            while not (all(f.done() for f in future_results.values())):
                sleep(1)

            # Handle errors that could happen in workers sub-processes.
            # Note that future.result() is no longer blocking because of the above wait.
            # We raise a RuntimeError here, because it cannot be raised within the callback.
            for task_id, future in future_results.items():
                if "error" in future.result():
                    msg = f"Something went wrong with task {task_id} ! Aborting reconstruction"
                    self.logger.fatal(msg)
                    raise RuntimeError(msg)

        finally:
            # Terminate workers
            self.tasks_processor.stop_workers()

    def _reconstruct_grouped(self):
        self.results = {}
        self._data_dumps = {}

        # Stage 1: radios processing
        self._modify_processconfig_stage_1()

        self._reconstruct_chunked()
        self.merge_data_dumps(axis=0)

        # self._destroy_pipeline()
        self.logger.info("End of first stage of processing. Will now process sinograms saved on disk")
        self._undo_modify_processconfig_stage_1()

        # Stage 2: sinograms processing and reconstruction
        if "reconstruction" not in self.process_config.processing_steps:
            return
        self._modify_processconfig_stage_2()
        self._pipeline_mode = "chunked"
        self._reconstruct_chunked(tasks=self._sino_tasks)
        self._pipeline_mode = "grouped"
        self._undo_modify_processconfig_stage_2()

    def reconstruct(self):
        if self._pipeline_mode == "chunked":
            self._reconstruct_chunked()
        else:
            self._reconstruct_grouped()

    #
    # Writing data
    #

    def get_relative_files(self, files=None):
        out_cfg = self.process_config.nabu_config["output"]
        if files is None:
            files = list(self.results.values())
        if all(f is None for f in files):
            return []
        try:
            files.sort(key=variable_idxlen_sort)
        except:
            self.logger.error(
                "Lexical ordering failed, falling back to default sort - it will fail for more than 10k projections"
            )
            files.sort()
        local_files = [join(out_cfg["file_prefix"], basename(fname)) for fname in files]
        return local_files

    def _get_reconstruction_metadata(self, partial_volumes_files=None):
        metadata = {
            "nabu_config": self.process_config.nabu_config,
            "processing_options": self.process_config.processing_options,
        }
        if self._reconstruction_output_format_is_hdf5 and partial_volumes_files is not None:
            metadata[self._process_name + "_stages"] = {
                str(k): v for k, v in zip(self.results.keys(), partial_volumes_files)
            }
        if not (self._reconstruction_output_format_is_hdf5):
            metadata["process_info"] = {
                "process_name": "reconstruction",
                "processing_index": 0,
                "nabu_version": nabu_version,
            }
        return metadata

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
        #
        # When dumping to disk an intermediate step taking place before cropping the radios,
        # 'start_z' and 'end_z' found in nabu config have to be augmented with margin_z.
        # (these values are checked in ProcessConfig._configure_resume())
        #
        patched_start_end_z = False
        if (
            self._margin_v > 0
            and process_name != "reconstruction"
            and self.process_config.is_before_radios_cropping(process_name)
            and "reconstruction" in self.process_config.processing_steps
        ):
            user_rec_config = self.process_config.processing_options["reconstruction"]
            patched_start_end_z = True
            old_start_z = user_rec_config["start_z"]
            old_end_z = user_rec_config["end_z"]
            user_rec_config["start_z"] = max(0, old_start_z - self._margin_v)
            user_rec_config["end_z"] = min(self.n_z, old_end_z + self._margin_v)
        #
        merge_hdf5_files(
            local_files,
            h5_path,
            output_file,
            process_name,
            output_entry=entry,
            output_filemode="a",
            processing_index=0,
            config=self._get_reconstruction_metadata(local_files),
            base_dir=out_dir,
            axis=axis,
            overwrite=out_cfg["overwrite_results"],
        )
        if merge_histograms:
            self.merge_histograms(output_file=output_file)
        if patched_start_end_z:
            user_rec_config["start_z"] = old_start_z
            user_rec_config["end_z"] = old_end_z
        return output_file

    def merge_histograms(self, output_file=None, force_merge=False):
        """
        Merge the partial histograms
        """
        if not (self._do_histograms):
            return
        if self._histogram_merged and not (force_merge):
            return
        self.logger.info("Merging histograms")

        masterfile_entry = getattr(self.process_config.dataset_info.dataset_scanner, "entry", "entry")
        masterfile_process_name = "histogram"  # TODO don't hardcode process name
        output_entry = masterfile_entry

        out_cfg = self.process_config.nabu_config["output"]
        if output_file is None:
            output_file = (
                join(dirname(first_generator_item(self._histograms.values())), out_cfg["file_prefix"] + "_histogram")
                + ".hdf5"
            )
        local_files = self.get_relative_files(files=list(self._histograms.values()))
        #
        h5_path = join(masterfile_entry, *[masterfile_process_name, "results", "data"])
        #

        try:
            files = sorted(self._histograms.values(), key=variable_idxlen_sort)
        except:
            self.logger.error(
                "Lexical ordering of histogram failed, falling back to default sort - it will fail for more than 10k projections"
            )
            files = sorted(self._histograms.values())
        data_urls = []
        for fname in files:
            url = DataUrl(file_path=fname, data_path=h5_path, data_slice=None, scheme="silx")
            data_urls.append(url)
        histograms = []
        for data_url in data_urls:
            h2D = get_data(data_url)
            histograms.append((h2D[0], add_last_bin(h2D[1])))
        histograms_merger = PartialHistogram(method="fixed_bins_number", num_bins=histograms[0][0].size)
        merged_hist = histograms_merger.merge_histograms(histograms)

        rec_region = self.process_config.rec_region
        # Not sure if we should account for binning here.
        # (note that "rec_region" does not account for binning).
        # Anyway the histogram has little use when using binning
        volume_shape = (
            rec_region["end_z"] - rec_region["start_z"] + 1,
            rec_region["end_y"] - rec_region["start_y"] + 1,
            rec_region["end_x"] - rec_region["start_x"] + 1,
        )
        writer = NXProcessWriter(output_file, entry=output_entry, filemode="a", overwrite=True)
        writer.write(
            hist_as_2Darray(merged_hist),
            "histogram",
            processing_index=1,
            config={
                "files": local_files,
                "bins": self.process_config.nabu_config["postproc"]["histogram_bins"],
                "volume_shape": volume_shape,
            },
            is_frames_stack=False,
            direct_access=False,
        )
        self._histogram_merged = True

    def merge_data_dumps(self, axis=1):
        # Collect in a dict where keys are step names (instead of task keys)
        dumps = {}
        for task_key, data_dumps in self._data_dumps.items():  # noqa: PERF102
            for step_name, fname in data_dumps.items():
                fname = join(basename(dirname(fname)), basename(fname))
                if step_name not in dumps:
                    dumps[step_name] = [fname]
                else:
                    dumps[step_name].append(fname)
        # Merge HDF5 files
        for step_name, files in dumps.items():
            dump_file = self.process_config.get_save_steps_file(step_name=step_name)
            self.merge_hdf5_reconstructions(
                output_file=dump_file,
                output_dir=dirname(dump_file),
                files=files,
                process_name=step_name,
                axis=axis,
                merge_histograms=False,
            )

    def write_metadata_file(self):
        metadata = self._get_reconstruction_metadata()
        save_options = self.process_config.processing_options["save"]
        # Perhaps there is more elegant
        metadata_writer = VolumeSingleFrameBase(
            url=DataUrl(file_path=save_options["location"], data_path="/"),
            volume_basename=save_options["file_prefix"],
            overwrite=True,
            metadata=metadata,
        )
        metadata_writer.save_metadata()

    def finalize_files_saving(self):
        """
        Last step to save data. This will do several things:
          - Merge data dumps (which are always HDF5 files): create a master file for all data-dump sub-volumes
          - Merge HDF5 reconstruction (if output format is HDF5)
          - Create a "metadata file" (if output format is not HDF5)
          - Merge histograms (if output format is not HDF5)
        """
        self.merge_data_dumps()
        if "reconstruction" not in self.process_config.processing_steps:
            return
        if self._reconstruction_output_format_is_hdf5:
            self.merge_hdf5_reconstructions()
        else:
            self.merge_histograms()
            self.write_metadata_file()
