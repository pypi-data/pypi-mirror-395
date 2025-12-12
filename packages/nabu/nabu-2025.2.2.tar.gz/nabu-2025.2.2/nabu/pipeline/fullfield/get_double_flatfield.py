"""
Double-flatfield:
  - Compute the average of all projections, which gives one resulting image
  - Apply some filter to this image (DFF)
  - Subtract or divide this image from all the projections
"""

from os import path
from silx.io.url import DataUrl
from silx.io.dictdump import h5todict

from nabu.io.utils import get_first_hdf5_entry

from ...utils import is_writeable
from ...app.double_flatfield import DoubleFlatFieldChunks
from ...resources.nxflatfield import data_url_exists

rel_file_path_template = "{scan_name}_dff.h5"
data_path_template = "{entry}/double_flatfield"


def get_possible_dff_urls(dataset_info, user_dir, output_dir):
    """
    See nabu.resources.nxflatfield.get_frame_possible_urls
    """
    entry = dataset_info.hdf5_entry or ""

    def make_dataurl(dirname):
        file_path = path.join(
            dirname,
            rel_file_path_template.format(scan_name=dataset_info.scan_basename),
        )
        return DataUrl(
            file_path=file_path,
            data_path=data_path_template.format(entry=entry),
            scheme="silx",
        )

    urls = {"user": None, "dataset": None, "output": None}

    if user_dir is not None:
        urls["user"] = make_dataurl(user_dir)
    urls["dataset"] = make_dataurl(dataset_info.scan_dirname)
    if output_dir is not None:
        urls["output"] = make_dataurl(output_dir)

    return urls


def compute_and_save_dff(dataset_info, possible_urls, dff_options):
    if possible_urls["user"] is not None:
        dff_output_file = possible_urls["user"].file_path()
    elif is_writeable(path.dirname(possible_urls["dataset"].file_path())):
        dff_output_file = possible_urls["dataset"].file_path()
    else:
        dff_output_file = possible_urls["output"].file_path()

    dataset_info.logger.info("Computing double flatfield")
    dff = DoubleFlatFieldChunks(
        None,
        dff_output_file,
        dataset_info=dataset_info,
        chunk_size=dff_options.get("chunk_size", 100),
        sigma=dff_options.get("dff_sigma", None),
        do_flatfield=dff_options.get("do_flatfield", True),
        logger=dataset_info.logger,
    )
    dff_image = dff.compute_double_flatfield()
    return dff.write_double_flatfield(dff_image)


def check_existing_dff(dff_url, dff_options, logger):
    # Check that the DFF exists at the given DataUrl, and that its configuration matches the wanted config
    # Return the DFF file path
    if not (data_url_exists(dff_url)):
        raise ValueError("DFF file not found:", dff_url)

    fname = dff_url.file_path()
    entry = get_first_hdf5_entry(fname)
    dff_file_options = h5todict(fname, path=entry + "/double_flatfield/configuration", asarray=False)

    ff_file = dff_file_options.get("do_flatfield", True)
    ff_user = dff_options.get("do_flatfield", True)
    # Use "==" instead of "is" here, as h5todict() will return something like numpy.True_ instead of True
    if ff_file != ff_user:
        msg = "DFF was computed with flatfield=%s, but you asked flatfield=%s" % (ff_file, ff_user)
        logger.error(msg)
        return False

    # Use this because h5todict() returns str("None") instead of None
    def _correct_none(x):
        if x in [None, "None"]:
            return None
        return x

    sigma_file = _correct_none(dff_file_options.get("dff_sigma", None))
    sigma_user = _correct_none(dff_options.get("dff_sigma", None))
    if sigma_file != sigma_user:
        msg = "DFF was computed with dff_sigma=%s, but you asked dff_sigma=%s" % (sigma_file, sigma_user)
        logger.error(msg)
        return False

    return fname


# pylint: disable=E1136
def get_double_flatfield(dataset_info, mode, output_dir=None, darks_flats_dir=None, dff_options=None):
    """
    See nabu.resources.nxflatfield.update_dataset_info_flats_darks for the logic
    """
    if mode is False:
        return
    dff_options = dff_options or {}

    possible_urls = get_possible_dff_urls(dataset_info, darks_flats_dir, output_dir)

    if mode == "force-compute":
        return compute_and_save_dff(dataset_info, possible_urls, dff_options)

    def _can_load_from(folder_type):
        if possible_urls.get(folder_type, None) is None:
            return False
        return data_url_exists(possible_urls[folder_type])

    where_to_load_from = None
    if possible_urls["user"] is not None and _can_load_from("user"):
        where_to_load_from = "user"
    elif _can_load_from("dataset"):
        where_to_load_from = "dataset"
    elif _can_load_from("output"):
        where_to_load_from = "output"

    if where_to_load_from is None:
        if mode == "force-load":
            raise ValueError("Could not load double-flatfield file (using 'force-load')")
        else:
            return compute_and_save_dff(dataset_info, possible_urls, dff_options)

    fname = check_existing_dff(possible_urls[where_to_load_from], dff_options, dataset_info.logger)
    if fname is False:
        if mode == "force-load":
            raise ValueError("Could not load double-flatfield file (using 'force-load'): wrong configuration")
        return compute_and_save_dff(dataset_info, possible_urls, dff_options)
    return fname

    # One possible corner case: if mode == "force-load" and darks_flats_dir is not None (but the actual folder is empty)
    # then nabu will load a DFF found elsewhere (if any). We might want to raise an error instead.
