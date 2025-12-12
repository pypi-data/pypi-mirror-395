from .. import version
from ..resources.utils import is_hdf5_extension
from ..pipeline.config import parse_nabu_config_file
from .cli_configs import ReconstructConfig
from .utils import parse_params_values
from .reconstruct import update_reconstruction_start_end, get_log_file


def main_helical():
    ReconstructConfig["dry_run"] = {
        "help": "Stops after printing some information on the reconstruction layout.",
        "default": 0,
        "type": int,
    }
    ReconstructConfig["diag_zpro_run"] = {
        "help": "run the pipeline without reconstructing but collecting the contributing radios slices for angles theta+n*360. The given argument is the number of thet in the interval  [0 ,180[. The same number is taken if available in [180,360[. And the whole is repated is available in [0,360[  for a total of 4*diag_zpro_run  possible exctracted contributions",
        "default": 0,
        "type": int,
    }

    args = parse_params_values(
        ReconstructConfig,
        parser_description=f"Perform a helical tomographic reconstruction",
        program_version="nabu " + version,
    )

    # Imports are done here, otherwise "nabu --version" takes forever
    from ..pipeline.helical.processconfig import ProcessConfig
    from ..pipeline.helical.helical_reconstruction import HelicalReconstructorRegridded

    #

    # A crash with scikit-cuda happens only on PPC64 platform if and nvidia-persistenced is running.
    # On such machines, a warm-up has to be done.
    import platform

    if platform.machine() == "ppc64le":
        try:
            from silx.math.fft.cufft import CUFFT
        except:  # can't catch narrower - cublasNotInitialized requires cublas !
            CUFFT = None  # noqa: F841
    #

    logfile = get_log_file(args["logfile"], args["log_file"], forbidden=[args["input_file"]])
    conf_dict = parse_nabu_config_file(args["input_file"])
    update_reconstruction_start_end(conf_dict, args["slice"].strip())

    proc = ProcessConfig(conf_dict=conf_dict, create_logger=logfile)
    logger = proc.logger

    if "tilt_correction" in proc.processing_steps:
        message = """ The rotate_projections step is activated. The Helical pipelines are not yet suited for  projection rotation
        it will soon be implemented. For the moment
        you should deactivate the rotation options in nabu.conf
        """
        raise ValueError(message)

    # Determine which reconstructor to use
    reconstructor_cls = None

    # fix the reconstruction roi if not given
    if "reconstruction" in proc.processing_steps:
        rec_config = proc.processing_options["reconstruction"]

        rot_center = rec_config["rotation_axis_position"]
        Nx, Ny = proc.dataset_info.radio_dims

        if proc.nabu_config["reconstruction"]["auto_size"]:
            if 2 * rot_center > Nx:
                w = round(2 * rot_center)
            else:
                w = round(2 * Nx - 2 * rot_center)
            rec_config["start_x"] = round(rot_center - w / 2)
            rec_config["end_x"] = round(rot_center + w / 2)

            rec_config["start_y"] = rec_config["start_x"]
            rec_config["end_y"] = rec_config["end_x"]

    reconstructor_cls = HelicalReconstructorRegridded

    logger.debug("Using pipeline: %s" % reconstructor_cls.__name__)

    # Get extra options
    extra_options = {
        "gpu_mem_fraction": args["gpu_mem_fraction"],
        "cpu_mem_fraction": args["cpu_mem_fraction"],
    }
    extra_options.update(
        {
            ##### ??? "use_phase_margin": args["use_phase_margin"],
            "max_chunk_size": args["max_chunk_size"] if args["max_chunk_size"] > 0 else None,
            "phase_margin": args["phase_margin"],
            "dry_run": args["dry_run"],
            "diag_zpro_run": args["diag_zpro_run"],
        }
    )

    R = reconstructor_cls(proc, logger=logger, extra_options=extra_options)

    R.reconstruct()
    if not R.dry_run:
        R.merge_data_dumps()
        if is_hdf5_extension(proc.nabu_config["output"]["file_format"]):
            R.merge_hdf5_reconstructions()
        R.merge_histograms()

    # here we have been called by the cli. The return value 0 means OK
    return 0


if __name__ == "__main__":
    main_helical()
