from math import pi
from bisect import bisect
import numpy as np
from scipy.fft import rfft2, irfft2, fft2, ifft2
from ..utils import generate_powers, get_decay, check_supported, get_num_threads, deprecation_warning

# COMPAT.

#


def lmicron_to_db(Lmicron, energy, distance):
    r"""
    Utility to convert the "Lmicron" parameter of PyHST
    to a value of delta/beta.

    Parameters
    -----------
    Lmicron: float
        Length in microns, values of the parameter "PAGANIN_Lmicron"
        in PyHST2 parameter file.
    energy: float
        Energy in keV.
    distance: float
        Sample-detector distance in microns

    Notes
    --------
    The conversion is done using the formula

    .. math::
       L^2 = \\pi \\lambda D \\frac{\\delta}{\\beta}

    """
    L2 = Lmicron**2
    wavelength = 1.23984199e-3 / energy
    return L2 / (pi * wavelength * distance)


class PaganinPhaseRetrieval:
    available_padding_modes = ["zeros", "mean", "edge", "symmetric", "reflect"]
    powers = generate_powers()

    def __init__(
        self,
        shape,
        distance=0.5,
        energy=20,
        delta_beta=250.0,
        pixel_size=1e-6,
        padding="edge",
        use_rfft=True,
        use_R2C=None,
        fftw_num_threads=None,
        fft_num_threads=None,
    ):
        r"""
        Paganin Phase Retrieval for an infinitely distant point source.
        Formula (10) in [1].

        Parameters
        ----------
        shape: int or tuple
            Shape of each radio, in the format (num_rows, num_columns), i.e
            (size_vertical, size_horizontal).
            If an integer is provided, the shape is assumed to be square.
        distance : float, optional
            Propagation distance in meters.
        energy : float, optional
            Energy in keV.
        delta_beta: float, optional
            delta/beta ratio, where n = (1 - delta) + i*beta is the complex
            refractive index of the sample.
        pixel_size : float or tuple, optional
            Detector pixel size in meters. Default is 1e-6 (one micron)
            If a tuple is passed, the pixel size is set as (horizontal_size, vertical_size).
        padding : str, optional
            Padding method. Available are "zeros", "mean", "edge", "sym",
            "reflect". Default is "edge".
            Please refer to the "Padding" section below for more details.
        use_rfft: bool, optional
            Whether to use Real-to-Complex (R2C) transform instead of
            standard Complex-to-Complex transform, providing better performances
        use_R2C: bool, optional
            DEPRECATED, use use_rfft instead
        fftw_num_threads: bool or None or int, optional
            DEPRECATED - please use fft_num_threads
        fft_num_threads: bool or None or int, optional
            Number of threads for FFT.
            Default is to use all available threads. You can pass a negative number
            to use N - fft_num_threads cores.

        Important
        ----------
        Mind the units! Distance and pixel size are in meters, and energy is in keV.


        Notes
        ------
        **Padding methods**

        The phase retrieval is a convolution done in Fourier domain using FFT,
        so the Fourier transform size has to be at least twice the size of
        the original data. Mathematically, the data should be padded with zeros
        before being Fourier transformed. However, in practice, this can lead
        to artefacts at the edges (Gibbs effect) if the data does not go to
        zero at the edges.
        Apart from applying an apodization (Hamming, Blackman, etc), a common
        strategy to avoid these artefacts is to pad the data.
        In tomography reconstruction, this is usually done by replicating the
        last(s) value(s) of the edges ; but one can think of other methods:

           - "zeros": the data is simply padded with zeros.
           - "mean": the upper side of extended data is padded with the mean of
             the first row, the lower side with the mean of the last row, etc.
           - "edge": the data is padded by replicating the edges.
             This is the default mode.
           - "sym": the data is padded by mirroring the data with respect
             to its edges. See ``numpy.pad()``.
           - "reflect": the data is padded by reflecting the data with respect
             to its edges, including the edges. See ``numpy.pad()``.


        **Formulas**

        The radio is divided, in the Fourier domain, by the original "Paganin filter" `[1]`.

        .. math::

          F = 1 + \\frac{\\delta}{\\beta} \\lambda D \\pi |k|^2

        where k is the wave vector.


        References
        -----------
        [1] D. Paganin Et Al, "Simultaneous phase and amplitude extraction
            from a single defocused image of a homogeneous object",
            Journal of Microscopy, Vol 206, Part 1, 2002
        """
        self._init_parameters(distance, energy, pixel_size, delta_beta, padding)
        self._calc_shape(shape)
        # COMPAT.
        if use_R2C is not None:
            deprecation_warning("'use_R2C' is replaced with 'use_rfft'", func_name="pag_r2c")
        if fftw_num_threads is not None:
            deprecation_warning("'fftw_num_threads' is replaced with 'fft_num_threads'", func_name="pag_fftw")
            fft_num_threads = fftw_num_threads
        # ---
        self._get_fft(use_rfft, fft_num_threads)
        self.compute_filter()

    def _init_parameters(self, distance, energy, pixel_size, delta_beta, padding):
        self.distance_cm = distance * 1e2
        self.distance_micron = distance * 1e6
        self.energy_kev = energy
        if np.isscalar(pixel_size):
            self.pixel_size_xy_micron = (pixel_size * 1e6, pixel_size * 1e6)
        else:
            self.pixel_size_xy_micron = pixel_size * 1e6
        # COMPAT.
        self.pixel_size_micron = self.pixel_size_xy_micron[0]
        #
        self.delta_beta = delta_beta
        self.wavelength_micron = 1.23984199e-3 / self.energy_kev
        self.padding = padding
        self.padding_methods = {
            "zeros": self._pad_zeros,
            "mean": self._pad_mean,
            "edge": self._pad_edge,
            "symmetric": self._pad_sym,
            "reflect": self._pad_reflect,
        }

    def _get_fft(self, use_rfft, fft_num_threads):
        self.use_rfft = use_rfft
        self.use_R2C = use_rfft  # Compat.
        self.fft_num_threads = get_num_threads(fft_num_threads)
        if self.use_rfft:
            self.fft_func = rfft2
            self.ifft_func = irfft2
        else:
            self.fft_func = fft2
            self.ifft_func = ifft2

    def _calc_shape(self, shape):
        if np.isscalar(shape):
            shape = (shape, shape)
        else:
            assert len(shape) == 2
        self.shape = shape
        self._calc_padded_shape()

    def _calc_padded_shape(self):
        """
        Compute the padded shape.
        If margin = 0, length_padded = next_power(2*length).
        Otherwise : length_padded = next_power(2*(length - margins))

        Principle
        ----------

        <--------------------- nx_p --------------------->
        |         |        original data       |         |
        < -- Pl - ><-- L -->< -- nx --><-- R --><-- Pr -->
                   <----------- nx0 ----------->

        Pl, Pr : left/right padding length
        L, R : left/right margin
        nx : length of inner data (and length of final result)
        nx0 : length of original data
        nx_p : total length of padded data
        """
        n_y, n_x = self.shape
        n_y_p = self._get_next_power(2 * n_y)
        n_x_p = self._get_next_power(2 * n_x)
        self.shape_padded = (n_y_p, n_x_p)
        self.data_padded = np.zeros((n_y_p, n_x_p), dtype=np.float64)
        self.pad_top_len = (n_y_p - n_y) // 2
        self.pad_bottom_len = n_y_p - n_y - self.pad_top_len
        self.pad_left_len = (n_x_p - n_x) // 2
        self.pad_right_len = n_x_p - n_x - self.pad_left_len

    def _get_next_power(self, n):
        """
        Given a number, get the closest (upper) number p such that
        p is a power of 2, 3, 5 and 7.
        """
        idx = bisect(self.powers, n)
        if self.powers[idx - 1] == n:
            return n
        return self.powers[idx]

    def compute_filter(self):
        nyp, nxp = self.shape_padded
        fftfreq = np.fft.rfftfreq if self.use_rfft else np.fft.fftfreq
        fy = np.fft.fftfreq(nyp, d=self.pixel_size_xy_micron[1])
        fx = fftfreq(nxp, d=self.pixel_size_xy_micron[0])
        self._coords_grid = np.add.outer(fy**2, fx**2)
        #
        k2 = self._coords_grid
        D = self.distance_micron
        L = self.wavelength_micron
        db = self.delta_beta
        self.paganin_filter = 1.0 / (1 + db * L * D * pi * k2)

    def pad_with_values(self, data, top_val=0, bottom_val=0, left_val=0, right_val=0):
        """
        Pad the data into `self.padded_data` with values.

        Parameters
        ----------
        data: numpy.ndarray
            data (radio)
        top_val: float or numpy.ndarray, optional
            Value(s) to fill the top of the padded data with.
        bottom_val: float or numpy.ndarray, optional
            Value(s) to fill the bottom of the padded data with.
        left_val: float or numpy.ndarray, optional
            Value(s) to fill the left of the padded data with.
        right_val: float or numpy.ndarray, optional
            Value(s) to fill the right of the padded data with.
        """
        self.data_padded.fill(0)
        Pu, Pd = self.pad_top_len, self.pad_bottom_len
        Pl, Pr = self.pad_left_len, self.pad_right_len
        self.data_padded[:Pu, :] = top_val
        self.data_padded[-Pd:, :] = bottom_val
        self.data_padded[:, :Pl] = left_val
        self.data_padded[:, -Pr:] = right_val
        self.data_padded[Pu:-Pd, Pl:-Pr] = data
        # Transform the data to the FFT layout
        self.data_padded = np.roll(self.data_padded, (-Pu, -Pl), axis=(0, 1))

    def _pad_zeros(self, data):
        return self.pad_with_values(data, top_val=0, bottom_val=0, left_val=0, right_val=0)

    def _pad_mean(self, data):
        """
        Pad the data at each border with a different constant value.
        The value depends on the padding size:
          - On the left, value = mean(first data column)
          - On the right, value = mean(last data column)
          - On the top, value = mean(first data row)
          - On the bottom, value = mean(last data row)
        """
        return self.pad_with_values(
            data,
            top_val=np.mean(data[0, :]),
            bottom_val=np.mean(data[-1, :]),
            left_val=np.mean(data[:, 0]),
            right_val=np.mean(data[:, -1]),
        )

    def _pad_numpy(self, data, mode):
        data_padded = np.pad(
            data, ((self.pad_top_len, self.pad_bottom_len), (self.pad_left_len, self.pad_right_len)), mode=mode
        )
        # Transform the data to the FFT layout
        Pu, Pl = self.pad_top_len, self.pad_left_len
        return np.roll(data_padded, (-Pu, -Pl), axis=(0, 1))

    def _pad_edge(self, data):
        self.data_padded = self._pad_numpy(data, mode="edge")

    def _pad_sym(self, data):
        self.data_padded = self._pad_numpy(data, mode="symmetric")

    def _pad_reflect(self, data):
        self.data_padded = self._pad_numpy(data, mode="reflect")

    def pad_data(self, data, padding_method=None):
        padding_method = padding_method or self.padding
        check_supported(padding_method, self.available_padding_modes, "padding mode")
        if padding_method not in self.padding_methods:
            raise ValueError(
                "Unknown padding method %s. Available are: %s"
                % (padding_method, str(list(self.padding_methods.keys())))
            )
        pad_func = self.padding_methods[padding_method]
        pad_func(data)
        return self.data_padded

    def apply_filter(self, radio, padding_method=None, output=None):
        self.pad_data(radio, padding_method=padding_method)
        radio_f = self.fft_func(self.data_padded, workers=self.fft_num_threads)
        radio_f *= self.paganin_filter
        radio_filtered = self.ifft_func(radio_f, workers=self.fft_num_threads).real
        s0, s1 = self.shape
        if output is None:
            return radio_filtered[:s0, :s1]
        else:
            output[:, :] = radio_filtered[:s0, :s1]
            return output

    def lmicron_to_db(self, Lmicron):
        """
        Utility to convert the "Lmicron" parameter of PyHST
        to a value of delta/beta.
        Please see the doc of nabu.preproc.phase.lmicron_to_db()
        """
        return lmicron_to_db(Lmicron, self.energy_kev, self.distance_micron)

    __call__ = apply_filter

    retrieve_phase = apply_filter


def compute_paganin_margin(shape, cutoff=1e3, **pag_kwargs):
    """
    Compute the convolution margin to use when calling PaganinPhaseRetrieval class.

    Parameters
    -----------
    shape: tuple
        Detector shape in the form (n_z, n_x)
    """
    P = PaganinPhaseRetrieval(shape, **pag_kwargs)

    ifft_func = np.fft.irfft2 if P.use_rfft else np.fft.ifft2
    conv_kernel = ifft_func(P.paganin_filter)

    vmax = conv_kernel[0, 0]

    v_margin = get_decay(conv_kernel[:, 0], cutoff=cutoff, vmax=vmax)
    h_margin = get_decay(conv_kernel[0, :], cutoff=cutoff, vmax=vmax)
    # If the Paganin filter is very narrow, then the corresponding convolution
    # kernel is constant, and np.argmax() gives 0 (when it should give the max value)
    if v_margin == 0:
        v_margin = shape[0]
    if h_margin == 0:
        h_margin = shape[1]

    return v_margin, h_margin
