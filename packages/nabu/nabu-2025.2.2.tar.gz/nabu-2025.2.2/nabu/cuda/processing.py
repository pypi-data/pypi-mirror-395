from ..utils import MissingComponentError, deprecation_warning, warnings
from ..processing.processing_base import ProcessingBase
from .utils import __has_cupy__, dtype_to_ctype

if __has_cupy__:
    import cupy

    cuda = cupy.cuda
    cuarray = cupy.ndarray
    from ..cuda.kernel import CudaKernel
else:
    cuarray = MissingComponentError("cupy")
    dtype_to_ctype = MissingComponentError("cupy")


# NB: we must detach from a context before creating another context
class CudaProcessing(ProcessingBase):
    array_class = cuarray if __has_cupy__ else None
    dtype_to_ctype = dtype_to_ctype

    def __init__(self, device_id=None, ctx=None, stream=None, cleanup_at_exit=None):
        """
        Initialie a CudaProcessing instance.

        CudaProcessing is a base class for all CUDA-based processings.
        This class provides utilities for context/device management, and
        arrays allocation.

        Parameters
        ----------
        device_id: int, optional
            ID of the cuda device to use (those of the `nvidia-smi` command).
            Ignored if 'stream' is provided
        ctx: Unused parameter
            Deprecated, not used anymore.
        stream: cupy stream, optional
            Cuda stream. If not provided, will use the default stream
        cleanup_at_exit: bool, optional
            Deprecated, not used anymore
        """
        super().__init__()
        # COMPAT.
        if ctx is not None:
            deprecation_warning("Using 'ctx' kwarg is deprecated")
        if cleanup_at_exit is not None:
            deprecation_warning("Using 'cleanup_at_exit' kwarg is deprecated")
        #
        if stream is not None:
            stream.use()
        elif device_id is not None:
            cuda.Device(device_id).use()
        self.stream = stream  # TODO get default stream ?
        self.device_id = cuda.runtime.getDevice()
        self.device = cuda.Device(self.device_id)
        self.device_name = cuda.runtime.getDeviceProperties(self.device_id)["name"].decode()
        try:
            cuda.driver.ctxGetDevice()
        except cuda.driver.CUDADriverError:
            warnings.warn(f"No context found on cuda device {self.device_id}, creating one", RuntimeWarning)
            cuda.Device(self.device_id).use()

    def _allocate_array_mem(self, shape, dtype):
        return cupy.zeros(shape, dtype)

    def kernel(self, kernel_name, filename=None, src=None, automation_params=None, **build_kwargs):
        return CudaKernel(  # pylint: disable=E0606
            kernel_name,
            filename=filename,
            src=src,
            automation_params=automation_params,
            **build_kwargs,
        )
