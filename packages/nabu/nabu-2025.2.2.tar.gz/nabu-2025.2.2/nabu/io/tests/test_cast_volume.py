import numpy
from nabu.io.cast_volume import (
    cast_volume,
    clamp_and_rescale_data,
    find_histogram,
    get_default_output_volume,
)
from tomoscan.esrf.volume import (
    EDFVolume,
    HDF5Volume,
    JP2KVolume,
    MultiTIFFVolume,
    TIFFVolume,
)
from tomoscan.esrf.volume.jp2kvolume import has_glymur as __have_jp2k__
from tomoscan.esrf.scan.edfscan import EDFTomoScan
from tomoscan.esrf.scan.nxtomoscan import NXtomoScan
import pytest
import h5py
import os
from silx.io.url import DataUrl


@pytest.mark.skipif(not __have_jp2k__, reason="need jp2k (glymur) for this test")
def test_get_default_output_volume():
    """
    insure nabu.io.cast_volume is working properly
    """
    with pytest.raises(TypeError):
        # test input_volume type
        get_default_output_volume(input_volume="dsad/dsad/", output_type="jp2")

    with pytest.raises(ValueError):
        # test output value
        get_default_output_volume(input_volume=EDFVolume(folder="test"), output_type="toto")

    # test edf to jp2
    input_volume = EDFVolume(
        folder="/path/to/my_folder",
    )
    output_volume = get_default_output_volume(
        input_volume=input_volume,
        output_type="jp2",
    )
    assert isinstance(output_volume, JP2KVolume)
    assert output_volume.data_url.file_path() == "/path/to/vol_cast"
    assert output_volume.get_volume_basename() == "my_folder"

    # test hdf5 to tiff
    input_volume = HDF5Volume(
        file_path="/path/to/my_file.hdf5",
        data_path="entry0012",
    )

    output_volume = get_default_output_volume(
        input_volume=input_volume,
        output_type="tiff",
    )
    assert isinstance(output_volume, TIFFVolume)
    assert output_volume.data_url.file_path() == "/path/to/vol_cast/my_file"
    assert output_volume.get_volume_basename() == "my_file"

    # test Multitiff to hdf5
    input_volume = MultiTIFFVolume(
        file_path="my_file.tiff",
    )
    output_volume = get_default_output_volume(
        input_volume=input_volume,
        output_type="hdf5",
    )
    assert isinstance(output_volume, HDF5Volume)
    assert output_volume.data_url.file_path() == "vol_cast/my_file.hdf5"
    assert output_volume.data_url.data_path() == "volume/" + HDF5Volume.DATA_DATASET_NAME
    assert output_volume.metadata_url.file_path() == "vol_cast/my_file.hdf5"
    assert output_volume.metadata_url.data_path() == "volume/" + HDF5Volume.METADATA_GROUP_NAME

    # test jp2 to hdf5
    input_volume = JP2KVolume(
        folder="folder",
        volume_basename="basename",
    )
    output_volume = get_default_output_volume(
        input_volume=input_volume,
        output_type="hdf5",
    )
    assert isinstance(output_volume, HDF5Volume)
    assert output_volume.data_url.file_path() == "folder/vol_cast/basename.hdf5"
    assert output_volume.data_url.data_path() == f"/volume/{HDF5Volume.DATA_DATASET_NAME}"
    assert output_volume.metadata_url.file_path() == "folder/vol_cast/basename.hdf5"
    assert output_volume.metadata_url.data_path() == f"/volume/{HDF5Volume.METADATA_GROUP_NAME}"


def test_find_histogram_hdf5_volume(tmp_path):
    """
    test find_histogram function with hdf5 volume
    """
    h5_file = os.path.join(tmp_path, "test_file")
    with h5py.File(h5_file, mode="w") as h5f:
        h5f.require_group("myentry/histogram/results/data")

    # if volume url provided then can find it
    assert find_histogram(volume=HDF5Volume(file_path=h5_file, data_path="myentry")) == DataUrl(
        file_path=h5_file,
        data_path="myentry/histogram/results/data",
        scheme="silx",
    )

    assert find_histogram(volume=HDF5Volume(file_path=h5_file, data_path="entry")) is None


def test_find_histogram_single_frame_volume(tmp_path):
    """
    test find_histogram function with single frame volume

    TODO: improve: for now histogram file are created manually. If this can be more coupled with the "real" histogram generation it would be way better
    """
    # create volume and histogram
    volume = EDFVolume(
        folder=tmp_path,
        volume_basename="volume",
    )
    histogram_file = os.path.join(tmp_path, "volume_histogram.hdf5")
    with h5py.File(histogram_file, mode="w") as h5f:
        h5f.require_group("entry/histogram/results/data")

    # check behavior
    assert find_histogram(volume=volume) == DataUrl(
        file_path=histogram_file,
        data_path="entry/histogram/results/data",
        scheme="silx",
    )

    assert find_histogram(
        volume=volume,
        scan=EDFTomoScan(scan=str(tmp_path)),
    ) == DataUrl(
        file_path=histogram_file,
        data_path="entry/histogram/results/data",
        scheme="silx",
    )

    assert find_histogram(
        volume=volume,
        scan=NXtomoScan(scan=str(tmp_path), entry="entry"),
    ) == DataUrl(
        file_path=histogram_file,
        data_path="entry/histogram/results/data",
        scheme="silx",
    )


def test_find_histogram_multi_tiff_volume(tmp_path):
    """
    test find_histogram function with multi tiff frame volume

    TODO: improve: for now histogram file are created manually. If this can be more coupled with the "real" histogram generation it would be way better
    """
    # create volume and histogram
    tiff_file = os.path.join(tmp_path, "my_tiff.tif")
    volume = MultiTIFFVolume(
        file_path=tiff_file,
    )
    histogram_file = os.path.join(tmp_path, "my_tiff_histogram.hdf5")
    with h5py.File(histogram_file, mode="w") as h5f:
        h5f.require_group("entry/histogram/results/data")

    # check behavior
    assert find_histogram(volume=volume) == DataUrl(
        file_path=histogram_file,
        data_path="entry/histogram/results/data",
        scheme="silx",
    )

    assert find_histogram(
        volume=volume,
        scan=EDFTomoScan(scan=str(tmp_path)),
    ) == DataUrl(
        file_path=histogram_file,
        data_path="entry/histogram/results/data",
        scheme="silx",
    )

    assert find_histogram(
        volume=volume,
        scan=NXtomoScan(scan=str(tmp_path), entry="entry"),
    ) == DataUrl(
        file_path=histogram_file,
        data_path="entry/histogram/results/data",
        scheme="silx",
    )


@pytest.mark.parametrize("input_dtype", (numpy.float32, numpy.float64, numpy.uint8, numpy.uint16))
def test_clamp_and_rescale_data(input_dtype):
    """
    test 'rescale_data' function
    """
    array = numpy.linspace(
        start=1,
        stop=100,
        num=100,
        endpoint=True,
        dtype=input_dtype,
    ).reshape(10, 10)

    rescaled_array = clamp_and_rescale_data(
        data=array,
        new_min=10,
        new_max=90,
        rescale_min_percentile=20,  # provided to insure they will be ignored
        rescale_max_percentile=80,  # provided to insure they will be ignored
    )
    assert rescaled_array.min() == 10
    assert rescaled_array.max() == 90
    numpy.testing.assert_equal(rescaled_array.flatten()[0:10], numpy.array([10] * 10))
    numpy.testing.assert_equal(rescaled_array.flatten()[90:100], numpy.array([90] * 10))


def test_cast_volume(tmp_path):
    """
    test cast_volume
    """
    raw_data = numpy.linspace(
        start=1,
        stop=100,
        num=100,
        endpoint=True,
        dtype=numpy.float64,
    ).reshape(1, 10, 10)
    volume_hdf5_file_path = os.path.join(tmp_path, "myvolume.hdf5")
    volume_hdf5 = HDF5Volume(
        file_path=volume_hdf5_file_path,
        data_path="myentry",
        data=raw_data,
    )
    volume_edf = EDFVolume(
        folder=os.path.join(tmp_path, "volume_folder"),
    )

    # test when no histogram existing
    cast_volume(
        input_volume=volume_hdf5,
        output_volume=volume_edf,
        output_data_type=numpy.dtype(numpy.uint16),
        rescale_min_percentile=10,
        rescale_max_percentile=90,
        save=True,
        store=True,
    )
    # if percentiles 10 and 90 provided, no data_min and data_max then they will be computed from data min / max

    # append histogram
    with h5py.File(volume_hdf5_file_path, mode="a") as h5s:
        hist = numpy.array([20, 20, 20, 20, 20, 20])
        bins = numpy.array([0, 20, 40, 60, 80, 100])
        h5s["myentry/histogram/results/data"] = numpy.vstack((hist, bins))

    # and test it again
    volume_edf.overwrite = True
    cast_volume(
        input_volume=volume_hdf5,
        output_volume=volume_edf,
        output_data_type=numpy.dtype(numpy.uint16),
        rescale_min_percentile=20,
        rescale_max_percentile=60,
        save=True,
        store=True,
    )

    # test to cast the already cast volumes
    volume_tif = EDFVolume(
        folder=os.path.join(tmp_path, "second_volume_folder"),
    )
    volume_tif.overwrite = True
    cast_volume(
        input_volume=volume_edf,
        output_volume=volume_tif,
        output_data_type=numpy.dtype(numpy.uint8),
        save=True,
        store=True,
    )
    assert volume_tif.data.dtype == numpy.uint8

    volume_tif.overwrite = False
    with pytest.raises(OSError):
        cast_volume(
            input_volume=volume_edf,
            output_volume=volume_tif,
            output_data_type=numpy.dtype(numpy.uint8),
            save=True,
            store=True,
        )


@pytest.mark.skipif(not __have_jp2k__, reason="need jp2k (glymur) for this test")
def test_jp2k_compression_ratios(tmp_path):
    """
    simple test to make sure the compression ratios are handled
    """
    import glymur

    raw_data = numpy.random.random(
        size=(1, 2048, 2048),
    )
    raw_data *= 2048.000005
    volume_hdf5_file_path = os.path.join(tmp_path, "myvolume.hdf5")
    volume_hdf5 = HDF5Volume(
        file_path=volume_hdf5_file_path,
        data_path="myentry",
        data=raw_data,
    )

    volume_jp2k_ratios_0 = JP2KVolume(
        folder=os.path.join(tmp_path, "volume_folder"),
        cratios=(100, 10),
    )

    volume_jp2k_ratios_1 = JP2KVolume(
        folder=os.path.join(tmp_path, "volume_folder_2"),
        cratios=(1000, 100),
    )

    # test when no histogram existing
    cast_volume(
        input_volume=volume_hdf5,
        output_volume=volume_jp2k_ratios_0,
        output_data_type=numpy.dtype(numpy.uint16),
        save=True,
        store=True,
    )

    cast_volume(
        input_volume=volume_hdf5,
        output_volume=volume_jp2k_ratios_1,
        output_data_type=numpy.dtype(numpy.uint16),
        save=True,
        store=True,
    )

    # make sure the ratio have been taking into account
    frame_0 = glymur.Jp2k(next(volume_jp2k_ratios_0.browse_data_files()))
    frame_0.layer = 0

    frame_1 = glymur.Jp2k(next(volume_jp2k_ratios_1.browse_data_files()))
    frame_1.layer = 0

    assert not numpy.array_equal(frame_0, frame_1)
