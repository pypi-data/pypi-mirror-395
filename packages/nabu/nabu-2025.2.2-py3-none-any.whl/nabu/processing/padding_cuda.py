import numpy as np
from ..utils import get_cuda_srcfile, updiv
from ..cuda.processing import CudaProcessing
from .padding_base import PaddingBase


class CudaPadding(PaddingBase):
    """
    A class for performing padding on GPU using Cuda
    """

    backend = "cuda"

    def __init__(self, shape, pad_width, mode="constant", cuda_options=None, **kwargs):
        super().__init__(shape, pad_width, mode=mode, **kwargs)
        self.cuda_processing = self.processing = CudaProcessing(**(cuda_options or {}))
        self._init_cuda_coordinate_transform()

    def _init_cuda_coordinate_transform(self):
        if self.mode == "constant":
            self.d_padded_array_constant = self.processing.to_device(
                "d_padded_array_constant", self.padded_array_constant
            )
            return
        self._coords_transform_kernel = self.processing.kernel(
            "coordinate_transform",
            filename=get_cuda_srcfile("padding.cu"),
        )
        self._coords_transform_block = (32, 32, 1)
        self._coords_transform_grid = [
            updiv(a, b) for a, b in zip(self.padded_shape[::-1], self._coords_transform_block)
        ]
        self.d_coords_rows = self.processing.to_device("d_coords_rows", self.coords_rows)
        self.d_coords_cols = self.processing.to_device("d_coords_cols", self.coords_cols)

    def _pad_constant(self, image, output):
        pad_y, pad_x = self.pad_width
        self.d_padded_array_constant[pad_y[0] : pad_y[0] + self.shape[0], pad_x[0] : pad_x[0] + self.shape[1]] = image[
            :
        ]
        output[:] = self.d_padded_array_constant[:]
        return output

    def pad(self, image, output=None):
        """
        Pad an array.

        Parameters
        ----------
        image: cupy array
            Image to pad
        output: cupy array, optional
            Output image. If provided, must be in the expected shape.
        """
        if output is None:
            output = self.processing.allocate_array("d_output", self.padded_shape)
        if self.mode == "constant":
            return self._pad_constant(image, output)
        self._coords_transform_kernel(
            image,
            output,
            self.d_coords_cols,
            self.d_coords_rows,
            np.int32(self.shape[1]),
            np.int32(self.padded_shape[1]),
            np.int32(self.padded_shape[0]),
            grid=self._coords_transform_grid,
            block=self._coords_transform_block,
        )
        return output

    __call__ = pad
