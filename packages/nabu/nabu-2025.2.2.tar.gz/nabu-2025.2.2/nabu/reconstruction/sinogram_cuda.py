import numpy as np
from ..utils import get_cuda_srcfile, updiv, deprecated_class
from .sinogram import SinoBuilder, SinoNormalization, SinoMult
from .sinogram import _convert_halftomo_right  # FIXME Temporary patch
from ..cuda.processing import CudaProcessing


class CudaSinoBuilder(SinoBuilder):
    def __init__(
        self, sinos_shape=None, radios_shape=None, rot_center=None, halftomo=False, angles=None, cuda_options=None
    ):
        """
        Initialize a CudaSinoBuilder instance.
        Please see the documentation of nabu.reconstruction.sinogram.Builder
        and nabu.cuda.processing.CudaProcessing.
        """
        super().__init__(
            sinos_shape=sinos_shape, radios_shape=radios_shape, rot_center=rot_center, halftomo=halftomo, angles=angles
        )
        self.cuda_processing = CudaProcessing(**(cuda_options or {}))
        self._init_cuda_halftomo()

    def _init_cuda_halftomo(self):
        if not (self.halftomo):
            return
        kernel_name = "halftomo_kernel"
        self.halftomo_kernel = self.cuda_processing.kernel(
            kernel_name,
            get_cuda_srcfile("halftomo.cu"),
        )
        blk = (32, 32, 1)  # tune ?
        self._halftomo_blksize = blk
        self._halftomo_gridsize = (updiv(self.extended_sino_width, blk[0]), updiv((self.n_angles + 1) // 2, blk[1]), 1)
        d = self.n_x - self.extended_sino_width // 2  # will have to be adapted for varying axis pos
        self.halftomo_weights = np.linspace(0, 1, 2 * abs(d), endpoint=True, dtype="f")
        self.d_halftomo_weights = self.cuda_processing.to_device("d_halftomo_weights", self.halftomo_weights)
        # Allocate one single sinogram (kernel needs c-contiguous array).
        # If odd number of angles: repeat last angle.
        self.d_sino = self.cuda_processing.allocate_array(
            "d_sino", (self.n_angles + (self.n_angles & 1), self.n_x), "f"
        )
        self.h_sino = self.d_sino.get()
        #
        self.cuda_processing.init_arrays_to_none(["d_output"])
        if self._halftomo_flip:
            self.xflip_kernel = self.cuda_processing.kernel(
                "reverse2D_x",
                get_cuda_srcfile("ElementOp.cu"),
            )
            blk = (32, 32, 1)
            self._xflip_blksize = blk
            self._xflip_gridsize_1 = (updiv(self.n_x, blk[0]), updiv(self.n_angles, blk[1]), 1)
            self._xflip_gridsize_2 = self._halftomo_gridsize

    #
    # 2D
    #

    def _get_sino_halftomo(self, sino, output=None):
        if output is None:
            output = self.cuda_processing.allocate_array("d_output", self.output_shape[1:])
        elif output.shape != self.output_shape[1:]:
            raise ValueError("Expected output to have shape %s but got %s" % (self.output_shape[1:], output.shape))

        d_sino = self.d_sino
        n_a, n_x = sino.shape
        d_sino[:n_a] = sino[:]
        if self.n_angles & 1:
            d_sino[-1, :].fill(0)
        if self._halftomo_flip:
            self.xflip_kernel(d_sino, n_x, n_a, grid=self._xflip_gridsize_1, block=self._xflip_blksize)
        # Sometimes CoR is set well outside the FoV. Not supported by cuda backend for now.
        # TODO/FIXME: TEMPORARY PATCH, waiting for cuda implementation
        if self.rot_center > self.n_x:
            d_sino.get(self.h_sino)  # copy D2H
            res = _convert_halftomo_right(self.h_sino, self.extended_sino_width)
            output.set(res)  # copy H2D
        #
        else:
            self.halftomo_kernel(
                d_sino,
                output,
                self.d_halftomo_weights,
                n_a,
                n_x,
                self.extended_sino_width // 2,
                grid=self._halftomo_gridsize,
                block=self._halftomo_blksize,
            )
        if self._halftomo_flip:
            self.xflip_kernel(
                output, self.extended_sino_width, (n_a + 1) // 2, grid=self._xflip_gridsize_2, block=self._xflip_blksize
            )
        return output

    #
    # 3D
    #

    def _get_sinos_simple(self, radios, output=None):
        if output is None:
            return radios.transpose(axes=(1, 0, 2))  # view
        else:
            # why can't I do a discontig single copy ?
            for i in range(radios.shape[1]):
                output[i] = radios[:, i, :]
            return output

    def _get_sinos_halftomo(self, radios, output=None):
        if output is None:
            output = self.cuda_processing.allocate_array("output", self.output_shape, "f")
        elif output.shape != self.output_shape:
            raise ValueError("Expected output to have shape %s but got %s" % (self.output_shape, output.shape))
        for i in range(self.n_z):
            sino = self._get_sino_simple(radios, i)
            self._get_sino_halftomo(sino, output=output[i])
        return output


CudaSinoProcessing = deprecated_class("'CudaSinoProcessing' was renamed 'CudaSinoBuilder'", do_print=True)(
    CudaSinoBuilder
)


class CudaSinoMult(SinoMult):
    def __init__(self, sino_shape, rot_center, **cuda_options):
        super().__init__(sino_shape, rot_center)
        self.cuda_processing = CudaProcessing(**cuda_options)
        self._init_kernel()

    def _init_kernel(self):
        self.halftomo_kernel = self.cuda_processing.kernel(
            "halftomo_prepare_sinogram",
            filename=get_cuda_srcfile("halftomo.cu"),
        )
        self.d_weights = self.cuda_processing.set_array("d_weights", self.weights)
        self._halftomo_kernel_other_args = [
            self.d_weights,
            np.int32(self.n_a),
            np.int32(self.n_x),
            np.int32(self.start_x),
            np.int32(self.end_x),
        ]
        self._grid = (self.n_x, self.n_a)
        self._blk = (32, 32, 1)  # tune ?

    def prepare_sino(self, sino):
        sino = self.cuda_processing.set_array("d_sino", sino)
        self.halftomo_kernel(sino, *self._halftomo_kernel_other_args, grid=self._grid, block=self._blk)
        return sino


class CudaSinoNormalization(SinoNormalization):
    def __init__(
        self, kind="chebyshev", sinos_shape=None, radios_shape=None, normalization_array=None, cuda_options=None
    ):
        super().__init__(
            kind=kind, sinos_shape=sinos_shape, radios_shape=radios_shape, normalization_array=normalization_array
        )
        self._get_shapes(sinos_shape, radios_shape)
        self.cuda_processing = CudaProcessing(**(cuda_options or {}))
        self._init_cuda_normalization()

    _get_shapes = SinoBuilder._get_shapes

    #
    # Chebyshev normalization
    #

    def _init_cuda_normalization(self):
        self._d_tmp = self.cuda_processing.allocate_array("_d_tmp", self.sinos_shape[-2:], "f")
        if self.normalization_kind == "chebyshev":
            self._chebyshev_kernel = self.cuda_processing.kernel(
                "normalize_chebyshev",
                filename=get_cuda_srcfile("normalization.cu"),
            )
            self._chebyshev_kernel_args = [np.int32(self.n_x), np.int32(self.n_angles), np.int32(self.n_z)]
            blk = (1, 64, 16)  # TODO tune ?
            self._chebyshev_kernel_kwargs = {
                "block": blk,
                "grid": (1, int(updiv(self.n_angles, blk[1])), int(updiv(self.n_z, blk[2]))),
            }
        elif self.normalization_array is not None:
            normalization_array = self.normalization_array
            # If normalization_array is 1D, make a 2D array by repeating the line
            if normalization_array.ndim == 1:
                normalization_array = np.tile(normalization_array, (self.n_angles, 1))
            self._d_normalization_array = self.cuda_processing.to_device(
                "_d_normalization_array", normalization_array.astype("f")
            )
            # pylint: disable=E0606
            if self.normalization_kind == "subtraction":
                generic_op_val = 1
            elif self.normalization_kind == "division":
                generic_op_val = 3
            self._norm_kernel = self.cuda_processing.kernel(
                "inplace_generic_op_2Dby2D",
                filename=get_cuda_srcfile("ElementOp.cu"),
                options=("-DGENERIC_OP=%d" % generic_op_val,),
            )
            self._norm_kernel_args = [self._d_normalization_array, np.int32(self.n_angles), np.int32(self.n_x)]
            blk = (32, 32, 1)
            self._norm_kernel_kwargs = {
                "block": blk,
                "grid": (int(updiv(self.n_angles, blk[0])), int(updiv(self.n_x, blk[1])), 1),
            }

    def _normalize_chebyshev(self, sinos):
        if sinos.flags.c_contiguous:
            self._chebyshev_kernel(sinos, *self._chebyshev_kernel_args, **self._chebyshev_kernel_kwargs)
        else:
            # This kernel seems to have an issue on arrays that are not C-contiguous.
            # We have to process image per image.
            nthreadsperblock = (1, 32, 1)  # TODO tune
            nblocks = (1, int(updiv(self.n_angles, nthreadsperblock[1])), 1)
            for i in range(sinos.shape[0]):
                self._d_tmp[:] = sinos[i][:]
                self._chebyshev_kernel(
                    self._d_tmp,
                    np.int32(self.n_x),
                    np.int32(self.n_angles),
                    np.int32(1),
                    grid=nblocks,
                    block=nthreadsperblock,
                )
                sinos[i][:] = self._d_tmp[:]
        return sinos

    #
    # Array subtraction/division
    #

    def _normalize_op(self, sino):
        if sino.ndim == 2:
            # Things can go wrong if "sino" is a non-contiguous 2D array
            # But this should be handled outside this function, as the processing is in-place
            self._norm_kernel(sino, *self._norm_kernel_args, **self._norm_kernel_kwargs)
        else:
            if sino.flags.forc:
                # Contiguous 3D array. But pycuda wants the same shape for both operands.
                for i in range(sino.shape[0]):
                    self._norm_kernel(sino[i], *self._norm_kernel_args, **self._norm_kernel_kwargs)
            else:
                # Non-contiguous 2D array. Make a temp. copy
                for i in range(sino.shape[0]):
                    self._d_tmp[:] = sino[i][:]
                    self._norm_kernel(self._d_tmp, *self._norm_kernel_args, **self._norm_kernel_kwargs)
                    sino[i][:] = self._d_tmp[:]
        return sino
