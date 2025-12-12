import numpy as np
from scipy.fft import rfft, irfft
from silx.image.tomography import get_next_power
from ..thirdparty.pore3d_deringer_munch import munchetal_filter
from ..utils import get_2D_3D_shape, get_num_threads, check_supported
from ..misc.fourier_filters import get_bandpass_filter


class MunchDeringer:
    def __init__(self, sigma, sinos_shape, levels=None, wname="db15", padding=None, padding_mode="edge"):
        """
        Initialize a "Munch Et Al" sinogram deringer. See References for more information.

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
        padding: tuple of two int, optional
            Horizontal padding to use for reducing the aliasing artefacts

        References
        ----------
        B. Munch, P. Trtik, F. Marone, M. Stampanoni, Stripe and ring artifact removal with
        combined wavelet-Fourier filtering, Optics Express 17(10):8567-8591, 2009.
        """
        self._get_shapes(sinos_shape, padding)
        self.sigma = sigma
        self.levels = levels
        self.wname = wname
        self.padding_mode = padding_mode
        self._check_can_use_wavelets()

    def _get_shapes(self, sinos_shape, padding):
        n_z, n_a, n_x = get_2D_3D_shape(sinos_shape)
        self.sinos_shape = n_z, n_a, n_x
        self.n_angles = n_a
        self.n_z = n_z
        self.n_x = n_x
        # Handle "padding=True" or "padding=False"
        if isinstance(padding, bool):
            if padding:
                padding = (n_x // 2, n_x // 2)
            else:
                padding = None
        #
        if padding is not None:
            pad_x1, pad_x2 = padding
            if np.iterable(pad_x1) or np.iterable(pad_x2):
                raise ValueError("Expected padding in the form (x1, x2)")
            self.sino_padded_shape = (n_a, n_x + pad_x1 + pad_x2)
        self.padding = padding

    def _check_can_use_wavelets(self):
        if munchetal_filter is None:
            raise ValueError("Need pywavelets to use this class")

    def _destripe_2D(self, sino, output):
        if self.padding is not None:
            sino = np.pad(sino, ((0, 0), self.padding), mode=self.padding_mode)
        res = munchetal_filter(sino, self.levels, self.sigma, wname=self.wname)
        if self.padding is not None:
            res = res[:, self.padding[0] : -self.padding[1]]
        output[:] = res
        return output

    def remove_rings(self, sinos, output=None):
        """
        Main function to performs rings artefacts removal on sinogram(s).
        CAUTION: this function defaults to in-place processing, meaning that
        the sinogram(s) you pass will be overwritten.

        Parameters
        ----------
        sinos: numpy.ndarray
            Sinogram or stack of sinograms.
        output: numpy.ndarray, optional
            Output array. If set to None (default), the output overwrites the input.
        """
        if output is None:
            output = sinos
        if sinos.ndim == 2:
            return self._destripe_2D(sinos, output)
        n_sinos = sinos.shape[0]
        for i in range(n_sinos):
            self._destripe_2D(sinos[i], output[i])
        return output


class VoDeringer:
    """
    An interface to Nghia Vo's "remove_all_stripe".
    Needs algotom to run.
    """

    def __init__(self, sinos_shape, **remove_all_stripe_options):
        self._init_lib()
        self._get_shapes(sinos_shape)
        self._remove_all_stripe_kwargs = remove_all_stripe_options

    def _init_lib(self):
        # Importing this is time-consumming, because of the numba initialization
        from algotom.prep.removal import remove_all_stripe

        #
        self._remove_all_stripe = remove_all_stripe

    def _get_shapes(self, sinos_shape):
        n_z, n_a, n_x = get_2D_3D_shape(sinos_shape)
        self.sinos_shape = n_z, n_a, n_x
        self.n_angles = n_a
        self.n_z = n_z
        self.n_x = n_x

    def remove_rings_sinogram(self, sino, output=None):
        new_sino = self._remove_all_stripe(sino, **self._remove_all_stripe_kwargs)  # out-of-place
        if output is not None:
            output[:] = new_sino[:]
            return output
        return new_sino

    def remove_rings_sinograms(self, sinos, output=None):
        if output is None:
            output = sinos
        for i in range(sinos.shape[0]):
            output[i] = self.remove_rings_sinogram(sinos[i])
        return output

    def remove_rings_radios(self, radios):
        sinos = np.moveaxis(radios, 1, 0)  # (n_a, n_z, n_x) --> (n_z, n_a, n_x)
        return self.remove_rings_sinograms(sinos)

    remove_rings = remove_rings_sinograms


class SinoMeanDeringer:
    supported_modes = ["subtract", "divide"]

    def __init__(self, sinos_shape, mode="subtract", filter_cutoff=None, padding_mode="edge", fft_num_threads=None):
        """
        Rings correction with mean subtraction/division.
        The principle of this method is to subtract (or divide) the sinogram by its mean along a certain axis.
        In short:
          sinogram -= filt(sinogram.mean(axis=0))
        where `filt` is some bandpass filter.

        Parameters
        ----------
        sinos_shape: tuple of int
            Sinograms shape, in the form (n_angles, n_x) or (n_sinos, n_angles, n_x)
        mode: str, optional
            Operation to do on the sinogram, either "subtract" or "divide"
        filter_cutoff: tuple, optional
            Cut-off of the bandpass filter applied on the sinogram profiles.
            Empty (default) means no filtering.
            Possible values forms are:
              - (sigma_low, sigma_high): two float values defining the standard deviation of
                gaussian(sigma_low) * (1 - gaussian(sigma_high)).
                High values of sigma mean stronger effect of associated filters.
              - ((cutoff_low, transition_low), (cutoff_high, transition_high))
                where "cutoff" is in normalized Nyquist frequency (0.5 is the maximum frequency),
                and "transition" is the width of filter decay in fraction of the cutoff frequency
        padding_mode: str, optional
            Padding mode when filtering the sinogram profile.
            Should be "constant" (i.e "zeros") for mathematical correctness,
            but in practice this yields a Gibbs effect when replicating the sinogram, so "edges" is recommended.
        fft_num_threads: int, optional
            How many threads to use for computing the fast Fourier transform when filtering the sinogram profile.
            Defaut is all the available threads.
        """
        self._get_shapes(sinos_shape)
        check_supported(mode, self.supported_modes, "operation mode")
        self.mode = mode
        self._init_filter(filter_cutoff, fft_num_threads, padding_mode)

    def _get_shapes(self, sinos_shape):
        n_z, n_a, n_x = get_2D_3D_shape(sinos_shape)
        self.sinos_shape = n_z, n_a, n_x
        self.n_angles = n_a
        self.n_z = n_z
        self.n_x = n_x

    def _init_filter(self, filter_cutoff, fft_num_threads, padding_mode):
        self.filter_cutoff = filter_cutoff
        self._filter_f = None
        if filter_cutoff is None:
            return
        self._filter_size = get_next_power(self.n_x * 2)
        self._filter_f = get_bandpass_filter(
            (1, self._filter_size),
            cutoff_lowpass=filter_cutoff[0],
            cutoff_highpass=filter_cutoff[1],
            use_rfft=True,
            data_type=np.float32,
        ).ravel()
        self._fft_n_threads = get_num_threads(fft_num_threads)
        # compat
        if padding_mode == "edges":
            padding_mode = "edge"
        #
        self.padding_mode = padding_mode
        size_diff = self._filter_size - self.n_x
        self._pad_left, self._pad_right = size_diff // 2, size_diff - size_diff // 2

    def _apply_filter(self, sino_profile):
        if self._filter_f is None:
            return sino_profile

        sino_profile = np.pad(sino_profile, (self._pad_left, self._pad_right), mode=self.padding_mode)

        sino_f = rfft(sino_profile, workers=self._fft_n_threads)
        sino_f *= self._filter_f

        return irfft(sino_f, workers=self._fft_n_threads)[self._pad_left : -self._pad_right]  # ascontiguousarray ?

    def remove_rings_sinogram(self, sino, output=None):
        #
        if output is not None:
            raise NotImplementedError
        #
        sino_profile = sino.mean(axis=0)
        sino_profile = self._apply_filter(sino_profile)
        if self.mode == "subtract":
            sino -= sino_profile
        elif self.mode == "divide":
            sino /= sino_profile
        return sino

    def remove_rings_sinograms(self, sinos, output=None):
        #
        if output is not None:
            raise NotImplementedError
        #
        for i in range(sinos.shape[0]):
            self.remove_rings_sinogram(sinos[i])

    remove_rings = remove_rings_sinograms
