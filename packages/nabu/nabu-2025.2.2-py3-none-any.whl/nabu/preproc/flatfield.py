import os
from multiprocessing.pool import ThreadPool
from bisect import bisect_left
import numpy as np
from tomoscan.io import HDF5File
from ..io.reader import load_images_from_dataurl_dict
from ..utils import check_supported, deprecated_class, get_num_threads
from .ccd import CCDFilter


class FlatFieldArrays:
    """
    A class for flat-field normalization
    """

    # the variable below will be True for the derived class
    # which is taylored for to helical case
    _full_shape = False

    _supported_interpolations = ["linear", "nearest"]

    def __init__(
        self,
        radios_shape: tuple,
        flats,
        darks,
        radios_indices=None,
        interpolation: str = "linear",
        distortion_correction=None,
        nan_value=1.0,
        radios_srcurrent=None,
        flats_srcurrent=None,
        n_threads=None,
    ):
        """
        Initialize a flat-field normalization process.

        Parameters
        ----------
        radios_shape: tuple
            A tuple describing the shape of the radios stack, in the form
            `(n_radios, n_z, n_x)`.
        flats: dict
            Dictionary where each key is the flat index, and the value is a
            numpy.ndarray of the flat image.
        darks: dict
            Dictionary where each key is the dark index, and the value is a
            numpy.ndarray of the dark image.
        radios_indices: array of int, optional
            Array containing the radios indices in the scan. `radios_indices[0]` is the index
            of the first radio, and so on.
        interpolation: str, optional
            Interpolation method for flat-field. See below for more details.
        distortion_correction: DistortionCorrection, optional
            A DistortionCorrection object. If provided, it is used to correct flat distortions based on each radio.
        nan_value: float, optional
            Which float value is used to replace nan/inf after flat-field.
        radios_srcurrent: array, optional
            Array with the same shape as radios_indices. Each item contains the synchrotron electric current.
            If not None, normalization with current is applied.
            Please refer to "Notes" for more information on this normalization.
        flats_srcurrent: array, optional
            Array with the same length as "flats". Each item is a measurement of the synchrotron electric current
            for the corresponding flat. The items must be ordered in the same order as the flats indices (`flats.keys()`).
            This parameter must be used along with 'radios_srcurrent'.
            Please refer to "Notes" for more information on this normalization.
        n_threads: int or None, optional
            Number of threads to use for flat-field correction. Default is to use half the threads.

        Important
        ----------
        `flats` and `darks` are expected to be a dictionary with integer keys (the flats/darks indices)
        and numpy array values.
        You can use the following helper functions: `nabu.io.reader.load_images_from_dataurl_dict`
        and `nabu.io.utils.create_dict_of_indices`


        Notes
        ------
        Usually, when doing a scan, only one or a few darks/flats are acquired.
        However, the flat-field normalization has to be performed on each radio,
        although incoming beam can fluctuate between projections.
        The usual way to overcome this is to interpolate between flats.
        If interpolation="nearest", the first flat is used for the first
        radios subset, the second flat is used for the second radios subset,
        and so on.
        If interpolation="linear", the normalization is done as a linear
        function of the radio index.

        The normalization with synchrotron electric current is done as follows.
        Let s = sr/sr_max denote the ratio between current and maximum current,
        D be the dark-current frame, and X' be the normalized frame. Then:
          srcurrent_normalization(X) = X' = (X - D)/s + D
          flatfield_normalization(X') = (X' - D)/(F' - D) = (X - D) / (F - D) * sF/sX
        So current normalization boils down to a scalar multiplication after flat-field.
        """
        if self._full_shape:  # noqa: SIM102
            # this is never going to happen in this base class. But in the derived class for helical
            # which needs to keep the full shape
            if radios_indices is not None:
                radios_shape = (len(radios_indices),) + radios_shape[1:]

        self._set_parameters(radios_shape, radios_indices, interpolation, nan_value)
        self._set_flats_and_darks(flats, darks)
        self._precompute_flats_indices_weights()
        self._configure_srcurrent_normalization(radios_srcurrent, flats_srcurrent)
        self.distortion_correction = distortion_correction
        self.n_threads = max(1, get_num_threads(n_threads) // 2)

    def _set_parameters(self, radios_shape, radios_indices, interpolation, nan_value):
        self._set_radios_shape(radios_shape)
        if radios_indices is None:
            radios_indices = np.arange(0, self.n_radios, dtype=np.int32)
        else:
            radios_indices = np.array(radios_indices, dtype=np.int32)
            self._check_radios_and_indices_congruence(radios_indices)

        self.radios_indices = radios_indices
        self.interpolation = interpolation
        check_supported(interpolation, self._supported_interpolations, "Interpolation mode")
        self.nan_value = nan_value
        self._radios_idx_to_pos = dict(zip(self.radios_indices, np.arange(self.radios_indices.size)))

    def _set_radios_shape(self, radios_shape):
        if len(radios_shape) == 2:
            self.radios_shape = (1,) + radios_shape
        elif len(radios_shape) == 3:
            self.radios_shape = radios_shape
        else:
            raise ValueError("Expected radios to have 2 or 3 dimensions")
        n_radios, n_z, n_x = self.radios_shape
        self.n_radios = n_radios
        self.n_angles = n_radios
        self.shape = (n_z, n_x)

    def _set_flats_and_darks(self, flats, darks):
        self._check_frames(flats, "flats", 1, 9999)
        self.n_flats = len(flats)
        self.flats = flats
        self._sorted_flat_indices = sorted(self.flats.keys())

        if self._full_shape:
            # this is never going to happen in this base class. But in the derived class for helical
            # which needs to keep the full shape
            self.shape = flats[self._sorted_flat_indices[0]].shape

        self._flat2arrayidx = dict(zip(self._sorted_flat_indices, np.arange(self.n_flats)))
        self.flats_arr = np.zeros((self.n_flats,) + self.shape, "f")
        for i, idx in enumerate(self._sorted_flat_indices):
            self.flats_arr[i] = self.flats[idx]

        self._check_frames(darks, "darks", 1, 1)
        self.darks = darks
        self.n_darks = len(darks)
        self._sorted_dark_indices = sorted(self.darks.keys())
        self._dark = None

    def _check_frames(self, frames, frames_type, min_frames_required, max_frames_supported):
        n_frames = len(frames)
        if n_frames < min_frames_required:
            raise ValueError("Need at least %d %s" % (min_frames_required, frames_type))
        if n_frames > max_frames_supported:
            raise ValueError(
                "Flat-fielding with more than %d %s is not supported" % (max_frames_supported, frames_type)
            )
        self._check_frame_shape(frames, frames_type)

    def _check_frame_shape(self, frames, frames_type):
        for frame_idx, frame in frames.items():
            if frame.shape != self.shape:
                raise ValueError(
                    "Invalid shape for %s %s: expected %s, but got %s"
                    % (frames_type, frame_idx, str(self.shape), str(frame.shape))
                )

    def _check_radios_and_indices_congruence(self, radios_indices):
        if radios_indices.size != self.n_radios:
            raise ValueError(
                "Expected radios_indices to have length %s = n_radios, but got length %d"
                % (self.n_radios, radios_indices.size)
            )

    def _precompute_flats_indices_weights(self):
        """
        Build two arrays: "indices" and "weights".
        These arrays contain pre-computed information so that the interpolated flat is obtained with

           flat_interpolated = weight_prev * flat_prev  + weight_next * flat_next

        where
           weight_prev, weight_next = weights[2*i], weights[2*i+1]
           idx_prev, idx_next = indices[2*i], indices[2*i+1]
           flat_prev, flat_next = flats[idx_prev], flats[idx_next]

        In words:
          - If a projection has an index between two flats, the equivalent flat is a linear interpolation
            between "previous flat" and "next flat".
          - If a projection has the same index as a flat, only this flat is used for normalization
            (this case normally never occurs, but it's handled in the code)
        """

        def _interp_linear(idx, prev_next):
            if len(prev_next) == 1:  # current index corresponds to an acquired flat
                weights = (1, 0)
                f_idx = (self._flat2arrayidx[prev_next[0]], -1)
            else:
                prev_idx, next_idx = prev_next
                delta = next_idx - prev_idx
                w1 = 1 - (idx - prev_idx) / delta
                w2 = 1 - (next_idx - idx) / delta
                weights = (w1, w2)
                f_idx = (self._flat2arrayidx[prev_idx], self._flat2arrayidx[next_idx])
            return f_idx, weights

        def _interp_nearest(idx, prev_next):
            if len(prev_next) == 1:  # current index corresponds to an acquired flat
                weights = (1, 0)
                f_idx = (self._flat2arrayidx[prev_next[0]], -1)
            else:
                prev_idx, next_idx = prev_next
                idx_to_take = prev_idx if abs(idx - prev_idx) < abs(idx - next_idx) else next_idx
                weights = (1, 0)
                f_idx = (self._flat2arrayidx[idx_to_take], -1)
            return f_idx, weights

        self.flats_idx = np.zeros((self.n_radios, 2), dtype=np.int32)
        self.flats_weights = np.zeros((self.n_radios, 2), dtype=np.float32)
        for i, idx in enumerate(self.radios_indices):
            prev_next = self.get_previous_next_indices(self._sorted_flat_indices, idx)
            if self.interpolation == "nearest":
                f_idx, weights = _interp_nearest(idx, prev_next)
            elif self.interpolation == "linear":
                f_idx, weights = _interp_linear(idx, prev_next)
            # pylint: disable=E0606
            self.flats_idx[i] = f_idx
            self.flats_weights[i] = weights

    # pylint: disable=E1307
    def _configure_srcurrent_normalization(self, radios_srcurrent, flats_srcurrent):
        self.normalize_srcurrent = False
        if radios_srcurrent is None or flats_srcurrent is None:
            return
        radios_srcurrent = np.array(radios_srcurrent)
        if radios_srcurrent.size != self.n_radios:
            raise ValueError(
                "Expected 'radios_srcurrent' to have %d elements but got %d" % (self.n_radios, radios_srcurrent.size)
            )
        flats_srcurrent = np.array(flats_srcurrent)
        if flats_srcurrent.size != self.n_flats:
            raise ValueError(
                "Expected 'flats_srcurrent' to have %d elements but got %d" % (self.n_flats, flats_srcurrent.size)
            )
        self.normalize_srcurrent = True
        self.radios_srcurrent = radios_srcurrent
        self.flats_srcurrent = flats_srcurrent
        self.srcurrent_ratios = np.zeros(self.n_radios, "f")
        # Flats SRCurrent is obtained with "nearest" interp, to emulate an already-done flats SR current normalization
        for i, radio_idx in enumerate(self.radios_indices):
            flat_idx = self.get_nearest_index(self._sorted_flat_indices, radio_idx)
            flat_srcurrent = self.flats_srcurrent[self._flat2arrayidx[flat_idx]]
            self.srcurrent_ratios[i] = flat_srcurrent / self.radios_srcurrent[i]

    @staticmethod
    def get_previous_next_indices(arr, idx):
        pos = bisect_left(arr, idx)
        if pos == len(arr):  # outside range
            return (arr[-1],)
        if arr[pos] == idx:
            return (idx,)
        if pos == 0:
            return (arr[0],)
        return arr[pos - 1], arr[pos]

    @staticmethod
    def get_nearest_index(arr, idx):
        pos = bisect_left(arr, idx)
        if pos == len(arr) or arr[pos] == idx:
            return arr[-1]
        return arr[pos - 1] if idx - arr[pos - 1] < arr[pos] - idx else arr[pos]

    @staticmethod
    def interp(pos, indices, weights, array, slice_y=slice(None, None), slice_x=slice(None, None)):
        """
        Interpolate between two values. The interpolator consists in pre-computed arrays such that

           prev, next = indices[pos]
           w1, w2 = weights[pos]
           interpolated_value = w1 * array[prev] + w2 * array[next]
        """
        prev_idx = indices[pos, 0]
        next_idx = indices[pos, 1]

        if slice_y != slice(None, None) or slice_x != slice(None, None):
            w1 = weights[pos, 0][slice_y, slice_x]
            w2 = weights[pos, 1][slice_y, slice_x]
        else:
            w1 = weights[pos, 0]
            w2 = weights[pos, 1]

        if next_idx == -1:
            val = array[prev_idx]
        else:
            val = w1 * array[prev_idx] + w2 * array[next_idx]
        return val

    def get_flat(self, pos, dtype=np.float32, slice_y=slice(None, None), slice_x=slice(None, None)):
        flat = self.interp(pos, self.flats_idx, self.flats_weights, self.flats_arr, slice_y=slice_y, slice_x=slice_x)
        if flat.dtype != dtype:
            flat = np.ascontiguousarray(flat, dtype=dtype)
        return flat

    def get_dark(self):
        if self._dark is None:
            first_dark_idx = self._sorted_dark_indices[0]
            dark = np.ascontiguousarray(self.darks[first_dark_idx], dtype=np.float32)
            self._dark = dark
        return self._dark

    def remove_invalid_values(self, img):
        if self.nan_value is None:
            return
        invalid_mask = np.logical_not(np.isfinite(img))
        img[invalid_mask] = self.nan_value

    def normalize_radios(self, radios):
        """
        Apply a flat-field normalization, with the current parameters, to a stack
        of radios.
        The processing is done in-place, meaning that the radios content is overwritten.

        Parameters
        -----------
        radios: numpy.ndarray
            Radios chunk
        """
        do_flats_distortion_correction = self.distortion_correction is not None
        dark = self.get_dark()

        def apply_flatfield(i):
            radio_data = radios[i]
            radio_data -= dark
            flat = self.get_flat(i)
            flat = flat - dark
            if do_flats_distortion_correction:
                flat = self.distortion_correction.estimate_and_correct(flat, radio_data)
            np.divide(radio_data, flat, out=radio_data)
            self.remove_invalid_values(radio_data)

        if self.n_threads > 2:
            with ThreadPool(self.n_threads) as tp:
                tp.map(apply_flatfield, range(self.n_radios))
        else:
            for i in range(self.n_radios):
                apply_flatfield(i)

        if self.normalize_srcurrent:
            radios *= self.srcurrent_ratios[:, np.newaxis, np.newaxis]
        return radios

    def normalize_single_radio(
        self, radio, radio_idx, dtype=np.float32, slice_y=slice(None, None), slice_x=slice(None, None)
    ):
        """
        Apply a flat-field normalization to a single projection image.
        """
        dark = self.get_dark()[slice_y, slice_x]
        radio -= dark
        radio_pos = self._radios_idx_to_pos[radio_idx]
        flat = self.get_flat(radio_pos, dtype=dtype, slice_y=slice_y, slice_x=slice_x)
        flat = flat - dark
        if self.distortion_correction is not None:
            flat = self.distortion_correction.estimate_and_correct(flat, radio)
        radio /= flat
        if self.normalize_srcurrent:
            radio *= self.srcurrent_ratios[radio_pos]
        self.remove_invalid_values(radio)
        return radio


FlatField = FlatFieldArrays


@deprecated_class(
    "FlatFieldDataUrls is deprecated since 2024.2.0 and will be removed in a future version", do_print=True
)
class FlatFieldDataUrls(FlatField):
    def __init__(
        self,
        radios_shape: tuple,
        flats: dict,
        darks: dict,
        radios_indices=None,
        interpolation: str = "linear",
        distortion_correction=None,
        nan_value=1.0,
        radios_srcurrent=None,
        flats_srcurrent=None,
        **chunk_reader_kwargs,
    ):
        """
        Initialize a flat-field normalization process with DataUrls.

        Parameters
        ----------
        radios_shape: tuple
            A tuple describing the shape of the radios stack, in the form
            `(n_radios, n_z, n_x)`.
        flats: dict
            Dictionary where the key is the flat index, and the value is a
            silx.io.DataUrl pointing to the flat.
        darks: dict
            Dictionary where the key is the dark index, and the value is a
            silx.io.DataUrl pointing to the dark.
        radios_indices: array, optional
            Array containing the radios indices. `radios_indices[0]` is the index
            of the first radio, and so on.
        interpolation: str, optional
            Interpolation method for flat-field. See below for more details.
        distortion_correction: DistortionCorrection, optional
            A DistortionCorrection object. If provided, it is used to correct flat distortions based on each radio.
        nan_value: float, optional
            Which float value is used to replace nan/inf after flat-field.


        Other Parameters
        ----------------
        The other named parameters are passed to the reading function (sub_region, binning, etc). Please read its
        documentation for more information.

        Notes
        ------
        Usually, when doing a scan, only one or a few darks/flats are acquired.
        However, the flat-field normalization has to be performed on each radio,
        although incoming beam can fluctuate between projections.
        The usual way to overcome this is to interpolate between flats.
        If interpolation="nearest", the first flat is used for the first
        radios subset, the second flat is used for the second radios subset,
        and so on.
        If interpolation="linear", the normalization is done as a linear
        function of the radio index.
        """

        flats_arrays_dict = load_images_from_dataurl_dict(flats, **chunk_reader_kwargs)
        darks_arrays_dict = load_images_from_dataurl_dict(darks, **chunk_reader_kwargs)
        super().__init__(
            radios_shape,
            flats_arrays_dict,
            darks_arrays_dict,
            radios_indices=radios_indices,
            interpolation=interpolation,
            distortion_correction=distortion_correction,
            nan_value=nan_value,
            radios_srcurrent=radios_srcurrent,
            flats_srcurrent=flats_srcurrent,
        )


class PCAFlatsNormalizer:
    """This class implement a flatfield normalization based on a PCA of a series of acquired flatfields.
    The PCA decomposition is handled by a PCAFlatsDecomposer object.

    This implementation was proposed by Jailin C. et al in https://journals.iucr.org/s/issues/2017/01/00/fv5055/

    Code initially written by ID11 @ ESRF staff.
    Jonathan Wright - Implementation based on research paper
    Pedro D. Resende - Added saving and loading from file capabilities

    Jerome Lesaint - Integrated the solution in Nabu.

    """

    def __init__(self, components, dark, mean):
        """Initializes all variables needed to perform the flatfield normalization.

        Parameters
        -----------
        components: ndarray
            The components of the PCA decomposition.
        dark: ndarray
            The dark image. Should be one single 2D image.
        mean: ndarray
            The mean image of the series of flats.
        """
        ones = np.ones_like(components[0], dtype=np.float32)[np.newaxis]  # This comp will account for I0
        self.components = np.concatenate([ones, components], axis=0)
        self.dark = dark
        self.mean = mean
        self.n_threads = max(1, get_num_threads() // 2)
        self._setmask()
        self.ccdfilter = CCDFilter(mean.shape)

    def _form_lsq_matrix(self):
        """This function form the Least Square matrix, based on the flats components and the mask."""
        self.Amat = np.stack([gg for gg in self.g], axis=1)  # JL: this is the matrix for the fit

    def _setmask(self, prop=0.125):
        """Sets the mask to select where the model is going to be fitted.

        Parameters
        ----------
        prop: float, default: 0.125
            The proportion of the image width to take on each side of the image as a mask.

            By default it sets the strips on each side of the frame in the form:
                mask[:, lim:] = True
                mask[:, -lim:] = True
            Where lim = prop * flat.shape[1]

        If you need a custom mask, see update_mask() method.
        """

        lim = int(prop * self.mean.shape[1])
        self.mask = np.zeros(self.mean.shape, dtype=bool)
        self.mask[:, :lim] = True
        self.mask[:, -lim:] = True
        self.g = []
        for component in self.components:
            self.g.append(component[self.mask])

        self._form_lsq_matrix()

    def update_mask(self, mask: np.ndarray):
        """Method to update the mask with a custom mask in the form of a boolean 2+D array.

        Paramters
        =========
        mask: np.ndarray of Boolean;
            The array of boolean allows the selection of the region of the image that will be used to fit against the components.

        It will set the mask, replacing the standard mask created with setmask().
        """
        if mask.dtype == bool:
            self.mask = mask
            self.g = []
            for component in self.components:
                self.g.append(component[self.mask])

            self._form_lsq_matrix()
        else:
            raise TypeError("Not a boolean array. Will keep the default mask")

    def normalize_radios(self, projections, mask=None, prop=0.125):
        """This is to keep the flatfield API in the pipeline."""
        self.correct_stack(projections, mask=mask, prop=prop)

    def correct_stack(
        self,
        projections: np.ndarray,
        mask: np.ndarray = None,
        prop: float = 0.125,
    ):
        """This functions normalizes the stack of projections.

        Performs correction on a stack of projections based on the calculated decomposition.
        The normalizations is done in-place. The previous projections before normalization are lost.

        Parameters
        ----------
        projections: ndarray
            Stack of projections to normalize.

        prop: float (default: {0.125})
            Fraction to mask on the horizontal field of view, assuming vertical rotation axis

        mask: np.ndarray (default: None)
            Custom mask if your data requires it.

        Returns
        -------
        corrected projections: np.ndarray
            Flat field corrected images. Note that the returned projections are exp-transformed to fit the pipeline (e.g. to allow for phase retrieval).
        """
        self.projections = self.ccdfilter.dezinger_correction(projections, self.dark)

        if mask is not None:
            self.update_mask(mask=mask)
        else:
            self._setmask(prop=prop)

        with ThreadPool(self.n_threads) as tp:
            for i, cor, sol in tp.map(self._readcorrect1, range(len(projections))):
                # solution[i] = sol
                projections[i] = np.exp(-cor)

    def _readcorrect1(self, ii):
        """Method to allow parallelization of the normalization."""
        corr, s = self.correctproj(self.projections[ii])
        return ii, corr, s

    def correctproj(self, projection):
        """Performs the correction on one projection of the stack.

        Parameters
        ----------
        projection: np.ndarray, float
            Radiograph from the acquisition stack.

        Returns
        -------
        The fitted projection.
        """
        logp = np.log(projection.astype(np.float32) - self.dark)
        corr = self.mean - logp
        # model to be fitted !!
        return self.fit(corr)

    def fit(self, corr):
        """Fit the (masked) projection to the (masked) components of the PCA decomposition.

        This is for each projection, so worth optimising ...
        """
        y = corr[self.mask]
        solution = np.linalg.lstsq(self.Amat, y, rcond=None)[0]
        correction = np.einsum("ijk,i->jk", self.components, solution)
        return corr - correction, solution


class PCAFlatsDecomposer:
    """This class implements a PCA decomposition of a serie of acquired flatfields.
    The PCA decomposition is used to normalize the projections through a PCAFLatNormalizer object.

    This implementation was proposed by Jailin C. et al in https://journals.iucr.org/s/issues/2017/01/00/fv5055/

    Code initially written by ID11 @ ESRF staff.
    Jonathan Wright - Implementation based on research paper
    Pedro D. Resende - Added saving and loading from file capabilities

    Jerome Lesaint - Integrated the solution in Nabu.
    """

    def __init__(self, flats: np.ndarray, darks: np.ndarray, nsigma=3):
        """

        Parameters
        -----------
        flats: np.ndarray
            A stack of darks corrected flat field images
        darks: np.ndarray
            An image or stack of images of the dark current images of the camera.

        Does the log scaling.
        Subtracts mean and does eigenvector decomposition.
        """
        self.n_threads = max(1, get_num_threads() // 2)
        self.flats = np.empty(flats.shape, dtype=np.float32)

        darks = darks.astype(np.float32)
        if darks.ndim == 3:
            self.dark = np.median(darks, axis=0)
        else:
            self.dark = darks.copy()
        del darks

        self.nsigma = nsigma
        self.ccdfilter = CCDFilter(self.dark.shape)
        self._ccdfilter_and_log(flats)  # Log is taken here (after dezinger)

        self.mean = np.mean(self.flats, axis=0)  # average

        self.flats = self.flats - self.mean  # makes a copy
        self.cov = self.compute_correlation_matrix()
        self.compute_pca()
        self.generate_pca_flats(nsigma=nsigma)  # Default nsigma=3

    def __str__(self):

        return f"PCA decomposition from flat images. \nThere are {self.components} components created at {self.sigma} level."

    def _ccdfilter_and_log(self, flats: np.ndarray):
        """Dezinger (subtract dark, apply median filter) and takes log of the flat stack"""

        self.ccdfilter.dezinger_correction(flats, self.dark)

        with ThreadPool(self.n_threads) as tp:
            for i, frame in enumerate(tp.map(np.log, flats)):
                self.flats[i] = frame

    @staticmethod
    def ccij(args):
        """Compute the covariance (img[i]*img[j]).sum() / npixels
        It is a wrapper for threading.
        args == i, j, npixels, imgs
        """

        i, j, NY, imgs = args
        return i, j, np.einsum("ij,ij", imgs[i], imgs[j]) / NY

    def compute_correlation_matrix(self):
        """Computes an (nflats x nflats) correlation matrix"""

        N = len(self.flats)
        CC = np.zeros((N, N), float)
        args = [(i, j, N, self.flats) for i in range(N) for j in range(i + 1)]
        with ThreadPool(self.n_threads) as tp:
            for i, j, result in tp.map(self.ccij, args):
                CC[i, j] = CC[j, i] = result
        return CC

    def compute_pca(self):
        """Gets eigenvectors and eigenvalues and sorts them into order"""

        self.eigenvalues, self.eigenvectors = np.linalg.eigh(
            self.cov
        )  # Not sure why the eigh is needed. eig should be enough.
        order = np.argsort(abs(self.eigenvalues))[::-1]  # high to low
        self.eigenvalues = self.eigenvalues[order]
        self.eigenvectors = self.eigenvectors[:, order]

    def generate_pca_flats(self, nsigma=3):
        """Projects the eigenvectors back into image space.

        Parameters
        ----------
        nsigma: int (default: 3)
        """

        self.sigma = nsigma
        av = abs(self.eigenvalues)
        N = max(1, (av > (av[-2] * nsigma)).sum())  # Go for 3 sigma. And always take at least one comp.

        self.components = [
            None,
        ] * N

        def calculate(ii):
            calc = np.einsum("i,ijk->jk", self.eigenvectors[:, ii], self.flats)
            norm = (calc**2).sum()
            return ii, calc / np.sqrt(norm)

        with ThreadPool(self.n_threads) as tp:
            for ii, result in tp.map(calculate, range(N)):
                self.components[ii] = result

        # simple gradients
        r, c = self.components[0].shape
        self.components.append(np.outer(np.ones(r), np.linspace(-1 / c, 1 / c, c)))
        self.components.append(np.outer(np.linspace(-1 / r, 1 / r, r), np.ones(c)))

    def save_decomposition(self, path="PCA_flats.h5", overwrite=True, entry="entry0000"):
        """Saves the basic information of a PCA decomposition in view of the normalization of projections.

        Parameters
        ----------
        path: str (default: "PCA_flats.h5")
            Full path to the h5 file you want to save your results. It will overwrite!! Be careful.
        """

        file_exists = os.path.exists(path)
        if overwrite or not file_exists:
            with HDF5File(path, "w") as hout:
                group = hout.create_group(entry)
                group["eigenvalues"] = self.eigenvalues
                group["dark"] = self.dark.astype(np.float32)
                group["p_mean"] = self.mean.astype(np.float32)
                group["p_components"] = np.array(self.components)
                hout.flush()
        else:
            raise OSError(f"The file {path} already exists and you chose to NOT overwrite.")
