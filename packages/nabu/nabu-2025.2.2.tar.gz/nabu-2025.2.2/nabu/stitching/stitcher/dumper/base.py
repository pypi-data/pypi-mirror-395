import h5py
import numpy
from tomoscan.identifier import BaseIdentifier
from nabu.stitching.config import StitchingConfiguration
from tomoscan.volumebase import VolumeBase


class DumperBase:
    """
    Base class to define all the functions that can be used to save a stitching
    """

    def __init__(self, configuration) -> None:
        assert isinstance(configuration, StitchingConfiguration)
        self._configuration = configuration

    @property
    def configuration(self):
        return self._configuration

    @property
    def output_identifier(self) -> BaseIdentifier:
        raise NotImplementedError("Base class")

    def save_stitched_frame(
        self,
        stitched_frame: numpy.ndarray,
        i_frame: int,
        axis: int,
        **kwargs,
    ):
        self.save_frame_to_disk(
            output_dataset=self.output_dataset,
            index=i_frame,
            stitched_frame=stitched_frame,
            axis=axis,
            region_start=0,
            region_end=None,
        )

    @property
    def output_dataset(self) -> h5py.VirtualLayout | h5py.Dataset | VolumeBase | None:
        return self._output_dataset

    @output_dataset.setter
    def output_dataset(self, dataset: h5py.VirtualLayout | h5py.Dataset | VolumeBase | None):
        self._output_dataset = dataset

    @staticmethod
    def save_frame_to_disk(
        output_dataset: h5py.Dataset | h5py.VirtualLayout,
        index: int,
        stitched_frame: numpy.ndarray | h5py.VirtualSource,
        axis: int,
        region_start: int,
        region_end: int,
    ):
        if not isinstance(output_dataset, (h5py.VirtualLayout, h5py.Dataset, numpy.ndarray)):
            raise TypeError(
                f"'output_dataset' should be a 'h5py.Dataset' or a 'h5py.VirtualLayout'. Get {type(output_dataset)}"
            )
        if not isinstance(stitched_frame, (h5py.VirtualSource, numpy.ndarray)):
            raise TypeError(
                f"'stitched_frame' should be a 'numpy.ndarray' or a 'h5py.VirtualSource'. Get {type(stitched_frame)}"
            )
        if isinstance(output_dataset, h5py.VirtualLayout) and not isinstance(stitched_frame, h5py.VirtualSource):
            raise TypeError(
                "output_dataset is an instance of h5py.VirtualLayout and stitched_frame not an instance of h5py.VirtualSource"
            )
        if axis == 0:
            if region_end is not None:
                output_dataset[index, region_start:region_end] = stitched_frame
            else:
                output_dataset[index, region_start:] = stitched_frame
        elif axis == 1:
            if region_end is not None:
                output_dataset[region_start:region_end, index, :] = stitched_frame
            else:
                output_dataset[region_start:, index, :] = stitched_frame
        elif axis == 2:
            if region_end is not None:
                output_dataset[region_start:region_end, :, index] = stitched_frame
            else:
                output_dataset[region_start:, :, index] = stitched_frame
        else:
            raise ValueError(f"provided axis ({axis}) is invalid")

    def create_output_dataset(self):
        """
        function called at the beginning of the stitching to prepare output dataset
        """
        raise NotImplementedError
