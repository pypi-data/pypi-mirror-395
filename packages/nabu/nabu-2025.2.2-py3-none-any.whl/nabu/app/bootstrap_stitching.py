from .cli_configs import BootstrapStitchingConfig
from ..pipeline.config import generate_nabu_configfile
from ..stitching.config import (
    get_default_stitching_config,
    SECTIONS_COMMENTS as _SECTIONS_COMMENTS,
    INPUT_DATASETS_FIELD as _INPUT_DATASETS_FIELD,
    INPUTS_SECTION as _INPUTS_SECTION,
)
from .utils import parse_params_values
from tomoscan.factory import Factory
from tomoscan.esrf.volume.utils import guess_volumes


def guess_tomo_objects(my_str: str) -> tuple:
    """
    Try to find some tomo object from a string.
    The string can be either related to a volume or a scan and can be an identifier or a file/folder path

    :param str my_str: string related to the tomo object
    :return: a tuple of tomo objects either instance of VolumeBase or TomoScanBase
    :rtype: tuple
    """
    try:
        # create_tomo_object_from_identifier will raise an exception is the string does not match an identifier
        return (Factory.create_tomo_object_from_identifier(my_str),)
    except Exception as exc:
        print("Error:", str(exc))
        pass

    try:
        volumes = guess_volumes(my_str)
    except Exception as exc:
        print("Error:", str(exc))
        pass
    else:
        if len(volumes) > 0:
            return volumes

    try:
        return Factory.create_scan_objects(my_str)
    except Exception:
        return tuple()


def bootstrap_stitching():
    args = parse_params_values(
        BootstrapStitchingConfig,
        parser_description="Initialize a 'nabu-stitching' configuration file",
    )

    prefilled_values = {}

    datasets_as_str = args.get("datasets", None)
    datasets = []
    for dataset in datasets_as_str:
        datasets.extend(guess_tomo_objects(dataset))

    if len(datasets) > 0:
        prefilled_values = {
            _INPUTS_SECTION: {_INPUT_DATASETS_FIELD: [dataset.get_identifier().to_str() for dataset in datasets]}
        }

    generate_nabu_configfile(
        fname=args["output"],
        default_config=get_default_stitching_config(args["stitching_type"]),
        comments=True,
        sections_comments=_SECTIONS_COMMENTS,
        options_level=args["level"],
        prefilled_values=prefilled_values,
    )
    return 0
