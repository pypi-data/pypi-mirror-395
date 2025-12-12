import os
import posixpath
from multiprocessing.pool import ThreadPool
import numpy as np
from silx.io.dictdump import dicttonx, nxtodict
from ..misc.binning import binning as image_binning
from ..io.utils import get_first_hdf5_entry
from ..pipeline.config_validators import optional_tuple_of_floats_validator, optional_positive_integer_validator
from .cli_configs import ShrinkConfig
from .utils import parse_params_values


def access_nested_dict(dict_, path, default=None):
    items = [s for s in path.split(posixpath.sep) if len(s) > 0]
    if len(items) == 1:
        return dict_.get(items[0], default)
    if items[0] not in dict_:
        return default
    return access_nested_dict(dict_[items[0]], posixpath.sep.join(items[1:]))


def set_nested_dict_value(dict_, path, val):
    dirname, basename = posixpath.split(path)
    sub_dict = access_nested_dict(dict_, dirname)
    sub_dict[basename] = val


def shrink_dataset(input_file, output_file, binning=None, subsampling=None, entry=None, n_threads=1):
    entry = entry or get_first_hdf5_entry(input_file)
    data_dict = nxtodict(input_file, path=entry, dereference_links=False)

    to_subsample = [
        "control/data",
        "instrument/detector/count_time",
        "instrument/detector/data",
        "instrument/detector/image_key",
        "instrument/detector/image_key_control",
        "instrument/detector/sequence_number",
        "sample/rotation_angle",
        "sample/x_translation",
        "sample/y_translation",
        "sample/z_translation",
    ]

    detector_data = access_nested_dict(data_dict, "instrument/detector/data")
    if detector_data is None:
        raise ValueError("No data found in %s entry %s" % (input_file, entry))

    if binning is not None:

        def _apply_binning(img_res_tuple):
            img, res = img_res_tuple
            res[:] = image_binning(img, binning)

        data_binned = np.zeros(
            (detector_data.shape[0], detector_data.shape[1] // binning[0], detector_data.shape[2] // binning[1]),
            detector_data.dtype,
        )
        with ThreadPool(n_threads) as tp:
            tp.map(_apply_binning, zip(detector_data, data_binned))
        detector_data = data_binned
        set_nested_dict_value(data_dict, "instrument/detector/data", data_binned)

    if subsampling is not None:
        for item_path in to_subsample:
            item_val = access_nested_dict(data_dict, item_path)
            if item_val is not None:
                set_nested_dict_value(data_dict, item_path, item_val[::subsampling])
    dicttonx(data_dict, output_file, h5path=entry)


def shrink_cli():
    args = parse_params_values(ShrinkConfig, parser_description="Shrink a NX dataset")

    if not (os.path.isfile(args["input_file"])):
        print("No such file: %s" % args["input_file"])
        exit(1)
    if os.path.isfile(args["output_file"]):
        print("Output file %s already exists, not overwriting it" % args["output_file"])
        exit(1)

    binning = optional_tuple_of_floats_validator("", "binning", args["binning"])  # pylint: disable=E1121
    if binning is not None:
        binning = tuple(map(int, binning))
    subsampling = optional_positive_integer_validator("", "subsampling", args["subsampling"])  # pylint: disable=E1121

    shrink_dataset(
        args["input_file"],
        args["output_file"],
        binning=binning,
        subsampling=subsampling,
        entry=args["entry"],
        n_threads=args["threads"],
    )
    return 0


if __name__ == "__main__":
    shrink_cli()
