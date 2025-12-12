from math import ceil
from silx.image.tomography import get_next_power
from ...utils import check_supported


def estimate_required_memory(
    process_config, delta_z=None, delta_a=None, max_mem_allocation_GB=None, fft_plans=True, debug=False
):
    """
    Estimate the memory (RAM) in Bytes needed for a reconstruction.

    Parameters
    -----------
    process_config: `ProcessConfig` object
        Data structure with the processing configuration
    delta_z: int, optional
        How many lines are to be loaded in the each projection image.
        Default is to load lines [start_z:end_z] (where start_z and end_z come from the user configuration file)
    delta_a: int, optional
        How many (partial) projection images to load at the same time. Default is to load all the projection images.
    max_mem_allocation_GB: float, optional
        Maximum amount of memory in GB for one single array.

    Returns
    -------
    required_memory: float
        Total required memory (in bytes).

    Raises
    ------
    ValueError if one single-array allocation exceeds "max_mem_allocation_GB"
    """

    def check_memory_limit(mem_GB, name):
        if max_mem_allocation_GB is None:
            return
        if mem_GB > max_mem_allocation_GB:
            raise ValueError(
                "Cannot allocate array '%s' %.3f GB > max_mem_allocation_GB = %.3f GB"
                % (name, mem_GB, max_mem_allocation_GB)
            )

    dataset = process_config.dataset_info
    processing_steps = process_config.processing_steps

    # The "x" dimension (last axis) is always the image width, because
    #  - Processing is never "cut" along this axis (we either split along frames, or images lines)
    #  - Even if we want to reconstruct a vertical slice (i.e end_x - start_x == 1),
    #    the tomography reconstruction will need the full information along this axis.
    # The only case where reading a x-subregion would be useful is to crop the initial data
    # (i.e knowing that a part of each image will be completely unused). This is not supported yet.
    Nx = process_config.radio_shape(binning=True)[-1]

    if delta_z is not None:
        Nz = delta_z // process_config.binning_z
    else:
        Nz = process_config.rec_delta_z  # accounting for binning
    if delta_a is not None:
        Na = ceil(delta_a / process_config.subsampling_factor)
    else:
        Na = process_config.n_angles(subsampling=True)

    total_memory_needed = 0

    # Read data
    # ----------
    data_image_size = Nx * Nz * 4
    data_volume_size = Na * data_image_size
    check_memory_limit(data_volume_size / 1e9, "projections")
    total_memory_needed += data_volume_size

    # CCD processing
    # ---------------
    if "flatfield" in processing_steps:
        # Flat-field is done in-place, but still need to load darks/flats
        n_darks = len(dataset.darks)
        n_flats = len(dataset.flats)
        total_memory_needed += (n_darks + n_flats) * data_image_size

    if "ccd_correction" in processing_steps:
        # CCD filter is "batched 2D"
        total_memory_needed += data_image_size

    # Phase retrieval
    # ---------------
    if "phase" in processing_steps:
        # Phase retrieval is done image-wise, so near in-place, but needs to allocate some memory:
        # filter with padded shape, radio_padded, radio_padded_fourier, and possibly FFT plan.
        # CTF phase retrieval uses "2 filters" (num and denom) but let's neglect this.
        Nx_p = get_next_power(2 * Nx)
        Nz_p = get_next_power(2 * Nz)
        img_size_real = Nx_p * Nz_p * 4
        img_size_cplx = ((Nx_p * Nz_p) // 2 + 1) * 8  # assuming RFFT
        factor = 1
        if fft_plans:
            factor = 2
        total_memory_needed += (2 * img_size_real + img_size_cplx) * factor

    # Sinogram de-ringing
    # -------------------
    if "sino_rings_correction" in processing_steps:
        method = process_config.processing_options["sino_rings_correction"]["method"]
        if method == "munch":
            # Process is done image-wise.
            # Needs one Discrete Wavelets transform and one FFT/IFFT plan for each scale
            factor = 2 if not (fft_plans) else 5.5  # approx!
            total_memory_needed += (Nx * Na * 4) * factor
        elif method == "vo":
            # cupy-based implementation makes many calls to "scipy-like" functions, where the memory usage is not under control
            # TODO try to estimate this
            pass

    # Reconstruction
    # ---------------
    reconstructed_volume_size = 0
    if "reconstruction" in processing_steps:
        rec_config = process_config.processing_options["reconstruction"]
        Nx_rec = rec_config["end_x"] - rec_config["start_x"] + 1
        Ny_rec = rec_config["end_y"] - rec_config["start_y"] + 1
        reconstructed_volume_size = Nz * Nx_rec * Ny_rec * 4
        check_memory_limit(reconstructed_volume_size / 1e9, "reconstructions")
        total_memory_needed += reconstructed_volume_size
        if process_config.rec_params["method"] == "cone":
            cone_implem = process_config.rec_params.get("implementation", "nabu")
            if cone_implem == "nabu":
                # In cone-beam reconstruction, need both sinograms and reconstruction inside GPU.
                # That's big!
                mult_factor = 2
                if rec_config["crop_filtered_data"] is False:
                    mult_factor = 4
                total_memory_needed += mult_factor * data_volume_size
            elif cone_implem == "astra":
                # Even when carefully using astra.data3d.link() with allocated memory,
                # astra will still allocate roughly 2.5 times (data_volume + reconstruction_volume), on host
                total_memory_needed -= reconstructed_volume_size
                total_memory_needed += (reconstructed_volume_size + data_volume_size) * 2.5

    if debug:
        print(
            "Mem for (delta_z=%s, delta_a=%s)  ==>  (Na=%d, Nz=%d, Nx=%d) : %.3f GB"
            % (delta_z, delta_a, Na, Nz, Nx, total_memory_needed / 1e9)
        )

    return total_memory_needed


def estimate_max_chunk_size(
    available_memory_GB,
    process_config,
    pipeline_part="all",
    n_rows=None,
    step=10,
    max_mem_allocation_GB=None,
    fft_plans=True,
    debug=False,
):
    """
    Estimate the maximum size of the data chunk that can be loaded in memory.

    Parameters
    ----------
    available_memory_GB: float
        available memory in Giga Bytes (GB - not GiB !).
    process_config: ProcessConfig
        ProcessConfig object
    pipeline_part: str
        Which pipeline part to consider. Possible options are:
          - "full": Account for all the pipeline steps (reading data all the way to reconstruction).
          - "radios": Consider only the processing steps on projection images (ignore sinogram-based steps and reconstruction)
          - "sinogram": Consider only the processing steps related to sinograms and reconstruction
    n_rows: int, optional
        How many lines to load in each projection. Only accounted for pipeline_part="radios".
    step: int, optional
        Step size when doing the iterative memory estimation
    max_mem_allocation_GB: float, optional
        Maximum size (in GB) for one single array.

    Returns
    -------
    n_max: int
        If pipeline_par is "full" or "sinos": return the maximum number of lines that can be loaded
        in all the projections while fitting memory, i.e `data[:, 0:n_max, :]`
        If pipeline_part is "radios", return the maximum number of (partial) images that can be loaded
        while fitting memory, i.e `data[:, zmin:zmax, 0:n_max]`

    """

    supported_pipeline_parts = ["all", "radios", "sinos"]
    check_supported(pipeline_part, supported_pipeline_parts, "pipeline_part")

    processing_steps_bak = process_config.processing_steps.copy()
    reconstruction_steps = ["sino_rings_correction", "reconstruction"]

    if pipeline_part == "all":
        # load lines from all the projections
        delta_a = None
        delta_z = 0
    if pipeline_part == "radios":
        # order should not matter
        process_config.processing_steps = list(set(process_config.processing_steps) - set(reconstruction_steps))
        # load lines from only a subset of projections
        delta_a = 0
        delta_z = n_rows
    if pipeline_part == "sinos":
        process_config.processing_steps = [
            step for step in process_config.processing_steps if step in reconstruction_steps
        ]
        # load lines from all the projections
        delta_a = None
        delta_z = 0

    mem = 0
    # pylint: disable=E0606, E0601
    last_valid_delta_a = delta_a
    last_valid_delta_z = delta_z
    while True:
        try:
            mem = estimate_required_memory(
                process_config,
                delta_z=delta_z,
                delta_a=delta_a,
                max_mem_allocation_GB=max_mem_allocation_GB,
                fft_plans=fft_plans,
                debug=debug,
            )
        except ValueError:
            # For very big dataset this function might return "0".
            # Either start at 1, or use a smaller step...
            break
        if mem / 1e9 > available_memory_GB:
            break
        if delta_a is not None and delta_a > process_config.n_angles():
            break
        if delta_z is not None and delta_z > process_config.radio_shape()[0]:
            break
        last_valid_delta_a, last_valid_delta_z = delta_a, delta_z
        if pipeline_part == "radios":
            delta_a += step
        else:
            delta_z += step

    process_config.processing_steps = processing_steps_bak

    if pipeline_part != "radios":
        if mem / 1e9 < available_memory_GB:
            res = min(delta_z, process_config.radio_shape()[0])
        else:
            res = last_valid_delta_z
    else:
        if mem / 1e9 < available_memory_GB:
            res = min(delta_a, process_config.n_angles())
        else:
            res = last_valid_delta_a

    # Really not ideal. For very large dataset, "step" should be very small.
    # Otherwise we go from 0 -> OK to 10 -> not OK, and then retain 0...
    if res == 0:
        res = 1
    #

    return res
