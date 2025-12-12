import h5py
import numpy
import logging
from .base import DumperBase
from nabu.stitching.config import PreProcessedSingleAxisStitchingConfiguration
from nabu import version as nabu_version
from nabu.io.writer import get_datetime
from silx.io.dictdump import dicttonx
from tomoscan.identifier import ScanIdentifier


_logger = logging.getLogger(__name__)


class PreProcessingStitchingDumper(DumperBase):
    """
    dumper to be used when save data durint pre-processing stitching (on projections). Output is expected to be an NXtomo
    """

    def __init__(self, configuration) -> None:
        if not isinstance(configuration, PreProcessedSingleAxisStitchingConfiguration):
            raise TypeError(
                f"configuration is expected to be an instance of {PreProcessedSingleAxisStitchingConfiguration}. Get {type(configuration)} instead"
            )
        super().__init__(configuration)

    def save_frame_to_disk(self, output_dataset: h5py.Dataset, index: int, stitched_frame: numpy.ndarray, **kwargs):
        output_dataset[index] = stitched_frame

    def save_configuration(self):
        """dump configuration used for stitching at the NXtomo entry"""
        process_name = "stitching_configuration"
        config_dict = self.configuration.to_dict()
        # adding nabu specific information
        nabu_process_info = {
            "@NX_class": "NXentry",
            f"{process_name}@NX_class": "NXprocess",
            f"{process_name}/program": "nabu-stitching",
            f"{process_name}/version": nabu_version,
            f"{process_name}/date": get_datetime(),
            f"{process_name}/configuration": config_dict,
        }

        dicttonx(
            nabu_process_info,
            h5file=self.configuration.output_file_path,
            h5path=self.configuration.output_data_path,
            update_mode="replace",
            mode="a",
        )

    @property
    def output_identifier(self) -> ScanIdentifier:
        return self.configuration.get_output_object().get_identifier()

    def create_output_dataset(self):
        """
        function called at the beginning of the stitching to prepare output dataset
        """
        raise NotImplementedError
