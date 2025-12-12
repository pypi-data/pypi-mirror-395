from enum import Enum
import os
import numpy as np
from silx.io.url import DataUrl
from silx.io import get_data
from tomoscan import __version__ as __tomoscan_version__
from tomoscan.esrf.scan.edfscan import EDFTomoScan
from tomoscan.esrf.scan.nxtomoscan import NXtomoScan
from packaging.version import parse as parse_version

from ..utils import BaseClassError, check_supported, indices_to_slices, is_scalar, search_sorted
from ..io.reader import EDFStackReader, NXDarksFlats, NXTomoReader
from ..io.utils import get_compacted_dataslices
from .utils import get_values_from_file, is_hdf5_extension
from .logger import LoggerOrPrint

from ..pipeline.utils import nabu_env_settings


# We could import the 1000+ LoC  nxtomo.nxobject.nxdetector.ImageKey... or we can do this
class ImageKey(Enum):
    ALIGNMENT = -1
    PROJECTION = 0
    FLAT_FIELD = 1
    DARK_FIELD = 2
    INVALID = 3


# ---

_image_type = {
    "projections": ImageKey.PROJECTION.value,
    "projection": ImageKey.PROJECTION.value,
    "radios": ImageKey.PROJECTION.value,
    "radio": ImageKey.PROJECTION.value,
    "flats": ImageKey.FLAT_FIELD.value,
    "flat": ImageKey.FLAT_FIELD.value,
    "darks": ImageKey.DARK_FIELD.value,
    "dark": ImageKey.DARK_FIELD.value,
    "static": ImageKey.ALIGNMENT.value,
    "alignment": ImageKey.ALIGNMENT.value,
    "return": ImageKey.ALIGNMENT.value,
    "invalid": ImageKey.INVALID.value,
}


class DatasetAnalyzer:
    _scanner = None
    kind = "none"

    """
    Base class for datasets analyzers.
    """

    def __init__(self, location, extra_options=None, logger=None):
        """
        Initialize a Dataset analyzer.

        Parameters
        ----------
        location: str
            Dataset location (directory or file name)
        extra_options: dict, optional
            Extra options on how to interpret the dataset.
        logger: logging object, optional
            Logger. If not set, messages will just be printed in stdout.
        """
        self.logger = LoggerOrPrint(logger)
        self.location = location
        self._set_extra_options(extra_options)
        self._get_excluded_projections()
        self._set_default_dataset_values()
        self._init_dataset_scan()
        self._finish_init()

    def _set_extra_options(self, extra_options):
        if extra_options is None:
            extra_options = {}
        # COMPAT.
        advanced_options = {
            "force_flatfield": False,
            "output_dir": None,
            "exclude_projections": None,
            "hdf5_entry": None,
            # "nx_version": 1.0,
        }
        # --
        advanced_options.update(extra_options)
        self.extra_options = advanced_options

    # pylint: disable=E1136
    def _get_excluded_projections(self):
        excluded_projs = self.extra_options["exclude_projections"]
        self._ignore_projections = None
        if excluded_projs is None:
            return

        if excluded_projs["type"] == "angular_range":
            excluded_projs["type"] = "range"  # compat with tomoscan #pylint: disable=E1137
            values = excluded_projs["range"]
        for ignore_kind, dtype in {"indices": np.int32, "angles": np.float32}.items():
            if excluded_projs["type"] == ignore_kind:
                values = get_values_from_file(excluded_projs["file"], any_size=True).astype(dtype).tolist()
        self._ignore_projections = {"kind": excluded_projs["type"], "values": values}  # pylint: disable=E0606

    def _init_dataset_scan(self, **kwargs):
        if self._scanner is None:
            raise ValueError("Base class")
        if self._scanner is NXtomoScan:
            if self.extra_options.get("hdf5_entry", None) is not None:
                kwargs["entry"] = self.extra_options["hdf5_entry"]
            if self.extra_options.get("nx_version", None) is not None:
                kwargs["nx_version"] = self.extra_options["nx_version"]
        if self._scanner is EDFTomoScan:
            # Assume 1 frame per file (otherwise too long to open each file)
            kwargs["n_frames"] = 1

        self.dataset_scanner = self._scanner(  # pylint: disable=E1102
            self.location, ignore_projections=self._ignore_projections, **kwargs
        )

        if self._ignore_projections is not None:
            self.logger.info("Excluding projections: %s" % str(self._ignore_projections))

        if nabu_env_settings.skip_tomoscan_checks:
            self.logger.warning(
                " WARNING: according to nabu_env_settings.skip_tomoscan_checks, skipping virtual layout integrity check of tomoscan which is time consuming"
            )
            self.dataset_scanner.set_check_behavior(run_check=False, raise_error=False)

        self.raw_flats = self.dataset_scanner.flats
        self.raw_darks = self.dataset_scanner.darks
        self.n_angles = len(self.dataset_scanner.projections)
        self.radio_dims = (self.dataset_scanner.dim_1, self.dataset_scanner.dim_2)
        self._radio_dims_notbinned = self.radio_dims  # COMPAT
        self._flip_lr = getattr(self.dataset_scanner, "detector_is_lr_flip", False)
        self._flip_ud = getattr(self.dataset_scanner, "detector_is_ud_flip", False)

    def _finish_init(self):
        pass

    def _set_default_dataset_values(self):
        self._detector_tilt = None
        self.translations = None
        self.ctf_translations = None
        self.axis_position = None
        self._rotation_angles = None
        self.z_per_proj = None
        self.x_per_proj = None
        self._energy = None
        self._pixel_size = None
        self._distance = None
        self._flats_srcurrent = None
        self._projections = None
        self._projections_srcurrent = None
        self._reduced_flats = None
        self._reduced_darks = None

    @property
    def energy(self):
        """
        Return the energy in kev.
        """
        if self._energy is None:
            self._energy = self.dataset_scanner.energy
        return self._energy

    @energy.setter
    def energy(self, val):
        self._energy = val

    @property
    def distance(self):
        """
        Return the sample-detector distance in meters.
        """
        if self._distance is None:
            if parse_version(__tomoscan_version__) < parse_version("2.2"):
                self._distance = abs(self.dataset_scanner.distance)
            else:
                self._distance = abs(self.dataset_scanner.sample_detector_distance)
        return self._distance

    @distance.setter
    def distance(self, val):
        self._distance = val

    @property
    def pixel_size(self):
        """
        Return the pixel size in microns.
        """
        # TODO X and Y pixel size
        if self._pixel_size is None:
            self._pixel_size = self.dataset_scanner.pixel_size * 1e6
        return self._pixel_size

    @pixel_size.setter
    def pixel_size(self, val):
        self._pixel_size = val

    def _get_rotation_angles(self):
        return self._rotation_angles  # None by default

    @property
    def rotation_angles(self):
        """
        Return the rotation angles in radians.
        """
        return self._get_rotation_angles()

    @rotation_angles.setter
    def rotation_angles(self, angles):
        self._rotation_angles = angles

    def _is_halftomo(self):
        return None  # base class

    @property
    def is_halftomo(self):
        """
        Indicates whether the current dataset was performed with half acquisition.
        """
        return self._is_halftomo()

    @property
    def detector_tilt(self):
        """
        Return the detector tilt in degrees
        """
        return self._detector_tilt

    @detector_tilt.setter
    def detector_tilt(self, tilt):
        self._detector_tilt = tilt

    def _get_srcurrent(self, frame_type):
        # To be implemented by inheriting class
        return None

    @property
    def projections(self):
        if self._projections is None:
            self._projections = self.dataset_scanner.projections
        return self._projections

    @projections.setter
    def projections(self, val):
        raise ValueError

    @property
    def projections_srcurrent(self):
        """
        Return the synchrotron electric current for each projection.
        """
        if self._projections_srcurrent is None:
            self._projections_srcurrent = self._get_srcurrent("radios")  # pylint: disable=E1128
        return self._projections_srcurrent

    @projections_srcurrent.setter
    def projections_srcurrent(self, val):
        self._projections_srcurrent = val

    @property
    def flats_srcurrent(self):
        """
        Return the synchrotron electric current for each flat image.
        """
        if self._flats_srcurrent is None:
            self._flats_srcurrent = self._get_srcurrent("flats")  # pylint: disable=E1128
        return self._flats_srcurrent

    @flats_srcurrent.setter
    def flats_srcurrent(self, val):
        self._flats_srcurrent = val

    def check_defined_attribute(self, name, error_msg=None):
        """
        Utility function to check that a given attribute is defined.
        """
        if getattr(self, name, None) is None:
            raise ValueError(error_msg or str("No information on %s was found in the dataset" % name))

    @property
    def flats(self):
        """
        Return the REDUCED flat-field images. Either by reducing (median) the raw flats, or a user-defined reduced flats.
        """
        if self._reduced_flats is None:
            self._reduced_flats = self.get_reduced_flats()
        return self._reduced_flats

    @flats.setter
    def flats(self, val):
        self._reduced_flats = val

    @property
    def darks(self):
        """
        Return the REDUCED flat-field images. Either by reducing (mean) the raw darks, or a user-defined reduced darks.
        """
        if self._reduced_darks is None:
            self._reduced_darks = self.get_reduced_darks()
        return self._reduced_darks

    @darks.setter
    def darks(self, val):
        self._reduced_darks = val

    @property
    def scan_basename(self):
        raise BaseClassError

    @property
    def scan_dirname(self):
        raise BaseClassError

    def get_alignment_projections(self, image_sub_region=None):
        raise NotImplementedError

    @property
    def all_angles(self):
        raise NotImplementedError

    def get_frame(self, idx): ...

    @property
    def is_360(self):
        """
        Return True iff the scan is 360 degrees (regardless of half-tomo mode)
        """
        angles = self.rotation_angles
        delta_theta = abs(angles.max() - angles.min())
        return abs(delta_theta - 2 * np.pi) < abs(delta_theta - np.pi)

    @property
    def flip_frame_lr(self):
        """
        Return True if frames should be flipped left<->right upon reading
        """
        return self._flip_lr

    @property
    def flip_frame_ud(self):
        """
        Return True if frames should be flipped left<->right upon reading
        """
        return self._flip_ud

    @flip_frame_lr.setter
    def flip_frame_lr(self, val):
        self._flip_lr = val

    @flip_frame_ud.setter
    def flip_frame_ud(self, val):
        self._flip_ud = val


class EDFDatasetAnalyzer(DatasetAnalyzer):
    """
    EDF Dataset analyzer for legacy ESRF acquisitions
    """

    _scanner = EDFTomoScan
    kind = "edf"

    def _finish_init(self):
        pass

    def _get_flats_darks(self):
        return

    @property
    def hdf5_entry(self):
        """
        Return the HDF5 entry of the current dataset.
        Not applicable for EDF (return None)
        """
        return None

    def _is_halftomo(self):
        return None

    def _get_rotation_angles(self):
        return np.deg2rad(self.dataset_scanner.rotation_angle())

    def get_reduced_flats(self, **reader_kwargs):
        if self.raw_flats in [None, {}]:
            raise FileNotFoundError("No reduced flat ('refHST') found in %s" % self.location)
        # A few notes:
        # (1) In principle we could do the reduction (mean/median) from raw frames (ref_xxxx_yyyy)
        #   but for legacy datasets it's always already done (by fasttomo3), and EDF support is supposed to be dropped on our side
        # (2) We use EDFStackReader class to handle the possible additional data modifications
        #  (eg. subsampling, binning, distortion correction...)
        # (3) The following spawns one reader instance per file, which is not elegant,
        #   but in principle there are typically 1-2 reduced flats in a scan
        readers = {k: EDFStackReader([self.raw_flats[k].file_path()], **reader_kwargs) for k in self.raw_flats}
        return {k: readers[k].load_data()[0] for k in self.raw_flats}

    def get_reduced_darks(self, **reader_kwargs):
        # See notes in get_reduced_flats() above
        if self.raw_darks in [None, {}]:
            raise FileNotFoundError("No reduced dark ('darkend.edf' or 'dark.edf') found in %s" % self.location)
        readers = {k: EDFStackReader([self.raw_darks[k].file_path()], **reader_kwargs) for k in self.raw_darks}
        return {k: readers[k].load_data()[0] for k in self.raw_darks}

    @property
    def files(self):
        return sorted([u.file_path() for u in self.dataset_scanner.projections.values()])

    def get_reader(self, **kwargs):
        return EDFStackReader(self.files, **kwargs)

    @property
    def scan_basename(self):
        # os.path.basename(self.dataset_scanner.path)
        return self.dataset_scanner.get_dataset_basename()

    @property
    def scan_dirname(self):
        return self.dataset_scanner.path

    def get_excluded_projections_indices(self, including_other_frames_types=True):
        if not (including_other_frames_types):
            raise NotImplementedError
        return self.dataset_scanner.get_ignored_projection_indices()


class HDF5DatasetAnalyzer(DatasetAnalyzer):
    """
    HDF5 dataset analyzer
    """

    _scanner = NXtomoScan
    kind = "nx"

    @property
    def z_translation(self):
        raw_data = np.array(self.dataset_scanner.z_translation)
        projs_idx = np.array(list(self.projections.keys()))
        filtered_data = raw_data[projs_idx]
        return 1.0e6 * filtered_data / self.pixel_size

    @property
    def x_translation(self):
        raw_data = np.array(self.dataset_scanner.x_translation)
        projs_idx = np.array(list(self.projections.keys()))
        filtered_data = raw_data[projs_idx]
        return 1.0e6 * filtered_data / self.pixel_size

    def _get_rotation_angles(self):
        if self._rotation_angles is None:
            angles = np.array(self.dataset_scanner.rotation_angle)
            projs_idx = np.array(list(self.projections.keys()))
            angles = angles[projs_idx]
            self._rotation_angles = np.deg2rad(angles)
        return self._rotation_angles

    def _get_dataset_hdf5_url(self):
        if len(self.projections) > 0:
            frames_to_take = self.projections
        elif len(self.raw_flats) > 0:
            frames_to_take = self.raw_flats
        elif len(self.raw_darks) > 0:
            frames_to_take = self.raw_darks
        else:
            raise ValueError("No projections, no flats and no darks ?!")
        first_proj_idx = sorted(frames_to_take.keys())[0]
        first_proj_url = frames_to_take[first_proj_idx]
        return DataUrl(
            file_path=first_proj_url.file_path(), data_path=first_proj_url.data_path(), data_slice=None, scheme="silx"
        )

    @property
    def dataset_hdf5_url(self):
        return self._get_dataset_hdf5_url()

    @property
    def hdf5_entry(self):
        """
        Return the HDF5 entry of the current dataset
        """
        return self.dataset_scanner.entry

    def _is_halftomo(self):
        try:
            is_halftomo = self.dataset_scanner.field_of_view.value.lower() == "half"
        except:
            is_halftomo = None
        return is_halftomo

    def get_data_slices(self, what):
        """
        Return indices in the data volume where images correspond to a given kind.

        Parameters
        ----------
        what: str
            Which keys to get. Can be "projections", "flats", "darks"

        Returns
        --------
        slices: list of slice
            A list where each item is a slice.
        """
        name_to_attr = {
            "projections": self.projections,
            "flats": self.raw_flats,
            "darks": self.raw_darks,
        }
        check_supported(what, name_to_attr.keys(), "image type")
        images = name_to_attr[what]  # dict
        # we can't directly use set() on slice() object (unhashable). Use tuples
        slices = set()
        for du in get_compacted_dataslices(images).values():
            if du.data_slice() is not None:
                # note: du.data_slice is a uint in recent tomoscan version
                s = (int(du.data_slice().start), int(du.data_slice().stop))
            else:
                s = None
            slices.add(s)
        slices_list = [slice(item[0], item[1]) if item is not None else None for item in list(slices)]
        return slices_list

    def _select_according_to_frame_type(self, data, frame_type):
        if data is None:
            return None
        return data[self.dataset_scanner.image_key_control == _image_type[frame_type]]

    def get_reduced_flats(self, method="median", force_reload=False, **reader_kwargs):
        dkrf_reader = NXDarksFlats(
            self.dataset_hdf5_url.file_path(), data_path=self.dataset_hdf5_url.data_path(), **reader_kwargs
        )
        return dkrf_reader.get_reduced_flats(method=method, force_reload=force_reload, as_dict=True)

    def get_reduced_darks(self, method="mean", force_reload=False, **reader_kwargs):
        dkrf_reader = NXDarksFlats(
            self.dataset_hdf5_url.file_path(), data_path=self.dataset_hdf5_url.data_path(), **reader_kwargs
        )
        return dkrf_reader.get_reduced_darks(method=method, force_reload=force_reload, as_dict=True)

    def _get_srcurrent(self, frame_type):
        return self._select_according_to_frame_type(self.dataset_scanner.machine_current, frame_type)

    def frames_slices(self, frame_type):
        """
        Return a list of slice objects corresponding to the data corresponding to "frame_type".
        For example, if the dataset flats are located at indices [1, 2, ..., 99], then
        frame_slices("flats") will return [slice(0, 100)].
        """
        return indices_to_slices(np.where(self.dataset_scanner.image_key_control == _image_type[frame_type])[0])

    def get_reader(self, **kwargs):
        return NXTomoReader(self.dataset_hdf5_url.file_path(), data_path=self.dataset_hdf5_url.data_path(), **kwargs)

    @property
    def scan_basename(self):
        # os.path.splitext(os.path.basename(self.dataset_hdf5_url.file_path()))[0]
        return self.dataset_scanner.get_dataset_basename()

    @property
    def scan_dirname(self):
        # os.path.dirname(di.dataset_hdf5_url.file_path())
        return self.dataset_scanner.path

    def get_alignment_projections(self, image_sub_region=None):
        """
        Get the extra projections (if any) that are used as "reference projections" for alignment.
        For certain scan, when completing a (half) turn, sometimes extra projections are acquired for alignment purpose.

        Returns
        -------
        projs: numpy.ndarray
            Array with shape (n_projections, n_y, n_x)
        angles: numpy.ndarray
            Corresponding angles in degrees
        indices:
            Indices of projections
        """
        sub_region = None
        if image_sub_region is not None:
            sub_region = (None,) + image_sub_region
        reader = self.get_reader(image_key=ImageKey.ALIGNMENT.value, sub_region=sub_region)
        projs = reader.load_data()
        indices = reader.get_frames_indices()
        angles = get_angle_at_index(self.all_angles, indices)
        return projs, angles, indices

    @property
    def all_angles(self):
        return np.array(self.dataset_scanner.rotation_angle)

    def get_index_from_angle(self, angle, image_key=0, return_found_angle=False):
        """
        Return the index of the image taken at rotation angle 'angle'.
        By default look at the projections, i.e image_key = 0
        """
        all_angles = self.all_angles
        all_indices = np.arange(len(all_angles))
        all_image_key = self.dataset_scanner.image_key_control

        idx2 = np.where(all_image_key == image_key)[0]
        angles = all_angles[idx2]
        idx_angles_sorted = np.argsort(angles)
        angles_sorted = angles[idx_angles_sorted]

        pos = search_sorted(angles_sorted, angle)
        # this gives a position in "idx2", but we need the position in "all_indices"
        idx = all_indices[idx2[idx_angles_sorted[pos]]]
        if return_found_angle:
            return idx, angles_sorted[pos]
        return idx

    def get_image_at_angle(self, angle_deg, image_type="projection", sub_region=None, return_angle_and_index=False):
        image_key = _image_type[image_type]
        idx, angle_found = self.get_index_from_angle(angle_deg, image_key=image_key, return_found_angle=True)

        # Option 1:
        if sub_region is None:
            sub_region = (None, None)
        # Convert absolute index to index of image_key
        idx2 = np.searchsorted(np.where(self.dataset_scanner.image_key_control == image_key)[0], idx)
        sub_region = (slice(idx2, idx2 + 1),) + sub_region
        reader = self.get_reader(image_key=image_key, sub_region=sub_region)
        img = reader.load_data()[0]
        if return_angle_and_index:
            return img, angle_found, idx
        return img

        # Option 2:
        # return self.get_frame(idx)
        # something like:
        # [fr for fr in self.dataset_scanner.frames if fr.image_key.value == 0 and fr.rotation_angle == 180 and fr._is_control_frame is False]

    def get_frame(self, idx):
        return get_data(self.dataset_scanner.frames[idx].url)

    def get_frames_indices(self, frame_type):
        return self._select_according_to_frame_type(np.arange(self.dataset_scanner.image_key_control.size), frame_type)

    def index_to_proj_number(self, proj_index):
        """
        Return the projection *number*, from its frame *index*.

        For example if there are 11 flats before projections,
        then projections will have indices [11, 12, .....] (possibly not contiguous)
        while their number is [0, 1, ..., ] (contiguous, starts from 0)
        """
        all_projs_indices = self.get_frames_indices("projection")
        return search_sorted(all_projs_indices, proj_index)

    def get_excluded_projections_indices(self, including_other_frames_types=True):
        # Get indices of ALL projections (even excluded ones)
        # the index accounts for flats/darks !
        # Get indices of excluded projs (again, accounting for flats/darks)
        ignored_projs_indices = self.dataset_scanner.get_ignored_projection_indices()
        ignored_projs_indices = [
            idx for idx in ignored_projs_indices if self.dataset_scanner.frames[idx].is_control is False
        ]
        if including_other_frames_types:
            return ignored_projs_indices
        # Get indices of excluded projs, now relative to the pure projections stack
        ignored_projs_indices_rel = [
            self.index_to_proj_number(ignored_proj_idx_abs) for ignored_proj_idx_abs in ignored_projs_indices
        ]
        return ignored_projs_indices_rel


def get_angle_at_index(all_angles, index):
    """
    Return the rotation angle corresponding to image index 'index'
    """
    if is_scalar(index):
        return all_angles[index]
    else:
        return all_angles[np.array(index)]


def get_radio_pair(dataset_info, radio_angles: tuple, return_indices=False):
    """
    Get closest radios at radio_angles[0] and radio_angles[1]
    angles must be in angles

    Parameters
    ----------
    dataset_info: `DatasetAnalyzer` instance
        Data structure with the dataset information
    radio_angles: tuple
        tuple of two elements: angles (in radian) to get
    return_indices: bool, optional
        Whether to return radios indices along with the radios array.

    Returns
    -------
    res: array or tuple
        If return_indices is True, return a tuple (radios, indices).
        Otherwise, return an array with the radios.
    """
    if not (isinstance(radio_angles, tuple) and len(radio_angles) == 2):
        raise TypeError("radio_angles should be a tuple of two elements.")
    if not isinstance(radio_angles[0], (np.floating, float)) or not isinstance(radio_angles[1], (np.floating, float)):
        raise TypeError(
            f"radio_angles should be float. Get {type(radio_angles[0])} and {type(radio_angles[1])} instead"
        )

    radios_indices = []
    radios_indices = sorted(dataset_info.projections.keys())
    angles = dataset_info.rotation_angles
    angles = angles - angles.min()
    i_radio_1 = np.argmin(np.abs(angles - radio_angles[0]))
    i_radio_2 = np.argmin(np.abs(angles - radio_angles[1]))
    radios_indices = [radios_indices[i_radio_1], radios_indices[i_radio_2]]
    n_radios = 2
    radios = np.zeros((n_radios,) + dataset_info.radio_dims[::-1], "f")
    for i in range(n_radios):
        radio_idx = radios_indices[i]
        radios[i] = get_data(dataset_info.projections[radio_idx]).astype("f")
    if return_indices:
        return radios, radios_indices
    else:
        return radios


def analyze_dataset(dataset_path, extra_options=None, logger=None):
    if not (os.path.isdir(dataset_path)):
        if not (os.path.isfile(dataset_path)):
            raise ValueError("Error: %s no such file or directory" % dataset_path)
        if not (is_hdf5_extension(os.path.splitext(dataset_path)[-1].replace(".", ""))):
            raise ValueError("Error: expected a HDF5 file")
        dataset_analyzer_class = HDF5DatasetAnalyzer
    else:  # directory -> assuming EDF
        dataset_analyzer_class = EDFDatasetAnalyzer
    dataset_structure = dataset_analyzer_class(dataset_path, extra_options=extra_options, logger=logger)
    return dataset_structure
