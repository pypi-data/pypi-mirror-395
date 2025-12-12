import os

import h5py
import numpy
import pytest
from tqdm import tqdm
from silx.image.phantomgenerator import PhantomGenerator
from tomoscan.esrf.volume import EDFVolume, HDF5Volume
from tomoscan.esrf.volume.tiffvolume import TIFFVolume, has_tifffile
from tomoscan.factory import Factory as TomoscanFactory
from tomoscan.utils.volume import concatenate as concatenate_volumes

from nabu.stitching.alignment import AlignmentAxis1, AlignmentAxis2
from nabu.stitching.config import NormalizationBySample, PostProcessedZStitchingConfiguration
from nabu.stitching.overlap import OverlapStitchingStrategy
from nabu.stitching.utils import ShiftAlgorithm
from nabu.stitching.z_stitching import PostProcessZStitcher, PostProcessZStitcherNoDD


strategies_to_test_weights = (
    OverlapStitchingStrategy.CLOSEST,
    OverlapStitchingStrategy.COSINUS_WEIGHTS,
    OverlapStitchingStrategy.LINEAR_WEIGHTS,
    OverlapStitchingStrategy.MEAN,
)


def build_raw_volume():
    """util to create some raw volume"""
    raw_volume = numpy.stack(
        [
            PhantomGenerator.get2DPhantomSheppLogan(n=120).astype(numpy.float32) * 256.0,
            PhantomGenerator.get2DPhantomSheppLogan(n=120).astype(numpy.float32) * 128.0,
            PhantomGenerator.get2DPhantomSheppLogan(n=120).astype(numpy.float32) * 32.0,
            PhantomGenerator.get2DPhantomSheppLogan(n=120).astype(numpy.float32) * 16.0,
        ]
    )
    assert raw_volume.shape == (4, 120, 120)
    raw_volume = numpy.rollaxis(raw_volume, axis=1, start=0)
    assert raw_volume.shape == (120, 4, 120)
    return raw_volume


_VOL_CLASSES_TO_TEST_FOR_POSTPROC_STITCHING = [HDF5Volume, EDFVolume]
# avoid testing glymur because doesn't handle float
# if has_minimal_openjpeg:
#     _VOL_CLASSES_TO_TEST_FOR_POSTPROC_STITCHING.append(JP2KVolume)
if has_tifffile:
    _VOL_CLASSES_TO_TEST_FOR_POSTPROC_STITCHING.append(TIFFVolume)


def build_volumes(output_dir: str, volume_class):
    # create some random data.
    raw_volume = build_raw_volume()

    # create a simple case where the volume have 10 voxel of overlap and a height (z) of 30 Voxels, 40 and 30 Voxels
    vol_1_constructor_params = {
        "data": raw_volume[0:30, :, :],
        "metadata": {
            "processing_options": {
                "reconstruction": {
                    "position": (-15.0, 0.0, 0.0),
                    "voxel_size_cm": (100.0, 100.0, 100.0),
                }
            },
        },
    }

    vol_2_constructor_params = {
        "data": raw_volume[20:80, :, :],
        "metadata": {
            "processing_options": {
                "reconstruction": {
                    "position": (-50.0, 0.0, 0.0),
                    "voxel_size_cm": (100.0, 100.0, 100.0),
                }
            },
        },
    }

    vol_3_constructor_params = {
        "data": raw_volume[60:, :, :],
        "metadata": {
            "processing_options": {
                "reconstruction": {
                    "position": (-90.0, 0.0, 0.0),
                    "voxel_size_cm": (100.0, 100.0, 100.0),
                }
            },
        },
    }

    volumes = []
    axis_0_positions = []
    for i_vol, vol_params in enumerate([vol_1_constructor_params, vol_2_constructor_params, vol_3_constructor_params]):
        if volume_class == HDF5Volume:
            vol_params.update(
                {
                    "file_path": os.path.join(output_dir, f"raw_volume_{i_vol}.hdf5"),
                    "data_path": "volume",
                }
            )
        else:
            vol_params.update(
                {
                    "folder": os.path.join(output_dir, f"raw_volume_{i_vol}"),
                }
            )
        axis_0_positions.append(vol_params["metadata"]["processing_options"]["reconstruction"]["position"][0])

        volume = volume_class(**vol_params)
        volume.save()
        volumes.append(volume)
    return volumes, axis_0_positions, raw_volume


@pytest.mark.parametrize("progress", (None, "with_tqdm"))
@pytest.mark.parametrize("volume_class", (_VOL_CLASSES_TO_TEST_FOR_POSTPROC_STITCHING))
def test_PostProcessZStitcher(
    tmp_path,
    volume_class,
    progress,
):
    """
    test PreProcessZStitcher class and insure a full stitching can be done automatically.

    :param bool clear_input_volumes_data: if True save the volume then clear volume.data (used to check internal management of loading volumes - used to check behavior with HDF5)
    :param volume_class: class to be used (same class for input and output for now)
    :param axis_0_pos: position of the different TomoObj along axis 0 (Also know as z axis)
    """
    if progress == "with_tqdm":
        progress = tqdm(total=100)

    # create folder to save data (and debug)
    raw_data_dir = tmp_path / "raw_data"
    raw_data_dir.mkdir()
    output_dir = tmp_path / "output_dir"
    output_dir.mkdir()

    volumes, axis_0_positions, raw_volume = build_volumes(output_dir=raw_data_dir, volume_class=volume_class)
    volume_1, volume_2, volume_3 = volumes

    output_volume = HDF5Volume(
        file_path=os.path.join(output_dir, "stitched_volume.hdf5"),
        data_path="stitched_volume",
    )

    z_stich_config = PostProcessedZStitchingConfiguration(
        stitching_strategy=OverlapStitchingStrategy.LINEAR_WEIGHTS,
        overwrite_results=True,
        input_volumes=(volume_1, volume_2, volume_3),
        output_volume=output_volume,
        slices=None,
        slurm_config=None,
        axis_0_pos_px=axis_0_positions,
        axis_0_pos_mm=None,
        axis_0_params={"img_reg_method": ShiftAlgorithm.NONE},
        axis_1_pos_px=None,
        axis_1_pos_mm=None,
        axis_1_params={"img_reg_method": ShiftAlgorithm.NONE},
        axis_2_pos_px=None,
        axis_2_pos_mm=None,
        axis_2_params={"img_reg_method": ShiftAlgorithm.NONE},
        slice_for_cross_correlation="middle",
        voxel_size=None,
    )

    stitcher = PostProcessZStitcher(z_stich_config, progress=progress)
    output_identifier = stitcher.stitch()
    assert output_identifier.file_path == output_volume.file_path
    assert output_identifier.data_path == output_volume.data_path

    output_volume.data = None
    output_volume.metadata = None
    output_volume.load_data(store=True)
    output_volume.load_metadata(store=True)

    assert raw_volume.shape == output_volume.data.shape

    numpy.testing.assert_array_almost_equal(raw_volume, output_volume.data)

    metadata = output_volume.metadata
    assert "about" in metadata
    assert "configuration" in metadata
    assert output_volume.position[0] == -60.0
    assert output_volume.pixel_size == (1.0, 1.0, 1.0)


slices_to_test_post = (
    {
        "slices": (None,),
        "complete": True,
    },
    {
        "slices": (("first",), ("middle",), ("last",)),
        "complete": False,
    },
    {
        "slices": ((0, 1, 2), slice(3, -1, 1)),
        "complete": True,
    },
)


@pytest.mark.parametrize("flip_ud", (True, False))
@pytest.mark.parametrize("configuration_dist", slices_to_test_post)
def test_DistributePostProcessZStitcher(tmp_path, configuration_dist, flip_ud):
    # create some random data.
    slices = configuration_dist["slices"]
    complete = configuration_dist["complete"]

    raw_volume = numpy.ones((80, 40, 120), dtype=numpy.float16)
    raw_volume[:, 0, :] = (
        PhantomGenerator.get2DPhantomSheppLogan(n=120).astype(numpy.float16)[30:110, :] * 80 * 40 * 120
    )
    raw_volume[:, 8, :] = (
        PhantomGenerator.get2DPhantomSheppLogan(n=120).astype(numpy.float16)[30:110, :] * 80 * 40 * 120 + 2
    )
    raw_volume[12] = 1.0
    raw_volume[:, 23] = 1.2
    # create folder to save data (and debug)
    raw_data_dir = tmp_path / "raw_data"
    raw_data_dir.mkdir()
    output_dir = tmp_path / "output_dir"
    output_dir.mkdir()

    def flip_input_data(data):
        if flip_ud:
            data = numpy.flipud(data)
        return data

    volume_1 = HDF5Volume(
        file_path=os.path.join(raw_data_dir, "volume_1.hdf5"),
        data_path="volume",
        data=flip_input_data(raw_volume[-60:, :, :]),
        metadata={
            "processing_options": {
                "reconstruction": {
                    "position": (-30.0, 0.0, 0.0),
                    "voxel_size_cm": (100.0, 100.0, 100.0),
                }
            },
        },
    )
    volume_1.save()

    volume_2 = HDF5Volume(
        file_path=os.path.join(raw_data_dir, "volume_2.hdf5"),
        data_path="volume",
        data=flip_input_data(raw_volume[:60, :, :]),
        metadata={
            "processing_options": {
                "reconstruction": {
                    "position": (-50.0, 0.0, 0.0),
                    "voxel_size_cm": (100.0, 100.0, 100.0),
                }
            },
        },
    )
    volume_2.save()

    reconstructed_sub_volumes = []
    for i_slice, s in enumerate(slices):
        output_volume = HDF5Volume(
            file_path=os.path.join(output_dir, f"stitched_subvolume_{i_slice}.hdf5"),
            data_path="stitched_volume",
        )
        volumes = (volume_2, volume_1)
        z_stich_config = PostProcessedZStitchingConfiguration(
            stitching_strategy=OverlapStitchingStrategy.LINEAR_WEIGHTS,
            axis_0_pos_px=tuple(
                volume.metadata["processing_options"]["reconstruction"]["position"][0] for volume in volumes
            ),
            axis_0_pos_mm=None,
            axis_0_params={},
            axis_1_pos_px=(0, 0),
            axis_1_pos_mm=None,
            axis_1_params={},
            axis_2_pos_px=None,
            axis_2_pos_mm=None,
            axis_2_params={},
            overwrite_results=True,
            input_volumes=volumes,
            output_volume=output_volume,
            slices=s,
            slurm_config=None,
            slice_for_cross_correlation="middle",
            voxel_size=None,
            flip_ud=flip_ud,
        )

        stitcher = PostProcessZStitcher(z_stich_config)
        vol_id = stitcher.stitch()
        reconstructed_sub_volumes.append(TomoscanFactory.create_tomo_object_from_identifier(identifier=vol_id))

    final_vol = HDF5Volume(
        file_path=os.path.join(output_dir, "final_volume"),
        data_path="volume",
    )
    if complete:
        concatenate_volumes(output_volume=final_vol, volumes=tuple(reconstructed_sub_volumes), axis=1)
        final_vol.load_data(store=True)
        numpy.testing.assert_almost_equal(
            raw_volume,
            final_vol.data,
        )


@pytest.mark.parametrize("alignment_axis_2", ("left", "right", "center"))
def test_vol_z_stitching_with_alignment_axis_2(tmp_path, alignment_axis_2):
    """
    test z volume stitching with different width (and so that requires image alignment over axis 2)
    """
    # create some random data.
    raw_volume = build_raw_volume()
    # create folder to save data (and debug)
    raw_data_dir = tmp_path / "raw_data"
    raw_data_dir.mkdir()
    output_dir = tmp_path / "output_dir"
    output_dir.mkdir()

    # create a simple case where the volume have 10 voxel of overlap and a height (z) of 30 Voxels, 40 and 30 Voxels
    vol_1_constructor_params = {
        "data": raw_volume[0:30, :, 4:-4],
        "metadata": {
            "processing_options": {
                "reconstruction": {
                    "position": (-15.0, 0.0, 0.0),
                    "voxel_size_cm": (100.0, 100.0, 100.0),
                }
            },
        },
    }

    vol_2_constructor_params = {
        "data": raw_volume[20:80, :, :],
        "metadata": {
            "processing_options": {
                "reconstruction": {
                    "position": (-50.0, 0.0, 0.0),
                    "voxel_size_cm": (100.0, 100.0, 100.0),
                }
            },
        },
    }

    vol_3_constructor_params = {
        "data": raw_volume[60:, :, 10:-10],
        "metadata": {
            "processing_options": {
                "reconstruction": {
                    "position": (-90.0, 0.0, 0.0),
                    "voxel_size_cm": (100.0, 100.0, 100.0),
                }
            },
        },
    }

    raw_volumes = []
    axis_0_positions = []
    for i_vol, vol_params in enumerate([vol_1_constructor_params, vol_2_constructor_params, vol_3_constructor_params]):
        vol_params.update(
            {
                "file_path": os.path.join(raw_data_dir, f"raw_volume_{i_vol}.hdf5"),
                "data_path": "volume",
            }
        )
        axis_0_positions.append(vol_params["metadata"]["processing_options"]["reconstruction"]["position"][0])
        volume = HDF5Volume(**vol_params)
        volume.save()
        raw_volumes.append(volume)

    volume_1, volume_2, volume_3 = raw_volumes

    output_volume = HDF5Volume(
        file_path=os.path.join(output_dir, "stitched_volume.hdf5"),
        data_path="stitched_volume",
    )

    z_stich_config = PostProcessedZStitchingConfiguration(
        stitching_strategy=OverlapStitchingStrategy.LINEAR_WEIGHTS,
        overwrite_results=True,
        input_volumes=(volume_1, volume_2, volume_3),
        output_volume=output_volume,
        slices=None,
        slurm_config=None,
        axis_0_pos_px=axis_0_positions,
        axis_0_pos_mm=None,
        axis_0_params={"img_reg_method": ShiftAlgorithm.NONE},
        axis_1_pos_px=None,
        axis_1_pos_mm=None,
        axis_1_params={"img_reg_method": ShiftAlgorithm.NONE},
        axis_2_pos_px=None,
        axis_2_pos_mm=None,
        axis_2_params={"img_reg_method": ShiftAlgorithm.NONE},
        slice_for_cross_correlation="middle",
        voxel_size=None,
        alignment_axis_2=AlignmentAxis2(alignment_axis_2),
    )

    stitcher = PostProcessZStitcher(z_stich_config, progress=None)
    output_identifier = stitcher.stitch()
    assert output_identifier.file_path == output_volume.file_path
    assert output_identifier.data_path == output_volume.data_path

    output_volume.load_data(store=True)
    output_volume.load_metadata(store=True)

    assert output_volume.data.shape == (120, 4, 120)

    if alignment_axis_2 == "center":
        numpy.testing.assert_array_almost_equal(raw_volume[:, :, 10:-10], output_volume.data[:, :, 10:-10])
    elif alignment_axis_2 == "left":
        numpy.testing.assert_array_almost_equal(raw_volume[:, :, :-20], output_volume.data[:, :, :-20])
    elif alignment_axis_2 == "right":
        numpy.testing.assert_array_almost_equal(raw_volume[:, :, 20:], output_volume.data[:, :, 20:])


@pytest.mark.parametrize("alignment_axis_1", ("front", "center", "back"))
def test_vol_z_stitching_with_alignment_axis_1(tmp_path, alignment_axis_1):
    """
    test z volume stitching with different number of frames (and so that requires image alignment over axis 0)
    """
    # create some random data.
    raw_volume = build_raw_volume()

    # create folder to save data (and debug)
    raw_data_dir = tmp_path / "raw_data"
    raw_data_dir.mkdir()
    output_dir = tmp_path / "output_dir"
    output_dir.mkdir()

    # create a simple case where the volume have 10 voxel of overlap and a height (z) of 30 Voxels, 40 and 30 Voxels
    vol_1_constructor_params = {
        "data": raw_volume[
            0:30,
            1:3,
        ],
        "metadata": {
            "processing_options": {
                "reconstruction": {
                    "position": (-15.0, 0.0, 0.0),
                    "voxel_size_cm": (100.0, 100.0, 100.0),
                }
            },
        },
    }

    vol_2_constructor_params = {
        "data": raw_volume[20:80, :, :],
        "metadata": {
            "processing_options": {
                "reconstruction": {
                    "position": (-50.0, 0.0, 0.0),
                    "voxel_size_cm": (100.0, 100.0, 100.0),
                }
            },
        },
    }

    vol_3_constructor_params = {
        "data": raw_volume[
            60:,
            1:3,
        ],
        "metadata": {
            "processing_options": {
                "reconstruction": {
                    "position": (-90.0, 0.0, 0.0),
                    "voxel_size_cm": (100.0, 100.0, 100.0),
                }
            },
        },
    }

    raw_volumes = []
    axis_0_positions = []
    for i_vol, vol_params in enumerate([vol_1_constructor_params, vol_2_constructor_params, vol_3_constructor_params]):
        vol_params.update(
            {
                "file_path": os.path.join(raw_data_dir, f"raw_volume_{i_vol}.hdf5"),
                "data_path": "volume",
            }
        )
        axis_0_positions.append(vol_params["metadata"]["processing_options"]["reconstruction"]["position"][0])
        volume = HDF5Volume(**vol_params)
        volume.save()
        raw_volumes.append(volume)

    volume_1, volume_2, volume_3 = raw_volumes

    output_volume = HDF5Volume(
        file_path=os.path.join(output_dir, "stitched_volume.hdf5"),
        data_path="stitched_volume",
    )

    z_stich_config = PostProcessedZStitchingConfiguration(
        stitching_strategy=OverlapStitchingStrategy.LINEAR_WEIGHTS,
        overwrite_results=True,
        input_volumes=(volume_1, volume_2, volume_3),
        output_volume=output_volume,
        slices=None,
        slurm_config=None,
        axis_0_pos_px=axis_0_positions,
        axis_0_pos_mm=None,
        axis_0_params={"img_reg_method": ShiftAlgorithm.NONE},
        axis_1_pos_px=None,
        axis_1_pos_mm=None,
        axis_1_params={"img_reg_method": ShiftAlgorithm.NONE},
        axis_2_pos_px=None,
        axis_2_pos_mm=None,
        axis_2_params={"img_reg_method": ShiftAlgorithm.NONE},
        slice_for_cross_correlation="middle",
        voxel_size=None,
        alignment_axis_1=AlignmentAxis1(alignment_axis_1),
    )

    stitcher = PostProcessZStitcher(z_stich_config, progress=None)
    output_identifier = stitcher.stitch()
    assert output_identifier.file_path == output_volume.file_path
    assert output_identifier.data_path == output_volume.data_path

    output_volume.load_data(store=True)
    output_volume.load_metadata(store=True)

    assert output_volume.data.shape == (120, 4, 120)

    if alignment_axis_1 == "middle":
        numpy.testing.assert_array_almost_equal(raw_volume[:, 10:-10, :], output_volume.data[:, 10:-10, :])
    elif alignment_axis_1 == "front":
        numpy.testing.assert_array_almost_equal(raw_volume[:, :-20, :], output_volume.data[:, :-20, :])
    elif alignment_axis_1 == "middle":
        numpy.testing.assert_array_almost_equal(raw_volume[:, 20:, :], output_volume.data[:, 20:, :])


def test_normalization_by_sample(tmp_path):
    """
    simple test of a volume stitching.
    Raw volumes have 'extra' values (+2, +5, +9) that must be removed at the end thanks to the normalization
    """
    raw_volume = build_raw_volume()
    # create folder to save data (and debug)
    raw_data_dir = tmp_path / "raw_data"
    raw_data_dir.mkdir()
    output_dir = tmp_path / "output_dir"
    output_dir.mkdir()

    # create a simple case where the volume have 10 voxel of overlap and a height (z) of 30 Voxels, 40 and 30 Voxels
    vol_1_constructor_params = {
        "data": raw_volume[0:30, :, :] + 3,
        "metadata": {
            "processing_options": {
                "reconstruction": {
                    "position": (-15.0, 0.0, 0.0),
                    "voxel_size_cm": (100.0, 100.0, 100.0),
                }
            },
        },
    }

    vol_2_constructor_params = {
        "data": raw_volume[20:80, :, :] + 5,
        "metadata": {
            "processing_options": {
                "reconstruction": {
                    "position": (-50.0, 0.0, 0.0),
                    "voxel_size_cm": (100.0, 100.0, 100.0),
                }
            },
        },
    }

    vol_3_constructor_params = {
        "data": raw_volume[60:, :, :] + 12,
        "metadata": {
            "processing_options": {
                "reconstruction": {
                    "position": (-90.0, 0.0, 0.0),
                    "voxel_size_cm": (100.0, 100.0, 100.0),
                }
            },
        },
    }

    raw_volumes = []
    axis_0_positions = []
    for i_vol, vol_params in enumerate([vol_1_constructor_params, vol_2_constructor_params, vol_3_constructor_params]):
        vol_params.update(
            {
                "file_path": os.path.join(raw_data_dir, f"raw_volume_{i_vol}.hdf5"),
                "data_path": "volume",
            }
        )

        axis_0_positions.append(vol_params["metadata"]["processing_options"]["reconstruction"]["position"][0])

        volume = HDF5Volume(**vol_params)
        volume.save()
        raw_volumes.append(volume)

    volume_1, volume_2, volume_3 = raw_volumes

    output_volume = HDF5Volume(
        file_path=os.path.join(output_dir, "stitched_volume.hdf5"),
        data_path="stitched_volume",
    )

    normalization_by_sample = NormalizationBySample()
    normalization_by_sample.set_is_active(True)
    normalization_by_sample.width = 1
    normalization_by_sample.margin = 0
    normalization_by_sample.side = "left"
    normalization_by_sample.method = "median"

    z_stich_config = PostProcessedZStitchingConfiguration(
        stitching_strategy=OverlapStitchingStrategy.CLOSEST,
        overwrite_results=True,
        input_volumes=(volume_1, volume_2, volume_3),
        output_volume=output_volume,
        slices=None,
        slurm_config=None,
        axis_0_pos_px=axis_0_positions,
        axis_0_pos_mm=None,
        axis_0_params={"img_reg_method": ShiftAlgorithm.NONE},
        axis_1_pos_px=None,
        axis_1_pos_mm=None,
        axis_1_params={"img_reg_method": ShiftAlgorithm.NONE},
        axis_2_pos_px=None,
        axis_2_pos_mm=None,
        axis_2_params={"img_reg_method": ShiftAlgorithm.NONE},
        slice_for_cross_correlation="middle",
        voxel_size=None,
        normalization_by_sample=normalization_by_sample,
    )

    stitcher = PostProcessZStitcher(z_stich_config, progress=None)
    output_identifier = stitcher.stitch()

    assert output_identifier.file_path == output_volume.file_path
    assert output_identifier.data_path == output_volume.data_path

    output_volume.data = None
    output_volume.metadata = None
    output_volume.load_data(store=True)
    output_volume.load_metadata(store=True)

    assert raw_volume.shape == output_volume.data.shape

    numpy.testing.assert_array_almost_equal(raw_volume, output_volume.data)

    metadata = output_volume.metadata
    assert "configuration" in metadata
    assert "about" in metadata
    assert metadata["about"]["program"] == "nabu-stitching"
    assert output_volume.position[0] == -60.0
    assert output_volume.pixel_size == (1.0, 1.0, 1.0)


@pytest.mark.parametrize("data_duplication", (True, False))
def test_data_duplication(tmp_path, data_duplication):
    """
    Test that the post-processing stitching can be done without duplicating data.
    And also making sure avoid data duplication can handle frame flips
    """
    raw_volume = build_raw_volume()

    # create folder to save data (and debug)
    raw_data_dir = tmp_path / "raw_data"
    raw_data_dir.mkdir()
    output_dir = tmp_path / "output_dir"
    output_dir.mkdir()

    volume_1 = HDF5Volume(
        data=raw_volume[0:30],
        metadata={
            "processing_options": {
                "reconstruction": {
                    "position": (-15.0, 0.0, 0.0),
                    "voxel_size_cm": (100.0, 100.0, 100.0),
                }
            },
        },
        file_path=os.path.join(raw_data_dir, f"raw_volume_1.hdf5"),
        data_path="volume",
    )

    volume_2 = HDF5Volume(
        data=raw_volume[20:80],
        metadata={
            "processing_options": {
                "reconstruction": {
                    "position": (-50.0, 0.0, 0.0),
                    "voxel_size_cm": (100.0, 100.0, 100.0),
                }
            },
        },
        file_path=os.path.join(raw_data_dir, f"raw_volume_2.hdf5"),
        data_path="volume",
    )

    volume_3 = HDF5Volume(
        data=raw_volume[60:],
        metadata={
            "processing_options": {
                "reconstruction": {
                    "position": (-90.0, 0.0, 0.0),
                    "voxel_size_cm": (100.0, 100.0, 100.0),
                }
            },
        },
        file_path=os.path.join(raw_data_dir, f"raw_volume_3.hdf5"),
        data_path="volume",
    )

    for volume in (volume_1, volume_2, volume_3):
        volume.save()
        volume.clear_cache()

    output_volume = HDF5Volume(
        file_path=os.path.join(output_dir, "stitched_volume.hdf5"),
        data_path="stitched_volume",
    )

    z_stich_config = PostProcessedZStitchingConfiguration(
        stitching_strategy=OverlapStitchingStrategy.CLOSEST,
        overwrite_results=True,
        input_volumes=(volume_1, volume_2, volume_3),
        output_volume=output_volume,
        slices=None,
        slurm_config=None,
        axis_0_pos_px=None,
        axis_0_pos_mm=None,
        axis_0_params={"img_reg_method": ShiftAlgorithm.NONE},
        axis_1_pos_px=None,
        axis_1_pos_mm=None,
        axis_1_params={"img_reg_method": ShiftAlgorithm.NONE},
        axis_2_pos_px=None,
        axis_2_pos_mm=None,
        axis_2_params={"img_reg_method": ShiftAlgorithm.NONE},
        slice_for_cross_correlation="middle",
        voxel_size=None,
        duplicate_data=data_duplication,
    )

    if data_duplication:
        stitcher = PostProcessZStitcher(z_stich_config, progress=None)
    else:
        stitcher = PostProcessZStitcherNoDD(z_stich_config, progress=None)
    output_identifier = stitcher.stitch()

    assert output_identifier.file_path == output_volume.file_path
    assert output_identifier.data_path == output_volume.data_path

    output_volume.data = None
    output_volume.metadata = None
    output_volume.load_data(store=True)
    output_volume.load_metadata(store=True)

    assert raw_volume.shape == output_volume.data.shape
    numpy.testing.assert_almost_equal(raw_volume.data, output_volume.data)

    with h5py.File(output_volume.file_path, mode="r") as h5f:
        if data_duplication:
            assert f"{output_volume.data_path}/stitching_regions" not in h5f
            assert not h5f[f"{output_volume.data_path}/results/data"].is_virtual
        else:
            assert f"{output_volume.data_path}/stitching_regions" in h5f
            assert h5f[f"{output_volume.data_path}/results/data"].is_virtual

    if not data_duplication:
        # make sure an error is raised if we try to ask for no data duplication and if we get some flips
        z_stich_config.flip_ud = (False, True, False)
        with pytest.raises(ValueError):  # noqa: PT012
            stitcher = PostProcessZStitcherNoDD(z_stich_config, progress=None)
            stitcher.stitch()
