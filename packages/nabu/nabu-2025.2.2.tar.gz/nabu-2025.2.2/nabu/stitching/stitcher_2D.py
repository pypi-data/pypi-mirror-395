# ruff: noqa: N999
import numpy
from math import ceil
from nabu.stitching.overlap import ImageStichOverlapKernel
from nabu.stitching.frame_composition import FrameComposition
from nabu.stitching.alignment import align_frame, _Alignment


def stitch_raw_frames(
    frames: tuple,
    key_lines: tuple,
    overlap_kernels: ImageStichOverlapKernel | tuple,
    output_dtype: numpy.dtype = numpy.float32,
    check_inputs=True,
    raw_frames_compositions: FrameComposition | None = None,
    overlap_frames_compositions: FrameComposition | None = None,
    return_composition_cls=False,
    alignment: _Alignment = "center",
    pad_mode="constant",
    new_unstitched_axis_size: int | None = None,
) -> numpy.ndarray:
    r"""
    Stitches raw frames (already shifted and flat fielded !!!) together using
    raw stitching (no pixel interpolation, y_overlap_in_px is expected to be an int).
    Stitching depends on the kernel used.

    It can be done:

    * vertically:

                                    X
        ------------------------------------------------------------------>
        |    --------------
        |    |            |
        |    |  Frame 1   |                           --------------
        |    |            |                           |  Frame 1    |
        |    --------------                           |             |
        Y |                         --> stitching  -->  |~ stitching ~|
        |    --------------                           |             |
        |    |            |                           |  Frame 2    |
        |    |  Frame 2   |                            --------------
        |    |            |
        |    --------------
        \/

    * horizontally:

        ------------------------------------------------------------------>
        |    --------------    --------------                     -----------------------
        |    |            |    |            |                     |         ~ ~         |
        Y |    |  Frame 1   |    |  Frame 2   | --> stitching  -->  | Frame 1 ~ ~ Frame 2 |
        |    |            |    |            |                     |         ~ ~         |
        |    --------------    --------------                     -----------------------
        |
        \/

    returns stitched_projection, raw_img_1, raw_img_2, computed_overlap
    proj_0 and proj_1 are already expected to be in a row, having stitching_height_in_px in common. At top of proj_0
    and at bottom of proj_1

    :param tuple frames: tuple of 2D numpy array. Expected to be Z up oriented at this stage
    :param tuple key_lines: for each junction define the two lines to overlay (from the upper and the lower frames). In the reference where 0 is the bottom line of the image.
    :param overlap_kernels: ImageStichOverlapKernel overlap kernel to be used or a list of kernels (one per overlap). Define strategy and overlap heights
    :param numpy.dtype output_dtype: dataset dtype. For now must be provided because flat field correction changes data type (numpy.float32 for now)
    :param bool check_inputs: if True will do more test on inputs parameters like checking frame shapes, coherence of the request.. As it can be time consuming it is optional
    :param raw_frames_compositions: pre computed raw frame composition. If not provided will compute them. allow providing it to speed up calculation
    :param overlap_frames_compositions: pre computed stitched frame composition. If not provided will compute them. allow providing it to speed up calculation
    :param bool return_frame_compositions: if False return simply the stitched frames. Else return a tuple with stitching frame and the dictionary with the composition frames...
    :param alignment: how to align frames if two frames have different sizes along the unstitched axis
    :param pad_mode: how to pad data for alignment (provided to numpy.pad function)
    :param new_unstitched_axis_size: size of the image along the axis not stitched. So it will be the frame width if the stitching axis is 0 and the frame height if the stitching axis is 1
    """
    if overlap_kernels is None or len(overlap_kernels) == 0:
        raise ValueError("overlap kernels must be provided")

    stitched_axis = overlap_kernels[0].stitched_axis
    unstitched_axis = overlap_kernels[0].unstitched_axis

    if check_inputs:
        # check frames are 2D numpy arrays
        def check_frame(proj):
            if not isinstance(proj, numpy.ndarray) and proj.ndim == 2:
                raise ValueError(f"frames are expected to be 2D numpy array")

        [check_frame(frame) for frame in frames]
        for frame_0, frame_1 in zip(frames[:-1], frames[1:]):
            if not (frame_0.ndim == frame_1.ndim == 2):
                raise ValueError("Frames are expected to be 2D")

        # check there is coherence between overlap kernels and frames
        for frame_0, frame_1, kernel in zip(frames[:-1], frames[1:], overlap_kernels):
            if frame_0.shape[stitched_axis] < kernel.overlap_size:
                raise ValueError(
                    f"frame_0 height ({frame_0.shape[stitched_axis]}) is less than kernel overlap ({kernel.overlap_size})"
                )
            if frame_1.shape[stitched_axis] < kernel.overlap_size:
                raise ValueError(
                    f"frame_1 height ({frame_1.shape[stitched_axis]}) is less than kernel overlap ({kernel.overlap_size})"
                )
        # check key lines are coherent with overlp kernels
        if not len(key_lines) == len(overlap_kernels):
            raise ValueError("we expect to have the same number of key_lines then the number of kernel")
        else:
            for key_line in key_lines:
                for value in key_line:
                    if not isinstance(value, (int, numpy.integer)):
                        raise TypeError(f"key_line is expected to be an integer. {type(key_line)} provided")
                    elif value < 0:
                        raise ValueError(f"key lines are expected to be positive values. Get {value} as key line value")

        # check overlap kernel stitching axis are coherent (for now make sure they are all along the same axis)
        if len(overlap_kernels) > 1:
            for previous_kernel, next_kernel in zip(overlap_kernels[:-1], overlap_kernels[1:]):
                if not isinstance(previous_kernel, ImageStichOverlapKernel):
                    raise TypeError(
                        f"overlap kernels must be instances of {ImageStichOverlapKernel}. Get {type(previous_kernel)}"
                    )
                if not isinstance(next_kernel, ImageStichOverlapKernel):
                    raise TypeError(
                        f"overlap kernels must be instances of {ImageStichOverlapKernel}. Get {type(next_kernel)}"
                    )
                if previous_kernel.stitched_axis != next_kernel.stitched_axis:
                    raise ValueError(
                        "kernels with different stitching axis provided. For now all kernels must have the same stitchign axis"
                    )

    if new_unstitched_axis_size is None:
        new_unstitched_axis_size = max([frame.shape[unstitched_axis] for frame in frames])

    frames = tuple(
        [
            align_frame(
                data=frame,
                alignment=alignment,
                new_aligned_axis_size=new_unstitched_axis_size,
                pad_mode=pad_mode,
                alignment_axis=unstitched_axis,
            )
            for frame in frames
        ]
    )

    # step 1: create numpy array that will contain stitching
    # if raw composition doesn't exists create it
    if raw_frames_compositions is None:
        raw_frames_compositions = FrameComposition.compute_raw_frame_compositions(
            frames=frames,
            overlap_kernels=overlap_kernels,
            key_lines=key_lines,
            stitching_axis=stitched_axis,
        )

    new_stitched_axis_size = raw_frames_compositions.global_end[-1] - raw_frames_compositions.global_start[0]
    if stitched_axis == 0:
        stitched_projection_shape = (
            int(new_stitched_axis_size),
            new_unstitched_axis_size,
        )
    else:
        stitched_projection_shape = (
            new_unstitched_axis_size,
            int(new_stitched_axis_size),
        )

    stitch_array = numpy.empty(stitched_projection_shape, dtype=output_dtype)

    # step 2: set raw data
    # fill stitch array with raw data raw data
    raw_frames_compositions.compose(
        output_frame=stitch_array,
        input_frames=frames,
    )

    # step 3 set stitched data

    # 3.1 create stitched overlaps
    stitched_overlap = []
    for frame_0, frame_1, kernel, key_line in zip(frames[:-1], frames[1:], overlap_kernels, key_lines):
        assert kernel.overlap_size >= 0
        frame_0_overlap, frame_1_overlap = get_overlap_areas(
            upper_frame=frame_0,
            lower_frame=frame_1,
            upper_frame_key_line=key_line[0],
            lower_frame_key_line=key_line[1],
            overlap_size=kernel.overlap_size,
            stitching_axis=stitched_axis,
        )

        assert (
            frame_0_overlap.shape[stitched_axis] == frame_1_overlap.shape[stitched_axis] == kernel.overlap_size
        ), f"{frame_0_overlap.shape[stitched_axis]} == {frame_1_overlap.shape[stitched_axis]} == {kernel.overlap_size}"

        stitched_overlap.append(
            kernel.stitch(
                frame_0_overlap,
                frame_1_overlap,
            )[0]
        )
    # 3.2 fill stitched overlap on output array
    if overlap_frames_compositions is None:
        overlap_frames_compositions = FrameComposition.compute_stitch_frame_composition(
            frames=frames,
            overlap_kernels=overlap_kernels,
            key_lines=key_lines,
            stitching_axis=stitched_axis,
        )
    overlap_frames_compositions.compose(
        output_frame=stitch_array,
        input_frames=stitched_overlap,
    )
    if return_composition_cls:
        return (
            stitch_array,
            {
                "raw_composition": raw_frames_compositions,
                "overlap_composition": overlap_frames_compositions,
            },
        )

    return stitch_array


def get_overlap_areas(
    upper_frame: numpy.ndarray,
    lower_frame: numpy.ndarray,
    upper_frame_key_line: int,
    lower_frame_key_line: int,
    overlap_size: int,
    stitching_axis: int,
):
    """
    return the requested area from lower_frame and upper_frame.

    Lower_frame contains at the end of it the 'real overlap' with the upper_frame.
    Upper_frame contains the 'real overlap' at the end of it.

    For some reason the user can ask the stitching height to be smaller than the `real overlap`.

    Here are some drawing to have a better of view of those regions:

    .. image:: images/stitching/z_stitch_real_overlap.png
        :width: 600

    .. image:: z_stitch_stitch_height.png
        :width: 600
    """
    assert stitching_axis in (0, 1)
    for pf, pn in zip((lower_frame_key_line, upper_frame_key_line), ("lower_frame", "upper_frame")):
        if not isinstance(pf, (int, numpy.number)):
            raise TypeError(f"{pn} is expected to be a number. {type(pf)} provided")
    assert overlap_size >= 0

    lf_start = ceil(lower_frame_key_line - overlap_size / 2)
    lf_end = ceil(lower_frame_key_line + overlap_size / 2)
    uf_start = ceil(upper_frame_key_line - overlap_size / 2)
    uf_end = ceil(upper_frame_key_line + overlap_size / 2)

    lf_start, lf_end = min(lf_start, lf_end), max(lf_start, lf_end)
    uf_start, uf_end = min(uf_start, uf_end), max(uf_start, uf_end)
    if lf_start < 0 or uf_start < 0:
        raise ValueError(
            f"requested overlap ({overlap_size}) is incoherent with key line positions ({lower_frame_key_line}, {upper_frame_key_line}) - expected to be smaller."
        )

    if stitching_axis == 0:
        overlap_upper = upper_frame[uf_start:uf_end]
        overlap_lower = lower_frame[lf_start:lf_end]
    elif stitching_axis == 1:
        overlap_upper = upper_frame[:, uf_start:uf_end]
        overlap_lower = lower_frame[:, lf_start:lf_end]
    else:
        raise NotImplementedError
    if not overlap_upper.shape == overlap_lower.shape:
        # maybe in the future: try to reduce one according to the other ????
        raise RuntimeError(
            f"lower and upper frame have different overlap size ({overlap_upper.shape} vs {overlap_lower.shape})"
        )
    return overlap_upper, overlap_lower
