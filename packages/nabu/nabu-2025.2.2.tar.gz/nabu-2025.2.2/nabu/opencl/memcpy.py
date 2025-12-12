import numpy as np
from ..utils import get_opencl_srcfile
from .kernel import OpenCLKernel
from .processing import OpenCLProcessing


class OpenCLMemcpy2D(OpenCLProcessing):
    """
    A class for performing rectangular memory copies between pyopencl arrays.
    It will only work for float32 arrays!
    It was written as pyopencl.enqueue_copy is too cumbersome to use for buffers.
    """

    def __init__(self, ctx=None, device_type="GPU", queue=None, **kwargs):
        super().__init__(ctx=ctx, device_type=device_type, queue=queue, **kwargs)
        self.memcpy2D = OpenCLKernel("cpy2d", self.queue, filename=get_opencl_srcfile("ElementOp.cl"))

    def __call__(self, dst, src, transfer_shape_xy, dst_offset_xy=None, src_offset_xy=None, wait=True):
        if dst_offset_xy is None:
            dst_offset_xy = (0, 0)
        if src_offset_xy is None:
            src_offset_xy = (0, 0)
        evt = self.memcpy2D(
            dst,
            src,
            np.int32(dst.shape[-1]),
            np.int32(src.shape[-1]),
            np.int32(dst_offset_xy),
            np.int32(src_offset_xy),
            np.int32(transfer_shape_xy),
            global_size=transfer_shape_xy,
        )
        if wait:
            evt.wait()
