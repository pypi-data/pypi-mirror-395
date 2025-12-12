import sys

from nabu.app.cli_configs import ReduceDarkFlatConfig
from .utils import parse_params_values
from .. import version

from tomoscan.framereducer.method import ReduceMethod
from tomoscan.scanbase import TomoScanBase
from tomoscan.esrf.scan.edfscan import EDFTomoScan
from tomoscan.factory import Factory
from silx.io.url import DataUrl


reduce_methods = tuple(member.value for member in ReduceMethod)


def _create_data_urls(output_file: str | None, output_data_path: str | None, name: str):
    """
    util function to compute reduced Data and metadata url(s)
    This only handle the case of hdf5 outputs
    """
    assert name in ("flats", "darks"), f"name is '{name}'"

    def get_data_paths(data_path: str | None) -> tuple:
        """return (data_path, metadata_path)"""
        if data_path is None:
            return "{entry}/" + name + "/{index}", "{entry}/" + name
        elif not data_path.endswith("/{index}"):
            # we are not expecting useds to provide the index but only upstream part
            return data_path + "/{index}", data_path
        else:
            raise RuntimeError(
                "unhandled use case (/index provided) and don;t know where to set the data and the metadata"
            )

    data_path, metadata_path = get_data_paths(output_data_path)

    output_file = output_file or "{scan_prefix}_" + f"{name}.hdf5"
    data_urls = [
        DataUrl(
            file_path=output_file,
            data_path=data_path,
            scheme="silx",
        ),
    ]

    metadata_urls = [
        DataUrl(
            file_path=output_file,
            data_path=metadata_path,
            scheme="silx",
        ),
    ]
    return data_urls, metadata_urls


def reduce_dark_flat(
    scan: TomoScanBase,
    dark_method: ReduceMethod,
    flat_method: ReduceMethod,
    overwrite: bool = False,
    output_reduced_darks_file: str | None = None,
    output_reduced_darks_data_path: str | None = None,
    output_reduced_flats_file: str | None = None,
    output_reduced_flats_data_path: str | None = None,
) -> int:
    """
    calculation of the darks / flats calling tomoscan utils function
    """
    dark_method = ReduceMethod(dark_method) if dark_method is not None else None
    flat_method = ReduceMethod(flat_method) if flat_method is not None else None

    # 1. define url where to save the file
    ## 1.1 for darks
    if dark_method is None:
        reduced_darks_data_urls = ()
        reduced_darks_metadata_urls = ()
    elif output_reduced_darks_file is None and output_reduced_darks_data_path is None:
        # if no settings provided then take the default path (the idea is also to be more robust to future modifications)
        reduced_darks_data_urls = scan.REDUCED_DARKS_DATAURLS
        reduced_darks_metadata_urls = scan.REDUCED_DARKS_METADATAURLS
    elif isinstance(scan, EDFTomoScan):
        # simplification of the equation
        raise ValueError("reduce-dark-flat can only compute create dark-flats at default location for edf")
    else:
        reduced_darks_data_urls, reduced_darks_metadata_urls = _create_data_urls(
            output_file=output_reduced_darks_file,
            output_data_path=output_reduced_darks_data_path,
            name="darks",
        )
    ## 1.2 for flats
    if flat_method is None:
        reduced_flats_data_urls = ()
        reduced_flats_metadata_urls = ()
    elif output_reduced_flats_file is None and output_reduced_flats_data_path is None:
        # if no settings provided then take the default path (the idea is also to be more robust to future modifications)
        reduced_flats_data_urls = scan.REDUCED_FLATS_DATAURLS
        reduced_flats_metadata_urls = scan.REDUCED_FLATS_METADATAURLS
    elif isinstance(scan, EDFTomoScan):
        # simplification of the equation
        raise ValueError("reduce-dark-flat can only compute create dark-flats at default location for edf")
    else:
        reduced_flats_data_urls, reduced_flats_metadata_urls = _create_data_urls(
            output_file=output_reduced_flats_file,
            output_data_path=output_reduced_flats_data_path,
            name="flats",
        )

    # 2. compute and save darks / flats

    success = True
    ## 2.1 handle dark
    if dark_method is not None:
        try:
            reduced_darks, darks_metadata = scan.compute_reduced_darks(
                reduced_method=dark_method,
                overwrite=overwrite,
                return_info=True,
            )
        except Exception as e:
            print(f"failed to create reduced darks. Error is {e}")
            success = False
        else:
            scan.save_reduced_darks(
                darks=reduced_darks,
                darks_infos=darks_metadata,
                output_urls=reduced_darks_data_urls,
                metadata_output_urls=reduced_darks_metadata_urls,
                overwrite=overwrite,
            )

    ## 2.2 handle flats
    if flat_method is not None:
        try:
            reduced_flats, flats_metadata = scan.compute_reduced_flats(
                reduced_method=flat_method,
                overwrite=overwrite,
                return_info=True,
            )
        except Exception as e:
            print(f"failed to create reduced flats. Error is {e}")
            success = False
        else:
            scan.save_reduced_flats(
                flats=reduced_flats,
                flats_infos=flats_metadata,
                output_urls=reduced_flats_data_urls,
                metadata_output_urls=reduced_flats_metadata_urls,
                overwrite=overwrite,
            )

    return success


def main(argv=None):
    """
    Compute reduce dark(s) and flat(s) of a dataset
    """
    if argv is None:
        argv = sys.argv[1:]

    args = parse_params_values(
        ReduceDarkFlatConfig,
        parser_description=main.__doc__,
        program_version="nabu " + version,
        user_args=argv,
    )

    scan = Factory.create_scan_object(args["dataset"], entry=args["entry"])
    exit(
        reduce_dark_flat(
            scan=scan,
            dark_method=args["dark_method"],
            flat_method=args["flat_method"],
            overwrite=args["overwrite"],
            output_reduced_darks_file=args["output_reduced_darks_file"],
            output_reduced_darks_data_path=args["output_reduced_darks_data_path"],
            output_reduced_flats_file=args["output_reduced_flats_file"],
            output_reduced_flats_data_path=args["output_reduced_flats_data_path"],
        )
    )
