from enum import Enum
import numpy


class SampleSide(Enum):
    LEFT = "left"
    RIGHT = "right"


class Method(Enum):
    MEAN = "mean"
    MEDIAN = "median"


def normalize_frame(
    frame: numpy.ndarray, side: SampleSide, method: Method, sample_width: int = 50, margin_before_sample: int = 0
):
    """
    normalize the frame from a sample section picked at the left of the right of the frame

    :param frame: frame to normalize
    :param SampleSide side: side to pick the sample
    :param Method method: normalization method
    :param int sample_width: sample width
    :param int margin: margin before the sampling area
    """
    if not isinstance(frame, numpy.ndarray):
        raise TypeError(f"Frame is expected to be a 2D numpy array.")
    if frame.ndim != 2:
        raise TypeError(f"Frame is expected to be a 2D numpy array. Get {frame.ndim}D")
    side = SampleSide(side)
    method = Method(method)

    if frame.shape[1] < sample_width + margin_before_sample:
        raise ValueError(
            f"frame width ({frame.shape[1]}) < sample_width + margin ({sample_width + margin_before_sample})"
        )

    # create sample
    if side is SampleSide.LEFT:
        sample_start = margin_before_sample
        sample_end = margin_before_sample + sample_width
        sample = frame[:, sample_start:sample_end]
    elif side is SampleSide.RIGHT:
        sample_start = frame.shape[1] - (sample_width + margin_before_sample)
        sample_end = frame.shape[1] - margin_before_sample
        sample = frame[:, sample_start:sample_end]
    else:
        raise ValueError(f"side {side.value} not handled")

    # do normalization
    if method is Method.MEAN:
        normalization_array = numpy.mean(sample, axis=1)
    elif method is Method.MEDIAN:
        normalization_array = numpy.median(sample, axis=1)
    else:
        raise ValueError(f"side {side.value} not handled")
    for line in range(normalization_array.shape[0]):
        frame[line, :] -= normalization_array[line]
    return frame
