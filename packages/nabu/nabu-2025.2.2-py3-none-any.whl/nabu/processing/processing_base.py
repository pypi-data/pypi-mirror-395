import numpy as np
from ..utils import BaseClassError

"""
Base class for OpenCLProcessing and CudaProcessing
Should not be used directly
"""


class ProcessingBase:
    array_class = None
    dtype_to_ctype = BaseClassError

    def __init__(self):
        self._allocated = {}

    def init_arrays_to_none(self, arrays_names):
        """
        Initialize arrays to None. After calling this method, the current instance will
        have self.array_name = None, and self._old_array_name = None.

        Parameters
        ----------
        arrays_names: list of str
            List of arrays names.
        """
        for array_name in arrays_names:
            setattr(self, array_name, None)
            setattr(self, "_old_" + array_name, None)
            self._allocated[array_name] = False

    def recover_arrays_references(self, arrays_names):
        """
        Performs self._array_name = self._old_array_name,
        for each array_name in arrays_names.

        Parameters
        ----------
        arrays_names: list of str
            List of array names
        """
        for array_name in arrays_names:
            old_arr = getattr(self, "_old_" + array_name, None)
            if old_arr is not None:
                setattr(self, array_name, old_arr)

    def _allocate_array_mem(self, shape, dtype):
        raise ValueError("Base class")

    def allocate_array(self, array_name, shape, dtype=np.float32):
        """
        Allocate a GPU array on the current context/stream/device,
        and set 'self.array_name' to this array.

        Parameters
        ----------
        array_name: str
            Name of the array (for book-keeping)
        shape: tuple of int
            Array shape
        dtype: numpy.dtype, optional
            Data type. Default is float32.
        """
        if not self._allocated.get(array_name, False):
            new_device_arr = self._allocate_array_mem(shape, dtype)
            setattr(self, array_name, new_device_arr)
            self._allocated[array_name] = True
        return getattr(self, array_name)

    def set_array(self, array_name, array_ref, dtype=np.float32):
        """
        Set the content of a device array.

        Parameters
        ----------
        array_name: str
            Array name. This method will look for self.array_name.
        array_ref: array (numpy or GPU array)
            Array containing the data to copy to 'array_name'.
        dtype: numpy.dtype, optional
            Data type. Default is float32.
        """
        if isinstance(array_ref, self.array_class):
            current_arr = getattr(self, array_name, None)
            setattr(self, "_old_" + array_name, current_arr)
            setattr(self, array_name, array_ref)
        elif isinstance(array_ref, np.ndarray):
            self.allocate_array(array_name, array_ref.shape, dtype=dtype)
            getattr(self, array_name).set(array_ref)
        else:
            raise TypeError("Expected numpy array or cupy array")
        return getattr(self, array_name)

    def get_array(self, array_name):
        return getattr(self, array_name, None)

    # COMPAT.
    _init_arrays_to_none = init_arrays_to_none
    _recover_arrays_references = recover_arrays_references
    _allocate_array = allocate_array
    _set_array = set_array
    # --

    def is_contiguous(self, arr):
        if isinstance(arr, self.array_class):
            return arr.flags.c_contiguous
        elif isinstance(arr, np.ndarray):
            return arr.flags["C_CONTIGUOUS"]
        else:
            raise TypeError

    def check_array(self, arr, expected_shape, expected_dtype="f", check_contiguous=True):
        """
        Check whether a given array is suitable for being processed (shape, dtype, contiguous)
        """
        if arr.shape != expected_shape:
            raise ValueError("Expected shape %s but got %s" % (str(expected_shape), str(arr.shape)))
        if arr.dtype != np.dtype(expected_dtype):
            raise ValueError("Expected data type %s but got %s" % (str(expected_dtype), str(arr.dtype)))
        if check_contiguous and not (self.is_contiguous(arr)):
            raise ValueError("Expected C-contiguous array")

    def kernel(self, *args, **kwargs):
        raise ValueError("Base class")

    def to_device(self, array_name, array):
        arr_ref = self.allocate_array(array_name, array.shape, dtype=array.dtype)
        arr_ref.set(array)
        return arr_ref
