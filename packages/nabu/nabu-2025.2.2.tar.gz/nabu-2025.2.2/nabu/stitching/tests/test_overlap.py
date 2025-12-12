import numpy
import pytest

from nabu.stitching.overlap import compute_image_minimum_divergence, compute_image_higher_signal, check_overlaps
from nabu.testutils import get_data
from nabu.stitching.overlap import ImageStichOverlapKernel, OverlapStitchingStrategy
from nabu.stitching.stitcher_2D import stitch_raw_frames
from silx.image.phantomgenerator import PhantomGenerator


strategies_to_test_weights = (
    OverlapStitchingStrategy.CLOSEST,
    OverlapStitchingStrategy.COSINUS_WEIGHTS,
    OverlapStitchingStrategy.LINEAR_WEIGHTS,
    OverlapStitchingStrategy.MEAN,
)


@pytest.mark.parametrize("strategy", strategies_to_test_weights)
@pytest.mark.parametrize("stitching_axis", (0, 1))
def test_overlap_stitcher(strategy, stitching_axis):
    frame_width = 128
    frame_height = frame_width
    frame_1 = PhantomGenerator.get2DPhantomSheppLogan(n=frame_width)
    stitcher = ImageStichOverlapKernel(
        stitching_strategy=strategy,
        overlap_size=frame_height,
        frame_unstitched_axis_size=128,
        stitching_axis=stitching_axis,
    )
    stitched_frame = stitcher.stitch(frame_1, frame_1)[0]
    assert stitched_frame.shape == (frame_height, frame_width)
    # check result is close to the expected one
    numpy.testing.assert_allclose(frame_1, stitched_frame, atol=10e-10)

    # check sum of weights ~ 1.0
    numpy.testing.assert_allclose(
        stitcher.weights_img_1 + stitcher.weights_img_2,
        numpy.ones_like(stitcher.weights_img_1),
    )


@pytest.mark.parametrize("stitching_axis", (0, 1))
def test_compute_image_minimum_divergence(stitching_axis):
    """make sure the compute_image_minimum_divergence function is processing"""
    raw_data_1 = get_data("brain_phantom.npz")["data"]
    raw_data_2 = numpy.random.rand(*raw_data_1.shape) * 255.0

    stitching = compute_image_minimum_divergence(
        raw_data_1, raw_data_2, high_frequency_threshold=2, stitching_axis=stitching_axis
    )
    assert stitching.shape == raw_data_1.shape


def test_compute_image_higher_signal():
    """
    make sure compute_image_higher_signal is processing
    """
    raw_data = get_data("brain_phantom.npz")["data"]
    raw_data_1 = raw_data.copy()
    raw_data_1[40:75] = 0.0
    raw_data_1[:, 210:245] = 0.0

    raw_data_2 = raw_data.copy()
    raw_data_2[:, 100:120] = 0.0

    stitching = compute_image_higher_signal(raw_data_1, raw_data_2)

    numpy.testing.assert_array_equal(
        stitching,
        raw_data,
    )


def test_check_overlaps():
    """test 'check_overlaps' function"""

    # two frames, ordered and with an overlap
    check_overlaps(
        frames=(
            numpy.ones(10),
            numpy.ones(20),
        ),
        positions=((10, 0, 0), (0, 0, 0)),
        axis=0,
        raise_error=True,
    )

    # two frames, ordered and without an overlap
    with pytest.raises(ValueError):
        check_overlaps(
            frames=(
                numpy.ones(10),
                numpy.ones(20),
            ),
            positions=((0, 0, 0), (100, 0, 0)),
            axis=0,
            raise_error=True,
        )

    # two frames, frame 0 fully overlap frame 1
    with pytest.raises(ValueError):
        check_overlaps(
            frames=(
                numpy.ones(20),
                numpy.ones(10),
            ),
            positions=((8, 0, 0), (5, 0, 0)),
            axis=0,
            raise_error=True,
        )

    # three frames 'overlaping' as expected
    check_overlaps(
        frames=(
            numpy.ones(10),
            numpy.ones(20),
            numpy.ones(10),
        ),
        positions=((20, 0, 0), (10, 0, 0), (0, 0, 0)),
        axis=0,
        raise_error=True,
    )

    # three frames: frame 0 overlap frame 1 but also frame 2
    with pytest.raises(ValueError):
        check_overlaps(
            frames=(
                numpy.ones(20),
                numpy.ones(10),
                numpy.ones(10),
            ),
            positions=((20, 0, 0), (15, 0, 0), (11, 0, 0)),
            axis=0,
            raise_error=True,
        )


@pytest.mark.parametrize("dtype", (numpy.float16, numpy.float32))
def test_stitch_vertically_raw_frames(dtype):
    """
    ensure a stitching with 3 frames and different overlap can be done
    """
    ref_frame_width = 256
    frame_ref = PhantomGenerator.get2DPhantomSheppLogan(n=ref_frame_width).astype(dtype)

    # split the frame into several part
    frame_1 = frame_ref[0:100]
    frame_2 = frame_ref[80:164]
    frame_3 = frame_ref[154:]

    kernel_1 = ImageStichOverlapKernel(frame_unstitched_axis_size=ref_frame_width, overlap_size=20, stitching_axis=0)
    kernel_2 = ImageStichOverlapKernel(frame_unstitched_axis_size=ref_frame_width, overlap_size=10, stitching_axis=0)

    stitched = stitch_raw_frames(
        frames=(frame_1, frame_2, frame_3),
        output_dtype=dtype,
        overlap_kernels=(kernel_1, kernel_2),
        raw_frames_compositions=None,
        overlap_frames_compositions=None,
        key_lines=(
            (
                90,  # frame_1 height - kernel_1 height / 2.0
                10,  # kernel_1 height / 2.0
            ),
            (
                79,  # frame_2 height - kernel_2 height / 2.0 ou 102-20 ?
                5,  # kernel_2 height / 2.0
            ),
        ),
    )

    assert stitched.shape == frame_ref.shape
    numpy.testing.assert_array_almost_equal(frame_ref, stitched)


def test_stitch_vertically_raw_frames_2():
    """
    ensure a stitching with 3 frames and different overlap can be done
    """
    ref_frame_width = 256
    frame_ref = PhantomGenerator.get2DPhantomSheppLogan(n=ref_frame_width).astype(numpy.float32)

    # split the frame into several part
    frame_1 = frame_ref.copy()
    frame_2 = frame_ref.copy()
    frame_3 = frame_ref.copy()

    kernel_1 = ImageStichOverlapKernel(frame_unstitched_axis_size=ref_frame_width, overlap_size=10, stitching_axis=0)
    kernel_2 = ImageStichOverlapKernel(frame_unstitched_axis_size=ref_frame_width, overlap_size=10, stitching_axis=0)

    stitched = stitch_raw_frames(
        frames=(frame_1, frame_2, frame_3),
        output_dtype=numpy.float32,
        overlap_kernels=(kernel_1, kernel_2),
        raw_frames_compositions=None,
        overlap_frames_compositions=None,
        key_lines=((20, 20), (105, 105)),
    )

    assert stitched.shape == frame_ref.shape
    numpy.testing.assert_array_almost_equal(frame_ref, stitched)


@pytest.mark.parametrize("dtype", (numpy.float16, numpy.float32))
def test_stitch_horizontally_raw_frames(dtype):
    """
    ensure a stitching with 3 frames and different overlap can be done along axis 1
    """
    ref_frame_width = 256
    frame_ref = PhantomGenerator.get2DPhantomSheppLogan(n=ref_frame_width).astype(dtype)

    # split the frame into several part
    frame_1 = frame_ref[:, 0:100]
    frame_2 = frame_ref[:, 80:164]
    frame_3 = frame_ref[:, 154:]

    kernel_1 = ImageStichOverlapKernel(frame_unstitched_axis_size=ref_frame_width, overlap_size=20, stitching_axis=1)
    kernel_2 = ImageStichOverlapKernel(frame_unstitched_axis_size=ref_frame_width, overlap_size=10, stitching_axis=1)

    stitched = stitch_raw_frames(
        frames=(frame_1, frame_2, frame_3),
        output_dtype=dtype,
        overlap_kernels=(kernel_1, kernel_2),
        raw_frames_compositions=None,
        overlap_frames_compositions=None,
        key_lines=(
            (
                90,  # frame_1 height - kernel_1 height / 2.0
                10,  # kernel_1 height / 2.0
            ),
            (
                79,  # frame_2 height - kernel_2 height / 2.0 ou 102-20 ?
                5,  # kernel_2 height / 2.0
            ),
        ),
    )

    assert stitched.shape == frame_ref.shape
    numpy.testing.assert_array_almost_equal(frame_ref, stitched)
