from dataclasses import dataclass
import numpy
from math import ceil


@dataclass
class FrameComposition:
    """
    class used to define intervals to know where to dump raw data or stitched data according to requested policy.
    The idea is to create this once for all for one stitching operation and reuse it for each frame.
    """

    composed_axis: int
    """axis along which the composition is done"""
    local_start: tuple
    """tuple of indices on the input frames ref to know where each region start (along the composed axis)"""
    local_end: tuple
    """tuple of indices on the input frames ref to know where each region end (along the composed axis)"""
    global_start: tuple
    """tuple of indices on the output frame ref to know where each region start (along the composed axis)"""
    global_end: tuple
    """tuple of indices on the output frame ref to know where each region end (along the composed axis)"""

    def browse(self):
        for i in range(len(self.local_start)):
            yield (
                self.local_start[i],
                self.local_end[i],
                self.global_start[i],
                self.global_end[i],
            )

    def compose(self, output_frame: numpy.ndarray, input_frames: tuple):
        if output_frame.ndim not in (2, 3):
            raise TypeError(
                f"output_frame is expected to be 2D (gray scale) or 3D (RGB(A)) and not {output_frame.ndim}"
            )
        for (
            global_start,
            global_end,
            local_start,
            local_end,
            input_frame,
        ) in zip(
            self.global_start,
            self.global_end,
            self.local_start,
            self.local_end,
            input_frames,
        ):
            if input_frame is not None:
                if self.composed_axis == 0:
                    output_frame[global_start:global_end] = input_frame[local_start:local_end]
                elif self.composed_axis == 1:
                    output_frame[:, global_start:global_end] = input_frame[:, local_start:local_end]
                else:
                    raise ValueError(f"composed axis must be in (0, 1). Get {self.composed_axis}")

    @staticmethod
    def compute_raw_frame_compositions(frames: tuple, key_lines: tuple, overlap_kernels: tuple, stitching_axis):
        """
        compute frame composition for raw data

        warning: we expect frames to be ordered y downward and the frame order to keep this ordering
        """
        assert len(frames) == len(overlap_kernels) + 1 == len(key_lines) + 1

        global_start_indices = [0]

        # extend shifts and kernels to have a first shift of 0 and two overlaps values at 0 to
        # generalize processing
        local_start_indices = [0]

        local_start_indices.extend(
            [ceil(key_line[1] + kernel.overlap_size / 2) for (key_line, kernel) in zip(key_lines, overlap_kernels)]
        )
        local_end_indices = [
            ceil(key_line[0] - kernel.overlap_size / 2) for (key_line, kernel) in zip(key_lines, overlap_kernels)
        ]

        local_end_indices.append(frames[-1].shape[stitching_axis])

        for (
            new_local_start_index,
            new_local_end_index,
            kernel,
        ) in zip(local_start_indices, local_end_indices, overlap_kernels):
            global_start_indices.append(
                global_start_indices[-1] + (new_local_end_index - new_local_start_index) + kernel.overlap_size
            )

        # global end can be easily found from global start + local start and end
        global_end_indices = []
        for global_start_index, new_local_start_index, new_local_end_index in zip(
            global_start_indices, local_start_indices, local_end_indices
        ):
            global_end_indices.append(global_start_index + new_local_end_index - new_local_start_index)

        return FrameComposition(
            composed_axis=stitching_axis,
            local_start=tuple(local_start_indices),
            local_end=tuple(local_end_indices),
            global_start=tuple(global_start_indices),
            global_end=tuple(global_end_indices),
        )

    @staticmethod
    def compute_stitch_frame_composition(frames, key_lines: tuple, overlap_kernels: tuple, stitching_axis: int):
        """
        Compute frame composition for stitching.
        """
        assert len(frames) == len(overlap_kernels) + 1 == len(key_lines) + 1
        assert stitching_axis in (0, 1)

        # position in the stitched frame;
        local_start_indices = [0] * len(overlap_kernels)
        local_end_indices = [kernel.overlap_size for kernel in overlap_kernels]

        # position in the global frame. For this one it is simpler to rely on the raw frame composition
        composition_raw = FrameComposition.compute_raw_frame_compositions(
            frames=frames,
            key_lines=key_lines,
            overlap_kernels=overlap_kernels,
            stitching_axis=stitching_axis,
        )
        global_start_indices = composition_raw.global_end[:-1]
        global_end_indices = composition_raw.global_start[1:]

        return FrameComposition(
            composed_axis=stitching_axis,
            local_start=tuple(local_start_indices),
            local_end=tuple(local_end_indices),
            global_start=tuple(global_start_indices),
            global_end=tuple(global_end_indices),
        )

    @staticmethod
    def pprint_composition(raw_composition, stitch_composition):
        """
        util to display what the output of the composition will looks like from composition
        """
        for i_frame, (raw_comp, stitch_comp) in enumerate(zip(raw_composition.browse(), stitch_composition.browse())):
            raw_local_start, raw_local_end, raw_global_start, raw_global_end = raw_comp

            print(
                f"stitch_frame[{raw_global_start}:{raw_global_end}] = frame_{i_frame}[{raw_local_start}:{raw_local_end}]"
            )

            (
                stitch_local_start,
                stitch_local_end,
                stitch_global_start,
                stitch_global_end,
            ) = stitch_comp

            print(
                f"stitch_frame[{stitch_global_start}:{stitch_global_end}] = stitched_frame_{i_frame}[{stitch_local_start}:{stitch_local_end}]"
            )
        i_frame += 1
        raw_local_start, raw_local_end, raw_global_start, raw_global_end = list(raw_composition.browse())[-1]
        print(f"stitch_frame[{raw_global_start}:{raw_global_end}] = frame_{i_frame}[{raw_local_start}:{raw_local_end}]")
