import numpy as np
from nabu.utils import get_cuda_srcfile, updiv
from .muladd import MulAdd
from ..cuda.utils import to_int2
from ..cuda.processing import CudaProcessing


class CudaMulAdd(MulAdd):
    processing_cls = CudaProcessing

    def _init_finalize(self):
        self._init_kernel()

    def _init_kernel(self):
        self.muladd_kernel = self.processing.kernel(
            "mul_add",
            filename=get_cuda_srcfile("ElementOp.cu"),
        )

    def mul_add(self, dst, other, fac_dst, fac_other, dst_region=None, other_region=None):
        """
        Performs
            dst[DST_IDX] = fac_dst*dst[DST_IDX] + fac_other*other[OTHER_IDX]
        where
            DST_IDX = dst_start_row:dst_end_row, dst_start_col:dst_end_col
            OTHER_IDX = other_start_row:other_end_row, other_start_col:other_end_col

        'region' should be a tuple (slice(y_start, y_end), slice(x_start, x_end))
        """

        if dst_region is None:
            dst_coords = (0, dst.shape[1], 0, dst.shape[0])
        else:
            dst_coords = (dst_region[1].start, dst_region[1].stop, dst_region[0].start, dst_region[0].stop)
        if other_region is None:
            other_coords = (0, other.shape[1], 0, other.shape[0])
        else:
            other_coords = (other_region[1].start, other_region[1].stop, other_region[0].start, other_region[0].stop)

        delta_x = np.diff(dst_coords[:2])
        delta_y = np.diff(dst_coords[2:])
        if delta_x != np.diff(other_coords[:2]) or delta_y != np.diff(other_coords[2:]):
            raise ValueError("Invalid dst_region and other_region provided. Regions must have the same size")
        if delta_x == 0 or delta_y == 0:
            raise ValueError("delta_x or delta_y is 0")

        dst_x_range = to_int2(dst_coords[:2])
        dst_y_range = to_int2(dst_coords[2:])
        other_x_range = to_int2(other_coords[:2])
        other_y_range = to_int2(other_coords[2:])

        block = (32, 32, 1)
        grid = [updiv(length, b) for (length, b) in zip((delta_x[0], delta_y[0]), block)]

        self.muladd_kernel(
            dst,
            other,
            np.int32(dst.shape[1]),
            np.int32(other.shape[1]),
            np.float32(fac_dst),
            np.float32(fac_other),
            dst_x_range,
            dst_y_range,
            other_x_range,
            other_y_range,
            grid=grid,
            block=block,
        )

    __call__ = mul_add
