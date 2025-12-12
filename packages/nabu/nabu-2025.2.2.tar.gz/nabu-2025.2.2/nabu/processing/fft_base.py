import numpy as np
from ..utils import BaseClassError


class _BaseFFT:
    """
    A base class for FFTs.
    """

    implem = "none"
    ProcessingCls = BaseClassError

    def __init__(self, shape, dtype, r2c=True, axes=None, normalize="rescale", **backend_options):
        """
        Base class for Fast Fourier Transform (FFT).

        Parameters
        ----------
        shape: list of int
            Shape of the input data
        dtype: str or numpy.dtype
            Data type of the input data
        r2c: bool, optional
            Whether to use real-to-complex transform for real-valued input. Default is True.
        axes: list of int, optional
            Axes along which FFT is computed.
              * For 2D transform: axes=(1,0)
              * For batched 1D transform of 2D image: axes=(-1,)
        normalize: str, optional
            Whether to normalize FFT and IFFT. Possible values are:
              * "rescale": in this case, Fourier data is divided by "N"
                before IFFT, so that IFFT(FFT(data)) = data.
                This corresponds to numpy norm=None i.e norm="backward".
              * "ortho": in this case, FFT and IFFT are adjoint of each other,
                the transform is unitary. Both FFT and IFFT are scaled with 1/sqrt(N).
              * "none": no normalization is done : IFFT(FFT(data)) = data*N

        Other Parameters
        -----------------
        backend_options: dict, optional
            Parameters to pass to CudaProcessing or OpenCLProcessing class.
        """
        self._init_backend(backend_options)
        self._set_dtypes(dtype, r2c)
        self._set_shape_and_axes(shape, axes)
        self._configure_batched_transform()
        self._configure_normalization(normalize)
        self._compute_fft_plans()

    def _init_backend(self, backend_options):
        self.processing = self.ProcessingCls(**backend_options)

    def _set_dtypes(self, dtype, r2c):
        self.dtype = np.dtype(dtype)
        dtypes_mapping = {
            np.dtype("float32"): np.complex64,
            np.dtype("float64"): np.complex128,
            np.dtype("complex64"): np.complex64,
            np.dtype("complex128"): np.complex128,
        }
        if self.dtype not in dtypes_mapping:
            raise ValueError("Invalid input data type: got %s" % self.dtype)
        self.dtype_out = dtypes_mapping[self.dtype]
        self.r2c = r2c

    def _set_shape_and_axes(self, shape, axes):
        # Input shape
        if np.isscalar(shape):
            shape = (shape,)
        self.shape = shape
        # Axes
        default_axes = tuple(range(len(self.shape)))
        if axes is None:
            self.axes = default_axes
        else:
            self.axes = tuple(np.array(default_axes)[np.array(axes)])
        # Output shape
        shape_out = self.shape
        if self.r2c:
            reduced_dim = self.axes[-1] if self.axes is not None else -1
            shape_out = list(shape_out)
            shape_out[reduced_dim] = shape_out[reduced_dim] // 2 + 1
            shape_out = tuple(shape_out)
        self.shape_out = shape_out

    def _configure_batched_transform(self):
        pass

    def _configure_normalization(self, normalize):
        pass

    def _compute_fft_plans(self):
        pass

    def get_transformed_axes_shape(self):
        return tuple(int(i) for i in np.array(self.shape)[np.array(self.axes)])


def raise_base_class_error(slf, *args, **kwargs):
    raise ValueError


class _BaseVKFFT(_BaseFFT):
    """
    FFT using VKFFT backend
    """

    implem = "vkfft"
    backend = "none"
    ProcessingCls = BaseClassError
    get_fft_obj = raise_base_class_error

    def _configure_batched_transform(self):
        if self.axes is not None and len(self.shape) == len(self.axes):
            self.axes = None
            return
        if self.r2c:
            # batched Real-to-complex transforms are supported only along fast axes
            if not (is_fast_axes(len(self.shape), self.axes)):
                raise ValueError("For %dD R2C, only batched transforms along fast axes are allowed" % (len(self.shape)))
            self._vkfft_ndim = len(self.axes)
            self.axes = None  # vkfft still can do a batched transform by providing dim=XX, axes=None

    def _configure_normalization(self, normalize):
        self.normalize = normalize
        self._vkfft_norm = {
            "rescale": 1,
            "backward": 1,
            "ortho": "ortho",
            "none": 0,
        }.get(self.normalize, 1)

    def _set_shape_and_axes(self, shape, axes):
        super()._set_shape_and_axes(shape, axes)
        self._vkfft_ndim = None

    def _compute_fft_plans(self):
        self._vkfft_plan = self.get_fft_obj(
            self.shape,
            self.dtype,
            ndim=self._vkfft_ndim,
            inplace=False,
            norm=self._vkfft_norm,
            r2c=self.r2c,
            dct=False,
            axes=self.axes,
            strides=None,
            **self._vkfft_other_init_kwargs,
        )

    def fft(self, array, output=None):
        if output is None:
            output = self.output_fft = self.processing.allocate_array(
                "output_fft", self.shape_out, dtype=self.dtype_out
            )
        return self._vkfft_plan.fft(array, dest=output)

    def ifft(self, array, output=None):
        if output is None:
            output = self.output_ifft = self.processing.allocate_array("output_ifft", self.shape, dtype=self.dtype)
        return self._vkfft_plan.ifft(array, dest=output)


def is_fast_axes(ndim, axes):
    """
    Return true if "axes" are the fast dimensions
    """
    all_axes = list(range(ndim))
    axes = sorted([ax + ndim if ax < 0 else ax for ax in axes])  # transform "-1" to an actual axis index (1 for 2D)
    return all_axes[-len(axes) :] == axes
