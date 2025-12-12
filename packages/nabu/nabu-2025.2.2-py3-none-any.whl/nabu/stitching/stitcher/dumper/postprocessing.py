import h5py
import numpy
import logging
from .base import DumperBase
from nabu.stitching.config import PostProcessedSingleAxisStitchingConfiguration
from nabu import version as nabu_version
from nabu.io.writer import get_datetime
from tomoscan.identifier import VolumeIdentifier
from tomoscan.volumebase import VolumeBase
from tomoscan.esrf.volume import HDF5Volume
from tomoscan.io import HDF5File
from contextlib import AbstractContextManager


_logger = logging.getLogger(__name__)


class OutputVolumeContext(AbstractContextManager):
    """
    Utils class to Manage the data volume creation and save it (data only !). target: used for volume stitching
    In the case of HDF5 we want to save this directly in the file to avoid
    keeping the full volume in memory.
    Insure also contain processing will be common between the different processing

    If stitching_sources_arr_shapes is provided this mean that we want to create stitching region and then create a VDS to avoid data duplication
    """

    def __init__(
        self,
        volume: VolumeBase,
        volume_shape: tuple,
        dtype: numpy.dtype,
        dumper,
    ) -> None:
        super().__init__()
        if not isinstance(volume, VolumeBase):
            raise TypeError(f"Volume is expected to be an instance of {VolumeBase}. {type(volume)} provided instead")

        self._volume = volume
        self._volume_shape = volume_shape
        self.__file_handler = None
        self._dtype = dtype
        self._dumper = dumper

    @property
    def _file_handler(self):
        return self.__file_handler

    def _build_hdf5_output(self):
        return self._file_handler.create_dataset(
            self._volume.data_url.data_path(),
            shape=self._volume_shape,
            dtype=self._dtype,
        )

    def _create_stitched_volume_dataset(self):
        # handle the specific case of HDF5. Goal: avoid getting the full stitched volume in memory
        if isinstance(self._volume, HDF5Volume):
            self.__file_handler = HDF5File(self._volume.data_url.file_path(), mode="a")
            # if need to delete an existing dataset
            if self._volume.overwrite and self._volume.data_path in self._file_handler:
                try:
                    del self._file_handler[self._volume.data_path]
                except Exception as e:
                    _logger.error(f"Fail to overwrite data. Reason is {e}")
                    data = None
                    self._file_handler.close()
                    self._duplicate_data = True
                    # avoid creating a dataset for stitched volume as creation of the stitched_volume failed
                    return data

            # create dataset
            try:
                data = self._build_hdf5_output()
            except Exception as e2:
                _logger.error(f"Fail to create final dataset. Reason is {e2}")
                data = None
                self._file_handler.close()
                self._duplicate_data = True
                # avoid creating a dataset for stitched volume as creation of the stitched_volume failed
        else:
            raise TypeError("only HDF5 output is handled")
        # else:
        #     # for other file format: create the full dataset in memory before dumping it
        #     data = numpy.empty(self._volume_shape, dtype=self._dtype)
        #     self._volume.data = data
        return data

    def __enter__(self):
        assert self._dumper.output_dataset is None
        self._dumper.output_dataset = self._create_stitched_volume_dataset()
        return self._dumper.output_dataset

    def __exit__(self, exc_type, exc_value, traceback):
        if self._file_handler is not None:
            return self._file_handler.close()
        self._volume.save_data()
        return None


class OutputVolumeNoDDContext(OutputVolumeContext):
    """
    Dedicated output volume context for saving a volume without Data Duplication (DD)
    """

    def __init__(
        self,
        volume: VolumeBase,
        volume_shape: tuple,
        dtype: numpy.dtype,
        dumper,
        stitching_sources_arr_shapes: tuple | None,
    ) -> None:
        if not isinstance(dumper, PostProcessingStitchingDumperNoDD):
            raise TypeError
        # TODO: compute volume_shape from here
        self._stitching_sources_arr_shapes = stitching_sources_arr_shapes

        super().__init__(volume, volume_shape, dtype, dumper)

    def __enter__(self):
        dataset = super().__enter__()
        assert isinstance(self._dumper, PostProcessingStitchingDumperNoDD)
        self._dumper.stitching_regions_hdf5_dataset = self._create_stitched_sub_region_datasets()
        return dataset

    def _build_hdf5_output(self):
        return h5py.VirtualLayout(
            shape=self._volume_shape,
            dtype=self._dtype,
        )

    def __exit__(self, exc_type, exc_value, traceback):
        # in the case of no data duplication we need to create the virtual dataset at the end
        if not isinstance(self._dumper.output_dataset, h5py.VirtualLayout):
            raise TypeError("dumper output_dataset should be a virtual layout")
        self._file_handler.create_virtual_dataset(self._volume.data_url.data_path(), layout=self._dumper.output_dataset)
        super().__exit__(exc_type=exc_type, exc_value=exc_value, traceback=traceback)

    def _create_stitched_sub_region_datasets(self):
        # create datasets to store overlaps if needed
        if not isinstance(self._volume, HDF5Volume):
            raise TypeError("Avoid Data Duplication is only available for HDF5 output volume")

        stitching_regions_hdf5_dataset = []
        for i_region, overlap_shape in enumerate(self._stitching_sources_arr_shapes):
            data_path = f"{self._volume.data_path}/stitching_regions/region_{i_region}"
            if self._volume.overwrite and data_path in self._file_handler:
                del self._file_handler[data_path]
            stitching_regions_hdf5_dataset.append(
                self._file_handler.create_dataset(
                    name=data_path,
                    shape=overlap_shape,
                    dtype=self._dtype,
                )
            )
        self._dumper.stitching_regions_hdf5_dataset = stitching_regions_hdf5_dataset
        return stitching_regions_hdf5_dataset


class PostProcessingStitchingDumper(DumperBase):
    """
    dumper to be used when save data during post-processing stitching (on reconstructed volume). Output is expected to be an NXtomo
    """

    OutputDatasetContext = OutputVolumeContext

    def __init__(self, configuration) -> None:
        if not isinstance(configuration, PostProcessedSingleAxisStitchingConfiguration):
            raise TypeError(
                f"configuration is expected to be an instance of {PostProcessedSingleAxisStitchingConfiguration}. Get {type(configuration)} instead"
            )
        super().__init__(configuration)
        self._output_dataset = None
        self._input_volumes = configuration.input_volumes

    def save_configuration(self):
        voxel_size = self._input_volumes[0].voxel_size

        def get_position():
            # the z-serie is z-ordered from higher to lower. We can reuse this with pixel size and shape to
            # compute the position of the stitched volume
            if voxel_size is None:
                return None
            return numpy.array(self._input_volumes[0].position) + voxel_size * (
                numpy.array(self._input_volumes[0].get_volume_shape()) / 2.0
                - numpy.array(self.configuration.output_volume.get_volume_shape()) / 2.0
            )

        self.configuration.output_volume.voxel_size = voxel_size or ""
        try:
            self.configuration.output_volume.position = get_position()
        except Exception:
            self.configuration.output_volume.position = numpy.array([0, 0, 0])

        self.configuration.output_volume.metadata.update(
            {
                "about": {
                    "program": "nabu-stitching",
                    "version": nabu_version,
                    "date": get_datetime(),
                },
                "configuration": self.configuration.to_dict(),
            }
        )
        self.configuration.output_volume.save_metadata()

    @property
    def output_identifier(self) -> VolumeIdentifier:
        return self.configuration.output_volume.get_identifier()

    def create_output_dataset(self):
        """
        function called at the beginning of the stitching to prepare output dataset
        """
        self._dataset = h5py.VirtualLayout(
            shape=self._volume_shape,
            dtype=self._dtype,
        )


class PostProcessingStitchingDumperWithCache(PostProcessingStitchingDumper):
    """
    PostProcessingStitchingDumper with intermediate cache in order to speed up writting.
    The cache is save to disk when full or when closing the dumper.
    Mostly convenient for HDF5
    """

    def __init__(self, configuration):
        super().__init__(configuration)
        self.__cache = None
        """cache as a numpy.ndarray"""
        self.__cache_size = None
        """how many frame do we want to keep in memory before dumping to disk"""
        self.__dump_axis = None
        """axis along which we load / save the data. Different of the stitching axis"""
        self.__final_volume_shape = None
        self.__output_frame_index = 0
        self.__cache_index = 0

    def init_cache(self, dump_axis, size, dtype):
        if dump_axis not in (0, 1, 2):
            raise ValueError(f"axis should be in (0, 1, 2). Got {dump_axis}")

        self.__dump_axis = dump_axis
        self.__cache_size = size
        self.__cache = numpy.empty(
            self._get_cache_shape(),
            dtype=dtype,
        )

    def reset_cache(self):
        self.__cache_index = 0

    def set_final_volume_shape(self, shape):
        self.__final_volume_shape = shape

    def _get_cache_shape(self):
        assert self.__final_volume_shape is not None, "final volume shape should already be defined"
        if self.__dump_axis == 0:
            return (
                self.__cache_size,
                self.__final_volume_shape[1],
                self.__final_volume_shape[2],
            )
        elif self.__dump_axis == 1:
            return (
                self.__final_volume_shape[0],
                self.__cache_size,
                self.__final_volume_shape[2],
            )
        elif self.__dump_axis == 2:
            return (
                self.__final_volume_shape[0],
                self.__final_volume_shape[1],
                self.__cache_size,
            )
        else:
            raise RuntimeError("dump axis should be defined before using the cache")

    def save_stitched_frame(
        self,
        stitched_frame: numpy.ndarray,
        composition_cls: dict,
        i_frame: int,
        axis: int,
    ):
        """save the frame to the volume. In this use case save the frame to the buffer. Waiting to be dump later.
        We expect 'save_stitched_frame' to be called with contiguous frames (in the output volume space)
        """
        index_cache = self.__cache_index
        if self.__dump_axis == 0:
            self.__cache[index_cache,] = stitched_frame
        elif self.__dump_axis == 1:
            self.__cache[:, index_cache, :] = stitched_frame
        elif self.__dump_axis == 2:
            self.__cache[:, :, index_cache] = stitched_frame
        else:
            raise RuntimeError("dump axis should be defined before using the cache")
        self.__cache_index += 1

    def dump_cache(self, nb_frames):
        """
        dump the first nb_frames to disk
        """
        output_dataset_start_index = self.__output_frame_index
        output_dataset_end_index = self.__output_frame_index + nb_frames
        if self.__dump_axis == 0:
            self.output_dataset[output_dataset_start_index:output_dataset_end_index] = self.__cache[:nb_frames]
        elif self.__dump_axis == 1:
            self.output_dataset[
                :,
                output_dataset_start_index:output_dataset_end_index,
            ] = self.__cache[:, :nb_frames]
        elif self.__dump_axis == 2:
            self.output_dataset[:, :, output_dataset_start_index:output_dataset_end_index] = self.__cache[
                :, :, :nb_frames
            ]
        else:
            raise RuntimeError("dump axis should be defined before using the cache")

        self.__output_frame_index = output_dataset_end_index
        self.reset_cache()


class PostProcessingStitchingDumperNoDD(PostProcessingStitchingDumper):
    """
    same as PostProcessingStitchingDumper but prevent to do data duplication.
    In this case we need to work on HDF5 file only
    """

    OutputDatasetContext = OutputVolumeNoDDContext

    def __init__(self, configuration) -> None:
        if not isinstance(configuration, PostProcessedSingleAxisStitchingConfiguration):
            raise TypeError(
                f"configuration is expected to be an instance of {PostProcessedSingleAxisStitchingConfiguration}. Get {type(configuration)} instead"
            )
        super().__init__(configuration)
        self._stitching_regions_hdf5_dataset = None
        self._raw_regions_hdf5_dataset = None

    def create_output_dataset(self):
        """
        function called at the beginning of the stitching to prepare output dataset
        """
        self._dataset = h5py.VirtualLayout(
            shape=self._volume_shape,
            dtype=self._dtype,
        )

    @staticmethod
    def create_subset_selection(dataset: h5py.Dataset, slices: tuple) -> h5py.VirtualSource:
        assert isinstance(dataset, h5py.Dataset), f"dataset is expected to be a h5py.Dataset. Get {type(dataset)}"
        assert isinstance(slices, tuple), f"slices is expected to be a tuple of slices. Get {type(slices)} instead"
        import h5py._hl.selections as selection

        virtual_source = h5py.VirtualSource(dataset)
        sel = selection.select(dataset.shape, slices, dataset=dataset)
        virtual_source.sel = sel
        return virtual_source

    @PostProcessingStitchingDumper.output_dataset.setter
    def output_dataset(self, dataset: h5py.VirtualLayout | None):
        if dataset is not None and not isinstance(dataset, h5py.VirtualLayout):
            raise TypeError("in the case we want to avoid data duplication 'output_dataset' must be a VirtualLayout")
        self._output_dataset = dataset

    @property
    def stitching_regions_hdf5_dataset(self) -> tuple | None:
        """hdf5 dataset storing the stitched regions"""
        return self._stitching_regions_hdf5_dataset

    @stitching_regions_hdf5_dataset.setter
    def stitching_regions_hdf5_dataset(self, datasets: tuple):
        self._stitching_regions_hdf5_dataset = datasets

    @property
    def raw_regions_hdf5_dataset(self) -> tuple | None:
        """hdf5 raw dataset"""
        return self._raw_regions_hdf5_dataset

    @raw_regions_hdf5_dataset.setter
    def raw_regions_hdf5_dataset(self, datasets: tuple):
        self._raw_regions_hdf5_dataset = datasets

    def save_stitched_frame(
        self,
        stitched_frame: numpy.ndarray,
        composition_cls: dict,
        i_frame: int,
        axis: int,
    ):
        """
        Save the full stitched frame to disk
        """
        output_dataset = self.output_dataset
        if output_dataset is None:
            raise ValueError("output_dataset must be set before calling any frame stitching")
        stitching_regions_hdf5_dataset = self.stitching_regions_hdf5_dataset
        if stitching_regions_hdf5_dataset is None:
            raise ValueError("stitching_region_hdf5_dataset must be set before calling any frame stitching")
        raw_regions_hdf5_dataset = self.raw_regions_hdf5_dataset

        # save stitched region
        stitching_regions = composition_cls["overlap_composition"]
        for (_, _, region_start, region_end), stitching_region_hdf5_dataset in zip(
            stitching_regions.browse(), stitching_regions_hdf5_dataset
        ):
            assert isinstance(output_dataset, h5py.VirtualLayout)
            assert isinstance(stitching_region_hdf5_dataset, h5py.Dataset)
            stitching_region_array = stitched_frame[region_start:region_end]
            self.save_frame_to_disk(
                output_dataset=stitching_region_hdf5_dataset,
                index=i_frame,
                stitched_frame=stitching_region_array,
                axis=1,
                region_start=0,
                region_end=None,
            )
            vs = self.create_subset_selection(
                dataset=stitching_region_hdf5_dataset,
                slices=(
                    slice(0, stitching_region_hdf5_dataset.shape[0]),
                    slice(i_frame, i_frame + 1),
                    slice(0, stitching_region_hdf5_dataset.shape[2]),
                ),
            )

            self.save_frame_to_disk(
                output_dataset=output_dataset,
                index=i_frame,
                axis=axis,
                region_start=region_start,
                region_end=region_end,
                stitched_frame=vs,
            )

        # create virtual source of the raw data
        raw_regions = composition_cls["raw_composition"]
        for (frame_start, frame_end, region_start, region_end), raw_region_hdf5_dataset in zip(
            raw_regions.browse(), raw_regions_hdf5_dataset
        ):
            vs = self.create_subset_selection(
                dataset=raw_region_hdf5_dataset,
                slices=(
                    slice(frame_start, frame_end),
                    slice(i_frame, i_frame + 1),
                    slice(0, raw_region_hdf5_dataset.shape[2]),
                ),
            )
            self.save_frame_to_disk(
                output_dataset=output_dataset,
                index=i_frame,
                axis=1,
                region_start=region_start,
                region_end=region_end,
                stitched_frame=vs,
            )
