import argparse
import os
import sys
import logging
from argparse import RawTextHelpFormatter
import numpy
from silx.io.url import DataUrl
from tomoscan.esrf.volume.utils import guess_volumes
from tomoscan.factory import Factory
from tomoscan.esrf.volume import (
    EDFVolume,
    HDF5Volume,
    JP2KVolume,
    MultiTIFFVolume,
    TIFFVolume,
)
from nabu.io.cast_volume import (
    RESCALE_MAX_PERCENTILE,
    RESCALE_MIN_PERCENTILE,
    cast_volume,
    get_default_output_volume,
)
from nabu.pipeline.params import files_formats
from nabu.utils import convert_str_to_tuple
from nabu.io.cast_volume import _min_max_from_histo


_logger = logging.getLogger(__name__)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    _volume_url_helps = "\n".join(
        [
            f"- {(volume.__name__).ljust(15)}: {volume.example_defined_from_str_identifier()}"
            for volume in (
                EDFVolume,
                HDF5Volume,
                JP2KVolume,
                MultiTIFFVolume,
                TIFFVolume,
            )
        ]
    )

    volume_help = f"""To define a volume you can either provide: \n
    * an url (recommanded way) - see details lower \n
    * a path. For hdf5 and multitiff we expect a file path. For edf, tif and jp2k we expect a folder path. In this case we will try to deduce the Volume from it. \n
    url must be defined like: \n{_volume_url_helps}
    """

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "input_volume",
        help=f"input volume. {volume_help}",
    )
    parser.add_argument(
        "--output-data-type",
        help="output data type. Valid value are numpy default types name like (uint8, uint16, int8, int16, int32, float32, float64)",
        default="uint16",
    )
    parser.add_argument(
        "--output_volume",
        help=f"output volume. Must be provided if 'output_type' isn't. Must looks like: \n{volume_help}",
        default=None,
    )
    parser.add_argument(
        "--output_type",
        help=f"output type. Must be provided if 'output_volume' isn't. Valid values are {tuple(files_formats.keys())}",
        default=None,
    )
    parser.add_argument(
        "--data_min",
        help=f"value to clamp to volume cast new min. Any lower value will also be clamp to this value.",
        default=None,
    )
    parser.add_argument(
        "--data_max",
        help=f"value to clamp to volume cast new max. Any higher value will also be clamp to this value.",
        default=None,
    )
    parser.add_argument(
        "--rescale_min_percentile",
        help=f"used to determine data_min if not provided. Expected as percentage. Default is {RESCALE_MIN_PERCENTILE}%%",
        default=RESCALE_MIN_PERCENTILE,
    )
    parser.add_argument(
        "--rescale_max_percentile",
        help=f"used to determine data_max if not provided. Expected as percentage. Default is {RESCALE_MAX_PERCENTILE}%%",
        default=RESCALE_MAX_PERCENTILE,
    )
    parser.add_argument(
        "--overwrite",
        dest="overwrite",
        action="store_true",
        default=False,
        help="Overwrite file or dataset if exists",
    )
    parser.add_argument(
        "--compression-ratios",
        dest="compression_ratios",
        default=None,
        help="Define compression ratios for jp2k. Expected as a list like [20, 10, 1] for [quality layer 1, quality layer 2, quality layer 3]... Pass parameter to glymur. See https://glymur.readthedocs.io/en/latest/how_do_i.html#write-images-with-different-compression-ratios-for-different-layers for more details",
    )
    parser.add_argument(
        "--histogram-url",
        dest="histogram_url",
        default=None,
        help="Provide url to the histogram - like: '/{path}/my_file.hdf5?path/to/my/data' with my_file.hdf5 is the file containing the histogram. Located under 'path'. And 'path/to/my/data' is the location of the HDF5 dataset",
    )
    parser.add_argument(
        "--remove-input-volume",
        "--remove",
        dest="remove",
        action="store_true",
        default=False,
        help="Whether to remove the input volume after cast. Default is False.",
    )
    options = parser.parse_args(argv[1:])

    # handle input volume
    if os.path.exists(options.input_volume):
        volumes = guess_volumes(options.input_volume)

        def is_not_histogram(vol_identifier):
            return not (hasattr(vol_identifier, "data_path") and vol_identifier.data_path.endswith("histogram"))

        volumes = tuple(filter(is_not_histogram, volumes))
        if len(volumes) == 0:
            _logger.error(f"no valid volume found in {options.input_volume}")
            exit(1)
        elif len(volumes) > 1:
            _logger.error(
                f"found several volume from {options.input_volume}. Please provide one full url from {[volume.get_identifier() for volume in volumes]}"
            )
        else:
            input_volume = volumes[0]
    else:
        try:
            input_volume = Factory.create_tomo_object_from_identifier(options.input_volume)
        except Exception as e:
            raise ValueError(f"Fail to build input volume from url {options.input_volume}") from e

    # handle output format
    output_format = files_formats.get(options.output_type, None)

    # handle output volume
    if options.output_volume is not None:
        # if an url is provided
        if ":" in options.output_volume:
            try:
                output_volume = Factory.create_tomo_object_from_identifier(options.output_volume)
            except Exception as e:
                raise ValueError(f"Fail to build output volume from {options.output_volume}") from e

            # ruff: noqa: SIM102
            if output_format is not None:
                if not (
                    (isinstance(output_volume, EDFVolume) and output_format == "edf")
                    or (isinstance(output_format, HDF5Volume) and output_format == "hdf5")
                    or (isinstance(output_format, JP2KVolume) and output_format == "jp2")
                    or (isinstance(output_format, (TIFFVolume, MultiTIFFVolume)) and output_format == "tiff")
                ):
                    raise ValueError(
                        "Requested 'output_type' and output volume url are incoherent. 'output_type' is optional when url provided"
                    )
        else:
            path_extension = os.path.splitext(options.output_volume)[-1]
            if path_extension == "":
                # if a folder ha sbeen provided we try to create a volume from this path and the output format
                if output_format == "tiff":
                    output_volume = TIFFVolume(
                        folder=options.output_volume,
                    )
                elif output_format == "edf":
                    output_volume = EDFVolume(
                        folder=options.output_volume,
                    )
                elif output_format == "jp2":
                    output_volume = JP2KVolume(
                        folder=options.output_volume,
                    )
                else:
                    raise ValueError(
                        f"Unable to deduce an output volume from {options.output_volume} and output format {output_format}. Please provide an output_volume as an url"
                    )
            else:
                # if a file path_has been provided
                if path_extension.lower() in ("tif", "tiff") and output_format in (
                    None,
                    "tiff",
                ):
                    output_volume = MultiTIFFVolume(
                        file_path=options.output_volume,
                    )
                elif path_extension.lower() in (
                    "h5",
                    "nx",
                    "nexus",
                    "hdf",
                    "hdf5",
                ) and output_format in (None, "hdf5"):
                    output_volume = HDF5Volume(
                        file_path=options.output_volume,
                        data_path="volume",
                    )
                else:
                    raise ValueError(
                        f"Unable to deduce an output volume from {options.output_volume} and output format {output_format}. Please provide an output_volume as an url"
                    )

    elif options.output_type is None:
        raise ValueError("'output_type' or 'output_volume' is expected")
    else:
        output_volume = get_default_output_volume(
            input_volume=input_volume, output_type=output_format  # pylint: disable=E0606
        )
    try:
        output_data_type = numpy.dtype(getattr(numpy, options.output_data_type))
    except Exception as e:
        raise ValueError(f"Unable to get output data type from {options.output_data_type}") from e

    # get data_min and data_max
    data_min = options.data_min
    if data_min is not None:
        data_min = float(data_min)
    data_max = options.data_max
    if data_max is not None:
        data_max = float(data_max)

    # get rescale_min_percentile and rescale_min_percentile
    rescale_min_percentile = options.rescale_min_percentile

    def clean_percentiles_str(percentile):
        # remove ' char
        percentile = percentile.rstrip("'").lstrip("'")
        # remove " char
        percentile = percentile.rstrip('"').lstrip('"')
        # remove % char
        return percentile.rstrip("%")

    if isinstance(rescale_min_percentile, str):
        rescale_min_percentile = float(clean_percentiles_str(rescale_min_percentile))
    rescale_max_percentile = options.rescale_max_percentile
    if isinstance(rescale_min_percentile, str):
        rescale_max_percentile = float(clean_percentiles_str(rescale_max_percentile))
    assert rescale_min_percentile is not None, "rescale_min_percentile should be an int"
    assert rescale_max_percentile is not None, "rescale_max_percentile should be an int"

    # handle histogram and data_min, data_max
    if options.histogram_url is not None:
        if data_min is not None or data_max is not None:
            raise ValueError("Both histogram url and data min/max are provided. Don't know which one to take")
        else:
            if not options.histogram_url.startswith("silx:"):
                options.histogram_url = "silx:" + options.histogram_url
            histogram_url = DataUrl(path=options.histogram_url)
            data_min, data_max = _min_max_from_histo(
                url=histogram_url,
                rescale_min_percentile=rescale_min_percentile,
                rescale_max_percentile=rescale_max_percentile,
            )

    # update output volume from options
    output_volume.overwrite = options.overwrite
    if options.compression_ratios is not None:
        output_volume.cratios = [int(value) for value in convert_str_to_tuple(options.compression_ratios)]

    # do volume casting
    cast_volume(
        input_volume=input_volume,
        output_volume=output_volume,
        output_data_type=output_data_type,
        data_min=data_min,
        data_max=data_max,
        rescale_min_percentile=rescale_min_percentile,
        rescale_max_percentile=rescale_max_percentile,
        remove_input_volume=options.remove,
    )
    exit(0)


if __name__ == "__main__":
    main(sys.argv)
