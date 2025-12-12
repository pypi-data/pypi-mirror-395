flatfield_modes = {
    "true": True,
    "1": True,
    "false": False,
    "0": False,
    # These three should be removed after a while (moved to 'flatfield_loading_mode')
    "forced": "force-load",
    "force-load": "force-load",
    "force-compute": "force-compute",
    #
    "pca": "pca",
}

flatfield_loading_mode = {
    "": "load_if_present",
    "load_if_present": "load_if_present",
    "forced": "force-load",
    "force-load": "force-load",
    "force-compute": "force-compute",
}

phase_retrieval_methods = {
    "": None,
    "none": None,
    "paganin": "paganin",
    "tie": "paganin",
    "ctf": "CTF",
}

unsharp_methods = {
    "gaussian": "gaussian",
    "log": "log",
    "laplacian": "log",
    "imagej": "imagej",
    "none": None,
    "": None,
}

# see PaddingBase.supported_modes
padding_modes = {
    "zeros": "zeros",
    "zero": "zeros",
    "constant": "zeros",
    "edges": "edge",
    "edge": "edge",
    "mirror": "reflect",
    "reflect": "reflect",
    "symmetric": "symmetric",
    "wrap": "wrap",
}

reconstruction_methods = {
    "fbp": "FBP",
    "cone": "cone",
    "conic": "cone",
    "none": None,
    "": None,
    "mlem": "mlem",
    "fluo": "mlem",
    "em": "mlem",
    "hbp": "HBP",
    "ghbp": "HBP",
}

fbp_filters = {
    "ramlak": "ramlak",
    "ram-lak": "ramlak",
    "none": None,
    "": None,
    "shepp-logan": "shepp-logan",
    "cosine": "cosine",
    "hamming": "hamming",
    "hann": "hann",
    "tukey": "tukey",
    "lanczos": "lanczos",
    "hilbert": "hilbert",
}

iterative_methods = {
    "tv": "TV",
    "wavelets": "wavelets",
    "l2": "L2",
    "ls": "L2",
    "sirt": "SIRT",
    "em": "EM",
}

optim_algorithms = {
    "chambolle": "chambolle-pock",
    "chambollepock": "chambolle-pock",
    "chambolle-pock": "chambolle-pock",
    "fista": "fista",
}

reco_implementations = {
    "astra": "astra",
    "corrct": "corrct",
    "corr-ct": "corrct",
    "nabu": "nabu",
    "": None,
}

files_formats = {
    "h5": "hdf5",
    "hdf5": "hdf5",
    "nexus": "hdf5",
    "nx": "hdf5",
    "npy": "npy",
    "npz": "npz",
    "tif": "tiff",
    "tiff": "tiff",
    "jp2": "jp2",
    "jp2k": "jp2",
    "j2k": "jp2",
    "jpeg2000": "jp2",
    "edf": "edf",
    "vol": "vol",
}

distribution_methods = {
    "local": "local",
    "slurm": "slurm",
    "": "local",
    "preview": "preview",
}

log_levels = {
    "0": "error",
    "1": "warning",
    "2": "info",
    "3": "debug",
}

sino_normalizations = {
    "none": None,
    "": None,
    "chebyshev": "chebyshev",
    "subtraction": "subtraction",
    "division": "division",
}

cor_methods = {
    "auto": "centered",
    "centered": "centered",
    "global": "global",
    "sino sliding window": "sino-sliding-window",
    "sino-sliding-window": "sino-sliding-window",
    "sliding window": "sliding-window",
    "sliding-window": "sliding-window",
    "sino growing window": "sino-growing-window",
    "sino-growing-window": "sino-growing-window",
    "growing window": "growing-window",
    "growing-window": "growing-window",
    "sino-coarse-to-fine": "sino-coarse-to-fine",
    "composite-coarse-to-fine": "composite-coarse-to-fine",
    "near": "composite-coarse-to-fine",
    "fourier-angles": "fourier-angles",
    "fourier angles": "fourier-angles",
    "fourier-angle": "fourier-angles",
    "fourier angle": "fourier-angles",
    "octave-accurate": "octave-accurate",
    "vo": "vo",
}


tilt_methods = {
    "1d-correlation": "1d-correlation",
    "1dcorrelation": "1d-correlation",
    "polarfft": "fft-polar",
    "polar-fft": "fft-polar",
    "fft-polar": "fft-polar",
}

rings_methods = {
    "none": None,
    "": None,
    "munch": "munch",
    "mean-subtraction": "mean-subtraction",
    "mean_subtraction": "mean-subtraction",
    "mean-division": "mean-division",
    "mean_division": "mean-division",
    "vo": "vo",
}

detector_distortion_correction_methods = {"none": None, "": None, "identity": "identity", "map_xz": "map_xz"}


radios_rotation_mode = {
    "none": None,
    "": None,
    "chunk": "chunk",
    "chunks": "chunk",
    "full": "full",
}

exclude_projections_type = {
    "indices": "indices",
    "angular_range": "angular_range",
    "angles": "angles",
}
