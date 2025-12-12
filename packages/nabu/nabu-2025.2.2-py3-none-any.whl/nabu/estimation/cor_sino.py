import numpy as np
from scipy.fft import rfft

from ..utils import deprecated_class, deprecation_warning, is_scalar
from ..resources.logger import LoggerOrPrint


@deprecated_class("SinoCor center of rotation estimator is deprecated and will be removed in a future version")
class SinoCor:
    """
    This class has 2 methods:
        - overlap. Find a rough estimate of COR
        - accurate. Try to refine COR to 1/10 pixel
    """

    def __init__(self, img_1, img_2, logger=None):
        self.logger = LoggerOrPrint(logger)
        self.sx = img_1.shape[1]

        # algorithm cannot accept odd number of projs. This is handled in the SinoCORFinder class.

        # extract upper and lower part of sinogram, flipping H the upper part
        self.data1 = img_1
        self.data2 = img_2

        self.rcor_abs = round(self.sx / 2.0)
        self.cor_acc = round(self.sx / 2.0)

        # parameters for overlap sino - rough estimation

        # default sliding ROI is 20% of the width of the detector
        # the maximum size of ROI in the "right" case is 2*(self.sx - COR)
        # ex: 2048 pixels, COR= 2000, window_width should not exceed 96!

        self.window_width = round(self.sx / 5)

        # FIXME this import takes too much time
        # The SinoCor class will be removed anyway
        from scipy.signal import convolve2d

        self._convolve2d = convolve2d

    def schift(self, mat, val):
        ker = np.zeros((3, 3))
        s = 1.0
        if val < 0:
            s = -1.0
        val = s * val
        ker[1, 1] = 1 - val
        if s > 0:
            ker[1, 2] = val
        else:
            ker[1, 0] = val
        mat = self._convolve2d(mat, ker, mode="same")
        return mat

    def overlap(self, side="right", window_width=None):
        """
        Compute COR by minimizing difference of circulating ROI

         - side:         preliminary knowledge if the COR is on right or left
         - window_width: width of ROI that will slide on the other part of the sinogram
                         by default, 20% of the width of the detector.
        """

        if window_width is None:
            window_width = self.window_width

        if not (window_width & 1):
            window_width -= 1

        # number of pixels where the window will "slide".
        n = self.sx - int(window_width)
        nr = range(n)

        dmax = 1000000000.0
        imax = 0

        # Should we do both right and left and take the minimum "diff" of the 2 ?
        # windows self.data2 moves over self.data1, measure the width of the histogram and retains the smaller one.
        if side == "right":
            for i in nr:
                imout = self.data1[:, n - i : n - i + window_width] - self.data2[:, 0:window_width]
                diff = imout.max() - imout.min()
                if diff < dmax:
                    dmax = diff
                    imax = i
            self.cor_abs = self.sx - (imax + window_width + 1.0) / 2.0
            self.cor_rel = self.sx / 2 - (imax + window_width + 1.0) / 2.0
        elif side == "left":
            for i in nr:
                imout = self.data1[:, i : i + window_width] - self.data2[:, self.sx - window_width : self.sx]
                diff = imout.max() - imout.min()
                if diff < dmax:
                    dmax = diff
                    imax = i
            self.cor_abs = (imax + window_width - 1.0) / 2
            self.cor_rel = self.cor_abs - self.sx / 2.0 - 1
        else:
            raise ValueError(f"Invalid side given ({side}). should be 'left' or 'right'")
        if imax < 1:
            self.logger.warning("sliding width %d seems too large!" % window_width)
        self.rcor_abs = round(self.cor_abs)
        return self.rcor_abs

    def accurate(self, neighborhood=7, shift_value=0.1):
        """
        refine the calculation around COR integer pre-calculated value
        The search will be executed in the defined neighborhood

        Parameters
        -----------
        neighborhood: int
            Parameter for accurate calculation in the vicinity of the rough estimate.
            It must be an odd number.
            0.1 pixels float shifts will be performed over this number of pixel
        """
        # define the H-size (odd) of the window one can use to find the best overlap moving finely over ng pixels
        if not (neighborhood & 1):
            neighborhood += 1
        ng2 = int(neighborhood / 2)

        # pleft and pright are the number of pixels available on the left and the right of the cor position
        # to slide a window
        pleft = self.rcor_abs - ng2
        pright = self.sx - self.rcor_abs - ng2 - 1

        # the maximum window to slide is restricted by the smaller side
        if pleft > pright:
            p_sign = 1
            xwin = 2 * (self.sx - self.rcor_abs - ng2) - 1
        else:
            p_sign = -1
            xwin = 2 * (self.rcor_abs - ng2) + 1

        # Note that xwin is odd
        xc1 = self.rcor_abs - int(xwin / 2)
        xc2 = self.sx - self.rcor_abs - int(xwin / 2) - 1

        pixs = p_sign * (np.arange(neighborhood) - ng2)
        diff0 = 1000000000.0

        isfr = shift_value * np.arange(10)
        self.cor_acc = self.rcor_abs

        for pix in pixs:
            x0 = xc1 + pix
            for isf in isfr:
                if isf != 0:
                    ims = self.schift(self.data1[:, x0 : x0 + xwin].copy(), -p_sign * isf)
                else:
                    ims = self.data1[:, x0 : x0 + xwin]

                imout = ims - self.data2[:, xc2 : xc2 + xwin]
                diff = imout.max() - imout.min()
                if diff < diff0:
                    self.cor_acc = self.rcor_abs + (pix + p_sign * isf) / 2.0
                    diff0 = diff
        return self.cor_acc

    # Aliases
    estimate_cor_coarse = overlap
    estimate_cor_fine = accurate


class SinoCorInterface:
    """
    A class that mimics the interface of CenterOfRotation, while calling SinoCor
    """

    def __init__(self, logger=None, **kwargs):
        self._logger = logger

    def find_shift(
        self,
        img_1,
        img_2,
        side="right",
        window_width=None,
        neighborhood=7,
        shift_value=0.1,
        return_relative_to_middle=None,
        **kwargs,
    ):

        # COMPAT.
        if return_relative_to_middle is None:
            deprecation_warning(
                "The current default behavior is to return the shift relative the the middle of the image. In a future release, this function will return the shift relative to the left-most pixel. To keep the current behavior, please use 'return_relative_to_middle=True'.",
                do_print=True,
                func_name="CenterOfRotationCoarseToFine.find_shift",
            )
            return_relative_to_middle = True  # the kwarg above will be False by default in a future release
        # ---

        cor_finder = SinoCor(img_1, img_2, logger=self._logger)
        cor_finder.estimate_cor_coarse(side=side, window_width=window_width)
        cor = cor_finder.estimate_cor_fine(neighborhood=neighborhood, shift_value=shift_value)
        # offset will be added later - keep compatibility with result from AlignmentBase.find_shift()
        if return_relative_to_middle:
            return cor - (img_1.shape[1] - 1) / 2
        else:
            return cor


class CenterOfRotationFourierAngles:
    """This CoR estimation algo is proposed by V. Valls (BCU). It is based on the Fourier
    transform of the columns on the sinogram.
    It requires an initial guess of the CoR which is retrieved from
    dataset_info.dataset_scanner.x_rotation_axis_pixel_position. It is assumed in mm and pixel size in um.
    Options are (for the moment) hard-coded in the SinoCORFinder.cor_finder.extra_options dict.
    """

    def __init__(self, *args, **kwargs):
        pass

    def _convert_from_fft_2_fftpack_format(self, f_signal, o_signal_length):
        """
        Converts a scipy.fft.rfft into the (legacy) scipy.fftpack.rfft format.
        The fftpack.rfft returns a (roughly) twice as long array as fft.rfft as the latter returns an array
        of complex numbers whereas the former returns an array with real and imag parts in consecutive
        spots in the array.

        Parameters
        ----------
        f_signal : array_like
            The output of scipy.fft.rfft(signal)
        o_signal_length : int
            Size of the original signal (before FT).

        Returns
        -------
        out
            The rfft converted to the fftpack.rfft format (roughly twice as long).
        """
        out = np.zeros(o_signal_length, dtype=np.float32)
        if o_signal_length % 2 == 0:
            out[0] = f_signal[0].real
            out[1::2] = f_signal[1:].real
            out[2::2] = f_signal[1:-1].imag
        else:
            out[0] = f_signal[0].real
            out[1::2] = f_signal[1:].real
            out[2::2] = f_signal[1:].imag
        return out

    def _freq_radio(self, sinos, ifrom, ito):
        size = (sinos.shape[0] + sinos.shape[0] % 2) // 2
        fs = np.empty((size, sinos.shape[1]))
        for i in range(ifrom, ito):
            line = sinos[:, i]
            f_signal = rfft(line)
            f_signal = self._convert_from_fft_2_fftpack_format(f_signal, line.shape[0])
            f = np.abs(f_signal[: (f_signal.size - 1) // 2 + 1])
            f2 = np.abs(f_signal[(f_signal.size - 1) // 2 + 1 :][::-1])
            if len(f) > len(f2):
                f[1:] += f2
            else:
                f[0:] += f2
            fs[:, i] = f
        with np.errstate(divide="ignore", invalid="ignore", under="ignore"):
            fs = np.log(fs)
        return fs

    def gaussian(self, p, x):
        return p[3] + p[2] * np.exp(-((x - p[0]) ** 2) / (2 * p[1] ** 2))

    def tukey(self, p, x):
        pos, std, alpha, height, background = p
        alpha = np.clip(alpha, 0, 1)
        pi = np.pi
        inv_alpha = 1 - alpha
        width = std / (1 - alpha * 0.5)
        xx = (np.abs(x - pos) - (width * 0.5 * inv_alpha)) / (width * 0.5 * alpha)
        xx = np.clip(xx, 0, 1)
        return (0.5 + np.cos(pi * xx) * 0.5) * height + background

    def sinlet(self, p, x):
        std = p[1] * 2.5
        lin = np.maximum(0, std - np.abs(p[0] - x)) * 0.5 * np.pi / std
        return p[3] + p[2] * np.sin(lin)

    def _px(self, detector_width, abs_pos, near_width, near_std, crop_around_cor, near_step):
        sym_range = None
        if abs_pos is not None and crop_around_cor:
            sym_range = int(abs_pos - near_std * 2), int(abs_pos + near_std * 2)

        window = near_width
        if sym_range is not None:
            xx_from = max(window, sym_range[0])
            xx_to = max(xx_from, min(detector_width - window, sym_range[1]))
            if xx_from == xx_to:
                sym_range = None
        if sym_range is None:
            xx_from = window
            xx_to = detector_width - window

        xx = np.arange(xx_from, xx_to, near_step)

        return xx

    def _symmetry_correlation(self, px, array, angles, window, shift_sino):
        if shift_sino:
            shift_index = np.argmin(np.abs(angles - np.pi)) - np.argmin(np.abs(angles - 0))
        else:
            shift_index = None
        px_from = int(px[0])
        px_to = int(np.ceil(px[-1]))
        f_coef = np.empty(len(px))
        f_array = self._freq_radio(array, px_from - window, px_to + window)
        if shift_index is not None:
            shift_array = np.empty(array.shape, dtype=array.dtype)
            shift_array[0 : len(shift_array) - shift_index, :] = array[shift_index:, :]
            shift_array[len(shift_array) - shift_index :, :] = array[:shift_index, :]
            f_shift_array = self._freq_radio(shift_array, px_from - window, px_to + window)
        else:
            f_shift_array = f_array

        for j, x in enumerate(px):
            i = int(np.floor(x))
            if x - i > 0.4:  # TO DO : Specific to near_step = 0.5?
                f_left = f_array[:, i - window : i]
                f_right = f_shift_array[:, i + 1 : i + window + 1][:, ::-1]
            else:
                f_left = f_array[:, i - window : i]
                f_right = f_shift_array[:, i : i + window][:, ::-1]
            with np.errstate(divide="ignore", invalid="ignore"):
                f_coef[j] = np.sum(np.abs(f_left - f_right))
        return f_coef

    def _cor_correlation(self, px, abs_pos, near_std, signal, near_weight, near_alpha):
        if abs_pos is not None:
            if signal == "sinlet":
                coef = self.sinlet((abs_pos, near_std, -near_weight, 1), px)
            elif signal == "gaussian":
                coef = self.gaussian((abs_pos, near_std, -near_weight, 1), px)
            elif signal == "tukey":
                coef = self.tukey((abs_pos, near_std * 2, near_alpha, -near_weight, 1), px)
            else:
                raise ValueError("Shape unsupported")
        else:
            coef = np.ones_like(px)
        return coef

    def find_shift(
        self,
        sino,
        angles=None,
        side="center",
        near_std=100,
        near_width=20,
        shift_sino=True,
        crop_around_cor=False,
        signal="tukey",
        near_weight=0.1,
        near_alpha=0.5,
        near_step=0.5,
        return_relative_to_middle=None,
    ):
        detector_width = sino.shape[1]

        # COMPAT.
        if return_relative_to_middle is None:
            deprecation_warning(
                "The current default behavior is to return the shift relative the the middle of the image. In a future release, this function will return the shift relative to the left-most pixel. To keep the current behavior, please use 'return_relative_to_middle=True'.",
                do_print=True,
                func_name="CenterOfRotationFourierAngles.find_shift",
            )
            return_relative_to_middle = True  # the kwarg above will be False by default in a future release
        # ---

        if angles is None:
            angles = np.linspace(0, 2 * np.pi, sino.shape[0], endpoint=True)
        increment = np.abs(angles[0] - angles[1])
        if np.abs(angles[0] - angles[-1]) < (360 - 0.5) * np.pi / 180 - increment:
            raise ValueError("Not enough angles, estimator skipped")

        if is_scalar(side):
            abs_pos = side
        # COMPAT.
        elif side == "near":
            deprecation_warning(
                "side='near' is deprecated, please use side=<a scalar>", do_print=True, func_name="fourier_angles_near"
            )
            abs_pos = detector_width // 2
        ##.
        elif side == "center":
            abs_pos = detector_width // 2
        elif side == "left":
            abs_pos = detector_width // 4
        elif side == "right":
            abs_pos = detector_width * 3 // 4
        else:
            raise ValueError(f"side '{side}' is not handled")

        px = self._px(detector_width, abs_pos, near_width, near_std, crop_around_cor, near_step)

        coef_f = self._symmetry_correlation(
            px,
            sino,
            angles,
            near_width,
            shift_sino,
        )
        coef_p = self._cor_correlation(px, abs_pos, near_std, signal, near_weight, near_alpha)
        coef = coef_f * coef_p

        if len(px) > 0:
            cor = px[np.argmin(coef)] - (detector_width - 1) / 2
        else:
            # raise ValueError ?
            cor = None
        if not (return_relative_to_middle):
            cor += (detector_width - 1) / 2
        return cor

    __call__ = find_shift


class CenterOfRotationVo:
    """
    A wrapper around algotom 'find_center_vo' and 'find_center_360'.

    Nghia T. Vo, Michael Drakopoulos, Robert C. Atwood, and Christina Reinhard,
    "Reliable method for calculating the center of rotation in parallel-beam tomography,"
    Opt. Express 22, 19078-19086 (2014)
    """

    default_extra_options = {}

    def __init__(self, logger=None, verbose=False, extra_options=None):
        # These imports are time-consimming (numba initialization ?), do it here
        from algotom.prep.calculation import find_center_vo, find_center_360

        self._find_center_vo = find_center_vo
        self._find_center_360 = find_center_360
        self.extra_options = self.default_extra_options.copy()
        self.extra_options.update(extra_options or {})

    def find_shift(
        self,
        sino,
        halftomo=False,
        is_360=False,
        win_width=100,
        side="center",
        search_width_fraction=0.1,
        step=0.25,
        radius=4,
        ratio=0.5,
        dsp=True,
        ncore=None,
        hor_drop=None,
        ver_drop=None,
        denoise=True,
        norm=True,
        use_overlap=False,
        return_relative_to_middle=None,
    ):
        # COMPAT.
        if return_relative_to_middle is None:
            deprecation_warning(
                "The current default behavior is to return the shift relative the the middle of the image. In a future release, this function will return the shift relative to the left-most pixel. To keep the current behavior, please use 'return_relative_to_middle=True'.",
                do_print=True,
                func_name="CenterOfRotationVo.find_shift",
            )
            return_relative_to_middle = True  # the kwarg above will be False by default in a future release
        # ---

        if halftomo:
            side_algotom = {"left": 0, "right": 1}.get(side, None)
            cor, _, _, _ = self._find_center_360(
                sino, win_width, side=side_algotom, denoise=denoise, norm=norm, use_overlap=use_overlap, ncore=ncore
            )
        else:
            if is_360 and not (halftomo):
                # Take only one part of the sinogram and use "find_center_vo" - this works better in this case
                sino = sino[: sino.shape[0] // 2]

            sino_width = sino.shape[-1]
            search_width = int(search_width_fraction * sino_width)

            if side == "left":
                start, stop = 0, search_width
            elif side == "center":
                start, stop = sino_width // 2 - search_width, sino_width // 2 + search_width
            elif side == "right":
                start, stop = sino_width - search_width, sino_width
            elif is_scalar(side):
                # side is passed as an offset from the middle of detector
                side = side + (sino.shape[-1] - 1) / 2.0
                start, stop = max(0, side - search_width), min(sino_width, side + search_width)
            else:
                raise ValueError("Expected 'side' to be 'left', 'center', 'right' or a scalar")

            cor = self._find_center_vo(
                sino,
                start=start,
                stop=stop,
                step=step,
                radius=radius,
                ratio=ratio,
                dsp=dsp,
                ncore=ncore,
                hor_drop=hor_drop,
                ver_drop=ver_drop,
            )
        return cor if not (return_relative_to_middle) else cor - (sino.shape[1] - 1) / 2
