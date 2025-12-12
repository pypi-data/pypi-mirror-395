# pylint: disable=too-many-arguments
import numpy as np
from ...utils import get_cuda_srcfile, updiv
from ...reconstruction.filtering import get_next_power
from ...reconstruction.filtering_cuda import CudaSinoFilter

# pylint: disable=too-many-arguments,too-many-instance-attributes,too-many-function-args


class HelicalSinoFilter(CudaSinoFilter):
    def __init__(
        self,
        sino_shape,
        filter_name=None,
        padding_mode="zeros",
        extra_options=None,
        cuda_options=None,
    ):
        """Derived from nabu.reconstruction.filtering.SinoFilter
        It is used by helical_chunked_regridded pipeline.
        The shape of the processed sino, as a matter of fact which is due to the helical_chunked_regridded.py module
        which is using the here present class, is always, but not necessarily [nangles, nslices, nhorizontal]
        with nslices = 1. This  because  helical_chunked_regridded.py after a first preprocessing phase,
        always processes slices one by one.
        In helical_chunked_regridded .py, the call to the filter_sino method here contained  is
        followed by  the weight redistribution ( done by another module), which solves the HA problem,
        and the backprojection. The latter is performed by fbp.py or hbp.py

        The reason for having this class, derived from nabu.reconstruction.filtering.SinoFilter,
        is that the padding mechanism here implemented incorporates the padding with the available
        theta+180 projection on the half-tomo side.

        """
        super().__init__(
            sino_shape,
            filter_name=filter_name,
            padding_mode=padding_mode,
            extra_options=extra_options,
            cuda_options=cuda_options,
        )

        self._init_pad_kernel()

    def _check_array(self, arr):
        """
        This class may work with an arbitrary number of projections. This is a consequence
        of the first implementation of the helical pipeline. In the first implementation
        the slices were reconstructed by backprojecting several turns, and the number of useful projections
        was different from the beginning or end, to the center of the scan.
        Now in helical_chunked_regridded.py the number of projections is fixed. The only relic left
        is that the present class may work with an arbitrary number of projections.
        """
        if arr.dtype != np.float32:
            raise ValueError("Expected data type = numpy.float32")
        if arr.shape[1:] != self.sino_shape[1:]:
            raise ValueError("Expected sinogram shape %s, got %s" % (self.sino_shape, arr.shape))

    def _init_pad_kernel(self):
        """The four possible padding kernels.
        The first two, compared to nabu.reconstruction.filtering.SinoFilter
        can work with an arbitrary number of projection.
        The latter two implement the padding with the available information from theta+180.
        """

        self.kern_args = (self.d_sino_f, self.d_filter_f)
        self.kern_args += self.d_sino_f.shape[::-1]
        self._pad_mirror_edges_kernel = self.cuda.kernel(
            "padding",
            filename=get_cuda_srcfile("helical_padding.cu"),
            signature="PPfiiiii",
            options=["-DMIRROR_EDGES"],
        )
        self._pad_mirror_constant_kernel = self.cuda.kernel(
            "padding",
            filename=get_cuda_srcfile("helical_padding.cu"),
            signature="PPfiiiiiff",
            options=["-DMIRROR_CONSTANT"],
        )

        self._pad_mirror_edges_variable_rot_pos_kernel = self.cuda.kernel(
            "padding",
            filename=get_cuda_srcfile("helical_padding.cu"),
            signature="PPPiiiii",
            options=["-DMIRROR_EDGES_VARIABLE_ROT_POS"],
        )
        self._pad_mirror_constant_variable_rot_pos_kernel = self.cuda.kernel(
            "padding",
            filename=get_cuda_srcfile("helical_padding.cu"),
            signature="PPPiiiiiff",
            options=["-DMIRROR_CONSTANT_VARIABLE_ROT_POS"],
        )

        self.d_mirror_indexes = self.cuda.allocate_array(
            "d_mirror_indexes", (self.sino_padded_shape[-2],), dtype=np.int32
        )
        self.d_variable_rot_pos = self.cuda.allocate_array(
            "d_variable_rot_pos", (self.sino_padded_shape[-2],), dtype=np.float32
        )
        self._pad_edges_kernel = self.cuda.kernel(
            "padding_edge", filename=get_cuda_srcfile("padding.cu"), signature="Piiiiiiii"
        )
        self._pad_block = (32, 32, 1)
        self._pad_grid = tuple([updiv(n, p) for n, p in zip(self.sino_padded_shape[::-1], self._pad_block)])

    def _pad_sino(self, sino, mirror_indexes=None, rot_center=None):
        """redefined here to adapt the memory copy to the length of the sino argument
        which, in the general helical case may be varying
        """
        if mirror_indexes is None:
            self._pad_sino_simple(sino)

        self.d_mirror_indexes[:] = np.zeros([len(self.d_mirror_indexes)], np.int32)
        self.d_mirror_indexes[: len(mirror_indexes)] = mirror_indexes.astype(np.int32)

        if np.isscalar(rot_center):
            argument_rot_center = rot_center
            tmp_pad_mirror_edges_kernel = self._pad_mirror_edges_kernel
            tmp_pad_mirror_constant_kernel = self._pad_mirror_constant_kernel
        else:
            self.d_variable_rot_pos[: len(rot_center)] = rot_center
            argument_rot_center = self.d_variable_rot_pos
            tmp_pad_mirror_edges_kernel = self._pad_mirror_edges_variable_rot_pos_kernel
            tmp_pad_mirror_constant_kernel = self._pad_mirror_constant_variable_rot_pos_kernel

        self.d_sino_padded[: len(sino), : self.dwidth] = sino[:]
        if self.padding_mode == "edges":
            tmp_pad_mirror_edges_kernel(
                self.d_sino_padded,
                self.d_mirror_indexes,
                argument_rot_center,
                self.dwidth,
                self.n_angles,
                self.dwidth_padded,
                self.pad_left,
                self.pad_right,
                grid=self._pad_grid,
                block=self._pad_block,
            )
        else:
            tmp_pad_mirror_constant_kernel(
                self.d_sino_padded,
                self.d_mirror_indexes,
                argument_rot_center,
                self.dwidth,
                self.n_angles,
                self.dwidth_padded,
                self.pad_left,
                self.pad_right,
                0.0,
                0.0,
                grid=self._pad_grid,
                block=self._pad_block,
            )

    def _pad_sino_simple(self, sino):
        if self.padding_mode == "edges":
            self.d_sino_padded[: len(sino), : self.dwidth] = sino[:]
            self._pad_edges_kernel(
                self.d_sino_padded,
                self.dwidth,
                self.n_angles,
                self.dwidth_padded,
                self.n_angles,
                self.pad_left,
                self.pad_right,
                0,
                0,
                grid=self._pad_grid,
                block=self._pad_block,
            )
        else:  # zeros
            self.d_sino_padded.fill(0)
            if self.ndim == 2:
                self.d_sino_padded[: len(sino), : self.dwidth] = sino[:]
            else:
                self.d_sino_padded[: len(sino), :, : self.dwidth] = sino[:]

    def filter_sino(self, sino, mirror_indexes=None, rot_center=None, output=None, no_output=False):
        """
        Perform the sinogram siltering.
        redefined here to use also mirror data

        Parameters
        ----------
        sino: numpy.ndarray or pycuda.gpuarray.GPUArray
            Input sinogram (2D or 3D)
        output: numpy.ndarray or pycuda.gpuarray.GPUArray, optional
            Output array.
        no_output: bool, optional
            If set to True, no copy is be done. The resulting data lies
            in self.d_sino_padded.
        """
        self._check_array(sino)
        # copy2d/copy3d
        self._pad_sino(sino, mirror_indexes=mirror_indexes, rot_center=rot_center)
        # FFT
        self.fft.fft(self.d_sino_padded, output=self.d_sino_f)

        # multiply padded sinogram with filter in the Fourier domain
        self.mult_kernel(*self.kern_args)  # TODO tune block size ?

        # iFFT
        self.fft.ifft(self.d_sino_f, output=self.d_sino_padded)

        # return
        if no_output:
            return self.d_sino_padded
        if output is None:
            res = np.zeros(self.sino_shape, dtype=np.float32)
            # can't do memcpy2d D->H ? (self.d_sino_padded[:, w]) I have to get()
            sino_ref = self.d_sino_padded.get()
        else:
            res = output
            sino_ref = self.d_sino_padded
        if self.ndim == 2:
            res[:] = sino_ref[:, : self.dwidth]
        else:
            res[:] = sino_ref[:, :, : self.dwidth]
        return res

    def _calculate_shapes(self, sino_shape):
        self.ndim = len(sino_shape)
        if self.ndim == 2:
            n_angles, dwidth = sino_shape
            n_sinos = 1
        elif self.ndim == 3:
            n_sinos, n_angles, dwidth = sino_shape
        else:
            raise ValueError("Invalid sinogram number of dimensions")
        self.sino_shape = sino_shape
        self.n_angles = n_angles
        self.dwidth = dwidth
        # int() is crucial here ! Otherwise some pycuda arguments (ex. memcpy2D)
        # will not work with numpy.int64 (as for 2018.X)

        ### the original get_next_power used in  nabu gives a lower ram footprint
        self.dwidth_padded = 2 * int(get_next_power(self.dwidth))

        self.sino_padded_shape = (n_angles, self.dwidth_padded)
        if self.ndim == 3:
            self.sino_padded_shape = (n_sinos,) + self.sino_padded_shape
        sino_f_shape = list(self.sino_padded_shape)
        sino_f_shape[-1] = sino_f_shape[-1] // 2 + 1
        self.sino_f_shape = tuple(sino_f_shape)
        #
        self.pad_left = (self.dwidth_padded - self.dwidth) // 2
        self.pad_right = self.dwidth_padded - self.dwidth - self.pad_left
