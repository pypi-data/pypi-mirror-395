from .nabu_config import nabu_config, renamed_keys
from .dataset_validator import HelicalDatasetValidator
from ..fullfield import processconfig as ff_processconfig
from ...resources import dataset_analyzer


class ProcessConfig(ff_processconfig.ProcessConfig):
    default_nabu_config = nabu_config
    config_renamed_keys = renamed_keys
    _use_horizontal_translations = False

    def _configure_save_steps(self):
        self._dump_sinogram = False
        steps_to_save = self.nabu_config["pipeline"]["save_steps"]
        if steps_to_save in (None, ""):
            self.steps_to_save = []
            return
        steps_to_save = [s.strip() for s in steps_to_save.split(",")]
        for step in self.processing_steps:
            step = step.strip()
            if step in steps_to_save:
                self.processing_options[step]["save"] = True
                self.processing_options[step]["save_steps_file"] = self.get_save_steps_file(step_name=step)
        # "sinogram" is a special keyword, not explicitly in the processing steps
        if "sinogram" in steps_to_save:
            self._dump_sinogram = True
            self._dump_sinogram_file = self.get_save_steps_file(step_name="sinogram")
        self.steps_to_save = steps_to_save

    def _update_dataset_info_with_user_config(self):
        super()._update_dataset_info_with_user_config()

        self._get_translation_file("reconstruction", "z_per_proj_file", "z_per_proj", last_dim=1)
        self._get_translation_file("reconstruction", "x_per_proj_file", "x_per_proj", last_dim=1)

    def _get_user_sino_normalization(self):
        """is called by the base class but it is not used in helical"""
        pass

    def _coupled_validation(self):
        self.logger.debug("Doing coupled validation")
        self._dataset_validator = HelicalDatasetValidator(self.nabu_config, self.dataset_info)
        for what in ["rec_params", "rec_region", "binning", "subsampling_factor"]:
            setattr(self, what, getattr(self._dataset_validator, what))
            print(what, self._dataset_validator)

    def _browse_dataset(self, dataset_info):
        """
        Browse a dataset and builds a data structure with the relevant information.
        """
        self.logger.debug("Browsing dataset")
        if dataset_info is not None:
            self.dataset_info = dataset_info
        else:
            self.dataset_info = dataset_analyzer.analyze_dataset(
                self.nabu_config["dataset"]["location"],
                extra_options={
                    "exclude_projections": self.nabu_config["dataset"]["exclude_projections"],
                    "hdf5_entry": self.nabu_config["dataset"]["hdf5_entry"],
                },
                logger=self.logger,
            )
