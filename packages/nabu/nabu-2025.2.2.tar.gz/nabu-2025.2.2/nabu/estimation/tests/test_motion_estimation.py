from math import cos, sin
import numpy as np
from nabu.utils import search_sorted
from nabu.estimation.motion import MotionEstimation
from nabu.estimation.translation import estimate_shifts
from nabu.testutils import get_data, __do_long_tests__
from scipy.ndimage import shift
import pytest

try:
    import astra
except (ImportError, RuntimeError):
    astra = None


def test_estimate_shifts():
    image = get_data("chelsea.npz")["data"]
    n_tests = 10
    shift_min = -50
    shift_max = 50
    max_tol = 0.2  # in pixel unit
    shifts = np.random.rand(n_tests, 2) * (shift_max - shift_min) - shift_min
    for s in shifts:
        image_shifted = shift(image, s)
        estimated_shifts = estimate_shifts(image, image_shifted)
        abs_diff = np.abs(np.array(estimated_shifts) - np.array(s))
        assert np.all(abs_diff < max_tol), "Wrong estimation for shifts=%s : got %s" % (s, estimated_shifts)


def _bootstrap_test_motion_combined(cls):
    cls._fdesc = get_data("motion/test_correct_motion_combined.npz")
    cls.projs = cls._fdesc["projs"]
    cls.angles = cls._fdesc["angles_rad"]
    cls.shifts = cls._fdesc["shifts"]
    cls.cor = -2.81  # center of rotation in pixel units, (relative to the middle of the detector)
    if __do_long_tests__:
        cls._fdesc = get_data("motion/test_correct_motion_horizontal.npz")
        cls.projs_horiz = cls._fdesc["projs"]
        cls.angles_horiz = cls._fdesc["angles_rad"]
        cls.shifts_horiz = cls._fdesc["shifts"]
        cls._fdesc = get_data("motion/test_correct_motion_vertical.npz")
        cls.projs_vertic = cls._fdesc["projs"]
        cls.angles_vertic = cls._fdesc["angles_rad"]
        cls.shifts_vertic = cls._fdesc["shifts"]


@pytest.fixture(scope="class")
def bootstrap_test_motion_combined(request):
    cls = request.cls
    _bootstrap_test_motion_combined(cls)


# ruff: noqa: PT028
@pytest.mark.usefixtures("bootstrap_test_motion_combined")
class TestMotionEstimation:

    def _test_estimate_motion_360(
        self,
        projs,
        angles,
        reference_shifts,
        deg=2,
        deg_z=2,
        tol_x=1e-5,
        tol_y=1e-5,
        tol_z=1e-5,
        estimate_cor=False,
        verbose=True,
    ):
        """
        Test MotionEstimation using pairs of projs
        """
        n_a = projs.shape[0]
        projs1 = projs[: n_a // 2]
        projs2 = projs[n_a // 2 :]
        angles1 = angles[: n_a // 2]
        angles2 = angles[n_a // 2 :]
        estimator = MotionEstimation(projs1, projs2, angles1, angles2, shifts_estimator="DetectorTranslationAlongBeam")
        estimated_shifts_v = estimator.estimate_vertical_motion(degree=deg_z)
        cor = None if estimate_cor else self.cor
        estimated_shifts_h, cor_est = estimator.estimate_horizontal_motion(degree=deg, cor=cor)

        shifts = reference_shifts
        shifts_xy = -shifts[:, :2]
        shifts_z = -shifts[:, 2]

        # mind the signs, nabu vs RTK geometry
        abs_diff_x = np.max(np.abs(estimated_shifts_h[:, 0] - shifts_xy[:360, 0]))
        abs_diff_y = np.max(np.abs(estimated_shifts_h[:, 1] - shifts_xy[:360, 1]))
        abs_diff_z = np.max(np.abs(estimated_shifts_v - shifts_z[:360]))

        if verbose:
            estimator.plot_detector_shifts(cor=cor)
            estimator.plot_movements(cor=cor, angles_rad=angles, gt_xy=shifts_xy, gt_z=shifts_z)

        assert abs_diff_x < tol_x, "Wrong x-movement estimation (estimate_cor=%s)" % estimate_cor
        assert abs_diff_y < tol_y, "Wrong y-movement estimation (estimate_cor=%s)" % estimate_cor
        assert abs_diff_z < tol_z, "Wrong z-movement estimation (estimate_cor=%s)" % estimate_cor

    def test_estimate_motion_360(self, verbose=False):
        """
        Test with a synthetic dataset that underwent horizontal AND vertical translations
        """
        params_dict = {
            "estimate_cor": [False, True],
            "tol_x": [0.05, 0.1],
            "tol_y": [0.05, 0.2],
            "tol_z": [0.005, 0.01],
        }
        params_names = params_dict.keys()
        params_values = np.array(list(params_dict.values()), dtype="O")
        for i in range(params_values.shape[1]):
            params = {k: v for k, v in zip(params_names, params_values[:, i].tolist())}
            self._test_estimate_motion_360(
                self.projs[:360],
                self.angles[:360],
                self.shifts[:360],
                verbose=verbose,
                **params,
            )

    def test_estimate_motion_360_return(self, verbose=False):
        return_angles = np.deg2rad([360, 270, 180, 90, 0])
        outward_angles_indices = np.array([search_sorted(self.angles[:360], ra) for ra in return_angles])
        outward_angles = self.angles[outward_angles_indices]
        projs1 = self.projs[outward_angles_indices]
        projs2 = self.projs[-5:]

        estimator = MotionEstimation(
            projs1,
            projs2,
            outward_angles,
            return_angles,
            indices1=outward_angles_indices,
            indices2=np.arange(self.projs.shape[0])[-5:],
            n_projs_tot=self.projs.shape[0],
        )
        estimated_shifts_z = estimator.estimate_vertical_motion(degree=2)
        estimated_shifts_xy, c = estimator.estimate_horizontal_motion(degree=2, cor=self.cor)

        shifts = self.shifts
        gt_xy = -shifts[:, :2][:-5]
        gt_z = -shifts[:, 2][:-5]

        if verbose:
            estimator.plot_detector_shifts(cor=self.cor)
            estimator.plot_movements(cor=self.cor, angles_rad=self.angles[:-5], gt_xy=gt_xy, gt_z=gt_z)

        estimated_shifts_xy = estimator.apply_fit_horiz(angles=self.angles[:-5])
        estimated_shifts_z = estimator.apply_fit_vertic(angles=self.angles[:-5])

        abs_diff_x = np.max(np.abs(estimated_shifts_xy[:360, 0] - gt_xy[:360, 0]))
        abs_diff_y = np.max(np.abs(estimated_shifts_xy[:360, 1] - gt_xy[:360, 1]))
        abs_diff_z = np.max(np.abs(estimated_shifts_z[:360] - gt_z[:360]))

        max_fit_err_vu = estimator.get_max_fit_error(cor=self.cor)
        assert (
            max_fit_err_vu[0] < 0.7
        ), "Max difference between detector_v_shifts and fit(detector_v_shifts) is too high"  # can't do better for z estimation ?!
        assert (
            max_fit_err_vu[1] < 0.2
        ), "Max difference between detector_u_shifts and fit(detector_u_shifts) is too high"

        assert np.max(abs_diff_x) < 0.3, "Wrong x-movement estimation"
        assert np.max(abs_diff_y) < 0.5, "Wrong y-movement estimation"
        assert np.max(abs_diff_z) < 0.5, "Wrong z-movement estimation"


@pytest.fixture(scope="class")
def bootstrap_test_motion_estimation2(request):
    cls = request.cls
    cls.volume = get_data("motion/mri_volume_subsampled.npy")


def _create_translations_vector(a, alpha, beta):
    return alpha * a**2 + beta * a


def project_volume(vol, angles, tx, ty, tz, cor=0, orig_det_dist=0):
    """
    Forward-project a volume with translations (tx, ty, tz) of the sample
    """
    n_y, n_x, n_z = vol.shape
    vol_geom = astra.create_vol_geom(n_y, n_x, n_z)

    det_row_count = n_z
    det_col_count = max(n_y, n_x)

    vectors = np.zeros((len(angles), 12))
    for i in range(len(angles)):
        theta = angles[i]
        # ray direction
        vectors[i, 0] = sin(theta)
        vectors[i, 1] = -cos(theta)
        vectors[i, 2] = 0

        # center of detector
        vectors[i, 3] = (
            (cos(theta) ** 2) * tx[i] + cos(theta) * sin(theta) * ty[i] - orig_det_dist * sin(theta) + cos(theta) * cor
        )
        vectors[i, 4] = (
            sin(theta) * cos(theta) * tx[i] + (sin(theta) ** 2) * ty[i] + orig_det_dist * cos(theta) + sin(theta) * cor
        )
        vectors[i, 5] = tz[i]

        # vector from detector pixel (0,0) to (0,1)
        vectors[i, 6] = cos(theta)  # uX
        vectors[i, 7] = sin(theta)  # uY
        vectors[i, 8] = 0  # uZ

        # vector from detector pixel (0,0) to (1,0)
        vectors[i, 9] = 0
        vectors[i, 10] = 0
        vectors[i, 11] = 1

    proj_geom = astra.create_proj_geom("parallel3d_vec", det_row_count, det_col_count, vectors)

    sinogram_id, sinogram = astra.create_sino3d_gpu(vol, proj_geom, vol_geom)
    return sinogram


def check_motion_estimation(
    motion_estimator,
    angles,
    cor,
    gt_xy,
    gt_z,
    fit_error_shifts_tol_vu=(1e-5, 1e-5),
    fit_error_det_tol_vu=(1e-5, 1e-5),
    fit_error_tol_xyz=(1e-5, 1e-5, 1e-5),
    fit_error_det_all_angles_tol_vu=(1e-5, 1e-5),
):
    """
    Assess the fit quality of a MotionEstimation object, given known ground truth sample movements.

    Parameters
    ----------
    motion_estimator: MotionEstimation
        MotionEstimation object
    angles: numpy.ndarray
        Array containing rotation angles in radians. For 180° scan it must not contain the "return projections".
    cor: float
        Center of rotation
    gt_xy: numpy.ndarray
        Ground-truth sample movements in (x, y). Shape (n_angles, 2)
    gt_z: numpy.ndarray
        Ground-truth sample movements in z. Shape (n_angles,)
    fit_error_shifts_tol_vu: tuple of float
        Maximum error tolerance when assessing the fit of radios movements,
        i.e see how well the cross-correlation shifts between pairs of radios  are fitted
    fit_error_det_tol_vu: tuple of float
        Maximum error tolerance when assessing the sample movements fit on used angles, projected on the detector
    fit_error_tol_xyz: tuple of float
        Maximum error tolerance when assessing the fit of sample movements, in the sample domain
    fit_error_det_all_angles_tol_vu: tuple of float
        Maximum error tolerance when assessing the sample movements fit on ALL angles, projected on the detector
    """

    is_return = motion_estimator.is_return
    n_angles = angles.size
    outward_angles = motion_estimator.angles1
    return_angles = motion_estimator.angles1
    ma = lambda x: np.max(np.abs(x))
    outward_angles_indices = motion_estimator.indices1

    # (1) Check the fit in the detector domain, wrt measured shifts between pair of projs
    # ------------------------------------------------------------------------------------
    for fit_err, fit_max_error_tol, coord_name in zip(
        motion_estimator.get_max_fit_error(cor), fit_error_shifts_tol_vu, ["v", "u"]
    ):
        assert (
            fit_err < fit_max_error_tol
        ), f"Max error between (measured detector {coord_name}-shifts) and (estimated fit) is too high: {fit_err} > {fit_max_error_tol}"

    # (2) Check the fit wrt the ground truth motion projected onto detector
    # ----------------------------------------------------------------------
    shifts_vu = motion_estimator.apply_fit_to_get_detector_displacements(cor)
    if is_return:
        gt_shifts_vu_1 = motion_estimator.convert_sample_motion_to_detector_shifts(
            gt_xy[outward_angles_indices], gt_z[outward_angles_indices], outward_angles, cor=cor
        )
        gt_shifts_vu_2 = motion_estimator.convert_sample_motion_to_detector_shifts(
            gt_xy[n_angles:], gt_z[n_angles:], return_angles, cor=cor
        )
    else:
        gt_shifts_vu_1 = motion_estimator.convert_sample_motion_to_detector_shifts(
            gt_xy[: n_angles // 2], gt_z[: n_angles // 2], outward_angles, cor=cor
        )
        gt_shifts_vu_2 = motion_estimator.convert_sample_motion_to_detector_shifts(
            gt_xy[n_angles // 2 :], gt_z[n_angles // 2 :], outward_angles, cor=cor
        )
    gt_shifts_vu = gt_shifts_vu_2 - gt_shifts_vu_1
    if not (is_return):
        gt_shifts_vu[:, 1] += (
            2 * cor
        )  # when comparing pairs of opposits projs, delta_u = u(theta+) - u(theta) + 2*cor !

    err_max_vu = np.max(np.abs(gt_shifts_vu - shifts_vu), axis=0)
    assert (
        err_max_vu[0] < fit_error_det_tol_vu[0]
    ), f"Max difference of fit(used_angles) on 'v' coordinate is too high: {err_max_vu[0]} > {fit_error_det_tol_vu[0]}"
    assert (
        err_max_vu[1] < fit_error_det_tol_vu[1]
    ), f"Max difference of fit(used_angles) on 'u'' coordinate is too high: {err_max_vu[1]} > {fit_error_det_tol_vu[1]}"

    # (3) Check the fit wrt ground truth motion of the sample
    # This is less precise when using only return projections,
    # because the movements were estimated from the detector shifts between a few pairs of projections
    # Here apply the shift on all angles (above was only on the angles used to calculate the fit)
    # --------------------------------------------------------------------------------------------
    txy_est_all_angles = motion_estimator.apply_fit_horiz(angles=angles)
    tz_est_all_angles = motion_estimator.apply_fit_vertic(angles=angles)
    err_max_x = ma(txy_est_all_angles[:, 0] - gt_xy[:n_angles, 0])
    err_max_y = ma(txy_est_all_angles[:, 1] - gt_xy[:n_angles, 1])
    err_max_z = ma(tz_est_all_angles - gt_z[:n_angles])
    assert (
        err_max_x < fit_error_tol_xyz[0]
    ), f"Max error for x coordinate is too high: {err_max_x} > {fit_error_tol_xyz[0]}"
    assert (
        err_max_y < fit_error_tol_xyz[1]
    ), f"Max error for y coordinate is too high: {err_max_y} > {fit_error_tol_xyz[1]}"
    assert (
        err_max_z < fit_error_tol_xyz[2]
    ), f"Max error for z coordinate is too high: {err_max_z} > {fit_error_tol_xyz[2]}"

    # (4) Check the fit wrt ground truth motion, projected onto the detector, for all angles
    # ---------------------------------------------------------------------------------------
    estimated_shifts_vu_all_angles = motion_estimator.convert_sample_motion_to_detector_shifts(
        txy_est_all_angles, tz_est_all_angles, angles, cor=cor
    )
    gt_shifts_vu_all_angles = motion_estimator.convert_sample_motion_to_detector_shifts(
        gt_xy[:n_angles], gt_z[:n_angles], angles, cor=cor
    )
    err_max_vu_all_angles = np.max(np.abs(estimated_shifts_vu_all_angles - gt_shifts_vu_all_angles), axis=0)
    assert (
        err_max_vu_all_angles[0] < fit_error_det_all_angles_tol_vu[0]
    ), f"Max error of fit(all_angles) on 'v' coordinate is too high: {err_max_vu_all_angles[0]} > {fit_error_det_all_angles_tol_vu[0]}"
    assert (
        err_max_vu_all_angles[1] < fit_error_det_all_angles_tol_vu[1]
    ), f"Max error  of fit(all_angles) on 'u' coordinate is too high: {err_max_vu_all_angles[1]} > {fit_error_det_all_angles_tol_vu[1]}"


@pytest.mark.skipif(not (__do_long_tests__), reason="Need NABU_LONG_TESTS=1 for this test")
@pytest.mark.skipif(astra is None, reason="Need astra for this test")
@pytest.mark.usefixtures("bootstrap_test_motion_estimation2")
class TestMotionEstimationFromProjectedVolume:

    def test_180_with_return_projections(self, verbose=False):
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

        if not (hasattr(self, "volume")):
            self.volume = get_data("motion/mri_volume_subsampled.npy")
        sinos = project_volume(self.volume, angles, -tx, -ty, -tz, cor=-cor, orig_det_dist=orig_det_dist)
        radios = np.moveaxis(sinos, 1, 0)

        n_return_angles = return_angles.size
        projs_stack2 = radios[-n_return_angles:]
        outward_angles_indices = np.array([search_sorted(angles0, ra) for ra in return_angles])
        outward_angles = angles0[outward_angles_indices]
        projs_stack1 = radios[:-n_return_angles][outward_angles_indices]

        motion_estimator = MotionEstimation(
            projs_stack1,
            projs_stack2,
            outward_angles,
            return_angles,
            indices1=outward_angles_indices,
            indices2=np.arange(n_angles, n_angles + n_return_angles),
            shifts_estimator="DetectorTranslationAlongBeam",
        )
        motion_estimator.estimate_horizontal_motion(degree=2, cor=cor)
        motion_estimator.estimate_vertical_motion()

        gt_h = np.stack([-tx, ty], axis=1)
        gt_v = -tz
        if verbose:
            motion_estimator.plot_detector_shifts(cor=cor)
            motion_estimator.plot_movements(cor, angles_rad=angles0, gt_xy=gt_h[:n_angles], gt_z=gt_v[:n_angles])

        check_motion_estimation(
            motion_estimator,
            angles0,
            cor,
            gt_h,
            gt_v,
            fit_error_shifts_tol_vu=(0.01, 0.05),
            fit_error_det_tol_vu=(0.02, 0.5),
            fit_error_tol_xyz=(0.5, 1, 0.05),
            fit_error_det_all_angles_tol_vu=(0.02, 1),
        )

    def test_360(self, verbose=False):
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

        if not (hasattr(self, "volume")):
            self.volume = get_data("motion/mri_volume_subsampled.npy")

        sinos = project_volume(self.volume, angles, -tx, -ty, -tz, cor=-cor, orig_det_dist=orig_det_dist)
        radios = np.moveaxis(sinos, 1, 0)

        projs_stack1 = radios[: n_angles // 2]
        projs_stack2 = radios[n_angles // 2 :]
        angles1 = angles[: n_angles // 2]
        angles2 = angles[n_angles // 2 :]

        motion_estimator = MotionEstimation(
            projs_stack1, projs_stack2, angles1, angles2, shifts_estimator="phase_cross_correlation"
        )
        motion_estimator.estimate_horizontal_motion(degree=2, cor=cor)
        motion_estimator.estimate_vertical_motion()

        gt_xy = np.stack([-tx, ty], axis=1)
        gt_z = -tz

        if verbose:
            motion_estimator.plot_detector_shifts(cor=cor)
            motion_estimator.plot_movements(cor=cor, angles_rad=angles, gt_xy=gt_xy, gt_z=gt_z)

        check_motion_estimation(
            motion_estimator,
            angles,
            cor,
            gt_xy,
            gt_z,
            fit_error_shifts_tol_vu=(1e-5, 0.2),
            fit_error_det_tol_vu=(1e-5, 0.05),
            fit_error_tol_xyz=(0.1, 0.1, 1e-5),
            fit_error_det_all_angles_tol_vu=(1e-5, 0.1),
        )


if __name__ == "__main__":
    test1 = TestMotionEstimationFromProjectedVolume()
    test1.test_180_with_return_projections(verbose=True)
    test1.test_360(verbose=True)

    test2 = TestMotionEstimation()
    _bootstrap_test_motion_combined(test2)
    test2.test_estimate_motion_360(verbose=True)
    test2.test_estimate_motion_360_return(verbose=True)
