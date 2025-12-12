# ruff: noqa: F405
import os

path = os.path
from ..utils import check_supported, deprecation_warning, get_num_threads, is_writeable
from .params import *  # noqa: F403

"""
A validator is a function with
  - input: a value
  - output: the input value, or a modified input value
  - possibly raising exceptions in case of invalid value.
"""


# ------------------------------------------------------------------------------
# ---------------------------- Utils -------------------------------------------
# ------------------------------------------------------------------------------


def raise_error(section, key, msg=""):
    raise ValueError("Invalid value for %s/%s: %s" % (section, key, msg))


def validator(func):
    """
    Common decorator for all validator functions.
    It modifies the signature of the decorated functions !
    """

    def wrapper(section, key, value):
        try:
            res = func(value)
        except AssertionError as e:
            raise_error(section, key, e)
        return res

    return wrapper


def convert_to_int(val):
    val_int = 0
    try:
        val_int = int(val)
        conversion_error = None
    except ValueError as exc:
        conversion_error = exc
    return val_int, conversion_error


def convert_to_float(val):
    val_float = 0.0
    try:
        val_float = float(val)
        conversion_error = None
    except ValueError as exc:
        conversion_error = exc
    return val_float, conversion_error


def convert_to_bool(val):
    val_int, error = convert_to_int(val)
    res = None
    if not error:
        res = val_int > 0
    else:
        if val.lower() in ["yes", "true", "y"]:
            res = True
            error = None
        if val.lower() in ["no", "false", "n"]:
            res = False
            error = None
    return res, error


def str2bool(val):
    """This is an interface to convert_to_bool and it is meant
    to work as a class: in argparse interface the type argument can be set to float, int .. in general to a class.
    The argument value is then created, at parsing time, by typecasting the input string to the given class.
    A possibly occuring exception then trigger, in case, the display explanation provided by the argparse library.
    All what this methods does is simply trying to convert an argument into a bool, and return it,
    or generate an exception if there is a problem
    """
    import argparse

    res, error = convert_to_bool(val)
    if error:
        raise argparse.ArgumentTypeError(error)
    else:
        return res


def convert_to_bool_noerr(val):
    res, err = convert_to_bool(val)
    if err is not None:
        raise ValueError("Could not convert to boolean: %s" % str(val))
    return res


def name_range_checker(name, available_names, descr):
    """
    Check whether a parameter name is valid, against a list or dictionary of names.
    """
    name = name.strip().lower()
    valid = name in available_names
    if isinstance(available_names, dict):
        # handle replacements, eg. {"edge": "edges"}
        name = available_names[name]
        # we could use .keys() instead to be more permissive to the user
        available_names_str = str(set(available_names.values()))
    else:
        # assuming list
        available_names_str = str(available_names)
    assert valid, "Invalid %s '%s'. Available are %s" % (descr, name, available_names_str)
    return name


# ------------------------------------------------------------------------------
# ---------------------------- Validators --------------------------------------
# ------------------------------------------------------------------------------


@validator
def optional_string_validator(val):
    if len(val.strip()) == 0:
        return None
    return val


@validator
def file_name_validator(name):
    assert len(name) >= 1, "Name should be non-empty"
    return name


@validator
def file_location_validator(location):
    assert path.isfile(location), "location must be a file"
    return os.path.abspath(location)


@validator
def optional_file_location_validator(location):
    if len(location.strip()) > 0:
        assert path.isfile(location), "location must be a file"
        return os.path.abspath(location)
    return None


@validator
def optional_values_file_validator(location):
    if len(location.strip()) == 0:
        return None
    if path.splitext(location)[-1].strip() == "":
        # Assume path to h5 dataset. Validation is done later.
        if "://" not in location:
            location = "silx://" + os.path.abspath(location)
    else:
        # Assume plaintext file
        assert path.isfile(location), "Invalid file path"
        location = os.path.abspath(location)
    return location


@validator
def directory_location_validator(location):
    assert path.isdir(location), "location must be a directory"
    return os.path.abspath(location)


@validator
def optional_directory_location_validator(location):
    if len(location.strip()) > 0:
        assert is_writeable(location), "Directory must be writeable"
        return os.path.abspath(location)
    return None


@validator
def dataset_location_validator(location):
    if not (path.isdir(location)):
        assert (
            path.isfile(location) and path.splitext(location)[-1].split(".")[-1].lower() in files_formats
        ), "Dataset location must be a directory or a HDF5 file"
    return os.path.abspath(location)


@validator
def directory_writeable_validator(location):
    assert is_writeable(location), "Directory must be writeable"
    return os.path.abspath(location)


@validator
def optional_output_directory_validator(location):
    if len(location.strip()) > 0:
        return directory_writeable_validator(location)
    return None


@validator
def optional_output_file_path_validator(location):
    if len(location.strip()) > 0:
        dirname, fname = path.split(location)
        assert os.access(dirname, os.W_OK), "Directory must be writeable"
        return os.path.abspath(location)
    return None


@validator
def integer_validator(val):
    val_int, error = convert_to_int(val)
    assert error is None, "number must be an integer"
    return val_int


@validator
def nonnegative_integer_validator(val):
    val_int, error = convert_to_int(val)
    assert error is None and val_int >= 0, "number must be a non-negative integer"
    return val_int


@validator
def positive_integer_validator(val):
    val_int, error = convert_to_int(val)
    assert error is None and val_int > 0, "number must be a positive integer"
    return val_int


@validator
def optional_positive_integer_validator(val):
    if len(val.strip()) == 0:
        return None
    val_int, error = convert_to_int(val)
    assert error is None and val_int > 0, "number must be a positive integer"
    return val_int


@validator
def nonzero_integer_validator(val):
    val_int, error = convert_to_int(val)
    assert error is None and val_int != 0, "number must be a non-zero integer"
    return val_int


@validator
def binning_validator(val):
    if val == "":
        val = "1"
    val_int, error = convert_to_int(val)
    assert error is None and val_int >= 0, "number must be a non-negative integer"
    return max(1, val_int)


@validator
def projections_subsampling_validator(val):
    val = val.strip()
    err_msg = "projections_subsampling: expected one positive integer or two integers in the format step:begin"
    if ":" not in val:
        val += ":0"
    step, begin = val.split(":")
    step_int, error1 = convert_to_int(step)
    begin_int, error2 = convert_to_int(begin)
    if error1 is not None or error2 is not None or step_int <= 0 or begin_int < 0:
        raise ValueError(err_msg)
    return step_int, begin_int


@validator
def optional_file_name_validator(val):
    if len(val) > 0:
        assert len(val) >= 1, "Name should be non-empty"
        assert path.basename(val) == val, "File name should not be a path (no '/')"
        return val
    return None


@validator
def boolean_validator(val):
    res, error = convert_to_bool(val)
    assert error is None, "Invalid boolean value"
    return res


@validator
def boolean_or_auto_validator(val):
    res, error = convert_to_bool(val)
    if error is not None:
        assert val.lower() == "auto", "Valid values are 0, 1 and auto"
        return val
    return res


@validator
def float_validator(val):
    val_float, error = convert_to_float(val)
    assert error is None, "Invalid number"
    return val_float


@validator
def optional_float_validator(val):
    if isinstance(val, float):
        return val
    elif len(val.strip()) >= 1:
        val_float, error = convert_to_float(val)
        assert error is None, "Invalid number"
    else:
        val_float = None
    return val_float


@validator
def optional_nonzero_float_validator(val):
    if isinstance(val, float):
        val_float = val
    elif len(val.strip()) >= 1:
        val_float, error = convert_to_float(val)
        assert error is None, "Invalid number"
    else:
        val_float = None
    if val_float is not None:  # noqa: SIM102
        if abs(val_float) < 1e-6:
            val_float = None
    return val_float


@validator
def optional_tuple_of_floats_validator(val):
    if len(val.strip()) == 0:
        return None
    err_msg = "Expected a tuple of two numbers, but got %s" % val
    try:
        res = tuple(float(x) for x in val.strip("()").split(","))
    except Exception:
        raise ValueError(err_msg)
    if len(res) != 2:
        raise ValueError(err_msg)
    return res


@validator
def cor_validator(val):
    val_float, error = convert_to_float(val)
    if error is None:
        return val_float
    if len(val.strip()) == 0:
        return None
    val = name_range_checker(val, cor_methods, "center of rotation estimation method")
    return val


@validator
def tilt_validator(val):
    val_float, error = convert_to_float(val)
    if error is None:
        return val_float
    if len(val.strip()) == 0:
        return None
    val = name_range_checker(val, tilt_methods, "automatic detector tilt estimation method")
    return val


@validator
def slice_num_validator(val):
    val_int, error = convert_to_int(val)
    if error is None:
        return val_int
    else:
        assert val in [
            "first",
            "middle",
            "last",
        ], "Expected start_z and end_z to be either a number or first, middle or last"
        return val


@validator
def generic_options_validator(val):
    if len(val.strip()) == 0:
        return None
    return val


cor_options_validator = generic_options_validator


@validator
def cor_slice_validator(val):
    if len(val) == 0:
        return None
    val_int, error = convert_to_int(val)
    if error:
        supported = ["top", "first", "bottom", "last", "middle"]
        assert val in supported, "Invalid value, must be a number or one of %s" % supported
        return val
    else:
        return val_int


@validator
def flatfield_validator(val):
    ret = name_range_checker(val, flatfield_modes, "flatfield mode")
    if ret in ["force-load", "force-compute"]:
        deprecation_warning(
            f"Using 'flatfield = {ret}' is deprecated since version 2025.1.0. Please use the parameter 'flatfield_loading_mode'",
        )
    return ret


@validator
def flatfield_loading_mode_validator(val):
    return name_range_checker(val, flatfield_loading_mode, "flatfield mode")


@validator
def phase_method_validator(val):
    return name_range_checker(val, phase_retrieval_methods, "phase retrieval method")


@validator
def detector_distortion_correction_validator(val):
    return name_range_checker(
        val,
        detector_distortion_correction_methods,
        "detector_distortion_correction_methods",
    )


@validator
def unsharp_method_validator(val):
    return name_range_checker(val, unsharp_methods, "unsharp mask method")


@validator
def padding_mode_validator(val):
    return name_range_checker(val, padding_modes, "padding mode")


@validator
def reconstruction_method_validator(val):
    return name_range_checker(val, reconstruction_methods, "reconstruction method")


@validator
def fbp_filter_name_validator(val):
    return name_range_checker(
        val,
        fbp_filters,
        "FBP filter",
    )


@validator
def reconstruction_implementation_validator(val):
    return name_range_checker(
        val,
        reco_implementations,
        "Reconstruction method implementation",
    )


@validator
def optimization_algorithm_name_validator(val):
    return name_range_checker(val, optim_algorithms, "optimization algorithm name")


@validator
def output_file_format_validator(val):
    return name_range_checker(val, files_formats, "output file format")


@validator
def distribution_method_validator(val):
    val = name_range_checker(val, distribution_methods, "workload distribution method")
    # TEMP.
    if val != "local":
        raise NotImplementedError("Computation method '%s' is not implemented yet" % val)
    # --
    return val


@validator
def sino_normalization_validator(val):
    val = name_range_checker(val, sino_normalizations, "sinogram normalization method")
    return val


@validator
def sino_deringer_methods(val):
    val = name_range_checker(
        val,
        rings_methods,
        "sinogram rings artefacts correction method",
    )
    return val


@validator
def list_of_int_validator(val):
    ids = val.replace(",", " ").split()
    res = list(map(convert_to_int, ids))
    err = list(filter(lambda x: x[1] is not None or x[0] < 0, res))
    if err != []:
        raise ValueError("Could not convert to a list of GPU IDs: %s" % val)
    return list(set(map(lambda x: x[0], res)))


@validator
def num_threads_validator(val):
    err_msg = f"Expected either an integer or a fraction of integers (eg. 1/2) for 'num_threads', but got {val}"
    val_int, err = convert_to_int(val)
    if err is None:
        return val_int
    # COMPAT. with percentage (older config files)
    if "%" in val:
        n_cpus = get_num_threads()
        try:
            n_cpus = int((float(val.strip("%")) / 100) * get_num_threads())
        except:
            raise ValueError(f"Could not extract a percentage from: {val}")
        return n_cpus
    #
    if "/" not in val:
        raise ValueError(err_msg)
    num, denom = val.split("/")
    num, err_n = convert_to_int(num)
    denom, err_d = convert_to_int(denom)
    if err_n is not None or err_d is not None:
        raise ValueError(err_msg)
    return int((num / denom) * get_num_threads())


@validator
def list_of_shift_validator(values):
    ids = values.replace(" ", "").split(",")
    return [int(val) if val not in ("auto", "'auto'", '"auto"') else "auto" for val in ids]


@validator
def list_of_tomoscan_identifier(val):
    # TODO: insure those are valid tomoscan identifier
    return val


@validator
def resources_validator(val):
    val = val.strip()
    is_percentage = False
    if "%" in val:
        is_percentage = True
        val = val.replace("%", "")
    val_float, conversion_error = convert_to_float(val)
    assert conversion_error is None, str("Error while converting %s to float" % val)
    return (val_float, is_percentage)


@validator
def walltime_validator(val):
    # HH:mm:ss
    vals = val.strip().split(":")
    error_msg = "Invalid walltime format, expected HH:mm:ss"
    assert len(vals) == 3, error_msg
    hours, mins, secs = vals
    hours, err1 = convert_to_int(hours)
    mins, err2 = convert_to_int(mins)
    secs, err3 = convert_to_int(secs)
    assert err1 is None and err2 is None and err3 is None, error_msg
    err = hours < 0 or mins < 0 or mins > 59 or secs < 0 or secs > 59
    assert err is False, error_msg
    return hours, mins, secs


@validator
def nonempty_string_validator(val):
    assert val != "", "Value cannot be empty"
    return val


@validator
def logging_validator(val):
    return name_range_checker(val, log_levels, "logging level")


@validator
def exclude_projections_validator(val):
    val = val.strip()
    if val == "":
        return None
    if path.isfile(val):
        # previous/default behavior
        return {"type": "indices", "file": val}
    if "=" not in val:
        raise ValueError(
            "exclude_projections: expected either 'angles=angles_file.txt' or 'indices=indices_file.txt' or 'angular_range=[a,b]'"
        )
    excl_type, excl_val = val.split("=")
    excl_type = excl_type.strip()
    excl_val = excl_val.strip()
    check_supported(excl_type, exclude_projections_type.keys(), "exclude_projections type")
    if excl_type == "angular_range":

        def _get_range(range_val):
            for c in ["(", ")", "[", "]"]:
                range_val = range_val.replace(c, "")
            r_min, r_max = range_val.split(",")
            return (float(r_min), float(r_max))

        return {"type": "angular_range", "range": _get_range(excl_val)}
    else:
        return {"type": excl_type, "file": excl_val}


@validator
def no_validator(val):
    return val
