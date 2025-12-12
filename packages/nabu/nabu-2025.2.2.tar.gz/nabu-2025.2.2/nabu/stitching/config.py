import pint
from math import ceil
from collections.abc import Iterable, Sized
from dataclasses import dataclass
import numpy
from nxtomo.paths import nxtomo
from tomoscan.factory import Factory
from tomoscan.identifier import VolumeIdentifier, ScanIdentifier
from tomoscan.esrf.scan.nxtomoscan import NXtomoScan
from ..pipeline.config_validators import (
    boolean_validator,
    convert_to_bool,
)
from ..utils import concatenate_dict, convert_str_to_tuple
from .overlap import OverlapStitchingStrategy
from .utils.utils import ShiftAlgorithm
from .definitions import StitchingType
from .alignment import AlignmentAxis1, AlignmentAxis2

_ureg = pint.get_application_registry()

# ruff: noqa: S105

KEY_IMG_REG_METHOD = "img_reg_method"

KEY_WINDOW_SIZE = "window_size"

KEY_LOW_PASS_FILTER = "low_pass"

KEY_HIGH_PASS_FILTER = "high_pass"

KEY_OVERLAP_SIZE = "overlap_size"

KEY_SIDE = "side"

OUTPUT_SECTION = "output"

INPUTS_SECTION = "inputs"

PRE_PROC_SECTION = "preproc"

POST_PROC_SECTION = "postproc"

INPUT_DATASETS_FIELD = "input_datasets"

INPUT_PIXEL_SIZE_MM = "pixel_size"

INPUT_VOXEL_SIZE_MM = "voxel_size"

STITCHING_SECTION = "stitching"

STITCHING_STRATEGY_FIELD = "stitching_strategy"

STITCHING_TYPE_FIELD = "type"

DATA_FILE_FIELD = "location"

OVERWRITE_RESULTS_FIELD = "overwrite_results"

DATA_PATH_FIELD = "data_path"

AXIS_0_POS_PX = "axis_0_pos_px"

AXIS_1_POS_PX = "axis_1_pos_px"

AXIS_2_POS_PX = "axis_2_pos_px"

AXIS_0_POS_MM = "axis_0_pos_mm"

AXIS_1_POS_MM = "axis_1_pos_mm"

AXIS_2_POS_MM = "axis_2_pos_mm"

AXIS_0_PARAMS = "axis_0_params"

AXIS_1_PARAMS = "axis_1_params"

AXIS_2_PARAMS = "axis_2_params"

FLIP_LR = "fliplr"

FLIP_UD = "flipud"

NEXUS_VERSION_FIELD = "nexus_version"

OUTPUT_DTYPE = "data_type"

OUTPUT_VOLUME = "output_volume"

STITCHING_SLICES = "slices"

CROSS_CORRELATION_SLICE_FIELD = "slice_index_for_correlation"

RESCALE_FRAMES = "rescale_frames"

RESCALE_PARAMS = "rescale_params"

KEY_RESCALE_MIN_PERCENTILES = "rescale_min_percentile"

KEY_RESCALE_MAX_PERCENTILES = "rescale_max_percentile"

ALIGNMENT_AXIS_2_FIELD = "alignment_axis_2"

ALIGNMENT_AXIS_1_FIELD = "alignment_axis_1"

PAD_MODE_FIELD = "pad_mode"

AVOID_DATA_DUPLICATION_FIELD = "avoid_data_duplication"

# SLURM

SLURM_SECTION = "slurm"

SLURM_PARTITION = "partition"

SLURM_MEM = "memory"

SLURM_COR_PER_TASKS = "cpu-per-task"

SLURM_NUMBER_OF_TASKS = "n_tasks"

SLURM_N_JOBS = "n_jobs"

SLURM_OTHER_OPTIONS = "other_options"

SLURM_PREPROCESSING_COMMAND = "python_venv"

SLURM_MODULES_TO_LOADS = "modules"

SLURM_CLEAN_SCRIPTS = "clean_scripts"

SLURM_JOB_NAME = "job_name"

# normalization by sample

NORMALIZATION_BY_SAMPLE_SECTION = "normalization_by_sample"

NORMALIZATION_BY_SAMPLE_ACTIVE_FIELD = "active"

NORMALIZATION_BY_SAMPLE_METHOD = "method"

NORMALIZATION_BY_SAMPLE_SIDE = "side"

NORMALIZATION_BY_SAMPLE_MARGIN = "margin"

NORMALIZATION_BY_SAMPLE_WIDTH = "width"

# kernel extra options

STITCHING_KERNELS_EXTRA_PARAMS = "stitching_kernels_extra_params"

KEY_THRESHOLD_FREQUENCY = "threshold_frequency"


CROSS_CORRELATION_METHODS_AXIS_0 = {
    "": "",  # for display
    ShiftAlgorithm.NABU_FFT.value: "will call nabu `find_shift_correlate` function - shift search in fourier space",
    ShiftAlgorithm.SKIMAGE.value: "use scikit image `phase_cross_correlation` function in real space",
    ShiftAlgorithm.NONE.value: "no shift research is done. will only get shift from motor positions",
}

CROSS_CORRELATION_METHODS_AXIS_2 = CROSS_CORRELATION_METHODS_AXIS_0.copy()
CROSS_CORRELATION_METHODS_AXIS_2.update(
    {
        ShiftAlgorithm.CENTERED.value: "a fast and simple auto-CoR method. It only works when the CoR is not far from the middle of the detector. It does not work for half-tomography.",
        ShiftAlgorithm.GLOBAL.value: "a slow but robust auto-CoR.",
        ShiftAlgorithm.GROWING_WINDOW.value: "automatically find the CoR with a sliding-and-growing window. You can tune the option with the parameter 'cor_options'.",
        ShiftAlgorithm.SLIDING_WINDOW.value: "semi-automatically find the CoR with a sliding window. You have to specify on which side the CoR is (left, center, right). Please see the 'cor_options' parameter.",
        ShiftAlgorithm.COMPOSITE_COARSE_TO_FINE.value: "Estimate CoR from composite multi-angle images. Only works for 360 degrees scans.",
        ShiftAlgorithm.SINO_COARSE_TO_FINE.value: "Estimate CoR from sinogram. Only works for 360 degrees scans.",
    }
)

SECTIONS_COMMENTS = {
    STITCHING_SECTION: "section dedicated to stich parameters\n",
    OUTPUT_SECTION: "section dedicated to output parameters\n",
    INPUTS_SECTION: "section dedicated to inputs\n",
    SLURM_SECTION: "section didicated to slurm. If you want to run locally avoid setting 'partition or remove this section'",
    NORMALIZATION_BY_SAMPLE_SECTION: "section dedicated to normalization by a sample. If activate each frame can be normalized by a sample of the frame",
}

DEFAULT_SHIFT_ALG_AXIS_0 = "nabu-fft"
DEFAULT_SHIFT_ALG_AXIS_2 = "sliding-window"

_shift_algs_axis_0 = "\n            + ".join(
    [f"{key}: {value}" for key, value in CROSS_CORRELATION_METHODS_AXIS_0.items()]
)
_shift_algs_axis_2 = "\n            + ".join(
    [f"{key}: {value}" for key, value in CROSS_CORRELATION_METHODS_AXIS_2.items()]
)

HELP_SHIFT_PARAMS = f"""options for shifts algorithms as `key1=value1,key2=value2`. For now valid keys are:
    - {KEY_OVERLAP_SIZE}: size to apply stitching. If not provided will take the largest size possible'.
    - {KEY_IMG_REG_METHOD}: algorithm to use to find overlaps between the different sections. Possible values are \n        * for axis 0: {_shift_algs_axis_0}\n        * and for axis 2: {_shift_algs_axis_2}
    - {KEY_LOW_PASS_FILTER}: low pass filter value for filtering frames before shift research
    - {KEY_HIGH_PASS_FILTER}: high pass filter value for filtering frames before shift research"""


def _str_to_dict(my_str: str | dict):
    """convert a string as key_1=value_2;key_2=value_2 to a dict"""
    if isinstance(my_str, dict):
        return my_str
    res = {}
    for key_value in filter(None, my_str.split(";")):
        key, value = key_value.split("=")
        res[key] = value
    return res


def _dict_to_str(ddict: dict):
    return ";".join([f"{key!s}={value!s}" for key, value in ddict.items()])


def str_to_shifts(my_str: str | None) -> str | tuple:
    if my_str is None:
        return None
    elif isinstance(my_str, str):
        my_str = my_str.replace(" ", "")
        my_str = my_str.lstrip("[").lstrip("(")
        my_str = my_str.rstrip("]").lstrip(")")
        if my_str == "":
            return None
        try:
            shift = ShiftAlgorithm(my_str)
        except ValueError:
            shifts_as_str = filter(None, my_str.replace(";", ",").split(","))
            return [float(shift) for shift in shifts_as_str]
        else:
            return shift
    elif isinstance(my_str, (tuple, list)):
        return [float(shift) for shift in my_str]
    else:
        raise TypeError("Only str or tuple of str expected expected")


def _valid_stitching_kernels_params(my_dict: dict | str):
    if isinstance(my_dict, str):
        my_dict = _str_to_dict(my_str=my_dict)

    valid_keys = (KEY_THRESHOLD_FREQUENCY, KEY_SIDE)
    for key in my_dict:
        if key not in valid_keys:
            raise KeyError(f"{key} is a unrecognized key")
    return my_dict


def _valid_shifts_params(my_dict: dict | str):
    if isinstance(my_dict, str):
        my_dict = _str_to_dict(my_str=my_dict)

    valid_keys = (
        KEY_WINDOW_SIZE,
        KEY_IMG_REG_METHOD,
        KEY_OVERLAP_SIZE,
        KEY_HIGH_PASS_FILTER,
        KEY_LOW_PASS_FILTER,
        KEY_SIDE,
    )
    for key in my_dict:
        if key not in valid_keys:
            raise KeyError(f"{key} is a unrecognized key")
    return my_dict


def _slices_to_list_or_slice(my_str: str | None) -> str | slice:
    if my_str is None:
        return None
    if isinstance(my_str, (tuple, list)):
        if len(my_str) == 2:
            return slice(int(my_str[0]), int(my_str[1]))
        elif len(my_str) == 3:
            return slice(int(my_str[0]), int(my_str[1]), int(my_str[2]))
        else:
            raise ValueError("expect at most free values to define a slice")

    assert isinstance(my_str, str), f"wrong type. Get {my_str}, {type(my_str)}"
    my_str = my_str.replace(" ", "")
    if ":" in my_str:
        split_string = my_str.split(":")
        start = int(split_string[0])
        stop = int(split_string[1])
        if len(split_string) == 2:
            step = None
        elif len(split_string) == 3:
            step = int(split_string[2])
        else:
            raise ValueError(f"unable to interpret `slices` parameter: {my_str}")
        return slice(start, stop, step)
    else:
        my_str.replace(",", ";")
        return list(filter(None, my_str.split(";")))


def _scalar_or_tuple_to_bool_or_tuple_of_bool(my_str: bool | tuple | str, default=False):
    if isinstance(my_str, bool):
        return my_str
    elif isinstance(my_str, str):
        my_str = my_str.replace(" ", "")
        my_str = my_str.lstrip("(").lstrip("[")
        my_str = my_str.rstrip(")").lstrip("]")
        my_str = my_str.replace(",", ";")
        values = my_str.split(";")
        values = tuple([convert_to_bool(value)[0] for value in values])
    else:
        values = my_str
    if len(values) == 0:
        return default
    elif len(values) == 1:
        return values[0]
    else:
        return values


from nabu.stitching.sample_normalization import Method, SampleSide


class NormalizationBySample:
    __hash__ = object.__hash__

    def __init__(self) -> None:
        self._active = False
        self._method = Method.MEAN
        self._margin = 0
        self._side = SampleSide.LEFT
        self._width = 30

    def is_active(self):
        return self._active

    def set_is_active(self, active: bool):
        assert isinstance(
            active, bool
        ), f"active is expected to be a bool. Get {type(active)} instead. Value == {active}"
        self._active = active

    @property
    def method(self) -> Method:
        return self._method

    @method.setter
    def method(self, method: Method | str) -> None:
        self._method = Method(method)

    @property
    def margin(self) -> int:
        return self._margin

    @margin.setter
    def margin(self, margin: int):
        assert isinstance(margin, int), f"margin is expected to be an int. Get {type(margin)} instead"
        self._margin = margin

    @property
    def side(self) -> SampleSide:
        return self._side

    @side.setter
    def side(self, side: SampleSide | str):
        self._side = SampleSide(side)

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, width: int):
        assert isinstance(width, int), f"width is expected to be an int. Get {type(width)} instead"

    @staticmethod
    def from_dict(my_dict: dict):
        sample_normalization = NormalizationBySample()
        # active
        active = my_dict.get(NORMALIZATION_BY_SAMPLE_ACTIVE_FIELD, None)
        if active is not None:
            active = active in (True, "True", 1, "1")
            sample_normalization.set_is_active(active)

        # method
        method = my_dict.get(NORMALIZATION_BY_SAMPLE_METHOD, None)
        if method is not None:
            sample_normalization.method = method

        # margin
        margin = my_dict.get(NORMALIZATION_BY_SAMPLE_MARGIN, None)
        if margin is not None:
            sample_normalization.margin = int(margin)

        # side
        side = my_dict.get(NORMALIZATION_BY_SAMPLE_SIDE, None)
        if side is not None:
            sample_normalization.side = side

        # width
        width = my_dict.get(NORMALIZATION_BY_SAMPLE_WIDTH, None)
        if width is not None:
            sample_normalization.width = int(width)

        return sample_normalization

    def to_dict(self) -> dict:
        return {
            NORMALIZATION_BY_SAMPLE_ACTIVE_FIELD: self.is_active(),
            NORMALIZATION_BY_SAMPLE_METHOD: self.method.value,
            NORMALIZATION_BY_SAMPLE_MARGIN: self.margin,
            NORMALIZATION_BY_SAMPLE_SIDE: self.side.value,
            NORMALIZATION_BY_SAMPLE_WIDTH: self.width,
        }

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, NormalizationBySample):
            return False
        else:
            return self.to_dict() == value.to_dict()


@dataclass
class SlurmConfig:
    """configuration for slurm jobs"""

    partition: str = ""  # note: must stay empty to make by default we don't use slurm (use by the  configuration file)
    mem: str = "128"
    n_jobs: int = 1
    other_options: str = ""
    preprocessing_command: str = ""
    modules_to_load: tuple = tuple()
    clean_script: bool = ""
    n_tasks: int = 1
    n_cpu_per_task: int = 4
    job_name: str = ""

    def __post_init__(self) -> None:
        # make sure either 'modules' or 'preprocessing_command' is provided
        if len(self.modules_to_load) > 0 and self.preprocessing_command not in (None, ""):
            raise ValueError(
                f"Either modules {SLURM_MODULES_TO_LOADS} or preprocessing_command {SLURM_PREPROCESSING_COMMAND} can be provided. Not both."
            )

    def to_dict(self) -> dict:
        """dump configuration to dict"""
        return {
            SLURM_PARTITION: self.partition if self.partition is not None else "",
            SLURM_MEM: self.mem,
            SLURM_N_JOBS: self.n_jobs,
            SLURM_OTHER_OPTIONS: self.other_options,
            SLURM_PREPROCESSING_COMMAND: self.preprocessing_command,
            SLURM_MODULES_TO_LOADS: self.modules_to_load,
            SLURM_CLEAN_SCRIPTS: self.clean_script,
            SLURM_NUMBER_OF_TASKS: self.n_tasks,
            SLURM_COR_PER_TASKS: self.n_cpu_per_task,
            SLURM_JOB_NAME: self.job_name,
        }

    @staticmethod
    def from_dict(config: dict):
        return SlurmConfig(
            partition=config.get(
                SLURM_PARTITION, None
            ),  # warning: never set a default value. Would generate infinite loop from slurm call
            mem=config.get(SLURM_MEM, "32GB"),
            n_jobs=int(config.get(SLURM_N_JOBS, 10)),
            other_options=config.get(SLURM_OTHER_OPTIONS, ""),
            n_tasks=config.get(SLURM_NUMBER_OF_TASKS, 1),
            n_cpu_per_task=config.get(SLURM_COR_PER_TASKS, 4),
            preprocessing_command=config.get(SLURM_PREPROCESSING_COMMAND, ""),
            modules_to_load=convert_str_to_tuple(config.get(SLURM_MODULES_TO_LOADS, "")),
            clean_script=convert_to_bool(config.get(SLURM_CLEAN_SCRIPTS, False))[0],
            job_name=config.get(SLURM_JOB_NAME, ""),
        )


def _cast_shift_to_str(shifts: tuple | numpy.ndarray | str | None) -> str:
    if shifts is None:
        return ""
    elif isinstance(shifts, ShiftAlgorithm):
        return shifts.value
    elif isinstance(shifts, str):
        return shifts
    elif isinstance(shifts, (tuple, list, numpy.ndarray)):
        return ";".join([str(value) for value in shifts])
    else:
        raise TypeError(f"unexpected type: {type(shifts)}")


@dataclass
class StitchingConfiguration:
    """
    bass class to define stitching configuration
    """

    axis_0_pos_px: tuple | str | None
    "position along axis 0 in absolute. unit: px"
    axis_1_pos_px: tuple | str | None
    "position along axis 1 in absolute. unit: px"
    axis_2_pos_px: tuple | str | None
    "position along axis 2 in absolute. unit: px"

    axis_0_pos_mm: tuple | str | None = None
    "position along axis 0 in absolute. unit: mm"
    axis_1_pos_mm: tuple | str | None = None
    "position along axis 0 in absolute. unit: mm"
    axis_2_pos_mm: tuple | str | None = None
    "position along axis 0 in absolute. unit: mm"

    axis_0_params: dict = None
    axis_1_params: dict = None
    axis_2_params: dict = None
    slurm_config: SlurmConfig = None
    flip_lr: tuple | bool = False
    "flip frame left-right. For scan this will be append to the NXtransformations of the detector"
    flip_ud: tuple | bool = False
    "flip frame up-down. For scan this will be append to the NXtransformations of the detector"

    overwrite_results: bool = False
    stitching_strategy: OverlapStitchingStrategy = OverlapStitchingStrategy.COSINUS_WEIGHTS
    stitching_kernels_extra_params: dict = None

    slice_for_cross_correlation: str | int = "middle"

    # opts for rescaling frame during stitching
    rescale_frames: bool = False
    rescale_params: dict = None

    normalization_by_sample: NormalizationBySample = None

    duplicate_data: bool = True
    """when possible (for HDF5) avoid duplicating data as-much-much-as-possible. Overlaping region between two frames will be duplicated. Remaining will be 'raw_data' for volume.
    For projection flat field will be applied"""

    @property
    def stitching_type(self):
        raise NotImplementedError("Base class")

    def __post_init__(self):
        if self.normalization_by_sample is None:
            self.normalization_by_sample = NormalizationBySample()

    @staticmethod
    def get_description_dict() -> dict:
        def get_pos_info(axis, unit, alternative):
            return f"position over {axis} in {unit}. If provided {alternative} must be set to blank. If none provided then will try to get information from existing metadata"

        def get_default_shift_params(window_size=None, shift_alg=None) -> str:
            return ";".join(
                [
                    f"{KEY_WINDOW_SIZE}={window_size or ''}",
                    f"{KEY_IMG_REG_METHOD}={shift_alg or ''}",
                ]
            )

        return {
            STITCHING_SECTION: {
                STITCHING_TYPE_FIELD: {
                    "default": StitchingType.Z_PREPROC.value,
                    "help": f"stitching to be applied. Must be in {[st.value for st in StitchingType]}",
                    "type": "required",
                },
                STITCHING_STRATEGY_FIELD: {
                    "default": "cosinus weights",
                    "help": f"Policy to apply to compute the overlap area. Must be in {[ov.value for ov in OverlapStitchingStrategy]}.",
                    "type": "required",
                },
                CROSS_CORRELATION_SLICE_FIELD: {
                    "default": "middle",
                    "help": f"slice to use for image registration",
                    "type": "optional",
                },
                AXIS_0_POS_PX: {
                    "default": "",
                    "help": get_pos_info(axis=0, unit="pixel", alternative=AXIS_0_POS_MM),
                    "type": "optional",
                },
                AXIS_0_POS_MM: {
                    "default": "",
                    "help": get_pos_info(axis=1, unit="millimeter", alternative=AXIS_0_POS_PX),
                    "type": "optional",
                },
                AXIS_0_PARAMS: {
                    "default": get_default_shift_params(window_size=50, shift_alg=DEFAULT_SHIFT_ALG_AXIS_0),
                    "help": HELP_SHIFT_PARAMS,
                    "type": "optional",
                },
                AXIS_1_POS_PX: {
                    "default": "",
                    "help": get_pos_info(axis=1, unit="pixel", alternative=AXIS_1_POS_MM),
                    "type": "optional",
                },
                AXIS_1_POS_MM: {
                    "default": "",
                    "help": get_pos_info(axis=1, unit="millimeter", alternative=AXIS_1_POS_PX),
                    "type": "optional",
                },
                AXIS_1_PARAMS: {
                    "default": get_default_shift_params(),
                    "help": f"same as {AXIS_0_PARAMS} but for axis 1",
                    "type": "optional",
                },
                AXIS_2_POS_PX: {
                    "default": "",
                    "help": get_pos_info(axis=2, unit="pixel", alternative=AXIS_2_POS_MM),
                    "type": "optional",
                },
                AXIS_2_POS_MM: {
                    "default": "",
                    "help": get_pos_info(axis=2, unit="millimeter", alternative=AXIS_1_POS_PX),
                    "type": "optional",
                },
                AXIS_2_PARAMS: {
                    "default": get_default_shift_params(window_size=200, shift_alg=DEFAULT_SHIFT_ALG_AXIS_2),
                    "help": f"same as {AXIS_0_PARAMS} but for axis 2",
                    "type": "optional",
                },
                FLIP_LR: {
                    "default": False,
                    "help": "sometime scan or volume can have a left-right flip in frame (projection/slice) space. For recent NXtomo it should be handled automatically. But for volume you might need to request some flip.",
                    "type": "optional",
                },
                FLIP_UD: {
                    "default": False,
                    "help": "sometime scan or volume can have a up_down flip in frame (projection/slice) space. For recent NXtomo it should be handled automatically. But for volume you might need to request some flip.",
                    "type": "optional",
                },
                RESCALE_FRAMES: {
                    "default": False,
                    "help": "rescale each frame before applying stithcing",
                    "type": "advanced",
                },
                RESCALE_PARAMS: {
                    "default": "",
                    "help": f"parameters for rescaling frames as 'key1=value1;key_2=value2'. Valid Keys are {KEY_RESCALE_MIN_PERCENTILES} and {KEY_RESCALE_MAX_PERCENTILES}.",
                    "type": "advanced",
                },
                STITCHING_KERNELS_EXTRA_PARAMS: {
                    "default": "",
                    "help": f"advanced parameters for some stitching kernels. must be provided as 'key1=value1;key_2=value2'. Valid keys for now are: {KEY_THRESHOLD_FREQUENCY}: threshold to be used by the {OverlapStitchingStrategy.IMAGE_MINIMUM_DIVERGENCE.value} to split images low and high frequencies in Fourier space.",
                    "type": "advanced",
                },
                ALIGNMENT_AXIS_2_FIELD: {
                    "default": "center",
                    "help": f"In case frame have different frame widths how to align them (so along volume axis 2). Valid keys are {[aa.value for aa in AlignmentAxis2]}",
                    "type": "advanced",
                },
                PAD_MODE_FIELD: {
                    "default": "constant",
                    "help": f"pad mode to use for frame alignment. Valid values are 'constant', 'edge', 'linear_ramp', maximum', 'mean', 'median', 'minimum', 'reflect', 'symmetric', 'wrap', and 'empty'. See nupy.pad documentation for details",
                    "type": "advanced",
                },
                AVOID_DATA_DUPLICATION_FIELD: {
                    "default": "1",
                    "help": "When possible (stitching on reconstructed volume and HDF5 volume as input and output) create link to original data instead of duplicating it all. Warning: this will create relative link between the stiched volume and the original reconstructed volume.",
                    "validator": boolean_validator,
                    "type": "advanced",
                },
            },
            OUTPUT_SECTION: {
                OVERWRITE_RESULTS_FIELD: {
                    "default": "1",
                    "help": "What to do in the case where the output file exists.\nBy default, the output data is never overwritten and the process is interrupted if the file already exists.\nSet this option to 1 if you want to overwrite the output files.",
                    "validator": boolean_validator,
                    "type": "required",
                },
            },
            INPUTS_SECTION: {
                INPUT_DATASETS_FIELD: {
                    "default": "",
                    "help": f"Dataset to stitch together. Must be volume for {StitchingType.Z_PREPROC.value} or NXtomo for {StitchingType.Z_POSTPROC.value}",
                    "type": "required",
                },
                STITCHING_SLICES: {
                    "default": "",
                    "help": f"slices to be stitched. Must be given along axis 0 for pre-processing (z) and along axis 1 for post-processing (y)",
                    "type": "advanced",
                },
            },
            SLURM_SECTION: {
                SLURM_PARTITION: {
                    "default": "",
                    "help": "slurm partition to be used. If empty will run locally",
                    "type": "optional",
                },
                SLURM_MEM: {
                    "default": "32GB",
                    "help": "memory to allocate for each job",
                    "type": "optional",
                },
                SLURM_N_JOBS: {
                    "default": 10,
                    "help": "number of job to launch (split computation on N parallel jobs). Once all are finished we will concatenate the result.",
                    "type": "optional",
                },
                SLURM_COR_PER_TASKS: {
                    "default": 4,
                    "help": "number of cor per task launched",
                    "type": "optional",
                },
                SLURM_NUMBER_OF_TASKS: {
                    "default": 1,
                    "help": "(for parallel execution when possible). Split each job into this number of tasks",
                    "type": "optional",
                },
                SLURM_OTHER_OPTIONS: {
                    "default": "",
                    "help": "you can provide axtra options to slurm from this string",
                    "type": "optional",
                },
                SLURM_PREPROCESSING_COMMAND: {
                    "default": "",
                    "help": "python virtual environment to use",
                    "type": "optional",
                },
                SLURM_MODULES_TO_LOADS: {
                    "default": "tomotools/stable",
                    "help": "module to load",
                    "type": "optional",
                },
            },
            NORMALIZATION_BY_SAMPLE_SECTION: {
                NORMALIZATION_BY_SAMPLE_ACTIVE_FIELD: {
                    "default": False,
                    "help": "should we apply frame normalization by a sample or not",
                    "type": "advanced",
                },
                NORMALIZATION_BY_SAMPLE_METHOD: {
                    "default": "median",
                    "help": "method to compute the normalization value",
                    "type": "advanced",
                },
                NORMALIZATION_BY_SAMPLE_SIDE: {
                    "default": "left",
                    "help": "side to pick the sample",
                    "type": "advanced",
                },
                NORMALIZATION_BY_SAMPLE_MARGIN: {
                    "default": 0,
                    "help": "margin (in px) between border and sample",
                    "type": "advanced",
                },
                NORMALIZATION_BY_SAMPLE_WIDTH: {
                    "default": 30,
                    "help": "sample width (in px)",
                    "type": "advanced",
                },
            },
        }

    def to_dict(self):
        """dump configuration to a dict. Must be serializable because might be dump to HDF5 file"""
        return {
            SLURM_SECTION: self.slurm_config.to_dict() if self.slurm_config is not None else SlurmConfig().to_dict(),
            STITCHING_SECTION: {
                STITCHING_TYPE_FIELD: self.stitching_type.value,
                CROSS_CORRELATION_SLICE_FIELD: str(self.slice_for_cross_correlation),
                AXIS_0_POS_PX: _cast_shift_to_str(self.axis_0_pos_px),
                AXIS_0_POS_MM: _cast_shift_to_str(self.axis_0_pos_mm),
                AXIS_0_PARAMS: _dict_to_str(self.axis_0_params or {}),
                AXIS_1_POS_PX: _cast_shift_to_str(self.axis_1_pos_px),
                AXIS_1_POS_MM: _cast_shift_to_str(self.axis_1_pos_mm),
                AXIS_1_PARAMS: _dict_to_str(self.axis_1_params or {}),
                AXIS_2_POS_PX: _cast_shift_to_str(self.axis_2_pos_px),
                AXIS_2_POS_MM: _cast_shift_to_str(self.axis_2_pos_mm),
                AXIS_2_PARAMS: _dict_to_str(self.axis_2_params or {}),
                STITCHING_STRATEGY_FIELD: OverlapStitchingStrategy(self.stitching_strategy).value,
                FLIP_UD: self.flip_ud,
                FLIP_LR: self.flip_lr,
                RESCALE_FRAMES: self.rescale_frames,
                RESCALE_PARAMS: _dict_to_str(self.rescale_params or {}),
                STITCHING_KERNELS_EXTRA_PARAMS: _dict_to_str(self.stitching_kernels_extra_params or {}),
                AVOID_DATA_DUPLICATION_FIELD: not self.duplicate_data,
            },
            OUTPUT_SECTION: {
                OVERWRITE_RESULTS_FIELD: int(
                    self.overwrite_results,
                ),
            },
            NORMALIZATION_BY_SAMPLE_SECTION: self.normalization_by_sample.to_dict(),
        }


class SingleAxisConfigMetaClass(type):
    """
    Metaclass for single axis stitcher in order to aggregate dumper class and axis

    warning: this class is used by tomwer as well
    """

    def __new__(mcls, name, bases, attrs, axis=None):
        # assert axis is not None
        mcls = super().__new__(mcls, name, bases, attrs)
        mcls._axis = axis
        return mcls


@dataclass
class SingleAxisStitchingConfiguration(StitchingConfiguration, metaclass=SingleAxisConfigMetaClass):
    """
    base class to define z-stitching parameters
    """

    slices: slice | tuple | None = (
        None  # slices to reconstruct. Over axis 0 for pre-processing, over axis 1 for post-processing. If None will reconstruct all
    )

    alignment_axis_2: AlignmentAxis2 = AlignmentAxis2.CENTER

    pad_mode: str = "constant"  # pad mode to be used for alignment

    @property
    def axis(self) -> int:
        # self._axis is defined by the metaclass
        return self._axis

    def settle_inputs(self) -> None:
        self.settle_slices()

    def settle_slices(self) -> tuple:
        raise ValueError("Base class")

    def get_output_object(self):
        raise ValueError("Base class")

    def to_dict(self):
        if isinstance(self.slices, slice):
            slices = f"{self.slices.start}:{self.slices.stop}:{self.slices.step}"
        elif self.slices in ("", None):
            slices = ""
        else:
            slices = ";".join(str(s) for s in self.slices)
        return concatenate_dict(
            super().to_dict(),
            {
                INPUTS_SECTION: {
                    STITCHING_SLICES: slices,
                },
                STITCHING_SECTION: {
                    ALIGNMENT_AXIS_2_FIELD: self.alignment_axis_2.value,
                    PAD_MODE_FIELD: self.pad_mode,
                },
            },
        )


@dataclass
class PreProcessedSingleAxisStitchingConfiguration(SingleAxisStitchingConfiguration):
    """
    base class to define z-stitching parameters
    """

    input_scans: tuple = ()  # tuple of ScanBase
    output_file_path: str = ""
    output_data_path: str = ""
    output_nexus_version: float | None = None
    pixel_size: float | None = None

    @property
    def stitching_type(self) -> StitchingType:
        if self.axis == 0:
            return StitchingType.Z_PREPROC
        elif self.axis == 1:
            return StitchingType.Y_PREPROC
        else:
            raise ValueError(
                "unexpected axis value. Only stitching over axis 0 (aka z) and 1 (aka y) are handled. Current axis value is %s",
                self.axis,
            )

    def get_output_object(self):
        return NXtomoScan(
            scan=self.output_file_path,
            entry=self.output_data_path,
        )

    def settle_inputs(self) -> None:
        super().settle_inputs()
        self.settle_input_scans()

    def settle_input_scans(self):
        self.input_scans = [
            (
                Factory.create_tomo_object_from_identifier(identifier)
                if isinstance(identifier, (str, ScanIdentifier))
                else identifier
            )
            for identifier in self.input_scans
        ]

    def slice_idx_from_str_to_int(self, index):
        if isinstance(index, str):
            index = index.lower()
            if index == "first":
                return 0
            elif index == "last":
                return len(self.input_scans[0].projections) - 1
            elif index == "middle":
                return max(len(self.input_scans[0].projections) // 2 - 1, 0)
        return int(index)

    def settle_slices(self) -> tuple:
        """
        interpret the slices to be stitched if needed

        Nore: if slices is an instance of slice will redefine start and stop to avoid having negative indexes

        :return: (slices:[slice,Iterable], n_proj:int)
        :rtype: tuple
        """
        slices = self.slices
        if isinstance(slices, Sized) and len(slices) == 0:
            # in this case will stitch them all
            slices = None
        if len(self.input_scans) == 0:
            raise ValueError("No input scan provided")
        if slices is None:
            slices = slice(0, len(self.input_scans[0].projections), 1)
            n_proj = slices.stop
        elif isinstance(slices, slice):
            # force slices indices to be positive
            start = slices.start
            if start < 0:
                start += len(self.input_scans[0].projections) + 1
            stop = slices.stop
            if stop < 0:
                stop += len(self.input_scans[0].projections) + 1
            step = slices.step
            if step is None:
                step = 1
            n_proj = ceil((stop - start) / step)
            # update slices for iteration simplify things
            slices = slice(start, stop, step)
        elif isinstance(slices, (tuple, list)):
            n_proj = len(slices)
            slices = [self.slice_idx_from_str_to_int(s) for s in slices]
        else:
            raise TypeError(f"slices is expected to be a tuple or a lice. Not {type(slices)}")
        self.slices = slices
        return slices, n_proj

    def to_dict(self):
        if self.pixel_size is None:
            pixel_size_mm = ""
        else:
            pixel_size_mm = (self.pixel_size * _ureg.meter).to(_ureg.millimeter).magnitude
        return concatenate_dict(
            super().to_dict(),
            {
                PRE_PROC_SECTION: {
                    DATA_FILE_FIELD: self.output_file_path,
                    DATA_PATH_FIELD: self.output_data_path,
                    NEXUS_VERSION_FIELD: self.output_nexus_version,
                },
                INPUTS_SECTION: {
                    INPUT_DATASETS_FIELD: ";".join(
                        [str(scan.get_identifier()) for scan in self.input_scans],
                    ),
                    INPUT_PIXEL_SIZE_MM: pixel_size_mm,
                },
            },
        )

    @staticmethod
    def get_description_dict() -> dict:
        return concatenate_dict(
            SingleAxisStitchingConfiguration.get_description_dict(),
            {
                PRE_PROC_SECTION: {
                    DATA_FILE_FIELD: {
                        "default": "",
                        "help": "output nxtomo file path",
                        "type": "required",
                    },
                    DATA_PATH_FIELD: {
                        "default": "",
                        "help": "output nxtomo data path",
                        "type": "required",
                    },
                    NEXUS_VERSION_FIELD: {
                        "default": "",
                        "help": "nexus version. If not provided will pick the latest one know",
                        "type": "required",
                    },
                },
            },
        )

    @classmethod
    def from_dict(cls, config: dict):
        if not isinstance(config, dict):
            raise TypeError(f"config is expected to be a dict and not {type(config)}")
        inputs_scans_str = config.get(INPUTS_SECTION, {}).get(INPUT_DATASETS_FIELD, None)
        if inputs_scans_str in (None, ""):
            input_scans = []
        else:
            input_scans = identifiers_as_str_to_instances(inputs_scans_str)

        output_file_path = config.get(PRE_PROC_SECTION, {}).get(DATA_FILE_FIELD, None)

        nexus_version = config.get(PRE_PROC_SECTION, {}).get(NEXUS_VERSION_FIELD, None)
        if nexus_version in (None, ""):
            nexus_version = nxtomo.LATEST_VERSION
        else:
            nexus_version = float(nexus_version)
        pixel_size = config.get(INPUT_PIXEL_SIZE_MM, "").replace(" ", "")
        if pixel_size == "":
            pixel_size = None
        else:
            pixel_size = (float(pixel_size) * _ureg.millimeter).to_base_units().magnitude

        return cls(
            stitching_strategy=OverlapStitchingStrategy(
                config[STITCHING_SECTION].get(
                    STITCHING_STRATEGY_FIELD,
                    OverlapStitchingStrategy.COSINUS_WEIGHTS,
                ),
            ),
            axis_0_pos_px=str_to_shifts(config[STITCHING_SECTION].get(AXIS_0_POS_PX, None)),
            axis_0_pos_mm=str_to_shifts(config[STITCHING_SECTION].get(AXIS_0_POS_MM, None)),
            axis_0_params=_valid_shifts_params(_str_to_dict(config[STITCHING_SECTION].get(AXIS_0_PARAMS, {}))),
            axis_1_pos_px=str_to_shifts(config[STITCHING_SECTION].get(AXIS_1_POS_PX, None)),
            axis_1_pos_mm=str_to_shifts(config[STITCHING_SECTION].get(AXIS_1_POS_MM, None)),
            axis_1_params=_valid_shifts_params(
                _str_to_dict(
                    config[STITCHING_SECTION].get(AXIS_1_PARAMS, {}),
                )
            ),
            axis_2_pos_px=str_to_shifts(config[STITCHING_SECTION].get(AXIS_2_POS_PX, None)),
            axis_2_pos_mm=str_to_shifts(config[STITCHING_SECTION].get(AXIS_2_POS_MM, None)),
            axis_2_params=_valid_shifts_params(
                _str_to_dict(
                    config[STITCHING_SECTION].get(AXIS_2_PARAMS, {}),
                )
            ),
            input_scans=input_scans,
            output_file_path=output_file_path,
            output_data_path=config.get(PRE_PROC_SECTION, {}).get(DATA_PATH_FIELD, "entry_from_stitchig"),
            overwrite_results=config[STITCHING_SECTION].get(OVERWRITE_RESULTS_FIELD, True),
            output_nexus_version=nexus_version,
            slices=_slices_to_list_or_slice(config[INPUTS_SECTION].get(STITCHING_SLICES, None)),
            slurm_config=SlurmConfig.from_dict(config.get(SLURM_SECTION, {})),
            slice_for_cross_correlation=config[STITCHING_SECTION].get(CROSS_CORRELATION_SLICE_FIELD, "middle"),
            pixel_size=pixel_size,
            flip_ud=_scalar_or_tuple_to_bool_or_tuple_of_bool(config[STITCHING_SECTION].get(FLIP_UD, False)),
            flip_lr=_scalar_or_tuple_to_bool_or_tuple_of_bool(config[STITCHING_SECTION].get(FLIP_LR, False)),
            rescale_frames=convert_to_bool(config[STITCHING_SECTION].get(RESCALE_FRAMES, 0))[0],
            rescale_params=_str_to_dict(config[STITCHING_SECTION].get(RESCALE_PARAMS, {})),
            stitching_kernels_extra_params=_valid_stitching_kernels_params(
                _str_to_dict(
                    config[STITCHING_SECTION].get(STITCHING_KERNELS_EXTRA_PARAMS, {}),
                )
            ),
            alignment_axis_2=AlignmentAxis2(
                config[STITCHING_SECTION].get(ALIGNMENT_AXIS_2_FIELD, AlignmentAxis2.CENTER)
            ),
            pad_mode=config[STITCHING_SECTION].get(PAD_MODE_FIELD, "constant"),
            duplicate_data=not _scalar_or_tuple_to_bool_or_tuple_of_bool(
                config[STITCHING_SECTION].get(AVOID_DATA_DUPLICATION_FIELD, False)
            ),
        )


@dataclass
class PostProcessedSingleAxisStitchingConfiguration(SingleAxisStitchingConfiguration):
    """
    base class to define z-stitching parameters
    """

    input_volumes: tuple = ()  # tuple of VolumeBase
    output_volume: VolumeIdentifier | None = None
    voxel_size: float | None = None
    alignment_axis_1: AlignmentAxis1 = AlignmentAxis1.CENTER

    @property
    def stitching_type(self) -> StitchingType:
        if self.axis == 0:
            return StitchingType.Z_POSTPROC
        else:
            raise ValueError(f"unexpected axis value. Only stitching over axis 0 (aka z) is handled. Not {self.axis}")

    def get_output_object(self):
        return self.output_volume

    def settle_inputs(self) -> None:
        super().settle_inputs()
        self.settle_input_volumes()

    def settle_input_volumes(self):
        self.input_volumes = [
            (
                Factory.create_tomo_object_from_identifier(identifier)
                if isinstance(identifier, (str, VolumeIdentifier))
                else identifier
            )
            for identifier in self.input_volumes
        ]

    def slice_idx_from_str_to_int(self, index):
        if isinstance(index, str):
            index = index.lower()
            if index == "first":
                return 0
            elif index == "last":
                return self.input_volumes[0].get_volume_shape()[1] - 1
            elif index == "middle":
                return max(self.input_volumes[0].get_volume_shape()[1] // 2 - 1, 0)
        return int(index)

    def settle_slices(self) -> tuple:
        """
        interpret the slices to be stitched if needed

        Nore: if slices is an instance of slice will redefine start and stop to avoid having negative indexes

        :return: (slices:[slice,Iterable], n_proj:int)
        :rtype: tuple
        """
        slices = self.slices
        if isinstance(slices, Sized) and len(slices) == 0:
            # in this case will stitch them all
            slices = None
        if len(self.input_volumes) == 0:
            raise ValueError("No input volume provided. Cannot settle slices")
        if slices is None:
            # before alignment was existing
            # slices = slice(0, self.input_volumes[0].get_volume_shape()[1], 1)
            slices = slice(
                0,
                max([volume.get_volume_shape()[1] for volume in self.input_volumes]),
                1,
            )
            n_slices = slices.stop
        if isinstance(slices, slice):
            # force slices indices to be positive
            start = slices.start
            if start < 0:
                start += max([volume.get_volume_shape()[1] for volume in self.input_volumes]) + 1
            stop = slices.stop
            if stop < 0:
                stop += max([volume.get_volume_shape()[1] for volume in self.input_volumes]) + 1
            step = slices.step
            if step is None:
                step = 1
            n_slices = ceil((stop - start) / step)
            # update slices for iteration simplify things
            slices = slice(start, stop, step)
        elif isinstance(slices, Iterable):
            n_slices = len(slices)
            slices = [self.slice_idx_from_str_to_int(s) for s in slices]
        else:
            raise TypeError(f"slices is expected to be a tuple or a slice. Not {type(slices)}")
        self.slices = slices
        return slices, n_slices

    @classmethod
    def from_dict(cls, config: dict):
        if not isinstance(config, dict):
            raise TypeError(f"config is expected to be a dict and not {type(config)}")
        inputs_volumes_str = config.get(INPUTS_SECTION, {}).get(INPUT_DATASETS_FIELD, None)
        if inputs_volumes_str in (None, ""):
            input_volumes = []
        else:
            input_volumes = identifiers_as_str_to_instances(inputs_volumes_str)
        overwrite_results = config[STITCHING_SECTION].get(OVERWRITE_RESULTS_FIELD, True) in ("1", True, "True", 1)
        output_volume = config.get(POST_PROC_SECTION, {}).get(OUTPUT_VOLUME, None)
        if output_volume is not None:
            output_volume = Factory.create_tomo_object_from_identifier(output_volume)
            output_volume.overwrite = overwrite_results
        voxel_size = config.get(INPUTS_SECTION, {}).get(INPUT_VOXEL_SIZE_MM, "")
        voxel_size = voxel_size.replace(" ", "")
        if voxel_size == "":
            voxel_size = None
        else:
            voxel_size = (float(voxel_size) * _ureg.millimeter).to_base_units().magnitude

        # on the next section the one with a default value qre the optional one
        return cls(
            stitching_strategy=OverlapStitchingStrategy(
                config[STITCHING_SECTION].get(
                    STITCHING_STRATEGY_FIELD,
                    OverlapStitchingStrategy.COSINUS_WEIGHTS,
                ),
            ),
            axis_0_pos_px=str_to_shifts(config[STITCHING_SECTION].get(AXIS_0_POS_PX, None)),
            axis_0_pos_mm=str_to_shifts(config[STITCHING_SECTION].get(AXIS_0_POS_MM, None)),
            axis_0_params=_valid_shifts_params(config[STITCHING_SECTION].get(AXIS_0_PARAMS, {})),
            axis_1_pos_px=str_to_shifts(config[STITCHING_SECTION].get(AXIS_1_POS_PX, None)),
            axis_1_pos_mm=str_to_shifts(config[STITCHING_SECTION].get(AXIS_1_POS_MM, None)),
            axis_1_params=_valid_shifts_params(config[STITCHING_SECTION].get(AXIS_1_PARAMS, {})),
            axis_2_pos_px=str_to_shifts(config[STITCHING_SECTION].get(AXIS_2_POS_PX, None)),
            axis_2_pos_mm=str_to_shifts(config[STITCHING_SECTION].get(AXIS_2_POS_MM, None)),
            axis_2_params=_valid_shifts_params(config[STITCHING_SECTION].get(AXIS_2_PARAMS, {})),
            input_volumes=input_volumes,
            output_volume=output_volume,
            overwrite_results=overwrite_results,
            slices=_slices_to_list_or_slice(config[INPUTS_SECTION].get(STITCHING_SLICES, None)),
            slurm_config=SlurmConfig.from_dict(config.get(SLURM_SECTION, {})),
            voxel_size=voxel_size,
            slice_for_cross_correlation=config[STITCHING_SECTION].get(CROSS_CORRELATION_SLICE_FIELD, "middle"),
            flip_ud=_scalar_or_tuple_to_bool_or_tuple_of_bool(config[STITCHING_SECTION].get(FLIP_UD, False)),
            flip_lr=_scalar_or_tuple_to_bool_or_tuple_of_bool(config[STITCHING_SECTION].get(FLIP_LR, False)),
            rescale_frames=convert_to_bool(config[STITCHING_SECTION].get(RESCALE_FRAMES, 0))[0],
            rescale_params=_str_to_dict(config[STITCHING_SECTION].get(RESCALE_PARAMS, {})),
            stitching_kernels_extra_params=_valid_stitching_kernels_params(
                _str_to_dict(
                    config[STITCHING_SECTION].get(STITCHING_KERNELS_EXTRA_PARAMS, {}),
                )
            ),
            alignment_axis_1=AlignmentAxis1(
                config[STITCHING_SECTION].get(ALIGNMENT_AXIS_1_FIELD, AlignmentAxis1.CENTER)
            ),
            alignment_axis_2=AlignmentAxis2(
                config[STITCHING_SECTION].get(ALIGNMENT_AXIS_2_FIELD, AlignmentAxis2.CENTER)
            ),
            pad_mode=config[STITCHING_SECTION].get(PAD_MODE_FIELD, "constant"),
            duplicate_data=not _scalar_or_tuple_to_bool_or_tuple_of_bool(
                config[STITCHING_SECTION].get(AVOID_DATA_DUPLICATION_FIELD, False)
            ),
            normalization_by_sample=NormalizationBySample.from_dict(config.get(NORMALIZATION_BY_SAMPLE_SECTION, {})),
        )

    def to_dict(self):
        if self.voxel_size is None:
            voxel_size_mm = ""
        else:
            voxel_size_mm = numpy.array((self.voxel_size * _ureg.meter).to(_ureg.millimeter).magnitude)

        return concatenate_dict(
            super().to_dict(),
            {
                INPUTS_SECTION: {
                    INPUT_DATASETS_FIELD: [volume.get_identifier().to_str() for volume in self.input_volumes],
                    INPUT_VOXEL_SIZE_MM: voxel_size_mm,
                },
                POST_PROC_SECTION: {
                    OUTPUT_VOLUME: (
                        self.output_volume.get_identifier().to_str() if self.output_volume is not None else ""
                    ),
                },
                STITCHING_SECTION: {
                    ALIGNMENT_AXIS_1_FIELD: self.alignment_axis_1.value,
                },
            },
        )

    @staticmethod
    def get_description_dict() -> dict:
        return concatenate_dict(
            SingleAxisStitchingConfiguration.get_description_dict(),
            {
                POST_PROC_SECTION: {
                    OUTPUT_VOLUME: {
                        "default": "",
                        "help": "identifier of the output volume. Like hdf5:volume:[file_path]?path=[data_path] for an HDF5 volume",
                        "type": "required",
                    },
                },
                STITCHING_SECTION: {
                    ALIGNMENT_AXIS_1_FIELD: {
                        "default": "center",
                        "help": f"alignment to apply over axis 1 if needed. Valid values are {[aa for aa in AlignmentAxis1]}",
                        "type": "advanced",
                    }
                },
            },
        )


def identifiers_as_str_to_instances(list_identifiers_as_str: str) -> tuple:
    # convert str to a list of str that should represent identifiers
    if isinstance(list_identifiers_as_str, str):
        list_identifiers_as_str = list_identifiers_as_str.lstrip("[").lstrip("(")
        list_identifiers_as_str = list_identifiers_as_str.rstrip("]").rstrip(")")
        identifiers_as_str = convert_str_to_tuple(list_identifiers_as_str.replace(";", ","))
    else:
        identifiers_as_str = list_identifiers_as_str
    if identifiers_as_str is None:
        return tuple()
    # convert identifiers as string to IdentifierType instances
    return tuple(
        [Factory.create_tomo_object_from_identifier(identifier_as_str) for identifier_as_str in identifiers_as_str]
    )


def dict_to_config_obj(config: dict):
    if not isinstance(config, dict):
        raise TypeError
    stitching_type = config.get(STITCHING_SECTION, {}).get(STITCHING_TYPE_FIELD, None)
    if stitching_type is None:
        raise ValueError("Unable to find stitching type from config dict")
    else:
        stitching_type = StitchingType(stitching_type)
        if stitching_type is StitchingType.Z_POSTPROC:
            return PostProcessedZStitchingConfiguration.from_dict(config)
        elif stitching_type is StitchingType.Z_PREPROC:
            return PreProcessedZStitchingConfiguration.from_dict(config)
        elif stitching_type is StitchingType.Y_PREPROC:
            return PreProcessedYStitchingConfiguration.from_dict(config)
        else:
            raise NotImplementedError(f"stitching type {stitching_type.value} not handled yet")


def get_default_stitching_config(stitching_type: StitchingType | str | None) -> tuple:
    """
    Return a default configuration for doing stitching.

    :param stitching_type: if None then return a configuration were use can provide inputs for any
                           of the stitching.
                           Else return config dict dedicated to a particular stitching
    :return: (config, section comments)
    """
    if stitching_type is None:
        return concatenate_dict(z_postproc_stitching_config, z_preproc_stitching_config)

    stitching_type = StitchingType(stitching_type)
    if stitching_type is StitchingType.Z_POSTPROC:
        return z_postproc_stitching_config
    elif stitching_type is StitchingType.Z_PREPROC:
        return z_preproc_stitching_config
    elif stitching_type is StitchingType.Y_PREPROC:
        return y_preproc_stitching_config
    else:
        raise NotImplementedError


class PreProcessedYStitchingConfiguration(PreProcessedSingleAxisStitchingConfiguration, axis=1):
    pass


class PreProcessedZStitchingConfiguration(PreProcessedSingleAxisStitchingConfiguration, axis=0):
    pass


class PostProcessedZStitchingConfiguration(PostProcessedSingleAxisStitchingConfiguration, axis=0):
    pass


y_preproc_stitching_config = PreProcessedYStitchingConfiguration.get_description_dict()

z_preproc_stitching_config = PreProcessedZStitchingConfiguration.get_description_dict()

z_postproc_stitching_config = PostProcessedZStitchingConfiguration.get_description_dict()
