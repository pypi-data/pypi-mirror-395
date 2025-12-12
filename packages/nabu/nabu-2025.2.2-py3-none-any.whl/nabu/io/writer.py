from glob import glob
from pathlib import Path as pathlib_Path
from os import path, getcwd, chdir
from posixpath import join as posix_join
from datetime import datetime
import numpy as np
from h5py import VirtualSource, VirtualLayout
from silx.io.dictdump import dicttoh5
from silx.io.url import DataUrl

try:
    from tomoscan.io import HDF5File
except:
    from h5py import File as HDF5File
from tomoscan.esrf.volume.rawvolume import RawVolume
from .. import version as nabu_version
from ..utils import merged_shape
from .utils import convert_dict_values


def get_datetime():
    """
    Function used by some writers to indicate the current date.
    """
    return datetime.now().replace(microsecond=0).isoformat()


class Writer:
    """
    Base class for all writers.
    """

    def __init__(self, fname):
        self.fname = fname

    def get_filename(self):
        return self.fname


###################################################################################################
## Nabu original code for NXProcessWriter - also works for non-3D data, does not depend on tomoscan
###################################################################################################


def h5_write_object(h5group, key, value, overwrite=False, default_val=None):
    existing_val = h5group.get(key, default_val)
    if existing_val is not default_val:
        if not overwrite:
            raise OSError("Unable to create link (name already exists): %s" % h5group.name)
        else:
            h5group.pop(key)
    h5group[key] = value


class NXProcessWriter(Writer):
    """
    A class to write Nexus file with a processing result.
    """

    def __init__(self, fname, entry=None, filemode="a", overwrite=False):
        """
        Initialize a NXProcessWriter.

        Parameters
        -----------
        fname: str
            Path to the HDF5 file.
        entry: str, optional
            Entry in the HDF5 file. Default is "entry"
        """
        super().__init__(fname)
        self._set_entry(entry)
        self._filemode = filemode
        self.overwrite = overwrite

    def _set_entry(self, entry):
        self.entry = entry or "entry"
        data_path = posix_join("/", self.entry)
        self.data_path = data_path

    def write(
        self,
        result,
        process_name,
        processing_index=0,
        config=None,
        data_name="data",
        is_frames_stack=True,
        direct_access=True,
    ):
        """
        Write the result in the current NXProcess group.

        Parameters
        ----------
        result: numpy.ndarray
            Array containing the processing result
        process_name: str
            Name of the processing
        processing_index: int
            Index of the processing (in a pipeline)
        config: dict, optional
            Dictionary containing the configuration.
        """
        swmr = self._filemode == "r"
        with HDF5File(self.fname, self._filemode, swmr=swmr) as fid:
            nx_entry = fid.require_group(self.data_path)
            if "NX_class" not in nx_entry.attrs:
                nx_entry.attrs["NX_class"] = "NXentry"

            nx_process = nx_entry.require_group(process_name)
            nx_process.attrs["NX_class"] = "NXprocess"

            metadata = {
                "program": "nabu",
                "version": nabu_version,
                "date": get_datetime(),
                "sequence_index": np.int32(processing_index),
            }
            for key, val in metadata.items():
                h5_write_object(nx_process, key, val, overwrite=self.overwrite)

            if config is not None:
                export_dict_to_h5(
                    config, self.fname, posix_join(nx_process.name, "configuration"), overwrite_data=True, mode="a"
                )
                nx_process["configuration"].attrs["NX_class"] = "NXcollection"
            if isinstance(result, dict):
                results_path = posix_join(nx_process.name, "results")
                export_dict_to_h5(result, self.fname, results_path, overwrite_data=self.overwrite, mode="a")
            else:
                nx_data = nx_process.require_group("results")
                results_path = nx_data.name
                nx_data.attrs["NX_class"] = "NXdata"
                nx_data.attrs["signal"] = data_name

                results_data_path = posix_join(results_path, data_name)
                if self.overwrite and results_data_path in fid:
                    del fid[results_data_path]

                if isinstance(result, VirtualLayout):
                    nx_data.create_virtual_dataset(data_name, result)
                else:  # assuming array-like
                    nx_data[data_name] = result
                if is_frames_stack:
                    nx_data[data_name].attrs["interpretation"] = "image"
                nx_data.attrs["signal"] = data_name

            # prepare the direct access plots
            if direct_access:
                nx_process.attrs["default"] = "results"
                if "default" not in nx_entry.attrs:
                    nx_entry.attrs["default"] = posix_join(nx_process.name, "results")

            # Return the internal path to "results"
            return results_path


class NXVolVolume(NXProcessWriter):
    """
    An interface to NXProcessWriter with the same API than tomoscan.esrf.volume.

    NX files are written in two ways:

       1. Partial files containing sub-volumes
       2. Final volume: master file with virtual dataset pointing to partial files

    This class handles the first one, therefore expects the "start_index" parameter.
    In the case of HDF5, a sub-directory is creating to contain the partial files.
    In other words, if file_prefix="recons" and output_dir="/path/to/out":

    /path/to/out/recons.h5 # final master file
    /path/to/out/recons/
      /path/to/out/recons/recons_00000.h5
      /path/to/out/recons/recons_00100.h5
      ...
    """

    def __init__(self, **kwargs):
        # get parameters from kwargs passed to tomoscan XXVolume()
        folder = output_dir = kwargs.get("folder", None)
        volume_basename = file_prefix = kwargs.get("volume_basename", None)
        start_index = kwargs.get("start_index", None)
        overwrite = kwargs.get("overwrite", False)
        entry = kwargs.get("data_path", None)
        self._process_name = kwargs.get("process_name", "reconstruction")
        if any([param is None for param in [folder, volume_basename, start_index, entry]]):
            raise ValueError("Need the following parameters: folder, volume_basename, start_index, data_path")
        #

        # By default, a sub-folder is created so that partial volumes will be one folder below the master file
        # (see example above in class documentation)
        if kwargs.get("create_subfolder", True):
            output_dir = path.join(output_dir, file_prefix)

        if path.exists(output_dir):
            if not (path.isdir(output_dir)):
                raise ValueError("Unable to create directory %s: already exists and is not a directory" % output_dir)
        else:
            pathlib_Path(output_dir).mkdir(parents=True, exist_ok=True)
        #

        file_prefix += str("_%05d" % start_index)
        fname = path.join(output_dir, file_prefix + ".hdf5")

        super().__init__(fname, entry=entry, filemode="a", overwrite=overwrite)
        self.data = None
        self.metadata = None
        self.file_path = fname

    def save(self):
        if self.data is None:
            raise ValueError("Must set data first")
        self.write(self.data, self._process_name, config=self.metadata)

    def save_metadata(self):
        pass  # already done

    def browse_data_files(self):
        return [self.fname]


# COMPAT.
LegacyNXProcessWriter = NXProcessWriter
#

########################################################################################
########################################################################################
########################################################################################


def export_dict_to_h5(dic, h5file, h5path, overwrite_data=True, mode="a"):
    """
    Wrapper on top of silx.io.dictdump.dicttoh5 replacing None with "None"

    Parameters
    -----------
    dic: dict
        Dictionary containing the options
    h5file: str
        File name
    h5path: str
        Path in the HDF5 file
    overwrite_data: bool, optional
        Whether to overwrite data when writing HDF5. Default is True
    mode: str, optional
        File mode. Default is "a" (append).
    """
    modified_dic = convert_dict_values(
        dic,
        {None: "None"},
    )
    update_mode = {True: "modify", False: "add"}[bool(overwrite_data)]
    return dicttoh5(modified_dic, h5file=h5file, h5path=h5path, update_mode=update_mode, mode=mode)


def create_virtual_layout(files_or_pattern, h5_path, base_dir=None, axis=0, dtype="f"):
    """
    Create a HDF5 virtual layout.

    Parameters
    ----------
    files_or_pattern: str or list
        A list of file names, or a wildcard pattern.
        If a list is provided, it will not be sorted! This will have to be
        done before calling this function.
    h5_path: str
        Path inside the HDF5 input file(s)
    base_dir: str, optional
        Base directory when using relative file names.
    axis: int, optional
        Data axis to merge. Default is 0.
    """
    prev_cwd = None
    if base_dir is not None:
        prev_cwd = getcwd()
        chdir(base_dir)
    if isinstance(files_or_pattern, str):
        files_list = glob(files_or_pattern)
        files_list.sort()
    else:  # list
        files_list = files_or_pattern
    if files_list == []:
        raise ValueError("Nothing found as pattern %s" % files_or_pattern)
    virtual_sources = []
    shapes = []
    for fname in files_list:
        with HDF5File(fname, "r", swmr=True) as fid:
            shape = fid[h5_path].shape
        vsource = VirtualSource(fname, name=h5_path, shape=shape)
        virtual_sources.append(vsource)
        shapes.append(shape)
    total_shape = merged_shape(shapes, axis=axis)

    virtual_layout = VirtualLayout(shape=total_shape, dtype=dtype)
    start_idx = 0
    for vsource, shape in zip(virtual_sources, shapes):
        n_imgs = shape[axis]
        # Perhaps there is more elegant
        if axis == 0:
            virtual_layout[start_idx : start_idx + n_imgs] = vsource
        elif axis == 1:
            virtual_layout[:, start_idx : start_idx + n_imgs, :] = vsource
        elif axis == 2:
            virtual_layout[:, :, start_idx : start_idx + n_imgs] = vsource
        else:
            raise ValueError("Only axis 0,1,2 are supported")
        #
        start_idx += n_imgs

    if base_dir is not None:
        chdir(prev_cwd)
    return virtual_layout


def merge_hdf5_files(
    files_or_pattern,
    h5_path,
    output_file,
    process_name,
    output_entry=None,
    output_filemode="a",
    data_name="data",
    processing_index=0,
    config=None,
    base_dir=None,
    axis=0,
    overwrite=False,
    dtype="f",
):
    """
    Parameters
    -----------
    files_or_pattern: str or list
        A list of file names, or a wildcard pattern.
        If a list is provided, it will not be sorted! This will have to be
        done before calling this function.
    h5_path: str
        Path inside the HDF5 input file(s)
    output_file: str
        Path of the output file
    process_name: str
        Name of the process
    output_entry: str, optional
        Output HDF5 root entry (default is "/entry")
    output_filemode: str, optional
        File mode for output file. Default is "a" (append)
    processing_index: int, optional
        Processing index for the output file. Default is 0.
    config: dict, optional
        Dictionary describing the configuration needed to get the results.
    base_dir: str, optional
        Base directory when using relative file names.
    axis: int, optional
        Data axis to merge. Default is 0.
    overwrite: bool, optional
        Whether to overwrite already existing data in the final file.
        Default is False.
    """
    if base_dir is not None:
        prev_cwd = getcwd()
    virtual_layout = create_virtual_layout(files_or_pattern, h5_path, base_dir=base_dir, axis=axis, dtype=dtype)
    nx_file = NXProcessWriter(output_file, entry=output_entry, filemode=output_filemode, overwrite=overwrite)
    nx_file.write(
        virtual_layout,
        process_name,
        processing_index=processing_index,
        config=config,
        data_name=data_name,
        is_frames_stack=True,
    )
    # pylint: disable=E0606
    if base_dir is not None and prev_cwd != getcwd():
        chdir(prev_cwd)


class HSTVolWriter(Writer):
    """
    A writer to mimic PyHST2 ".vol" files
    """

    def __init__(self, fname, append=False, **kwargs):
        super().__init__(fname)
        self.append = append
        self._vol_writer = RawVolume(fname, overwrite=True, append=append)
        self._hst_metadata = kwargs.get("hst_metadata", {})

    def generate_metadata(self, data, **kwargs):
        n_z, n_y, n_x = data.shape
        metadata = {
            "NUM_X": n_x,
            "NUM_Y": n_y,
            "NUM_Z": n_z,
            "voxelSize": 40.0,
            "BYTEORDER": "LOWBYTEFIRST",
            "ValMin": kwargs.get("ValMin", 0.0),
            "ValMax": kwargs.get("ValMin", 1.0),
            "s1": 0.0,
            "s2": 0.0,
            "S1": 0.0,
            "S2": 0.0,
        }
        for key, default_val in metadata.items():
            metadata[key] = kwargs.get(key, None) or self._hst_metadata.get(key, None) or default_val
        return metadata

    @staticmethod
    def sanitize_metadata(metadata):
        # To be fixed in RawVolume
        for what in ["NUM_X", "NUM_Y", "NUM_Z"]:
            metadata[what] = int(metadata[what])
        for what in ["voxelSize", "ValMin", "ValMax", "s1", "s2", "S1", "S2"]:
            metadata[what] = float(metadata[what])

    def write(self, data, *args, config=None, **kwargs):
        existing_metadata = self._vol_writer.load_metadata()
        new_metadata = self.generate_metadata(data)
        if len(existing_metadata) == 0 or not (self.append):
            # first write or append==False
            metadata = new_metadata
        else:
            # append write ; update metadata
            metadata = existing_metadata.copy()
            self.sanitize_metadata(metadata)
            metadata["NUM_Z"] += new_metadata["NUM_Z"]
        self._vol_writer.data = data
        self._vol_writer.metadata = metadata
        self._vol_writer.save()
        # Also save .xml
        self._vol_writer.save_metadata(
            url=DataUrl(
                scheme="lxml",
                file_path=self._vol_writer.metadata_url.file_path().replace(".info", ".xml"),
            )
        )


class HSTVolVolume(HSTVolWriter):
    """
    An interface to HSTVolWriter with the same API than tomoscan.esrf.volume.
    This is really not ideal, see nabu:#381
    """

    def __init__(self, **kwargs):
        file_path = kwargs.get("file_path", None)
        if file_path is None:
            raise ValueError("Missing mandatory 'file_path' parameter")
        super().__init__(file_path, append=kwargs.pop("append", False), **kwargs)
        self.data = None
        self.metadata = None
        self.data_url = self._vol_writer.data_url

    def save(self):
        if self.data is None:
            raise ValueError("Must set data first")
        self.write(self.data)

    def save_metadata(self):
        pass  # already done for HST part - proper metadata is not supported

    def browse_data_files(self):
        return [self.fname]
