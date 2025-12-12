import numpy
import pytest
from nabu.stitching.sample_normalization import normalize_frame


def test_normalize_frame():
    """
    test normalize_frame function
    """
    with pytest.raises(TypeError):
        normalize_frame("toto", "left", "median")
    with pytest.raises(TypeError):
        normalize_frame(numpy.linspace(0, 100), "left", "median")

    frame = numpy.ones((10, 40))
    frame[:, 15:25] = numpy.arange(1, 101, step=1).reshape((10, 10))

    numpy.testing.assert_array_equal(
        normalize_frame(
            frame=frame,
            side="left",
            method="mean",
            sample_width=10,
            margin_before_sample=2,
        )[:, 15:25],
        numpy.arange(0, 100, step=1).reshape((10, 10)),
    )

    numpy.testing.assert_array_equal(
        normalize_frame(
            frame=frame,
            side="right",
            method="median",
            sample_width=10,
            margin_before_sample=2,
        )[:, 15:25],
        numpy.arange(0, 100, step=1).reshape((10, 10)),
    )

    assert not numpy.array_equal(
        normalize_frame(
            frame=frame,
            side="right",
            method="mean",
            sample_width=10,
            margin_before_sample=20,
        )[:, 15:25],
        numpy.arange(0, 100, step=1).reshape((10, 10)),
    )
