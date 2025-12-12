import os
import numpy as np
from nxtomo.io import HDF5File
from silx.io.url import DataUrl
from silx.io import get_data
from tomoscan.framereducer.reducedframesinfos import ReducedFramesInfos
from tomoscan.esrf.scan.nxtomoscan import NXtomoScan
from ..utils import check_supported, is_writeable
from ..preproc.flatfield import PCAFlatsDecomposer
from ..io.reader import NXDarksFlats


def get_frame_possible_urls(dataset_info, user_dir, output_dir):
    """
    Return a dict with the possible location of reduced dark/flat frames.

    Parameters
    ----------
    dataset_info: DatasetAnalyzer object
        DatasetAnalyzer object: data structure containing information on the parsed dataset
    user_dir: str or None
        User-provided directory location for the reduced frames.
    output_dir: str or None
        Output processing directory
    """

    frame_types = ["flats", "darks", "pcaflats"]
    h5scan = dataset_info.dataset_scanner  # tomoscan object

    def make_dataurl(dirname, frame_type):
        """
        The template formatting should be done by tomoscan in principle, but this complicates logging.
        """

        if frame_type == "flats":
            dataurl_default_template = h5scan.REDUCED_FLATS_DATAURLS[0]
        elif frame_type == "darks":
            dataurl_default_template = h5scan.REDUCED_DARKS_DATAURLS[0]
        elif frame_type == "pcaflats":
            dataurl_default_template = h5scan.PCA_FLATS_DATAURLS[0]

        rel_file_path = dataurl_default_template.file_path().format(scan_prefix=h5scan.get_dataset_basename())
        return DataUrl(
            file_path=os.path.join(dirname, rel_file_path),
            data_path=dataurl_default_template.data_path().format(entry=h5scan.entry, index="{index}"),
            data_slice=dataurl_default_template.data_slice(),  # not sure if needed
            scheme="silx",
        )

    urls = {"user": None, "dataset": None, "output": None}

    if user_dir is not None:
        urls["user"] = {frame_type: make_dataurl(user_dir, frame_type) for frame_type in frame_types}

    # tomoscan.esrf.scan.hdf5scan.REDUCED_{DARKS|FLATS}_DATAURLS.file_path() is a relative path
    # Create a absolute path instead
    urls["dataset"] = {
        frame_type: make_dataurl(os.path.dirname(h5scan.master_file), frame_type) for frame_type in frame_types
    }

    if output_dir is not None:
        urls["output"] = {frame_type: make_dataurl(output_dir, frame_type) for frame_type in frame_types}

    return urls


def save_reduced_frames(dataset_info, reduced_frames_arrays, reduced_frames_urls):
    reduce_func = {"flats": np.median, "darks": np.mean}  # TODO configurable ?

    # Get "where to write". tomoscan expects a DataUrl
    darks_flats_dir_url = reduced_frames_urls.get("user", None)
    if darks_flats_dir_url is not None:
        output_url = darks_flats_dir_url
    elif is_writeable(os.path.abspath(os.path.dirname(reduced_frames_urls["dataset"]["flats"].file_path()))):
        output_url = reduced_frames_urls["dataset"]
    else:
        output_url = reduced_frames_urls["output"]

    # Get the "ReducedFrameInfos" data structure expected by tomoscan
    def _get_additional_info(frame_type):
        machine_current = dataset_info.dataset_scanner.machine_current
        count_time = dataset_info.dataset_scanner.count_time
        if machine_current is not None:
            machine_current = {
                sl.start: reduce_func[frame_type](machine_current[sl]) for sl in dataset_info.frames_slices(frame_type)
            }
            machine_current = [machine_current[k] for k in sorted(machine_current.keys())]
        if count_time is not None:
            count_time = {
                sl.start: reduce_func[frame_type](count_time[sl]) for sl in dataset_info.frames_slices(frame_type)
            }
            count_time = [count_time[k] for k in sorted(count_time.keys())]
        info = ReducedFramesInfos()
        info.count_time = count_time
        info.machine_current = machine_current
        return info

    flats_info = _get_additional_info("flats")
    darks_info = _get_additional_info("darks")

    # Call tomoscan to save the reduced frames
    dataset_info.dataset_scanner.save_reduced_darks(
        reduced_frames_arrays["darks"],
        output_urls=[output_url["darks"]],
        darks_infos=darks_info,
        metadata_output_urls=[get_metadata_url(output_url["darks"], "darks")],
        overwrite=True,
    )
    dataset_info.dataset_scanner.save_reduced_flats(
        reduced_frames_arrays["flats"],
        output_urls=[output_url["flats"]],
        flats_infos=flats_info,
        metadata_output_urls=[get_metadata_url(output_url["flats"], "flats")],
        overwrite=True,
    )
    dataset_info.logger.info("Saved reduced darks/flats to %s" % output_url["flats"].file_path())
    return output_url, flats_info, darks_info


def get_metadata_url(url, frame_type):
    """
    Return the url of the metadata stored alongside flats/darks
    """
    check_supported(frame_type, ["flats", "darks"], "frame type")
    template_url = getattr(NXtomoScan, "REDUCED_%s_METADATAURLS" % frame_type.upper())[0]
    return DataUrl(
        file_path=url.file_path(),
        data_path=template_url.data_path(),
        scheme="silx",
    )


def tomoscan_load_reduced_frames(dataset_info, frame_type, url):
    tomoscan_method = getattr(dataset_info.dataset_scanner, "load_reduced_%s" % frame_type)
    return tomoscan_method(
        inputs_urls=[url],
        return_as_url=True,
        return_info=True,
        metadata_input_urls=[get_metadata_url(url, frame_type)],
    )


def data_url_exists(data_url):
    """
    Return true iff the file exists and the data URL is valid (i.e data/group is actually in the file)
    """
    if not (os.path.isfile(data_url.file_path())):
        return False
    group_exists = False
    with HDF5File(data_url.file_path(), "r") as f:
        data_path_without_index = data_url.data_path().split("{")[0]
        group_exists = f.get(data_path_without_index, default=None) is not None
    return group_exists


def _compute_and_save_reduced_frames(flatfield_mode, dataset_info, reduced_frames_urls):
    if flatfield_mode == "pca":
        dfreader = NXDarksFlats(dataset_info.location)
        darks = np.concatenate([d for d in dfreader.get_raw_darks()], axis=0)
        flats = np.concatenate([f for f in dfreader.get_raw_flats()], axis=0)
        pcaflats_darks = PCAFlatsDecomposer(flats, darks)

        # Get "where to write". tomoscan expects a DataUrl
        pcaflats_dir_url = reduced_frames_urls.get("user", None)
        if pcaflats_dir_url is not None:
            output_url = pcaflats_dir_url
        elif is_writeable(os.path.dirname(reduced_frames_urls["dataset"]["flats"].file_path())):
            output_url = reduced_frames_urls["dataset"]
        else:
            output_url = reduced_frames_urls["output"]
        pcaflats_darks.save_decomposition(
            path=output_url["pcaflats"].file_path(), entry=output_url["pcaflats"].data_path().strip("/").split("/")[0]
        )
        dataset_info.logger.info("PCA flats computed and written at %s" % (output_url["pcaflats"].file_path()))

        # Update dataset_info with pca flats and dark
        dataset_info.darks = {0: pcaflats_darks.dark}
        flats = {0: pcaflats_darks.mean}
        for k in range(len(pcaflats_darks.components)):
            flats.update({k + 1: pcaflats_darks.components[k]})
        dataset_info.flats = flats
    else:
        try:
            dataset_info.flats = dataset_info.get_reduced_flats()
            dataset_info.darks = dataset_info.get_reduced_darks()
        except FileNotFoundError:
            msg = "Could not find any flats and/or darks"
            raise FileNotFoundError(msg)
        _, flats_info, darks_info = save_reduced_frames(
            dataset_info, {"darks": dataset_info.darks, "flats": dataset_info.flats}, reduced_frames_urls
        )
        dataset_info.flats_srcurrent = flats_info.machine_current


def _load_existing_flatfields(dataset_info, reduced_frames_urls, frames_types, where_to_load_from):
    if "pcaflats" not in frames_types:
        reduced_frames_with_info = {}
        for frame_type in frames_types:
            reduced_frames_with_info[frame_type] = tomoscan_load_reduced_frames(
                dataset_info, frame_type, reduced_frames_urls[where_to_load_from][frame_type]
            )
            dataset_info.logger.info(
                "Loaded %s from %s" % (frame_type, reduced_frames_urls[where_to_load_from][frame_type].file_path())
            )
            red_frames_dict, red_frames_info = reduced_frames_with_info[frame_type]
            setattr(
                dataset_info,
                frame_type,
                {k: get_data(red_frames_dict[k]) for k in red_frames_dict},
            )
            if frame_type == "flats":
                dataset_info.flats_srcurrent = red_frames_info.machine_current
    else:
        df_path = reduced_frames_urls[where_to_load_from]["pcaflats"].file_path()
        entry = reduced_frames_urls[where_to_load_from]["pcaflats"].data_path()

        # Update dark
        dark_url = DataUrl(f"silx://{df_path}?{entry}/dark")
        dark = get_data(dark_url)
        setattr(dataset_info, "dark", {0: dark})  # noqa: B010 - # I know what I'm doing ruff!
        # Update flats with principal compenents
        # Take mean as first comp., mask as second, flats thereafter
        flats_url = DataUrl(f"silx://{df_path}?{entry}/p_components")
        mean_url = DataUrl(f"silx://{df_path}?{entry}/p_mean")
        flats = get_data(flats_url)
        # TODO what do do with this ?
        mean = get_data(mean_url)  # noqa: F841
        setattr(dataset_info, "flats", {k: flats[k] for k in range(len(flats))})  # noqa: B010

        dataset_info.flats = {k: flats[k] for k in range(len(flats))}
        dataset_info.logger.info("Loaded %s from %s" % ("PCA darks/flats", df_path))


# pylint: disable=E1136
def update_dataset_info_flats_darks(
    dataset_info, flatfield_mode, loading_mode="load_if_present", output_dir=None, darks_flats_dir=None
):
    """
    Update a DatasetAnalyzer object with reduced flats/darks (hereafter "reduced frames").

    How the reduced frames are loaded/computed/saved will depend on the "flatfield_mode" parameter.

    The principle is the following:
    (1) Attempt at loading already-computed reduced frames (XXX_darks.h5 and XXX_flats.h5):
       - First check files in the user-defined directory 'darks_flats_dir'
       - Then try to load from files located alongside the .nx dataset (dataset directory)
       - Then try to load from output_dir, if provided
    (2) If loading fails, or flatfield_mode == "force_compute", compute the reduced frames.
    (3) Save these reduced frames
       - Save in darks_flats_dir, if provided by user
       - Otherwise, save in the data directory (next to the .nx file), if write access OK
       - Otherwise, save in output directory
    """
    if flatfield_mode is False:
        return

    if flatfield_mode == "pca":
        frames_types = ["pcaflats"]
    else:
        frames_types = ["darks", "flats"]
    reduced_frames_urls = get_frame_possible_urls(dataset_info, darks_flats_dir, output_dir)

    if loading_mode == "force-compute":
        _compute_and_save_reduced_frames(flatfield_mode, dataset_info, reduced_frames_urls)
        return

    def _can_load_from(folder_type):
        if reduced_frames_urls.get(folder_type, None) is None:
            return False
        return all([data_url_exists(reduced_frames_urls[folder_type][frame_type]) for frame_type in frames_types])

    where_to_load_from = None
    if reduced_frames_urls["user"] is not None and _can_load_from("user"):
        where_to_load_from = "user"
    elif _can_load_from("dataset"):
        where_to_load_from = "dataset"
    elif _can_load_from("output"):
        where_to_load_from = "output"

    if where_to_load_from is None and flatfield_mode == "force-load":
        raise ValueError("Could not load darks/flats (using 'force-load')")

    if where_to_load_from is not None:
        _load_existing_flatfields(dataset_info, reduced_frames_urls, frames_types, where_to_load_from)
    else:
        _compute_and_save_reduced_frames(flatfield_mode, dataset_info, reduced_frames_urls)
