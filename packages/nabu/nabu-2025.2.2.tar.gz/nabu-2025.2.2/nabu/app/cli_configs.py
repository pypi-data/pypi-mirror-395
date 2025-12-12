#
# Default configuration for CLI tools
#

# Default configuration for "bootstrap" command
from nabu.stitching.definitions import StitchingType
from nabu.pipeline.config_validators import str2bool

from tomoscan.framereducer.method import ReduceMethod

reduce_methods = tuple(member.value for member in ReduceMethod)

BootstrapConfig = {
    "bootstrap": {
        "help": "DEPRECATED, this is the default behavior. Bootstrap a configuration file from scratch.",
        "action": "store_const",
        "const": 1,
    },
    "convert": {
        "help": "UNSUPPORTED. This option has no effect and will disappear. Convert a PyHST configuration file to a nabu configuration file.",
        "default": "",
    },
    "output": {
        "help": "Output filename",
        "default": "nabu.conf",
    },
    "nocomments": {
        "help": "Remove the comments in the configuration file (default: False)",
        "action": "store_const",
        "const": 1,
    },
    "level": {
        "help": "Level of options to embed in the configuration file. Can be 'required', 'optional', 'advanced'.",
        "default": "optional",
    },
    "dataset": {
        "help": "Pre-fill the configuration file with the dataset path.",
        "default": "",
    },
    "template": {
        "help": "Use a template configuration file. Available are: id19_pag, id16_holo, id16_ctf, id16a_fluo, bm05_pag. You can also define your own templates via the NABU_TEMPLATES_PATH environment variable.",
        "default": "",
    },
    "helical": {"help": "Prepare configuration file for helical", "default": 0, "required": False, "type": int},
    "overwrite": {
        "help": "Whether to overwrite the output file if exists",
        "action": "store_const",
        "const": 1,
    },
}


# Default configuration for "histogram" command
HistogramConfig = {
    "h5_file": {
        "help": "HDF5 file(s). It can be one or several paths to HDF5 files. You can specify entry for each file with /path/to/file.h5?entry0000",
        "mandatory": True,
        "nargs": "+",
    },
    "output_file": {
        "help": "Output file (HDF5)",
        "mandatory": True,
    },
    "bins": {
        "help": "Number of bins for histogram if they have to be computed. Default is one million.",
        "default": 1000000,
        "type": int,
    },
    "chunk_size_slices": {
        "help": "If histogram are computed, specify the maximum subvolume size (in number of slices) for computing histogram.",
        "default": 100,
        "type": int,
    },
    "chunk_size_GB": {
        "help": "If histogram are computed, specify the maximum subvolume size (in GibaBytes) for computing histogram.",
        "default": -1,
        "type": float,
    },
    "loglevel": {
        "help": "Logging level. Can be 'debug', 'info', 'warning', 'error'. Default is 'info'.",
        "default": "info",
    },
}


# Default configuration for "reconstruct" command
ReconstructConfig = {
    "input_file": {
        "help": "Nabu input file",
        "default": "",
        "mandatory": True,
    },
    "logfile": {
        "help": "Log file. Default is dataset_prefix_nabu.log",
        "default": "",
    },
    "log_file": {
        "help": "Same as logfile. Deprecated, use --logfile instead.",
        "default": "",
    },
    "slice": {
        "help": "Slice(s) indice(s) to reconstruct, in the format z1-z2. Default (empty) is the whole volume. This overwrites the configuration file start_z and end_z. You can also use --slice first, --slice last, --slice middle, and --slice all",
        "default": "",
    },
    "gpu_mem_fraction": {
        "help": "Which fraction of GPU memory to use. Default is 0.9.",
        "default": 0.9,
        "type": float,
    },
    "cpu_mem_fraction": {
        "help": "Which fraction of memory to use. Default is 0.9.",
        "default": 0.9,
        "type": float,
    },
    "max_chunk_size": {
        "help": "Maximum chunk size to use.",
        "default": -1,
        "type": int,
    },
    "phase_margin": {
        "help": "Specify an explicit phase margin to use when performing phase retrieval.",
        "default": 0,
        "type": int,
    },
    "force_use_grouped_pipeline": {
        "help": "Force nabu to use the 'grouped' reconstruction pipeline - slower but should work for all big datasets.",
        "default": 0,
        "type": int,
    },
}


MultiCorConfig = ReconstructConfig.copy()
MultiCorConfig.update(
    {
        "cor": {
            "help": "Absolute positions of the center of rotation. It must be a list of comma-separated scalars, or in the form start:stop:step, where start, stop and step can all be floating-point values.",
            "default": "",
            "mandatory": True,
        },
        "slice": {
            "help": "Slice(s) indice(s) to reconstruct, in the format z1-z2. Default (empty) is the whole volume. This overwrites the configuration file start_z and end_z. You can also use --slice first, --slice last, --slice middle, and --slice all",
            "default": "",
            "mandatory": True,
        },
    }
)


RotateRadiosConfig = {
    "dataset": {
        "help": "Path to the dataset. Only HDF5 format is supported for now.",
        "default": "",
        "mandatory": True,
    },
    "entry": {
        "help": "HDF5 entry. By default, the first entry is taken.",
        "default": "",
    },
    "angle": {
        "help": "Rotation angle in degrees",
        "default": 0.0,
        "mandatory": True,
        "type": float,
    },
    "center": {
        "help": "Rotation center, in the form (x, y) where x (resp. y) is the horizontal (resp. vertical) dimension, i.e along the columns (resp. lines). Default is (Nx/2 - 0.5, Ny/2 - 0.5).",
        "default": "",
    },
    "output": {
        "help": "Path to the output file. Only HDF5 output is supported. In the case of HDF5 input, the output file will have the same structure.",
        "default": "",
        "mandatory": True,
    },
    "loglevel": {
        "help": "Logging level. Can be 'debug', 'info', 'warning', 'error'. Default is 'info'.",
        "default": "info",
    },
    "batchsize": {
        "help": "Size of the batch of images to process. Default is 100",
        "default": 100,
        "type": int,
    },
    "use_cuda": {
        "help": "Whether to use Cuda if available",
        "default": "1",
    },
    "use_multiprocessing": {
        "help": "Whether to use multiprocessing if available",
        "default": "1",
    },
}

DFFConfig = {
    "dataset": {
        "help": "Path to the dataset.",
        "default": "",
        "mandatory": True,
    },
    "entry": {
        "help": "HDF5 entry (for HDF5 datasets). By default, the first entry is taken.",
        "default": "",
    },
    "flatfield": {
        "help": "Whether to perform flat-field normalization. Default is True.",
        "default": "1",
        "type": int,
    },
    "sigma": {
        "default": 0.0,
        "help": "Enable high-pass filtering on double flatfield with this value of 'sigma'",
        "type": float,
    },
    "output": {
        "help": "Path to the output file (HDF5).",
        "default": "",
        "mandatory": True,
    },
    "loglevel": {
        "help": "Logging level. Can be 'debug', 'info', 'warning', 'error'. Default is 'info'.",
        "default": "info",
    },
    "chunk_size": {
        "help": "Maximum number of lines to read in each projection in a single pass. Default is 100",
        "default": 100,
        "type": int,
    },
}

CompareVolumesConfig = {
    "volume1": {
        "help": "Path to the first volume.",
        "default": "",
        "mandatory": True,
    },
    "volume2": {
        "help": "Path to the first volume.",
        "default": "",
        "mandatory": True,
    },
    "entry": {
        "help": "HDF5 entry. By default, the first entry is taken.",
        "default": "",
    },
    "hdf5_path": {
        "help": "Full HDF5 path to the data. Default is <entry>/reconstruction/results/data",
        "default": "",
    },
    "chunk_size": {
        "help": "Maximum number of images to read in each step. Default is 100.",
        "default": 100,
        "type": int,
    },
    "stop_at": {
        "help": "Stop the comparison immediately when the difference exceeds this threshold. Default is to compare the full volumes.",
        "default": "1e-4",
    },
    "statistics": {
        "help": "Compute statistics on the compared (sub-)volumes. Mind that in this case the command output will not be empty!",
        "default": 0,
        "type": int,
    },
}

EstimateMotionConfig = {
    "dataset": {
        "help": "Path to the dataset.",
        "default": "",
        "mandatory": True,
    },
    "flatfield": {
        "help": "Whether to perform flatfield normalization. Default is True.",
        "default": "1",
        "type": int,
    },
    "rot_center": {
        "help": "Center of rotation. If not provided, will be estimated.",
        "default": None,
    },
    "subsampling": {
        "help": "For 360-degrees scan, angular subsampling for matching opposite projections. Default is 10.",
        "default": 10,
        "type": int,
    },
    "deg_xy": {
        "help": "Polynomial degree in x-y for sample movement polynomial model",
        "default": 2,
        "type": int,
    },
    "deg_z": {
        "help": "Polynomial degree in z (vertical) for sample movement polynomial model",
        "default": 2,
        "type": int,
    },
    "win_size": {
        "help": "Size of the look-up window for half-tomography",
        "default": 300,
        "type": int,
    },
    "verbose": {
        "help": "Whether to plot the movement estimation fit",
        "default": 1,
    },
    "output_file": {
        "help": "Path of the output file containing the sample translations projected in the detector reference frame. This file can be directly used in 'translation_movements_file' of nabu configuration",
        "default": "correct_motion.txt",
    },
    "only": {
        "help": "Whether to only generate motion file for horizontal or vertical movement: --only horizontal  or --only vertical",
        "default": "",
    },
    "ccd_filter_size": {
        "help": "Size of conditional median filter to apply on radios. Default is zero (disabled)",
        "default": 0,
        "type": int,
    },
    "ccd_filter_threshold": {
        "help": "Threshold for median filter, 'ccd_filter_size' is not zero. Default is 0.04",
        "default": 0.04,
        "type": float,
    },
}

# Default configuration for "stitching" command
StitchingConfig = {
    "input-file": {
        "help": "Nabu configuraiton file for stitching (can be obtain from nabu-stitching-boostrap command)",
        "default": "",
        "mandatory": True,
    },
    "loglevel": {
        "help": "Logging level. Can be 'debug', 'info', 'warning', 'error'. Default is 'info'.",
        "default": "info",
    },
    "--only-create-master-file": {
        "help": "Will create the master file with all sub files (volumes or scans). It expects the processing to be finished. It can happen if all slurm job have been submitted but you've been kicked out of the cluster of if you need to relaunch manually some failling job slurm for any reason",
        "default": False,
        "action": "store_true",
    },
}

# Default configuration for "stitching-bootstrap" command
BootstrapStitchingConfig = {
    "stitching-type": {
        "help": f"User can provide stitching type to filter some parameters. Must be in {[sst for sst in StitchingType]}.",
        "default": None,
    },
    "level": {
        "help": "Level of options to embed in the configuration file. Can be 'required', 'optional', 'advanced'.",
        "default": "optional",
    },
    "output": {
        "help": "output file to store the configuration",
        "default": "stitching.conf",
    },
    "datasets": {
        "help": "datasets to be stitched together",
        "default": tuple(),
        "nargs": "*",
    },
}


ShrinkConfig = {
    "input_file": {
        "help": "Path to the NX file",
        "default": "",
        "mandatory": True,
    },
    "output_file": {
        "help": "Path to the output NX file",
        "default": "",
        "mandatory": True,
    },
    "entry": {
        "help": "HDF5 entry in the file. Default is to take the first entry.",
        "default": "",
    },
    "binning": {
        "help": "Binning factor, in the form (bin_z, bin_x). Each image (projection, dark, flat) will be binned by this factor",
        "default": "",
    },
    "subsampling": {"help": "Subsampling factor for projections (and metadata)", "default": ""},
    "threads": {
        "help": "Number of threads to use for binning. Default is 1.",
        "default": 1,
        "type": int,
    },
}

CompositeCorConfig = {
    "--filename_template": {
        "required": True,
        "help": """The filename template. It can optionally contain a segment equal to "X"*ndigits which will be replaced by the stage number if several stages are requested by the user""",
    },
    "--entry_name": {
        "required": False,
        "help": "Optional. The entry_name. It defaults to entry0000",
        "default": "entry0000",
    },
    "--num_of_stages": {
        "type": int,
        "required": False,
        "help": "Optional. How many stages. Example: from 0 to 43 -> --num_of_stages  44. It is optional. ",
    },
    "--oversampling": {
        "type": int,
        "default": 4,
        "required": False,
        "help": "Oversampling in the research of the axis position. Defaults to 4 ",
    },
    "--n_subsampling_y": {
        "type": int,
        "default": 10,
        "required": False,
        "help": "How many lines we are going to take from each radio. Defaults to 10.",
    },
    "--theta_interval": {
        "type": float,
        "default": 5,
        "required": False,
        "help": "Angular step for composing the image. Default to 5",
    },
    "--first_stage": {"type": int, "default": None, "required": False, "help": "Optional. The first stage.  "},
    "--output_file": {
        "type": str,
        "required": False,
        "help": "Optional. Where the list of cors will be written. Default is the filename postixed with cors.txt. If the output filename is postfixed with .json the output will be in json format",
    },
    "--cor_options": {
        "type": str,
        "help": """the cor_options string used by Nabu. Example 
        --cor_options "side='near'; near_pos = 300.0;  near_width = 20.0"
        """,
        "required": True,
    },
}

CreateDistortionMapHorizontallyMatchedFromPolyConfig = {
    "--nz": {"type": int, "help": "vertical dimension of the detector", "required": True},
    "--nx": {"type": int, "help": "horizontal dimension of the detector", "required": True},
    "--center_z": {"type": float, "help": "vertical position of the optical center", "required": True},
    "--center_x": {"type": float, "help": "horizontal position of the optical center", "required": True},
    "--c4": {"type": float, "help": "order 4 coefficient", "required": True},
    "--c2": {"type": float, "help": "order 2 coefficient", "required": True},
    "--target_file": {"type": str, "help": "The map output filename", "required": True},
    "--axis_pos": {
        "type": float,
        "default": None,
        "help": "Optional argument. If given it will be corrected for use with the produced map. The value is printed, or given as return argument if the utility is used from a script",
        "required": False,
    },
    "--loglevel": {
        "help": "Logging level. Can be 'debug', 'info', 'warning', 'error'. Default is 'info'.",
        "default": "info",
    },
}

DiagToRotConfig = {
    "--diag_file": dict(
        required=True, help="The reconstruction file obtained by nabu-helical using the diag_zpro_run option", type=str
    ),
    "--near": dict(
        required=False,
        help="This is a relative offset respect to the center of the radios. The cor will be searched around the provided value. If not given the optinal parameter original_scan must be the original nexus file; and the estimated core will be taken there. The netry_name parameter also must be provided in this case",
        default=None,
        type=float,
    ),
    "--original_scan": dict(
        required=False,
        help="The original nexus file. Required only if near parameter is not given",
        default=None,
        type=str,
    ),
    "--entry_name": dict(
        required=False,
        help="The original nexus file entry name. Required only if near parameter is not given",
        default=None,
        type=str,
    ),
    "--near_width": dict(
        required=False,
        help="For the horizontal correlation, searching the cor. The radius around the near value",
        default=20,
        type=int,
    ),
    "--low_pass": dict(
        required=False,
        help="Data are filtered horizontally. details smaller than the provided value are filtered out. Default is 1( gaussian sigma)",
        default=1.0,
        type=float,
    ),
    "--high_pass": dict(
        required=False,
        help="Data are filtered horizontally. Bumps larger than the provided value are filtered out. Default is 10( gaussian sigma)",
        default=10,
        type=int,
    ),
    "--linear_interpolation": dict(
        required=False, help="If True(default) the cor will vary linearly with z_transl", default=True, type=str2bool
    ),
    "--use_l1_norm": dict(
        required=False,
        default=True,
        help="If false then a L2 norm will be used for the error metric, considering the overlaps, if true L1 norm will be considered",
        type=str2bool,
    ),
    "--cor_file": dict(required=True, help="The file where the information to correct the cor are written", type=str),
}

DiagToPixConfig = {
    "--diag_file": dict(
        required=True, help="The reconstruction file obtained by nabu-helical using the diag_zpro_run option", type=str
    ),
    "--entry_name": dict(required=False, help="entry_name. Defauls is entry0000", default="entry0000", type=str),
    "--search_radius_v": dict(
        required=False,
        help="For the vertical correlation, The maximal error in pixels of one turn respect to a contiguous one. Default is 20 ",
        default=20,
        type=int,
    ),
    "--nexus_target": dict(
        required=False,
        help="If given, the mentioned file will be edited with the proper pixel size, the proper COR, and corrected x_translations",
        default=None,
        type=str,
    ),
    "--nexus_source": dict(
        required=False,
        help="Optionaly given, used only if nexus_target has been give. The nexus file will be edited and written on nexus_target. Otherwise nexus_target is considered to be the source",
        default=None,
        type=str,
    ),
}

CorrectRotConfig = {
    "--cor_file": dict(required=True, help="The file produce by diag_to_rot", type=str),
    "--entry_name": dict(required=False, help="entry_name. Defauls is entry0000", default="entry0000", type=str),
    "--nexus_target": dict(
        required=True,
        help="The given file will be edited with the proper pixel size, the proper COR, and corrected x_translations",
        default=None,
        type=str,
    ),
    "--nexus_source": dict(
        required=True, help="The nexus file will be edited and written on nexus_target", default=None, type=str
    ),
}


ReduceDarkFlatConfig = {
    "dataset": {"help": "Dataset (NXtomo or EDF folder) to be treated", "mandatory": True},
    "entry": {
        "dest": "entry",
        "help": "an entry can be specify in case of an NXtomo",
        "default": None,
        "required": False,
    },
    "dark-method": {
        "help": f"Define the method to be used for computing darks. Valid methods are {reduce_methods}",
        "default": ReduceMethod.MEAN,
        "required": False,
    },
    "flat-method": {
        "help": f"Define the method to be used for computing flats. Valid methods are {reduce_methods}",
        "default": ReduceMethod.MEDIAN,
        "required": False,
    },
    "overwrite": {
        "dest": "overwrite",
        "action": "store_true",
        "default": False,
        "help": "Overwrite dark/flats if exists",
        "required": False,
    },
    "debug": {
        "dest": "debug",
        "action": "store_true",
        "default": False,
        "help": "Set logging system in debug mode",
        "required": False,
    },
    "output-reduced-flats-file": {
        "aliases": ("orfl",),
        "default": None,
        "help": "Where to save reduced flats. If not provided will be dump near the .nx file at {scan_prefix}_flats.hdf5",
        "required": False,
    },
    "output-reduced-flats-data-path": {
        "aliases": ("output-reduced-flats-dp", "orfdp"),
        "default": None,
        "help": "Path in the output reduced flats file to save the dataset. If not provided will be saved at {entry}/flats/",
        "required": False,
    },
    "output-reduced-darks-file": {
        "aliases": ("ordf",),
        "default": None,
        "help": "Where to save reduced dark. If not provided will be dump near the .nx file at {scan_prefix}_darks.hdf5",
        "required": False,
    },
    "output-reduced-darks-data-path": {
        "aliases": ("output-reduced-darks-dp", "orddp"),
        "default": None,
        "help": "Path in the output reduced darks file to save the dataset. If not provided will be saved at {entry}/darks/",
        "required": False,
    },
}

PCAFlatsConfig = {
    "datasets": {"help": "datasets to be stitched together", "default": tuple(), "nargs": "+", "mandatory": True},
    "nsigma": {
        "help": "Paramter to select PCA components. Default is 3. Higher nsigma, less components.",
        "default": 3.0,
        "type": float,
        "required": False,
    },
    "flat-method": {
        "help": f"Define the method to be used for computing flats. Valid methods are {reduce_methods}",
        "default": ReduceMethod.MEDIAN,
        "required": False,
    },
    "dark-method": {
        "help": f"Define the method to be used for computing darks. Valid methods are {reduce_methods}",
        "default": ReduceMethod.MEAN,
        "required": False,
    },
    "overwrite": {
        "dest": "overwrite",
        "action": "store_true",
        "default": False,
        "help": "Overwrite dark/flats if exists",
    },
    "debug": {
        "dest": "debug",
        "action": "store_true",
        "default": False,
        "help": "Set logging system in debug mode",
        "required": False,
    },
    "output-filename": {
        "aliases": ("orfl",),
        "default": None,
        "help": "Where to save PCA flats. If not provided will be dumped in the current folder as{scan_prefix}_PCAFlats.hdf5",
        "required": False,
    },
}

ShowReconstructionTimingsConfig = {
    "logfile": {
        "help": "Path to the log file.",
        "default": "",
        "mandatory": True,
    },
    "cutoff": {
        "help": "Cut-off parameter. Timings below this value will be discarded. For a upper-bound cutoff, provide a value in the form 'low, high'",
        "default": None,
    },
    "type": {
        "help": "How to display the result. Default is a pie chart. Possible values are: pie, bars, violin",
        "default": "pie",
        "type": str,
    },
}

FlipVolumeVerticallyConfig = {
    "input": {
        "help": "Path to the volume to flip upside-down, either a directory or a file.",
        "default": "",
        "mandatory": True,
    },
    "vol_type": {
        "help": "Which type of volume is to be flipped. Possible values are: hdf5, tiff, tiff3d, edf, jp2, raw",
        "mandatory": True,
        "default": "",
    },
    "file_prefix": {
        "help": "File prefix, if relevant",
        "default": "",
    },
    "mem_fraction": {
        "help": "For HDF5/tiff3D/Raw volumes, amount of available RAM to use. Should be a number between 0 and 1 (eg. 0.5). Default is 0.25",
        "default": 0.25,
        "type": float,
    },
}
