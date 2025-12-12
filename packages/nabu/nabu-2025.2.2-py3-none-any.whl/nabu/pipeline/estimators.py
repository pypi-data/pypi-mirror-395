"""
nabu.pipeline.estimators: helper classes/functions to estimate parameters of a dataset
(center of rotation, detector tilt, etc).
"""

import inspect
import numpy as np
import scipy.fft  #  pylint: disable=E0611
from silx.io import get_data
import math
from scipy import ndimage as nd

from ..preproc.flatfield import FlatField
from ..estimation.cor import (
    CenterOfRotation,
    CenterOfRotationAdaptiveSearch,
    CenterOfRotationSlidingWindow,
    CenterOfRotationGrowingWindow,
    CenterOfRotationOctaveAccurate,
)
from .. import version as nabu_version
from ..estimation.cor_sino import SinoCorInterface, CenterOfRotationFourierAngles, CenterOfRotationVo
from ..estimation.tilt import CameraTilt
from ..estimation.motion import MotionEstimation
from ..estimation.utils import is_fullturn_scan
from ..resources.logger import LoggerOrPrint
from ..resources.utils import extract_parameters
from ..utils import check_supported, deprecation_warning, get_num_threads, is_int, is_scalar
from ..resources.dataset_analyzer import get_radio_pair
from ..processing.rotation import Rotation
from ..preproc.ccd import Log, CCDFilter
from ..misc import fourier_filters
from .params import cor_methods, tilt_methods


def estimate_cor(method, dataset_info, do_flatfield=True, cor_options=None, logger=None):
    """
    High level function to compute the center of rotation (COR)

    Parameters
    ----------
    method: name of the method to be used for computing the center of rotation
    dataset_info: `nabu.resources.dataset_analyzer.DatasetAnalyzer`
        Dataset information structure
    do_flatfield: If True apply flat field to compute the center of rotation
    cor_options: optional dictionary that can contain the following keys:
        * slice_idx: index of the slice to use for computing the sinogram (for sinogram based algorithms)
        * subsampling subsampling
        * radio_angles: angles of the radios to use (for radio based algorithms)
    logger: logging object
    """
    logger = LoggerOrPrint(logger)
    cor_options = cor_options or {}
    check_supported(method, list(cor_methods.keys()), "COR estimation method")
    method = cor_methods[method]

    # Extract CoR parameters from configuration file
    if isinstance(cor_options, str):
        try:
            cor_options = extract_parameters(cor_options, sep=";")
        except Exception as exc:
            msg = "Could not extract parameters from cor_options: %s" % (str(exc))
            logger.fatal(msg)
            raise ValueError(msg)
    elif isinstance(cor_options, dict):
        pass
    else:
        raise TypeError(f"cor_options_str is expected to be a dict or a str. {type(cor_options)} provided")

    # Dispatch. COR estimation is always expressed in absolute number of pixels (i.e. from the center of the first pixel column)
    if method in CORFinder.search_methods:
        cor_finder = CORFinder(
            method,
            dataset_info,
            do_flatfield=do_flatfield,
            cor_options=cor_options,
            radio_angles=cor_options.get("radio_angles", (0.0, np.pi)),
            logger=logger,
        )
        estimated_cor = cor_finder.find_cor()
    elif method in SinoCORFinder.search_methods:
        cor_finder = SinoCORFinder(
            method,
            dataset_info,
            slice_idx=cor_options.get("slice_idx", "middle"),
            subsampling=cor_options.get("subsampling", 10),
            do_flatfield=do_flatfield,
            take_log=cor_options.get("take_log", True),
            cor_options=cor_options,
            logger=logger,
        )
        estimated_cor = cor_finder.find_cor()
    else:
        composite_options = update_func_kwargs(CompositeCORFinder, cor_options)
        for what in ["cor_options", "logger", "do_flatfield"]:
            composite_options.pop(what, None)
        cor_finder = CompositeCORFinder(
            dataset_info,
            cor_options=cor_options,
            do_flatfield=do_flatfield,
            logger=logger,
            **composite_options,  # contains take_log
        )
        estimated_cor = cor_finder.find_cor()
    return estimated_cor


class CORFinderBase:
    """
    A base class for CoR estimators.
    It does common tasks like data reading, flatfield, etc.
    """

    search_methods = {}

    def __init__(self, method, dataset_info, do_flatfield=True, cor_options=None, logger=None):
        """
        Initialize a CORFinder object.

        Parameters
        ----------
        dataset_info: `nabu.resources.dataset_analyzer.DatasetAnalyzer`
            Dataset information structure
        """
        check_supported(method, self.search_methods, "CoR estimation method")
        self.method = method
        self.cor_options = cor_options or {}
        self.logger = LoggerOrPrint(logger)
        self.dataset_info = dataset_info
        self.do_flatfield = do_flatfield
        self.shape = dataset_info.radio_dims[::-1]
        self._get_lookup_side()
        self._init_cor_finder()

    def _get_lookup_side(self):
        """
        Get the "initial guess" where the center-of-rotation (CoR) should be estimated.
        For example 'center' means that CoR search will be done near the middle of the detector, i.e center column.
        """
        lookup_side = self.cor_options.get("side", None)
        self._lookup_side = lookup_side
        # User-provided scalar
        if not (isinstance(lookup_side, str)) and np.isscalar(lookup_side):
            return

        default_lookup_side = "right" if self.dataset_info.is_halftomo else "center"

        # By default in nabu config, side='from_file' meaning that we inspect the dataset information for CoR metadata
        if lookup_side == "from_file":
            initial_cor_pos = self.dataset_info.dataset_scanner.x_rotation_axis_pixel_position  # relative pos in pixels
            if initial_cor_pos is None:
                self.logger.warning("Could not get an initial estimate for center of rotation in data file")
                lookup_side = default_lookup_side
            else:
                lookup_side = initial_cor_pos
            self._lookup_side = lookup_side

    def _init_cor_finder(self):
        cor_finder_cls = self.search_methods[self.method]["class"]
        self.cor_finder = cor_finder_cls(verbose=False, logger=self.logger, extra_options=None)


class CORFinder(CORFinderBase):
    """
    Find the Center of Rotation with methods based on two (180-degrees opposed) radios.
    """

    search_methods = {
        "centered": {
            "class": CenterOfRotation,
        },
        "global": {
            "class": CenterOfRotationAdaptiveSearch,
            "default_kwargs": {"low_pass": 1, "high_pass": 20},
        },
        "sliding-window": {
            "class": CenterOfRotationSlidingWindow,
        },
        "growing-window": {
            "class": CenterOfRotationGrowingWindow,
        },
        "octave-accurate": {
            "class": CenterOfRotationOctaveAccurate,
        },
    }

    def __init__(
        self, method, dataset_info, do_flatfield=True, cor_options=None, logger=None, radio_angles=(0.0, np.pi)
    ):
        """
        Initialize a CORFinder object.

        Parameters
        ----------
        dataset_info: `nabu.resources.dataset_analyzer.DatasetAnalyzer`
            Dataset information structure
        radio_angles: angles to use to find the cor
        """
        super().__init__(method, dataset_info, do_flatfield=do_flatfield, cor_options=cor_options, logger=logger)
        self._radio_angles = radio_angles
        self._init_radios()
        self._apply_flatfield()
        self._apply_tilt()
        # octave-accurate does not support half-acquisition scans,
        # but information on field of view is only known here with the "dataset_info" object.
        # Do the check here.
        if self.dataset_info.is_halftomo and method == "octave-accurate":
            raise ValueError("The CoR estimator 'octave-accurate' does not support half-acquisition scans")
        #

    def _init_radios(self):
        self.radios, self._radios_indices = get_radio_pair(
            self.dataset_info, radio_angles=self._radio_angles, return_indices=True
        )

    def _apply_flatfield(self):
        if not (self.do_flatfield):
            return
        self.flatfield = FlatField(
            self.radios.shape,
            flats=self.dataset_info.flats,
            darks=self.dataset_info.darks,
            radios_indices=self._radios_indices,
            interpolation="linear",
        )
        self.flatfield.normalize_radios(self.radios)

    def _apply_tilt(self):
        tilt = self.dataset_info.detector_tilt
        if tilt is None:
            return
        self.logger.debug("COREstimator: applying detector tilt correction of %f degrees" % tilt)
        rot = Rotation(self.shape, tilt)
        for i in range(self.radios.shape[0]):
            self.radios[i] = rot.rotate(self.radios[i])

    def find_cor(self):
        """
        Find the center of rotation.

        Returns
        -------
        cor: float
            The estimated center of rotation for the current dataset.
        """
        self.logger.info("Estimating center of rotation")
        # All find_shift() methods in self.search_methods have the same API with "img_1" and "img_2"
        cor_exec_kwargs = update_func_kwargs(self.cor_finder.find_shift, self.cor_options)
        cor_exec_kwargs["return_relative_to_middle"] = False
        # ----- FIXME -----
        # 'self.cor_options' can contain 'side="from_file"', and we should not modify it directly
        # because it's entered by the user.
        # Either make a copy of self.cor_options, or change the inspect() mechanism
        if cor_exec_kwargs.get("side", None) == "from_file":
            cor_exec_kwargs["side"] = self._lookup_side or "center"
        # ------
        if self._lookup_side is not None:
            cor_exec_kwargs["side"] = self._lookup_side
        self.logger.debug("%s.find_shift(%s)" % (self.cor_finder.__class__.__name__, str(cor_exec_kwargs)))
        shift = self.cor_finder.find_shift(self.radios[0], np.fliplr(self.radios[1]), **cor_exec_kwargs)
        return shift


# alias
COREstimator = CORFinder


class SinoCORFinder(CORFinderBase):
    """
    A class for finding Center of Rotation based on 360 degrees sinograms.
    This class handles the steps of building the sinogram from raw radios.
    """

    search_methods = {
        "sino-coarse-to-fine": {
            "class": SinoCorInterface,
        },
        "sino-sliding-window": {
            "class": CenterOfRotationSlidingWindow,
        },
        "sino-growing-window": {
            "class": CenterOfRotationGrowingWindow,
        },
        "fourier-angles": {"class": CenterOfRotationFourierAngles},
        "vo": {
            "class": CenterOfRotationVo,
        },
    }

    def __init__(
        self,
        method,
        dataset_info,
        do_flatfield=True,
        take_log=True,
        cor_options=None,
        logger=None,
        slice_idx="middle",
        subsampling=10,
    ):
        """
        Initialize a SinoCORFinder object.

        Other Parameters
        ----------------
        The following keys can be set in cor_options.

        slice_idx: int or str
            Which slice index to take for building the sinogram.
            For example slice_idx=0 means that we extract the first line of each projection.
            Value can also be "first", "top", "middle", "last", "bottom".
        subsampling: int, float
            subsampling strategy when building sinograms.
            As building the complete sinogram from raw projections might be tedious, the reading is done with subsampling.
            A positive integer value means the subsampling step (i.e `projections[::subsampling]`).
        """
        super().__init__(method, dataset_info, do_flatfield=do_flatfield, cor_options=cor_options, logger=logger)
        self._set_slice_idx(slice_idx)
        self._set_subsampling(subsampling)
        self._load_raw_sinogram()
        self._flatfield(do_flatfield)
        self._get_sinogram(take_log)

    def _check_360(self):
        if not is_fullturn_scan(self.dataset_info.rotation_angles):
            raise ValueError("Sinogram-based Center of Rotation estimation can only be used for 360 degrees scans")

    def _set_slice_idx(self, slice_idx):
        n_z = self.dataset_info.radio_dims[1]
        if isinstance(slice_idx, str):
            str_to_idx = {"top": 0, "first": 0, "middle": n_z // 2, "bottom": n_z - 1, "last": n_z - 1}
            check_supported(slice_idx, str_to_idx.keys(), "slice location")
            slice_idx = str_to_idx[slice_idx]
        self.slice_idx = slice_idx

    def _set_subsampling(self, subsampling):
        projs_idx = sorted(self.dataset_info.projections.keys())
        self.subsampling = None
        if is_int(subsampling):
            if subsampling < 0:  # Total number of angles
                raise NotImplementedError
            else:
                self.projs_indices = projs_idx[::subsampling]
                self.angles = self.dataset_info.rotation_angles[::subsampling]
                self.subsampling = subsampling
        else:  # Angular step
            raise NotImplementedError

    def _load_raw_sinogram(self):
        if self.slice_idx is None:
            raise ValueError("Unknow slice index")
        reader_kwargs = {
            "sub_region": (slice(None, None, self.subsampling), slice(self.slice_idx, self.slice_idx + 1), slice(None))
        }
        if self.dataset_info.kind == "edf":
            reader_kwargs = {"n_reading_threads": get_num_threads()}
        self.data_reader = self.dataset_info.get_reader(**reader_kwargs)
        self._radios = self.data_reader.load_data()

    def _flatfield(self, do_flatfield):
        self.do_flatfield = bool(do_flatfield)
        if not self.do_flatfield:
            return
        flats = {k: arr[self.slice_idx : self.slice_idx + 1, :] for k, arr in self.dataset_info.flats.items()}
        darks = {k: arr[self.slice_idx : self.slice_idx + 1, :] for k, arr in self.dataset_info.darks.items()}
        flatfield = FlatField(
            self._radios.shape,
            flats,
            darks,
            radios_indices=self.projs_indices,
        )
        flatfield.normalize_radios(self._radios)

    def _get_sinogram(self, take_log):
        sinogram = self._radios[:, 0, :].copy()
        if take_log:
            log = Log(self._radios.shape, clip_min=1e-6, clip_max=10.0)
            log.take_logarithm(sinogram)
        self.sinogram = sinogram

    @staticmethod
    def _split_sinogram(sinogram):
        n_a_2 = sinogram.shape[0] // 2
        img_1, img_2 = sinogram[:n_a_2], sinogram[n_a_2:]
        # "Handle" odd number of projections
        if img_2.shape[0] > img_1.shape[0]:
            img_2 = img_2[:-1, :]
        #
        return img_1, img_2

    def find_cor(self):
        self.logger.info("Estimating center of rotation")

        cor_exec_kwargs = update_func_kwargs(self.cor_finder.find_shift, self.cor_options)
        cor_exec_kwargs["return_relative_to_middle"] = False
        # FIXME
        # 'self.cor_options' can contain 'side="from_file"', and we should not modify it directly
        # because it's entered by the user.
        # Either make a copy of self.cor_options, or change the inspect() mechanism
        if cor_exec_kwargs["side"] == "from_file":
            cor_exec_kwargs["side"] = self._lookup_side or "center"
        #
        if self._lookup_side is not None:
            cor_exec_kwargs["side"] = self._lookup_side

        if self.method == "fourier-angles":
            cor_exec_args = [self.sinogram]
            cor_exec_kwargs["angles"] = self.dataset_info.rotation_angles
        elif self.method == "vo":
            cor_exec_args = [self.sinogram]
            cor_exec_kwargs["halftomo"] = self.dataset_info.is_halftomo
            cor_exec_kwargs["is_360"] = is_fullturn_scan(self.dataset_info.rotation_angles)
        else:
            # For these methods relying on find_shift() with two images, the sinogram needs to be split in two
            img_1, img_2 = self._split_sinogram(self.sinogram)
            cor_exec_args = [img_1, np.fliplr(img_2)]

        self.logger.debug("%s.find_shift(%s)" % (self.cor_finder.__class__.__name__, str(cor_exec_kwargs)))
        shift = self.cor_finder.find_shift(*cor_exec_args, **cor_exec_kwargs)

        return shift


# alias
SinoCOREstimator = SinoCORFinder


class CompositeCORFinder(CORFinderBase):
    """
    Class and method to prepare sinogram and calculate COR
    The pseudo sinogram is built with shrunken radios taken every theta_interval degrees

    Compared to first writing by Christian Nemoz:
        - gives the same result of the original octave script on the dataset so far tested
        - The meaning of parameter n_subsampling_y (alias subsampling_y)is now the number of lines which are taken from
          every radio. This is more meaningful in terms of amount of collected information because it
          does not depend on the radio size. Moreover this is what was done in the octave script
        - The spike_threshold has been added with default to 0.04
        - The angular sampling is every 5 degree by default, as it is now the case also in the octave script
        - The finding of the optimal overlap is doing by looping over the possible overlap, according to the overlap.
           After a first testing phase, this part, which is the time consuming part, can be accelerated
           by several order of magnitude without modifying the final result
    """

    search_methods = {
        "composite-coarse-to-fine": {
            "class": CenterOfRotation,  # Not used. Everything is done in the find_cor() func.
        }
    }
    _default_cor_options = {"low_pass": 0.4, "high_pass": 10, "side": "near", "near_pos": 0, "near_width": 100}

    def __init__(
        self,
        dataset_info,
        oversampling=4,
        theta_interval=5,
        n_subsampling_y=40,
        do_flatfield=True,
        take_log=True,
        cor_options=None,
        spike_threshold=0.04,
        logger=None,
        norm_order=1,
    ):
        super().__init__(
            "composite-coarse-to-fine", dataset_info, do_flatfield=False, cor_options=cor_options, logger=logger
        )
        if norm_order not in [1, 2]:
            raise ValueError(
                f""" the norm order (nom_order parameter) must be either 1 or 2. You passed {norm_order}
                """
            )

        self.norm_order = norm_order

        self.dataset_info = dataset_info
        self.logger = LoggerOrPrint(logger)

        self.sx, self.sy = self.dataset_info.radio_dims

        default_cor_options = self._default_cor_options.copy()
        default_cor_options.update(self.cor_options)
        self.cor_options = default_cor_options

        # the algorithm can work for angular ranges larger than 1.2*pi
        # up to an arbitrarily number of turns as it is the case in helical scans
        self.spike_threshold = spike_threshold
        # the following line is necessary for multi-turns scan because the encoders is always
        # in the interval 0-360
        self.unwrapped_rotation_angles = np.unwrap(self.dataset_info.rotation_angles)

        self.angle_min = self.unwrapped_rotation_angles.min()
        self.angle_max = self.unwrapped_rotation_angles.max()

        if (self.angle_max - self.angle_min) < 1.2 * np.pi:
            useful_span = None
            raise ValueError(
                f"""Sinogram-based Center of Rotation estimation can only be used for scans over more than 180 degrees.
                                 Your angular span was barely above 180 degrees, it was in fact {((self.angle_max - self.angle_min)/np.pi):.2f} x 180
                                 and it is not considered to be enough by the discriminating condition which requires at least 1.2 half-turns
                              """
            )
        else:
            useful_span = min(np.pi, (self.angle_max - self.angle_min) - np.pi)
            # readapt theta_interval accordingly if the span is smaller than pi
            if useful_span < np.pi:
                theta_interval = theta_interval * useful_span / np.pi

        self.take_log = take_log
        self.ovs = oversampling
        self.theta_interval = theta_interval

        target_sampling_y = np.round(np.linspace(0, self.sy - 1, n_subsampling_y + 2)).astype(int)[1:-1]

        if self.spike_threshold is not None:
            # take also one line below and on above for each line
            # to provide appropriate margin
            self.sampling_y = np.zeros([3 * len(target_sampling_y)], "i")
            self.sampling_y[0::3] = np.maximum(0, target_sampling_y - 1)
            self.sampling_y[2::3] = np.minimum(self.sy - 1, target_sampling_y + 1)
            self.sampling_y[1::3] = target_sampling_y

            self.ccd_correction = CCDFilter((len(self.sampling_y), self.sx), median_clip_thresh=self.spike_threshold)
        else:
            self.sampling_y = target_sampling_y

        self.nproj = self.dataset_info.n_angles

        my_condition = np.less(self.unwrapped_rotation_angles + np.pi, self.angle_max) * np.less(
            self.unwrapped_rotation_angles, self.angle_min + useful_span
        )

        possibly_probed_angles = self.unwrapped_rotation_angles[my_condition]
        possibly_probed_indices = np.arange(len(self.unwrapped_rotation_angles))[my_condition]

        self.dproj = round(len(possibly_probed_angles) / np.rad2deg(useful_span) * self.theta_interval)

        self.probed_angles = possibly_probed_angles[:: self.dproj]
        self.probed_indices = possibly_probed_indices[:: self.dproj]

        self.absolute_indices = sorted(self.dataset_info.projections.keys())

        if do_flatfield:
            my_flats = self.dataset_info.flats
        else:
            my_flats = None

        if my_flats is not None and len(list(my_flats.keys())) > 0:
            self.use_flat = True
            self.flatfield = FlatField(
                (len(self.absolute_indices), self.sy, self.sx),
                self.dataset_info.flats,
                self.dataset_info.darks,
                radios_indices=self.absolute_indices,
            )
        else:
            self.use_flat = False

        self.sx, self.sy = self.dataset_info.radio_dims
        self.mlog = Log((1,) + (self.sy, self.sx), clip_min=1e-6, clip_max=10.0)
        self.rcor_abs = round(self.sx / 2.0)
        self.cor_acc = round(self.sx / 2.0)

        self.nprobed = len(self.probed_angles)

        # initialize sinograms and radios arrays
        self.sino = np.zeros([2 * self.nprobed * n_subsampling_y, (self.sx - 1) * self.ovs + 1], "f")
        self._loaded = False
        self.high_pass = self.cor_options["high_pass"]
        img_filter = fourier_filters.get_bandpass_filter(
            (self.sino.shape[0] // 2, self.sino.shape[1]),
            cutoff_lowpass=self.cor_options["low_pass"] * self.ovs,
            cutoff_highpass=self.high_pass * self.ovs,
            use_rfft=False,  # rfft changes the image dimensions lenghts to even if odd
            data_type=np.float64,
        )

        # we are interested in filtering only along the x dimension only
        img_filter[:] = img_filter[0]
        self.img_filter = img_filter

    def _oversample(self, radio):
        """oversampling in the horizontal direction"""
        if self.ovs == 1:
            return radio
        else:
            ovs_2D = [1, self.ovs]
        return oversample(radio, ovs_2D)

    def _get_cor_options(self, cor_options):
        default_dict = self._default_cor_options.copy()
        if self.dataset_info.is_halftomo:
            default_dict["side"] = "right"

        if cor_options is None or cor_options == "":
            cor_options = {}
        if isinstance(cor_options, str):
            try:
                cor_options = extract_parameters(cor_options, sep=";")
            except Exception as exc:
                msg = "Could not extract parameters from cor_options: %s" % (str(exc))
                self.logger.fatal(msg)
                raise ValueError(msg)
        default_dict.update(cor_options)
        cor_options = default_dict

        self.cor_options = cor_options

    def get_radio(self, image_num):
        #  radio_dataset_idx = self.absolute_indices[image_num]
        radio_dataset_idx = image_num
        data_url = self.dataset_info.projections[radio_dataset_idx]
        radio = get_data(data_url).astype(np.float64)
        if self.use_flat:
            self.flatfield.normalize_single_radio(radio, radio_dataset_idx, dtype=radio.dtype)
        if self.take_log:
            self.mlog.take_logarithm(radio)

        radio = radio[self.sampling_y]
        if self.spike_threshold is not None:
            self.ccd_correction.median_clip_correction(radio, output=radio)
            radio = radio[1::3]
        return radio

    def get_sino(self, reload=False):
        """
        Build sinogram (composite image) from the radio files
        """
        if self._loaded and not reload:
            return self.sino

        sorting_indexes = np.argsort(self.unwrapped_rotation_angles)

        sorted_all_angles = self.unwrapped_rotation_angles[sorting_indexes]
        sorted_angle_indexes = np.arange(len(self.unwrapped_rotation_angles))[sorting_indexes]

        irad = 0
        for prob_a, prob_i in zip(self.probed_angles, self.probed_indices):
            radio1 = self.get_radio(self.absolute_indices[prob_i])
            other_angle = prob_a + np.pi

            insertion_point = np.searchsorted(sorted_all_angles, other_angle)
            if insertion_point > 0 and insertion_point < len(sorted_all_angles):
                other_i_l = sorted_angle_indexes[insertion_point - 1]
                other_i_h = sorted_angle_indexes[insertion_point]
                radio_l = self.get_radio(self.absolute_indices[other_i_l])
                radio_h = self.get_radio(self.absolute_indices[other_i_h])
                f = (other_angle - sorted_all_angles[insertion_point - 1]) / (
                    sorted_all_angles[insertion_point] - sorted_all_angles[insertion_point - 1]
                )
                radio2 = (1 - f) * radio_l + f * radio_h
            else:
                if insertion_point == 0:
                    other_i = sorted_angle_indexes[0]
                elif insertion_point == len(sorted_all_angles):
                    other_i = sorted_angle_indexes[insertion_point - 1]
                radio2 = self.get_radio(self.absolute_indices[other_i])  # pylint: disable=E0606

            self.sino[irad : irad + radio1.shape[0], :] = self._oversample(radio1)
            self.sino[
                irad + self.nprobed * radio1.shape[0] : irad + self.nprobed * radio1.shape[0] + radio1.shape[0], :
            ] = self._oversample(radio2)

            irad = irad + radio1.shape[0]

        self.sino[np.isnan(self.sino)] = 0.0001  # ?
        return self.sino

    def find_cor(self, reload=False):
        self.logger.info("Estimating center of rotation")
        self.logger.debug("%s.find_shift(%s)" % (self.__class__.__name__, self.cor_options))
        self.sinogram = self.get_sino(reload=reload)

        detector_center = (self.shape[-1] - 1) / 2.0
        dim_v, dim_h = self.sinogram.shape
        assert dim_v % 2 == 0, " this should not happen "
        dim_v = dim_v // 2

        radio1 = self.sinogram[:dim_v]
        radio2 = self.sinogram[dim_v:]

        orig_sy, orig_ovsd_sx = radio1.shape

        radio1 = scipy.fft.ifftn(
            scipy.fft.fftn(radio1, axes=(-2, -1)) * self.img_filter, axes=(-2, -1)
        ).real  # TODO: convolute only along x
        radio2 = scipy.fft.ifftn(
            scipy.fft.fftn(radio2, axes=(-2, -1)) * self.img_filter, axes=(-2, -1)
        ).real  # TODO: convolute only along x

        tmp_sy, radio_width = radio1.shape
        assert orig_sy == tmp_sy and orig_ovsd_sx == radio_width, "this should not happen"

        cor_side = self._lookup_side if self._lookup_side is not None else self.cor_options["side"]
        if cor_side == "center":
            overlap_min = max(round(radio_width - radio_width / 3), 4)
            overlap_max = min(round(radio_width + radio_width / 3), 2 * radio_width - 4)
        elif cor_side == "right":
            overlap_min = max(4, self.ovs * self.high_pass * 3)
            overlap_max = radio_width
        elif cor_side == "left":
            overlap_min = radio_width
            overlap_max = min(2 * radio_width - 4, 2 * radio_width - self.ovs * self.ovs * self.high_pass * 3)
        elif cor_side == "all":
            overlap_min = max(4, self.ovs * self.high_pass * 3)
            overlap_max = min(2 * radio_width - 4, 2 * radio_width - self.ovs * self.ovs * self.high_pass * 3)
        elif is_scalar(cor_side):
            near_pos = cor_side
            near_width = self.cor_options["near_width"]
            overlap_min = max(4, radio_width - 2 * self.ovs * (near_pos + near_width))
            overlap_max = min(2 * radio_width - 4, radio_width - 2 * self.ovs * (near_pos - near_width))
        # COMPAT.
        elif cor_side == "near":
            deprecation_warning(
                "using side='near' is deprecated, use side=<a scalar> instead",
                do_print=True,
                func_name="composite_near_pos",
            )
            near_pos = self.cor_options["near_pos"]
            near_width = self.cor_options["near_width"]
            overlap_min = max(4, radio_width - 2 * self.ovs * (near_pos + near_width))
            overlap_max = min(2 * radio_width - 4, radio_width - 2 * self.ovs * (near_pos - near_width))
        # ---
        else:
            raise ValueError("Invalid option 'side=%s'" % self.cor_options["side"])

        if overlap_min > overlap_max:
            message = f""" There is no safe search range in find_cor once the margins corresponding to the high_pass filter are discarded.
            Try reducing the low_pass parameter in cor_options
            """
            raise ValueError(message)

        # cor_min and cor_max are only for information, not used in the algorithm, they correspond to the search window in the original projection grid (before oversampling)
        cor_min = detector_center + (radio_width - overlap_max) / (2 * self.ovs)
        cor_max = detector_center + (radio_width - overlap_min) / (2 * self.ovs)
        self.logger.info(f"looking around {cor_side} overlap from min {cor_min:2f} and max {cor_max:2f}")

        best_overlap = overlap_min
        best_error = np.inf

        blurred_radio1 = nd.gaussian_filter(abs(radio1), [0, self.high_pass])
        blurred_radio2 = nd.gaussian_filter(abs(radio2), [0, self.high_pass])

        for z in range(int(overlap_min), int(overlap_max) + 1):
            if z <= radio_width:
                my_z = z
                my_radio1 = radio1
                my_radio2 = radio2
                my_blurred_radio1 = blurred_radio1
                my_blurred_radio2 = blurred_radio2
            else:
                my_z = radio_width - (z - radio_width)
                my_radio1 = np.fliplr(radio1)
                my_radio2 = np.fliplr(radio2)
                my_blurred_radio1 = np.fliplr(blurred_radio1)
                my_blurred_radio2 = np.fliplr(blurred_radio2)

            common_left = np.fliplr(my_radio1[:, radio_width - my_z :])[:, : -math.ceil(self.ovs * self.high_pass * 2)]
            # adopt a 'safe' margin considering high_pass value (possibly float)
            common_right = my_radio2[:, radio_width - my_z : -math.ceil(self.ovs * self.high_pass * 2)]

            common_blurred_left = np.fliplr(my_blurred_radio1[:, radio_width - my_z :])[
                :, : -math.ceil(self.ovs * self.high_pass * 2)
            ]
            # adopt a 'safe' margin considering high_pass value (possibly float)
            common_blurred_right = my_blurred_radio2[:, radio_width - my_z : -math.ceil(self.ovs * self.high_pass * 2)]

            if common_right.size == 0:
                continue

            error = self.error_metric(common_right, common_left, common_blurred_right, common_blurred_left)

            min_error = min(best_error, error)

            if min_error == error:
                best_overlap = z
                best_error = min_error
            # self.logger.debug(
            #     "testing an overlap of %.2f pixels, actual best overlap is %.2f pixels over %d\r"
            #     % (z / self.ovs, best_overlap / self.ovs, ovsd_sx / self.ovs),
            # )

        offset = (radio_width - best_overlap) / self.ovs / 2
        cor_abs = (self.sx - 1) / 2 + offset

        return cor_abs

    def error_metric(self, common_right, common_left, common_blurred_right, common_blurred_left):
        if self.norm_order == 2:
            return self.error_metric_l2(common_right, common_left)
        elif self.norm_order == 1:
            return self.error_metric_l1(common_right, common_left, common_blurred_right, common_blurred_left)
        else:
            raise RuntimeError("this cannot happen")

    def error_metric_l2(self, common_right, common_left):
        common = common_right - common_left

        tmp = np.linalg.norm(common)
        norm_diff2 = tmp * tmp

        norm_right = np.linalg.norm(common_right)
        norm_left = np.linalg.norm(common_left)

        res = norm_diff2 / (norm_right * norm_left)

        return res

    def error_metric_l1(self, common_right, common_left, common_blurred_right, common_blurred_left):
        common = (common_right - common_left) / (common_blurred_right + common_blurred_left)

        res = abs(common).mean()

        return res


def oversample(radio, ovs_s):
    """oversampling an image in arbitrary directions.
    The first and last point of each axis will still remain as  extremal points of the new axis.
    """
    result = np.zeros([(radio.shape[0] - 1) * ovs_s[0] + 1, (radio.shape[1] - 1) * ovs_s[1] + 1], "f")

    # Pre-initialisation: The original data falls exactly on the following strided positions in the new data array.
    result[:: ovs_s[0], :: ovs_s[1]] = radio

    for k in range(ovs_s[0]):
        # interpolation coefficient for axis 0
        g = k / ovs_s[0]
        for i in range(ovs_s[1]):
            if i == 0 and k == 0:
                # this case subset was already exactly matched from before the present double loop,
                # in the pre-initialisation line.
                continue
            # interpolation coefficent for axis 1
            f = i / ovs_s[1]

            # stop just a bit before cause we are not extending beyond the limits.
            # If we are exacly on a vertical or horizontal original line, then no shift will be applied,
            # and we will exploit the equality f+(1-f)=g+(1-g)=1 adding twice the same contribution with
            # interpolation factors which become dummies pour le coup.
            stop0 = -ovs_s[0] if k else None
            stop1 = -ovs_s[1] if i else None

            # Once again, we exploit the  g+(1-g)=1 equality
            start0 = ovs_s[0] if k else 0
            start1 = ovs_s[1] if i else 0

            # and what is done below makes clear the corundum above.
            result[k :: ovs_s[0], i :: ovs_s[1]] = (1 - g) * (
                (1 - f) * result[0 : stop0 : ovs_s[0], 0 : stop1 : ovs_s[1]]
                + f * result[0 : stop0 : ovs_s[0], start1 :: ovs_s[1]]
            ) + g * (
                (1 - f) * result[start0 :: ovs_s[0], 0 : stop1 : ovs_s[1]]
                + f * result[start0 :: ovs_s[0], start1 :: ovs_s[1]]
            )
    return result


# alias
CompositeCOREstimator = CompositeCORFinder


# Some heavily inelegant things going on here
def get_default_kwargs(func):
    params = inspect.signature(func).parameters
    res = {}
    for param_name, param in params.items():
        if param.default != inspect._empty:
            res[param_name] = param.default
    return res


def update_func_kwargs(func, options):
    res_options = get_default_kwargs(func)
    for option_name, option_val in options.items():
        if option_name in res_options:
            res_options[option_name] = option_val
    return res_options


def get_class_name(class_object):
    return str(class_object).split(".")[-1].strip(">").strip("'").strip('"')


class DetectorTiltEstimator:
    """
    Helper class for detector tilt estimation.
    It automatically chooses the right radios and performs flat-field.
    """

    default_tilt_method = "1d-correlation"
    # Given a tilt angle "a", the maximum deviation caused by the tilt (in pixels) is
    #  N/2 * |sin(a)|  where N is the number of pixels
    # We ignore tilts causing less than 0.25 pixel deviation: N/2*|sin(a)| < tilt_threshold
    tilt_threshold = 0.25

    def __init__(self, dataset_info, do_flatfield=True, logger=None, autotilt_options=None):
        """
        Initialize a detector tilt estimator helper.

        Parameters
        ----------
        dataset_info: `dataset_info` object
            Data structure with the dataset information.
        do_flatfield: bool, optional
            Whether to perform flat field on radios.
        logger: `Logger` object, optional
            Logger object
        autotilt_options: dict, optional
            named arguments to pass to the detector tilt estimator class.
        """
        self._set_params(dataset_info, do_flatfield, logger, autotilt_options)
        self.radios, self.radios_indices = get_radio_pair(dataset_info, radio_angles=(0.0, np.pi), return_indices=True)
        self._init_flatfield()
        self._apply_flatfield()

    def _set_params(self, dataset_info, do_flatfield, logger, autotilt_options):
        self.dataset_info = dataset_info
        self.do_flatfield = bool(do_flatfield)
        self.logger = LoggerOrPrint(logger)
        self._get_autotilt_options(autotilt_options)

    def _init_flatfield(self):
        if not (self.do_flatfield):
            return
        self.flatfield = FlatField(
            self.radios.shape,
            flats=self.dataset_info.flats,
            darks=self.dataset_info.darks,
            radios_indices=self.radios_indices,
            interpolation="linear",
        )

    def _apply_flatfield(self):
        if not (self.do_flatfield):
            return
        self.flatfield.normalize_radios(self.radios)

    def _get_autotilt_options(self, autotilt_options):
        if autotilt_options is None:
            self.autotilt_options = None
            return
        try:
            autotilt_options = extract_parameters(autotilt_options)
        except Exception as exc:
            msg = "Could not extract parameters from autotilt_options: %s" % (str(exc))
            self.logger.fatal(msg)
            raise ValueError(msg)
        self.autotilt_options = autotilt_options
        if "threshold" in autotilt_options:
            self.tilt_threshold = autotilt_options.pop("threshold")

    def find_tilt(self, tilt_method=None):
        """
        Find the detector tilt.

        Parameters
        ----------
        tilt_method: str, optional
            Which tilt estimation method to use.
        """
        if tilt_method is None:
            tilt_method = self.default_tilt_method
        check_supported(tilt_method, set(tilt_methods.values()), "tilt estimation method")
        self.logger.info("Estimating detector tilt angle")
        autotilt_params = {
            "roi_yxhw": None,
            "median_filt_shape": None,
            "padding_mode": None,
            "peak_fit_radius": 1,
            "high_pass": None,
            "low_pass": None,
        }
        autotilt_params.update(self.autotilt_options or {})
        self.logger.debug("%s(%s)" % ("CameraTilt", str(autotilt_params)))

        tilt_calc = CameraTilt()
        tilt_cor_position, camera_tilt = tilt_calc.compute_angle(
            self.radios[0], np.fliplr(self.radios[1]), method=tilt_method, **autotilt_params
        )
        self.logger.info("Estimated detector tilt angle: %f degrees" % camera_tilt)
        # Ignore too small tilts
        max_deviation = np.max(self.dataset_info.radio_dims) * np.abs(np.sin(np.deg2rad(camera_tilt)))
        if self.dataset_info.is_halftomo:
            max_deviation *= 2
        if max_deviation < self.tilt_threshold:
            self.logger.info(
                "Estimated tilt angle (%.3f degrees) results in %.2f maximum pixels shift, which is below threshold (%.2f pixel). Ignoring the tilt, no correction will be done."
                % (camera_tilt, max_deviation, self.tilt_threshold)
            )
            camera_tilt = None
        return camera_tilt


# alias
TiltFinder = DetectorTiltEstimator


def estimate_translations(dataset_info, do_flatfield=True): ...


class TranslationsEstimator:

    _default_extra_options = {
        "window_size": 300,
    }

    def __init__(
        self,
        dataset_info,
        do_flatfield=True,
        rot_center=None,
        halftomo_side=None,
        angular_subsampling=10,
        deg_xy=2,
        deg_z=2,
        shifts_estimator="phase_cross_correlation",
        radios_filter=None,
        extra_options=None,
    ):
        self._configure_extra_options(extra_options)
        self.logger = LoggerOrPrint(dataset_info.logger)
        self.dataset_info = dataset_info
        self.angular_subsampling = angular_subsampling
        self.do_360 = self.dataset_info.is_360
        self.do_flatfield = do_flatfield
        self.radios_filter = radios_filter
        self.radios = None
        self._deg_xy = deg_xy
        self._deg_z = deg_z
        self._shifts_estimator = shifts_estimator
        self._shifts_estimator_kwargs = {}
        self._cor = rot_center
        self._configure_halftomo(halftomo_side)
        self._estimate_cor = self._cor is None
        self.sample_shifts_xy = None
        self.sample_shifts_z = None

    def _configure_extra_options(self, extra_options):
        self.extra_options = self._default_extra_options.copy()
        self.extra_options.update(extra_options or {})

    def _configure_halftomo(self, halftomo_side):
        if halftomo_side is False:
            # Force disable halftomo
            self.halftomo_side = False
            return
        self._start_x = None
        self._end_x = None
        if (halftomo_side is not None) and not (self.do_360):
            raise ValueError(
                "Expected 360° dataset for half-tomography, but this dataset does not look like a 360° dataset"
            )
        if halftomo_side is None:
            if self.dataset_info.is_halftomo:
                halftomo_side = "right"
            else:
                self.halftomo_side = False
                return
        self.halftomo_side = halftomo_side
        window_size = self.extra_options["window_size"]
        if self._cor is not None:
            # In this case we look for shifts around the CoR
            self._start_x = int(self._cor - window_size / 2)
            self._end_x = int(self._cor + window_size / 2)
        elif halftomo_side == "right":
            self._start_x = -window_size
            self._end_x = None
        elif halftomo_side == "left":
            self._start_x = 0
            self._end_x = window_size
        elif is_scalar(halftomo_side):
            # Expect approximate location of CoR, relative to left-most column
            self._start_x = int(halftomo_side - window_size / 2)
            self._end_x = int(halftomo_side + window_size / 2)
        else:
            raise ValueError(
                f"Expected 'halftomo_side' to be either 'left', 'right', or an integer (got {halftomo_side})"
            )
        self.logger.debug(f"[MotionEstimation] Half-tomo looking at [{self._start_x}:{self._end_x}]")
        # For half-tomo, skimage.registration.phase_cross_correlation might look a bit too far away
        if (
            self._shifts_estimator == "phase_cross_correlation"
            and self._shifts_estimator_kwargs.get("overlap_ratio", 0.3) >= 0.3
        ):
            self._shifts_estimator_kwargs.update({"overlap_ratio": 0.2})
        #

    def _load_data(self):
        self.logger.debug("[MotionEstimation] reading data")
        if self.do_360:
            """
            In this case we compare pair of opposite projections.
            If rotation angles are arbitrary, we should do something like
              for angle in dataset_info.rotation_angles:
                  img, angle_deg, idx = dataset_info.get_image_at_angle(
                      np.degrees(angle)+180, return_angle_and_index=True
                  )
            Most of the time (always ?), the dataset was acquired with a circular trajectory,
            so we can use angles:
                dataset_info.rotation_angles[::self.angular_subsampling]
            which amounts to reading one radio out of "angular_subsampling"
            """

            # TODO account for more general rotation angles. The following will only work for circular trajectory and ordered angles
            self._reader = self.dataset_info.get_reader(
                sub_region=(slice(None, None, self.angular_subsampling), slice(None), slice(None))
            )
            self.radios = self._reader.load_data()
            self.angles = self.dataset_info.rotation_angles[:: self.angular_subsampling]
            self._radios_idx = self._reader.get_frames_indices()
            self.logger.debug("[MotionEstimation] This is a 360° scan, will use pairs of opposite projections")
        else:
            """
            In this case we use the "return projections", i.e special projections acquired at several angles
            (eg. [180, 90, 0]) before ending the scan
            """
            return_projs, return_angles_deg, return_idx = self.dataset_info.get_alignment_projections()
            self._angles_return = np.radians(return_angles_deg)
            self._radios_return = return_projs
            self._radios_idx_return = return_idx

            projs = []
            angles_rad = []
            projs_idx = []
            for angle_deg in return_angles_deg:
                proj, rot_angle_deg, proj_idx = self.dataset_info.get_image_at_angle(
                    angle_deg, image_type="projection", return_angle_and_index=True
                )
                projs.append(proj)
                angles_rad.append(np.radians(rot_angle_deg))
                projs_idx.append(proj_idx)
            self._radios_outwards = np.array(projs)
            self._angles_outward = np.array(angles_rad)
            self._radios_idx_outwards = np.array(projs_idx)
            self.logger.debug("[MotionEstimation] This is a 180° scan, will use 'return projections'")

    def _apply_flatfield(self):
        if not (self.do_flatfield):
            return
        self.logger.debug("[MotionEstimation] flatfield")
        if self.do_360:
            self._flatfield = FlatField(
                self.radios.shape,
                flats=self.dataset_info.flats,
                darks=self.dataset_info.darks,
                radios_indices=self._radios_idx,
            )
            self._flatfield.normalize_radios(self.radios)
        else:
            # 180 + return projs
            self._flatfield_outwards = FlatField(
                self._radios_outwards.shape,
                flats=self.dataset_info.flats,
                darks=self.dataset_info.darks,
                radios_indices=self._radios_idx_outwards,
            )
            self._flatfield_outwards.normalize_radios(self._radios_outwards)
            self._flatfield_return = FlatField(
                self._radios_return.shape,
                flats=self.dataset_info.flats,
                darks=self.dataset_info.darks,
                radios_indices=self._radios_idx_return,
            )
            self._flatfield_outwards.normalize_radios(self._radios_return)

    def estimate_motion(self):
        self._load_data()
        self._apply_flatfield()
        if self.radios_filter is not None:
            self.logger.debug("[MotionEstimation] applying radios filter")
            self.radios_filter(self.radios)

        n_projs_tot = self.dataset_info.n_angles
        if self.do_360:
            n_a = self.radios.shape[0]
            # See notes above - this works only for circular trajectory / ordered angles
            projs_stack1 = self.radios[: n_a // 2]
            projs_stack2 = self.radios[n_a // 2 :]
            angles1 = self.angles[: n_a // 2]
            angles2 = self.angles[n_a // 2 :]
            indices1 = (self._radios_idx - self._radios_idx[0])[: n_a // 2]
            indices2 = (self._radios_idx - self._radios_idx[0])[n_a // 2 :]
        else:
            projs_stack1 = self._radios_outwards
            projs_stack2 = self._radios_return
            angles1 = self._angles_outward
            angles2 = self._angles_return
            indices1 = self._radios_idx_outwards - self._radios_idx_outwards.min()
            indices2 = self._radios_idx_return - self._radios_idx_outwards.min()

        if self._start_x is not None:
            # Compute Motion Estimation on subset of images (eg. for half-tomo)
            projs_stack1 = projs_stack1[..., self._start_x : self._end_x]
            projs_stack2 = projs_stack2[..., self._start_x : self._end_x]

        self.motion_estimator = MotionEstimation(
            projs_stack1,
            projs_stack2,
            angles1,
            angles2,
            indices1,
            indices2,
            n_projs_tot,
            shifts_estimator=self._shifts_estimator,
            shifts_estimator_kwargs=self._shifts_estimator_kwargs,
        )

        self.logger.debug("[MotionEstimation] estimating shifts")

        estimated_shifts_v = self.motion_estimator.estimate_vertical_motion(degree=self._deg_z)
        estimated_shifts_h, cor = self.motion_estimator.estimate_horizontal_motion(degree=self._deg_xy, cor=self._cor)
        if self._start_x is not None:
            cor += (self._start_x % self.radios.shape[-1]) + (projs_stack1.shape[-1] - 1) / 2.0

        self.sample_shifts_xy = estimated_shifts_h
        self.sample_shifts_z = estimated_shifts_v
        if self._cor is None:
            self.logger.info(
                "[MotionEstimation] Estimated center of rotation (relative to left-most pixel): %.2f" % cor
            )
        return estimated_shifts_h, estimated_shifts_v, cor

    def generate_translations_movements_file(self, filename, fmt="%.3f", only=None):
        if self.sample_shifts_xy is None:
            raise RuntimeError("Need to run estimate_motion() first")

        angles = self.dataset_info.rotation_angles
        cor = self._cor or 0
        txy_est_all_angles = self.motion_estimator.apply_fit_horiz(angles=angles)
        tz_est_all_angles = self.motion_estimator.apply_fit_vertic(angles=angles)
        estimated_shifts_vu_all_angles = self.motion_estimator.convert_sample_motion_to_detector_shifts(
            txy_est_all_angles, tz_est_all_angles, angles, cor=cor
        )
        estimated_shifts_vu_all_angles[:, 1] -= cor
        correct_shifts_uv = -estimated_shifts_vu_all_angles[:, ::-1]

        if only is not None:
            if only == "horizontal":
                correct_shifts_uv[:, 1] = 0
            elif only == "vertical":
                correct_shifts_uv[:, 0] = 0
            else:
                raise ValueError("Expected 'only' to be either None, 'horizontal' or 'vertical'")

        header = f"Generated by nabu {nabu_version} : {str(self)}"  # noqa: RUF010
        np.savetxt(filename, correct_shifts_uv, fmt=fmt, header=header)

    def __str__(self):
        ret = f"{self.__class__.__name__}(do_flatfield={self.do_flatfield}, rot_center={self._cor}, angular_subsampling={self.angular_subsampling})"
        if self.sample_shifts_xy is not None:
            ret += f", shifts_estimator={self.motion_estimator.shifts_estimator}"
        return ret
