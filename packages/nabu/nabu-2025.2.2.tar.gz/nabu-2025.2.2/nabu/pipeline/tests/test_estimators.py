import os
from tempfile import TemporaryDirectory
import pytest
import numpy as np
from pint import get_application_registry
from nxtomo import NXtomo
from nabu.testutils import utilstest, __do_long_tests__, get_data
from nabu.resources.dataset_analyzer import HDF5DatasetAnalyzer, analyze_dataset, ImageKey
from nabu.resources.nxflatfield import update_dataset_info_flats_darks
from nabu.resources.utils import extract_parameters
from nabu.pipeline.estimators import CompositeCOREstimator, TranslationsEstimator
from nabu.pipeline.config import parse_nabu_config_file
from nabu.pipeline.estimators import SinoCORFinder, CORFinder

from nabu.estimation.tests.test_motion_estimation import (
    check_motion_estimation,
    project_volume,
    _create_translations_vector,
)


#
# Test CoR estimation with "composite-coarse-to-fine" (aka "near" in the legacy system vocable)
#


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls

    dataset_downloaded_path = utilstest.getfile("test_composite_cor_finder_data.h5")
    cls.theta_interval = 4.5 * 1  # this is given. Radios in the middle of steps 4.5 degree long
    # are set to zero for compression
    # You can still change it to a multiple of 4.5
    cls.cor_pix = 1321.625
    cls.abs_tol = 0.0001
    cls.dataset_info = HDF5DatasetAnalyzer(dataset_downloaded_path)
    update_dataset_info_flats_darks(cls.dataset_info, True)
    cls.cor_options = extract_parameters("side=300.0;  near_width = 20.0", sep=";")


@pytest.mark.skipif(not (__do_long_tests__), reason="Need NABU_LONG_TESTS=1 for this test")
@pytest.mark.usefixtures("bootstrap")
class TestCompositeCorFinder:
    def test(self):
        cor_finder = CompositeCOREstimator(
            self.dataset_info, theta_interval=self.theta_interval, cor_options=self.cor_options
        )

        cor_position = cor_finder.find_cor()
        message = "Computed CoR %f " % cor_position + " and real CoR %f do not coincide" % self.cor_pix
        assert np.isclose(self.cor_pix, cor_position, atol=self.abs_tol), message


@pytest.fixture(scope="class")
def bootstrap_bamboo_reduced(request):
    cls = request.cls
    cls.abs_tol = 0.2
    # Dataset without estimated_cor_frm_motor (non regression test)
    dataset_relpath = os.path.join("bamboo_reduced.nx")
    dataset_downloaded_path = utilstest.getfile(dataset_relpath)
    conf_relpath = os.path.join("bamboo_reduced.conf")
    conf_downloaded_path = utilstest.getfile(conf_relpath)
    cls.ds_std = analyze_dataset(dataset_downloaded_path)
    update_dataset_info_flats_darks(cls.ds_std, True)
    cls.conf_std = parse_nabu_config_file(conf_downloaded_path)

    # Dataset with estimated_cor_frm_motor
    dataset_relpath = os.path.join("bamboo_reduced_bliss.nx")
    dataset_downloaded_path = utilstest.getfile(dataset_relpath)
    conf_relpath = os.path.join("bamboo_reduced_bliss.conf")
    conf_downloaded_path = utilstest.getfile(conf_relpath)
    cls.ds_bliss = analyze_dataset(dataset_downloaded_path)
    update_dataset_info_flats_darks(cls.ds_bliss, True)
    cls.conf_bliss = parse_nabu_config_file(conf_downloaded_path)


@pytest.mark.skipif(not (__do_long_tests__), reason="need environment variable NABU_LONG_TESTS=1")
@pytest.mark.usefixtures("bootstrap_bamboo_reduced")
class TestCorNearPos:
    # TODO adapt test file
    true_cor = 339.486 - 0.5

    def test_cor_sliding_standard(self):
        cor_options = extract_parameters(self.conf_std["reconstruction"].get("cor_options", None), sep=";")
        for side in [None, "from_file", "center"]:
            if side is not None:
                cor_options.update({"side": side})
            finder = CORFinder("sliding-window", self.ds_std, do_flatfield=True, cor_options=cor_options)
            cor = finder.find_cor()
            message = f"Computed CoR {cor} and expected CoR {self.true_cor} do not coincide. Near_pos options was set to {cor_options.get('near_pos',None)}."
            assert np.isclose(self.true_cor, cor, atol=self.abs_tol + 0.5), message  # FIXME

    def test_cor_fourier_angles_standard(self):
        cor_options = extract_parameters(self.conf_std["reconstruction"].get("cor_options", None), sep=";")
        # TODO modify test files
        if "near_pos" in cor_options and "near" in cor_options.get("side", "") == "near":
            cor_options["side"] = cor_options["near_pos"]
        #
        for side in [None, "from_file", "center"]:
            if side is not None:
                cor_options.update({"side": side})
            finder = SinoCORFinder("fourier-angles", self.ds_std, do_flatfield=True, cor_options=cor_options)
            cor = finder.find_cor()
            message = f"Computed CoR {cor} and expected CoR {self.true_cor} do not coincide. Near_pos options was set to {cor_options.get('near_pos',None)}."
            assert np.isclose(self.true_cor + 0.5, cor, atol=self.abs_tol), message

    def test_cor_sliding_bliss(self):
        cor_options = extract_parameters(self.conf_bliss["reconstruction"].get("cor_options", None), sep=";")
        # TODO modify test files
        if "near_pos" in cor_options and "near" in cor_options.get("side", "") == "near":
            cor_options["side"] = cor_options["near_pos"]
        #
        for side in [None, "from_file", "center"]:
            if side is not None:
                cor_options.update({"side": side})
            finder = CORFinder("sliding-window", self.ds_bliss, do_flatfield=True, cor_options=cor_options)
            cor = finder.find_cor()
            message = f"Computed CoR {cor} and expected CoR {self.true_cor} do not coincide. Near_pos options was set to {cor_options.get('near_pos',None)}."
            assert np.isclose(self.true_cor, cor, atol=self.abs_tol), message

    def test_cor_fourier_angles_bliss(self):
        cor_options = extract_parameters(self.conf_bliss["reconstruction"].get("cor_options", None), sep=";")
        for side in [None, "from_file", "center"]:
            if side is not None:
                cor_options.update({"side": side})
            finder = SinoCORFinder("fourier-angles", self.ds_bliss, do_flatfield=True, cor_options=cor_options)
            cor = finder.find_cor()
            message = f"Computed CoR {cor} and expected CoR {self.true_cor} do not coincide. Near_pos options was set to {cor_options.get('near_pos',None)}."
            assert np.isclose(self.true_cor + 0.5, cor, atol=self.abs_tol), message


def _add_fake_flats_and_dark_to_data(data, n_darks=10, n_flats=21, dark_val=1, flat_val=3):
    img_shape = data.shape[1:]
    # Use constant darks/flats, to avoid "reduction" (mean/median) issues
    fake_darks = np.ones((n_darks,) + img_shape, dtype=np.uint16) * dark_val
    fake_flats = np.ones((n_flats,) + img_shape, dtype=np.uint16) * flat_val
    return data * (fake_flats[0, 0, 0] - fake_darks[0, 0, 0]) + fake_darks[0, 0, 0], fake_darks, fake_flats


def _generate_nx_for_180_dataset(volume, output_file_path, n_darks=10, n_flats=21):

    n_angles = 250
    cor = -10

    alpha_x = 4
    beta_x = 3
    alpha_y = -5
    beta_y = 10
    beta_z = 0
    orig_det_dist = 0

    angles0 = np.linspace(0, np.pi, n_angles, False)
    return_angles = np.deg2rad([180.0, 135.0, 90.0, 45.0, 0.0])
    angles = np.hstack([angles0, return_angles]).ravel()
    a = np.arange(angles0.size + return_angles.size) / angles0.size

    tx = _create_translations_vector(a, alpha_x, beta_x)
    ty = _create_translations_vector(a, alpha_y, beta_y)
    tz = _create_translations_vector(a, 0, beta_z)

    sinos = project_volume(volume, angles, -tx, -ty, -tz, cor=-cor, orig_det_dist=orig_det_dist)
    data = np.moveaxis(sinos, 1, 0)

    sample_motion_xy = np.stack([-tx, ty], axis=1)
    sample_motion_z = -tz
    angles_deg = np.degrees(angles0)
    return_angles_deg = np.degrees(return_angles)
    n_return_radios = len(return_angles_deg)
    n_radios = data.shape[0] - n_return_radios

    ureg = get_application_registry()
    fake_raw_data, darks, flats = _add_fake_flats_and_dark_to_data(data, n_darks=n_darks, n_flats=n_flats)

    nxtomo = NXtomo()
    nxtomo.instrument.detector.data = np.concatenate(
        [
            darks,
            flats,
            fake_raw_data,  # radios + return radios (in float32 !)
        ]
    )
    image_key_control = np.concatenate(
        [
            [ImageKey.DARK_FIELD.value] * n_darks,
            [ImageKey.FLAT_FIELD.value] * n_flats,
            [ImageKey.PROJECTION.value] * n_radios,
            [ImageKey.ALIGNMENT.value] * n_return_radios,
        ]
    )
    nxtomo.instrument.detector.image_key_control = image_key_control

    rotation_angle = np.concatenate(
        [np.zeros(n_darks, dtype="f"), np.zeros(n_flats, dtype="f"), angles_deg, return_angles_deg]
    )
    nxtomo.sample.rotation_angle = rotation_angle * ureg.degree
    nxtomo.instrument.detector.field_of_view = "Full"
    nxtomo.instrument.detector.x_pixel_size = nxtomo.instrument.detector.y_pixel_size = 1 * ureg.micrometer
    nxtomo.save(file_path=output_file_path, data_path="entry", overwrite=True)

    return sample_motion_xy, sample_motion_z, cor


def _generate_nx_for_360_dataset(volume, output_file_path, n_darks=10, n_flats=21):

    n_angles = 250
    cor = -5.5

    alpha_x = -2
    beta_x = 7.0
    alpha_y = -2
    beta_y = 3
    beta_z = 100
    orig_det_dist = 0

    angles = np.linspace(0, 2 * np.pi, n_angles, False)
    a = np.linspace(0, 1, angles.size, endpoint=False)  # theta/theta_max

    tx = _create_translations_vector(a, alpha_x, beta_x)
    ty = _create_translations_vector(a, alpha_y, beta_y)
    tz = _create_translations_vector(a, 0, beta_z)

    sinos = project_volume(volume, angles, -tx, -ty, -tz, cor=-cor, orig_det_dist=orig_det_dist)
    data = np.moveaxis(sinos, 1, 0)

    sample_motion_xy = np.stack([-tx, ty], axis=1)
    sample_motion_z = -tz
    angles_deg = np.degrees(angles)

    ureg = get_application_registry()

    fake_raw_data, darks, flats = _add_fake_flats_and_dark_to_data(data, n_darks=n_darks, n_flats=n_flats)

    nxtomo = NXtomo()
    nxtomo.instrument.detector.data = np.concatenate([darks, flats, fake_raw_data])  # in float32 !

    image_key_control = np.concatenate(
        [
            [ImageKey.DARK_FIELD.value] * n_darks,
            [ImageKey.FLAT_FIELD.value] * n_flats,
            [ImageKey.PROJECTION.value] * data.shape[0],
        ]
    )
    nxtomo.instrument.detector.image_key_control = image_key_control

    rotation_angle = np.concatenate(
        [
            np.zeros(n_darks, dtype="f"),
            np.zeros(n_flats, dtype="f"),
            angles_deg,
        ]
    )
    nxtomo.sample.rotation_angle = rotation_angle * ureg.degree
    nxtomo.instrument.detector.field_of_view = "Full"
    nxtomo.instrument.detector.x_pixel_size = nxtomo.instrument.detector.y_pixel_size = 1 * ureg.micrometer
    nxtomo.save(file_path=output_file_path, data_path="entry", overwrite=True)

    return sample_motion_xy, sample_motion_z, cor


@pytest.fixture(scope="class")
def setup_test_motion_estimator(request):
    cls = request.cls
    cls.volume = get_data("motion/mri_volume_subsampled.npy")


@pytest.mark.skipif(not (__do_long_tests__), reason="need environment variable NABU_LONG_TESTS=1")
@pytest.mark.usefixtures("setup_test_motion_estimator")
class TestMotionEstimator:

    def _setup(self, tmpdir):
        # pytest uses some weird data structure for "tmpdir"
        if not (isinstance(tmpdir, str)):
            tmpdir = str(tmpdir)
        #
        if getattr(self, "volume", None) is None:
            self.volume = get_data("motion/mri_volume_subsampled.npy")

    # ruff: noqa: PT028
    def test_estimate_motion_360_dataset(self, tmpdir, verbose=False):
        self._setup(tmpdir)
        nx_file_path = os.path.join(tmpdir, "mri_projected_360_motion.nx")
        sample_motion_xy, sample_motion_z, cor = _generate_nx_for_360_dataset(self.volume, nx_file_path)

        dataset_info = analyze_dataset(nx_file_path)

        translations_estimator = TranslationsEstimator(
            dataset_info, do_flatfield=True, rot_center=cor, angular_subsampling=5, deg_xy=2, deg_z=2
        )
        estimated_shifts_h, estimated_shifts_v, estimated_cor = translations_estimator.estimate_motion()

        s = translations_estimator.angular_subsampling
        if verbose:
            translations_estimator.motion_estimator.plot_detector_shifts(cor=cor)
            translations_estimator.motion_estimator.plot_movements(
                cor=cor,
                angles_rad=dataset_info.rotation_angles[::s],
                gt_xy=sample_motion_xy[::s, :],
                gt_z=sample_motion_z[::s],
            )
        check_motion_estimation(
            translations_estimator.motion_estimator,
            dataset_info.rotation_angles[::s],
            cor,
            sample_motion_xy[::s, :],
            sample_motion_z[::s],
            fit_error_shifts_tol_vu=(0.2, 0.2),
            fit_error_det_tol_vu=(1e-5, 5e-2),
            fit_error_tol_xyz=(0.05, 0.05, 0.05),
            fit_error_det_all_angles_tol_vu=(1e-5, 0.05),
        )

    # ruff: noqa: PT028
    def test_estimate_motion_180_dataset(self, tmpdir, verbose=False):
        self._setup(tmpdir)
        nx_file_path = os.path.join(tmpdir, "mri_projected_180_motion.nx")

        sample_motion_xy, sample_motion_z, cor = _generate_nx_for_180_dataset(self.volume, nx_file_path)

        dataset_info = analyze_dataset(nx_file_path)

        translations_estimator = TranslationsEstimator(
            dataset_info,
            do_flatfield=True,
            rot_center=cor,
            angular_subsampling=2,
            deg_xy=2,
            deg_z=2,
            shifts_estimator="DetectorTranslationAlongBeam",
        )
        estimated_shifts_h, estimated_shifts_v, estimated_cor = translations_estimator.estimate_motion()

        if verbose:
            translations_estimator.motion_estimator.plot_detector_shifts(cor=cor)
            translations_estimator.motion_estimator.plot_movements(
                cor=cor,
                angles_rad=dataset_info.rotation_angles,
                gt_xy=sample_motion_xy[: dataset_info.n_angles],
                gt_z=sample_motion_z[: dataset_info.n_angles],
            )

        check_motion_estimation(
            translations_estimator.motion_estimator,
            dataset_info.rotation_angles,
            cor,
            sample_motion_xy,
            sample_motion_z,
            fit_error_shifts_tol_vu=(0.02, 0.1),
            fit_error_det_tol_vu=(1e-2, 0.5),
            fit_error_tol_xyz=(0.5, 2, 1e-2),
            fit_error_det_all_angles_tol_vu=(1e-2, 2),
        )


if __name__ == "__main__":

    T = TestMotionEstimator()
    with TemporaryDirectory(suffix="_motion", prefix="nabu_testdata") as tmpdir:
        T.test_estimate_motion_360_dataset(tmpdir, verbose=True)
        T.test_estimate_motion_180_dataset(tmpdir, verbose=True)
