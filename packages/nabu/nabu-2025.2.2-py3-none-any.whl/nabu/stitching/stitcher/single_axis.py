import numpy
import logging
from collections.abc import Iterable
from tomoscan.series import Series
from tomoscan.identifier import BaseIdentifier
from nabu.stitching.stitcher.base import _StitcherBase, get_obj_constant_side_length
from nabu.stitching.stitcher_2D import stitch_raw_frames
from nabu.stitching.utils.utils import ShiftAlgorithm, from_slice_to_n_elements
from nabu.stitching.overlap import (
    check_overlaps,
    ImageStichOverlapKernel,
)
from nabu.stitching.config import (
    SingleAxisStitchingConfiguration,
    KEY_RESCALE_MIN_PERCENTILES,
    KEY_RESCALE_MAX_PERCENTILES,
)
from nabu.misc.utils import rescale_data
from nabu.stitching.sample_normalization import normalize_frame as normalize_frame_by_sample
from nabu.stitching.stitcher.dumper.base import DumperBase
from silx.io.utils import get_data
from silx.io.url import DataUrl
from scipy.ndimage import shift as shift_scipy


_logger = logging.getLogger(__name__)


PROGRESS_BAR_STITCH_VOL_DESC = "stitch volumes"
# description of the progress bar used when stitching volume.
# Needed to retrieve advancement from file when stitching remotely


class _SingleAxisMetaClass(type):
    """
    Metaclass for single axis stitcher in order to aggregate dumper class and axis
    """

    def __new__(mcls, name, bases, attrs, axis=None, dumper_cls=None):
        mcls = super().__new__(mcls, name, bases, attrs)
        mcls._axis = axis
        mcls._dumperCls = dumper_cls
        return mcls


class SingleAxisStitcher(_StitcherBase, metaclass=_SingleAxisMetaClass):
    """
    Any single-axis base class
    """

    def __init__(self, configuration, *args, **kwargs) -> None:
        super().__init__(configuration, *args, **kwargs)
        if self._dumperCls is not None:
            self._dumper = self._dumperCls(configuration=configuration)
        else:
            self._dumper = None

        # initial shifts
        self._axis_0_rel_ini_shifts = []
        """Shift between two juxtapose objects along axis 0 found from position metadata or given by the user"""
        self._axis_1_rel_ini_shifts = []
        """Shift between two juxtapose objects along axis 1 found from position metadata or given by the user"""
        self._axis_2_rel_ini_shifts = []
        """Shift between two juxtapose objects along axis 2 found from position metadata or given by the user"""

        # shifts to add once refine
        self._axis_0_rel_final_shifts = []
        """Shift over axis 0 found once refined by the cross correlation algorithm"""
        self._axis_1_rel_final_shifts = []
        """Shift over axis 1 found once refined by the cross correlation algorithm"""
        self._axis_2_rel_final_shifts = []
        """Shift over axis 2 found once refined by the cross correlation algorithm"""

        self._slices_to_stitch = None
        # slices to be stitched. Obtained from calling Configuration.settle_slices

        self._stitching_constant_length = None
        # stitching width: larger volume width. Other volume will be pad

        def shifts_is_scalar(shifts):
            return isinstance(shifts, ShiftAlgorithm) or numpy.isscalar(shifts)

        # 'expend' shift algorithm
        if shifts_is_scalar(self.configuration.axis_0_pos_px):
            self.configuration.axis_0_pos_px = [
                self.configuration.axis_0_pos_px,
            ] * (len(self.series) - 1)
        if shifts_is_scalar(self.configuration.axis_1_pos_px):
            self.configuration.axis_1_pos_px = [
                self.configuration.axis_1_pos_px,
            ] * (len(self.series) - 1)
        if shifts_is_scalar(self.configuration.axis_1_pos_px):
            self.configuration.axis_1_pos_px = [
                self.configuration.axis_1_pos_px,
            ] * (len(self.series) - 1)
        if numpy.isscalar(self.configuration.axis_0_params):
            self.configuration.axis_0_params = [
                self.configuration.axis_0_params,
            ] * (len(self.series) - 1)
        if numpy.isscalar(self.configuration.axis_1_params):
            self.configuration.axis_1_params = [
                self.configuration.axis_1_params,
            ] * (len(self.series) - 1)
        if numpy.isscalar(self.configuration.axis_2_params):
            self.configuration.axis_2_params = [
                self.configuration.axis_2_params,
            ] * (len(self.series) - 1)

    @property
    def axis(self) -> int:
        return self._axis

    @property
    def dumper(self):
        return self._dumper

    @property
    def stitching_axis_in_frame_space(self):
        """
        stitching is operated in 2D (frame) space. So the axis in frame space is different than the one in 3D ebs-tomo space (https://tomo.gitlab-pages.esrf.fr/bliss-tomo/master/modelization.html)
        """
        raise NotImplementedError("Base class")

    def stitch(self, store_composition: bool = True) -> BaseIdentifier:
        if self.progress is not None:
            self.progress.set_description("order scans")
        self.order_input_tomo_objects()
        if self.progress is not None:
            self.progress.set_description("check inputs")
        self.check_inputs()
        self.settle_flips()

        if self.progress is not None:
            self.progress.set_description("compute shifts")
        self._compute_positions_as_px()
        self.pre_processing_computation()

        self.compute_estimated_shifts()
        self._compute_shifts()
        self._createOverlapKernels()
        if self.progress is not None:
            self.progress.set_description(PROGRESS_BAR_STITCH_VOL_DESC)

        self._create_stitching(store_composition=store_composition)
        if self.progress is not None:
            self.progress.set_description("dump configuration")
        self.dumper.save_configuration()
        return self.dumper.output_identifier

    @property
    def serie_label(self) -> str:
        """return serie name for logs"""
        return "single axis serie"

    def get_n_slices_to_stitch(self):
        """Return the number of slice to be stitched"""
        if self._slices_to_stitch is None:
            raise RuntimeError("Slices needs to be settled first")
        return from_slice_to_n_elements(self._slices_to_stitch)

    def get_final_axis_positions_in_px(self) -> dict:
        """
        compute the final position (**in pixel**) from the initial position of the first object and the final relative shift computed (1)
        (1): the final relative shift is obtained from the initial shift (from motor position of provided by the user) + the refinement shift from cross correlation algorithm
        :return: dict with tomo object identifier (str) as key and a tuple of position in pixel (axis_0_pos, axis_1_pos, axis_2_pos)
        """
        pos_0_shift = numpy.concatenate(
            (
                numpy.atleast_1d(0.0),
                numpy.array(self._axis_0_rel_final_shifts) - numpy.array(self._axis_0_rel_ini_shifts),
            )
        )
        pos_0_cum_shift = numpy.cumsum(pos_0_shift)
        final_pos_axis_0 = self.configuration.axis_0_pos_px + pos_0_cum_shift

        pos_1_shift = numpy.concatenate(
            (
                numpy.atleast_1d(0.0),
                numpy.array(self._axis_1_rel_final_shifts) - numpy.array(self._axis_1_rel_ini_shifts),
            )
        )
        pos_1_cum_shift = numpy.cumsum(pos_1_shift)
        final_pos_axis_1 = self.configuration.axis_1_pos_px + pos_1_cum_shift

        pos_2_shift = numpy.concatenate(
            (
                numpy.atleast_1d(0.0),
                numpy.array(self._axis_2_rel_final_shifts) - numpy.array(self._axis_2_rel_ini_shifts),
            )
        )
        pos_2_cum_shift = numpy.cumsum(pos_2_shift)
        final_pos_axis_2 = self.configuration.axis_2_pos_px + pos_2_cum_shift

        assert len(final_pos_axis_0) == len(final_pos_axis_1)
        assert len(final_pos_axis_0) == len(final_pos_axis_2)
        assert len(final_pos_axis_0) == len(self.series)

        return {
            tomo_obj.get_identifier().to_str(): (pos_0, pos_1, pos_2)
            for tomo_obj, (pos_0, pos_1, pos_2) in zip(
                self.series, zip(final_pos_axis_0, final_pos_axis_1, final_pos_axis_2)
            )
        }

    def settle_flips(self):
        """
        User can provide some information on existing flips at frame level.
        The goal of this step is to get one flip_lr and on flip_ud value per scan or volume
        """
        if numpy.isscalar(self.configuration.flip_lr):
            self.configuration.flip_lr = tuple([self.configuration.flip_lr] * len(self.series))
        else:
            if not len(self.configuration.flip_lr) == len(self.series):
                raise ValueError("flip_lr expects a scalar value or one value per element to stitch")
            self.configuration.flip_lr = tuple(self.configuration.flip_lr)
            for elmt in self.configuration.flip_lr:
                if not isinstance(elmt, bool):
                    raise TypeError

        if numpy.isscalar(self.configuration.flip_ud):
            self.configuration.flip_ud = tuple([self.configuration.flip_ud] * len(self.series))
        else:
            if not len(self.configuration.flip_ud) == len(self.series):
                raise ValueError("flip_ud expects a scalar value or one value per element to stitch")
            self.configuration.flip_ud = tuple(self.configuration.flip_ud)
            for elmt in self.configuration.flip_ud:
                if not isinstance(elmt, bool):
                    raise TypeError

    def _createOverlapKernels(self):
        """
        after this stage the overlap kernels must be created and with the final overlap size
        """
        if self.axis == 0:
            stitched_axis_rel_shifts = self._axis_0_rel_final_shifts
            stitched_axis_params = self.configuration.axis_0_params
        elif self.axis == 1:
            stitched_axis_rel_shifts = self._axis_1_rel_final_shifts
            stitched_axis_params = self.configuration.axis_1_params
        elif self.axis == 2:
            stitched_axis_rel_shifts = self._axis_2_rel_final_shifts
            stitched_axis_params = self.configuration.axis_2_params
        else:
            raise NotImplementedError

        if stitched_axis_rel_shifts is None or len(stitched_axis_rel_shifts) == 0:
            raise RuntimeError(
                f"axis {self.axis} shifts have not been defined yet. Please define them before calling this function"
            )

        overlap_size = stitched_axis_params.get("overlap_size", None)
        if overlap_size in (None, "None", ""):
            overlap_size = -1
        else:
            overlap_size = int(overlap_size)

        self._stitching_constant_length = max(
            [get_obj_constant_side_length(obj, axis=self.axis) for obj in self.series]
        )

        for stitched_axis_shift in stitched_axis_rel_shifts:
            if overlap_size == -1:
                height = abs(stitched_axis_shift)
            else:
                height = overlap_size

            self._overlap_kernels.append(
                ImageStichOverlapKernel(
                    stitching_axis=self.stitching_axis_in_frame_space,
                    frame_unstitched_axis_size=self._stitching_constant_length,
                    stitching_strategy=self.configuration.stitching_strategy,
                    overlap_size=height,
                    extra_params=self.configuration.stitching_kernels_extra_params,
                )
            )

    @property
    def series(self) -> Series:
        return self._series

    @property
    def configuration(self) -> SingleAxisStitchingConfiguration:
        return self._configuration

    @property
    def progress(self):
        return self._progress

    @staticmethod
    def _data_bunch_iterator(slices, bunch_size):
        """util to get indices by bunch until we reach n_frames"""
        if isinstance(slices, slice):
            # note: slice step is handled at a different level
            start = end = slices.start

            while True:
                start, end = end, min((end + bunch_size), slices.stop)
                yield (start, end)
                if end >= slices.stop:
                    break
        # in the case of non-contiguous frames
        elif isinstance(slices, Iterable):
            for s in slices:
                yield (s, s + 1)
        else:
            raise TypeError(f"slices is provided as {type(slices)}. When Iterable or slice is expected")

    def rescale_frames(self, frames: tuple):
        """
        rescale_frames if requested by the configuration
        """
        _logger.info("apply rescale frames")

        def cast_percentile(percentile) -> int:
            if isinstance(percentile, str):
                percentile.replace(" ", "").rstrip("%")
            return int(percentile)

        rescale_min_percentile = cast_percentile(self.configuration.rescale_params.get(KEY_RESCALE_MIN_PERCENTILES, 0))
        rescale_max_percentile = cast_percentile(
            self.configuration.rescale_params.get(KEY_RESCALE_MAX_PERCENTILES, 100)
        )

        new_min = numpy.percentile(frames[0], rescale_min_percentile)
        new_max = numpy.percentile(frames[0], rescale_max_percentile)

        def rescale(data):
            # FIXME: takes time because browse several time the dataset, twice for percentiles and twices to get min and max when calling rescale_data...
            data_min = numpy.percentile(data, rescale_min_percentile)
            data_max = numpy.percentile(data, rescale_max_percentile)
            return rescale_data(data, new_min=new_min, new_max=new_max, data_min=data_min, data_max=data_max)

        return tuple([rescale(data) for data in frames])

    def normalize_frame_by_sample(self, frames: tuple):
        """
        normalize frame from a sample picked on the left or the right
        """
        _logger.info("apply normalization by a sample")
        return tuple(
            [
                normalize_frame_by_sample(
                    frame=frame,
                    side=self.configuration.normalization_by_sample.side,
                    method=self.configuration.normalization_by_sample.method,
                    margin_before_sample=self.configuration.normalization_by_sample.margin,
                    sample_width=self.configuration.normalization_by_sample.width,
                )
                for frame in frames
            ]
        )

    @staticmethod
    def stitch_frames(
        frames: tuple | numpy.ndarray,
        axis,
        x_relative_shifts: tuple,
        y_relative_shifts: tuple,
        output_dtype: numpy.ndarray,
        stitching_axis: int,
        overlap_kernels: tuple,
        dumper: DumperBase = None,
        check_inputs=True,
        shift_mode="nearest",
        i_frame=None,
        return_composition_cls=False,
        alignment="center",
        pad_mode="constant",
        new_width: int | None = None,
    ) -> numpy.ndarray:
        """
        shift frames according to provided `shifts` (as y, x tuples) then stitch all the shifted frames together and
        save them to output_dataset.

        :param tuple frames: element must be a DataUrl or a 2D numpy array
        :param stitching_regions_hdf5_dataset:
        """
        if check_inputs:
            if len(frames) < 2:
                raise ValueError(f"Not enought frames provided for stitching ({len(frames)} provided)")
            if len(frames) != len(x_relative_shifts) + 1:
                raise ValueError(
                    f"Incoherent number of shift provided ({len(x_relative_shifts)}) compare to number of frame ({len(frames)}). len(frames) - 1 expected"
                )
            if len(x_relative_shifts) != len(overlap_kernels):
                raise ValueError(
                    f"expect to have the same number of x_relative_shifts ({len(x_relative_shifts)}) and y_overlap ({len(overlap_kernels)})"
                )
            if len(y_relative_shifts) != len(overlap_kernels):
                raise ValueError(
                    f"expect to have the same number of y_relative_shifts ({len(y_relative_shifts)}) and y_overlap ({len(overlap_kernels)})"
                )

            relative_positions = [(0, 0, 0)]
            for y_rel_pos, x_rel_pos in zip(y_relative_shifts, x_relative_shifts):
                relative_positions.append(
                    (
                        y_rel_pos + relative_positions[-1][0],
                        0,  # position over axis 1 (aka y) is not handled yet
                        x_rel_pos + relative_positions[-1][2],
                    )
                )
            check_overlaps(
                frames=tuple(frames),
                positions=tuple(relative_positions),
                axis=axis,
                raise_error=False,
            )

        def check_frame_is_2d(frame):
            if frame.ndim != 2:
                raise ValueError(f"2D frame expected when {frame.ndim}D provided")

        # step_0 load data if from url
        data = []
        for frame in frames:
            if isinstance(frame, DataUrl):
                data_frame = get_data(frame)
                if check_inputs:
                    check_frame_is_2d(data_frame)
                data.append(data_frame)
            elif isinstance(frame, numpy.ndarray):
                if check_inputs:
                    check_frame_is_2d(frame)
                data.append(frame)
            else:
                raise TypeError(f"frames are expected to be DataUrl or 2D numpy array. Not {type(frame)}")

        # step 1: shift each frames (except the first one)
        if stitching_axis == 0:
            relative_shift_along_stitched_axis = y_relative_shifts
            relative_shift_along_unstitched_axis = x_relative_shifts
        elif stitching_axis == 1:
            relative_shift_along_stitched_axis = x_relative_shifts
            relative_shift_along_unstitched_axis = y_relative_shifts
        else:
            raise NotImplementedError("")

        shifted_data = [data[0]]
        for frame, relative_shift in zip(data[1:], relative_shift_along_unstitched_axis):
            # note: for now we only shift data in x. the y shift is handled in the FrameComposition
            relative_shift = numpy.asarray(relative_shift).astype(numpy.int8)
            if relative_shift == 0:
                shifted_frame = frame
            else:
                # TO speed up: should use the Fourier transform
                shifted_frame = shift_scipy(
                    frame,
                    mode=shift_mode,
                    shift=[0, -relative_shift] if stitching_axis == 0 else [-relative_shift, 0],
                    order=1,
                )
            shifted_data.append(shifted_frame)

        # step 2: create stitched frame
        stitched_frame, composition_cls = stitch_raw_frames(
            frames=shifted_data,
            key_lines=(
                [
                    (int(frame.shape[stitching_axis] - abs(relative_shift / 2)), int(abs(relative_shift / 2)))
                    for relative_shift, frame in zip(relative_shift_along_stitched_axis, frames)
                ]
            ),
            overlap_kernels=overlap_kernels,
            check_inputs=check_inputs,
            output_dtype=output_dtype,
            return_composition_cls=True,
            alignment=alignment,
            pad_mode=pad_mode,
            new_unstitched_axis_size=new_width,
        )
        if dumper is not None:
            dumper.save_stitched_frame(
                stitched_frame=stitched_frame,
                composition_cls=composition_cls,
                i_frame=i_frame,
                axis=1,
            )

        if return_composition_cls:
            return stitched_frame, composition_cls
        else:
            return stitched_frame
