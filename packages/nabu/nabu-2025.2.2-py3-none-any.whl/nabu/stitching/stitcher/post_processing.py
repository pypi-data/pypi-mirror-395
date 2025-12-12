import logging
import numpy
import os
import h5py
import pint
from nabu.stitching.config import PostProcessedSingleAxisStitchingConfiguration
from nabu.stitching.alignment import AlignmentAxis1
from nabu.stitching.alignment import PaddedRawData
from math import ceil
from tomoscan.io import HDF5File
from tomoscan.esrf.scan.utils import cwd_context
from tomoscan.esrf import NXtomoScan
from tomoscan.series import Series
from tomoscan.volumebase import VolumeBase
from tomoscan.esrf.volume import HDF5Volume
from collections.abc import Iterable
from contextlib import AbstractContextManager
from nabu.stitching.config import (
    KEY_IMG_REG_METHOD,
)
from nabu.stitching.utils.utils import find_volumes_relative_shifts
from nabu.io.utils import DatasetReader
from .single_axis import SingleAxisStitcher

_logger = logging.getLogger(__name__)

_ureg = pint.get_application_registry()


class FlippingValueError(ValueError):
    pass


class PostProcessingStitching(SingleAxisStitcher):
    """
    Loader to be used when load data during post-processing stitching (on recosntructed volume). Output is expected to be an NXtomo
    """

    def __init__(self, configuration, progress=None) -> None:
        if not isinstance(configuration, PostProcessedSingleAxisStitchingConfiguration):
            raise TypeError(
                f"configuration is expected to be an instance of {PostProcessedSingleAxisStitchingConfiguration}. Get {type(configuration)} instead"
            )
        self._input_volumes = configuration.input_volumes
        self.__output_data_type = None

        self._series = Series("series", iterable=self._input_volumes, use_identifiers=False)

        super().__init__(configuration, progress=progress)

    @property
    def stitching_axis_in_frame_space(self):
        if self.axis == 0:
            return 0
        elif self.axis in (1, 2):
            raise NotImplementedError(f"post-processing stitching along axis {self.axis} is not handled.")
        else:
            raise NotImplementedError(f"stitching axis must be in (0, 1, 2). Get {self.axis}")

    def settle_flips(self):
        super().settle_flips()
        if not self.configuration.duplicate_data:
            if len(numpy.unique(self.configuration.flip_lr)) > 1:
                raise FlippingValueError(
                    "Stitching without data duplication cannot handle volume with different flip. Please run the stitching with data duplication"
                )
            if True in self.configuration.flip_ud:
                raise FlippingValueError(
                    "Stitching without data duplication cannot handle with up / down flips. Please run the stitching with data duplication"
                )

    def order_input_tomo_objects(self):

        def get_min_bound(volume):
            try:
                bb = volume.get_bounding_box(axis=self.axis)
            except ValueError:  #  if missing information
                bb = None
            if bb is not None:
                return bb.min
            else:
                # if can't find bounding box (missing metadata to the volume
                # try to get it from the scan
                metadata = volume.metadata or volume.load_metadata()
                scan_location = metadata.get("nabu_config", {}).get("dataset", {}).get("location", None)
                scan_entry = metadata.get("nabu_config", {}).get("dataset", {}).get("hdf5_entry", None)
                if scan_location is not None:
                    # this work around (until most volume have position metadata) works only for Hdf5volume
                    with cwd_context(os.path.dirname(volume.file_path)):
                        o_scan = NXtomoScan(scan_location, scan_entry)
                        bb_acqui = o_scan.get_bounding_box(axis=None)
                        # for next step volume position will be required.
                        # if you can find it set it directly
                        volume.position = (numpy.array(bb_acqui.max) - numpy.array(bb_acqui.min)) / 2.0 + numpy.array(
                            bb_acqui.min
                        )
                        # for now translation are stored in pixel size ref instead of real_pixel_size
                        volume.pixel_size = o_scan.x_real_pixel_size
                        if bb_acqui is not None:
                            return bb_acqui.min[0]
                raise ValueError("Unable to find volume position. Unable to deduce z position")

        try:
            # order volumes from higher z to lower z
            # if axis 0 position is provided then use directly it
            if self.configuration.axis_0_pos_px is not None and len(self.configuration.axis_0_pos_px) > 0:
                order = numpy.argsort(self.configuration.axis_0_pos_px)
                sorted_series = Series(
                    self.series.name,
                    numpy.take_along_axis(numpy.array(self.series[:]), order, axis=0)[::-1],
                    use_identifiers=False,
                )
            else:
                # else use bounding box
                sorted_series = Series(
                    self.series.name,
                    sorted(self.series[:], key=get_min_bound, reverse=True),
                    use_identifiers=False,
                )
        except ValueError:
            _logger.warning(
                "Unable to find volume positions in metadata. Expect the volume to be ordered already (decreasing along axis 0.)"
            )
        else:
            if sorted_series == self.series:
                pass
            elif sorted_series != self.series:
                if sorted_series[:] != self.series[::-1]:
                    raise ValueError(
                        "Unable to get comprehensive input. ordering along axis 0 is not respected (decreasing)."
                    )
                else:
                    _logger.warning(
                        f"decreasing order haven't been respected. Need to reorder {self.serie_label} ({[str(scan) for scan in sorted_series[:]]}). Will also reorder positions"
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
        # check input volume
        if self.configuration.output_volume is None:
            raise ValueError("input volume should be provided")

        n_volumes = len(self.series)
        if n_volumes == 0:
            raise ValueError("no scan to stich together")

        if not isinstance(self.configuration.output_volume, VolumeBase):
            raise TypeError(f"make sure we return a volume identifier not {(type(self.configuration.output_volume))}")

        # check axis 0 position
        if isinstance(self.configuration.axis_0_pos_px, Iterable) and len(self.configuration.axis_0_pos_px) != (
            n_volumes
        ):
            raise ValueError(f"expect {n_volumes} overlap defined. Get {len(self.configuration.axis_0_pos_px)}")
        if isinstance(self.configuration.axis_0_pos_mm, Iterable) and len(self.configuration.axis_0_pos_mm) != (
            n_volumes
        ):
            raise ValueError(f"expect {n_volumes} overlap defined. Get {len(self.configuration.axis_0_pos_mm)}")

        # check axis 1 position
        if isinstance(self.configuration.axis_1_pos_px, Iterable) and len(self.configuration.axis_1_pos_px) != (
            n_volumes
        ):
            raise ValueError(f"expect {n_volumes} overlap defined. Get {len(self.configuration.axis_1_pos_px)}")
        if isinstance(self.configuration.axis_1_pos_mm, Iterable) and len(self.configuration.axis_1_pos_mm) != (
            n_volumes
        ):
            raise ValueError(f"expect {n_volumes} overlap defined. Get {len(self.configuration.axis_1_pos_mm)}")

        # check axis 2 position
        if isinstance(self.configuration.axis_1_pos_px, Iterable) and len(self.configuration.axis_1_pos_px) != (
            n_volumes
        ):
            raise ValueError(f"expect {n_volumes} overlap defined. Get {len(self.configuration.axis_1_pos_px)}")
        if isinstance(self.configuration.axis_2_pos_mm, Iterable) and len(self.configuration.axis_2_pos_mm) != (
            n_volumes
        ):
            raise ValueError(f"expect {n_volumes} overlap defined. Get {len(self.configuration.axis_2_pos_mm)}")

        self._reading_orders = []
        # the first scan will define the expected reading orderd, and expected flip.
        # if all scan are flipped then we will keep it this way
        self._reading_orders.append(1)

    @staticmethod
    def _get_bunch_of_data(
        bunch_start: int,
        bunch_end: int,
        step: int,
        volumes: tuple,
        flip_lr_arr: bool,
        flip_ud_arr: bool,
    ):
        """
        goal is to load contiguous frames as much as possible...
        return for each volume the bunch of slice along axis 1
        warning: they can have different shapes
        """

        def get_sub_volume(volume, flip_lr, flip_ud):
            sub_volume = volume[:, bunch_start:bunch_end:step, :]
            if flip_lr:
                sub_volume = numpy.fliplr(sub_volume)
            if flip_ud:
                sub_volume = numpy.flipud(sub_volume)
            return sub_volume

        sub_volumes = [
            get_sub_volume(volume, flip_lr, flip_ud)
            for volume, flip_lr, flip_ud in zip(volumes, flip_lr_arr, flip_ud_arr)
        ]
        # generator on it self: we want to iterate over the y axis
        n_slices_in_bunch = ceil((bunch_end - bunch_start) / step)
        assert isinstance(n_slices_in_bunch, int)
        for i in range(n_slices_in_bunch):
            yield [sub_volume[:, i, :] for sub_volume in sub_volumes]

    def compute_estimated_shifts(self):
        axis_0_pos_px = self.configuration.axis_0_pos_px
        self._axis_0_rel_ini_shifts = []
        # compute overlap along axis 0
        for upper_volume, lower_volume, upper_volume_axis_0_pos, lower_volume_axis_0_pos in zip(
            self.series[:-1], self.series[1:], axis_0_pos_px[:-1], axis_0_pos_px[1:]
        ):
            upper_volume_low_pos = upper_volume_axis_0_pos - upper_volume.get_volume_shape()[0] / 2
            lower_volume_high_pos = lower_volume_axis_0_pos + lower_volume.get_volume_shape()[0] / 2
            self._axis_0_rel_ini_shifts.append(
                int(lower_volume_high_pos - upper_volume_low_pos)  # overlap are expected to be int for now
            )
        self._axis_1_rel_ini_shifts = self.from_abs_pos_to_rel_pos(self.configuration.axis_1_pos_px)
        self._axis_2_rel_ini_shifts = [0.0] * (len(self.series) - 1)

    def _compute_positions_as_px(self):
        """compute if necessary position other axis 0 from volume metadata"""

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
                for volume, pos_in_mm in zip(self.series, pos_as_mm):
                    voxel_size_m = self.configuration.voxel_size or volume.voxel_size
                    axis_N_pos_px.append((pos_in_mm * _ureg.millimeter).to_base_units().magnitude / voxel_size_m[0])
                return axis_N_pos_px
            else:
                # deduce from motor position and pixel size
                axis_N_pos_px = []
                base_position_m = self.series[0].get_bounding_box(axis=axis).min
                for volume in self.series:
                    voxel_size_m = self.configuration.voxel_size or volume.voxel_size
                    volume_axis_bb = volume.get_bounding_box(axis=axis)
                    axis_N_mean_pos_m = (volume_axis_bb.max - volume_axis_bb.min) / 2 + volume_axis_bb.min
                    axis_N_mean_rel_pos_m = axis_N_mean_pos_m - base_position_m
                    axis_N_pos_px.append(int(axis_N_mean_rel_pos_m / voxel_size_m[0]))
                return axis_N_pos_px

        self.configuration.axis_0_pos_px = get_position_as_px_on_axis(
            axis=0,
            pos_as_px=self.configuration.axis_0_pos_px,
            pos_as_mm=self.configuration.axis_0_pos_mm,
        )
        self.configuration.axis_0_pos_mm = None

        self.configuration.axis_1_pos_px = get_position_as_px_on_axis(
            axis=1,
            pos_as_px=self.configuration.axis_1_pos_px,
            pos_as_mm=self.configuration.axis_1_pos_mm,
        )

        self.configuration.axis_2_pos_px = get_position_as_px_on_axis(
            axis=2,
            pos_as_px=self.configuration.axis_2_pos_px,
            pos_as_mm=self.configuration.axis_2_pos_mm,
        )
        self.configuration.axis_2_pos_mm = None

    def _compute_shifts(self):
        n_volumes = len(self.configuration.input_volumes)
        if n_volumes == 0:
            raise ValueError("no scan to stich provided")

        slice_for_shift = self.configuration.slice_for_cross_correlation or "middle"
        y_rel_shifts = self._axis_0_rel_ini_shifts
        x_rel_shifts = self._axis_1_rel_ini_shifts
        dim_axis_1 = max([volume.get_volume_shape()[1] for volume in self.series])

        final_rel_shifts = []
        for (
            upper_volume,
            lower_volume,
            x_rel_shift,
            y_rel_shift,
            flip_ud_upper,
            flip_ud_lower,
        ) in zip(
            self.series[:-1],
            self.series[1:],
            x_rel_shifts,
            y_rel_shifts,
            self.configuration.flip_ud[:-1],
            self.configuration.flip_ud[1:],
        ):
            x_cross_algo = self.configuration.axis_2_params.get(KEY_IMG_REG_METHOD, None)
            y_cross_algo = self.configuration.axis_0_params.get(KEY_IMG_REG_METHOD, None)

            # compute relative shift
            found_shift_y, found_shift_x = find_volumes_relative_shifts(
                upper_volume=upper_volume,
                lower_volume=lower_volume,
                dtype=self.get_output_data_type(),
                dim_axis_1=dim_axis_1,
                slice_for_shift=slice_for_shift,
                x_cross_correlation_function=x_cross_algo,
                y_cross_correlation_function=y_cross_algo,
                x_shifts_params=self.configuration.axis_2_params,
                y_shifts_params=self.configuration.axis_0_params,
                estimated_shifts=(y_rel_shift, x_rel_shift),
                flip_ud_lower_frame=flip_ud_lower,
                flip_ud_upper_frame=flip_ud_upper,
                alignment_axis_1=self.configuration.alignment_axis_1,
                alignment_axis_2=self.configuration.alignment_axis_2,
                overlap_axis=self.axis,
            )
            final_rel_shifts.append(
                (found_shift_y, found_shift_x),
            )

        # set back values. Now position should start at 0
        self._axis_0_rel_final_shifts = [final_shift[0] for final_shift in final_rel_shifts]
        self._axis_1_rel_final_shifts = [final_shift[1] for final_shift in final_rel_shifts]
        self._axis_2_rel_final_shifts = [0.0] * len(final_rel_shifts)
        _logger.info(f"axis 2 relative shifts (x in radio ref) to be used will be {self._axis_1_rel_final_shifts}")
        print(f"axis 2 relative shifts (x in radio ref) to be used will be {self._axis_1_rel_final_shifts}")
        _logger.info(f"axis 0 relative shifts (y in radio ref) y to be used will be {self._axis_0_rel_final_shifts}")
        print(f"axis 0 relative shifts (y in radio ref) y to be used will be {self._axis_0_rel_final_shifts}")

    def get_output_data_type(self):
        if self.__output_data_type is None:

            def find_output_data_type():
                first_vol = self._input_volumes[0]
                if first_vol.data is not None:
                    return first_vol.data.dtype
                elif isinstance(first_vol, HDF5Volume):
                    with DatasetReader(first_vol.data_url) as vol_dataset:
                        return vol_dataset.dtype
                else:
                    return first_vol.load_data(store=False).dtype

            self.__output_data_type = find_output_data_type()
        return self.__output_data_type

    def _create_stitched_volume(self, store_composition: bool):
        overlap_kernels = self._overlap_kernels
        self._slices_to_stitch, n_slices = self.configuration.settle_slices()

        # sync overwrite_results with volume overwrite parameter
        self.configuration.output_volume.overwrite = self.configuration.overwrite_results

        # init final volume
        final_volume = self.configuration.output_volume
        final_volume_shape = (
            int(
                numpy.asarray([volume.get_volume_shape()[0] for volume in self._input_volumes]).sum()
                - numpy.asarray([abs(overlap) for overlap in self._axis_0_rel_final_shifts]).sum(),
            ),
            n_slices,
            self._stitching_constant_length,
        )

        data_type = self.get_output_data_type()

        if self.progress is not None:
            self.progress.total = final_volume_shape[1]

        y_index = 0
        if isinstance(self._slices_to_stitch, slice):
            step = self._slices_to_stitch.step or 1
        else:
            step = 1

        output_dataset_args = {
            "volume": final_volume,
            "volume_shape": final_volume_shape,
            "dtype": data_type,
            "dumper": self.dumper,
        }
        from .dumper.postprocessing import PostProcessingStitchingDumperNoDD, PostProcessingStitchingDumperWithCache

        # TODO: FIXME: for now not very elegant but in the case of avoiding data duplication
        # we need to provide the the information about the stitched part shape.
        # this should be move to the dumper in the future
        if isinstance(self.dumper, PostProcessingStitchingDumperNoDD):
            output_dataset_args["stitching_sources_arr_shapes"] = tuple(
                [(abs(overlap), n_slices, self._stitching_constant_length) for overlap in self._axis_0_rel_final_shifts]
            )
        elif isinstance(self.dumper, PostProcessingStitchingDumperWithCache):
            self.dumper.set_final_volume_shape(final_volume_shape)

        bunch_size = 50
        # how many frame to we stitch between two read from disk / save to disk
        with self.dumper.OutputDatasetContext(**output_dataset_args):  # noqa: SIM117
            # note: output_dataset is a HDF5 dataset if final volume is an HDF5 volume else is a numpy array
            with _RawDatasetsContext(
                self._input_volumes,
                alignment_axis_1=self.configuration.alignment_axis_1,
            ) as raw_datasets:
                # note: raw_datasets can be numpy arrays or HDF5 dataset (in the case of HDF5Volume)
                # to speed up we read by bunch of dataset. For numpy array this doesn't change anything
                # but for HDF5 dataset this can speed up a lot the processing (depending on HDF5 dataset chuncks)
                # note: we read through axis 1
                if isinstance(self.dumper, PostProcessingStitchingDumperNoDD):
                    self.dumper.raw_regions_hdf5_dataset = raw_datasets
                if isinstance(self.dumper, PostProcessingStitchingDumperWithCache):
                    self.dumper.init_cache(dump_axis=1, dtype=data_type, size=bunch_size)

                for bunch_start, bunch_end in PostProcessingStitching._data_bunch_iterator(
                    slices=self._slices_to_stitch, bunch_size=bunch_size
                ):
                    for data_frames in PostProcessingStitching._get_bunch_of_data(
                        bunch_start,
                        bunch_end,
                        step=step,
                        volumes=raw_datasets,
                        flip_lr_arr=self.configuration.flip_lr,
                        flip_ud_arr=self.configuration.flip_ud,
                    ):
                        if self.configuration.rescale_frames:
                            data_frames = self.rescale_frames(data_frames)
                        if self.configuration.normalization_by_sample.is_active():
                            data_frames = self.normalize_frame_by_sample(data_frames)

                        sf = PostProcessingStitching.stitch_frames(
                            frames=data_frames,
                            axis=self.axis,
                            output_dtype=data_type,
                            x_relative_shifts=self._axis_1_rel_final_shifts,
                            y_relative_shifts=self._axis_0_rel_final_shifts,
                            overlap_kernels=overlap_kernels,
                            dumper=self.dumper,
                            i_frame=y_index,
                            return_composition_cls=store_composition if y_index == 0 else False,
                            stitching_axis=self.axis,
                            check_inputs=y_index == 0,  # on process check on the first iteration
                        )
                        if y_index == 0 and store_composition:
                            _, self._frame_composition = sf

                        if self.progress is not None:
                            self.progress.update()
                        y_index += 1

                    if isinstance(self.dumper, PostProcessingStitchingDumperWithCache):
                        self.dumper.dump_cache(nb_frames=(bunch_end - bunch_start))

    # alias to general API
    def _create_stitching(self, store_composition):
        self._create_stitched_volume(store_composition=store_composition)


class _RawDatasetsContext(AbstractContextManager):
    """
    return volume data for all input volume (target: used for volume stitching).
    If the volume is an HDF5Volume then the HDF5 dataset will be used (on disk)
    If the volume is of another type then it will be loaded in memory then used (more memory consuming)
    """

    def __init__(self, volumes: tuple, alignment_axis_1) -> None:
        super().__init__()
        for volume in volumes:
            if not isinstance(volume, VolumeBase):
                raise TypeError(
                    f"Volumes are expected to be an instance of {VolumeBase}. {type(volume)} provided instead"
                )

        self._volumes = volumes
        self.__file_handlers = []
        self._alignment_axis_1 = alignment_axis_1

    @property
    def alignment_axis_1(self):
        return self._alignment_axis_1

    def __enter__(self):
        # handle the specific case of HDF5. Goal: avoid getting the full stitched volume in memory
        datasets = []
        shapes = {volume.get_volume_shape()[1] for volume in self._volumes}
        axis_1_dim = max(shapes)
        axis_1_need_padding = len(shapes) > 1

        try:
            for volume in self._volumes:
                if volume.data is not None:
                    data = volume.data
                elif isinstance(volume, HDF5Volume):
                    file_handler = HDF5File(volume.data_url.file_path(), mode="r")
                    dataset = file_handler[volume.data_url.data_path()]
                    data = dataset
                    self.__file_handlers.append(file_handler)
                # for other file format: load the full dataset in memory
                else:
                    data = volume.load_data(store=False)
                    if data is None:
                        # TODO
                        raise ValueError(f"No data found for volume {volume.get_identifier()}")  # noqa: TRY301
                if axis_1_need_padding:
                    data = self.add_padding(data=data, axis_1_dim=axis_1_dim, alignment=self.alignment_axis_1)
                datasets.append(data)
        except Exception as e:
            # if some errors happen during loading HDF5
            for file_handled in self.__file_handlers:
                file_handled.close()
            raise e  # noqa: TRY201

        return datasets

    def __exit__(self, exc_type, exc_value, traceback):
        success = True
        for file_handler in self.__file_handlers:
            success = success and file_handler.close()
        if exc_type is None:
            return success
        return None

    def add_padding(self, data: h5py.Dataset | numpy.ndarray, axis_1_dim: int, alignment: AlignmentAxis1):
        alignment = AlignmentAxis1(alignment)
        if alignment is AlignmentAxis1.BACK:
            axis_1_pad_width = (axis_1_dim - data.shape[1], 0)
        elif alignment is AlignmentAxis1.CENTER:
            half_width = int((axis_1_dim - data.shape[1]) / 2)
            axis_1_pad_width = (half_width, axis_1_dim - data.shape[1] - half_width)
        elif alignment is AlignmentAxis1.FRONT:
            axis_1_pad_width = (0, axis_1_dim - data.shape[1])
        else:
            raise ValueError(f"alignment {alignment} is not handled")

        return PaddedRawData(
            data=data,
            axis_1_pad_width=axis_1_pad_width,
        )
