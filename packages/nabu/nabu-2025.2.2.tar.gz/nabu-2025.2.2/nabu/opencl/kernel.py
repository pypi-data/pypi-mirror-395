import pyopencl.array as parray
from pyopencl import Program, kernel_work_group_info
from ..utils import (
    deprecation_warning,
    catch_warnings,
)  # TODO use warnings.catch_warnings once python < 3.11 is dropped
from ..processing.kernel_base import KernelBase


class OpenCLKernel(KernelBase):
    """
    Helper class that wraps OpenCL kernel through pyopencl.

    Parameters
    -----------
    kernel_name: str
        Name of the OpenCL kernel.
    queue: pyopencl.CommandQueue
        OpenCL queue to use.
    filename: str, optional
        Path to the file name containing kernels definitions
    src: str, optional
        Source code of kernels definitions
    automation_params: dict, optional
        Automation parameters, see below
    build_kwargs: optional
        Extra arguments to provide to pyopencl.Program.build(),
    """

    def __init__(
        self,
        kernel_name,
        queue,
        filename=None,
        src=None,
        automation_params=None,
        silent_compilation_warnings=False,
        **build_kwargs,
    ):
        super().__init__(
            kernel_name,
            filename=filename,
            src=src,
            automation_params=automation_params,
            silent_compilation_warnings=silent_compilation_warnings,
        )

        self.ctx = queue.context
        self.queue = queue
        self.compile_kernel_source(kernel_name, build_kwargs)
        self.get_kernel()

    def compile_kernel_source(self, kernel_name, build_kwargs):
        self.build_kwargs = build_kwargs
        self.kernel_name = kernel_name
        with catch_warnings(action=("ignore" if self.silent_compilation_warnings else None)):  # pylint: disable=E1123
            self.program = Program(self.ctx, self.src).build(**self.build_kwargs)

    def get_kernel(self):
        self.kernel = None
        for kern in self.program.all_kernels():
            if kern.function_name == self.kernel_name:
                self.kernel = kern
        if self.kernel is None:
            raise ValueError(
                "Could not find a kernel with function name '%s'. Available are: %s"
                % (self.kernel_name, self.program.kernel_names)
            )

    # overwrite parent method
    def guess_block_size(self, shape):
        device = self.ctx.devices[0]
        wg_max = device.max_work_group_size
        wg_multiple = self.kernel.get_work_group_info(kernel_work_group_info.PREFERRED_WORK_GROUP_SIZE_MULTIPLE, device)
        ndim = len(shape)
        # Try to have workgroup relatively well-balanced in all dimensions,
        # with more work items in x > y > z
        if ndim == 1:
            wg = (wg_max, 1, 1)
        else:
            w = (wg_max // wg_multiple, wg_multiple)
            wg = w if w[0] > w[1] else w[::-1]
            wg = wg + (1,)
            if ndim == 3:
                (wg[0] // 2, wg[1] // 4, 8)
        return wg

    def get_block_grid(self, *args, **kwargs):
        local_size = None
        global_size = block = None
        # COMPAT.
        block = kwargs.pop("block", None)
        if block is not None:
            deprecation_warning("Please use 'local_size' instead of 'block'")
        grid = kwargs.pop("grid", None)
        if grid is not None:
            deprecation_warning("Please use 'global_size' instead of 'grid'")
            global_size = tuple(g * b for g, b in zip(grid, block))
        #

        global_size = kwargs.pop("global_size", global_size)
        local_size = kwargs.pop("local_size", block)

        if global_size is None:
            raise ValueError("Need to define global_size for kernel '%s'" % self.kernel_name)

        if len(global_size) == 2 and local_size is not None and len(local_size) == 3:
            local_size = local_size[:-1]  # TODO check that last dim is 1

        self.last_block_size = local_size
        self.last_grid_size = global_size
        return local_size, global_size

    def follow_device_arr(self, args):
        args = list(args)
        for i, arg in enumerate(args):
            if isinstance(arg, parray.Array):
                args[i] = arg.data
        return tuple(args)

    def call(self, *args, **kwargs):
        global_size, local_size, args, kwargs = self._prepare_call(*args, **kwargs)

        kwargs.pop("global_size", None)
        kwargs.pop("local_size", None)
        kwargs.pop("grid", None)
        kwargs.pop("block", None)

        return self.kernel(self.queue, global_size, local_size, *args, **kwargs)

    __call__ = call
