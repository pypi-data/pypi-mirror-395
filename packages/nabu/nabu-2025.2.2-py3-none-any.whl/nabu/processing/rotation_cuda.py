import numpy as np
from .rotation import Rotation
from ..utils import get_cuda_srcfile, updiv
from ..cuda.utils import create_texture
from ..cuda.processing import CudaProcessing


class CudaRotation(Rotation):
    def __init__(self, shape, angle, center=None, mode="edge", reshape=False, cuda_options=None, **sk_kwargs):
        if center is None:
            center = ((shape[1] - 1) / 2.0, (shape[0] - 1) / 2.0)
        super().__init__(shape, angle, center=center, mode=mode, reshape=reshape, **sk_kwargs)
        self._init_cuda_rotation(cuda_options)

    def _init_cuda_rotation(self, cuda_options):
        cuda_options = cuda_options or {}
        self.cuda_processing = CudaProcessing(**cuda_options)
        self._allocate_arrays()
        self._init_rotation_kernel()

    def _allocate_arrays(self):
        self.cuda_processing.init_arrays_to_none(["d_output"])

    def _get_textures(self):
        self.tex_image, self.tex_image_cua = create_texture(self.shape, "f", address_mode="clamp", filter_mode="linear")

    def _init_rotation_kernel(self):
        self._get_textures()
        self.cuda_rotation_kernel = self.cuda_processing.kernel(
            "rotate", filename=get_cuda_srcfile("rotation.cu")
        )  # pylint: disable=E0606
        self._cos_theta = np.float32(np.cos(np.deg2rad(self.angle)))
        self._sin_theta = np.float32(np.sin(np.deg2rad(self.angle)))
        self._Nx = np.int32(self.shape[1])
        self._Ny = np.int32(self.shape[0])
        self._center_x = np.float32(self.center[0])
        self._center_y = np.float32(self.center[1])
        self._block = (32, 32, 1)  # tune ?
        self._grid = (updiv(self.shape[1], self._block[1]), updiv(self.shape[0], self._block[0]), 1)

    def rotate(self, img, output=None, do_checks=True):
        self.tex_image_cua.copy_from(img)
        if output is not None:
            d_out = output
        else:
            self.cuda_processing.allocate_array("d_output", self.shape, np.float32)
            d_out = self.cuda_processing.d_output
        self.cuda_rotation_kernel(
            self.tex_image.ptr,
            d_out,
            self._Nx,
            self._Ny,
            self._cos_theta,
            self._sin_theta,
            self._center_x,
            self._center_y,
            grid=self._grid,
            block=self._block,
        )
        return d_out

    __call__ = rotate
