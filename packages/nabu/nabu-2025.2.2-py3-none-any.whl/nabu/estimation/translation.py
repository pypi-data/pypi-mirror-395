import numpy as np
from numpy.polynomial.polynomial import Polynomial, polyval
from scipy import fft

from ..utils import calc_padding_lengths, deprecation_warning
from .alignment import AlignmentBase, plt


class DetectorTranslationAlongBeam(AlignmentBase):
    def find_shift(
        self,
        img_stack: np.ndarray,
        img_pos: np.array,
        roi_yxhw=None,
        median_filt_shape=None,
        padding_mode=None,
        peak_fit_radius=1,
        high_pass=None,
        low_pass=None,
        return_shifts=False,
        use_adjacent_imgs=False,
    ):
        """Find the vertical and horizontal shifts for translations of the
        detector along the beam direction.

        These shifts are in pixels-per-unit-translation, and they are due to
        the misalignment of the translation stage, with respect to the beam
        propagation direction.

        To compute the vertical and horizontal tilt angles from the obtained `shift_pix`:

        >>> tilt_deg = np.rad2deg(np.arctan(shift_pix * pixel_size))

        where `pixel_size` and and the input parameter `img_pos` have to be
        expressed in the same units.

        Parameters
        ----------
        img_stack: numpy.ndarray
            A stack of images (usually 4) at different distances
        img_pos: numpy.ndarray
            Position of the images along the translation axis
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
            Low-pass filter properties, as described in `nabu.misc.fourier_filters`.
        high_pass: float or sequence of two floats
            High-pass filter properties, as described in `nabu.misc.fourier_filters`.
        return_shifts: boolean, optional
            Adds a third returned argument, containing the pixel shifts of each
            image with respect to the first one in the stack. Defaults to False.
        use_adjacent_imgs: boolean, optional
            Compute correlation between adjacent images.
            It can be used when dealing with large shifts, to avoid overflowing the shift.
            This option allows to replicate the behavior of the reference function `alignxc.m`
            However, it is detrimental to shift fitting accuracy. Defaults to False.

        Returns
        -------
        coeff_v: float
            Estimated vertical shift in pixel per unit-distance of the detector translation.
        coeff_h: float
            Estimated horizontal shift in pixel per unit-distance of the detector translation.
        shifts_vh: list, optional
            The pixel shifts of each image with respect to the first image in the stack.
            Activated if return_shifts is True.

        Examples
        --------
        The following example creates a stack of shifted images, and retrieves the computed shift.
        Here we use a high-pass filter, due to the presence of some low-frequency noise component.

        >>> import numpy as np
        ... import scipy as sp
        ... import scipy.ndimage
        ... from nabu.preproc.alignment import  DetectorTranslationAlongBeam
        ...
        ... tr_calc = DetectorTranslationAlongBeam()
        ...
        ... stack = np.zeros([4, 512, 512])
        ...
        ... # Add low frequency spurious component
        ... for i in range(4):
        ...     stack[i, 200 - i * 10, 200 - i * 10] = 1
        ... stack = sp.ndimage.filters.gaussian_filter(stack, [0, 10, 10.0]) * 100
        ...
        ... # Add the feature
        ... x, y = np.meshgrid(np.arange(stack.shape[-1]), np.arange(stack.shape[-2]))
        ... for i in range(4):
        ...     xc = x - (250 + i * 1.234)
        ...     yc = y - (250 + i * 1.234 * 2)
        ...     stack[i] += np.exp(-(xc * xc + yc * yc) * 0.5)
        ...
        ... # Image translation along the beam
        ... img_pos = np.arange(4)
        ...
        ... # Find the shifts from the features
        ... shifts_v, shifts_h = tr_calc.find_shift(stack, img_pos, high_pass=1.0)
        ... print(shifts_v, shifts_h)
        >>> ( -2.47 , -1.236 )

        and the following commands convert the shifts in angular tilts:

        >>> tilt_v_deg = np.rad2deg(np.arctan(shifts_v * pixel_size))
        >>> tilt_h_deg = np.rad2deg(np.arctan(shifts_h * pixel_size))

        To enable the legacy behavior of `alignxc.m` (correlation between adjacent images):

        >>> shifts_v, shifts_h = tr_calc.find_shift(stack, img_pos, use_adjacent_imgs=True)

        To plot the correlation shifts and the fitted straight lines for both directions:

        >>> tr_calc = DetectorTranslationAlongBeam(verbose=True)
        ... shifts_v, shifts_h = tr_calc.find_shift(stack, img_pos)
        """
        self._check_img_stack_size(img_stack, img_pos)

        if peak_fit_radius < 1:
            self.logger.warning("Parameter peak_fit_radius should be at least 1, given: %d instead." % peak_fit_radius)
            peak_fit_radius = 1

        num_imgs = img_stack.shape[0]
        img_shape = img_stack.shape[-2:]
        roi_yxhw = self._determine_roi(img_shape, roi_yxhw)

        img_stack = self._prepare_image(img_stack, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape)

        # do correlations
        ccs = [
            self._compute_correlation_fft(
                img_stack[ii - 1 if use_adjacent_imgs else 0, ...],
                img_stack[ii, ...],
                padding_mode,
                high_pass=high_pass,
                low_pass=low_pass,
            )
            for ii in range(1, num_imgs)
        ]

        img_shape = ccs[0].shape  # cc.shape can differ from img.shape, e.g. in case of odd number of cols.
        cc_vs = np.fft.fftfreq(img_shape[-2], 1 / img_shape[-2])
        cc_hs = np.fft.fftfreq(img_shape[-1], 1 / img_shape[-1])

        shifts_vh = np.zeros((num_imgs, 2))
        for ii, cc in enumerate(ccs):
            (f_vals, fv, fh) = self.extract_peak_region_2d(cc, peak_radius=peak_fit_radius, cc_vs=cc_vs, cc_hs=cc_hs)
            shifts_vh[ii + 1, :] = self.refine_max_position_2d(f_vals, fv, fh)

        if use_adjacent_imgs:
            shifts_vh = np.cumsum(shifts_vh, axis=0)

        # Polynomial.fit is supposed to be more numerically stable than polyfit
        # (according to numpy)
        coeffs_v = Polynomial.fit(img_pos, shifts_vh[:, 0], deg=1).convert().coef
        coeffs_h = Polynomial.fit(img_pos, shifts_vh[:, 1], deg=1).convert().coef
        # In some cases (singular matrix ?) the output is [0] while in some other its [eps, eps].
        if len(coeffs_v) == 1:
            coeffs_v = np.array([coeffs_v[0], coeffs_v[0]])
        if len(coeffs_h) == 1:
            coeffs_h = np.array([coeffs_h[0], coeffs_h[0]])

        if self.verbose:
            self.logger.info(
                "Fitted pixel shifts per unit-length: vertical = %f, horizontal = %f" % (coeffs_v[1], coeffs_h[1])
            )
            f, axs = plt.subplots(1, 2)
            self._add_plot_window(f, ax=axs)
            axs[0].scatter(img_pos, shifts_vh[:, 0])
            axs[0].plot(img_pos, polyval(img_pos, coeffs_v), "-C1")
            axs[0].set_title("Vertical shifts")
            axs[1].scatter(img_pos, shifts_vh[:, 1])
            axs[1].plot(img_pos, polyval(img_pos, coeffs_h), "-C1")
            axs[1].set_title("Horizontal shifts")
            plt.show(block=False)

        if return_shifts:
            return coeffs_v[1], coeffs_h[1], shifts_vh
        else:
            return coeffs_v[1], coeffs_h[1]


class OppositeImages2DRegistrationOctaveAccurate(AlignmentBase):
    """This is a Python implementation of Octave/fastomo3/accurate COR estimator.
    The Octave 'accurate' function is renamed `local_correlation`.
    The Nabu standard `find_shift` has the same API as the other COR estimators (sliding, growing...)
    Note that this estimator returns a 2d estimation of the shift between the 2 input images.
    If you need only the COR estimation, see estimation.cor.CenterOfRotationOctaveAccurate.
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
        maxsize=(5, 5),
        cor_estimate=(0, 0),
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

        maxsize : 2-list. Default [5,5]
            Size of the search window.

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
        c = [row,column] (or [NaN,NaN] if unsuccessful.)

        2007-01-05 P. Cloetens cloetens@esrf.eu
        * Initial revision
        2023-11-10 J. Lesaint jerome.lesaint@esrf.fr
        * Python conversion.
        """

        if type(maxsize) in (float, int):
            maxsize = [int(maxsize), int(maxsize)]
        elif type(maxsize) in (tuple, list):
            maxsize = [int(maxsize[0]), int(maxsize[1])]
        elif maxsize in ([], None, ""):
            maxsize = [5, 5]

        if refine is None:
            refine = np.allclose(maxsize, 0.0)

        if normalize:
            z1 /= np.mean(z1)
            z2 /= np.mean(z2)

        #####################################
        # JL : seems useless since func is always called with a first approximate.
        ## determination of approximative shift (manually or Fourier correlation)
        # if isinstance(cor_estimate,str):
        #    if cor_estimate in ('fft','auto','fourier'):
        #        padding_mode = None
        #        cor_estimate = self._compute_correlation_fft(
        #            z1,
        #            z2,
        #            padding_mode,
        #            high_pass=self.high_pass,
        #            low_pass=self.low_pass
        #        )
        #    elif cor_estimate in ('manual','man','m'):
        #        cor_estimate = None
        #        # No ImageJ plugin here :
        #        # rapp = ij_align(z1,z2)

        ####################################
        # check if refinement with realspace correlation is required
        # otherwise keep result as it is
        if np.allclose(maxsize, 0):
            shiftfound = 1
            if refine:
                c = np.round(np.array(cor_estimate, dtype=int))
            else:
                c = np.array(cor_estimate, dtype=int)
        else:
            shiftfound = 0
            cor_estimate = np.round(np.array(cor_estimate, dtype=int))

        rapp_hist = []
        if np.sum(np.abs(cor_estimate) + 1 >= z1.shape):
            self.logger.debug(f"Approximate shift of [{cor_estimate[0]},{cor_estimate[1]}] is too large, setting [0 0]")
            cor_estimate = np.array([0, 0])
        maxsize = np.minimum(maxsize, np.floor((np.array(z1.shape) - 1) / 2)).astype(int)
        maxsize = np.minimum(maxsize, np.array(z1.shape) - np.abs(cor_estimate) - 1).astype(int)

        while not shiftfound:
            # Set z1 region
            # Rationale: the (shift[0]+maxsize[0]:,shift[1]+maxsize[1]:) block of z1 should match
            # the (maxsize[0]:,maxisze[1]:)-upper-left corner of z2.
            # We first extract this z1 block.
            # Then, take moving z2-block according to maxsize.
            # Of course, care must be taken with borders, hence the various max,min calls.

            # Extract the reference block
            shape_ar = np.array(z1.shape)
            cor_ar = np.array(cor_estimate)
            maxsize_ar = np.array(maxsize)

            z1beg = np.maximum(cor_ar + maxsize_ar, np.zeros(2, dtype=int))
            z1end = shape_ar + np.minimum(cor_ar - maxsize_ar, np.zeros(2, dtype=int))

            z1p = z1[z1beg[0] : z1end[0], z1beg[1] : z1end[1]].flatten()

            # Build local correlations array.
            window_shape = (2 * int(maxsize[0]) + 1, 2 * int(maxsize[1]) + 1)
            cc = np.zeros(window_shape)

            # Prepare second block indices
            z2beg = (cor_ar + maxsize_ar > 0) * cc.shape + (cor_ar + maxsize_ar <= 0) * (shape_ar - z1end + z1beg) - 1
            z2end = z2beg + z1end - z1beg

            if pmcc:
                std_z1p = z1p.std()
            if normalize == 2:
                z1p /= z1p.mean()

            for k in range(cc.shape[0]):
                for l in range(cc.shape[1]):  # noqa: E741
                    if pmcc:
                        z2p = z2[z2beg[0] - k : z2end[0] - k, z2beg[1] - l : z2end[1] - l].flatten()
                        std_z2p = z2p.std()
                        cc[k, l] = -np.cov(z1p, z2p, rowvar=True)[1, 0] / (std_z1p * std_z2p)
                    else:
                        if normalize == 2:
                            z2p = z2[z2beg[0] - k : z2end[0] - k, z2beg[1] - l : z2end[1] - l].flatten()
                            z2p /= z2p.mean()
                            z2p -= z1p
                        else:
                            z2p = z2[z2beg[0] - k : z2end[0] - k, z2beg[1] - l : z2end[1] - l].flatten()
                            z2p -= z1p
                        cc[k, l] = ((z2p - z2p.mean()) ** 2).sum()
                        # cc(k,l) = std(z1p./z2(z2beg(1)-k:z2end(1)-k,z2beg(2)-l:z2end(2)-l)(:));

            c = np.unravel_index(np.argmin(cc, axis=None), shape=cc.shape)

            if not np.sum((c == 0) + (c == np.array(cc.shape) - 1)):
                # check that we are not at the edge of the region that was sampled
                x = np.array([-1, 0, 1])
                tmp = self.refine_max_position_2d(
                    cc[c[0] - 1 : c[0] + 2, c[1] - 1 : c[1] + 2], x, x, logger=self.logger
                )
                c += tmp
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
                    c = np.array([np.nan, np.nan])
                else:
                    rapp_hist.append(cor_estimate)
                    self.logger.debug(f"Changing shift estimate: {cor_estimate}")
                    maxsize = np.minimum(maxsize, np.array(z1.shape) - np.abs(cor_estimate) - 1).astype(int)
                    if (maxsize == 0).sum():
                        self.logger.debug("Edge of image reached")
                        refine = False
                        shiftfound = True
                        c = np.array([np.nan, np.nan])
            elif len(rapp_hist) > 0:
                self.logger.debug("\n")

        ####################################
        # refine result; useful when shifts are not integer values
        # JL: I don't understand why this refine step should be useful.
        # In Octave, from fastomo.m, refine is always set to False.
        # So this could be ignored.
        # I keep it for future use if it proves useful.
        # if refine:
        #    if debug:
        #        print('Refining solution ...')
        #    z2n = self.interpolate(z2,c)
        #    indices = np.ceil(np.abs(c)).astype(int)
        #    z1p = np.roll(z1,((c>0) * (-1) * indices),[0,1])
        #    z1p = z1p[1:-indices[0]-1,1:-indices[1]-1].flatten()
        #    z2n = np.roll(z2n,((c>0) * (-1) * indices),[0,1])
        #    z2n = z2n[:-indices[0],:-indices[1]]
        #    ccrefine = np.zeros([3,3])
        #    [n2,m2] = z2n.shape
        #    for k in range(3):
        #        for l in range(3):
        #            z2p = z1p - z2n[2-k:n2-k,2-l:m2-l].flatten()
        #            ccrefine[k,l] = ((z2p - z2p.mean())**2).sum()
        #    x = np.array([-1,0,1])
        #    crefine = self.refine_max_position_2d(ccrefine, x, x)
        #    #crefine = min2par(ccrefine)

        #    # Check if the refinement is effectively confined to subpixel
        #    if (np.abs(crefine) >= 1).sum():
        #        self.logger.info("Problems refining result\n")
        #    else:
        #        c += crefine

        return c

    def find_shift(
        self,
        img_1,
        img_2,
        side="center",
        roi_yxhw=None,
        median_filt_shape=None,
        padding_mode=None,
        low_pass=0.01,
        high_pass=None,
        maxsize=(5, 5),
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
        self._check_img_pair_sizes(img_1, img_2)

        img_shape = img_2.shape
        roi_yxhw = self._determine_roi(img_shape, roi_yxhw)

        img_1 = self._prepare_image(img_1, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape)
        img_2 = self._prepare_image(img_2, roi_yxhw=roi_yxhw, median_filt_shape=median_filt_shape)

        cc = self._compute_correlation_fft(
            img_1,
            img_2,
            padding_mode,
            high_pass=high_pass,
            low_pass=low_pass,
        )

        # We use fftshift to deal more easily with negative shifts.
        # This has a cost of subtracting half the image shape afterward.
        shift = np.unravel_index(np.argmax(np.fft.fftshift(cc)), img_shape)
        shift -= np.array(img_shape) // 2

        # The real "accurate" starts here (i.e. the octave findshift() func).
        if np.abs(shift[0]) > 10 * limz:
            # This is suspiscious. We don't trust results of correlate.
            self.logger.warning(f"Pre-correlation yields {shift[0]} pixels vertical motion")
            self.logger.warning("We do not consider it.")
            shift = (0, 0)

        # Limit the size of region for comparison to cutsize in both directions.
        # Hard-coded?
        cutsize = img_shape[1] // 2
        oldshift = np.round(shift).astype(int)
        if (img_shape[0] > cutsize) or (img_shape[1] > cutsize):
            im0 = self._cut(img_1, min(img_shape[0], cutsize), min(img_shape[1], cutsize))
            im1 = self._cut(
                np.roll(img_2, oldshift, axis=(0, 1)), min(img_shape[0], cutsize), min(img_shape[1], cutsize)
            )
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
        if ((shift - oldshift) ** 2).sum() > 4:
            self.logger.warning(f"Pre-correlation ({oldshift}) and accurate correlation ({shift}) are not consistent.")
            self.logger.warning("Please check!!!")

        offset = shift[1] / 2

        if np.abs(shift[0]) > limz:
            self.logger.debug("Verify alignment or sample motion.")
            self.logger.debug(f"Verical motion: {shift[0]} pixels.")
            self.logger.debug(f"Offset?: {offset} pixels.")
        else:
            self.logger.debug(f"Offset?: {offset} pixels.")

        if not (return_relative_to_middle):
            offset += (img_shape[1] - 1) / 2

        return shift


def _fft_pad(i, axes=None, padding_mode="constant"):
    pad_len = calc_padding_lengths(i.shape, np.array(i.shape) * 2)
    i_p = np.pad(i, pad_len, mode=padding_mode)
    return fft.fftn(i_p)


def estimate_shifts(im1, im2):
    """
    Simple implementation of shift estimation between two images, based on phase cross correlation.
    """
    pr = _fft_pad(im1) * _fft_pad(im2).conjugate()
    pr_n = pr / np.maximum(1e-7, np.abs(pr))
    corr = np.fft.fftshift(fft.ifftn(pr_n).real)
    argmax = np.array(np.unravel_index(np.argmax(corr), pr.shape))
    shp = np.array(pr.shape)
    argmax_refined = refine_parabola_2D(corr, argmax)
    argmax = argmax + argmax_refined
    return shp // 2 - np.array(argmax)


def refine_parabola_2D(im_vals, argmax):
    argmax = tuple(argmax)
    maxval = im_vals[argmax]
    ny, nx = im_vals.shape

    iy, ix = np.array(argmax, dtype=np.intp)
    ixm, ixp = (ix - 1) % nx, (ix + 1) % nx
    iym, iyp = (iy - 1) % ny, (iy + 1) % ny

    F = maxval
    A = (im_vals[iy, ixp] + im_vals[iy, ixm]) / 2 - F
    D = (im_vals[iy, ixp] - im_vals[iy, ixm]) / 2
    B = (im_vals[iyp, ix] + im_vals[iym, ix]) / 2 - F
    E = (im_vals[iyp, ix] - im_vals[iym, ix]) / 2
    C = (im_vals[iyp, ixp] - im_vals[iym, ixp] - im_vals[iyp, ixm] + im_vals[iym, ixm]) / 4
    det = C**2 - 4 * A * B
    dx = (2 * B * D - C * E) / det
    dy = (2 * A * E - C * D) / det
    dx = np.clip(dx, -0.5, 0.5)
    dy = np.clip(dy, -0.5, 0.5)
    return (dy, dx)
