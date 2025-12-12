from os import path
import numpy as np
from ..resources.logger import LoggerOrPrint
from .utils import get_subregion
from .writer import WriterManager
from ..io.reader import get_hdf5_dataset_shape


class DataDumpManager:
    """
    A helper class for managing data dumps, with the aim of saving/resuming the processing from a given step.
    """

    def __init__(self, process_config, sub_region, margin=None, logger=None):
        """
        Initialize a DataDump object.

        Parameters
        -----------
        process_config: ProcessConfig
            ProcessConfig object
        sub_region: tuple of int
            Series of integers defining the sub-region being processed.
            The form is ((start_angle, end_angle), (start_z, end_z), (start_x, end_x))
        margin: tuple of int, optional
            Margin, used when processing data, in the form ((up, down), (left, right)).
            Each item can be None.
            Using a margin means that a given chunk of data will eventually be cropped as
            `data[:, up:-down, left:-right]`
        logger: Logger, optional
            Logging object
        """
        self.process_config = process_config
        self.processing_steps = process_config.processing_steps
        self.processing_options = process_config.processing_options
        self.dataset_info = process_config.dataset_info

        self._set_subregion_and_margin(sub_region, margin)
        self.logger = LoggerOrPrint(logger)
        self._configure_data_dumps()

    def _set_subregion_and_margin(self, sub_region, margin):
        self.sub_region = get_subregion(sub_region)
        self._z_sub_region = self.sub_region[1]
        self.z_min = self._z_sub_region[0]
        self.margin = get_subregion(margin, ndim=2)  # ((U, D), (L, R))
        self.margin_up = self.margin[0][0] or 0
        self.start_index = self.z_min + self.margin_up
        self.delta_z = self._z_sub_region[-1] - self._z_sub_region[-2]

        self._grouped_processing = False
        iangle1, iangle2 = self.sub_region[0]
        if iangle1 != 0 or iangle2 < len(self.process_config.rotation_angles(subsampling=False)):
            self._grouped_processing = True
            self.start_index = self.sub_region[0][0]

    def _configure_dump(self, step_name, force_dump_to_fname=None):
        if force_dump_to_fname is not None:
            # Shortcut
            fname_full = force_dump_to_fname
        elif step_name in self.processing_steps:
            # Standard case
            if not self.processing_options[step_name].get("save", False):
                return
            fname_full = self.processing_options[step_name]["save_steps_file"]
        elif step_name == "sinogram" and self.process_config.dump_sinogram:
            # "sinogram" is a special keyword
            fname_full = self.process_config.dump_sinogram_file
        else:
            return

        # "fname_full" is the path to the final master file.
        # We also need to create partial files (in a sub-directory)
        fname, ext = path.splitext(fname_full)
        dirname, file_prefix = path.split(fname)

        self.data_dump[step_name] = WriterManager(
            dirname,
            file_prefix,
            file_format="hdf5",
            overwrite=True,
            start_index=self.start_index,
            logger=self.logger,
            metadata={
                "process_name": step_name,
                "processing_index": 0,
                "config": {
                    "processing_options": self.processing_options,  # slow!
                    "nabu_config": self.process_config.nabu_config,
                },
                "entry": getattr(self.dataset_info.dataset_scanner, "entry", "entry"),
            },
        )

    def _configure_data_dumps(self):
        self.data_dump = {}
        for step_name in self.processing_steps:
            self._configure_dump(step_name)
        # sinogram is a special keyword: not in processing_steps, but guaranteed to be before sinogram generation
        if self.process_config.dump_sinogram:
            self._configure_dump("sinogram")

    def get_data_dump(self, step_name):
        """
        Get information on where to write a given processing step.

        Parameters
        ----------
        step_name: str
            Name of the processing step

        Returns
        -------
        writer_configurator: WriterConfigurator
            An object with information on where to write the data for the given processing step.
        """
        return self.data_dump.get(step_name, None)

    def get_read_dump_subregion(self):
        read_opts = self.processing_options["read_chunk"]
        if read_opts.get("process_file", None) is None:
            return None
        dump_start_z, dump_end_z = read_opts["dump_start_z"], read_opts["dump_end_z"]  # noqa: F841
        relative_start_z = self.z_min - dump_start_z
        relative_end_z = relative_start_z + self.delta_z
        # When using binning, every step after "read" results in smaller-sized data.
        # Therefore dumped data has shape (ceil(n_angles/subsampling), n_z//binning_z, n_x//binning_x)
        relative_start_z //= self.process_config.binning_z
        relative_end_z //= self.process_config.binning_z
        # (n_angles, n_z, n_x)
        subregion = (None, None, relative_start_z, relative_end_z, None, None)
        return subregion

    def _check_resume_from_step(self):
        read_opts = self.processing_options["read_chunk"]
        expected_radios_shape = get_hdf5_dataset_shape(  # noqa: F841
            read_opts["process_file"],
            read_opts["process_h5_path"],
            sub_region=self.get_read_dump_subregion(),
        )
        # TODO check

    def dump_data_to_file(self, step_name, data, crop_margin=False):
        if step_name not in self.data_dump:
            return
        writer = self.data_dump[step_name]
        self.logger.info("Dumping data to %s" % writer.fname)
        if not (isinstance(data, np.ndarray)):
            # assuming "device array" (cupy/pycuda/pyopencl)
            # note that we don't explicitly test the array type, as it would entail to import cupy (for example)
            # and we want to avoid importing cupy because cuda should not be initialized until really wanted (mess with multiprocessing fork)
            data = data.get()

        margin_up = self.margin[0][0] or None
        margin_down = self.margin[0][1] or None
        margin_down = -margin_down if margin_down is not None else None  # pylint: disable=E1130
        if crop_margin and (margin_up is not None or margin_down is not None):
            data = data[:, margin_up:margin_down, :]
        metadata = {"dump_sub_region": {"sub_region": self.sub_region, "margin": self.margin}}
        writer.write_data(data, metadata=metadata)

    def __repr__(self):
        res = "%s(%s, margin=%s)" % (self.__class__.__name__, str(self.sub_region), str(self.margin))
        if len(self.data_dump) > 0:
            for step_name, writer_configurator in self.data_dump.items():
                res += "\n- Dump %s to %s" % (step_name, writer_configurator.fname)
        return res
