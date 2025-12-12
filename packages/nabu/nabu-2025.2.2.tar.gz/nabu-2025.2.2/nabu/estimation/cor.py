import math
import numpy as np
from ..utils import deprecated_class, deprecation_warning, is_scalar
from ..misc import fourier_filters
from .alignment import AlignmentBase, plt, progress_bar, local_fftn, local_ifftn


# three possible  values for the validity check, which can optionally be returned by the find_shifts methods
cor_result_validity = {
    "unknown": "unknown",
    "sound": "sound",
    "correct": "sound",
    "questionable": "questionable",
}


class CenterOfRotation(AlignmentBase):

    def find_shift(
        self,
        img_1: np.ndarray,
        img_2: np.ndarray,
        side=None,
        shift_axis: int = -1,
        roi_yxhw=None,
        median_filt_shape=None,
        padding_mode=None,
        peak_fit_radius=1,
        high_pass=None,
        low_pass=None,
        return_validity=False,
        return_relative_to_middle=None,
    ):
        """Find the Center of Rotation (CoR), given two images.

        This method finds the half-shift between two opposite images, by
        means of correlation computed in Fourier space.

        The output of this function, allows to compute motor movements for
        aligning the sample rotation axis. Given the following values:

           - L1: distance from source to motor
           - L2: distance from source to detector
           - ps: physical pixel size
           - v: output of this function

        displacement of motor = (L1 / L2 * ps) * v

        Parameters
        ----------
        img_1: numpy.ndarray
            First image
        img_2: numpy.ndarray
            Second image, it needs to have been flipped already (e.g. using numpy.fliplr).
        shift_axis: int
            Axis along which we want the shift to be computed. Default is -1 (horizontal).
        roi_yxhw: (2, ) or (4, ) numpy.ndarray, tuple, or array, optional
            4 elements vector containing: vertical and horizontal coordinates
            of first pixel, plus height and width of the Region of Interest (RoI).
            Or a 2 elements vector containing: plus height and width of the
            centered Region of Interest (RoI).
            Default is None -> deactivated.
        median_filt_shape: (2, ) numpy.ndarray, tuple, or array, optional
            Shape of the median filter window. Default is None -> deactivated.
        padding_mode: str in numpy.pad's mode list, optional
            Padding mode, which determines the type of convolution. If None or
            'wrap' are passed, this resorts to the traditional circular convolution.
            If 'edge' or 'constant' are passed, it results in a linear convolution.
            Default is the circular convolution.
            All options are:
                None | 'constant' | 'edge' | 'linear_ramp' | 'maximum' | 'mean'
                | 'median' | 'minimum' | 'reflect' | 'symmetric' |'wrap'
        peak_fit_radius: int, optional
            Radius size around the max correlation pixel, for sub-pixel fitting.
            Minimum and default value is 1.
        low_pass: float or sequence of two floats
            Low-pass filter properties, as described in `nabu.misc.fourier_filters`
        high_pass: float or sequence of two floats
            High-pass filter properties, as described in `nabu.misc.fourier_filters`
        return_validity: a boolean, defaults to false
            if set to True adds a second return value which may have three string values.
            These values are "unknown", "sound", "questionable".
            It will be "unknown" if the  validation method is not implemented
            and it will be "sound" or "questionable" if it is implemented.


        Raises
        ------
        ValueError
            In case images are not 2-dimensional or have different sizes.

        Returns
        -------
        float
            Estimated center of rotation position from the center of the RoI in pixels.

        Examples
        --------
        The following code computes the center of rotation position for two
        given images in a tomography scan, where the second image is taken at
        180 degrees from the first.

        >>> radio1 = data[0, :, :]
        ... radio2 = np.fliplr(data[1, :, :])
        ... CoR_calc = CenterOfRotation()
        ... cor_position = CoR_calc.find_shift(radio1, radio2)

        Or for noisy images:

        >>> cor_position = CoR_calc.find_shift(radio1, radio2, median_filt_shape=(3, 3))
        """
        # COMPAT.
        if return_relative_to_middle is None:
            deprecation_warning(
                "The current default behavior is to return the shift relative the the middle of the image. In a future release, this function will return the shift relative to the left-most pixel. To keep the current behavior, please use 'return_relative_to_middle=True'.",
                do_print=True,
                func_name="CenterOfRotation.find_shift",
            )
            return_relative_to_middle = True  # the kwarg above will be False by default in a future release
        # ---

        self._check_img_pair_sizes(img_1, img_2)

        if peak_fit_radius < 1:
            self.logger.warning("Parameter peak_fit_radius should be at least 1, given: %d instead." % peak_fit_radius)
            peak_fit_radius = 1

        img_shape = img_2.shape
        roi_yxhw = self._determine_roi(img_shape, roi_yxhw)

        img_1 = self._prepare_image(img_1, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape)
        img_2 = self._prepare_image(img_2, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape)

        cc = self._compute_correlation_fft(img_1, img_2, padding_mode, high_pass=high_pass, low_pass=low_pass)
        img_shape = cc.shape  # Because cc.shape can differ from img_2.shape (e.g. in case of odd nb of cols)
        cc_vs = np.fft.fftfreq(img_shape[-2], 1 / img_shape[-2])
        cc_hs = np.fft.fftfreq(img_shape[-1], 1 / img_shape[-1])

        (f_vals, fv, fh) = self.extract_peak_region_2d(cc, peak_radius=peak_fit_radius, cc_vs=cc_vs, cc_hs=cc_hs)
        fitted_shifts_vh = self.refine_max_position_2d(f_vals, fv, fh)

        estimated_cor = fitted_shifts_vh[shift_axis] / 2.0

        if is_scalar(side):
            near_pos = side - (img_1.shape[-1] - 1) / 2
            if (
                np.abs(near_pos - estimated_cor) / near_pos > 0.2
            ):  # For comparison, near_pos is RELATIVE to the middle of image (as estimated_cor is).
                validity_check_result = cor_result_validity["questionable"]
            else:
                validity_check_result = cor_result_validity["sound"]
        else:
            validity_check_result = cor_result_validity["unknown"]

        if not (return_relative_to_middle):
            estimated_cor += (img_1.shape[-1] - 1) / 2

        if return_validity:
            return estimated_cor, validity_check_result
        else:
            return estimated_cor


class CenterOfRotationSlidingWindow(CenterOfRotation):
    def find_shift(
        self,
        img_1: np.ndarray,
        img_2: np.ndarray,
        side="center",
        window_width=None,
        roi_yxhw=None,
        median_filt_shape=None,
        peak_fit_radius=1,
        high_pass=None,
        low_pass=None,
        return_validity=False,
        return_relative_to_middle=None,
    ):
        """Semi-automatically find the Center of Rotation (CoR), given two images
        or sinograms. Suitable for half-acquisition scan.

        This method finds the half-shift between two opposite images,  by
        minimizing difference over a moving window.

        Parameters and usage is the same as CenterOfRotation, except for the following two parameters.

        Parameters
        ----------
        side: string or float, optional
            Expected region of the CoR. Allowed values: 'left', 'center' or 'right'. Default is 'center'
        window_width: int, optional
            Width of window that will slide on the other image / part of the sinogram. Default is None.
        """
        # COMPAT.
        if return_relative_to_middle is None:
            deprecation_warning(
                "The current default behavior is to return the shift relative the the middle of the image. In a future release, this function will return the shift relative to the left-most pixel. To keep the current behavior, please use 'return_relative_to_middle=True'.",
                do_print=True,
                func_name="CenterOfRotationSlidingWindow.find_shift",
            )
            return_relative_to_middle = True  # the kwarg above will be False by default in a future release
        # ---
        validity_check_result = cor_result_validity["unknown"]

        if side is None:
            raise ValueError("Side should be one of 'left', 'right', 'center' or a scalar. 'None' was given instead")

        self._check_img_pair_sizes(img_1, img_2)

        if peak_fit_radius < 1:
            self.logger.warning("Parameter peak_fit_radius should be at least 1, given: %d instead." % peak_fit_radius)
            peak_fit_radius = 1

        img_shape = img_2.shape
        roi_yxhw = self._determine_roi(img_shape, roi_yxhw)

        img_1 = self._prepare_image(
            img_1, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape, high_pass=high_pass, low_pass=low_pass
        )
        img_2 = self._prepare_image(
            img_2, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape, high_pass=high_pass, low_pass=low_pass
        )
        img_shape = img_2.shape
        img_width = img_shape[-1]

        if isinstance(side, str):
            if window_width is None:
                if side == "center":
                    window_width = round(img_width / 4.0 * 3.0)
                else:
                    window_width = round(img_width / 10)
            window_shift = window_width // 2
            window_width = window_shift * 2 + 1
            if side == "right":
                win_2_start = 0
            elif side == "left":
                win_2_start = img_width - window_width
            else:
                win_2_start = img_width // 2 - window_shift
        else:
            abs_pos = int(side + img_width // 2)
            window_fraction = 0.1  # Hard-coded ?

            window_width = round(window_fraction * img_width)
            window_shift = window_width // 2
            window_width = window_shift * 2 + 1

            win_2_start = np.clip(abs_pos - window_shift, 0, img_width // 2 - 1)
            win_2_start = img_width // 2 - 1 - win_2_start

        win_1_start_seed = 0
        # number of pixels where the window will "slide".
        n = img_width - window_width

        win_2_end = win_2_start + window_width

        diffs_mean = np.zeros((n,), dtype=img_1.dtype)
        diffs_std = np.zeros((n,), dtype=img_1.dtype)

        for ii in progress_bar(range(n), verbose=self.verbose):
            win_1_start = win_1_start_seed + ii
            win_1_end = win_1_start + window_width
            img_diff = img_1[:, win_1_start:win_1_end] - img_2[:, win_2_start:win_2_end]
            diffs_abs = np.abs(img_diff)
            diffs_mean[ii] = diffs_abs.mean()
            diffs_std[ii] = diffs_abs.std()

        diffs_mean = diffs_mean.min() - diffs_mean
        win_ind_max = np.argmax(diffs_mean)

        diffs_std = diffs_std.min() - diffs_std
        if win_ind_max != np.argmax(diffs_std):
            self.logger.warning(
                "Minimum mean difference and minimum std-dev of differences do not coincide. This means that the validity of the found solution might be questionable."
            )
            validity_check_result = cor_result_validity["questionable"]
        else:
            validity_check_result = cor_result_validity["sound"]

        (f_vals, f_pos) = self.extract_peak_regions_1d(diffs_mean, peak_radius=peak_fit_radius)
        win_pos_max, win_val_max = self.refine_max_position_1d(f_vals, return_vertex_val=True)

        # Derive the COR
        if is_scalar(side):
            cor_h = -(win_2_start - (win_1_start_seed + win_ind_max + win_pos_max)) / 2.0
            cor_pos = -(win_2_start - (win_1_start_seed + np.arange(n))) / 2.0
        else:
            cor_h = -(win_2_start - (win_ind_max + win_pos_max)) / 2.0
            cor_pos = -(win_2_start - np.arange(n)) / 2.0

        if (side == "right" and win_ind_max == 0) or (side == "left" and win_ind_max == n):
            self.logger.warning("Sliding window width %d might be too large!" % window_width)

        if self.verbose:
            print("Lowest difference window: index=%d, range=[0, %d]" % (win_ind_max, n))
            print("CoR tested for='%s', found at voxel=%g (from center)" % (side, cor_h))

            f, ax = plt.subplots(1, 1)
            self._add_plot_window(f, ax=ax)
            ax.stem(cor_pos, diffs_mean, label="Mean difference")
            ax.stem(cor_h, win_val_max, linefmt="C1-", markerfmt="C1o", label="Best mean difference")
            ax.stem(cor_pos, -diffs_std, linefmt="C2-", markerfmt="C2o", label="Std-dev difference")
            ax.set_title("Window dispersions")
            plt.legend()
            plt.show(block=False)

        if not (return_relative_to_middle):
            cor_h += (img_width - 1) / 2.0

        if return_validity:
            return cor_h, validity_check_result
        else:
            return cor_h


class CenterOfRotationGrowingWindow(CenterOfRotation):
    def find_shift(
        self,
        img_1: np.ndarray,
        img_2: np.ndarray,
        side="all",
        min_window_width=11,
        roi_yxhw=None,
        median_filt_shape=None,
        padding_mode=None,
        peak_fit_radius=1,
        high_pass=None,
        low_pass=None,
        return_validity=False,
        return_relative_to_middle=None,
    ):
        """Automatically find the Center of Rotation (CoR), given two images or
        sinograms. Suitable for half-acquisition scan.

        This method finds the half-shift between two opposite images,  by
        minimizing difference over a moving window.

        Usage and parameters are the same as CenterOfRotationSlidingWindow, except for the following parameter.

        Parameters
        ----------
        min_window_width: int, optional
            Minimum window width that covers the common region of the two images /
            sinograms. Default is 11.
        """
        # COMPAT.
        if return_relative_to_middle is None:
            deprecation_warning(
                "The current default behavior is to return the shift relative the the middle of the image. In a future release, this function will return the shift relative to the left-most pixel. To keep the current behavior, please use 'return_relative_to_middle=True'.",
                do_print=True,
                func_name="CenterOfRotationGrowingWindow.find_shift",
            )
            return_relative_to_middle = True  # the kwarg above will be False by default in a future release
        # ---
        validity_check_result = cor_result_validity["unknown"]

        self._check_img_pair_sizes(img_1, img_2)

        if peak_fit_radius < 1:
            self.logger.warning("Parameter peak_fit_radius should be at least 1, given: %d instead." % peak_fit_radius)
            peak_fit_radius = 1

        img_shape = img_2.shape
        roi_yxhw = self._determine_roi(img_shape, roi_yxhw)

        img_1 = self._prepare_image(
            img_1, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape, high_pass=high_pass, low_pass=low_pass
        )
        img_2 = self._prepare_image(
            img_2, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape, high_pass=high_pass, low_pass=low_pass
        )
        img_shape = img_2.shape

        def window_bounds(mid_point, window_max_width=img_shape[-1]):
            return (
                np.fmax(np.ceil(mid_point - window_max_width / 2), 0).astype(np.intp),
                np.fmin(np.ceil(mid_point + window_max_width / 2), img_shape[-1]).astype(np.intp),
            )

        img_lower_half_size = np.floor(img_shape[-1] / 2).astype(np.intp)
        img_upper_half_size = np.ceil(img_shape[-1] / 2).astype(np.intp)

        if is_scalar(side):
            self.logger.error(
                "Passing a first CoR guess is not supported for CenterOfRotationGrowingWindow. Using side='all'."
            )
            side = "all"
        if side.lower() == "right":
            win_1_mid_start = img_lower_half_size
            win_1_mid_end = np.floor(img_shape[-1] * 3 / 2).astype(np.intp) - min_window_width
            win_2_mid_start = -img_upper_half_size + min_window_width
            win_2_mid_end = img_upper_half_size
        elif side.lower() == "left":
            win_1_mid_start = -img_lower_half_size + min_window_width
            win_1_mid_end = img_lower_half_size
            win_2_mid_start = img_upper_half_size
            win_2_mid_end = np.ceil(img_shape[-1] * 3 / 2).astype(np.intp) - min_window_width
        elif side.lower() == "center":
            win_1_mid_start = 0
            win_1_mid_end = img_shape[-1]
            win_2_mid_start = 0
            win_2_mid_end = img_shape[-1]
        elif side.lower() == "all":
            win_1_mid_start = -img_lower_half_size + min_window_width
            win_1_mid_end = np.floor(img_shape[-1] * 3 / 2).astype(np.intp) - min_window_width
            win_2_mid_start = -img_upper_half_size + min_window_width
            win_2_mid_end = np.ceil(img_shape[-1] * 3 / 2).astype(np.intp) - min_window_width
        else:
            raise ValueError(
                "Side should be one of 'left', 'right', or 'center' or 'all'. '%s' was given instead" % side.lower()
            )

        n1 = win_1_mid_end - win_1_mid_start
        n2 = win_2_mid_end - win_2_mid_start

        if not n1 == n2:
            raise ValueError(
                "Internal error: the number of window steps for the two images should be the same."
                + "Found the following configuration instead => Side: %s, #1: %d, #2: %d" % (side, n1, n2)
            )

        diffs_mean = np.zeros((n1,), dtype=img_1.dtype)
        diffs_std = np.zeros((n1,), dtype=img_1.dtype)

        for ii in progress_bar(range(n1), verbose=self.verbose):
            win_1 = window_bounds(win_1_mid_start + ii)
            win_2 = window_bounds(win_2_mid_end - ii)
            img_diff = img_1[:, win_1[0] : win_1[1]] - img_2[:, win_2[0] : win_2[1]]
            diffs_abs = np.abs(img_diff)
            diffs_mean[ii] = diffs_abs.mean()
            diffs_std[ii] = diffs_abs.std()

        diffs_mean = diffs_mean.min() - diffs_mean
        win_ind_max = np.argmax(diffs_mean)

        diffs_std = diffs_std.min() - diffs_std
        if win_ind_max != np.argmax(diffs_std):
            self.logger.warning(
                "Minimum mean difference and minimum std-dev of differences do not coincide. This means that the validity of the found solution might be questionable."
            )
            validity_check_result = cor_result_validity["questionable"]
        else:
            validity_check_result = cor_result_validity["sound"]

        (f_vals, f_pos) = self.extract_peak_regions_1d(diffs_mean, peak_radius=peak_fit_radius)
        win_pos_max, win_val_max = self.refine_max_position_1d(f_vals, return_vertex_val=True)

        cor_h = (win_1_mid_start + (win_ind_max + win_pos_max) - img_upper_half_size) / 2.0

        if (side.lower() == "right" and win_ind_max == 0) or (side.lower() == "left" and win_ind_max == n1):
            self.logger.warning("Minimum growing window width %d might be too large!" % min_window_width)

        if self.verbose:
            cor_pos = (win_1_mid_start + np.arange(n1) - img_upper_half_size) / 2.0

            self.logger.info("Lowest difference window: index=%d, range=[0, %d]" % (win_ind_max, n1))
            self.logger.info("CoR tested for='%s', found at voxel=%g (from center)" % (side, cor_h))

            f, ax = plt.subplots(1, 1)
            self._add_plot_window(f, ax=ax)
            ax.stem(cor_pos, diffs_mean, label="Mean difference")
            ax.stem(cor_h, win_val_max, linefmt="C1-", markerfmt="C1o", label="Best mean difference")
            ax.stem(cor_pos, -diffs_std, linefmt="C2-", markerfmt="C2o", label="Std-dev difference")
            ax.set_title("Window dispersions")
            plt.show(block=False)

        if not (return_relative_to_middle):
            cor_h += (img_shape[-1] - 1) / 2.0

        if return_validity:
            return cor_h, validity_check_result
        else:
            return cor_h


class CenterOfRotationAdaptiveSearch(CenterOfRotation):
    """This adaptive method works by applying a gaussian which highlights, by apodisation, a region
    which can possibly contain the good center of rotation.
    The whole image is spanned during several applications of the apodisation. At each application
    the apodisation function, which is a gaussian, is moved to a new guess position.
    The length of the step, by which the gaussian is moved, and its sigma are
    obtained by multiplying the shortest distance from the left or right border with
    a self.step_fraction and  self.sigma_fraction factors which ensure global overlapping.
    for each step a region around the CoR  of each image is selected, and the regions of the two images
    are compared to  calculate a cost function. The value of the cost function, at its minimum
    is used to select the best step at which the CoR is taken as final result.
    The option filtered_cost= True (default) triggers the filtering (according to low_pass and high_pass)
    of the two images which are used for he cost function. ( Note: the low_pass and high_pass options
    are used, if given, also without the filtered_cost option, by being passed to the base class
    CenterOfRotation )
    """

    sigma_fraction = 1.0 / 4.0
    step_fraction = 1.0 / 6.0

    def find_shift(
        self,
        img_1: np.ndarray,
        img_2: np.ndarray,
        side=None,
        roi_yxhw=None,
        median_filt_shape=None,
        padding_mode=None,
        high_pass=None,
        low_pass=None,
        margins=None,
        filtered_cost=True,
        return_validity=False,
        return_relative_to_middle=None,
    ):
        """Find the Center of Rotation (CoR), given two images.

        This method finds the half-shift between two opposite images, by
        means of correlation computed in Fourier space.
        A global search is done on on the detector span (minus a margin) without assuming centered scan conditions.

        Usage and parameters are the same as CenterOfRotation, except for the following parameters.

        Parameters
        ----------
        margins:  None or a couple of floats or ints
            if margins is None or in the form of  (margin1,margin2) the search is done between margin1 and  dim_x-1-margin2.
            If left to None then by default (margin1,margin2)  = ( 10, 10 ).
        filtered_cost: boolean.
            True by default. It triggers the use of filtered images in the calculation of the cost function.
        """
        # COMPAT.
        if return_relative_to_middle is None:
            deprecation_warning(
                "The current default behavior is to return the shift relative the the middle of the image. In a future release, this function will return the shift relative to the left-most pixel. To keep the current behavior, please use 'return_relative_to_middle=True'.",
                do_print=True,
                func_name="CenterOfRotationAdaptiveSearch.find_shift",
            )
            return_relative_to_middle = True  # the kwarg above will be False by default in a future release
        # ---

        if side is not None:
            self.logger.error("CenterOfRotationOctaveAccurate: the 'side' keyword argument will have no effect")

        validity_check_result = cor_result_validity["unknown"]

        self._check_img_pair_sizes(img_1, img_2)

        used_type = img_1.dtype

        roi_yxhw = self._determine_roi(img_1.shape, roi_yxhw)

        if filtered_cost and (low_pass is not None or high_pass is not None):
            img_filter = fourier_filters.get_bandpass_filter(
                img_1.shape[-2:],
                cutoff_lowpass=low_pass,
                cutoff_highpass=high_pass,
                use_rfft=True,
                data_type=self.data_type,
            )
            # fft2 and iff2 use axes=(-2, -1) by default
            img_filtered_1 = local_ifftn(local_fftn(img_1, axes=(-2, -1)) * img_filter, axes=(-2, -1)).real
            img_filtered_2 = local_ifftn(local_fftn(img_2, axes=(-2, -1)) * img_filter, axes=(-2, -1)).real
        else:
            img_filtered_1 = img_1
            img_filtered_2 = img_2

        img_1 = self._prepare_image(img_1, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape)
        img_2 = self._prepare_image(img_2, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape)

        img_filtered_1 = self._prepare_image(img_filtered_1, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape)
        img_filtered_2 = self._prepare_image(img_filtered_2, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape)

        dim_radio = img_1.shape[1]

        if margins is None:
            lim_1, lim_2 = 10, dim_radio - 1 - 10
        else:
            lim_1, lim_2 = margins
            lim_2 = dim_radio - 1 - lim_2

        if lim_1 < 1:
            lim_1 = 1
        if lim_2 > dim_radio - 2:
            lim_2 = dim_radio - 2

        if lim_2 <= lim_1:
            message = (
                "Image shape or cropped selection too small for global search. After removal of the margins the search limits collide."
                + " The cropped size is %d\n" % (dim_radio)
            )
            raise ValueError(message)

        found_centers = []
        x_cor = lim_1
        while x_cor < lim_2:
            tmp_sigma = (
                min(
                    (img_1.shape[1] - x_cor),
                    (x_cor),
                )
                * self.sigma_fraction
            )

            tmp_x = (np.arange(img_1.shape[1]) - x_cor) / tmp_sigma
            apodis = np.exp(-tmp_x * tmp_x / 2.0)

            x_cor_rel = x_cor - (img_1.shape[1] // 2)

            img_1_apodised = img_1 * apodis

            try:
                cor_position = CenterOfRotation.find_shift(
                    self,
                    img_1_apodised.astype(used_type),
                    img_2.astype(used_type),
                    low_pass=low_pass,
                    high_pass=high_pass,
                    roi_yxhw=roi_yxhw,
                    return_relative_to_middle=True,
                )
            except ValueError as err:
                if "positions are outside the input margins" in str(err):
                    x_cor = min(x_cor + x_cor * self.step_fraction, x_cor + (dim_radio - x_cor) * self.step_fraction)
                    continue
            except Exception as err:
                self.logger.error(
                    "Unexpected error from base class CenterOfRotation.find_shift in CenterOfRotationAdaptiveSearch.find_shift: %s"
                    % (str(err))
                )
                raise

            p_1 = cor_position * 2
            if cor_position < 0:
                p_2 = img_2.shape[1] + cor_position * 2
            else:
                p_2 = -img_2.shape[1] + cor_position * 2

            if abs(x_cor_rel - p_1 / 2) < abs(x_cor_rel - p_2 / 2):
                cor_position = p_1 / 2
            else:
                cor_position = p_2 / 2

            cor_in_img = img_1.shape[1] // 2 + cor_position
            tmp_sigma = (
                min(
                    (img_1.shape[1] - cor_in_img),
                    (cor_in_img),
                )
                * self.sigma_fraction
            )

            M1 = round(cor_position + img_1.shape[1] // 2) - round(tmp_sigma)
            M2 = round(cor_position + img_1.shape[1] // 2) + round(tmp_sigma)

            piece_1 = img_filtered_1[:, M1:M2]
            piece_2 = img_filtered_2[:, img_1.shape[1] - M2 : img_1.shape[1] - M1]

            if piece_1.size and piece_2.size:
                piece_1 = piece_1 - piece_1.mean()
                piece_2 = piece_2 - piece_2.mean()
                energy = np.array(piece_1 * piece_1 + piece_2 * piece_2, "d").sum()
                diff_energy = np.array((piece_1 - piece_2) * (piece_1 - piece_2), "d").sum()
                cost = diff_energy / energy

                if not np.isnan(cost) and tmp_sigma * 2 > abs(x_cor_rel - cor_position):
                    found_centers.append([cost, abs(x_cor_rel - cor_position), cor_position, energy])

            x_cor = min(x_cor + x_cor * self.step_fraction, x_cor + (dim_radio - x_cor) * self.step_fraction)

        if len(found_centers) == 0:
            message = f"Unable to find any valid CoR candidate in {self.__class__.__name__}.find_shift "
            raise ValueError(message)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Now build the neigborhood of the minimum as a list of five elements:
        # the minimum in the middle of the two before, and the two after

        filtered_found_centers = []
        for i in range(len(found_centers)):
            # ruff: noqa: SIM102
            if i > 0:
                if abs(found_centers[i][2] - found_centers[i - 1][2]) < 0.5:
                    filtered_found_centers.append(found_centers[i])
                    continue
            if i + 1 < len(found_centers):
                if abs(found_centers[i][2] - found_centers[i + 1][2]) < 0.5:
                    filtered_found_centers.append(found_centers[i])
                    continue

        if len(filtered_found_centers) > 0:
            found_centers = filtered_found_centers

        min_choice = min(found_centers)
        index_min_choice = found_centers.index(min_choice)
        min_neighborood = [
            found_centers[i][2] if (i >= 0 and i < len(found_centers)) else math.nan
            for i in range(index_min_choice - 2, index_min_choice + 2 + 1)
        ]

        score_right = 0
        for i_pos in [3, 4]:
            if abs(min_neighborood[i_pos] - min_neighborood[2]) < 0.5:
                score_right += 1
            else:
                break

        score_left = 0
        for i_pos in [1, 0]:
            if abs(min_neighborood[i_pos] - min_neighborood[2]) < 0.5:
                score_left += 1
            else:
                break

        if score_left + score_right >= 2:
            validity_check_result = cor_result_validity["sound"]
        else:
            self.logger.warning(
                "Minimum mean difference and minimum std-dev of differences do not coincide. This means that the validity of the found solution might be questionable."
            )
            validity_check_result = cor_result_validity["questionable"]

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # An informative message in case one wish to look at how it has gone
        informative_message = " ".join(
            ["CenterOfRotationAdaptiveSearch found this neighborood of the optimal position:"]
            + [str(t) if not math.isnan(t) else "N.A." for t in min_neighborood]
        )
        self.logger.debug(informative_message)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # The return value is the optimum which had been placed in the middle of the neighborood
        cor_position = min_neighborood[2]

        if not (return_relative_to_middle):
            cor_position += (img_1.shape[-1] - 1) / 2.0

        if return_validity:
            return cor_position, validity_check_result
        else:
            return cor_position

    __call__ = find_shift


class CenterOfRotationOctaveAccurate(CenterOfRotation):
    """This is a Python implementation of Octave/fastomo3/accurate COR estimator.
    The Octave 'accurate' function is renamed `local_correlation`.
    The Nabu standard `find_shift` has the same API as the other COR estimators (sliding, growing...)

    """

    def _cut(self, im, nrows, ncols, new_center_row=None, new_center_col=None):
        """Cuts a sub-matrix out of a larger matrix.
        Cuts in the center of the original matrix, except if new center is specified
        NO CHECKING of validity indices sub-matrix!

        Parameters
        ----------
        im : array.
            Original matrix
        nrows : int
            Number of rows in the output matrix.
        ncols : int
            Number of columns in the output matrix.
        new_center_row : int
            Index of center row around which to cut (default: None, i.e. center)
        new_center_col : int
            Index of center column around which to cut (default: None, i.e. center)

        Returns
        -------
        nrows x ncols array.

        Examples
        --------
        im_roi = cut(im, 1024, 1024)                -> cut center 1024x1024 pixels
        im_roi = cut(im, 1024, 1024, 600.5, 700.5)  -> cut 1024x1024 pixels around pixels (600-601, 700-701)

        Author: P. Cloetens <cloetens@esrf.eu>
        2023-11-06 J. Lesaint <jerome.lesaint@esrf.fr>

        * See octave-archive for the original Octave code.
        * 2023-11-06: Python implementation. Comparison seems OK.
        """
        [n, m] = im.shape
        if new_center_row is None:
            new_center_row = (n + 1) / 2
        if new_center_col is None:
            new_center_col = (m + 1) / 2

        rb = int(np.round(0.5 + new_center_row - nrows / 2))
        rb = int(np.round(new_center_row - nrows / 2))
        re = int(nrows + rb)
        cb = int(np.round(0.5 + new_center_col - ncols / 2))
        cb = int(np.round(new_center_col - ncols / 2))
        ce = int(ncols + cb)

        return im[rb:re, cb:ce]

    def _checkifpart(self, rapp, rapp_hist):
        res = 0
        for k in range(rapp_hist.shape[0]):
            if np.allclose(rapp, rapp_hist[k, :]):
                res = 1
                return res
        return res

    def _interpolate(self, input_, shift, mode="mean", interpolation_method="linear"):
        """Applies to the input a translation by a vector `shift`. Based on
        `scipy.ndimage.affine_transform` function.
        JL: This Octave function was initially used in the refine clause of the local_correlation (Octave find_shift).
        Since find_shift is always called with refine=False in Octave, refine is not implemented (see local_interpolation())
        and this function becomes useless.

        Parameters
        ----------
        input_ : array
            Array to which the translation is applied.
        shift : tuple, list or array of length 2.
        mode : str
            Type of padding applied to the unapplicable areas of the output image.
            Default `mean` is a constant padding with the mean of the input array.
            `mode` must belong to 'reflect', 'grid-mirror', 'constant', 'grid-constant', 'nearest', 'mirror', 'grid-wrap', 'wrap'
            See `scipy.ndimage.affine_transform` for details.
        interpolation_method : str or int.
            The interpolation is based on spline interpolation.
            Either 0, 1, 2, 3, 4 or 5: order of the spline interpolation functions.
            Or one among 'linear','cubic','pchip','nearest','spline' (Octave legacy).
                'nearest' is equivalent to 0
                'linear' is equivalent to 1
                'cubic','pchip','spline' are equivalent to 3.
        """
        admissible_modes = (
            "reflect",
            "grid-mirror",
            "constant",
            "grid-constant",
            "nearest",
            "mirror",
            "grid-wrap",
            "wrap",
        )
        admissible_interpolation_methods = ("linear", "cubic", "pchip", "nearest", "spline")

        from scipy.ndimage import affine_transform

        [s0, s1] = shift
        matrix = np.zeros([2, 3], dtype=float)
        matrix[0, 0] = 1.0
        matrix[1, 1] = 1.0
        matrix[:, 2] = [-s0, -s1]  # JL: due to transf. convention diff in Octave and scipy (push fwd vs pull back)

        if interpolation_method == "nearest":
            order = 0
        elif interpolation_method == "linear":
            order = 1
        elif interpolation_method in ("pchip", "cubic", "spline"):
            order = 3
        elif interpolation_method in (0, 1, 2, 3, 4, 5):
            order = interpolation_method
        else:
            raise ValueError(
                f"Interpolation method is {interpolation_method} and should either an integer between 0 (inc.) and 5 (inc.) or in {admissible_interpolation_methods}."
            )

        if mode == "mean":
            mode = "constant"
            cval = input_.mean()
            return affine_transform(input_, matrix, mode=mode, order=order, cval=cval)
        elif mode not in admissible_modes:
            raise ValueError(f"Pad method is {mode} and should be in {admissible_modes}.")

        return affine_transform(input_, matrix, mode=mode, order=order)

    def _local_correlation(
        self,
        z1,
        z2,
        maxsize=5,
        cor_estimate=0,
        refine=None,
        pmcc=False,
        normalize=True,
    ):
        """Returns the 2D shift in pixels between two images.
        It looks for a local optimum around the initial shift cor_estimate
        and within a window 'maxsize'.
        It uses variance of the difference of the normalized images or PMCC
        It adapts the shift estimate in case optimum is at the edge of the window
        If 'maxsize' is set to 0, it will only use approximate shift (+ refine possibly)
        Set 'cor_estimate' to allow for the use of any initial shift estimation.

        When not successful (stuck in loop or edge reached), returns [nan nan]
        Positive values corresponds to moving z2 to higher values of the index
        to compensate drift: interpolate(f)(z2, row, column)

        Parameters
        ----------
        z1,z2 : 2D arrays.
            The two (sub)images to be compared.

        maxsize : 5
            Size of the (horizontal) search window.

        cor_estimate:
            Initial guess of the center of rotation.

        refine: Boolean or None (default is None)
            Wether the initial guess should be refined of not.

        pmcc: Boolean (default is False)
            Use Pearson correlation coefficient  i.o. variance.

        normalize: Boolean (default is True)
            Set mean of each image to 1 if True.

        Returns
        -------
        c = cor (or [NaN,NaN] if unsuccessful.)

        2007-01-05 P. Cloetens cloetens@esrf.eu
        * Initial revision
        2023-11-10 J. Lesaint jerome.lesaint@esrf.fr
        * Python conversion.
        """

        if maxsize in ([], None, ""):
            maxsize = 5

        if refine is None:
            refine = np.allclose(maxsize, 0.0)

        if normalize:
            z1 /= np.mean(z1)
            z2 /= np.mean(z2)

        # check if refinement with realspace correlation is required
        # otherwise keep result as it is
        if np.allclose(maxsize, 0):
            shiftfound = 1
            if refine:
                c = np.round(cor_estimate)
            else:
                c = cor_estimate
        else:
            shiftfound = 0
            cor_estimate = np.round(cor_estimate)

        rapp_hist = []
        if np.sum(np.abs(cor_estimate) + 1 >= z1.shape[1]):
            self.logger.debug(f"Approximate shift of [{cor_estimate[0]},{cor_estimate[1]}] is too large, setting [0 0]")
            cor_estimate = 0
        maxsize = np.minimum(maxsize, np.floor((z1.shape[1] - 1) / 2)).astype(int)
        maxsize = int(np.minimum(maxsize, z1.shape[1] - np.abs(cor_estimate) - 1))

        while not shiftfound:
            # Set z1 region
            # Rationale: the (shift[0]+maxsize[0]:,shift[1]+maxsize[1]:) block of z1 should match
            # the (maxsize[0]:,maxisze[1]:)-upper-left corner of z2.
            # We first extract this z1 block.
            # Then, take moving z2-block according to maxsize.
            # Of course, care must be taken with borders, hence the various max,min calls.

            # Extract the reference block
            # shape_ar = np.array(z1.shape)
            shape_x = z1.shape[1]
            # cor_ar = np.array(cor_estimate)
            cor = cor_estimate
            # maxsize_ar = np.array(maxsize)

            # z1beg = np.maximum(cor_ar + maxsize_ar, np.zeros(2, dtype=int))
            z1beg = np.maximum(cor + maxsize, 0)
            # z1end = shape_ar + np.minimum(cor_ar - maxsize_ar, np.zeros(2, dtype=int))
            z1end = z1.shape[1] + np.minimum(cor - maxsize, 0)

            z1p = z1[:, z1beg:z1end].flatten()

            # Build local correlations array.
            window_shape = 2 * int(maxsize) + 1
            cc = np.zeros(window_shape)

            # Prepare second block indices
            # z2beg = (cor_ar + maxsize_ar > 0) * cc.shape + (cor_ar + maxsize_ar <= 0) * (shape_ar - z1end + z1beg) - 1
            z2beg = (cor + maxsize > 0) * window_shape + (cor + maxsize <= 0) * (shape_x - z1end + z1beg) - 1
            z2end = z2beg + z1end - z1beg

            if pmcc:
                std_z1p = z1p.std()
            if normalize:
                z1p /= z1p.mean()

            for l in range(len(cc)):  # noqa: E741
                if pmcc:
                    z2p = z2[:, z2beg - l : z2end - l].flatten()
                    std_z2p = z2p.std()
                    cc[l] = -np.cov(z1p, z2p, rowvar=True)[1, 0] / (std_z1p * std_z2p)
                else:
                    if normalize:
                        z2p = z2[:, z2beg - l : z2end - l].flatten()
                        z2p /= z2p.mean()
                        z2p -= z1p
                    else:
                        z2p = z2[:, z2beg - l : z2end - l].flatten()
                        z2p -= z1p
                    cc[l] = ((z2p - z2p.mean()) ** 2).sum()

            c = np.argmin(cc)
            (f_vals, _) = self.extract_peak_regions_1d(-cc, peak_radius=1)
            win_pos_max, _ = self.refine_max_position_1d(f_vals, return_vertex_val=True)

            c = float(np.argmin(cc)) + win_pos_max

            shiftfound = True

            c += z1beg - z2beg

            rapp_hist = []
            if not shiftfound:
                cor_estimate = c
                # Check that new shift estimate was not already done (avoid eternal loop)
                if self._checkifpart(cor_estimate, rapp_hist):
                    self.logger.debug("Stuck in loop?")
                    refine = True
                    shiftfound = True
                    c = np.nan
                else:
                    rapp_hist.append(cor_estimate)
                    self.logger.debug(f"Changing shift estimate: {cor_estimate}")
                    maxsize = np.minimum(maxsize, z1.shape[1] - np.abs(cor_estimate) - 1).astype(int)
                    if maxsize == 0:
                        self.logger.debug("Edge of image reached")
                        refine = False
                        shiftfound = True
                        c = np.nan
            elif len(rapp_hist) > 0:
                self.logger.debug("\n")

        return c

    def find_shift(
        self,
        img_1,
        img_2,
        side=None,
        roi_yxhw=None,
        median_filt_shape=None,
        padding_mode=None,
        low_pass=0.01,
        high_pass=None,
        maxsize=5,
        refine=None,
        pmcc=False,
        normalize=True,
        limz=0.5,
        return_relative_to_middle=None,
    ):
        # COMPAT.
        if return_relative_to_middle is None:
            deprecation_warning(
                "The current default behavior is to return the shift relative the the middle of the image. In a future release, this function will return the shift relative to the left-most pixel. To keep the current behavior, please use 'return_relative_to_middle=True'.",
                do_print=True,
                func_name="CenterOfRotationOctaveAccurate.find_shift",
            )
            return_relative_to_middle = True  # the kwarg above will be False by default in a future release
        # ---

        if side is not None:
            self.logger.error("CenterOfRotationOctaveAccurate: the 'side' keyword argument will have no effect")

        self._check_img_pair_sizes(img_1, img_2)

        img_shape = img_2.shape
        roi_yxhw = self._determine_roi(img_shape, roi_yxhw)

        img_1 = self._prepare_image(img_1, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape)
        img_2 = self._prepare_image(img_2, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape)

        cc = self._compute_correlation_fft(
            img_1,
            img_2,
            padding_mode,
            axes=(-1,),
            high_pass=high_pass,
            low_pass=low_pass,
        )

        # We use fftshift to deal more easily with negative shifts.
        # This has a cost of subtracting half the image shape afterward.
        shift = int(np.argmax(np.fft.fftshift(cc).sum(axis=0)))
        shift -= img_shape[1] // 2

        # Limit the size of region for comparison to cutsize in both directions.
        # Hard-coded?
        cutsize = img_shape[1] // 2
        oldshift = np.round(shift).astype(int)
        if (img_shape[0] > cutsize) or (img_shape[1] > cutsize):
            im0 = self._cut(img_1, min(img_shape[0], cutsize), min(img_shape[1], cutsize))
            im1 = self._cut(np.roll(img_2, oldshift, axis=(1,)), min(img_shape[0], cutsize), min(img_shape[1], cutsize))
            shift = oldshift + self._local_correlation(
                im0,
                im1,
                maxsize=maxsize,
                refine=refine,
                pmcc=pmcc,
                normalize=normalize,
            )
        else:
            shift = self._local_correlation(
                img_1,
                img_2,
                maxsize=maxsize,
                cor_estimate=oldshift,
                refine=refine,
                pmcc=pmcc,
                normalize=normalize,
            )
        if (shift - oldshift) ** 2 > 4:
            self.logger.warning(
                f"Pre-correlation ({oldshift}) and accurate correlation ({shift}) are not consistent. Please check !"
            )

        offset = shift / 2

        self.logger.debug(f"Offset?: {offset} pixels.")

        if not (return_relative_to_middle):
            offset += (img_shape[1] - 1) / 2

        return offset


# COMPAT.
from .cor_sino import CenterOfRotationFourierAngles as CenterOfRotationFourierAngles0

CenterOfRotationFourierAngles = deprecated_class(
    "CenterOfRotationFourierAngles was moved to nabu.estimation.cor_sino", do_print=True
)(CenterOfRotationFourierAngles0)
#
