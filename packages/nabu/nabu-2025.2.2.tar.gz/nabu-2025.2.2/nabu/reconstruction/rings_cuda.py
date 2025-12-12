import numpy as np

from ..utils import docstring, get_cuda_srcfile, updiv
from ..cuda.processing import CudaProcessing, __has_cupy__
from ..cuda.utils import cupy_array_from_ptr
from ..processing.padding_cuda import CudaPadding
from ..processing.fft_cuda import get_fft_class, get_available_fft_implems
from ..processing.transpose import CudaTranspose
from .rings import MunchDeringer, SinoMeanDeringer, VoDeringer

if __has_cupy__:
    from ..cuda.kernel import CudaKernel

try:
    from pycudwt import Wavelets

    __have_pycudwt__ = True
except ImportError:
    __have_pycudwt__ = False

# pylint: disable=E0606


class CudaMunchDeringer(MunchDeringer):
    def __init__(
        self,
        sigma,
        sinos_shape,
        levels=None,
        wname="db15",
        padding=None,
        padding_mode="edge",
        fft_backend="vkfft",
        cuda_options=None,
    ):
        """
        Initialize a "Munch Et Al" sinogram deringer with the Cuda backend.
        See References for more information.

        Parameters
        -----------
        sigma: float
            Standard deviation of the damping parameter. The higher value of sigma,
            the more important the filtering effect on the rings.
        levels: int, optional
            Number of wavelets decomposition levels.
            By default (None), the maximum number of decomposition levels is used.
        wname: str, optional
            Default is "db15" (Daubechies, 15 vanishing moments)
        sinos_shape: tuple, optional
            Shape of the sinogram (or sinograms stack).

        References
        ----------
        B. Munch, P. Trtik, F. Marone, M. Stampanoni, Stripe and ring artifact removal with
        combined wavelet-Fourier filtering, Optics Express 17(10):8567-8591, 2009.
        """
        super().__init__(sigma, sinos_shape, levels=levels, wname=wname, padding=padding, padding_mode=padding_mode)
        self._check_can_use_wavelets()
        self.cuda_processing = CudaProcessing(**(cuda_options or {}))
        # self.ctx = self.cuda_processing.ctx
        self._init_pycudwt()
        self._init_padding()
        self._init_fft(fft_backend)
        self._setup_fw_kernel()

    def _check_can_use_wavelets(self):
        if not (__have_pycudwt__ and __has_cupy__):
            raise ValueError("Needs cupy and pycudwt to use this class")

    def _init_padding(self):
        if self.padding is None:
            return
        self.padder = CudaPadding(
            self.sinos_shape[1:],
            ((0, 0), self.padding),
            mode=self.padding_mode,
            # cuda_options={"ctx": self.cuda_processing.ctx},
        )

    def _init_fft(self, fft_backend):
        self.fft_cls = get_fft_class(backend=fft_backend)
        # For all k >= 1, we perform a batched (I)FFT along axis 0 on an array
        # of shape (n_a/2^k, n_x/2^k)  (up to DWT size rounding)
        if self.fft_cls.implem == "vkfft":
            self._create_plans_vkfft()
        else:
            self._create_plans_skfft()

    def _create_plans_skfft(self):
        self._fft_plans = {}
        for level, d_vcoeff in self._d_vertical_coeffs.items():
            self._fft_plans[level] = self.fft_cls(d_vcoeff.shape, np.float32, r2c=True, axes=(0,), ctx=self.ctx)

    def _create_plans_vkfft(self):
        """
        VKFFT does not support batched R2C transforms along axis 0 ("slow axis").
        We can either use C2C (faster, but needs more memory) or transpose the arrays to do R2C along axis=1.
        Here we transpose the arrays.
        """
        self._fft_plans = {}
        self._transpose_forward_1 = {}
        self._transpose_forward_2 = {}
        self._transpose_inverse_1 = {}
        self._transpose_inverse_2 = {}
        for level, d_vcoeff in self._d_vertical_coeffs.items():
            shape = d_vcoeff.shape
            # Normally, a batched 1D fft on 2D data of shape (Ny, Nx) along axis 0 returns an array of shape (Ny/2+1, Nx):
            #
            #  (Ny, Nx)  --[fft_0]--> (Ny/2, Nx)
            #    f32                      c64
            #
            # In this case, we can only do batched 1D transform along axis 1, so we have to trick with transposes:
            #
            #  (Ny, Nx) --[T]--> (Nx, Ny) --[fft_1]--> (Nx, Ny/2) --[T]--> (Ny/2, Nx)
            #    f32                f32                   c64                  c64
            #
            # (In both cases IFFT is done the same way from right to left)
            self._transpose_forward_1[level] = CudaTranspose(shape, np.float32)  # , ctx=self.ctx)
            self._fft_plans[level] = self.fft_cls(shape[::-1], np.float32, r2c=True, axes=(1,))  # , ctx=self.ctx)
            self._transpose_forward_2[level] = CudaTranspose(
                (shape[1], shape[0] // 2 + 1), np.complex64
            )  # , ctx=self.ctx)
            self._transpose_inverse_1[level] = CudaTranspose(
                (shape[0] // 2 + 1, shape[1]), np.complex64
            )  # , ctx=self.ctx)
            self._transpose_inverse_2[level] = CudaTranspose(shape[::-1], np.float32)  # , ctx=self.ctx)

    def _init_pycudwt(self):
        if self.levels is None:
            self.levels = 100  # will be clipped by pycudwt
        sino_shape = self.sinos_shape[1:] if self.padding is None else self.sino_padded_shape
        self.cudwt = Wavelets(np.zeros(sino_shape, "f"), self.wname, self.levels)
        self.levels = self.cudwt.levels
        # Access memory allocated by "pypwt" from cupy
        self._d_sino = cupy_array_from_ptr(self.cudwt.image_int_ptr(), sino_shape, np.float32, self.cudwt)
        self._get_vertical_coeffs()

    def _get_vertical_coeffs(self):
        self._d_vertical_coeffs = {}
        # Transfer the (0-memset) coefficients in order to get all the shapes
        coeffs = self.cudwt.coeffs
        for i in range(self.cudwt.levels):
            shape = coeffs[i + 1][1].shape
            self._d_vertical_coeffs[i + 1] = cupy_array_from_ptr(
                self.cudwt.coeff_int_ptr(3 * i + 2), shape, np.float32, self.cudwt
            )

    def _setup_fw_kernel(self):
        self._fw_kernel = CudaKernel(
            "kern_fourierwavelets",
            filename=get_cuda_srcfile("fourier_wavelets.cu"),
        )
        self._fw_kernel_block = (32, 32)

    def _apply_fft(self, level):
        d_coeffs = self._d_vertical_coeffs[level]
        # All the memory is allocated (or re-used) under the hood
        if self.fft_cls.implem == "vkfft":
            d_coeffs_t = self._transpose_forward_1[level](
                d_coeffs
            )  # allocates self._transpose_forward_1[level].processing.dst
            d_coeffs_t_f = self._fft_plans[level].fft(d_coeffs_t)  # allocates self._fft_plans[level].output_fft
            d_coeffs_f = self._transpose_forward_2[level](
                d_coeffs_t_f
            )  # allocates self._transpose_forward_2[level].processing.dst
        else:
            d_coeffs_f = self._fft_plans[level].fft(d_coeffs)
        return d_coeffs_f

    def _apply_ifft(self, d_coeffs_f, level):
        d_coeffs = self._d_vertical_coeffs[level]
        if self.fft_cls.implem == "vkfft":
            d_coeffs_t_f = self._transpose_inverse_1[level](d_coeffs_f, dst=self._fft_plans[level].output_fft)
            d_coeffs_t = self._fft_plans[level].ifft(
                d_coeffs_t_f, output=self._transpose_forward_1[level].processing.dst
            )
            self._transpose_inverse_2[level](d_coeffs_t, dst=d_coeffs)
        else:
            self._fft_plans[level].ifft(d_coeffs_f, output=d_coeffs)

    def _destripe_2D(self, d_sino, output):
        if not (d_sino.flags.c_contiguous):
            sino = self.cuda_processing.allocate_array("_d_sino", d_sino.shape, np.float32)
            sino[:] = d_sino[:]
        else:
            sino = d_sino
        if self.padding is not None:
            sino = self.padder.pad(sino)
        # set the "image" for DWT (memcpy D2D)
        self._d_sino[:] = sino[:]
        # perform forward DWT
        self.cudwt.forward()

        for i in range(self.cudwt.levels):
            level = i + 1
            # Batched FFT along axis 0
            d_vertical_coeffs_f = self._apply_fft(level)
            Ny, Nx = d_vertical_coeffs_f.shape

            # Dampen the wavelets coefficients
            grid_size = tuple([updiv(a, b) for a, b in zip((Nx, Ny), self._fw_kernel_block)])
            self._fw_kernel(
                d_vertical_coeffs_f,
                np.int32(Nx),
                np.int32(Ny),
                np.float32(self.sigma),
                grid=grid_size,
                block=self._fw_kernel_block,
            )
            # IFFT
            self._apply_ifft(d_vertical_coeffs_f, level)

        # Finally, inverse DWT
        self.cudwt.inverse()
        d_out = self._d_sino
        if self.padding is not None:
            d_out = self._d_sino[:, self.padding[0] : -self.padding[1]]  # memcpy2D
        output[:] = d_out[:]
        return output


def can_use_cuda_deringer():
    """
    Check whether the CUDA implementation of deringer can be used.
    Checking for installed modules is not enough, as for example pyvkfft can be installed without CUDA devices
    """
    can_do_fft = get_available_fft_implems() != []
    return can_do_fft and __have_pycudwt__


class CudaVoDeringer(VoDeringer):
    """
    An interface to topocupy's "remove_all_stripe".
    """

    def _init_lib(self):
        # Do it here, otherwise cupy shows warnings at import even if not used
        from ..thirdparty.tomocupy_remove_stripe import remove_all_stripe_pycuda, __have_tomocupy_deringer__

        if not (__have_tomocupy_deringer__):
            raise ImportError("need cupy")
        self._remove_all_stripe_pycuda = remove_all_stripe_pycuda

    def remove_rings_radios(self, radios):
        return self._remove_all_stripe_pycuda(radios, layout="radios", **self._remove_all_stripe_kwargs)

    def remove_rings_sinograms(self, sinos):
        return self._remove_all_stripe_pycuda(sinos, layout="sinos", **self._remove_all_stripe_kwargs)

    def remove_rings_sinogram(self, sino):
        sinos = sino.reshape((1, sino.shape[0], -1))  # no copy
        self.remove_rings_sinograms(sinos)
        return sino

    remove_rings = remove_rings_sinograms


class CudaSinoMeanDeringer(SinoMeanDeringer):
    @docstring(SinoMeanDeringer)
    def __init__(
        self,
        sinos_shape,
        mode="subtract",
        filter_cutoff=None,
        padding_mode="edge",
        fft_num_threads=None,
        **cuda_options,
    ):
        self.processing = CudaProcessing(**(cuda_options or {}))
        super().__init__(sinos_shape, mode, filter_cutoff, padding_mode, fft_num_threads)
        self._init_kernels()

    def _init_kernels(self):
        self.d_sino_profile = self.processing.allocate_array("sino_profile", self.n_x)
        self._mean_kernel = self.processing.kernel(
            "vertical_mean",
            filename=get_cuda_srcfile("normalization.cu"),
        )
        self._set_kernel_args_normalization()

        self._op_kernel = self.processing.kernel(
            "inplace_generic_op_3Dby1D",
            filename=get_cuda_srcfile("ElementOp.cu"),
            options=("-DGENERIC_OP=%d" % (3 if self.mode == "divide" else 1),),
        )
        self._set_kernel_args_mult()

    def _set_kernel_args_normalization(self, blk_z=32, n_z=None):
        n_z = n_z or self.n_z
        self._mean_kernel_block = (32, 1, blk_z)
        sinos_shape_xyz = self.sinos_shape[1:][::-1] + (n_z,)
        self._mean_kernel_grid = [updiv(a, b) for a, b in zip(sinos_shape_xyz, self._mean_kernel_block)]
        self._mean_kernel_args = [self.d_sino_profile, np.int32(self.n_x), np.int32(self.n_angles), np.int32(n_z)]
        self._mean_kernel_kwargs = {
            "grid": self._mean_kernel_grid,
            "block": self._mean_kernel_block,
        }

    def _set_kernel_args_mult(self, blk_z=4, n_z=None):
        n_z = n_z or self.n_z
        self._op_kernel_block = (16, 16, blk_z)
        sinos_shape_xyz = self.sinos_shape[1:][::-1] + (n_z,)
        self._op_kernel_grid = [updiv(a, b) for a, b in zip(sinos_shape_xyz, self._op_kernel_block)]
        self._op_kernel_args = [self.d_sino_profile, np.int32(self.n_x), np.int32(self.n_angles), np.int32(n_z)]
        self._op_kernel_kwargs = {
            "grid": self._op_kernel_grid,
            "block": self._op_kernel_block,
        }

    def _init_filter(self, filter_cutoff, fft_num_threads, padding_mode):
        super()._init_filter(filter_cutoff, fft_num_threads, padding_mode)
        if filter_cutoff is None:
            return
        self._d_filter_f = self.processing.to_device("_filter_f", self._filter_f)

        self.padder = CudaPadding(
            (self.n_x, 1),
            ((self._pad_left, self._pad_right), (0, 0)),
            mode=self.padding_mode,
            # cuda_options={"ctx": self.processing.ctx},
        )
        fft_cls = get_fft_class()
        self._fft = fft_cls(self._filter_size, np.float32, r2c=True)

    def _apply_filter(self, sino_profile):
        if self._filter_f is None:
            return sino_profile

        sino_profile = sino_profile.reshape((-1, 1))  # view
        sino_profile_p = self.padder.pad(sino_profile).ravel()

        sino_profile_f = self._fft.fft(sino_profile_p)
        sino_profile_f *= self._d_filter_f
        self._fft.ifft(sino_profile_f, output=sino_profile_p)

        self.d_sino_profile[:] = sino_profile_p[self._pad_left : -self._pad_right]
        return self.d_sino_profile

    def _remove_rings_sino(self, d_sino):
        self._mean_kernel(d_sino, *self._mean_kernel_args, **self._mean_kernel_kwargs)
        self._apply_filter(self.d_sino_profile)
        self._op_kernel(d_sino, *self._op_kernel_args, **self._op_kernel_kwargs)

    def remove_rings_sinogram(self, sino, output=None):
        #
        if output is not None:
            raise NotImplementedError
        #
        if not (sino.flags.c_contiguous):
            # If the sinogram (or stack of sinogram) is not C-Contiguous, we'll proceed by looping over each
            # C-Contiguous sinogram
            d_sino = self.processing.allocate_array("d_sino", sino.shape, np.float32)
            d_sino[:] = sino[:]
        else:
            d_sino = sino
        self._remove_rings_sino(d_sino)
        if not (sino.flags.c_contiguous):
            sino[:] = self.processing.d_sino[:]
        return sino

    def remove_rings_sinograms(self, sinograms):
        if sinograms.flags.c_contiguous:
            self._remove_rings_sino(sinograms)
            return sinograms

        # If the stack of sinograms is not C-Contiguous, we have to proceed by looping over each C-Contiguous sinogram
        # (i.e don't copy the entire stack, just one sinogram at a time)
        self._set_kernel_args_normalization(blk_z=1, n_z=1)
        self._set_kernel_args_mult(blk_z=1, n_z=1)
        for i in range(sinograms.shape[0]):
            self.remove_rings_sinogram(sinograms[i])
        self._set_kernel_args_normalization()
        self._set_kernel_args_mult()
        return sinograms

    remove_rings = remove_rings_sinograms
