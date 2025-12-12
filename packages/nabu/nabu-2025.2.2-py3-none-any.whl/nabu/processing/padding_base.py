import numpy as np
from ..utils import check_supported


class PaddingBase:
    """
    A class for performing padding based on coordinate transform.
    The Cuda and OpenCL backends will subclass this class.
    """

    supported_modes = ["constant", "edge", "reflect", "symmetric", "wrap"]

    def __init__(self, shape, pad_width, mode="constant", **kwargs):
        """
        Initialize a Padding object.

        Parameters
        ----------
        shape: tuple
            Image shape
        pad_width: tuple
            Padding width for each axis. Please see the documentation of numpy.pad().
        mode: str
            Padding mode

        Other Parameters
        ----------------
        constant_values: tuple
            Tuple containing the values to fill when mode="constant" (as in numpy.pad)
        """
        if len(shape) != 2:
            raise ValueError("This class only works on images")
        self.shape = shape
        self._set_mode(mode, **kwargs)
        self._get_padding_arrays(pad_width)

    def _set_mode(self, mode, **kwargs):
        # COMPAT.
        if mode == "edges":
            mode = "edge"
        #
        check_supported(mode, self.supported_modes, "padding mode")
        self.mode = mode
        self._kwargs = kwargs

    def _get_padding_arrays(self, pad_width):
        self.pad_width = pad_width
        if isinstance(pad_width, tuple) and isinstance(pad_width[0], np.ndarray):
            # user-defined coordinate transform
            err_msg = "pad_width must be either a scalar, a tuple in the form ((a, b), (c, d)), or a tuple of two one-dimensional numpy arrays (eg. use numpy.indices(..., sparse=True))"
            if len(pad_width) != 2:
                raise ValueError(err_msg)
            if any([np.squeeze(pw).ndim > 1 for pw in pad_width]):
                raise ValueError(err_msg)
            if self.mode == "constant":
                raise ValueError("Custom coordinate transform does not work with mode='constant'")
            self.mode = "custom"
            self.coords_rows, self.coords_cols = pad_width
        else:
            if self.mode == "constant":
                # no need for coordinate transform here
                constant_values = self._kwargs.get("constant_values", 0)
                self.padded_array_constant = np.pad(
                    np.zeros(self.shape, dtype="f"), self.pad_width, mode="constant", constant_values=constant_values
                )
                self.padded_shape = self.padded_array_constant.shape
                return
            R, C = np.indices(self.shape, dtype=np.int32, sparse=True)
            self.coords_rows = np.pad(R.ravel(), self.pad_width[0], mode=self.mode)
            self.coords_cols = np.pad(C.ravel(), self.pad_width[1], mode=self.mode)
        self.padded_shape = (self.coords_rows.size, self.coords_cols.size)
