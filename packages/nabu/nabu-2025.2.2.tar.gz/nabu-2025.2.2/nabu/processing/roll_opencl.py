#
# WIP !
#
# pylint: skip-file
import numpy as np
from ..opencl.utils import __has_pyopencl__
from ..utils import get_opencl_srcfile

if __has_pyopencl__:
    import pyopencl as cl
    from ..opencl.processing import OpenCLProcessing
    from ..opencl.kernel import OpenCLKernel
    from pyopencl.tools import dtype_to_ctype as cl_dtype_to_ctype


class OpenCLRoll:
    def __init__(self, dtype, direction=1, offset=None, **processing_kwargs):
        self.processing = OpenCLProcessing(queue=processing_kwargs.get("queue", None))
        self.dtype = np.dtype(dtype)
        compile_options = ["-DDTYPE=%s" % cl_dtype_to_ctype(self.dtype)]
        self.offset = offset or 0
        self.roll_kernel = OpenCLKernel(
            "roll_forward_x",
            self.processing.queue,
            filename=get_opencl_srcfile("roll.cl"),
            options=compile_options,
        )
        self.shmem = cl.LocalMemory(self.dtype.itemsize)
        self.direction = direction
        if self.direction < 0:
            self.revert_kernel = OpenCLKernel(
                "revert_array_x",
                self.processing.queue,
                filename=get_opencl_srcfile("roll.cl"),
                options=compile_options,
            )

    def __call__(self, arr):
        ny, nx = arr.shape
        # Launch one big horizontal workgroup
        wg_x = min((nx - self.offset) // 2, self.processing.queue.device.max_work_group_size)
        local_size = (wg_x, 1, 1)
        global_size = [wg_x, ny]
        if self.direction < 0:
            local_size2 = None
            global_size2 = [nx - self.offset, ny]
            self.revert_kernel(
                arr, np.int32(nx), np.int32(ny), np.int32(self.offset), local_size=local_size2, global_size=global_size2
            )
        self.roll_kernel(
            arr,
            np.int32(nx),
            np.int32(ny),
            np.int32(self.offset),
            self.shmem,
            local_size=local_size,
            global_size=global_size,
        )
        if self.direction < 0:
            self.revert_kernel(
                arr, np.int32(nx), np.int32(ny), np.int32(self.offset), local_size=local_size2, global_size=global_size2
            )
        return arr
