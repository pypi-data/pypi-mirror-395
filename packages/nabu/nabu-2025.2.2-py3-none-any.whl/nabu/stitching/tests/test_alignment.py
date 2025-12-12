import numpy
import pytest
from nabu.stitching.alignment import align_horizontally, PaddedRawData
from nabu.testutils import get_data


def test_alignment_axis_2():
    """
    test 'align_horizontally' function
    """
    dataset = get_data("chelsea.npz")["data"]  # shape is (300, 451)

    # test if new_width < current_width: should raise an error
    with pytest.raises(ValueError):
        align_horizontally(dataset, alignment="center", new_width=10)

    # test some use cases
    res = align_horizontally(
        dataset,
        alignment="center",
        new_width=600,
        pad_mode="mean",
    )
    assert res.shape == (300, 600)
    numpy.testing.assert_array_almost_equal(res[:, 74:-75], dataset)

    res = align_horizontally(
        dataset,
        alignment="left",
        new_width=600,
        pad_mode="median",
    )
    assert res.shape == (300, 600)
    numpy.testing.assert_array_almost_equal(res[:, :451], dataset)

    res = align_horizontally(
        dataset,
        alignment="right",
        new_width=600,
        pad_mode="reflect",
    )
    assert res.shape == (300, 600)
    numpy.testing.assert_array_almost_equal(res[:, -451:], dataset)


def test_PaddedRawData():
    """
    test PaddedVolume class
    """
    data = numpy.linspace(
        start=0,
        stop=20 * 6 * 3,
        dtype=numpy.int64,
        num=20 * 6 * 3,
    )
    data = data.reshape((3, 6, 20))

    padded_volume = PaddedRawData(data=data, axis_1_pad_width=(4, 1))

    assert padded_volume.shape == (3, 6 + 4 + 1, 20)

    numpy.testing.assert_array_equal(
        padded_volume[:, 0, :],
        numpy.zeros(shape=(3, 1, 20), dtype=numpy.int64),
    )
    numpy.testing.assert_array_equal(
        padded_volume[:, 3, :],
        numpy.zeros(shape=(3, 1, 20), dtype=numpy.int64),
    )
    numpy.testing.assert_array_equal(
        padded_volume[:, 10, :],
        numpy.zeros(shape=(3, 1, 20), dtype=numpy.int64),
    )
    assert padded_volume[:, 3, :].shape == (3, 1, 20)
    numpy.testing.assert_array_equal(
        padded_volume[:, 4, :],
        data[:, 0:1, :],  # TODO: have a look, return a 3D array when a 2D expected...
    )

    with pytest.raises(ValueError):
        padded_volume[:, 40, :]
    with pytest.raises(ValueError):
        padded_volume[:, 5:1, :]

    arrays = (
        numpy.zeros(shape=(3, 4, 20), dtype=numpy.int64),
        data,
        numpy.zeros(shape=(3, 1, 20), dtype=numpy.int64),
    )
    expected_volume = numpy.hstack(
        arrays,
    )
    assert padded_volume[:, :, :].shape == padded_volume.shape
    assert expected_volume.shape == padded_volume.shape

    numpy.testing.assert_array_equal(
        padded_volume[:, :, :],
        expected_volume,
    )
