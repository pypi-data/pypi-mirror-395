import numpy as np
from ..utils import get_opencl_srcfile, get_cuda_srcfile, updiv, BaseClassError, MissingComponentError
from ..opencl.utils import __has_pyopencl__
from ..cuda.utils import __has_cupy__, dtype_to_ctype as cu_dtype_to_ctype

if __has_pyopencl__:
    from ..opencl.kernel import OpenCLKernel
    from ..opencl.processing import OpenCLProcessing
    from pyopencl.tools import dtype_to_ctype as cl_dtype_to_ctype
else:
    OpenCLKernel = OpenCLProcessing = cl_dtype_to_ctype = MissingComponentError("need pyopencl to use this class")
if __has_cupy__:
    from ..cuda.kernel import CudaKernel
    from ..cuda.processing import CudaProcessing
else:
    CudaKernel = CudaProcessing = cu_dtype_to_ctype = MissingComponentError("need cupy to use this class")


# pylint: disable=E1101, E1102
class TransposeBase:
    """
    A class for transposing (out-of-place) a cuda or opencl array
    """

    KernelCls = BaseClassError
    ProcessingCls = BaseClassError
    dtype_to_ctype = BaseClassError
    backend = "none"

    def __init__(self, shape, dtype, dst_dtype=None, **backend_options):
        self.processing = self.ProcessingCls(**(backend_options or {}))
        self.shape = shape
        self.dtype = dtype
        self.dst_dtype = dst_dtype or dtype
        if len(shape) != 2:
            raise ValueError("Expected 2D array")

        self._kernel_init_args = [
            "transpose",
        ]
        self._kernel_init_kwargs = {
            "options": (
                "-DSRC_DTYPE=%s" % self.__class__.dtype_to_ctype(self.dtype),
                "-DDST_DTYPE=%s" % self.__class__.dtype_to_ctype(self.dst_dtype),
            ),
        }
        self._configure_kenel_initialization()
        self._transpose_kernel = self.KernelCls(*self._kernel_init_args, **self._kernel_init_kwargs)
        self._configure_kernel_call()

    def __call__(self, arr, dst=None):
        if dst is None:
            dst = self.processing.allocate_array("dst", self.shape[::-1], dtype=self.dst_dtype)
        self._transpose_kernel(arr, dst, np.int32(self.shape[1]), np.int32(self.shape[0]), **self._kernel_kwargs)
        return dst


class CudaTranspose(TransposeBase):
    KernelCls = CudaKernel
    ProcessingCls = CudaProcessing
    dtype_to_ctype = cu_dtype_to_ctype
    backend = "cuda"

    def _configure_kenel_initialization(self):
        self._kernel_init_kwargs.update(
            {
                "filename": get_cuda_srcfile("transpose.cu"),
            }
        )

    def _configure_kernel_call(self):
        block = (32, 32, 1)
        grid = tuple(updiv(a, b) for a, b in zip(self.shape, block))
        self._kernel_kwargs = {"grid": grid, "block": block}


class OpenCLTranspose(TransposeBase):
    KernelCls = OpenCLKernel
    ProcessingCls = OpenCLProcessing
    dtype_to_ctype = cl_dtype_to_ctype
    backend = "opencl"

    def _configure_kenel_initialization(self):
        self._kernel_init_args.append(self.processing.queue)
        self._kernel_init_kwargs.update(
            {
                "filename": get_opencl_srcfile("transpose.cl"),
            }
        )

    def _configure_kernel_call(self):
        block = (16, 16, 1)
        grid = [updiv(a, b) * b for a, b in zip(self.shape, block)]
        self._kernel_kwargs = {"global_size": grid, "local_size": block}


#
# An attempt to have a simplified access to transpose operation
#

# (backend, shape, dtype, dtype_out)
_transposes_store = {}


def transpose(array, dst=None, **backend_options):
    if hasattr(array, "with_queue"):
        backend = "opencl"
        transpose_cls = OpenCLTranspose
        backend_options["queue"] = array.queue  # !
    elif hasattr(array, "bind_to_texref"):
        backend = "cuda"
        transpose_cls = CudaTranspose
    else:
        raise ValueError("array should be either a cupy array or pyopencl.array.Array instance")

    dst_dtype = dst.dtype if dst is not None else None
    key = (backend, array.shape, np.dtype(array.dtype), dst_dtype)
    transpose_instance = _transposes_store.get(key, None)
    if transpose_instance is None:
        transpose_instance = transpose_cls(array.shape, array.dtype, dst_dtype=dst_dtype, **backend_options)
        _transposes_store[key] = transpose_instance

    return transpose_instance(array, dst=dst)
