import os
import posixpath
import numpy as np
from silx.io import get_data
from silx.io.url import DataUrl
from ...utils import copy_dict_items, compare_dicts, deprecation_warning
from ...io.utils import hdf5_entry_exists, get_h5_value
from ...io.reader import import_h5_to_dict
from ...resources.utils import extract_parameters, get_values_from_file
from ...resources.nxflatfield import update_dataset_info_flats_darks
from ...resources.utils import get_quantities_and_units
from ..estimators import estimate_cor
from ..processconfig import ProcessConfigBase
from ..config_validators import convert_to_bool
from .nabu_config import nabu_config, renamed_keys
from .dataset_validator import FullFieldDatasetValidator
from nxtomo.nxobject.nxdetector import ImageKey


class ProcessConfig(ProcessConfigBase):
    """
    A ProcessConfig object has these main fields:
      - dataset_info: information about the current dataset
      - nabu_config: configuration from the user side
      - processing_steps/processing_options: configuration "ready-to use" for underlying classes

    It is built from the following steps.

    (1a) parse config: (conf_fname or conf_dict) --> "nabu_config"

    (1b) browse dataset: (nabu_config or existing dataset_info)  --> dataset_info


    (2) update_dataset_info_with_user_config
      - Update flats/darks
      - Double-flat-field
      - CoR  (value or estimation method) # no estimation yet
      - rotation angles
      - translations files
      - user sino normalization (eg. subtraction etc)

    (3) estimations
      - tilt
      - CoR

    (4) coupled validation

    (5) build processing steps

    (6) configure checkpoints (save/resume)
    """

    default_nabu_config = nabu_config
    config_renamed_keys = renamed_keys
    _use_horizontal_translations = True
    _all_processing_steps = [
        "read_chunk",
        "flatfield",
        "ccd_correction",
        "double_flatfield",
        "tilt_correction",
        "phase",
        "unsharp_mask",
        "take_log",
        "radios_movements",  # radios are cropped after this step, if needed
        "sino_normalization",
        "sino_rings_correction",
        "reconstruction",
        "histogram",
        "save",
    ]

    def _update_dataset_info_with_user_config(self):
        """
        Update the 'dataset_info' (DatasetAnalyzer class instance) data structure with options from user configuration.
        """
        self.logger.debug("Updating dataset information with user configuration")
        if self.dataset_info.kind == "nx" and self.nabu_config["preproc"]["flatfield"]:
            update_dataset_info_flats_darks(
                self.dataset_info,
                self.nabu_config["preproc"]["flatfield"],
                loading_mode=self.nabu_config["preproc"]["flatfield_loading_mode"],
                output_dir=self.nabu_config["output"]["location"],
                darks_flats_dir=self.nabu_config["dataset"]["darks_flats_dir"],
            )
        elif self.dataset_info.kind == "edf":
            self.dataset_info.flats = self.dataset_info.get_reduced_flats()
            self.dataset_info.darks = self.dataset_info.get_reduced_darks()
        self.rec_params = self.nabu_config["reconstruction"]

        subsampling_factor, subsampling_start = self.nabu_config["dataset"]["projections_subsampling"]
        self.subsampling_factor = subsampling_factor or 1
        self.subsampling_start = subsampling_start or 0

        self._get_double_flatfield()
        self._update_dataset_with_user_overwrites()
        self._get_rotation_axis_position()
        self._update_rotation_angles()
        self._get_translation_file("reconstruction", "translation_movements_file", "translations")
        self._get_user_sino_normalization()

    def _get_double_flatfield(self):
        self._dff_file = None
        dff_mode = self.nabu_config["preproc"]["double_flatfield"]
        if not (dff_mode):
            return
        from .get_double_flatfield import get_double_flatfield

        self._dff_file = get_double_flatfield(
            self.dataset_info,
            dff_mode,
            output_dir=self.nabu_config["output"]["location"],
            darks_flats_dir=self.nabu_config["dataset"]["darks_flats_dir"],
            dff_options={
                "dff_sigma": self.nabu_config["preproc"]["dff_sigma"],
                "do_flatfield": (self.nabu_config["preproc"]["flatfield"] is not False),
            },
        )

    def _update_dataset_with_user_overwrites(self):
        # Update info on frames flip
        user_flip_lr = self.nabu_config["dataset"].get("flip_lr", "auto")
        if user_flip_lr != "auto":
            self.logger.warning(f"Resetting flip_lr to {user_flip_lr}")
            self.dataset_info.flip_frame_lr = user_flip_lr
        user_flip_ud = self.nabu_config["dataset"].get("flip_ud", "auto")
        if user_flip_ud != "auto":
            self.logger.warning(f"Resetting flip_ud to {user_flip_ud}")
            self.dataset_info.flip_frame_ud = user_flip_ud

        # Update some metadata: pixel_size, distance, energy
        user_overwrites = self.nabu_config["dataset"]["overwrite_metadata"].strip()
        if user_overwrites in ("", None):
            return
        possible_overwrites = {"pixel_size": 1e6, "distance": 1.0, "energy": 1.0}
        try:
            overwrites = get_quantities_and_units(user_overwrites)
        except ValueError:
            msg = (
                "Something wrong in config file in 'overwrite_metadata': could not get quantities/units from '%s'. Please check that separators are ';' and that units are provided (separated by a space)"
                % user_overwrites
            )
            self.logger.fatal(msg)
            raise ValueError(msg)
        for quantity, conversion_factor in possible_overwrites.items():
            user_value = overwrites.pop(quantity, None)
            if user_value is not None:
                self.logger.info("Overwriting %s = %s" % (quantity, user_value))
                user_value *= conversion_factor
                setattr(self.dataset_info, quantity, user_value)

    def _get_translation_file(self, config_section, config_key, dataset_info_attr, last_dim=2):
        transl_file = self.nabu_config[config_section][config_key]
        if transl_file in (None, ""):
            return
        translations = None
        if transl_file is not None and "://" not in transl_file:
            try:
                translations = get_values_from_file(
                    transl_file, shape=(self.n_angles(subsampling=False), last_dim), any_size=True
                ).astype(np.float32)
                translations = translations[self.subsampling_start :: self.subsampling_factor]
            except ValueError:
                print("Something wrong with translation_movements_file %s" % transl_file)
                raise
        else:
            try:
                translations = get_data(transl_file)
            except:
                print("Something wrong with translation_movements_file %s" % transl_file)
                raise
        setattr(self.dataset_info, dataset_info_attr, translations)
        if self._use_horizontal_translations and translations is not None:
            # Horizontal translations are handled by "axis_correction" in backprojector
            horizontal_translations = translations[:, 0]
            if np.max(np.abs(horizontal_translations)) > 1e-3:
                self.dataset_info.axis_correction = horizontal_translations

    def _get_rotation_axis_position(self):
        super()._get_rotation_axis_position()
        rec_params = self.nabu_config["reconstruction"]
        axis_correction_file = rec_params["axis_correction_file"]
        axis_correction = None
        if axis_correction_file is not None:
            try:
                axis_correction = get_values_from_file(
                    axis_correction_file,
                    n_values=self.n_angles(subsampling=False),
                    any_size=True,
                ).astype(np.float32)
                axis_correction = axis_correction[self.subsampling_start :: self.subsampling_factor]
            except ValueError:
                print("Something wrong with axis correction file %s" % axis_correction_file)
                raise
        self.dataset_info.axis_correction = axis_correction

    def _update_rotation_angles(self):
        rec_params = self.nabu_config["reconstruction"]
        n_angles = self.dataset_info.n_angles
        angles_file = rec_params["angles_file"]
        if angles_file is not None:
            try:
                angles = get_values_from_file(angles_file, n_values=n_angles, any_size=True)
                angles = np.deg2rad(angles)
            except ValueError:
                self.logger.fatal("Something wrong with angle file %s" % angles_file)
                raise
            self.dataset_info.rotation_angles = angles
        elif self.dataset_info.rotation_angles is None:
            angles_range_txt = "[0, 180[ degrees"
            if rec_params["enable_halftomo"]:
                angles_range_txt = "[0, 360] degrees"
                angles = np.linspace(0, 2 * np.pi, n_angles, True)
            else:
                angles = np.linspace(0, np.pi, n_angles, False)
            self.logger.warning(
                "No information was found on rotation angles. Using default %s (half tomo is %s)"
                % (angles_range_txt, {0: "OFF", 1: "ON"}[int(self.do_halftomo)])
            )
            self.dataset_info.rotation_angles = angles

    def _get_cor(self):
        cor = self.nabu_config["reconstruction"]["rotation_axis_position"]
        if isinstance(cor, str):  # auto-CoR
            cor = estimate_cor(
                cor,
                self.dataset_info,
                do_flatfield=(self.nabu_config["preproc"]["flatfield"] is not False),
                cor_options=self.nabu_config["reconstruction"]["cor_options"],
                logger=self.logger,
            )
            self.logger.info("Estimated center of rotation: %.3f" % cor)
        self.dataset_info.axis_position = cor

    def _get_user_sino_normalization(self):
        self._sino_normalization_arr = None
        norm = self.nabu_config["preproc"]["sino_normalization"]
        if norm not in ["subtraction", "division"]:
            return
        norm_path = "silx://" + self.nabu_config["preproc"]["sino_normalization_file"].strip()
        url = DataUrl(norm_path)
        try:
            norm_array = get_data(url)
            self._sino_normalization_arr = norm_array.astype("f")
        except (ValueError, OSError) as exc:
            error_msg = "Could not load sino_normalization_file %s. The error was: %s" % (norm_path, str(exc))
            self.logger.error(error_msg)
            raise ValueError(error_msg)

    @property
    def do_halftomo(self):
        """
        Return True if the current dataset is to be reconstructed using 'half-acquisition' setting.
        """
        enable_halftomo = self.nabu_config["reconstruction"]["enable_halftomo"]
        is_halftomo_dataset = self.dataset_info.is_halftomo
        if enable_halftomo == "auto":
            if is_halftomo_dataset is None:
                raise ValueError(
                    "enable_halftomo was set to 'auto', but information on field of view was not found. Please set either 0 or 1 for enable_halftomo"
                )
            return is_halftomo_dataset
        return enable_halftomo

    def _coupled_validation(self):
        self.logger.debug("Doing coupled validation")
        self._dataset_validator = FullFieldDatasetValidator(self.nabu_config, self.dataset_info)
        # Not so ideal to propagate fields like this
        for what in ["rec_params", "rec_region", "binning"]:
            setattr(self, what, getattr(self._dataset_validator, what))

    #
    # Attributes that combine dataset information and user overwrites (eg. binning).
    # Must be accessed after __init__() is done
    #

    @property
    def binning_x(self):
        return getattr(self, "binning", (1, 1))[0]

    @property
    def binning_z(self):
        return getattr(self, "binning", (1, 1))[1]

    @property
    def subsampling(self):
        return getattr(self, "subsampling_factor", None)

    def radio_shape(self, binning=False):
        n_x, n_z = self.dataset_info.radio_dims
        if binning:
            n_z //= self.binning_z
            n_x //= self.binning_x
        return (n_z, n_x)

    def n_angles(self, subsampling=False):
        rot_angles = self.dataset_info.rotation_angles
        if subsampling:
            rot_angles = rot_angles[self.subsampling_start :: self.subsampling_factor]
        return len(rot_angles)

    def radios_shape(self, binning=False, subsampling=False):
        n_z, n_x = self.radio_shape(binning=binning)
        n_a = self.n_angles(subsampling=subsampling)
        return (n_a, n_z, n_x)

    def rotation_axis_position(self, binning=False):
        cor = self.dataset_info.axis_position  # might be None (default to the middle of detector)
        if cor is None and self.do_halftomo:
            raise ValueError("No information on center of rotation, cannot use half-tomography reconstruction")
        if cor is not None and binning:
            # Backprojector uses middle of pixel for coordinate indices.
            # This means that the leftmost edge of the leftmost pixel has coordinate -0.5.
            # When using binning with a factor 'b', the CoR has to adapted as
            #   cor_binned  =  (cor + 0.5)/b - 0.5
            cor = (cor + 0.5) / self.binning_x - 0.5
        return cor

    def sino_shape(self, binning=False, subsampling=False):
        """
        Return the shape of a sinogram image.

        Parameter
        ---------
        binning: bool
            Whether to account for image binning
        subsampling: bool
            Whether to account for projections subsampling
        """
        n_a, _, n_x = self.radios_shape(binning=binning, subsampling=subsampling)
        return (n_a, n_x)

    def sinos_shape(self, binning=False, subsampling=False):
        n_z, _ = self.radio_shape(binning=binning)
        return (n_z,) + self.sino_shape(binning=binning, subsampling=subsampling)

    def projs_indices(self, subsampling=False):
        step = 1
        if subsampling:
            step = self.subsampling or 1
        return sorted(self.dataset_info.projections.keys())[::step]

    def rotation_angles(self, subsampling=False):
        start = 0
        step = 1
        if subsampling:
            start = self.subsampling_start
            step = self.subsampling_factor
        return self.dataset_info.rotation_angles[start::step]

    @property
    def rec_roi(self):
        """
        Returns the reconstruction region of interest (ROI), accounting for binning in both dimensions.
        """
        rec_params = self.rec_params  # accounts for binning
        x_s, x_e = rec_params["start_x"], rec_params["end_x"]
        y_s, y_e = rec_params["start_y"], rec_params["end_y"]
        # Upper bound (end_xy) is INCLUDED in nabu config, hence the +1 here
        return (x_s, x_e + 1, y_s, y_e + 1)

    @property
    def rec_shape(self):
        # Accounts for binning!
        return tuple(np.diff(self.rec_roi)[::-2])

    @property
    def rec_delta_z(self):
        # Accounts for binning!
        z_s, z_e = self.rec_params["start_z"], self.rec_params["end_z"]
        # Upper bound (end_xy) is INCLUDED in nabu config, hence the +1 here
        return z_e + 1 - z_s

    def is_before_radios_cropping(self, step):
        """
        Return true if a given processing step happens before radios cropping
        """
        if step == "sinogram":
            return False
        if step not in self._all_processing_steps:
            raise ValueError("Unknown step: '%s'. Available are: %s" % (step, self._all_processing_steps))
        # sino_normalization
        return self._all_processing_steps.index(step) <= self._all_processing_steps.index("radios_movements")

    #
    # Build processing steps
    #

    # TODO update behavior and remove this function once GroupedPipeline cuda backend is implemented
    def get_radios_rotation_mode(self):
        """
        Determine whether projections are to be rotated, and if so, when they are to be rotated.

        Returns
        -------
        method: str or None
            Rotation method: one of the values of `nabu.resources.params.radios_rotation_mode`
        """
        tilt = self.dataset_info.detector_tilt
        phase_method = self.nabu_config["phase"]["method"]
        do_ctf = phase_method == "CTF"
        do_pag = phase_method == "paganin"
        do_unsharp = (
            self.nabu_config["phase"]["unsharp_method"] is not None and self.nabu_config["phase"]["unsharp_coeff"] > 0
        )
        if tilt is None:
            return None
        if do_ctf:
            return "full"
        # TODO "chunked" rotation is done only when using a "processing margin"
        # For now the processing margin is enabled only if phase or unsharp is enabled.
        # We can either
        #   - Enable processing margin if rotating projections is needed (more complicated to implement)
        #   - Always do "full" rotation (simpler to implement, at the expense of performances)
        if do_pag or do_unsharp:
            return "chunk"
        else:
            return "full"

    def _build_processing_steps(self):
        nabu_config = self.nabu_config
        dataset_info = self.dataset_info
        binning = (nabu_config["dataset"]["binning"], nabu_config["dataset"]["binning_z"])
        tasks = []
        options = {}

        #
        # Dataset / Get data
        #
        # First thing to do is to get the data (radios or sinograms)
        # For now data is assumed to be on disk (see issue #66).
        tasks.append("read_chunk")
        options["read_chunk"] = {
            "sub_region": None,
            "binning": binning,
            "dataset_subsampling": nabu_config["dataset"]["projections_subsampling"],
        }
        #
        # Flat-field
        #
        if nabu_config["preproc"]["flatfield"]:
            ff_method = "pca" if nabu_config["preproc"]["flatfield"] == "pca" else "default"
            tasks.append("flatfield")
            options["flatfield"] = {
                "method": ff_method,
                #  Data reader handles binning/subsampling by itself,
                # but FlatField needs "real" indices (after binning/subsampling)
                "projs_indices": self.projs_indices(subsampling=False),
                "binning": binning,
                "do_flat_distortion": nabu_config["preproc"]["flat_distortion_correction_enabled"],
                "flat_distortion_params": extract_parameters(nabu_config["preproc"]["flat_distortion_params"]),
            }
            normalize_srcurrent = nabu_config["preproc"]["normalize_srcurrent"] and ff_method == "default"
            radios_srcurrent = None
            flats_srcurrent = None
            if normalize_srcurrent:
                if (
                    dataset_info.projections_srcurrent is None
                    or dataset_info.flats_srcurrent is None
                    or len(dataset_info.flats_srcurrent) == 0
                ):
                    self.logger.error("Cannot do SRCurrent normalization: missing flats and/or projections SRCurrent")
                    normalize_srcurrent = False
                else:
                    radios_srcurrent = dataset_info.projections_srcurrent
                    flats_srcurrent = dataset_info.flats_srcurrent
            options["flatfield"].update(
                {
                    "normalize_srcurrent": normalize_srcurrent,
                    "radios_srcurrent": radios_srcurrent,
                    "flats_srcurrent": flats_srcurrent,
                }
            )
            if len(dataset_info.darks) > 1:
                self.logger.warning("Cannot do flat-field with more than one reduced dark. Taking the first one.")
                dataset_info.darks = dataset_info.darks[sorted(dataset_info.darks.keys())[0]]

        #
        # Spikes filter
        #
        if nabu_config["preproc"]["ccd_filter_enabled"]:
            tasks.append("ccd_correction")
            options["ccd_correction"] = {
                "type": "median_clip",  # only one available for now
                "median_clip_thresh": nabu_config["preproc"]["ccd_filter_threshold"],
            }
        #
        # Double flat field
        #
        # ---- COMPAT  ----
        if convert_to_bool(nabu_config["preproc"].get("double_flatfield_enabled", False))[0]:
            deprecation_warning(
                "'double_flatfield_enabled' has been renamed to 'double_flatfield'. Please update your configuration file"
            )
            nabu_config["preproc"]["double_flatfield"] = True

        # -------------
        if nabu_config["preproc"]["double_flatfield"]:
            tasks.append("double_flatfield")
            options["double_flatfield"] = {
                "sigma": nabu_config["preproc"]["dff_sigma"],
                "processes_file": self._dff_file or nabu_config["preproc"]["processes_file"],
                "log_min_clip": nabu_config["preproc"]["log_min_clip"],
                "log_max_clip": nabu_config["preproc"]["log_max_clip"],
            }
        #
        # Radios rotation (do it here if possible)
        #
        if self.get_radios_rotation_mode() == "chunk":
            tasks.append("tilt_correction")
            options["tilt_correction"] = {
                "angle": dataset_info.detector_tilt,
                "center": nabu_config["preproc"]["rotate_projections_center"],
                "mode": "chunk",
            }
        #
        #
        # Phase retrieval
        #
        if nabu_config["phase"]["method"] is not None:
            tasks.append("phase")
            options["phase"] = copy_dict_items(nabu_config["phase"], ["method", "delta_beta", "padding_type"])
            options["phase"].update(
                {
                    "energy_kev": dataset_info.energy,
                    "distance_cm": dataset_info.distance * 1e2,
                    "distance_m": dataset_info.distance,
                    "pixel_size_microns": dataset_info.pixel_size,
                    "pixel_size_m": dataset_info.pixel_size * 1e-6,
                }
            )
            if binning != (1, 1):
                options["phase"]["delta_beta"] /= binning[0] * binning[1]
            if options["phase"]["method"] == "CTF":
                self._get_ctf_parameters(options["phase"])
        #
        # Unsharp
        #
        if (
            nabu_config["phase"]["unsharp_method"] is not None
            and nabu_config["phase"]["unsharp_coeff"] > 0
            and nabu_config["phase"]["unsharp_sigma"] > 0
        ):
            tasks.append("unsharp_mask")
            options["unsharp_mask"] = copy_dict_items(
                nabu_config["phase"], ["unsharp_coeff", "unsharp_sigma", "unsharp_method"]
            )
        #
        # -logarithm
        #
        if nabu_config["preproc"]["take_logarithm"]:
            tasks.append("take_log")
            options["take_log"] = copy_dict_items(nabu_config["preproc"], ["log_min_clip", "log_max_clip"])
        #
        # Radios rotation (do it here if mode=="full")
        #
        if self.get_radios_rotation_mode() == "full":
            tasks.append("tilt_correction")
            options["tilt_correction"] = {
                "angle": dataset_info.detector_tilt,
                "center": nabu_config["preproc"]["rotate_projections_center"],
                "mode": "full",
            }
        #
        # Translation movements
        #

        translations = dataset_info.translations
        if translations is not None:
            if np.max(np.abs(translations[:, 1])) < 1e-5:
                self.logger.warning("No vertical translation greater than 1e-5 - disabling vertical shifts")
                # horizontal movements are handled in backprojector
            else:
                tasks.append("radios_movements")
                options["radios_movements"] = {"translation_movements": dataset_info.translations}
        #
        # Sinogram normalization (before half-tomo)
        #
        if nabu_config["preproc"]["sino_normalization"] is not None:
            tasks.append("sino_normalization")
            options["sino_normalization"] = {
                "method": nabu_config["preproc"]["sino_normalization"],
                "normalization_array": self._sino_normalization_arr,
            }

        #
        # Sinogram-based rings artefacts removal
        #
        if nabu_config["preproc"]["sino_rings_correction"]:
            tasks.append("sino_rings_correction")
            options["sino_rings_correction"] = {
                "method": nabu_config["preproc"]["sino_rings_correction"],
                "user_options": nabu_config["preproc"]["sino_rings_options"],
            }
        #
        # Reconstruction
        #
        if nabu_config["reconstruction"]["method"] is not None:
            tasks.append("reconstruction")
            # Iterative is not supported through configuration file for now.
            options["reconstruction"] = copy_dict_items(
                self.rec_params,
                [
                    "method",
                    "iterations",
                    "implementation",
                    "fbp_filter_type",
                    "fbp_filter_cutoff",
                    "padding_type",
                    "start_x",
                    "end_x",
                    "start_y",
                    "end_y",
                    "start_z",
                    "end_z",
                    "centered_axis",
                    "clip_outer_circle",
                    "outer_circle_value",
                    "source_sample_dist",
                    "sample_detector_dist",
                    "hbp_legs",
                    "hbp_reduction_steps",
                    "crop_filtered_data",
                ],
            )
            rec_options = options["reconstruction"]
            rec_options["rotation_axis_position"] = self.rotation_axis_position(binning=True)
            if self.dataset_info.flip_frame_lr:
                # flip 'rotation_axis_position' according to detector lr flip
                rec_options["rotation_axis_position"] = (
                    self.sino_shape(binning=True)[-1] - 1 - rec_options["rotation_axis_position"]
                )
            rec_options["enable_halftomo"] = self.do_halftomo
            rec_options["axis_correction"] = dataset_info.axis_correction
            if dataset_info.axis_correction is not None:
                rec_options["axis_correction"] = rec_options["axis_correction"]

            rec_options["angles"] = np.array(self.rotation_angles(subsampling=True))
            rec_options["angles"] += np.deg2rad(nabu_config["reconstruction"]["angle_offset"])
            voxel_size = dataset_info.pixel_size * 1e-4
            rec_options["voxel_size_cm"] = (
                voxel_size,
                voxel_size,
                voxel_size,
            )  # pix size is in microns in dataset_info

            # x/y/z position information
            def get_mean_pos(position_array):
                if position_array is None:
                    return None
                else:
                    position_array = np.array(position_array)
                    # filter only projections. Avoid getting noise
                    position_array = position_array[
                        np.asarray(dataset_info.dataset_scanner.image_key_control) == ImageKey.PROJECTION.value
                    ]
                    return float(np.mean(position_array))

            mean_positions_xyz = (
                get_mean_pos(dataset_info.dataset_scanner.z_translation),
                get_mean_pos(dataset_info.dataset_scanner.y_translation),
                get_mean_pos(dataset_info.dataset_scanner.x_translation),
            )
            if all([m is not None for m in mean_positions_xyz]):
                rec_options["position"] = mean_positions_xyz
            if rec_options["method"] == "cone" and rec_options["sample_detector_dist"] is None:
                rec_options["sample_detector_dist"] = self.dataset_info.distance  # was checked to be not None earlier
            if rec_options["method"].lower() == "mlem" and rec_options["implementation"] in [None, ""]:
                rec_options["implementation"] = "nabu"

            # New key
            rec_options["cor_estimated_auto"] = isinstance(nabu_config["reconstruction"]["rotation_axis_position"], str)
        #
        # Histogram
        #
        if nabu_config["postproc"]["output_histogram"]:
            tasks.append("histogram")
            options["histogram"] = copy_dict_items(nabu_config["postproc"], ["histogram_bins"])
        #
        # Save
        #
        if nabu_config["output"]["location"] is not None:
            tasks.append("save")
            options["save"] = copy_dict_items(nabu_config["output"], list(nabu_config["output"].keys()))
            options["save"]["overwrite"] = nabu_config["output"]["overwrite_results"]

        self.processing_steps = tasks
        self.processing_options = options
        if set(self.processing_steps) != set(self.processing_options.keys()):
            raise ValueError("Something wrong with process_config: options do not correspond to steps")
        # Add check
        if set(self.processing_steps) != set(self.processing_options.keys()):
            raise ValueError("Something wrong when building processing steps")

    def _get_ctf_parameters(self, phase_options):
        dataset_info = self.dataset_info
        user_phase_options = self.nabu_config["phase"]

        ctf_geom = extract_parameters(user_phase_options["ctf_geometry"])
        ctf_advanced_params = extract_parameters(user_phase_options["ctf_advanced_params"])

        # z1_vh
        z1_v = ctf_geom["z1_v"]
        z1_h = ctf_geom["z1_h"]
        z1_vh = None
        if z1_h is None and z1_v is None:
            # parallel beam
            z1_vh = None
        elif (z1_v is None) ^ (z1_h is None):
            # only one is provided: source-sample distance
            z1_vh = z1_v or z1_h
        if z1_h is not None and z1_v is not None:
            # distance of the vertically focused source (horizontal line) and the horizontaly focused source (vertical line)
            # for KB mirrors
            z1_vh = (z1_v, z1_h)
        # pix_size_det
        pix_size_det = ctf_geom["detec_pixel_size"] or dataset_info.pixel_size * 1e-6
        # wavelength
        wavelength = 1.23984199e-9 / dataset_info.energy

        phase_options["ctf_geo_pars"] = {
            "z1_vh": z1_vh,
            "z2": phase_options["distance_m"],
            "pix_size_det": pix_size_det,
            "wavelength": wavelength,
            "magnification": bool(ctf_geom["magnification"]),
            "length_scale": ctf_advanced_params["length_scale"],
        }
        phase_options["ctf_lim1"] = ctf_advanced_params["lim1"]
        phase_options["ctf_lim2"] = ctf_advanced_params["lim2"]
        phase_options["ctf_normalize_by_mean"] = ctf_advanced_params["normalize_by_mean"]

    def _configure_save_steps(self, steps_to_save=None):
        self.steps_to_save = []
        self.dump_sinogram = False
        if steps_to_save is None:
            steps_to_save = self.nabu_config["pipeline"]["save_steps"]
            if steps_to_save in (None, ""):
                return
            steps_to_save = [s.strip() for s in steps_to_save.split(",")]
        for step in self.processing_steps:
            step = step.strip()
            if step in steps_to_save:
                self.processing_options[step]["save"] = True
                self.processing_options[step]["save_steps_file"] = self.get_save_steps_file(step_name=step)
        # "sinogram" is a special keyword, not explicitly in the processing steps
        if "sinogram" in steps_to_save:
            self.dump_sinogram = True
            self.dump_sinogram_file = self.get_save_steps_file(step_name="sinogram")
        self.steps_to_save = steps_to_save

    def _get_dump_file_and_h5_path(self):
        resume_from = self.resume_from_step
        process_file = self.get_save_steps_file(step_name=resume_from)
        if not os.path.isfile(process_file):
            self.logger.error("Cannot resume processing from step '%s': no such file %s" % (resume_from, process_file))
            return None, None
        h5_entry = self.dataset_info.hdf5_entry or "entry"
        process_h5_path = posixpath.join(h5_entry, resume_from, "results/data")
        if not hdf5_entry_exists(process_file, process_h5_path):
            self.logger.error("Could not find data in %s in file %s" % (process_h5_path, process_file))
            process_h5_path = None
        return process_file, process_h5_path

    def _configure_resume(self, resume_from=None):
        self.resume_from_step = None
        if resume_from is None:
            resume_from = self.nabu_config["pipeline"]["resume_from_step"]
            if resume_from in (None, ""):
                return
            resume_from = resume_from.strip(" ,;")
        self.resume_from_step = resume_from

        processing_steps = self.processing_steps
        # special case: resume from sinogram
        if resume_from == "sinogram":
            # disable up to 'reconstruction', not included
            if "sino_rings_correction" in processing_steps:
                # Sinogram destriping is done before building the half tomo sino.
                # Not sure if this is needed (i.e can we do before building the extended sino ?)
                # TODO find a more elegant way
                idx = processing_steps.index("sino_rings_correction")
            else:
                idx = processing_steps.index("reconstruction")
        #
        elif resume_from in processing_steps:
            idx = processing_steps.index(resume_from) + 1  # disable up to resume_from, included
        else:
            msg = "Cannot resume processing from step '%s': no such step in the current configuration" % resume_from
            self.logger.error(msg)
            self.resume_from_step = None
            return

        # Get corresponding file and h5 path
        process_file, process_h5_path = self._get_dump_file_and_h5_path()
        if process_file is None or process_h5_path is None:
            self.resume_from_step = None
            return
        dump_info = self._check_dump_file(process_file, raise_on_error=False)
        if dump_info is None:
            self.logger.error("Cannot resume from step %s: cannot use file %s" % (resume_from, process_file))
            self.resume_from_step = None
            return
        dump_start_z, dump_end_z = dump_info

        # Disable steps
        steps_to_disable = processing_steps[1:idx]
        self.logger.debug("Disabling steps %s" % str(steps_to_disable))
        for step_name in steps_to_disable:
            processing_steps.remove(step_name)
            self.processing_options.pop(step_name)

        # Update configuration
        self.logger.info("Processing will be resumed from step '%s' using file %s" % (resume_from, process_file))
        self._old_read_chunk = self.processing_options["read_chunk"]
        self.processing_options["read_chunk"] = {
            "process_file": process_file,
            "process_h5_path": process_h5_path,
            "step_name": resume_from,
            "dump_start_z": dump_start_z,
            "dump_end_z": dump_end_z,
        }
        # Dont dump a step if we resume from this step
        if resume_from in self.steps_to_save:
            self.logger.warning(
                "Processing is resumed from step '%s'. This step won't be dumped to a file" % resume_from
            )
            self.steps_to_save.remove(resume_from)
            if resume_from == "sinogram":
                self.dump_sinogram = False
            else:
                if resume_from in self.processing_options:  # should not happen
                    self.processing_options[resume_from].pop("save")

    def _check_dump_file(self, process_file, raise_on_error=False):
        """
        Return (start_z, end_z) on success
        Return None on failure
        """
        # Ensure data in the file correspond to what is currently asked
        if self.resume_from_step is None:
            return None

        # Check dataset shape/start_z/end_z
        rec_cfg_h5_path = posixpath.join(
            self.dataset_info.hdf5_entry or "entry",
            self.resume_from_step,
            "configuration/processing_options/reconstruction",
        )
        dump_start_z = get_h5_value(process_file, posixpath.join(rec_cfg_h5_path, "start_z"))
        dump_end_z = get_h5_value(process_file, posixpath.join(rec_cfg_h5_path, "end_z"))
        if dump_end_z < 0:
            dump_end_z += self.radio_shape(binning=False)[0]
        start_z, end_z = (
            self.processing_options["reconstruction"]["start_z"],
            self.processing_options["reconstruction"]["end_z"],
        )
        if not (dump_start_z <= start_z and end_z <= dump_end_z):
            msg = (
                "File %s was built with start_z=%d, end_z=%d but current configuration asks for start_z=%d, end_z=%d"
                % (process_file, dump_start_z, dump_end_z, start_z, end_z)
            )
            if not raise_on_error:
                self.logger.error(msg)
                return None
            self.logger.fatal(msg)
            raise ValueError(msg)

        # Check parameters other than reconstruction
        filedump_nabu_config = import_h5_to_dict(
            process_file,
            posixpath.join(self.dataset_info.hdf5_entry or "entry", self.resume_from_step, "configuration/nabu_config"),
        )
        sections_to_ignore = ["reconstruction", "output", "pipeline"]
        for section in sections_to_ignore:
            filedump_nabu_config[section] = self.nabu_config[section]
        # special case of the "save_steps process"
        # filedump_nabu_config["pipeline"]["save_steps"] = self.nabu_config["pipeline"]["save_steps"]

        diff = compare_dicts(filedump_nabu_config, self.nabu_config)
        if diff is not None:
            msg = "Nabu configuration in file %s differ from the current one: %s" % (process_file, diff)
            if not raise_on_error:
                self.logger.error(msg)
                return None
            self.logger.fatal(msg)
            raise ValueError(msg)
        #

        return (dump_start_z, dump_end_z)

    def get_save_steps_file(self, step_name=None):
        if self.nabu_config["pipeline"]["steps_file"] not in (None, ""):
            return self.nabu_config["pipeline"]["steps_file"]
        nabu_save_options = self.nabu_config["output"]
        output_dir = nabu_save_options["location"]
        file_prefix = step_name + "_" + nabu_save_options["file_prefix"]
        fname = os.path.join(output_dir, file_prefix) + ".hdf5"
        return fname
