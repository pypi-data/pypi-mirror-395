import numpy as np
from ..utils import BaseClassError, get_opencl_srcfile, updiv
from ..opencl.kernel import OpenCLKernel
from ..opencl.processing import OpenCLProcessing
from pyopencl.tools import dtype_to_ctype as cl_dtype_to_ctype


class FFTshiftBase:
    KernelCls = BaseClassError
    ProcessingCls = BaseClassError
    dtype_to_ctype = BaseClassError
    backend = "none"

    def __init__(self, shape, dtype, dst_dtype=None, axes=None, **backend_options):
        """

        Parameters
        ----------
        shape: tuple
            Array shape - can be 1D or 2D. 3D is not supported.
        dtype: str or numpy.dtype
            Data type, eg. "f", numpy.complex64, ...
        dst_dtype: str or numpy.dtype
            Output data type. If not provided (default), the shift is done in-place.
        axes: tuple, optional
            Axes over which to shift.  Default is None, which shifts all axes.

        Other Parameters
        ----------------
        backend_options:
            named arguments to pass to CudaProcessing or OpenCLProcessing
        """
        #
        if axes not in [1, (1,), (-1,)]:
            raise NotImplementedError
        #
        self.processing = self.ProcessingCls(**backend_options)
        self.shape = shape
        if len(self.shape) not in [1, 2]:
            raise ValueError("Expected 1D or 2D array")
        self.dtype = np.dtype(dtype)
        self.dst_dtype = dst_dtype

        if dst_dtype is None:
            self._configure_inplace_shift()
        else:
            self._configure_out_of_place_shift()
        self._configure_kenel_initialization()
        self._fftshift_kernel = self.KernelCls(*self._kernel_init_args, **self._kernel_init_kwargs)
        self._configure_kernel_call()

    def _configure_inplace_shift(self):
        self.inplace = True
        # in-place on odd-sized array is more difficult - see fftshift.cl
        if self.shape[-1] & 1:
            raise NotImplementedError
        #
        self._kernel_init_args = [
            "fftshift_x_inplace",
        ]
        self._kernel_init_kwargs = {
            "options": [
                "-DDTYPE=%s" % self.dtype_to_ctype(self.dtype),
            ],
        }

    def _configure_out_of_place_shift(self):
        self.inplace = False
        self._kernel_init_args = [
            "fftshift_x",
        ]
        self._kernel_init_kwargs = {
            "options": [
                "-DDTYPE=%s" % self.dtype_to_ctype(self.dtype),
                "-DDTYPE_OUT=%s" % self.dtype_to_ctype(np.dtype(self.dst_dtype)),
            ],
        }
        additional_flag = None
        input_is_complex = np.iscomplexobj(np.ones(1, dtype=self.dtype))
        output_is_complex = np.iscomplexobj(np.ones(1, dtype=self.dst_dtype))
        if not (input_is_complex) and output_is_complex:
            additional_flag = "-DCAST_TO_COMPLEX"
        if input_is_complex and not (output_is_complex):
            additional_flag = "-DCAST_TO_REAL"
        if additional_flag is not None:
            self._kernel_init_kwargs["options"].append(additional_flag)

    def _call_fftshift_inplace(self, arr, direction):
        self._fftshift_kernel(  # pylint: disable=E1102
            arr, np.int32(self.shape[1]), np.int32(self.shape[0]), np.int32(direction), **self._kernel_kwargs
        )
        return arr

    def _call_fftshift_out_of_place(self, arr, dst, direction):
        if dst is None:
            dst = self.processing.allocate_array("dst", arr.shape, dtype=self.dst_dtype)
        self._fftshift_kernel(  # pylint: disable=E1102
            arr, dst, np.int32(self.shape[1]), np.int32(self.shape[0]), np.int32(direction), **self._kernel_kwargs
        )
        return dst

    def fftshift(self, arr, dst=None):
        if self.inplace:
            return self._call_fftshift_inplace(arr, 1)
        else:
            return self._call_fftshift_out_of_place(arr, dst, 1)

    def ifftshift(self, arr, dst=None):
        if self.inplace:
            return self._call_fftshift_inplace(arr, -1)
        else:
            return self._call_fftshift_out_of_place(arr, dst, -1)


class OpenCLFFTshift(FFTshiftBase):
    KernelCls = OpenCLKernel
    ProcessingCls = OpenCLProcessing
    dtype_to_ctype = cl_dtype_to_ctype
    backend = "opencl"

    def _configure_kenel_initialization(self):
        self._kernel_init_args.append(self.processing.queue)
        self._kernel_init_kwargs.update(
            {
                "filename": get_opencl_srcfile("fftshift.cl"),
                "queue": self.processing.queue,
            }
        )

    def _configure_kernel_call(self):
        # TODO in-place fftshift needs to launch only arr.size//2 threads
        block = (16, 16, 1)
        grid = [updiv(a, b) * b for a, b in zip(self.shape[::-1], block)]
        self._kernel_kwargs = {"global_size": grid, "local_size": block}
