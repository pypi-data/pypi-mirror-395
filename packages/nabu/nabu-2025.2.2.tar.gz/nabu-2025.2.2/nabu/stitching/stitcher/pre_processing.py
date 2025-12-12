import numpy
import logging
import h5py
import os
import pint
from collections.abc import Iterable
from silx.io.url import DataUrl
from silx.io.utils import get_data
from datetime import datetime

from nxtomo.nxobject.nxdetector import ImageKey
from nxtomo.application.nxtomo import NXtomo
from nxtomo.nxobject.nxtransformations import NXtransformations
from nxtomo.utils.transformation import build_matrix, DetYFlipTransformation, DetZFlipTransformation
from nxtomo.paths.nxtomo import get_paths as _get_nexus_paths

from tomoscan.io import HDF5File
from tomoscan.series import Series
from tomoscan.esrf import NXtomoScan, EDFTomoScan
from tomoscan.esrf.scan.utils import (
    get_compacted_dataslices,
)  # this version has a 'return_url_set' needed here. At one point they should be merged together
from nabu.stitching.config import (
    PreProcessedSingleAxisStitchingConfiguration,
    KEY_IMG_REG_METHOD,
)
from nabu.stitching.utils import find_projections_relative_shifts
from functools import lru_cache as cache
from .single_axis import SingleAxisStitcher

_ureg = pint.get_application_registry()

_logger = logging.getLogger(__name__)


class PreProcessingStitching(SingleAxisStitcher):
    """
    loader to be used when save data during pre-processing stitching (on projections). Output is expected to be an NXtomo

    warning: axis are provided according to the `acquisition space <https://tomo.gitlab-pages.esrf.fr/bliss-tomo/master/modelization.html>`_
    """

    def __init__(self, configuration, progress=None) -> None:
        if not isinstance(configuration, PreProcessedSingleAxisStitchingConfiguration):
            raise TypeError(
                f"configuration is expected to be an instance of {PreProcessedSingleAxisStitchingConfiguration}. Get {type(configuration)} instead"
            )
        super().__init__(configuration, progress=progress)
        self._series = Series("series", iterable=configuration.input_scans, use_identifiers=False)
        self._reading_orders = []
        # TODO: rename flips to axis_0_flips, axis_1_flips, axis_2_flips...
        self._x_flips = []
        self._y_flips = []
        self._z_flips = []

        # 'expend' auto shift request if only set once for all
        if numpy.isscalar(self.configuration.axis_0_pos_px):
            self.configuration.axis_0_pos_px = [
                self.configuration.axis_0_pos_px,
            ] * (len(self.series) - 1)
        if numpy.isscalar(self.configuration.axis_1_pos_px):
            self.configuration.axis_1_pos_px = [
                self.configuration.axis_1_pos_px,
            ] * (len(self.series) - 1)
        if numpy.isscalar(self.configuration.axis_1_pos_px):
            self.configuration.axis_1_pos_px = [
                self.configuration.axis_1_pos_px,
            ] * (len(self.series) - 1)

        if self.configuration.axis_0_params is None:
            self.configuration.axis_0_params = {}
        if self.configuration.axis_1_params is None:
            self.configuration.axis_1_params = {}
        if self.configuration.axis_2_params is None:
            self.configuration.axis_2_params = {}

    def pre_processing_computation(self):
        self.compute_reduced_flats_and_darks()

    @property
    def stitching_axis_in_frame_space(self):
        if self.axis == 0:
            return 0
        elif self.axis == 1:
            return 1
        elif self.axis == 2:
            raise NotImplementedError(
                "pre-processing stitching along axis 2 is not handled. This would require to do interpolation between frame along the rotation angle. Just not possible"
            )
        else:
            raise NotImplementedError(f"stitching axis must be in (0, 1, 2). Get {self.axis}")

    @property
    def x_flips(self) -> list:
        return self._x_flips

    @property
    def y_flips(self) -> list:
        return self._y_flips

    def order_input_tomo_objects(self):

        def get_min_bound(scan):
            return scan.get_bounding_box(axis=self.axis).min

        # order scans along the stitched axis
        if self.axis == 0:
            position_along_stitched_axis = self.configuration.axis_0_pos_px
        elif self.axis == 1:
            position_along_stitched_axis = self.configuration.axis_1_pos_px
        else:
            raise ValueError(
                "stitching cannot be done along axis 2 for pre-processing. This would require to interpolate frame between different rotation angle"
            )
        # if axis 0 position is provided then use directly it
        if position_along_stitched_axis is not None and len(position_along_stitched_axis) > 0:
            order = numpy.argsort(position_along_stitched_axis)[::-1]
            sorted_series = Series(
                self.series.name,
                numpy.take_along_axis(numpy.array(self.series[:]), order, axis=0),
                use_identifiers=False,
            )
        else:
            # else use bounding box
            sorted_series = Series(
                self.series.name,
                sorted(self.series[:], key=get_min_bound, reverse=True),
                use_identifiers=False,
            )
        if sorted_series != self.series:
            if sorted_series[:] != self.series[::-1]:
                raise ValueError(
                    f"Unable to get comprehensive input. Axis {self.axis} (decreasing) ordering is not respected."
                )
            else:
                _logger.warning(
                    f"decreasing order haven't been respected. Need to reorder {self.serie_label} ({[str(scan) for scan in sorted_series[:]]}). Will also reorder overlap height, stitching height and invert shifts"
                )
                if self.configuration.axis_0_pos_mm is not None:
                    self.configuration.axis_0_pos_mm = self.configuration.axis_0_pos_mm[::-1]
                if self.configuration.axis_0_pos_px is not None:
                    self.configuration.axis_0_pos_px = self.configuration.axis_0_pos_px[::-1]
                if self.configuration.axis_1_pos_mm is not None:
                    self.configuration.axis_1_pos_mm = self.configuration.axis_1_pos_mm[::-1]
                if self.configuration.axis_1_pos_px is not None:
                    self.configuration.axis_1_pos_px = self.configuration.axis_1_pos_px[::-1]
                if self.configuration.axis_2_pos_mm is not None:
                    self.configuration.axis_2_pos_mm = self.configuration.axis_2_pos_mm[::-1]
                if self.configuration.axis_2_pos_px is not None:
                    self.configuration.axis_2_pos_px = self.configuration.axis_2_pos_px[::-1]
                if not numpy.isscalar(self._configuration.flip_ud):
                    self._configuration.flip_ud = self._configuration.flip_ud[::-1]
                if not numpy.isscalar(self._configuration.flip_lr):
                    self._configuration.flip_ud = self._configuration.flip_lr[::-1]

        self._series = sorted_series

    def check_inputs(self):
        """
        insure input data is coherent
        """
        n_scans = len(self.series)
        if n_scans == 0:
            raise ValueError("no scan to stich together")

        for scan in self.series:
            from tomoscan.scanbase import TomoScanBase

            if not isinstance(scan, TomoScanBase):
                raise TypeError(f"z-preproc stitching expects instances of {TomoScanBase}. {type(scan)} provided.")

        # check output file path and data path are provided
        if self.configuration.output_file_path in (None, ""):
            raise ValueError("output_file_path should be provided to the configuration")
        if self.configuration.output_data_path in (None, ""):
            raise ValueError("output_data_path should be provided to the configuration")

        # check number of shift provided
        for axis_pos_px, axis_name in zip(
            (
                self.configuration.axis_0_pos_px,
                self.configuration.axis_1_pos_px,
                self.configuration.axis_1_pos_px,
                self.configuration.axis_0_pos_mm,
                self.configuration.axis_1_pos_mm,
                self.configuration.axis_2_pos_mm,
            ),
            (
                "axis_0_pos_px",
                "axis_1_pos_px",
                "axis_2_pos_px",
                "axis_0_pos_mm",
                "axis_1_pos_mm",
                "axis_2_pos_mm",
            ),
        ):
            if isinstance(axis_pos_px, Iterable) and len(axis_pos_px) != (n_scans):
                raise ValueError(f"{axis_name} expect {n_scans} shift defined. Get {len(axis_pos_px)}")

        self._reading_orders = []
        # the first scan will define the expected reading orderd, and expected flip.
        # if all scan are flipped then we will keep it this way
        self._reading_orders.append(1)

        # check scans are coherent (nb projections, rotation angle, energy...)
        for scan_0, scan_1 in zip(self.series[0:-1], self.series[1:]):
            if len(scan_0.projections) != len(scan_1.projections):
                raise ValueError(f"{scan_0} and {scan_1} have a different number of projections")
            if isinstance(scan_0, NXtomoScan) and isinstance(scan_1, NXtomoScan):
                # check rotation (only of is an NXtomoScan)
                scan_0_angles = numpy.asarray(scan_0.rotation_angle)
                scan_0_projections_angles = scan_0_angles[
                    numpy.asarray(scan_0.image_key_control) == ImageKey.PROJECTION.value
                ]
                scan_1_angles = numpy.asarray(scan_1.rotation_angle)
                scan_1_projections_angles = scan_1_angles[
                    numpy.asarray(scan_1.image_key_control) == ImageKey.PROJECTION.value
                ]
                if not numpy.allclose(scan_0_projections_angles, scan_1_projections_angles, atol=10e-1):
                    if numpy.allclose(
                        scan_0_projections_angles,
                        scan_1_projections_angles[::-1],
                        atol=10e-1,
                    ):
                        reading_order = -1 * self._reading_orders[-1]
                    else:
                        raise ValueError(f"Angles from {scan_0} and {scan_1} are different")
                else:
                    reading_order = 1 * self._reading_orders[-1]
                self._reading_orders.append(reading_order)
            # check energy
            if scan_0.energy is None:
                _logger.warning(f"no energy found for {scan_0}")
            elif not numpy.isclose(scan_0.energy, scan_1.energy, rtol=1e-03):
                _logger.warning(
                    f"different energy found between {scan_0} ({scan_0.energy}) and {scan_1} ({scan_1.energy})"
                )
            # check FOV
            if not scan_0.field_of_view == scan_1.field_of_view:
                raise ValueError(f"{scan_0} and {scan_1} have different field of view")
            # check distance
            if scan_0.sample_detector_distance is None:
                _logger.warning(f"no distance found for {scan_0}")
            elif not numpy.isclose(scan_0.sample_detector_distance, scan_1.sample_detector_distance, rtol=10e-3):
                raise ValueError(f"{scan_0} and {scan_1} have different sample / detector distance")
            # check pixel size
            if not numpy.isclose(scan_0.sample_x_pixel_size, scan_1.sample_x_pixel_size):
                raise ValueError(
                    f"{scan_0} and {scan_1} have different x pixel size. {scan_0.sample_x_pixel_size} vs {scan_1.sample_x_pixel_size}"
                )
            if not numpy.isclose(scan_0.sample_y_pixel_size, scan_1.sample_y_pixel_size):
                raise ValueError(
                    f"{scan_0} and {scan_1} have different y pixel size. {scan_0.sample_y_pixel_size} vs {scan_1.sample_y_pixel_size}"
                )

        for scan in self.series:
            # check x, y and z translation are constant (only if is an NXtomoScan)
            if isinstance(scan, NXtomoScan):
                if scan.x_translation is not None and not numpy.isclose(
                    min(scan.x_translation), max(scan.x_translation)
                ):
                    _logger.warning(
                        "x translations appears to be evolving over time. Might end up with wrong stitching"
                    )
                if scan.y_translation is not None and not numpy.isclose(
                    min(scan.y_translation), max(scan.y_translation)
                ):
                    _logger.warning(
                        "y translations appears to be evolving over time. Might end up with wrong stitching"
                    )
                if scan.z_translation is not None and not numpy.isclose(
                    min(scan.z_translation), max(scan.z_translation)
                ):
                    _logger.warning(
                        "z translations appears to be evolving over time. Might end up with wrong stitching"
                    )

    def _compute_positions_as_px(self):
        """insure we have or we can deduce an estimated position as pixel"""

        def get_position_as_px_on_axis(axis, pos_as_px, pos_as_mm):
            if pos_as_px is not None:
                if pos_as_mm is not None:
                    raise ValueError(
                        f"position of axis {axis} is provided twice: as mm and as px. Please provide one only ({pos_as_mm} vs {pos_as_px})"
                    )
                else:
                    return pos_as_px

            elif pos_as_mm is not None:
                # deduce from position given in configuration and pixel size
                axis_N_pos_px = []
                for scan, pos_in_mm in zip(self.series, pos_as_mm):
                    pixel_size_m = self.configuration.pixel_size or scan.pixel_size
                    axis_N_pos_px.append((pos_in_mm * _ureg.millimeter).to_base_units().magnitude / pixel_size_m)
                return axis_N_pos_px
            else:
                # deduce from motor position and pixel size
                axis_N_pos_px = []
                base_position_m = self.series[0].get_bounding_box(axis=axis).min
                for scan in self.series:
                    pixel_size_m = self.configuration.pixel_size or scan.pixel_size
                    scan_axis_bb = scan.get_bounding_box(axis=axis)
                    axis_N_mean_pos_m = (scan_axis_bb.max - scan_axis_bb.min) / 2 + scan_axis_bb.min
                    axis_N_mean_rel_pos_m = axis_N_mean_pos_m - base_position_m
                    axis_N_pos_px.append(int(axis_N_mean_rel_pos_m / pixel_size_m))
                return axis_N_pos_px

        for axis, property_px_name, property_mm_name in zip(
            (0, 1, 2),
            (
                "axis_0_pos_px",
                "axis_1_pos_px",
                "axis_2_pos_px",
            ),
            (
                "axis_0_pos_mm",
                "axis_1_pos_mm",
                "axis_2_pos_mm",
            ),
        ):
            assert hasattr(
                self.configuration, property_px_name
            ), f"configuration API changed. should have {property_px_name}"
            assert hasattr(
                self.configuration, property_mm_name
            ), f"configuration API changed. should have {property_px_name}"
            try:
                new_px_position = get_position_as_px_on_axis(
                    axis=axis,
                    pos_as_px=getattr(self.configuration, property_px_name),
                    pos_as_mm=getattr(self.configuration, property_mm_name),
                )
            except ValueError:
                # when unable to find the position
                if axis == self.axis:
                    # if we cannot find position over the stitching axis then raise an error: unable to process without
                    raise
                else:
                    _logger.warning(f"Unable to find position over axis {axis}. Set them to zero")
                    setattr(
                        self.configuration,
                        property_px_name,
                        numpy.array([0] * len(self.series)),
                    )
            else:
                setattr(
                    self.configuration,
                    property_px_name,
                    new_px_position,
                )

        # clear position in mm as the one we will used are the px one
        self.configuration.axis_0_pos_mm = None
        self.configuration.axis_1_pos_mm = None
        self.configuration.axis_2_pos_mm = None

        # add some log
        if self.configuration.axis_2_pos_mm is not None or self.configuration.axis_2_pos_px is not None:
            _logger.warning("axis 2 position is not handled by the stitcher. Will be ignored")
        axis_0_pos = ", ".join([f"{pos}px" for pos in self.configuration.axis_0_pos_px])
        axis_1_pos = ", ".join([f"{pos}px" for pos in self.configuration.axis_1_pos_px])
        axis_2_pos = ", ".join([f"{pos}px" for pos in self.configuration.axis_2_pos_px])
        _logger.info(f"axis 0 position to be used: " + axis_0_pos)
        _logger.info(f"axis 1 position to be used: " + axis_1_pos)
        _logger.info(f"axis 2 position to be used: " + axis_2_pos)
        _logger.info(f"stitching will be applied along axis: {self.axis}")

    def compute_estimated_shifts(self):
        if self.axis == 0:
            # if we want to stitch over axis 0 (aka z)
            axis_0_pos_px = self.configuration.axis_0_pos_px
            self._axis_0_rel_ini_shifts = []
            # compute overlap along axis 0
            for upper_scan, lower_scan, upper_scan_axis_0_pos, lower_scan_axis_0_pos in zip(
                self.series[:-1], self.series[1:], axis_0_pos_px[:-1], axis_0_pos_px[1:]
            ):
                upper_scan_pos = upper_scan_axis_0_pos - upper_scan.dim_2 / 2
                lower_scan_high_pos = lower_scan_axis_0_pos + lower_scan.dim_2 / 2
                # simple test of overlap. More complete test are run by check_overlaps later
                if lower_scan_high_pos <= upper_scan_pos:
                    raise ValueError(f"no overlap found between {upper_scan} and {lower_scan}")
                self._axis_0_rel_ini_shifts.append(
                    int(lower_scan_high_pos - upper_scan_pos)  # overlap are expected to be int for now
                )
            self._axis_1_rel_ini_shifts = self.from_abs_pos_to_rel_pos(self.configuration.axis_1_pos_px)
            self._axis_2_rel_ini_shifts = [0.0] * (len(self.series) - 1)
        elif self.axis == 1:
            # if we want to stitch over axis 1 (aka Y in acquisition reference - which is x in frame reference)
            axis_1_pos_px = self.configuration.axis_1_pos_px
            self._axis_1_rel_ini_shifts = []
            # compute overlap along axis 0
            for left_scan, right_scan, left_scan_axis_1_pos, right_scan_axis_1_pos in zip(
                self.series[:-1], self.series[1:], axis_1_pos_px[:-1], axis_1_pos_px[1:]
            ):
                left_scan_pos = left_scan_axis_1_pos - left_scan.dim_1 / 2
                right_scan_high_pos = right_scan_axis_1_pos + right_scan.dim_1 / 2
                # simple test of overlap. More complete test are run by check_overlaps later
                if right_scan_high_pos <= left_scan_pos:
                    raise ValueError(f"no overlap found between {left_scan} and {right_scan}")
                self._axis_1_rel_ini_shifts.append(
                    int(right_scan_high_pos - left_scan_pos)  # overlap are expected to be int for now
                )
            self._axis_0_rel_ini_shifts = self.from_abs_pos_to_rel_pos(self.configuration.axis_0_pos_px)
            self._axis_2_rel_ini_shifts = [0.0] * (len(self.series) - 1)
        else:
            raise NotImplementedError("stitching only forseen for axis 0 and 1 for now")

    def _compute_shifts(self):
        """
        compute all shift requested (set to 'auto' in the configuration)

        """
        n_scans = len(self.configuration.input_scans)
        if n_scans == 0:
            raise ValueError("no scan to stich provided")

        projection_for_shift = self.configuration.slice_for_cross_correlation or "middle"
        if self.axis not in (0, 1):
            raise NotImplementedError("only stitching over axis 0 and 2 are handled for pre-processing stitching")

        final_rel_shifts = []
        for (
            scan_0,
            scan_1,
            order_s0,
            order_s1,
            x_rel_shift,
            y_rel_shift,
        ) in zip(
            self.series[:-1],
            self.series[1:],
            self.reading_orders[:-1],
            self.reading_orders[1:],
            self._axis_1_rel_ini_shifts,
            self._axis_0_rel_ini_shifts,
        ):
            x_cross_algo = self.configuration.axis_1_params.get(KEY_IMG_REG_METHOD, None)
            y_cross_algo = self.configuration.axis_0_params.get(KEY_IMG_REG_METHOD, None)

            # compute relative shift
            found_shift_y, found_shift_x = find_projections_relative_shifts(
                upper_scan=scan_0,
                lower_scan=scan_1,
                projection_for_shift=projection_for_shift,
                x_cross_correlation_function=x_cross_algo,
                y_cross_correlation_function=y_cross_algo,
                x_shifts_params=self.configuration.axis_1_params,  # image x map acquisition axis 1 (Y)
                y_shifts_params=self.configuration.axis_0_params,  # image y map acquisition axis 0 (Z)
                invert_order=order_s1 != order_s0,
                estimated_shifts=(y_rel_shift, x_rel_shift),
                axis=self.axis,
            )
            final_rel_shifts.append(
                (found_shift_y, found_shift_x),
            )

        # set back values. Now position should start at 0
        self._axis_0_rel_final_shifts = [final_shift[0] for final_shift in final_rel_shifts]
        self._axis_1_rel_final_shifts = [final_shift[1] for final_shift in final_rel_shifts]
        self._axis_2_rel_final_shifts = [0.0] * len(final_rel_shifts)
        _logger.info(f"axis 1 relative shifts (x in radio ref) to be used will be {self._axis_0_rel_final_shifts}")
        print(f"axis 1 relative shifts (x in radio ref) to be used will be {self._axis_0_rel_final_shifts}")
        _logger.info(f"axis 0 relative shifts (y in radio ref) y to be used will be {self._axis_1_rel_final_shifts}")
        print(f"axis 0 relative shifts (y in radio ref) y to be used will be {self._axis_1_rel_final_shifts}")

    def _create_nx_tomo(self, store_composition: bool = False):
        """
        create final NXtomo with stitched frames.
        Policy: save all projections flat fielded. So this NXtomo will only contain projections (no dark and no flat).
        But nabu will be able to reconstruct it with field `flatfield` set to False
        """
        nx_tomo = NXtomo()

        nx_tomo.energy = self.series[0].energy * _ureg.keV
        start_times = list(filter(None, [scan.start_time for scan in self.series]))
        end_times = list(filter(None, [scan.end_time for scan in self.series]))

        if len(start_times) > 0:
            nx_tomo.start_time = (
                numpy.asarray([numpy.datetime64(start_time) for start_time in start_times]).min().astype(datetime)
            )
        else:
            _logger.warning("Unable to find any start_time from input")
        if len(end_times) > 0:
            nx_tomo.end_time = (
                numpy.asarray([numpy.datetime64(end_time) for end_time in end_times]).max().astype(datetime)
            )
        else:
            _logger.warning("Unable to find any end_time from input")

        title = ";".join([scan.sequence_name or "" for scan in self.series])
        nx_tomo.title = f"stitch done from {title}"

        self._slices_to_stitch, n_proj = self.configuration.settle_slices()

        # handle detector (without frames)
        nx_tomo.instrument.detector.field_of_view = self.series[0].field_of_view
        nx_tomo.instrument.detector.distance = self.series[0].sample_detector_distance * _ureg.meter
        nx_tomo.instrument.detector.x_pixel_size = self.series[0].x_pixel_size * _ureg.meter
        nx_tomo.instrument.detector.y_pixel_size = self.series[0].y_pixel_size * _ureg.meter
        nx_tomo.instrument.detector.image_key_control = [ImageKey.PROJECTION] * n_proj
        nx_tomo.instrument.detector.tomo_n = n_proj
        # note: stitching process insure un-flipping of frames. So make sure transformations is defined as an empty set
        nx_tomo.instrument.detector.transformations = NXtransformations()

        if isinstance(self.series[0], NXtomoScan):
            # note: first scan is always the reference as order to read data (so no rotation_angle inversion here)
            rotation_angle = numpy.asarray(self.series[0].rotation_angle) * _ureg.degree
            nx_tomo.sample.rotation_angle = rotation_angle[
                numpy.asarray(self.series[0].image_key_control) == ImageKey.PROJECTION.value
            ]
        elif isinstance(self.series[0], EDFTomoScan):
            nx_tomo.sample.rotation_angle = (
                numpy.linspace(start=0, stop=self.series[0].scan_range, num=self.series[0].tomo_n) * _ureg.degree
            )
        else:
            raise NotImplementedError(
                f"scan type ({type(self.series[0])} is not handled)",
                NXtomoScan,
                isinstance(self.series[0], NXtomoScan),
            )

        # do a sub selection of the rotation angle if a we are only computing a part of the slices
        def apply_slices_selection(array, slices, allow_empty: bool = False):
            if isinstance(slices, slice):
                return array[slices.start : slices.stop : 1]
            elif isinstance(slices, Iterable):
                return [array[index] for index in slices]
            else:
                raise RuntimeError("slices must be instance of a slice or of an iterable")  # noqa: TRY004

        nx_tomo.sample.rotation_angle = (
            apply_slices_selection(
                array=nx_tomo.sample.rotation_angle.to_base_units().magnitude, slices=self._slices_to_stitch
            )
            * _ureg.degree
        )

        # handle sample
        if False not in [isinstance(scan, NXtomoScan) for scan in self.series]:

            def get_sample_translation_for_projs(scan: NXtomoScan, attr):
                values = numpy.array(getattr(scan, attr))
                mask = scan.image_key_control == ImageKey.PROJECTION.value
                return values[mask]

            # we consider the new x, y and z position to be at the center of the one created
            x_translation = [
                get_sample_translation_for_projs(scan, "x_translation")
                for scan in self.series
                if scan.x_translation is not None
            ]
            if len(x_translation) > 0:
                # if there is some metadata about {x|y|z} translations
                # we want to take the mean of each frame for each projections
                x_translation = apply_slices_selection(
                    numpy.array(x_translation).mean(axis=0),
                    slices=self._slices_to_stitch,
                )
            else:
                # if no NXtomo has information about x_translation.
                # note: if at least one has missing values the numpy.Array(x_translation) with create an error as well
                x_translation = [0.0] * n_proj
                _logger.warning("Unable to fin input nxtomo x_translation values. Set it to 0.0")
            nx_tomo.sample.x_translation = x_translation * _ureg.meter

            y_translation = [
                get_sample_translation_for_projs(scan, "y_translation")
                for scan in self.series
                if scan.y_translation is not None
            ]
            if len(y_translation) > 0:
                y_translation = apply_slices_selection(
                    numpy.array(y_translation).mean(axis=0),
                    slices=self._slices_to_stitch,
                )
            else:
                y_translation = [0.0] * n_proj
                _logger.warning("Unable to fin input nxtomo y_translation values. Set it to 0.0")
            nx_tomo.sample.y_translation = y_translation * _ureg.meter
            z_translation = [
                get_sample_translation_for_projs(scan, "z_translation")
                for scan in self.series
                if scan.z_translation is not None
            ]
            if len(z_translation) > 0:
                z_translation = apply_slices_selection(
                    numpy.array(z_translation).mean(axis=0),
                    slices=self._slices_to_stitch,
                )
            else:
                z_translation = [0.0] * n_proj
                _logger.warning("Unable to fin input nxtomo z_translation values. Set it to 0.0")
            nx_tomo.sample.z_translation = z_translation * _ureg.meter

            nx_tomo.sample.name = self.series[0].sample_name

        # compute stitched frame shape
        if self.axis == 0:
            stitched_frame_shape = (
                n_proj,
                (
                    numpy.asarray([scan.dim_2 for scan in self.series]).sum()
                    - numpy.asarray([abs(overlap) for overlap in self._axis_0_rel_final_shifts]).sum()
                ),
                self._stitching_constant_length,
            )
        elif self.axis == 1:
            stitched_frame_shape = (
                n_proj,
                self._stitching_constant_length,
                (
                    numpy.asarray([scan.dim_1 for scan in self.series]).sum()
                    - numpy.asarray([abs(overlap) for overlap in self._axis_1_rel_final_shifts]).sum()
                ),
            )
        else:
            raise NotImplementedError("stitching on pre-processing along axis 2 (x-ray direction) is not handled")

        if stitched_frame_shape[0] < 1 or stitched_frame_shape[1] < 1 or stitched_frame_shape[2] < 1:
            raise RuntimeError(f"Error in stitched frame shape calculation. {stitched_frame_shape} found.")
        # get expected output dataset first (just in case output and input files are the same)
        first_proj_idx = sorted(self.series[0].projections.keys())[0]
        first_proj_url = self.series[0].projections[first_proj_idx]
        if h5py.is_hdf5(first_proj_url.file_path()):
            first_proj_url = DataUrl(
                file_path=first_proj_url.file_path(),
                data_path=first_proj_url.data_path(),
                scheme="h5py",
            )

        # first save the NXtomo entry without the frame
        # dicttonx will fail if the folder does not exists
        dir_name = os.path.dirname(self.configuration.output_file_path)
        if dir_name not in (None, ""):
            os.makedirs(dir_name, exist_ok=True)
        nx_tomo.save(
            file_path=self.configuration.output_file_path,
            data_path=self.configuration.output_data_path,
            nexus_path_version=self.configuration.output_nexus_version,
            overwrite=self.configuration.overwrite_results,
        )

        transformation_matrices = {
            scan.get_identifier()
            .to_str()
            .center(80, "-"): numpy.array2string(build_matrix(scan.get_detector_transformations(tuple())))
            for scan in self.series
        }
        _logger.info(
            "scan detector transformation matrices are:\n"
            "\n".join(["/n".join(item) for item in transformation_matrices.items()])
        )

        _logger.info(
            f"reading order is {self.reading_orders}",
        )

        def get_output_data_type():
            return numpy.float32  # because we will apply flat field correction on it and they are not raw data

        output_dtype = get_output_data_type()
        # append frames ("instrument/detector/data" dataset)
        with HDF5File(self.configuration.output_file_path, mode="a") as h5f:
            # note: nx_tomo.save already handles the possible overwrite conflict by removing
            # self.configuration.output_file_path or raising an error

            stitched_frame_path = "/".join(
                [
                    self.configuration.output_data_path,
                    _get_nexus_paths(self.configuration.output_nexus_version).PROJ_PATH,
                ]
            )
            self.dumper.output_dataset = h5f.create_dataset(
                name=stitched_frame_path,
                shape=stitched_frame_shape,
                dtype=output_dtype,
            )
            # TODO: we could also create in several time and create a virtual dataset from it.
            scans_projections_indexes = []
            for scan, reverse in zip(self.series, self.reading_orders):
                scans_projections_indexes.append(sorted(scan.projections.keys(), reverse=(reverse == -1)))
            if self.progress is not None:
                self.progress.total = self.get_n_slices_to_stitch()

            if isinstance(self._slices_to_stitch, slice):
                step = self._slices_to_stitch.step or 1
            else:
                step = 1
            i_proj = 0
            for bunch_start, bunch_end in self._data_bunch_iterator(slices=self._slices_to_stitch, bunch_size=50):
                for data_frames in self._get_bunch_of_data(
                    bunch_start,
                    bunch_end,
                    step=step,
                    scans=self.series,
                    scans_projections_indexes=scans_projections_indexes,
                    flip_ud_arr=self.configuration.flip_ud,
                    flip_lr_arr=self.configuration.flip_lr,
                    reading_orders=self.reading_orders,
                ):
                    if self.configuration.rescale_frames:
                        data_frames = self.rescale_frames(data_frames)
                    if self.configuration.normalization_by_sample.is_active():
                        data_frames = self.normalize_frame_by_sample(data_frames)

                    sf = SingleAxisStitcher.stitch_frames(
                        frames=data_frames,
                        axis=self.axis,
                        x_relative_shifts=self._axis_1_rel_final_shifts,
                        y_relative_shifts=self._axis_0_rel_final_shifts,
                        overlap_kernels=self._overlap_kernels,
                        i_frame=i_proj,
                        output_dtype=output_dtype,
                        dumper=self.dumper,
                        return_composition_cls=store_composition if i_proj == 0 else False,
                        stitching_axis=self.axis,
                        pad_mode=self.configuration.pad_mode,
                        alignment=self.configuration.alignment_axis_2,
                        new_width=self._stitching_constant_length,
                        check_inputs=i_proj == 0,  # on process check on the first iteration
                    )
                    if i_proj == 0 and store_composition:
                        _, self._frame_composition = sf
                    if self.progress is not None:
                        self.progress.update()

                    i_proj += 1

            # create link to this dataset that can be missing
            # "data/data" link
            if "data" in h5f[self.configuration.output_data_path]:
                data_group = h5f[self.configuration.output_data_path]["data"]
                if not stitched_frame_path.startswith("/"):
                    stitched_frame_path = "/" + stitched_frame_path
                data_group["data"] = h5py.SoftLink(stitched_frame_path)
                if "default" not in h5f[self.configuration.output_data_path].attrs:
                    h5f[self.configuration.output_data_path].attrs["default"] = "data"
                for attr_name, attr_value in zip(
                    ("NX_class", "SILX_style/axis_scale_types", "signal"),
                    ("NXdata", ["linear", "linear"], "data"),
                ):
                    if attr_name not in data_group.attrs:
                        data_group.attrs[attr_name] = attr_value

        return nx_tomo

    def _create_stitching(self, store_composition):
        self._create_nx_tomo(store_composition=store_composition)

    @staticmethod
    def get_bunch_of_data(
        bunch_start: int,
        bunch_end: int,
        step: int,
        scans: tuple,
        scans_projections_indexes: tuple,
        reading_orders: tuple,
        flip_lr_arr: tuple,
        flip_ud_arr: tuple,
    ):
        """
        goal is to load contiguous projections as much as possible...

        :param int bunch_start: beginning of the bunch
        :param int bunch_end: end of the bunch
        :param int scans: ordered scan for which we want to get data
        :param scans_projections_indexes: tuple with scans and scan projection indexes to be loaded
        :param tuple flip_lr_arr: extra information from the user to left-right flip frames
        :param tuple flip_ud_arr: extra information from the user to up-down flip frames
        :return: list of lists. Each frame to stitch contains the (flat-fielded) frames to stitch together
        """
        assert len(scans) == len(scans_projections_indexes)
        assert isinstance(flip_lr_arr, tuple)
        assert isinstance(flip_ud_arr, tuple)
        assert isinstance(step, int)
        scans_proj_urls = []
        # for each scan store the real indices and the data url

        for scan, scan_projection_indexes in zip(scans, scans_projections_indexes):
            scan_proj_urls = {}
            # for each scan get the list of url to be loaded
            for i_proj in range(bunch_start, bunch_end):
                if i_proj % step != 0:
                    continue
                proj_index_in_full_scan = scan_projection_indexes[i_proj]
                scan_proj_urls[proj_index_in_full_scan] = scan.projections[proj_index_in_full_scan]
            scans_proj_urls.append(scan_proj_urls)

        # then load data
        all_scan_final_data = numpy.empty((bunch_end - bunch_start, len(scans)), dtype=object)
        from nabu.preproc.flatfield import FlatFieldArrays

        for i_scan, (scan_urls, scan_flip_lr, scan_flip_ud, reading_order) in enumerate(
            zip(scans_proj_urls, flip_lr_arr, flip_ud_arr, reading_orders)
        ):
            i_frame = 0
            _, set_of_compacted_slices = get_compacted_dataslices(scan_urls, return_url_set=True)
            for url in set_of_compacted_slices.values():
                scan = scans[i_scan]
                url = DataUrl(
                    file_path=url.file_path(),
                    data_path=url.data_path(),
                    scheme="silx",
                    data_slice=url.data_slice(),
                )
                raw_radios = get_data(url)[::reading_order]
                radio_indices = url.data_slice()
                if isinstance(radio_indices, slice):
                    step = radio_indices.step if radio_indices is not None else 1
                    radio_indices = numpy.arange(
                        start=radio_indices.start,
                        stop=radio_indices.stop,
                        step=step,
                        dtype=numpy.int16,
                    )

                missing = []
                if len(scan.reduced_flats) == 0:
                    missing = "flats"
                if len(scan.reduced_darks) == 0:
                    missing = "darks"

                if len(missing) > 0:
                    _logger.warning(f"missing {'and'.join(missing)}. Unable to do flat field correction")
                    ff_arrays = None
                    data = raw_radios
                else:
                    has_reduced_metadata = (
                        scan.reduced_flats_infos is not None
                        and len(scan.reduced_flats_infos.machine_current) > 0
                        and scan.reduced_darks_infos is not None
                        and len(scan.reduced_darks_infos.machine_current) > 0
                    )
                    if not has_reduced_metadata:
                        _logger.warning("no metadata about current found. Won't normalize according to machine current")

                    ff_arrays = FlatFieldArrays(
                        radios_shape=(len(radio_indices), scan.dim_2, scan.dim_1),
                        flats=scan.reduced_flats,
                        darks=scan.reduced_darks,
                        radios_indices=radio_indices,
                        radios_srcurrent=scan.machine_current[radio_indices] if has_reduced_metadata else None,
                        flats_srcurrent=(scan.reduced_flats_infos.machine_current if has_reduced_metadata else None),
                    )
                    # note: we need to cast radios to float 32. Darks and flats are cast to anyway
                    data = ff_arrays.normalize_radios(raw_radios.astype(numpy.float32))

                transformations = list(scans[i_scan].get_detector_transformations(tuple()))
                if scan_flip_lr:
                    transformations.append(DetZFlipTransformation(flip=True))
                if scan_flip_ud:
                    transformations.append(DetYFlipTransformation(flip=True))

                transformation_matrix_det_space = build_matrix(transformations)
                if transformation_matrix_det_space is None or numpy.allclose(
                    transformation_matrix_det_space, numpy.identity(3)
                ):
                    flip_ud = False
                    flip_lr = False
                elif numpy.array_equal(transformation_matrix_det_space, PreProcessingStitching._get_UD_flip_matrix()):
                    flip_ud = True
                    flip_lr = False
                elif numpy.allclose(transformation_matrix_det_space, PreProcessingStitching._get_LR_flip_matrix()):
                    flip_ud = False
                    flip_lr = True
                elif numpy.allclose(
                    transformation_matrix_det_space, PreProcessingStitching._get_UD_AND_LR_flip_matrix()
                ):
                    flip_ud = True
                    flip_lr = True
                else:
                    raise ValueError("case not handled... For now only handle up-down flip as left-right flip")

                for frame in data:
                    if flip_ud:
                        frame = numpy.flipud(frame)
                    if flip_lr:
                        frame = numpy.fliplr(frame)
                    all_scan_final_data[i_frame, i_scan] = frame
                    i_frame += 1

        return all_scan_final_data

    def compute_reduced_flats_and_darks(self):
        """
        make sure reduced dark and flats are existing otherwise compute them
        """
        # TODO
        # ruff: noqa: SIM105, S110
        # --
        for scan in self.series:
            try:
                reduced_darks, darks_infos = scan.load_reduced_darks(return_info=True)
            except:
                _logger.info("no reduced dark found. Try to compute them.")
            if reduced_darks in (None, {}):
                reduced_darks, darks_infos = scan.compute_reduced_darks(return_info=True)
                try:
                    # if we don't have write in the folder containing the .nx for example
                    scan.save_reduced_darks(reduced_darks, darks_infos=darks_infos)
                except Exception:
                    pass
            scan.set_reduced_darks(reduced_darks, darks_infos=darks_infos)

            try:
                reduced_flats, flats_infos = scan.load_reduced_flats(return_info=True)
            except:
                _logger.info("no reduced flats found. Try to compute them.")
            if reduced_flats in (None, {}):
                reduced_flats, flats_infos = scan.compute_reduced_flats(return_info=True)
                try:
                    # if we don't have write in the folder containing the .nx for example
                    scan.save_reduced_flats(reduced_flats, flats_infos=flats_infos)
                except Exception:
                    pass
            scan.set_reduced_flats(reduced_flats, flats_infos=flats_infos)

    @staticmethod
    @cache(maxsize=None)
    def _get_UD_flip_matrix():
        return DetYFlipTransformation(flip=True).as_matrix()

    @staticmethod
    @cache(maxsize=None)
    def _get_LR_flip_matrix():
        return DetZFlipTransformation(flip=True).as_matrix()

    @staticmethod
    @cache(maxsize=None)
    def _get_UD_AND_LR_flip_matrix():
        return numpy.matmul(
            PreProcessingStitching._get_UD_flip_matrix(),
            PreProcessingStitching._get_LR_flip_matrix(),
        )

    @staticmethod
    def _get_bunch_of_data(
        bunch_start: int,
        bunch_end: int,
        step: int,
        scans: tuple,
        scans_projections_indexes: tuple,
        reading_orders: tuple,
        flip_lr_arr: tuple,
        flip_ud_arr: tuple,
    ):
        """
        goal is to load contiguous projections as much as possible...

        :param int bunch_start: beginning of the bunch
        :param int bunch_end: end of the bunch
        :param int scans: ordered scan for which we want to get data
        :param scans_projections_indexes: tuple with scans and scan projection indexes to be loaded
        :param tuple flip_lr_arr: extra information from the user to left-right flip frames
        :param tuple flip_ud_arr: extra information from the user to up-down flip frames
        :return: list of lists. Each frame to stitch contains the (flat-fielded) frames to stitch together
        """
        assert len(scans) == len(scans_projections_indexes)
        assert isinstance(flip_lr_arr, tuple)
        assert isinstance(flip_ud_arr, tuple)
        assert isinstance(step, int)
        scans_proj_urls = []
        # for each scan store the real indices and the data url

        for scan, scan_projection_indexes in zip(scans, scans_projections_indexes):
            scan_proj_urls = {}
            # for each scan get the list of url to be loaded
            for i_proj in range(bunch_start, bunch_end):
                if i_proj % step != 0:
                    continue
                proj_index_in_full_scan = scan_projection_indexes[i_proj]
                scan_proj_urls[proj_index_in_full_scan] = scan.projections[proj_index_in_full_scan]
            scans_proj_urls.append(scan_proj_urls)

        # then load data
        all_scan_final_data = numpy.empty((bunch_end - bunch_start, len(scans)), dtype=object)
        from nabu.preproc.flatfield import FlatFieldArrays

        for i_scan, (scan_urls, scan_flip_lr, scan_flip_ud, reading_order) in enumerate(
            zip(scans_proj_urls, flip_lr_arr, flip_ud_arr, reading_orders)
        ):
            i_frame = 0
            _, set_of_compacted_slices = get_compacted_dataslices(scan_urls, return_url_set=True)
            for url in set_of_compacted_slices.values():
                scan = scans[i_scan]
                url = DataUrl(
                    file_path=url.file_path(),
                    data_path=url.data_path(),
                    scheme="silx",
                    data_slice=url.data_slice(),
                )
                raw_radios = get_data(url)[::reading_order]
                radio_indices = url.data_slice()
                if isinstance(radio_indices, slice):
                    step = radio_indices.step if radio_indices is not None else 1
                    radio_indices = numpy.arange(
                        start=radio_indices.start,
                        stop=radio_indices.stop,
                        step=step,
                        dtype=numpy.int16,
                    )

                missing = []
                if len(scan.reduced_flats) == 0:
                    missing.append("flats")
                if len(scan.reduced_darks) == 0:
                    missing.append("darks")

                if len(missing) > 0:
                    _logger.warning(f"missing {' and '.join(missing)}. Unable to do flat field correction")
                    ff_arrays = None
                    data = raw_radios
                else:
                    has_reduced_metadata = (
                        scan.reduced_flats_infos is not None
                        and len(scan.reduced_flats_infos.machine_current) > 0
                        and scan.reduced_darks_infos is not None
                        and len(scan.reduced_darks_infos.machine_current) > 0
                    )
                    if not has_reduced_metadata:
                        _logger.warning("no metadata about current found. Won't normalize according to machine current")

                    ff_arrays = FlatFieldArrays(
                        radios_shape=(len(radio_indices), scan.dim_2, scan.dim_1),
                        flats=scan.reduced_flats,
                        darks=scan.reduced_darks,
                        radios_indices=radio_indices,
                        radios_srcurrent=scan.machine_current[radio_indices] if has_reduced_metadata else None,
                        flats_srcurrent=(scan.reduced_flats_infos.machine_current if has_reduced_metadata else None),
                    )
                    # note: we need to cast radios to float 32. Darks and flats are cast to anyway
                    data = ff_arrays.normalize_radios(raw_radios.astype(numpy.float32))

                transformations = list(scans[i_scan].get_detector_transformations(tuple()))
                if scan_flip_lr:
                    transformations.append(DetZFlipTransformation(flip=True))
                if scan_flip_ud:
                    transformations.append(DetYFlipTransformation(flip=True))

                transformation_matrix_det_space = build_matrix(transformations)
                if transformation_matrix_det_space is None or numpy.allclose(
                    transformation_matrix_det_space, numpy.identity(3)
                ):
                    flip_ud = False
                    flip_lr = False
                elif numpy.array_equal(transformation_matrix_det_space, PreProcessingStitching._get_UD_flip_matrix()):
                    flip_ud = True
                    flip_lr = False
                elif numpy.allclose(transformation_matrix_det_space, PreProcessingStitching._get_LR_flip_matrix()):
                    flip_ud = False
                    flip_lr = True
                elif numpy.allclose(
                    transformation_matrix_det_space, PreProcessingStitching._get_UD_AND_LR_flip_matrix()
                ):
                    flip_ud = True
                    flip_lr = True
                else:
                    raise ValueError("case not handled... For now only handle up-down flip as left-right flip")

                for frame in data:
                    if flip_ud:
                        frame = numpy.flipud(frame)
                    if flip_lr:
                        frame = numpy.fliplr(frame)
                    all_scan_final_data[i_frame, i_scan] = frame
                    i_frame += 1

        return all_scan_final_data
