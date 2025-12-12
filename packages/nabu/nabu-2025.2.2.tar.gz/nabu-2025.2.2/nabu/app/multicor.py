from os import remove
import numpy as np
from .. import version
from .reconstruct import get_reconstructor
from ..pipeline.fullfield.reconstruction import NannyPipeline
from .cli_configs import MultiCorConfig
from .utils import parse_params_values
from ..utils import view_as_images_stack


def get_user_cors(cors):
    """
    From a user-provided str describing the centers of rotation, build a list.
    """
    cors = cors.strip("[()]")
    cors = cors.split(",")
    cors = [c.strip() for c in cors]
    cors_list = []
    for c in cors:
        if ":" in c:
            if c.count(":") != 2:
                raise ValueError("Malformed range format for '%s': expected format start:stop:step" % c)
            start, stop, step = c.split(":")
            c_list = np.arange(float(start), float(stop), float(step)).tolist()
        else:
            c_list = [float(c)]
        cors_list.extend(c_list)
    return cors_list


def main():
    args = parse_params_values(
        MultiCorConfig,
        parser_description=f"Perform a tomographic reconstruction of a single slice using multiple centers of rotation",
        program_version="nabu " + version,
    )

    cors = get_user_cors(args["cor"])
    reconstructor = get_reconstructor(
        args,
        # Put a dummy CoR to avoid crash in both full-FoV and extended-FoV.
        # It will be overwritten later by the user-defined CoRs
        overwrite_options={"reconstruction/rotation_axis_position": cors[0]},
    )

    if reconstructor.delta_z > 1:
        raise ValueError("Only slice reconstruction can be used (have delta_z = %d)" % reconstructor.delta_z)

    pipeline_kwargs = {}
    if reconstructor.backend == "cuda":
        pipeline_kwargs["cuda_options"] = reconstructor.cuda_options
    pipeline_kwargs["use_grouped_mode"] = reconstructor._pipeline_mode == "grouped"

    nap = NannyPipeline(
        reconstructor.process_config,
        backend=reconstructor.backend,
        pipeline_mode=reconstructor._pipeline_mode,
        logging_options={"level": reconstructor.logger.level, "logfile": reconstructor.logger.logfile},
        **pipeline_kwargs,
    )
    nap._instantiate_pipeline(reconstructor.tasks[0])
    pipeline = nap.pipeline
    pipeline.process_chunk(reconstructor.tasks[0]["sub_region"])  # warm-up

    file_prefix = pipeline.processing_options["save"]["file_prefix"]
    #####
    # Remove the first reconstructed file (not used here)
    last_file = list(pipeline.writer.writer.browse_data_files())[-1]
    # ruff: noqa: SIM105, S110
    try:
        remove(last_file)
    except:
        pass
    ######

    options = reconstructor.process_config.processing_options["reconstruction"]
    reconstruct_from_sinos_stack = (options["method"].lower() == "cone") or (
        options["method"].lower() == "mlem" and options["implementation"].lower() == "corrct"
    )
    rec_kwargs = {}
    if options["method"].lower() == "cone":
        z_min, z_max = pipeline.sub_region_xz[2:]
        n_z_tot = pipeline.process_config.radio_shape(binning=True)[0]
        z_pos = ((z_min + z_max) / reconstructor.process_config.binning_z / 2) - n_z_tot / 2
        rec_kwargs["relative_z_position"] = z_pos
    do_halftomo = pipeline.process_config.do_halftomo

    rec_instance = pipeline.reconstruction
    # FIXME
    # ConebeamReconstructor will modify in-place the input sinogram when doing FDK, even if non-contiguous (radios layout).
    # FDK uses the 'mult_factor' below that is corrected by SinoFilter.
    # In our case this compensation has to be done once, since we re-use always the same sinogram
    if rec_instance.__class__.__name__ == "ConebeamReconstructor":
        mult_factor = rec_instance.n_angles / 3.141592 * 2
        rec_instance.sino_filter.set_filter(rec_instance.sino_filter.filter_f * mult_factor, normalize=False)
    # ---

    # Get sinogram
    if reconstruct_from_sinos_stack:
        sino = pipeline._d_radios.transpose((1, 0, 2))
    else:
        # Get sinogram into contiguous array
        # TODO Can't do memcpy2D ?! It used to work in cuda 11.
        # For now: transfer to host... not optimal
        sino = pipeline._d_radios[:, pipeline._d_radios.shape[1] // 2, :].get()  # pylint: disable=E1136

    for cor in cors:
        # Re-configure with new CoR
        pipeline.processing_options["reconstruction"]["rotation_axis_position"] = cor
        pipeline.processing_options["save"]["file_prefix"] = file_prefix + "_%.03f" % cor
        pipeline._init_writer(create_subfolder=False, single_output_file_initialized=False)
        # Reconfigure center of rotation
        if not (do_halftomo):
            pipeline.reconstruction.reset_rot_center(cor)
        else:
            # re-initialize FBP object, because in half-tomography the output slice size is a function of CoR
            rec_instance = pipeline.FBPClass(
                sino.shape,
                angles=options["angles"],
                rot_center=cor,
                filter_name=options["fbp_filter_type"] or "none",
                halftomo=options["enable_halftomo"],
                # slice_roi=self.process_config.rec_roi,
                padding_mode=options["padding_type"],
                extra_options={
                    "scale_factor": 1.0 / options["voxel_size_cm"][0],
                    "axis_correction": options["axis_correction"],
                    "centered_axis": options["centered_axis"],
                    "clip_outer_circle": options["clip_outer_circle"],
                    "filter_cutoff": options["fbp_filter_cutoff"],
                },
            )

        # Run reconstruction
        if reconstruct_from_sinos_stack:
            # Need to copy the sino each time, as it is modified by FDK
            rec = rec_instance.reconstruct(sino.copy(), **rec_kwargs)
            # take the middle slice
            rec = rec[rec.shape[0] // 2]
        else:
            rec = rec_instance.fbp(sino)
        rec_3D = view_as_images_stack(rec)  # writer wants 3D data

        # Write
        pipeline.writer.write_data(rec_3D)
        reconstructor.logger.info("Wrote %s" % pipeline.writer.fname)

    return 0


if __name__ == "__main__":
    main()
