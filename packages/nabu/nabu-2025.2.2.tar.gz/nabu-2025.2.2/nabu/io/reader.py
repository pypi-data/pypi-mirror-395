import os
from threading import get_ident
from multiprocessing.pool import ThreadPool
from posixpath import sep as posix_sep, join as posix_join
import numpy as np
from h5py import Dataset
from silx.io import get_data
from silx.io.dictdump import h5todict
from tomoscan.io import HDF5File
from .utils import convert_dict_values, get_first_hdf5_entry
from ..misc.binning import binning as image_binning
from ..utils import (
    check_supported,
    deprecated,
    deprecation_warning,
    indices_to_slices,
    compacted_views,
    merge_slices,
    get_3D_subregion,
    get_shape_from_sliced_dims,
    get_size_from_sliced_dimension,
    safe_format,
)

try:
    from fabio.edfimage import EdfImage
except ImportError:
    EdfImage = None


class Reader:
    """
    Abstract class for various file readers.
    """

    def __init__(self, sub_region=None):
        """
        Parameters
        ----------
        sub_region: tuple, optional
            Coordinates in the form (start_x, end_x, start_y, end_y), to read
            a subset of each frame. It can be used for Regions of Interest (ROI).
            Indices start at zero !
        """
        self._set_default_parameters(sub_region)

    def _set_default_parameters(self, sub_region):
        self._set_subregion(sub_region)

    def _set_subregion(self, sub_region):
        self.sub_region = sub_region
        if sub_region is not None:
            start_x, end_x, start_y, end_y = sub_region
            self.start_x = start_x
            self.end_x = end_x
            self.start_y = start_y
            self.end_y = end_y
        else:
            self.start_x = 0
            self.end_x = None
            self.start_y = 0
            self.end_y = None

    def get_data(self, data_url):
        """
        Get data from a silx.io.url.DataUrl
        """
        raise ValueError("Base class")

    def release(self):
        """
        Release the file if needed.
        """
        pass


class NPReader(Reader):
    multi_load = True

    def __init__(self, sub_region=None, mmap=True):
        """
        Reader for NPY/NPZ files. Mostly used for internal development.
        Please refer to the documentation of nabu.io.reader.Reader
        """
        super().__init__(sub_region=sub_region)
        self._file_desc = {}
        self._set_mmap(mmap)

    def _set_mmap(self, mmap):
        self.mmap_mode = "r" if mmap else None

    def _open(self, data_url):
        file_path = data_url.file_path()
        file_ext = self._get_file_type(file_path)
        if file_ext == "npz":
            if file_path not in self._file_desc:
                self._file_desc[file_path] = np.load(file_path, mmap_mode=self.mmap_mode)
            data_ref = self._file_desc[file_path][data_url.data_path()]
        else:
            data_ref = np.load(file_path, mmap_mode=self.mmap_mode)
        return data_ref

    @staticmethod
    def _get_file_type(fname):
        if fname.endswith(".npy"):
            return "npy"
        elif fname.endswith(".npz"):
            return "npz"
        else:
            raise ValueError("Not a numpy file: %s" % fname)

    def get_data(self, data_url):
        data_ref = self._open(data_url)
        data_slice = data_url.data_slice()
        if data_slice is None:
            res = data_ref[self.start_y : self.end_y, self.start_x : self.end_x]
        else:
            res = data_ref[data_slice, self.start_y : self.end_y, self.start_x : self.end_x]
        return res

    def release(self):
        for fname, fdesc in self._file_desc.items():
            if fdesc is not None:
                fdesc.close()
                self._file_desc[fname] = None

    def __del__(self):
        self.release()


class EDFReader(Reader):
    multi_load = False  # not implemented

    def __init__(self, sub_region=None):
        """
        A class for reading series of EDF Files.
        Multi-frames EDF are not supported.
        """
        if EdfImage is None:
            raise ImportError("Need fabio to use this reader")
        super().__init__(sub_region=sub_region)
        self._reader = EdfImage()
        self._first_fname = None

    def read(self, fname):
        if self._first_fname is None:
            self._first_fname = fname
            self._reader.read(fname)
        if self.sub_region is None:
            data = self._reader.data
        else:
            data = self._reader.fast_read_roi(fname, (slice(self.start_y, self.end_y), slice(self.start_x, self.end_x)))
        # self._reader.close()
        return data

    def get_data(self, data_url):
        return self.read(data_url.file_path())


class HDF5Reader(Reader):
    multi_load = True

    def __init__(self, sub_region=None):
        """
        A class for reading a HDF5 File.
        """
        super().__init__(sub_region=sub_region)
        self._file_desc = {}

    def _open(self, file_path):
        if file_path not in self._file_desc:
            self._file_desc[file_path] = HDF5File(file_path, "r", swmr=True)

    def get_data(self, data_url):
        file_path = data_url.file_path()
        self._open(file_path)
        h5dataset = self._file_desc[file_path][data_url.data_path()]
        data_slice = data_url.data_slice()
        if data_slice is None:
            res = h5dataset[self.start_y : self.end_y, self.start_x : self.end_x]
        else:
            res = h5dataset[data_slice, self.start_y : self.end_y, self.start_x : self.end_x]

        return res

    def release(self):
        for fname, fdesc in self._file_desc.items():
            if fdesc is not None:
                try:
                    fdesc.close()
                    self._file_desc[fname] = None
                except Exception as exc:
                    print("Error while closing %s: %s" % (fname, str(exc)))

    def __del__(self):
        self.release()


class HDF5Loader:
    """
    An alternative class to HDF5Reader where information is first passed at class instantiation
    """

    def __init__(self, fname, data_path, sub_region=None, data_buffer=None, pre_allocate=True, dtype="f"):
        self.fname = fname
        self.data_path = data_path
        self._set_subregion(sub_region)
        if not ((data_buffer is not None) ^ (pre_allocate is True)):
            raise ValueError("Please provide either 'data_buffer' or 'pre_allocate'")
        self.data = data_buffer
        self._loaded = False
        self.expected_shape = get_hdf5_dataset_shape(fname, data_path, sub_region=sub_region)
        if pre_allocate:
            self.data = np.zeros(self.expected_shape, dtype=dtype)

    def _set_subregion(self, sub_region):
        self.sub_region = sub_region
        if sub_region is not None:
            start_z, end_z, start_y, end_y, start_x, end_x = sub_region
            self.start_x, self.end_x = start_x, end_x
            self.start_y, self.end_y = start_y, end_y
            self.start_z, self.end_z = start_z, end_z
        else:
            self.start_x, self.end_x = None, None
            self.start_y, self.end_y = None, None
            self.start_z, self.end_z = None, None

    def load_data(self, force_load=False, output=None):
        if self._loaded and not force_load:
            return self.data
        output = self.data if output is None else output
        with HDF5File(self.fname, "r") as fdesc:
            if output is None:
                output = fdesc[self.data_path][
                    self.start_z : self.end_z, self.start_y : self.end_y, self.start_x : self.end_x
                ]
            else:
                output[:] = fdesc[self.data_path][
                    self.start_z : self.end_z, self.start_y : self.end_y, self.start_x : self.end_x
                ]
        self._loaded = True
        return output


class VolReaderBase:
    """
    Base class with common code for data readers (EDFStackReader, NXTomoReader, etc)
    """

    def __init__(self, *args, **kwargs):
        raise ValueError("Base class")

    def _set_subregion(self, sub_region):
        slice_angle, slice_z, slice_x = (None, None, None)
        if isinstance(sub_region, slice):
            # Assume selection is done only along dimension 0
            slice_angle = sub_region
            slice_z = None
            slice_x = None
        if isinstance(sub_region, (tuple, list)):
            slice_angle, slice_z, slice_x = sub_region
        self.sub_region = (
            slice_angle if slice_angle is not None else slice(None, None),
            slice_z if slice_z is not None else slice(None, None),
            slice_x if slice_x is not None else slice(None, None),
        )

    def _set_processing_function(self, processing_func, processing_func_args, processing_func_kwargs):
        self.processing_func = processing_func
        self._processing_func_args = processing_func_args or []
        self._processing_func_kwargs = processing_func_kwargs or {}

    def _get_output(self, array):
        if array is not None:
            if array.shape != self.output_shape:
                raise ValueError("Expected output shape %s but got %s" % (self.output_shape, array.shape))
            if array.dtype != self.output_dtype:
                raise ValueError("Expected output dtype '%s' but got '%s'" % (self.output_dtype, array.dtype))
            output = array
        else:
            output = np.zeros(self.output_shape, dtype=self.output_dtype)
        return output

    def get_frames_indices(self):
        return np.arange(self.data_shape_total[0])[self._source_selection[0]]


class NXTomoReader(VolReaderBase):
    image_key_path = "instrument/detector/image_key_control"
    multiple_frames_per_file = True

    def __init__(
        self,
        filename,
        data_path="{entry}/instrument/detector/data",
        sub_region=None,
        image_key=0,
        output_dtype=np.float32,
        processing_func=None,
        processing_func_args=None,
        processing_func_kwargs=None,
    ):
        """
        Read a HDF5 file in NXTomo layout.

        Parameters
        ----------
        filename: str
            Path to the file to read.
        data_path: str
            Path within the HDF5 file, eg. "entry/instrument/detector/data".
            Default is {entry}/data/data where {entry} is a magic keyword for the first entry.
        sub_region: slice or tuple, optional
            Region to select within the data, once the "image key" selection has been done.
            If None, all the data (corresponding to image_key) is selected.
            If slice(start, stop) is provided, the selection is done along dimension 0.
            Otherwise, it must be a 3-tuple of slices in the form
            (slice(start_angle, end_angle, step_angle), slice(start_z, end_z, step_z), slice(start_x, end_x, step_x))
            Each of the parameters can be None, in this case the default start and end are taken in each dimension.
        output_dtype: numpy.dtype, optional
            Output data type if the data memory is allocated by this class. Default is float32.
        image_key: int, or None, optional
            Image type to read (see NXTomo documentation). 0 for projections, 1 for flat-field, 2 for dark field.
            If set to None, all the data will be read.
        processing_func: callable, optional
            Function to be called on each loaded stack of images.
            If provided, this function first argument must be the source buffer (3D array: stack of raw images),
            and the second argument must be the destination buffer (3D array, stack of output images). It can be None.

        Other Parameters
        ----------------
        The other parameters are passed to "processing_func" if this parameter is not None.

        """
        self.filename = filename
        self.data_path = safe_format(data_path or "", entry=get_first_hdf5_entry(filename))
        self._set_image_key(image_key)
        self._set_subregion(sub_region)
        self._get_shape()
        self._set_processing_function(processing_func, processing_func_args, processing_func_kwargs)
        self._get_source_selection()
        self._init_output(output_dtype)

    def _get_input_dtype(self):
        return get_hdf5_dataset_dtype(self.filename, self.data_path)

    def _init_output(self, output_dtype):
        output_shape = get_shape_from_sliced_dims(self.data_shape_total, self._source_selection)
        self.output_dtype = output_dtype
        self._output_shape_no_processing = output_shape
        if self.processing_func is not None:
            test_subvolume = np.zeros((1,) + output_shape[1:], dtype=self._get_input_dtype())
            out = self.processing_func(
                test_subvolume, None, *self._processing_func_args, **self._processing_func_kwargs
            )
            output_image_shape = out.shape[1:]
            output_shape = (output_shape[0],) + output_image_shape
        self.output_shape = output_shape
        self._tmp_dst_buffer = None

    def _set_image_key(self, image_key):
        self.image_key = image_key
        entry = get_entry_from_h5_path(self.data_path)
        image_key_path = posix_join(entry, self.image_key_path)
        with HDF5File(self.filename, "r") as f:
            image_key_val = f[image_key_path][()]
        idx = np.where(image_key_val == image_key)[0]
        if len(idx) == 0:
            raise FileNotFoundError("No frames found with image key = %d" % image_key)
        self._image_key_slices = indices_to_slices(idx)

    def _get_shape(self):
        # Shape of the total HDF5-NXTomo data (including darks and flats)
        self.data_shape_total = get_hdf5_dataset_shape(self.filename, self.data_path)
        # Shape of the data once the "image key" is selected
        n_imgs = self.data_shape_total[0]
        self.data_shape_imagekey = (
            sum([get_size_from_sliced_dimension(n_imgs, slice_) for slice_ in self._image_key_slices]),
        ) + self.data_shape_total[1:]

        # Shape of the data after sub-regions are selected
        self.data_shape_subregion = get_shape_from_sliced_dims(self.data_shape_imagekey, self.sub_region)

    def _get_source_selection(self):
        if len(self._image_key_slices) == 1 and self.processing_func is None:
            # Simple case:
            #   - One single chunk to load, i.e len(self._image_key_slices) == 1
            #   - No on-the-fly processing (binning, distortion correction, ...)
            # In this case, we can use h5py read_direct() to avoid extraneous memory consumption
            image_key_slice = self._image_key_slices[0]
            # merge image key selection and user selection (if any)
            angles_slice = self.sub_region[0]
            if isinstance(angles_slice, slice) or angles_slice is None:
                angles_slice = merge_slices(image_key_slice, self.sub_region[0] or slice(None, None))
            else:  # assuming numpy array
                # TODO more elegant
                angles_slice = np.arange(self.data_shape_total[0], dtype=np.uint64)[image_key_slice][angles_slice]
            self._source_selection = (angles_slice,) + self.sub_region[1:]
        else:
            user_selection_dim0 = self.sub_region[0]
            indices = np.arange(self.data_shape_total[0])
            data_selection_indices_axis0 = np.hstack(
                [indices[image_key_slice] for image_key_slice in self._image_key_slices]
            )[user_selection_dim0]

            self._source_selection = (data_selection_indices_axis0,) + self.sub_region[1:]

    def _get_temporary_buffer(self, convert_after_reading):
        if self._tmp_dst_buffer is None:
            shape = self._output_shape_no_processing
            dtype = self.output_dtype if not (convert_after_reading) else self._get_input_dtype()
            self._tmp_dst_buffer = np.zeros(shape, dtype=dtype)
        return self._tmp_dst_buffer

    def load_data(self, output=None, convert_after_reading=True):
        """
        Read data.

        Parameters
        -----------
        output: array-like, optional
            Destination 3D array that will hold the data.
            If provided, use this memory buffer instead of allocating the memory.
            Its shape must be compatible with the selection of 'sub_region' and 'image_key'.
        conver_after_reading: bool, optional
            Whether to do the dtype conversion (if any, eg. uint16 to float32) after data reading.
            With using h5py's read_direct(), reading from uint16 to float32 is extremely slow,
            so data type conversion should be done after reading.
            The drawback is that it requires more memory.
        """
        output = self._get_output(output)
        convert_after_reading &= np.dtype(self.output_dtype) != np.dtype(self._get_input_dtype())
        if convert_after_reading or self.processing_func is not None:
            dst_buffer = self._get_temporary_buffer(convert_after_reading)
        else:
            dst_buffer = output

        with HDF5File(self.filename, "r") as f:
            dptr = f[self.data_path]
            dptr.read_direct(
                dst_buffer,
                source_sel=self._source_selection,
                dest_sel=None,
            )
        if self.processing_func is not None:
            self.processing_func(dst_buffer, output, *self._processing_func_args, **self._processing_func_kwargs)
        elif dst_buffer.ctypes.data != output.ctypes.data:
            output[:] = dst_buffer[:]  # cast

        return output


class NXDarksFlats:

    _reduce_func = {
        "median": np.median,
        "mean": np.mean,
    }

    def __init__(self, filename, **nxtomoreader_kwargs):
        nxtomoreader_kwargs.pop("image_key", None)
        self.darks_reader = NXTomoReader(filename, image_key=2, **nxtomoreader_kwargs)
        self.flats_reader = NXTomoReader(filename, image_key=1, **nxtomoreader_kwargs)
        self._raw_darks = None
        self._raw_flats = None

    def _get_raw_frames(self, what, force_reload=False, as_multiple_array=True):
        check_supported(what, ["darks", "flats"], "frame type")
        loaded_frames = getattr(self, "_raw_%s" % what)
        reader = getattr(self, "%s_reader" % what)
        if force_reload or loaded_frames is None:
            loaded_frames = reader.load_data()
            setattr(self, "_raw_%s" % what, loaded_frames)
        res = loaded_frames
        if as_multiple_array:
            slices_ = compacted_views(reader._image_key_slices)
            return [res[slice_] for slice_ in slices_]
        return res

    def _get_reduced_frames(self, what, method="mean", force_reload=False, as_dict=False):
        raw_frames = self._get_raw_frames(what, force_reload=force_reload, as_multiple_array=True)
        reduced_frames = [self._reduce_func[method](frames, axis=0) for frames in raw_frames]
        reader = getattr(self, "%s_reader" % what)
        if as_dict:
            return {k: v for k, v in zip([s.start for s in reader._image_key_slices], reduced_frames)}
        return reduced_frames

    def get_raw_darks(self, force_reload=False, as_multiple_array=True):
        return self._get_raw_frames("darks", force_reload=force_reload, as_multiple_array=as_multiple_array)

    def get_raw_flats(self, force_reload=False, as_multiple_array=True):
        return self._get_raw_frames("flats", force_reload=force_reload, as_multiple_array=as_multiple_array)

    def get_reduced_darks(self, method="mean", force_reload=False, as_dict=False):
        return self._get_reduced_frames("darks", method=method, force_reload=force_reload, as_dict=as_dict)

    def get_reduced_flats(self, method="median", force_reload=False, as_dict=False):
        return self._get_reduced_frames("flats", method=method, force_reload=force_reload, as_dict=as_dict)

    def get_raw_current(self, h5_path="{entry}/control/data"):
        h5_path = safe_format(h5_path, entry=self.flats_reader.data_path.split(posix_sep)[0])
        with HDF5File(self.flats_reader.filename, "r") as f:
            current = f[h5_path][()]
        return {sl.start: current[sl] for sl in self.flats_reader._image_key_slices}

    def get_reduced_current(self, h5_path="{entry}/control/data", method="median"):
        current = self.get_raw_current(h5_path=h5_path)
        return {k: self._reduce_func[method](current[k]) for k in current}


class EDFStackReader(VolReaderBase):
    multiple_frames_per_file = False

    def __init__(
        self,
        filenames,
        sub_region=None,
        output_dtype=np.float32,
        n_reading_threads=1,
        processing_func=None,
        processing_func_args=None,
        processing_func_kwargs=None,
    ):
        self.filenames = filenames
        self.n_reading_threads = n_reading_threads
        self._set_subregion(sub_region)
        self._get_shape()
        self._set_processing_function(processing_func, processing_func_args, processing_func_kwargs)
        self._get_source_selection()
        self._init_output(output_dtype)

    def _get_input_dtype(self):
        return EDFReader().read(self.filenames[0]).dtype

    def _get_shape(self):
        first_filename = self.filenames[0]

        # Shape of the total data (without subregion selection)
        reader_all = EDFReader()
        first_frame_full = reader_all.read(first_filename)
        self.data_shape_total = (len(self.filenames),) + first_frame_full.shape
        self.input_dtype = first_frame_full.dtype

        self.data_shape_subregion = get_shape_from_sliced_dims(
            self.data_shape_total, self.sub_region
        )  # might fail if sub_region is not a slice ?

    def _init_output(self, output_dtype):
        output_shape = get_shape_from_sliced_dims(self.data_shape_total, self._source_selection)
        self.output_dtype = output_dtype
        if self.processing_func is not None:
            test_image = np.zeros(output_shape[1:], dtype=self._get_input_dtype())
            out = self.processing_func(test_image, *self._processing_func_args, **self._processing_func_kwargs)
            output_image_shape = out.shape
            output_shape = (output_shape[0],) + output_image_shape
        self.output_shape = output_shape

    def _get_source_selection(self):
        self._source_selection = self.sub_region

        self._sub_region_xy_for_edf_reader = (
            self.sub_region[2].start or 0,
            self.sub_region[2].stop or self.data_shape_total[2],
            self.sub_region[1].start or 0,
            self.sub_region[1].stop or self.data_shape_total[1],
        )
        self.filenames_subsampled = self.filenames[self.sub_region[0]]

    def load_data(self, output=None):
        output = self._get_output(output)

        readers = {}

        def _init_reader_thread():
            readers[get_ident()] = EDFReader(self._sub_region_xy_for_edf_reader)

        def _get_data(i_fname):
            i, fname = i_fname
            reader = readers[get_ident()]
            frame = reader.read(fname)
            if self.processing_func is not None:
                frame = self.processing_func(frame, *self._processing_func_args, **self._processing_func_kwargs)
            output[i] = frame

        with ThreadPool(self.n_reading_threads, initializer=_init_reader_thread) as tp:
            tp.map(
                _get_data,
                zip(
                    range(len(self.filenames_subsampled)),
                    self.filenames_subsampled,
                ),
            )

        return output


Readers = {
    "edf": EDFReader,
    "hdf5": HDF5Reader,
    "h5": HDF5Reader,
    "nx": HDF5Reader,
    "npz": NPReader,
    "npy": NPReader,
}


@deprecated(
    "Function load_images_from_dataurl_dict is deprecated and will be removed in a fugure version", do_print=True
)
def load_images_from_dataurl_dict(data_url_dict, sub_region=None, dtype="f", binning=None):
    """
    Load a dictionary of dataurl into numpy arrays.

    Parameters
    ----------
    data_url_dict: dict
        A dictionary where the keys are integers (the index of each image in the dataset),
        and the values are numpy.ndarray (data_url_dict).
    sub_region: tuple, optional
        Tuple in the form (y_subregion, x_subregion)
        where xy_subregion is a tuple in the form slice(start, stop, step)

    Returns
    --------
    res: dict
        A dictionary where the keys are the same as `data_url_dict`, and the values are numpy arrays.

    Notes
    -----
    This function is used to load flats/darks. Usually, these are reduced flats/darks, meaning that
    'data_url_dict' is a collection of a handful of files (less than 10).
    To load more frames, it would be best to use NXTomoReader / EDFStackReader.
    """
    res = {}
    if sub_region is not None and not isinstance(sub_region[0], slice):
        if len(sub_region) == 4:  # (start_y, end_y, start_x, end_x)
            deprecation_warning(
                "The parameter 'sub_region' was passed as (start_x, end_x, start_y, end_y). This is deprecated and will yield an error in the future. Please use the syntax ((start_z, end_z), (start_x, end_x))",
                do_print=True,
                func_name="load_images_from_dataurl_dict",
            )
            sub_region = (slice(sub_region[2], sub_region[3]), slice(sub_region[0], sub_region[1]))
        else:  # ((start_z, end_z), (start_x, end_x))
            sub_region = tuple(slice(s[0], s[1]) for s in sub_region)
    for idx, data_url in data_url_dict.items():
        frame = get_data(data_url)
        if sub_region is not None:
            frame = frame[sub_region[0], sub_region[1]]
        if binning is not None:
            frame = image_binning(frame, binning, out_dtype=dtype)
        res[idx] = frame
    return res


def load_images_stack_from_hdf5(fname, h5_data_path, sub_region=None):
    """
    Load a 3D dataset from a HDF5 file.

    Parameters
    -----------
    fname: str
        File path
    h5_data_path: str
        Data path within the HDF5 file
    sub_region: tuple, optional
        Tuple indicating which sub-volume to load, in the form (xmin, xmax, ymin, ymax, zmin, zmax)
        where the 3D dataset has the python shape (N_Z, N_Y, N_X).
        This means that the data will be loaded as `data[zmin:zmax, ymin:ymax, xmin:xmax]`.
    """
    xmin, xmax, ymin, ymax, zmin, zmax = get_3D_subregion(sub_region)
    with HDF5File(fname, "r") as f:
        d_ptr = f[h5_data_path]
        data = d_ptr[zmin:zmax, ymin:ymax, xmin:xmax]
    return data


def get_hdf5_dataset_shape(fname, h5_data_path, sub_region=None):
    zmin, zmax, ymin, ymax, xmin, xmax = get_3D_subregion(sub_region)
    with HDF5File(fname, "r") as f:
        d_ptr = f[h5_data_path]
        shape = d_ptr.shape
    n_z, n_y, n_x = shape
    # perhaps there is more elegant
    res_shape = []
    for n, bounds in zip([n_z, n_y, n_x], ((zmin, zmax), (ymin, ymax), (xmin, xmax))):
        res_shape.append(np.arange(n)[bounds[0] : bounds[1]].size)
    return tuple(res_shape)


def get_hdf5_dataset_dtype(fname, h5_data_path):
    with HDF5File(fname, "r") as f:
        d_ptr = f[h5_data_path]
        dtype = d_ptr.dtype
    return dtype


def get_entry_from_h5_path(h5_path):
    v = h5_path.split(posix_sep)
    return v[0] or v[1]


def list_hdf5_entries(fname):
    with HDF5File(fname, "r") as f:
        entries = list(f.keys())
    return entries


def check_virtual_sources_exist(fname, data_path):
    with HDF5File(fname, "r") as f:
        if data_path not in f:
            print("No dataset %s in file %s" % (data_path, fname))
            return False
        dptr = f[data_path]
        if not dptr.is_virtual:
            return True
        for vsource in dptr.virtual_sources():
            vsource_fname = os.path.join(os.path.dirname(dptr.file.filename), vsource.file_name)
            if not os.path.isfile(vsource_fname):
                print("No such file: %s" % vsource_fname)
                return False
            elif not check_virtual_sources_exist(vsource_fname, vsource.dset_name):
                print("Error with virtual source %s" % vsource_fname)
                return False
    return True


def get_hdf5_file_all_virtual_sources(file_path_or_obj, return_only_filenames=False):
    result = []

    def collect_vsources(name, obj):
        if isinstance(obj, Dataset) and obj.is_virtual:
            vs = obj.virtual_sources()
            if return_only_filenames:
                vs = [vs_.file_name for vs_ in vs]
            result.append({name: vs})

    _self_opened_file = False
    if isinstance(file_path_or_obj, str):
        fdesc = HDF5File(file_path_or_obj, "r")
        _self_opened_file = True
    else:
        fdesc = file_path_or_obj

    fdesc.visititems(collect_vsources)

    if _self_opened_file:
        fdesc.close()
    return result


def import_h5_to_dict(h5file, h5path, asarray=False):
    """
    Wrapper on top of silx.io.dictdump.dicttoh5 replacing "None" with None

    Parameters
    -----------
    h5file: str
        File name
    h5path: str
        Path in the HDF5 file
    asarray: bool, optional
        Whether to convert each numeric value to an 0D array. Default is False.
    """
    dic = h5todict(h5file, path=h5path, asarray=asarray)
    modified_dic = convert_dict_values(dic, {"None": None}, bytes_tostring=True)
    return modified_dic
