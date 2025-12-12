from ...preproc.flatfield import FlatFieldArrays
import numpy as np
from scipy import ndimage as nd
import math


class GriddedAccumulator:
    nominal_current = 0.2

    def __init__(
        self,
        gridded_radios,
        gridded_weights,
        diagnostic_radios,
        diagnostic_weights,
        diagnostic_angles,
        diagnostic_searched_angles_rad_clipped,
        diagnostic_zpix_transl,
        diag_zpro_run=0,
        dark=None,
        flat_indexes=None,
        flats=None,
        weights=None,
        double_flat=None,
        radios_srcurrent=None,
        flats_srcurrent=None,
    ):
        """
        This class creates, for a selected volume slab, a standard set of radios from a helical dataset.

        Parameters
        ----------
        gridded_radios : 3D np.array
           this is the stack of new radios which will be resynthesized, by this class,
           for a selected slab.
           The object is initialised with this array, and this array will accumulate, during subsequent
           calls to  method extract_preprocess_with_flats, the sum of the transformed contributions
           obtained from the arguments of the mentioned method (extract_preprocess_with_flats).
        gridded_weights : 3d np.array
           same shape as gridded_radios, but it will accumulate the weights, during calls to
           extract_preprocess_with_flats
        diag_zpro_run: int
           if > 0 then only the diagnostics are filled, and no accumulation is done

        diagnostic_searched_angles_rad_clipped:
           the angles between 0 and 2pi. The contributions to diagnostic will be searched for these angles
           plus for the same angles + 2pi ( following turn)

        diagnostic_radios   : 3d np.array,  a stack composed of
           each radio must have the same size as a radio of the gridded_radios argument.
           During the calls to extract_preprocess_with_flats methods,
           the  radios will collect the transformed data for the angles given by diagnostic_searched_angles_rad_clipped and redundancy
        diagnostic_weights: 3d np.array  a stack composed of two radios
           Same shape as diagnostic_radios. The weights for diagnostic radios ( will be zero on pixel
           where no data is available, or where the weight is null)
        diagnostic_angles : 1D np.array
           Must have shape==(2*len(diagnostic_searched_angles_rad_clipped),). The entries will be filled with the angles at which the contributions
           to diagnostic_radios have been summed.
        diagnostic_zpix_transl: 1D np.array
           same as for diagnostic_angles, but for vertical translation in pixels
        dark:  None or 2D np.array
           must have the shape of the detector ( generally larger that a radio of gridded_radios)
           If given, the dark will be subtracted from data and flats.
        radios_srcurrent: 1D np.array
             the machine current for every radio
        flats_srcurrent: 1D np.array
             the machine current for every flat


        flat_indexes: None or a list of integers
           the projection index corresponding to the flats
        flats   : None or 3D np.array
           the stack of flats. Each flat must have the shape of the detector  (generally larger that a radio of gridded_radios)
           The flats, if given, are subtracted of the dark, if given, and the result is used to normalise the data.
        weights      : None or 2D np.array
           If not given each data pixel will be considered with unit weight.
           If given it must have the same shape as the detector.
        double_flat  = None or 2D np.array
           If given, the double flat will be applied (division by double_flat)
           Must have  the same shape as the detector.
        """
        self.diag_zpro_run = diag_zpro_run
        self.gridded_radios = gridded_radios
        self.gridded_weights = gridded_weights
        self.diagnostic_radios = diagnostic_radios
        self.diagnostic_weights = diagnostic_weights
        self.diagnostic_angles = diagnostic_angles

        self.diagnostic_zpix_transl = diagnostic_zpix_transl
        self.diagnostic_searched_angles_rad_clipped = diagnostic_searched_angles_rad_clipped

        self.dark = dark

        self.radios_srcurrent = radios_srcurrent

        self.flats_srcurrent = flats_srcurrent

        self.flat_indexes = flat_indexes
        self.flat_indexes_reverse_map = dict(  # noqa: C404
            [(global_index, local_index) for (local_index, global_index) in enumerate(flat_indexes)]
        )
        self.flats = flats
        self.weights = weights
        self.double_flat = double_flat

    def extract_preprocess_with_flats(
        self,
        subchunk_slice,
        subchunk_file_indexes,
        chunk_info,
        subr_start_end,
        dtasrc_start_end,
        data_raw,
        radios_angular_range_slicing,
    ):
        """
        This functions is meant to be called providing, each time, a subset of the data
        which are needed to reconstruct a chunk (to reconstruct a slab).
        When all the necessary data have flown through the subsequent  calls to this method,
        the accumulators are ready.

        Parameters
        ----------
        subchunk_slice: an object of the python class "slice"
          this slice slices the angular domain which corresponds to the useful
          projections  which are useful for the chunk, and whose information
          are contained in the companion argument "chunk_info"
          Such slicing correspond to the angular subset, for which we are providing
          data_raw
        subchunk_file_indexes: a sequence of integers.
           they correspond to the projection numbers from which the data in data_raw are coming.
           They are used to interpolate between flat fields
        chunk_info: an object returned by the get_chunk_info of the SpanStrategy class
                  this object must have the following members, which relates to the wanted chunk

                  angle_index_span: a pair of integers indicating the start and the end of useful angles
                        in the array of all the scan angle self.projection_angles_deg
                  span_v:  a pair of two integers indicating the start and end of the span relatively  to the lowest value
                        of array self.total_view_heights
                  integer_shift_v: an array, containing for each one of the  useful projections of the span,
                       the integer part of vertical shift to be used in cropping,
                  fract_complement_to_integer_shift_v :
                       the fractional remainder for cropping.
                  z_pix_per_proj: an array, containing for each to be used projection of the span
                       the vertical shift
                  x_pix_per_proj: ....the horizontal shift
                       angles_rad    :    an array, for each useful projection of the chunk the angle in radian
        subr_start_end: a pair of integers
            the start height, and the end height, of the slab for which we are collecting the data.
            The number are given with the same logic as for member span_v of the chunk_info.
            Without the phase margin, when the phase margin is zero, hey would correspond exactly to
            the start and end, vertically, of the reconstructed slices.
        dtasrc_start_end: a pair of integers
            These numbers are relative to the detector ( they are detector line indexes).
            They indicate, vertically, the detector portion the data_raw data correspond to
        data_raw: np.array 3D
            the data which correspond to a limited detector stripe and a limited angular subset
        radios_angular_range_slicing:
            my_subsampled_indexes  is important in order to compare the
            radios positions with respect to the flat position, and these position
            are given as the sequential acquisition number which counts everything ( flats, darks, radios )
            Instead, in order to access array which spans only the radios, we need to have an idea of where we are.
            this is provided by radios_angular_range_slicing which addresses the radios domain

        """

        # the object below is going to containing some auxiliary variable that are use to reframe the data.
        # This object is used to pass in a compact way such informations to different methods.
        # The informations are extracted from chunk info
        reframing_infos = self._ReframingInfos(
            chunk_info, subchunk_slice, subr_start_end, dtasrc_start_end, subchunk_file_indexes
        )

        # give the proper dimensioning to an auxiliary stack which will contain the reframed data extracted
        # from the treatement of the sub-chunk
        radios_subset = np.zeros(
            [data_raw.shape[0], subr_start_end[1] - subr_start_end[0], data_raw.shape[2]], np.float32
        )

        # ... and in the same way we dimension the container for the  associated reframed weights.
        radios_weights_subset = np.zeros(
            [data_raw.shape[0], subr_start_end[1] - subr_start_end[0], data_raw.shape[2]], np.float32
        )

        # extraction of the data
        self._extract_preprocess_with_flats(
            data_raw, reframing_infos, chunk_info, radios_subset, radios_angular_range_slicing
        )

        if self.weights is not None:
            # ... and, if required, extraction of the associated weights
            wdata_read = self.weights.data[reframing_infos.dtasrc_start_z : reframing_infos.dtasrc_end_z]
            self._extract_preprocess_with_flats(
                wdata_read, reframing_infos, chunk_info, radios_weights_subset, it_is_weight=True
            )

        else:
            radios_weights_subset[:] = 1.0

        # and the remaining part is a simple projection over the accumulators,  for
        # the data and for the weights
        my_angles = chunk_info.angles_rad[subchunk_slice]

        n_gridded_angles = self.gridded_radios.shape[0]

        my_i_float = my_angles * (n_gridded_angles / (2 * math.pi))

        tmp_i_rounded = np.floor(my_i_float).astype(np.int32)
        my_epsilon = my_i_float - tmp_i_rounded
        my_i0 = np.mod(tmp_i_rounded, n_gridded_angles)
        my_i1 = np.mod(my_i0 + 1, n_gridded_angles)

        if self.diag_zpro_run:
            # these are used only when collection the diagnostics

            # an estimation of the angular step
            my_angle_step_rad = abs(np.diff(chunk_info.angles_rad[subchunk_slice]).mean())
            my_angles_02pi = np.mod(my_angles, 2 * np.pi)
            # bins are delimited by ticks
            ticks = np.empty(2 * len(self.diagnostic_searched_angles_rad_clipped), "f")
            ticks[::2] = self.diagnostic_searched_angles_rad_clipped - my_angle_step_rad / 2
            ticks[1::2] = ticks[::2] + my_angle_step_rad

        for i0, epsilon, i1, data, weight, original_angle, original_zpix_transl in zip(
            my_i0,
            my_epsilon,
            my_i1,
            radios_subset,
            radios_weights_subset,
            chunk_info.angles_rad[subchunk_slice],
            chunk_info.z_pix_per_proj[subchunk_slice],
        ):
            data_token = data * weight

            if not self.diag_zpro_run:
                self.gridded_radios[i0] += data_token * (1 - epsilon)
                self.gridded_radios[i1] += data_token * epsilon

                self.gridded_weights[i0] += weight * (1 - epsilon)
                self.gridded_weights[i1] += weight * epsilon

        # building the intervals around the diagnostic angles

        if self.diag_zpro_run:
            my_i0 = np.searchsorted(ticks, my_angles_02pi)

            for i0, a02pi, data, weight, original_angle, original_zpix_transl in zip(
                my_i0,
                my_angles_02pi,
                radios_subset,
                radios_weights_subset,
                chunk_info.angles_rad[subchunk_slice],
                chunk_info.z_pix_per_proj[subchunk_slice],
            ):
                if i0 % 2 == 0:
                    # not in an intervals
                    continue

                # There is a contribution to the first regridded radio ( the one indexed by 0)
                # We build  two diagnostics for the contributions to this radio.
                # The first for the first pass (i_diag=0)
                # The second for the second pass if any (i_diag=1)

                # To discriminate we introduce
                # An angular margin beyond which we know that a possible contribution
                # is coming from another turn

                safe_angular_margin = 3.14 / 40

                my_dist = abs(
                    a02pi - self.diagnostic_searched_angles_rad_clipped[(i0 - 1) // 2 : (i0 - 1) // 2 + 1].mean()
                )

                # print(" i0 ", i0, " original_angle ",  original_angle, "  a02pi" , a02pi, " my_dist " , my_dist)

                # consider fist pass and second possible pass. There might be further passes which we dont consider here
                i_diag_list = [(i0 - 1) // 2, (i0 - 1) // 2 + len(self.diagnostic_searched_angles_rad_clipped)]
                for i_redundancy, i_diag in enumerate(i_diag_list):
                    # print("IRED ", i_redundancy)
                    if i_redundancy:  # noqa: SIM102
                        # to avoid, in z_stages with >360 range for one single stage, to fill the second items which should instead be filled by another stage.
                        if abs(original_zpix_transl - self.diagnostic_zpix_transl[i_diag_list[0]]) < 2.0:
                            # print( " >>>>>> stesso z" , i_redundancy )
                            continue

                    if np.isnan(self.diagnostic_angles[i_diag]) or (
                        abs(original_angle) < abs(self.diagnostic_angles[i_diag] + safe_angular_margin)
                    ):
                        # we are searching for the first contributions ( the one at the lowest angle)
                        # for the two diagnostics. With the constraint that the second is at an higher angle
                        # than the first. So if we are here this means that we have found an occurrence with
                        # lower angle and we discard what we could have previously found.

                        self.diagnostic_radios[i_diag][:] = 0
                        self.diagnostic_weights[i_diag][:] = 0
                        self.diagnostic_angles[i_diag] = original_angle

                        self.diagnostic_zpix_transl[i_diag] = original_zpix_transl
                    else:
                        continue

                    if abs(my_dist) <= my_angle_step_rad * 1.1:
                        factor = 1 - abs(my_dist) / (my_angle_step_rad)

                        self.diagnostic_radios[i_diag] += data_token * factor
                        self.diagnostic_weights[i_diag] += weight * factor
                        break
                    else:  # noqa: RET508
                        pass

    class _ReframingInfos:
        def __init__(self, chunk_info, subchunk_slice, subr_start_end, dtasrc_start_end, subchunk_file_indexes):
            self.subchunk_file_indexes = subchunk_file_indexes
            my_integer_shifts_v = chunk_info.integer_shift_v[subchunk_slice]
            self.fract_complement_shifts_v = chunk_info.fract_complement_to_integer_shift_v[subchunk_slice]
            self.x_shifts_list = chunk_info.x_pix_per_proj[subchunk_slice]
            subr_start_z, subr_end_z = subr_start_end
            self.subr_start_z_list = subr_start_z - my_integer_shifts_v
            self.subr_end_z_list = subr_end_z - my_integer_shifts_v + 1

            self.dtasrc_start_z, self.dtasrc_end_z = dtasrc_start_end

            floating_start_z = self.subr_start_z_list.min()
            floating_end_z = self.subr_end_z_list.max()

            self.floating_subregion = None, None, floating_start_z, floating_end_z

    def _extract_preprocess_with_flats(
        self, data_raw, reframing_infos, chunk_info, output, radios_angular_range_slicing=None, it_is_weight=False
    ):
        if not it_is_weight:
            if self.dark is not None:
                data_raw = data_raw - self.dark[reframing_infos.dtasrc_start_z : reframing_infos.dtasrc_end_z]

            if self.flats is not None:
                for i, idx in enumerate(reframing_infos.subchunk_file_indexes):
                    flat = self._get_flat(idx, slice(reframing_infos.dtasrc_start_z, reframing_infos.dtasrc_end_z))
                    if self.dark is not None:
                        flat = flat - self.dark[reframing_infos.dtasrc_start_z : reframing_infos.dtasrc_end_z]

                    if self.radios_srcurrent is not None:
                        factor = self.nominal_current / self.radios_srcurrent[radios_angular_range_slicing.start + i]
                    else:
                        factor = 1

                    data_raw[i] = data_raw[i] * factor / flat

            if self.double_flat is not None:
                data_raw = data_raw / self.double_flat[reframing_infos.dtasrc_start_z : reframing_infos.dtasrc_end_z]

        if it_is_weight:
            # for the weight, the detector weights, depends on the detector portion,
            # the one corresponding to dtasrc_start_end, and is the same across
            # the subchunk first index ( the projection index)
            take_data_from_this = [data_raw] * len(reframing_infos.subr_start_z_list)
        else:
            take_data_from_this = data_raw

        for data_read, list_subr_start_z, list_subr_end_z, fract_shift, x_shift, data_target in zip(
            take_data_from_this,
            reframing_infos.subr_start_z_list,
            reframing_infos.subr_end_z_list,
            reframing_infos.fract_complement_shifts_v,
            reframing_infos.x_shifts_list,
            output,
        ):
            _fill_in_chunk_by_shift_crop_data(
                data_target,
                data_read,
                fract_shift,
                list_subr_start_z,
                list_subr_end_z,
                reframing_infos.dtasrc_start_z,
                reframing_infos.dtasrc_end_z,
                x_shift=x_shift,
                extension_padding=(not it_is_weight),
            )

    def _get_flat(self, idx, slice_y=slice(None, None), slice_x=slice(None, None), dtype=np.float32):
        prev_next = FlatFieldArrays.get_previous_next_indices(self.flat_indexes, idx)

        if len(prev_next) == 1:  # current index corresponds to an acquired flat
            flat_data = self.flats[self.flat_indexes_reverse_map[prev_next[0]]][slice_y, slice_x]
        else:  # interpolate
            prev_idx, next_idx = prev_next

            n_prev = self.flat_indexes_reverse_map[prev_idx]
            n_next = self.flat_indexes_reverse_map[next_idx]

            flat_data_prev = self.flats[n_prev][slice_y, slice_x]
            flat_data_next = self.flats[n_next][slice_y, slice_x]

            if self.flats_srcurrent is not None:
                prev_current_factor = self.nominal_current / self.flats_srcurrent[n_prev]
                next_current_factor = self.nominal_current / self.flats_srcurrent[n_next]
            else:
                prev_current_factor = 1
                next_current_factor = 1

            delta = next_idx - prev_idx
            w1 = 1 - (idx - prev_idx) / delta
            w2 = 1 - (next_idx - idx) / delta

            if self.dark is not None:
                dark = self.dark[slice_y, slice_x]
            else:
                dark = 0

            flat_data = (
                dark
                + w1 * (flat_data_prev - dark) * prev_current_factor
                + w2 * (flat_data_next - dark) * next_current_factor
            )

        if flat_data.dtype != dtype:
            flat_data = np.ascontiguousarray(flat_data, dtype=dtype)
        return flat_data


def _fill_in_chunk_by_shift_crop_data(
    data_target,
    data_read,
    fract_shift,
    my_subr_start_z,
    my_subr_end_z,
    dtasrc_start_z,
    dtasrc_end_z,
    x_shift=0.0,
    extension_padding=True,
):
    data_read_precisely_shifted = nd.shift(data_read, (-fract_shift, x_shift), order=1, mode="nearest")[:-1]

    target_central_slicer, dtasrc_central_slicer = overlap_logic(
        my_subr_start_z, my_subr_end_z - 1, dtasrc_start_z, dtasrc_end_z - 1
    )

    if None not in [target_central_slicer, dtasrc_central_slicer]:
        data_target[target_central_slicer] = data_read_precisely_shifted[dtasrc_central_slicer]

    target_lower_slicer, target_upper_slicer = padding_logic(
        my_subr_start_z, my_subr_end_z - 1, dtasrc_start_z, dtasrc_end_z - 1
    )

    if extension_padding:
        if target_lower_slicer is not None:
            data_target[target_lower_slicer] = data_read_precisely_shifted[0]
        if target_upper_slicer is not None:
            data_target[target_upper_slicer] = data_read_precisely_shifted[-1]
    else:
        if target_lower_slicer is not None:
            data_target[target_lower_slicer] = 1.0e-6
        if target_upper_slicer is not None:
            data_target[target_upper_slicer] = 1.0e-6


def overlap_logic(subr_start_z, subr_end_z, dtasrc_start_z, dtasrc_end_z):
    """determines the useful lines which can be transferred from the dtasrc_start_z:dtasrc_end_z
    range targeting the range  subr_start_z: subr_end_z ..................

    """

    t_h = subr_end_z - subr_start_z
    s_h = dtasrc_end_z - dtasrc_start_z

    my_start = max(0, dtasrc_start_z - subr_start_z)
    my_end = min(t_h, dtasrc_end_z - subr_start_z)

    if my_start >= my_end:
        return None, None

    target_central_slicer = slice(my_start, my_end)

    my_start = max(0, subr_start_z - dtasrc_start_z)
    my_end = min(s_h, subr_end_z - dtasrc_start_z)

    assert my_start < my_end, "Overlap_logic logic error"

    dtasrc_central_slicer = slice(my_start, my_end)

    return target_central_slicer, dtasrc_central_slicer


def padding_logic(subr_start_z, subr_end_z, dtasrc_start_z, dtasrc_end_z):
    """.......... and the missing ranges which possibly could be obtained by extension padding"""
    # t_h = subr_end_z - subr_start_z
    # s_h = dtasrc_end_z - dtasrc_start_z

    if dtasrc_start_z <= subr_start_z:
        target_lower_padding = None
    else:
        target_lower_padding = slice(0, dtasrc_start_z - subr_start_z)

    if dtasrc_end_z >= subr_end_z:
        target_upper_padding = None
    else:
        target_upper_padding = slice(dtasrc_end_z - subr_end_z, None)

    return target_lower_padding, target_upper_padding


def get_reconstruction_space(span_info, min_scanwise_z, end_scanwise_z, phase_margin_pix):
    """Utility function, so far used only by the unit test, which, given the span_info object, creates the auxiliary collection arrays
    and initialises the my_z_min, my_z_end variable taking into account the scan direction
    and the min_scanwise_z, end_scanwise_z input arguments

    Parameters
    ----------
    span_info: SpanStrategy

    min_scanwise_z: int
          non negative number, where zero indicates the first feasible slice doable scanwise.
          Indicates the first (scanwise) requested slice to be reconstructed

    end_scanwise_z: int
          non negative number, where zero indicates the first feasible slice doable scanwise.
          Indicates the end (scanwise) slice which delimits the to be reconstructed requested slab.

    """

    detector_z_start, detector_z_end = (span_info.get_doable_span()).view_heights_minmax

    if span_info.z_pix_per_proj[-1] > span_info.z_pix_per_proj[0]:
        my_z_min = detector_z_start + min_scanwise_z
        my_z_end = detector_z_start + end_scanwise_z
    else:
        my_z_min = detector_z_end - (end_scanwise_z - 1)
        my_z_end = detector_z_end - (min_scanwise_z + 1)

    # while the raw dataset may have non uniform angular step
    # the regridded dataset will have a constant step.
    # We evaluate here below the number of angles for the
    # regridded dataset, estimating a meaningul angular step representative
    # of the raw data
    my_angle_step = abs(np.diff(span_info.projection_angles_deg).mean())
    n_gridded_angles = round(360.0 / my_angle_step)

    radios_h = phase_margin_pix + (my_z_end - my_z_min) + phase_margin_pix

    # the accumulators
    gridded_radios = np.zeros([n_gridded_angles, radios_h, span_info.detector_shape_vh[1]], np.float32)
    gridded_cumulated_weights = np.zeros([n_gridded_angles, radios_h, span_info.detector_shape_vh[1]], np.float32)

    # this utility function is meant for testing the reconstruction only, not the diagnostic collection.
    # However we build diagnostic targets all the same to feed something through the API
    # which contemplates the diagnostics. So that the unit test runs correctly

    diagnostic_radios = np.zeros((4,) + gridded_radios.shape[1:], np.float32)
    diagnostic_weights = np.zeros((4,) + gridded_radios.shape[1:], np.float32)
    diagnostic_proj_angle = np.zeros([4], "f")

    diagnostic_searched_angles_rad_clipped = (0.5 + np.arange(2)) * (2 * np.pi / (2))
    diagnostic_zpix_transl = np.zeros([4], "f")

    gridded_angles_rad = np.arange(n_gridded_angles) * 2 * np.pi / n_gridded_angles
    gridded_angles_deg = np.rad2deg(gridded_angles_rad)

    res = type(
        "on_the_fly_class_for_reconstruction_room_in_gridded_accumulator.py",
        (object,),
        {
            "my_z_min": my_z_min,
            "my_z_end": my_z_end,
            "gridded_radios": gridded_radios,
            "gridded_cumulated_weights": gridded_cumulated_weights,
            "diagnostic_radios": diagnostic_radios,
            "diagnostic_weights": diagnostic_weights,
            "diagnostic_proj_angle": diagnostic_proj_angle,
            "diagnostic_searched_angles_rad_clipped": diagnostic_searched_angles_rad_clipped,
            "diagnostic_zpix_transl": diagnostic_zpix_transl,
            "gridded_angles_rad": gridded_angles_rad,
            "gridded_angles_deg": gridded_angles_deg,
        },
    )
    return res
