import os
import pint
from silx.image.phantomgenerator import PhantomGenerator
from scipy.ndimage import shift as scipy_shift
import numpy
import pytest
from nabu.stitching.config import PreProcessedZStitchingConfiguration
from nabu.stitching.config import KEY_IMG_REG_METHOD
from nabu.stitching.overlap import OverlapStitchingStrategy
from nabu.stitching.z_stitching import (
    PreProcessZStitcher,
)
from nabu.stitching.stitcher_2D import get_overlap_areas
from nxtomo.nxobject.nxdetector import ImageKey
from nxtomo.utils.transformation import DetYFlipTransformation, DetZFlipTransformation
from nxtomo.application.nxtomo import NXtomo
from tomoscan.esrf.scan.nxtomoscan import NXtomoScan
from nabu.stitching.utils import ShiftAlgorithm
import h5py

_ureg = pint.get_application_registry()


_stitching_configurations = (
    # simple case where shifts are provided
    {
        "n_proj": 4,
        "raw_pos": ((0, 0, 0), (-90, 0, 0), (-180, 0, 0)),  # requested shift to
        "input_pos": ((0, 0, 0), (-90, 0, 0), (-180, 0, 0)),  # requested shift to
        "raw_shifts": ((0, 0), (-90, 0), (-180, 0)),
    },
    # simple case where shift is found from z position
    {
        "n_proj": 4,
        "raw_pos": ((90, 0, 0), (0, 0, 0), (-90, 0, 0)),
        "input_pos": ((90, 0, 0), (0, 0, 0), (-90, 0, 0)),
        "check_bb": ((40, 140), (-50, 50), (-140, -40)),
        "axis_0_params": {
            KEY_IMG_REG_METHOD: ShiftAlgorithm.NONE,
        },
        "axis_2_params": {
            KEY_IMG_REG_METHOD: ShiftAlgorithm.NONE,
        },
        "raw_shifts": ((0, 0), (-90, 0), (-180, 0)),
    },
)


@pytest.mark.parametrize("configuration", _stitching_configurations)
@pytest.mark.parametrize("dtype", (numpy.float32, numpy.int16))
def test_PreProcessZStitcher(tmp_path, dtype, configuration):
    """
    test PreProcessZStitcher class and insure a full stitching can be done automatically.
    """
    n_proj = configuration["n_proj"]
    ref_frame_width = 280
    raw_frame_height = 100
    ref_frame = PhantomGenerator.get2DPhantomSheppLogan(n=ref_frame_width).astype(dtype) * 256.0

    # add some mark for image registration
    ref_frame[:, 96] = -3.2
    ref_frame[:, 125] = 9.1
    ref_frame[:, 165] = 4.4
    ref_frame[:, 200] = -2.5
    # create raw data
    frame_0_shift, frame_1_shift, frame_2_shift = configuration["raw_shifts"]
    frame_0 = scipy_shift(ref_frame, shift=frame_0_shift)[:raw_frame_height]
    frame_1 = scipy_shift(ref_frame, shift=frame_1_shift)[:raw_frame_height]
    frame_2 = scipy_shift(ref_frame, shift=frame_2_shift)[:raw_frame_height]

    frames = frame_0, frame_1, frame_2
    frame_0_input_pos, frame_1_input_pos, frame_2_input_pos = configuration["input_pos"]
    frame_0_raw_pos, frame_1_raw_pos, frame_2_raw_pos = configuration["raw_pos"]

    # create a Nxtomo for each of those raw data
    raw_data_dir = tmp_path / "raw_data"
    raw_data_dir.mkdir()
    output_dir = tmp_path / "output_dir"
    output_dir.mkdir()
    z_position = (
        frame_0_raw_pos[0],
        frame_1_raw_pos[0],
        frame_2_raw_pos[0],
    )
    scans = []
    for (i_frame, frame), z_pos in zip(enumerate(frames), z_position):
        nx_tomo = NXtomo()
        # warning: nabu uses esrf coordiante system, nxtomo McStas (mapping z -> y)
        nx_tomo.sample.y_translation = ([z_pos] * n_proj) * _ureg.meter
        nx_tomo.sample.rotation_angle = numpy.linspace(0, 180, num=n_proj, endpoint=False) * _ureg.degree
        nx_tomo.instrument.detector.image_key_control = [ImageKey.PROJECTION] * n_proj
        nx_tomo.instrument.detector.x_pixel_size = 1.0 * _ureg.meter
        nx_tomo.instrument.detector.y_pixel_size = 1.0 * _ureg.meter
        nx_tomo.instrument.detector.distance = 2.3 * _ureg.meter
        nx_tomo.energy = 19.2 * _ureg.keV
        nx_tomo.instrument.detector.data = numpy.asarray([frame] * n_proj)

        file_path = os.path.join(raw_data_dir, f"nxtomo_{i_frame}.nx")
        entry = f"entry000{i_frame}"
        nx_tomo.save(file_path=file_path, data_path=entry)
        scans.append(NXtomoScan(scan=file_path, entry=entry))

    # if requested: check bounding box
    check_bb = configuration.get("check_bb", None)
    if check_bb is not None:
        for scan, expected_bb in zip(scans, check_bb):
            assert scan.get_bounding_box(axis="z") == expected_bb
    output_file_path = os.path.join(output_dir, "stitched.nx")
    output_data_path = "stitched"
    z_stich_config = PreProcessedZStitchingConfiguration(
        stitching_strategy=OverlapStitchingStrategy.LINEAR_WEIGHTS,
        overwrite_results=True,
        axis_0_pos_px=(
            frame_0_input_pos[0],
            frame_1_input_pos[0],
            frame_2_input_pos[0],
        ),
        axis_1_pos_px=(
            frame_0_input_pos[1],
            frame_1_input_pos[1],
            frame_2_input_pos[1],
        ),
        axis_2_pos_px=(
            frame_0_input_pos[2],
            frame_1_input_pos[2],
            frame_2_input_pos[2],
        ),
        axis_0_pos_mm=None,
        axis_1_pos_mm=None,
        axis_2_pos_mm=None,
        input_scans=scans,
        output_file_path=output_file_path,
        output_data_path=output_data_path,
        axis_0_params=configuration.get("axis_0_params", {}),
        axis_1_params=configuration.get("axis_1_params", {}),
        axis_2_params=configuration.get("axis_2_params", {}),
        output_nexus_version=None,
        slices=None,
        slurm_config=None,
        slice_for_cross_correlation="middle",
        pixel_size=None,
    )
    stitcher = PreProcessZStitcher(z_stich_config)
    output_identifier = stitcher.stitch()
    assert output_identifier.file_path == output_file_path
    assert output_identifier.data_path == output_data_path

    created_nx_tomo = NXtomo().load(
        file_path=output_identifier.file_path,
        data_path=output_identifier.data_path,
        detector_data_as="as_numpy_array",
    )

    assert created_nx_tomo.instrument.detector.data.ndim == 3
    mean_abs_error = configuration.get("mean_abs_error", None)
    if mean_abs_error is not None:
        assert (
            numpy.mean(numpy.abs(ref_frame - created_nx_tomo.instrument.detector.data[0, :ref_frame_width, :]))
            < mean_abs_error
        )
    else:
        numpy.testing.assert_array_almost_equal(
            ref_frame, created_nx_tomo.instrument.detector.data[0, :ref_frame_width, :]
        )

    # check also other metadata are here
    assert created_nx_tomo.instrument.detector.distance == 2.3 * _ureg.meter
    assert created_nx_tomo.energy == 19.2 * _ureg.keV
    numpy.testing.assert_array_equal(
        created_nx_tomo.instrument.detector.image_key_control,
        numpy.asarray([ImageKey.PROJECTION.PROJECTION] * n_proj),
    )

    # check configuration has been saved
    with h5py.File(output_identifier.file_path, mode="r") as h5f:
        assert "stitching_configuration" in h5f[output_identifier.data_path]


slices_to_test_pre = (
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


def build_nxtomos(output_dir) -> tuple:
    r"""
    build two nxtomos in output_dir and return the list of NXtomos ready to be stitched
       /\
       |        ______________
       |       |  nxtomo 1    |
    Z* |       |  frame       |
       |       |~~~~~~~~~~~~~~|
       |       |~~~~~~~~~~~~~~|
       |       |______________|
       |        ______________
       |       |~~~~~~~~~~~~~~|
       |       |~~~~~~~~~~~~~~|
       |       |  nxtomo 2    |
       |       |  frame       |
       |       |______________|
       |
    <-----------------------------------------------
                    y (in acquisition space)

    * ~: represent the overlap area
    Z*: Z in esrf coordinate system (== Y in McStas coordinate system)
    """
    n_projs = 100
    raw_data = numpy.arange(100 * 128 * 128).reshape((100, 128, 128))

    # create raw data
    frame_0 = raw_data[:, 60:]
    assert frame_0.ndim == 3
    frame_0_pos = 40
    frame_1 = raw_data[:, 0:80]
    assert frame_1.ndim == 3
    frame_1_pos = 94
    frames = (frame_0, frame_1)
    z_positions = (frame_0_pos, frame_1_pos)

    # create a Nxtomo for each of those raw data

    scans = []
    for (i_frame, frame), z_pos in zip(enumerate(frames), z_positions):
        nx_tomo = NXtomo()
        # warning: mapping esrf coordiante system to McStas
        nx_tomo.sample.y_translation = [z_pos] * n_projs * _ureg.meter
        nx_tomo.sample.rotation_angle = numpy.linspace(0, 180, num=n_projs, endpoint=False) * _ureg.degree
        nx_tomo.instrument.detector.image_key_control = [ImageKey.PROJECTION] * n_projs
        nx_tomo.instrument.detector.x_pixel_size = 1.0 * _ureg.meter
        nx_tomo.instrument.detector.y_pixel_size = 1.0 * _ureg.meter
        nx_tomo.instrument.detector.distance = 2.3 * _ureg.meter
        nx_tomo.energy = 19.2 * _ureg.keV
        nx_tomo.instrument.detector.data = frame

        file_path = os.path.join(output_dir, f"nxtomo_{i_frame}.nx")
        entry = f"entry000{i_frame}"
        nx_tomo.save(file_path=file_path, data_path=entry)
        scans.append(NXtomoScan(scan=file_path, entry=entry))
    return scans, z_positions, raw_data


@pytest.mark.parametrize("configuration_dist", slices_to_test_pre)
def test_DistributePreProcessZStitcher(tmp_path, configuration_dist):
    slices = configuration_dist["slices"]
    complete = configuration_dist["complete"]

    raw_data_dir = tmp_path / "raw_data"
    raw_data_dir.mkdir()

    output_dir = tmp_path / "output_dir"
    output_dir.mkdir()

    scans, z_positions, raw_data = build_nxtomos(output_dir=raw_data_dir)
    stitched_nx_tomo = []
    for s in slices:
        output_file_path = os.path.join(output_dir, "stitched_section.nx")
        output_data_path = f"stitched_{s}"
        z_stich_config = PreProcessedZStitchingConfiguration(
            axis_0_pos_px=z_positions,
            axis_1_pos_px=(0, 0),
            axis_2_pos_px=None,
            axis_0_pos_mm=None,
            axis_1_pos_mm=None,
            axis_2_pos_mm=None,
            axis_0_params={},
            axis_1_params={},
            axis_2_params={},
            stitching_strategy=OverlapStitchingStrategy.CLOSEST,
            overwrite_results=True,
            input_scans=scans,
            output_file_path=output_file_path,
            output_data_path=output_data_path,
            output_nexus_version=None,
            slices=s,
            slurm_config=None,
            slice_for_cross_correlation="middle",
            pixel_size=None,
        )
        stitcher = PreProcessZStitcher(z_stich_config)
        output_identifier = stitcher.stitch()
        assert output_identifier.file_path == output_file_path
        assert output_identifier.data_path == output_data_path

        created_nx_tomo = NXtomo().load(
            file_path=output_identifier.file_path,
            data_path=output_identifier.data_path,
            detector_data_as="as_numpy_array",
        )
        stitched_nx_tomo.append(created_nx_tomo)
    assert len(stitched_nx_tomo) == len(slices)
    final_nx_tomo = NXtomo.concatenate(stitched_nx_tomo)
    assert isinstance(final_nx_tomo.instrument.detector.data, numpy.ndarray)
    final_nx_tomo.save(
        file_path=os.path.join(output_dir, "final_stitched.nx"),
        data_path="entry0000",
    )

    if complete:
        assert len(final_nx_tomo.instrument.detector.data) == 100
        # test middle
        numpy.testing.assert_array_almost_equal(raw_data[1], final_nx_tomo.instrument.detector.data[1, :, :])
    else:
        assert len(final_nx_tomo.instrument.detector.data) == 3
        # test middle
        numpy.testing.assert_array_almost_equal(raw_data[49], final_nx_tomo.instrument.detector.data[1, :, :])
    # in the case of first, middle and last frames
    # test first
    numpy.testing.assert_array_almost_equal(raw_data[0], final_nx_tomo.instrument.detector.data[0, :, :])

    # test last
    numpy.testing.assert_array_almost_equal(raw_data[-1], final_nx_tomo.instrument.detector.data[-1, :, :])


def test_get_overlap_areas():
    """test get_overlap_areas function"""
    f_upper = numpy.linspace(7, 15, num=9, endpoint=True)
    f_lower = numpy.linspace(0, 12, num=13, endpoint=True)

    o_1, o_2 = get_overlap_areas(
        upper_frame=f_upper,
        lower_frame=f_lower,
        upper_frame_key_line=3,
        lower_frame_key_line=10,
        overlap_size=4,
        stitching_axis=0,
    )

    numpy.testing.assert_array_equal(o_1, o_2)
    numpy.testing.assert_array_equal(o_1, numpy.linspace(8, 11, num=4, endpoint=True))


def test_frame_flip(tmp_path):
    """check it with some NXtomo flipped"""
    ref_frame_width = 280
    n_proj = 10
    raw_frame_width = 100
    ref_frame = PhantomGenerator.get2DPhantomSheppLogan(n=ref_frame_width).astype(numpy.float32) * 256.0
    # create raw data
    frame_0_shift = (0, 0)
    frame_1_shift = (-90, 0)
    frame_2_shift = (-180, 0)

    frame_0 = scipy_shift(ref_frame, shift=frame_0_shift)[:raw_frame_width]
    frame_1 = scipy_shift(ref_frame, shift=frame_1_shift)[:raw_frame_width]
    frame_2 = scipy_shift(ref_frame, shift=frame_2_shift)[:raw_frame_width]
    frames = frame_0, frame_1, frame_2

    x_flips = [False, True, True]
    y_flips = [False, False, True]

    def apply_flip(args):
        frame, flip_x, flip_y = args
        if flip_x:
            frame = numpy.fliplr(frame)
        if flip_y:
            frame = numpy.flipud(frame)
        return frame

    frames = map(apply_flip, zip(frames, x_flips, y_flips))

    # create a Nxtomo for each of those raw data
    raw_data_dir = tmp_path / "raw_data"
    raw_data_dir.mkdir()
    output_dir = tmp_path / "output_dir"
    output_dir.mkdir()
    z_position = (90, 0, -90)

    scans = []
    for (i_frame, frame), z_pos, x_flip, y_flip in zip(enumerate(frames), z_position, x_flips, y_flips):
        nx_tomo = NXtomo()
        nx_tomo.sample.z_translation = [z_pos] * n_proj * _ureg.meter
        nx_tomo.sample.rotation_angle = numpy.linspace(0, 180, num=n_proj, endpoint=False) * _ureg.degree
        nx_tomo.instrument.detector.image_key_control = [ImageKey.PROJECTION] * n_proj
        nx_tomo.instrument.detector.x_pixel_size = 1.0 * _ureg.meter
        nx_tomo.instrument.detector.y_pixel_size = 1.0 * _ureg.meter
        nx_tomo.instrument.detector.distance = 2.3 * _ureg.meter
        nx_tomo.instrument.detector.transformations.add_transformation(DetZFlipTransformation(flip=x_flip))
        nx_tomo.instrument.detector.transformations.add_transformation(DetYFlipTransformation(flip=y_flip))
        nx_tomo.energy = 19.2 * _ureg.keV
        nx_tomo.instrument.detector.data = numpy.asarray([frame] * n_proj)

        file_path = os.path.join(raw_data_dir, f"nxtomo_{i_frame}.nx")
        entry = f"entry000{i_frame}"
        nx_tomo.save(file_path=file_path, data_path=entry)
        scans.append(NXtomoScan(scan=file_path, entry=entry))

    output_file_path = os.path.join(output_dir, "stitched.nx")
    output_data_path = "stitched"
    assert len(scans) == 3
    z_stich_config = PreProcessedZStitchingConfiguration(
        axis_0_pos_px=(0, -90, -180),
        axis_1_pos_px=(0, 0, 0),
        axis_2_pos_px=None,
        axis_0_pos_mm=None,
        axis_1_pos_mm=None,
        axis_2_pos_mm=None,
        axis_0_params={},
        axis_1_params={},
        axis_2_params={},
        stitching_strategy=OverlapStitchingStrategy.LINEAR_WEIGHTS,
        overwrite_results=True,
        input_scans=scans,
        output_file_path=output_file_path,
        output_data_path=output_data_path,
        output_nexus_version=None,
        slices=None,
        slurm_config=None,
        slice_for_cross_correlation="middle",
        pixel_size=None,
    )
    stitcher = PreProcessZStitcher(z_stich_config)
    output_identifier = stitcher.stitch()
    assert output_identifier.file_path == output_file_path
    assert output_identifier.data_path == output_data_path

    created_nx_tomo = NXtomo().load(
        file_path=output_identifier.file_path,
        data_path=output_identifier.data_path,
        detector_data_as="as_numpy_array",
    )

    assert created_nx_tomo.instrument.detector.data.ndim == 3
    # insure flipping has been taking into account
    numpy.testing.assert_array_almost_equal(ref_frame, created_nx_tomo.instrument.detector.data[0, :ref_frame_width, :])

    assert len(created_nx_tomo.instrument.detector.transformations) == 0
