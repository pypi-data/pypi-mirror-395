from ..dataset_validator import DatasetValidatorBase


class FullFieldDatasetValidator(DatasetValidatorBase):
    def _validate(self):
        self._check_not_empty()
        self._convert_negative_indices()
        self._get_output_filename()
        self._check_can_do_flatfield()
        self._check_can_do_phase()
        self._check_can_do_reconstruction()
        self._check_slice_indices()
        self._handle_processing_mode()
        self._handle_binning()
        self._check_output_file()

    def _check_can_do_flatfield(self):
        if self.nabu_config["preproc"]["flatfield"]:
            darks = self.dataset_info.darks
            assert len(darks) > 0, "Need at least one dark to perform flat-field correction"
            flats = self.dataset_info.flats
            assert len(flats) > 0, "Need at least one flat to perform flat-field correction"

    def _check_slice_indices(self):
        nx, nz = self.dataset_info.radio_dims
        rec_params = self.rec_params
        if self.is_halftomo:
            ny, nx = self._get_nx_ny()
        what = (("start_x", "end_x", nx), ("start_y", "end_y", nx), ("start_z", "end_z", nz))
        for start_name, end_name, numels in what:
            self._check_start_end_idx(
                rec_params[start_name], rec_params[end_name], numels, start_name=start_name, end_name=end_name
            )

    def _check_can_do_phase(self):
        if self.nabu_config["phase"]["method"] is None:
            return
        self.dataset_info.check_defined_attribute("distance")
        self.dataset_info.check_defined_attribute("pixel_size")

    def _check_can_do_reconstruction(self):
        rec_options = self.nabu_config["reconstruction"]
        if rec_options["method"] is None:
            return
        self.dataset_info.check_defined_attribute("pixel_size")
        if rec_options["method"] == "cone":
            if rec_options["source_sample_dist"] is None:
                err_msg = "In cone-beam reconstruction, you have to provide 'source_sample_dist' in [reconstruction]"
                self.logger.fatal(err_msg)
                raise ValueError(err_msg)
            if rec_options["sample_detector_dist"] is None:
                if self.dataset_info.distance is None:
                    err_msg = "Cone-beam reconstruction: 'sample_detector_dist' was not provided but could not be found in the dataset metadata either. Please provide 'sample_detector_dist'"
                    self.logger.fatal(err_msg)
                    raise ValueError(err_msg)
                self.logger.warning(
                    "Cone-beam reconstruction: 'sample_detector_dist' not provided, will use the one in dataset metadata"
                )
            if self.is_halftomo:
                err_msg = "Cone-beam reconstruction with half-acquisition is not supported yet"
                self.logger.fatal(err_msg)
                raise NotImplementedError(err_msg)
