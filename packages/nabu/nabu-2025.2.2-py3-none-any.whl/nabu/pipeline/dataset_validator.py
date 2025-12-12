import os
from ..resources.logger import LoggerOrPrint
from ..utils import copy_dict_items
from ..reconstruction.sinogram import get_extended_sinogram_width


class DatasetValidatorBase:
    # this in the helical derived class will be False
    _check_also_z = True

    def __init__(self, nabu_config, dataset_info, logger=None):
        """
        Perform a coupled validation of nabu configuration against dataset information.
        Check the consistency of these two structures, and modify them in-place.

        Parameters
        ----------
        nabu_config: dict
            Dictionary containing the nabu configuration, usually got from
            `nabu.pipeline.config.validate_config()`
            It will be modified !
        dataset_info: `DatasetAnalyzer` instance
            Structure containing information on the dataset to process.
            It will be modified !
        """
        self.nabu_config = nabu_config
        self.dataset_info = dataset_info
        self.logger = LoggerOrPrint(logger)
        self.rec_params = copy_dict_items(self.nabu_config["reconstruction"], self.nabu_config["reconstruction"].keys())
        self._validate()

    def _validate(self):
        raise ValueError("Base class")

    @property
    def is_halftomo(self):
        do_halftomo = self.nabu_config["reconstruction"].get("enable_halftomo", False)
        if do_halftomo == "auto":
            do_halftomo = self.dataset_info.is_halftomo
            if do_halftomo is None:
                raise ValueError(
                    "'enable_halftomo' was set to 'auto' but unable to get the information on field of view"
                )
        return do_halftomo

    def _check_not_empty(self):
        if len(self.dataset_info.projections) == 0:
            msg = "Dataset seems to be empty (no projections)"
            self.logger.fatal(msg)
            raise ValueError(msg)
        if self.dataset_info.n_angles is None:
            msg = "Could not determine the number of projections. Please check the .info or HDF5 file"
            self.logger.fatal(msg)
            raise ValueError(msg)
        for dim_name, n in zip(["dim_1", "dim_2"], self.dataset_info.radio_dims):
            if n is None:
                msg = "Could not determine %s. Please check the .info file or HDF5 file" % dim_name
                self.logger.fatal(msg)
                raise ValueError(msg)

    @staticmethod
    def _convert_negative_idx(idx, last_idx):
        res = idx
        if idx < 0:
            res = last_idx + idx
        return res

    def _get_nx_ny(self, binning_factor=1):
        nx = self.dataset_info.radio_dims[0] // binning_factor
        if self.is_halftomo:
            cor = self._get_cor(binning_factor=binning_factor)
            nx = get_extended_sinogram_width(nx, cor)
        ny = nx
        return nx, ny

    def _get_cor(self, binning_factor=1):
        cor = self.dataset_info.axis_position
        if binning_factor >= 1:
            # Backprojector uses middle of pixel for coordinate indices.
            # This means that the leftmost edge of the leftmost pixel has coordinate -0.5.
            # When using binning with a factor 'b', the CoR has to adapted as
            #   cor_binned  =  (cor + 0.5)/b - 0.5
            cor = (cor + 0.5) / binning_factor - 0.5
        return cor

    def _convert_negative_indices(self):
        """
        Convert any negative index to the corresponding positive index.
        """
        nx, nz = self.dataset_info.radio_dims
        ny = nx
        if self.is_halftomo:
            if self.dataset_info.axis_position is None:
                raise ValueError(
                    "Cannot use rotation axis position in the middle of the detector when half tomo is enabled"
                )
            nx, ny = self._get_nx_ny()

        what = (
            ("start_x", nx),
            ("end_x", nx),
            ("start_y", ny),
            ("end_y", ny),
        )
        if self._check_also_z:
            what = what + (
                ("start_z", nz),
                ("end_z", nz),
            )
        for key, upper_bound in what:
            val = self.rec_params[key]
            if isinstance(val, str):
                idx_mapping = {
                    "first": 0,
                    "middle": upper_bound // 2,  # works on both start_ and end_ since the end_ index is included
                    "last": upper_bound - 1,  # upper bound is included in the user interface (contrarily to python)
                }
                res = idx_mapping[val]
            else:
                res = self._convert_negative_idx(self.rec_params[key], upper_bound)
            self.rec_params[key] = res
            self.rec_region = copy_dict_items(self.rec_params, [w[0] for w in what])

    def _get_output_filename(self):
        # This function modifies nabu_config !
        opts = self.nabu_config["output"]
        dataset_path = self.nabu_config["dataset"]["location"]
        if opts["location"] == "" or opts["location"] is None:
            opts["location"] = os.path.dirname(dataset_path)
        if opts["file_prefix"] == "" or opts["file_prefix"] is None:
            if os.path.isfile(dataset_path):  # hdf5
                file_prefix = os.path.basename(dataset_path).split(".")[0]
            elif os.path.isdir(dataset_path):
                file_prefix = os.path.basename(dataset_path)
            else:
                raise ValueError("dataset location %s is neither a file or directory" % dataset_path)
            file_prefix += "_rec"  # avoid overwriting dataset
            opts["file_prefix"] = file_prefix

    @staticmethod
    def _check_start_end_idx(start, end, n_elements, start_name="start_x", end_name="end_x"):
        assert start >= 0 and start < n_elements, "Invalid value %d for %s, must be >= 0 and < %d" % (
            start,
            start_name,
            n_elements,
        )
        assert end >= 0 and end < n_elements, "Invalid value for %d %s, must be >= 0 and < %d" % (
            end,
            end_name,
            n_elements,
        )
        assert start <= end, "Must have %s <= %s" % (start_name, end_name)

    def _handle_binning(self):
        """
        Modify the dataset description/process config to handle binning and projections subsampling
        """
        dataset_cfg = self.nabu_config["dataset"]
        self.binning = (dataset_cfg["binning"], dataset_cfg["binning_z"])
        subsampling_factor, subsampling_start = dataset_cfg["projections_subsampling"]
        self.subsampling_factor = subsampling_factor or 1
        self.subsampling_start = subsampling_start or 0

        if self.binning != (1, 1):
            bin_x, bin_z = self.binning
            rec_cfg = self.rec_params

            # Update "start_xyz"
            rec_cfg["start_x"] //= bin_x
            rec_cfg["start_y"] //= bin_x
            rec_cfg["start_z"] //= bin_z

            # Update "end_xyz". Things are a little bit more complicated for several reasons:
            #   - In the user interface (configuration file), end_xyz index is INCLUDED (contrarily to python). So there are +1, -1 all over the place.
            #   - When using half tomography, n_x and n_y are less straightforward : 2*CoR(binning) instead of 2*CoR//binning
            #   - delta = end - start [+1]  should be a multiple of binning factor. This makes things much easier for processing pipeline.

            def ensure_multiple_of_binning(end, start, binning_factor):
                """
                Update "end" so that end-start is a multiple of "binning_factor"
                Note that "end" is INCLUDED here (comes from user configuration)
                """
                return end - ((end - start + 1) % binning_factor)

            end_z = ensure_multiple_of_binning(rec_cfg["end_z"], rec_cfg["start_z"], bin_z)
            rec_cfg["end_z"] = (end_z + 1) // bin_z - 1

            nx_binned, ny_binned = self._get_nx_ny(binning_factor=bin_x)

            end_y = ensure_multiple_of_binning(rec_cfg["end_y"], rec_cfg["start_y"], bin_x)
            rec_cfg["end_y"] = min((end_y + 1) // bin_x - 1, ny_binned - 1)

            end_x = ensure_multiple_of_binning(rec_cfg["end_x"], rec_cfg["start_x"], bin_x)
            rec_cfg["end_x"] = min((end_x + 1) // bin_x - 1, nx_binned - 1)

    def _check_output_file(self):
        out_cfg = self.nabu_config["output"]
        out_fname = os.path.join(out_cfg["location"], out_cfg["file_prefix"] + out_cfg["file_format"])
        if os.path.exists(out_fname):
            raise ValueError("File %s already exists" % out_fname)

    def _handle_processing_mode(self):
        mode = self.nabu_config["resources"]["method"]
        if mode == "preview":
            print(
                "Warning: the method 'preview' was selected. This means that the data volume will be binned so that everything fits in memory."
            )
            # TODO automatically compute binning/subsampling factors as a function of lowest memory (GPU)
            self.nabu_config["dataset"]["binning"] = 2
            self.nabu_config["dataset"]["binning_z"] = 2
            self.nabu_config["dataset"]["projections_subsampling"] = 2, 0
        # TODO handle other modes
