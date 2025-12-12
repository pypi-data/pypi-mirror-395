from math import pi
import numpy as np
from scipy.fft import rfft, irfft
from silx.image.tomography import compute_fourier_filter, get_next_power
from ..processing.padding_base import PaddingBase
from ..utils import check_supported, get_num_threads


class SinoFilter:
    available_filters = [
        "ramlak",
        "shepp-logan",
        "cosine",
        "hamming",
        "hann",
        "tukey",
        "lanczos",
        "hilbert",
    ]

    """
    A class for sinogram filtering.
    It does the following:
      - pad input array
      - Fourier transform each row
      - multiply with a 1D or 2D filter
      - inverse Fourier transform
    """

    available_padding_modes = PaddingBase.supported_modes
    default_extra_options = {"cutoff": 1.0, "fft_threads": 0}  # use all threads by default

    def __init__(
        self,
        sino_shape,
        filter_name=None,
        padding_mode="zeros",
        crop_filtered_data=True,
        extra_options=None,
    ):
        """
        Initialize a SinoFilter instance.

        Parameters
        ----------
        sino_shape: tuple
            Shape of sinogram, in the form (n_angles, detector_width) or (n_sinos, n_angles, detector_width)
        filter_name: str, optional
            Name of the filter. Default is ram-lak.
        padding_mode: str, optional
            How to pad the data prior to filtering. Default is zero-padding, corresponding to linear convolution with the filter kernel.
            In practice this value is often set to "edges" for interior tomography.
        crop_filtered_data: bool, optional
            Whether to crop the final, filtered sinogram. Default is True. See notes below.
        extra_options: dict, optional
            Dictionary of advanced extra options.

        Notes
        -----
        Sinogram filtering done in the Filtered Back-Projection (FBP) method consists, in theory, in applying a high-pass filter
        to the sinogram prior to backprojection. This high-pass filter is normally the Ramachandran-Lakshminarayanan (Ram-Lak) filter
        yielding a close-to-ideal reconstruction (see Natterer's "Mathematical methods in image reconstruction").
        As the filter kernel has a large extent in spatial domain, it's best performed in Fourier domain via the Fourier-convolution theorem.
        Filtering in Fourier domain should be done with a data padded to at least twice its size.
        Zero-padding should be used for mathematical correctness (so that multiplication in Fourier domain corresponds to an actual linear convolution).
        However if the sinogram does not decay to "zero" near the edges (i.e in interior tomography), padding with zeros usually gives artefacts after filtering.
        In this case, padding with edges is preferred (corresponding to a convolution with the "edges" extension mode).

        After inverse Fourier transform, the (padded and filtered) data is cropped back to its original size.
        In some cases, it's preferable to keep the data un-cropped for further processing.
        """

        self._init_extra_options(extra_options)
        self._set_padding_mode(padding_mode)
        self._calculate_shapes(sino_shape, crop_filtered_data)
        self._init_fft()
        self._allocate_memory()
        self._compute_filter(filter_name)

    def _init_extra_options(self, extra_options):
        self.extra_options = self.default_extra_options.copy()
        self.extra_options.update(extra_options or {})

    def _set_padding_mode(self, padding_mode):
        # Compat.
        if padding_mode == "edges":
            padding_mode = "edge"
        if padding_mode == "zeros":
            padding_mode = "constant"
        #
        check_supported(padding_mode, self.available_padding_modes, "padding mode")
        self.padding_mode = padding_mode

    def _calculate_shapes(self, sino_shape, crop_filtered_data):
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
        # Make sure to use int() here, otherwise pycuda/pyopencl will crash in some cases
        self.dwidth_padded = int(get_next_power(2 * self.dwidth))
        self.sino_padded_shape = (n_angles, self.dwidth_padded)
        if self.ndim == 3:
            self.sino_padded_shape = (n_sinos,) + self.sino_padded_shape
        sino_f_shape = list(self.sino_padded_shape)
        sino_f_shape[-1] = sino_f_shape[-1] // 2 + 1
        self.sino_f_shape = tuple(sino_f_shape)
        self.pad_left = (self.dwidth_padded - self.dwidth) // 2
        self.pad_right = self.dwidth_padded - self.dwidth - self.pad_left

        self.crop_filtered_data = crop_filtered_data
        self.output_shape = self.sino_shape
        if not (self.crop_filtered_data):
            self.output_shape = self.sino_padded_shape

    def _init_fft(self):
        pass

    def _allocate_memory(self):
        pass

    def set_filter(self, h_filt, normalize=True):
        """
        Set a filter for sinogram filtering.

        Parameters
        ----------
        h_filt: numpy.ndarray
            Array containing the filter. Each line of the sinogram will be filtered with
            this filter. It has to be the Real-to-Complex Fourier Transform
            of some real filter, padded to 2*sinogram_width.
        normalize: bool or float, optional
            Whether to normalize (multiply) the filter with pi/num_angles.
        """
        if h_filt.size != self.sino_f_shape[-1]:
            raise ValueError(
                """
                Invalid filter size: expected %d, got %d.
                Please check that the filter is the Fourier R2C transform of
                some real 1D filter.
                """
                % (self.sino_f_shape[-1], h_filt.size)
            )
        if not (np.iscomplexobj(h_filt)):
            print("Warning: expected a complex Fourier filter")
        self.filter_f = h_filt.copy()
        if normalize:
            self.filter_f *= pi / self.n_angles
        self.filter_f = self.filter_f.astype(np.complex64)

    def _compute_filter(self, filter_name):
        self.filter_name = filter_name or "ram-lak"
        # TODO add this one into silx
        if self.filter_name == "hilbert":
            freqs = np.fft.fftfreq(self.dwidth_padded)
            filter_f = 1.0 / (2 * pi * 1j) * np.sign(freqs)
        #
        else:
            filter_f = compute_fourier_filter(
                self.dwidth_padded,
                self.filter_name,
                cutoff=self.extra_options["cutoff"],
            )
        filter_f = filter_f[: self.dwidth_padded // 2 + 1]  # R2C
        self.set_filter(filter_f, normalize=True)

    def _check_array(self, arr):
        if arr.dtype != np.float32:
            raise ValueError("Expected data type = numpy.float32")
        if arr.shape != self.sino_shape:
            raise ValueError("Expected sinogram shape %s, got %s" % (self.sino_shape, arr.shape))

    def filter_sino(self, sino, output=None):
        """
        Perform the sinogram siltering.

        Parameters
        ----------
        sino: array
            Input sinogram (2D or 3D)
        output: array, optional
            Output array.
        """
        self._check_array(sino)
        # sino_padded = np.pad(
        #     sino, ((0, 0), (0, self.dwidth_padded - self.dwidth)), mode=self.padding_mode
        # )  # pad with a FFT-friendly layout
        sino_padded = np.pad(sino, ((0, 0), (self.pad_left, self.pad_right)), mode=self.padding_mode)
        sino_padded_f = rfft(sino_padded, axis=1, workers=get_num_threads(self.extra_options["fft_threads"]))
        sino_padded_f *= self.filter_f
        sino_filtered = irfft(sino_padded_f, axis=1, workers=get_num_threads(self.extra_options["fft_threads"]))

        if output is None:
            if not (self.crop_filtered_data):
                # No need to allocate extra memory here
                return sino_filtered
            res = np.zeros(self.output_shape, dtype=np.float32)
        else:
            res = output

        if self.crop_filtered_data:
            # res[:] = sino_filtered[..., : self.dwidth]  # pylint: disable=E1126 # ?!
            res[:] = sino_filtered[..., self.pad_left : -self.pad_right]  # pylint: disable=E1126 # ?!
        else:
            res[:] = sino_filtered[:]

        return res

    __call__ = filter_sino


def filter_sinogram(
    sinogram,
    padded_width,
    filter_name="ramlak",
    padding_mode="constant",
    normalize=True,
    filter_cutoff=1.0,
    crop_filtered_data=True,
    **padding_kwargs,
):
    """
    Simple function to filter sinogram.

    Parameters
    ----------
    sinogram: numpy.ndarray
        Sinogram, two dimensional array with shape (n_angles, sino_width)
    padded_width: int
        Width to use for padding. Must be greater than sinogram width (i.e than sinogram.shape[-1])
    filter_name: str, optional
        Which filter to use. Default is ramlak (roughly equivalent to abs(nu) in frequency domain)
    padding_mode: str, optional
        Which padding mode to use. Default is zero-padding.
    normalize: bool, optional
        Whether to multiply the filtered sinogram with pi/n_angles
    filter_cutoff: float, optional
        frequency cutoff for filter
    """
    n_angles, width = sinogram.shape

    # Initially, padding was done this way
    # sinogram_padded = np.pad(sinogram, ((0, 0), (0, padded_width - width)), mode=padding_mode, **padding_kwargs)

    #
    pad_left = (padded_width - width) // 2
    pad_right = padded_width - width - pad_left
    sinogram_padded = np.pad(sinogram, ((0, 0), (pad_left, pad_right)), mode=padding_mode, **padding_kwargs)
    #

    fourier_filter = compute_fourier_filter(padded_width, filter_name, cutoff=filter_cutoff)
    if normalize:
        fourier_filter *= np.pi / n_angles
    fourier_filter = fourier_filter[: padded_width // 2 + 1]  # R2C
    sino_f = rfft(sinogram_padded, axis=1)
    sino_f *= fourier_filter
    sino_filtered = irfft(sino_f, axis=1)
    if crop_filtered_data:
        # sino_filtered = sino_filtered[:, :width]  # pylint: disable=E1126 # ?!
        sino_filtered = sino_filtered[:, pad_left:-pad_right]  # pylint: disable=E1126 # ?!
    return sino_filtered
