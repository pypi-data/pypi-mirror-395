from .processing_base import ProcessingBase


class MulAdd:
    processing_cls = ProcessingBase

    def __init__(self, **backend_options):
        self.processing = self.processing_cls(**(backend_options or {}))
        self._init_finalize()

    def _init_finalize(self):
        pass

    def mul_add(self, dst, other, fac_dst, fac_other, dst_region=None, other_region=None):
        if dst_region is None:
            dst_slice_y = dst_slice_x = slice(None, None)
        else:
            dst_slice_y, dst_slice_x = dst_region
        if other_region is None:
            other_slice_y = other_slice_x = slice(None, None)
        else:
            other_slice_y, other_slice_x = other_region

        dst[dst_slice_y, dst_slice_x] = (
            fac_dst * dst[dst_slice_y, dst_slice_x] + fac_other * other[other_slice_y, other_slice_x]
        )

    __call__ = mul_add
