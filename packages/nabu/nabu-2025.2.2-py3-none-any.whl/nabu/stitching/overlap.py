import numpy
import logging
from enum import Enum
from nabu.misc import fourier_filters
from scipy.fft import rfftn as local_fftn
from scipy.fft import irfftn as local_ifftn
from tomoscan.utils.geometry import BoundingBox1D

_logger = logging.getLogger(__name__)


class OverlapStitchingStrategy(Enum):
    MEAN = "mean"
    COSINUS_WEIGHTS = "cosinus weights"
    LINEAR_WEIGHTS = "linear weights"
    CLOSEST = "closest"
    IMAGE_MINIMUM_DIVERGENCE = "image minimum divergence"
    HIGHER_SIGNAL = "higher signal"


DEFAULT_OVERLAP_STRATEGY = OverlapStitchingStrategy.COSINUS_WEIGHTS

DEFAULT_OVERLAP_SIZE = None  # could also be an int
# default overlap to be take for stitching. Ig None: take the largest possible area


class OverlapKernelBase:
    pass


class ImageStichOverlapKernel(OverlapKernelBase):
    """
    Stitch two images along Y (axis 0 in image space)
    """

    DEFAULT_HIGH_FREQUENCY_THRESHOLD = 2

    def __init__(
        self,
        stitching_axis: int,
        frame_unstitched_axis_size: int,
        stitching_strategy: OverlapStitchingStrategy = DEFAULT_OVERLAP_STRATEGY,
        overlap_size: int = DEFAULT_OVERLAP_SIZE,
        extra_params: dict | None = None,
    ) -> None:
        """
        :param stitching_axis: axis along which stitching is operate. Must be in '0', '1'
        :param frame_unstitched_axis_size: according to the stitching axis the stitched framed will always have a constant size:
            * If stitching_axis == 0 then it will be the frame width
            * If stitching_axis == 1 then it will be the frame height
        :param stitching_strategy: strategy / algorithm to use in order to generate the stitching
        :param overlap_size: size (int) of the overlap (stitching) between the two images
        :param extra_params: possibly extra parameters to operate the stitching
        """
        from nabu.stitching.config import KEY_THRESHOLD_FREQUENCY  # avoid acylic import

        if not isinstance(overlap_size, int) and overlap_size > 0:
            raise TypeError(
                f"overlap_size is expected to be a positive int, {overlap_size} - not {overlap_size} ({type(overlap_size)})"
            )
        if not isinstance(frame_unstitched_axis_size, int) or not frame_unstitched_axis_size > 0:
            raise TypeError(
                f"frame_width is expected to be a positive int, {frame_unstitched_axis_size} - not {frame_unstitched_axis_size} ({type(frame_unstitched_axis_size)})"
            )

        if stitching_axis not in (0, 1):
            raise ValueError(
                "stitching_axis is expected to be the axis along which stitching must be done. It should be '0' or '1'"
            )

        self._stitching_axis = stitching_axis
        self._overlap_size = abs(overlap_size)
        self._frame_unstitched_axis_size = frame_unstitched_axis_size
        self._stitching_strategy = OverlapStitchingStrategy(stitching_strategy)
        self._weights_img_1 = None
        self._weights_img_2 = None
        if extra_params is None:
            extra_params = {}
        self._high_frequency_threshold = extra_params.get(
            KEY_THRESHOLD_FREQUENCY, self.DEFAULT_HIGH_FREQUENCY_THRESHOLD
        )

    def __str__(self) -> str:
        return f"z-stitching kernel (policy={self.stitching_strategy.value}, overlap_size={self.overlap_size}, frame={self._frame_unstitched_axis_size})"

    @staticmethod
    def __check_img(img, name):
        if not isinstance(img, numpy.ndarray) and img.ndim == 2:
            raise ValueError(f"{name} is expected to be 2D numpy array")

    @property
    def stitched_axis(self) -> int:
        return self._stitching_axis

    @property
    def unstitched_axis(self) -> int:
        """
        util function. The kernel is operating stitching on images along a single axis (`stitching_axis`).
        This property is returning the other axis.
        """
        if self.stitched_axis == 0:
            return 1
        else:
            return 0

    @property
    def overlap_size(self) -> int:
        return self._overlap_size

    @overlap_size.setter
    def overlap_size(self, size: int):
        if not isinstance(size, int):
            raise TypeError(f"height expects a int ({type(size)} provided instead)")
        if not size >= 0:
            raise ValueError(f"height is expected to be positive")
        self._overlap_size = abs(size)
        # update weights if needed
        if self._weights_img_1 is not None or self._weights_img_2 is not None:
            self.compute_weights()

    @property
    def img_2(self) -> numpy.ndarray:
        return self._img_2

    @property
    def weights_img_1(self) -> numpy.ndarray | None:
        return self._weights_img_1

    @property
    def weights_img_2(self) -> numpy.ndarray | None:
        return self._weights_img_2

    @property
    def stitching_strategy(self) -> OverlapStitchingStrategy:
        return self._stitching_strategy

    def compute_weights(self):
        if self.stitching_strategy is OverlapStitchingStrategy.MEAN:
            weights_img_1 = numpy.ones(self._overlap_size) * 0.5
            weights_img_2 = weights_img_1[::-1]
        elif self.stitching_strategy is OverlapStitchingStrategy.CLOSEST:
            n_item = self._overlap_size // 2 + self._overlap_size % 2
            weights_img_1 = numpy.concatenate(
                [
                    numpy.ones(n_item),
                    numpy.zeros(self._overlap_size - n_item),
                ]
            )
            weights_img_2 = numpy.concatenate(
                [
                    numpy.zeros(n_item),
                    numpy.ones(self._overlap_size - n_item),
                ]
            )
        elif self.stitching_strategy is OverlapStitchingStrategy.LINEAR_WEIGHTS:
            weights_img_1 = numpy.linspace(1.0, 0.0, self._overlap_size)
            weights_img_2 = weights_img_1[::-1]
        elif self.stitching_strategy is OverlapStitchingStrategy.COSINUS_WEIGHTS:
            angles = numpy.linspace(0.0, numpy.pi / 2.0, self._overlap_size)
            weights_img_1 = numpy.cos(angles) ** 2
            weights_img_2 = numpy.sin(angles) ** 2
        elif self.stitching_strategy in (
            OverlapStitchingStrategy.IMAGE_MINIMUM_DIVERGENCE,
            OverlapStitchingStrategy.HIGHER_SIGNAL,
        ):
            # those strategies are not using constant weights but have treatments depending on the provided img_1 and mg_2 during stitching
            return
        else:
            raise NotImplementedError(f"{self.stitching_strategy} not implemented")

        if self._stitching_axis == 0:
            self._weights_img_1 = weights_img_1.reshape(-1, 1) * numpy.ones(self._frame_unstitched_axis_size).reshape(
                1, -1
            )
            self._weights_img_2 = weights_img_2.reshape(-1, 1) * numpy.ones(self._frame_unstitched_axis_size).reshape(
                1, -1
            )
        elif self._stitching_axis == 1:
            self._weights_img_1 = weights_img_1.reshape(1, -1) * numpy.ones(self._frame_unstitched_axis_size).reshape(
                -1, 1
            )
            self._weights_img_2 = weights_img_2.reshape(1, -1) * numpy.ones(self._frame_unstitched_axis_size).reshape(
                -1, 1
            )
        else:
            raise ValueError(f"stitching_axis should be in (0, 1). {self._stitching_axis} provided")

    def stitch(self, img_1, img_2, check_input=True) -> tuple:
        """Compute overlap region from the defined strategy"""
        if check_input:
            self.__check_img(img_1, "img_1")
            self.__check_img(img_2, "img_2")

            if img_1.shape != img_2.shape:
                raise ValueError(
                    f"both images are expected to be of the same shape to apply stitch ({img_1.shape} vs {img_2.shape})"
                )

        if self._stitching_strategy is OverlapStitchingStrategy.IMAGE_MINIMUM_DIVERGENCE:
            return (
                compute_image_minimum_divergence(
                    img_1=img_1,
                    img_2=img_2,
                    high_frequency_threshold=self._high_frequency_threshold,
                    stitching_axis=self.stitched_axis,
                ),
                None,
                None,
            )
        elif self._stitching_strategy is OverlapStitchingStrategy.HIGHER_SIGNAL:
            return (
                compute_image_higher_signal(
                    img_1=img_1,
                    img_2=img_2,
                ),
                None,
                None,
            )
        else:
            if self.weights_img_1 is None or self.weights_img_2 is None:
                self.compute_weights()

            return (
                img_1 * self.weights_img_1 + img_2 * self.weights_img_2,
                self.weights_img_1,
                self.weights_img_2,
            )


def compute_image_minimum_divergence(
    img_1: numpy.ndarray, img_2: numpy.ndarray, high_frequency_threshold, stitching_axis: int
):
    """
    Algorithm to improve treatment of high frequency.

    It split the two images into two parts: high frequency and low frequency.

    The two low frequency part will be stitched using a 'sinusoidal' / cosinus weights approach.
    When the two high frequency parts will be stitched by taking the lower divergent pixels
    """

    # split low and high frequencies
    def split_image(image: numpy.ndarray, threshold: int) -> tuple:
        """split an image to return (low_frequency, high_frequency)"""

        lowpass_filter = fourier_filters.get_lowpass_filter(
            image.shape[-2:],
            cutoff_par=threshold,
            use_rfft=True,
            data_type=image.dtype,
        )
        highpass_filter = fourier_filters.get_highpass_filter(
            image.shape[-2:],
            cutoff_par=threshold,
            use_rfft=True,
            data_type=image.dtype,
        )
        low_fre_part = local_ifftn(local_fftn(image, axes=(-2, -1)) * lowpass_filter, axes=(-2, -1)).real
        high_fre_part = local_ifftn(local_fftn(image, axes=(-2, -1)) * highpass_filter, axes=(-2, -1)).real
        return (low_fre_part, high_fre_part)

    low_freq_img_1, high_freq_img_1 = split_image(img_1, threshold=high_frequency_threshold)
    low_freq_img_2, high_freq_img_2 = split_image(img_2, threshold=high_frequency_threshold)

    # handle low frequency
    if stitching_axis == 0:
        frame_cst_size = img_1.shape[1]
        overlap_size = img_1.shape[0]
    elif stitching_axis == 1:
        frame_cst_size = img_1.shape[0]
        overlap_size = img_1.shape[1]
    else:
        raise ValueError("")

    low_freq_stitching_kernel = ImageStichOverlapKernel(
        frame_unstitched_axis_size=frame_cst_size,
        stitching_strategy=OverlapStitchingStrategy.COSINUS_WEIGHTS,
        overlap_size=overlap_size,
        stitching_axis=stitching_axis,
    )
    low_freq_stitched = low_freq_stitching_kernel.stitch(
        img_1=low_freq_img_1,
        img_2=low_freq_img_2,
        check_input=False,
    )[0]

    # handle high frequency
    mean_high_frequency = numpy.mean([high_freq_img_1, high_freq_img_2])
    assert numpy.isscalar(mean_high_frequency)
    high_freq_distance_img_1 = numpy.abs(high_freq_img_1 - mean_high_frequency)
    high_freq_distance_img_2 = numpy.abs(high_freq_img_2 - mean_high_frequency)
    high_freq_stitched = numpy.where(
        high_freq_distance_img_1 >= high_freq_distance_img_2, high_freq_distance_img_2, high_freq_distance_img_1
    )

    # merge back low and high frequencies together
    def merge_images(low_freq: numpy.ndarray, high_freq: numpy.ndarray) -> numpy.ndarray:
        """merge two part of an image. The low frequency part with the high frequency part"""
        return low_freq + high_freq

    return merge_images(low_freq_stitched, high_freq_stitched)


def compute_image_higher_signal(img_1: numpy.ndarray, img_2: numpy.ndarray):
    """
    the higher signal will pick pixel on the image having the higher signal.
    A use case is that if there is some artefacts on images which creates stripes (from scintillator artefacts for example)
    it could be removed from this method
    """
    # note: to be think about. But maybe it can be interesting to rescale img_1 and img_2
    # to ge something more coherent
    return numpy.where(img_1 >= img_2, img_1, img_2)


def check_overlaps(frames: tuple | numpy.ndarray, positions: tuple, axis: int, raise_error: bool):
    """
    check over frames if there is a single overlap other juxtaposed frames (at most and at least)

    :param frames: liste of ordered / sorted frames along axis to test (from higher to lower)
    :param positions: positions of frames in 3D space as (position axis 0, position axis 1, position axis 2)
    :param axis: axis to check
    :param raise_error: if True then raise an error if two frames don't have at least and at most one overlap. Else log an error
    """
    if not isinstance(frames, (tuple, numpy.ndarray)):
        raise TypeError(f"frames is expected to be a tuple or a numpy array. Get {type(frames)} instead")
    if not isinstance(positions, tuple) and len(positions) == 3:
        raise TypeError(f"positions is expected to be a tuple of 3 elements. Get {type(positions)} instead")
    assert isinstance(axis, int), "axis is expected to be an int"
    assert isinstance(raise_error, bool), "raise_error is expected to be a bool"

    def treat_error(error_msg: str):
        if raise_error:
            raise ValueError(error_msg)
        else:
            _logger.error(raise_error)

    if axis == 0:
        axis_frame_space = 0
    elif axis == 2:
        raise NotImplementedError(f"overlap check along axis {axis_frame_space}")
    elif axis == 1:
        axis_frame_space = 1

    # convert each frame to appropriate bounding box according to the axis
    def convert_to_bb(frame: numpy.ndarray, position: tuple, axis: int):
        assert isinstance(axis, int)
        assert isinstance(position, tuple), f"position expected a tuple. Get {type(position)} instead"
        assert len(position) == 3, f"Expect to have three items for the position. Get {len(position)}"
        start_frame = position[axis] - frame.shape[axis_frame_space] // 2
        end_frame = start_frame + frame.shape[axis_frame_space]
        return BoundingBox1D(start_frame, end_frame)

    bounding_boxes = {
        convert_to_bb(frame=frame, position=position, axis=axis): position for frame, position in zip(frames, positions)
    }

    def get_frame_index(my_bb) -> str:
        bb_index = tuple(bounding_boxes.keys()).index(my_bb) + 1
        if bb_index in (1, 21, 31):
            return f"{bb_index}st"
        elif bb_index in (2, 22, 32):
            return f"{bb_index}nd"
        elif bb_index == (3, 23, 33):
            return f"{bb_index}rd"
        else:
            return f"{bb_index}th"

    # check that theres an overlap between two juxtaposed bb (or frame at the end)
    all_bounding_boxes = tuple(bounding_boxes.keys())
    bb_with_expected_overlap = [
        (bb_frame, bb_next_frame) for bb_frame, bb_next_frame in zip(all_bounding_boxes[:-1], all_bounding_boxes[1:])
    ]

    for bb_pair in bb_with_expected_overlap:
        bb_frame, bb_next_frame = bb_pair
        if bb_frame.max < bb_next_frame.min:
            treat_error(f"provided frames seems un sorted (from the higher to the lower)")
        if bb_frame.min < bb_next_frame.min:
            treat_error(
                f"Seems like {get_frame_index(bb_frame)} frame is fully overlaping with frame {get_frame_index(bb_next_frame)}"
            )
        if bb_frame.get_overlap(bb_next_frame) is None:
            treat_error(
                f"no overlap found between two juxtaposed frames - {get_frame_index(bb_frame)} and {get_frame_index(bb_next_frame)}"
            )

    # check there is no overlap between none juxtaposed bb
    def pick_all_none_juxtaposed_bb(index, my_bounding_boxes: tuple):
        """return all the bounding boxes to check for the index 'index':

        :return: (tested_bounding_box, bounding_boxes_to_test)
        """
        my_bounding_boxes = {bb_index: bb for bb_index, bb in enumerate(my_bounding_boxes)}
        bounding_boxes = dict(
            filter(
                lambda pair: pair[0] not in (index - 1, index, index + 1),
                my_bounding_boxes.items(),
            )
        )
        return my_bounding_boxes[index], bounding_boxes.values()

    bb_without_expected_overlap = [
        pick_all_none_juxtaposed_bb(index, all_bounding_boxes) for index in range(len(all_bounding_boxes))
    ]

    for bb_pair in bb_without_expected_overlap:
        bb_frame, bb_not_juxtaposed_frames = bb_pair
        for bb_not_juxtaposed_frame in bb_not_juxtaposed_frames:
            if bb_frame.get_overlap(bb_not_juxtaposed_frame) is not None:
                treat_error(
                    f"overlap found between two frames not juxtaposed - {bounding_boxes[bb_frame]} and {bounding_boxes[bb_not_juxtaposed_frame]}"
                )
