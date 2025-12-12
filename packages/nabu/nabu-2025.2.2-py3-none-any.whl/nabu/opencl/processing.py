from ..processing.processing_base import ProcessingBase
from ..utils import MissingComponentError
from .utils import get_opencl_context, __has_pyopencl__

if __has_pyopencl__:
    from .kernel import OpenCLKernel
    import pyopencl as cl
    import pyopencl.array as parray
    from pyopencl.tools import dtype_to_ctype

    OpenCLArray = parray.Array
else:
    OpenCLArray = MissingComponentError("pyopencl")
    dtype_to_ctype = MissingComponentError("pyopencl")


# pylint: disable=E0606
class OpenCLProcessing(ProcessingBase):
    array_class = OpenCLArray
    dtype_to_ctype = dtype_to_ctype

    def __init__(self, ctx=None, device_type="all", queue=None, profile=False, **kwargs):
        """
        Initialie a OpenCLProcessing instance.

        Parameters
        ----------
        ctx: pyopencl context, optional
            Existing context to use. If provided, do not create a new context.
        cleanup_at_exit: bool, optional
            Whether to clean-up the context at exit.
            Ignored if ctx is not None.
        """
        super().__init__()
        if queue is not None:
            # re-use an existing queue. In this case the this instance is mostly for convenience
            ctx = queue.context
        if ctx is None:
            self.ctx = get_opencl_context(device_type=device_type, **kwargs)
        else:
            self.ctx = ctx
        if queue is None:
            queue_init_kwargs = {}
            if profile:
                queue_init_kwargs = {"properties": cl.command_queue_properties.PROFILING_ENABLE}
            queue = cl.CommandQueue(self.ctx, **queue_init_kwargs)
        self.queue = queue
        dev_types = {
            cl.device_type.CPU: "cpu",
            cl.device_type.GPU: "gpu",
            cl.device_type.ACCELERATOR: "accelerator",
            -1: "unknown",
        }
        self.device_type = dev_types.get(self.ctx.devices[0].type, "unknown")

    # TODO push_context, pop_context ?

    def _allocate_array_mem(self, shape, dtype):
        return parray.zeros(self.queue, shape, dtype)

    def kernel(self, kernel_name, filename=None, src=None, automation_params=None, **build_kwargs):
        return OpenCLKernel(
            kernel_name,
            self.queue,
            filename=filename,
            src=src,
            automation_params=automation_params,
            **build_kwargs,
        )
