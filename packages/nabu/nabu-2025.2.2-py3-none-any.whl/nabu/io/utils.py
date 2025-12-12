import os
import contextlib
import h5py
import numpy as np
from silx.io.url import DataUrl
from tomoscan.io import HDF5File

from nabu.utils import first_generator_item


# This function might be moved elsewhere
def get_compacted_dataslices(urls, subsampling=None, begin=0):
    """
    Regroup urls to get the data more efficiently.
    Build a structure mapping files indices to information on
    how to load the data: `{indices_set: data_location}`
    where `data_location` contains contiguous indices.

    Parameters
    -----------
    urls: dict
        Dictionary where the key is an integer and the value is a silx `DataUrl`.
    subsampling: int, optional
        Subsampling factor when reading the frames. If an integer `n` is provided,
        then one frame out of `n` will be read.

    Returns
    --------
    merged_urls: dict
        Dictionary with the same keys as the `urls` parameter, and where the
        values are the corresponding `silx.io.url.DataUrl` with merged data_slice.
    """
    subsampling = subsampling or 1

    def _convert_to_slice(idx):
        if np.isscalar(idx):
            return slice(idx, idx + 1)
        # otherwise, assume already slice object
        return idx

    def is_contiguous_slice(slice1, slice2, step=1):
        if np.isscalar(slice1):
            slice1 = slice(slice1, slice1 + step)
        if np.isscalar(slice2):
            slice2 = slice(slice2, slice2 + step)
        return slice2.start == slice1.stop

    def merge_slices(slice1, slice2, step=1):
        return slice(slice1.start, slice2.stop, step)

    if len(urls) == 0:
        return urls

    sorted_files_indices = sorted(urls.keys())
    # if begin > 0:
    # sorted_files_indices = sorted_files_indices[begin:]
    idx0 = sorted_files_indices[begin]
    first_url = urls[idx0]

    merged_indices = [[idx0]]
    # location = (file_path, data_path, slice)
    data_location = [[first_url.file_path(), first_url.data_path(), _convert_to_slice(first_url.data_slice())]]
    pos = 0
    curr_fp, curr_dp, curr_slice = data_location[pos]
    skip_next = 0
    for idx in sorted_files_indices[begin + 1 :]:
        if skip_next > 1:
            skip_next -= 1
            continue
        url = urls[idx]
        next_slice = _convert_to_slice(url.data_slice())
        if (
            (url.file_path() == curr_fp)
            and (url.data_path() == curr_dp)
            and is_contiguous_slice(curr_slice, next_slice, step=subsampling)
        ):
            merged_indices[pos].append(idx)
            merged_slices = merge_slices(curr_slice, next_slice, step=subsampling)
            data_location[pos][-1] = merged_slices
            curr_slice = merged_slices
            skip_next = 0
        else:  # "jump"
            if begin > 0 and skip_next == 0:
                # Skip the "begin" next urls (first of a new block)
                skip_next = begin
                continue
            pos += 1
            merged_indices.append([idx])
            data_location.append([url.file_path(), url.data_path(), _convert_to_slice(url.data_slice())])
            curr_fp, curr_dp, curr_slice = data_location[pos]

    # Format result
    res = {}
    for ind, dl in zip(merged_indices, data_location):
        res.update(dict.fromkeys(ind, DataUrl(file_path=dl[0], data_path=dl[1], data_slice=dl[2])))

    return res


def get_first_hdf5_entry(fname):
    with HDF5File(fname, "r") as fid:
        entry = first_generator_item(fid.keys())
    return entry


def hdf5_entry_exists(fname, entry):
    with HDF5File(fname, "r") as fid:
        res = fid.get(entry, None) is not None
    return res


def get_h5_value(fname, h5_path, default_ret=None):
    with HDF5File(fname, "r") as fid:
        try:
            val_ptr = fid[h5_path][()]
        except KeyError:
            val_ptr = default_ret
    return val_ptr


def get_h5_str_value(dataset_ptr):
    """
    Get a HDF5 field which can be bytes or str (depending on h5py version !).
    """
    data = dataset_ptr[()]
    if isinstance(data, str):
        return data
    else:
        return bytes.decode(data)


def create_dict_of_indices(images_stack, images_indices):
    """
    From an image stack with the images indices, create a dictionary where
    each index is the image index, and the value is the corresponding image.

    Parameters
    ----------
    images_stack: numpy.ndarray
        A 3D numpy array in the layout (n_images, n_y, n_x)
    images_indices: array or list of int
        Array containing the indices of images in the stack

    Examples
    --------
    Given a simple array stack:

    >>> images_stack = np.arange(3*4*5).reshape((3,4,5))
    ... images_indices = [2, 7, 1]
    ... create_dict_of_indices(images_stack, images_indices)
    ... # returns {2: array1, 7: array2, 1: array3}
    """
    if images_stack.ndim != 3:
        raise ValueError("Expected a 3D array")
    if len(images_indices) != images_stack.shape[0]:
        raise ValueError("images_stack must have as many images as the length of images_indices")
    res = {}
    for i in range(len(images_indices)):
        res[images_indices[i]] = images_stack[i]
    return res


def convert_dict_values(dic, val_replacements, bytes_tostring=False):
    """
    Modify a dictionary to be able to export it with silx.io.dicttoh5
    """
    modified_dic = {}
    for key, value in dic.items():
        if isinstance(key, int):  # np.isscalar ?
            key = str(key)
        if isinstance(value, bytes) and bytes_tostring:
            value = bytes.decode(value.tostring())
        if isinstance(value, dict):
            value = convert_dict_values(value, val_replacements, bytes_tostring=bytes_tostring)
        else:
            if isinstance(value, DataUrl):
                value = value.path()
            elif value.__hash__ is not None and value in val_replacements:
                value = val_replacements[value]
        modified_dic[key] = value
    return modified_dic


class _BaseReader(contextlib.AbstractContextManager):
    def __init__(self, url: DataUrl):
        if not isinstance(url, DataUrl):
            raise TypeError("url should be an instance of DataUrl")
        if url.scheme() not in ("silx", "h5py"):
            raise ValueError("Valid scheme are silx and h5py")
        if url.data_slice() is not None:
            raise ValueError("Data slices are not managed. Data path should point to a bliss node (h5py.Group)")
        self._url = url
        self._file_handler = None

    def __exit__(self, *exc):
        return self._file_handler.close()


class EntryReader(_BaseReader):
    """Context manager used to read a bliss node"""

    def __enter__(self):
        self._file_handler = HDF5File(self._url.file_path(), mode="r")
        if self._url.data_path() == "":
            entry = self._file_handler
        else:
            entry = self._file_handler[self._url.data_path()]
        if not isinstance(entry, h5py.Group):
            raise TypeError("Data path should point to a bliss node (h5py.Group)")
        return entry


class DatasetReader(_BaseReader):
    """Context manager used to read a bliss node"""

    def __enter__(self):
        self._file_handler = HDF5File(self._url.file_path(), mode="r")
        entry = self._file_handler[self._url.data_path()]
        if not isinstance(entry, h5py.Dataset):
            raise TypeError(f"Data path ({self._url.path()}) should point to a dataset (h5py.Dataset)")
        return entry


# TODO: require some utils function to deduce type. And insure homogeneity. Might be moved in tomoscan ?
def file_format_is_edf(file_format: str):
    return file_format.lower().lstrip(".") == "edf"


def file_format_is_jp2k(file_format: str):
    return file_format.lower().lstrip(".") in ("jp2k", "jp2")


def file_format_is_tiff(file_format: str):
    return file_format.lower().lstrip(".") in ("tiff", "tif")


def file_format_is_hdf5(file_format: str):
    return file_format.lower().lstrip(".") in ("hdf5", "hdf", "nx", "nexus")


def get_output_volume(location: str, file_prefix: str | None, file_format: str, multitiff=False):

    # FIXME
    # These imports take an awful lot of time.
    # Waiting for the fix in tomoscan & underlying libs, the imports are done here for now
    from tomoscan.esrf import EDFVolume, HDF5Volume, TIFFVolume, JP2KVolume, MultiTIFFVolume

    #

    # TODO: see strategy. what if user provide a .nx ... ?
    # this function should be more generic
    location, extension = os.path.splitext(location)
    if extension == "":
        extension = file_format
    if file_format_is_edf(extension):
        return EDFVolume(folder=location, volume_basename=file_prefix)
    elif file_format_is_jp2k(extension):
        return JP2KVolume(folder=location, volume_basename=file_prefix)
    elif file_format_is_hdf5(file_format=extension):
        if extension is None:
            if file_prefix is None:
                location = ".".join([location, extension])
            else:
                location = os.path.join(location, ".".join([file_prefix, extension]))
        return HDF5Volume(file_path=location)
    elif file_format_is_tiff(extension):
        if multitiff:
            return MultiTIFFVolume(file_path=location)
        else:
            return TIFFVolume(folder=location, volume_basename=file_prefix)
    else:
        raise ValueError
