import os
import logging
from enum import Enum
from multiprocessing.pool import ThreadPool
from warnings import warn
import numpy as np
from ..pipeline.config_validators import convert_to_bool
from ..utils import check_supported, get_num_threads, is_scalar

try:
    from skimage.registration import phase_cross_correlation
except ImportError:
    phase_cross_correlation = None
from .translation import DetectorTranslationAlongBeam as RadiosShiftEstimator, estimate_shifts

plt = None
disable_matplotlib = convert_to_bool(os.environ.get("NABU_DISABLE_MATPLOTLIB", "0"))[0]
if not (disable_matplotlib):
    try:
        import matplotlib.pyplot as plt

        __have_matplotlib__ = True
    except ImportError:
        logging.getLogger(__name__).warning("Matplotlib not available or disabled. Plotting disabled")


class PairType(Enum):
    OPPOSITE = 1
    RETURN = 0


class MotionEstimation:
    """
    A class for estimating rigid sample motion during acquisition.
    The motion is estimated by
       1. Measuring the translations between radios (either opposite radios for 360-degrees scan ; or "reference radios")
       2. Fitting these measured translations with a displacement model.

    For (1), there are various available functions to estimate the shift between projections.
    The workhorse is phase cross-correlation, but this class allows to use other functions.
    For (2), you can pick several displacement model. The default one is a low-degree polynomial.

    Once the displacement model is computed, you have the displacement in sample reference frame,
    and you can "project" these displacements in the detector reference frame.
    Having the displacements converted as detector shifts allows you to
      (a) assess the fit between displacement model, and measured detector shifts
      (b) get a list movements to correct during reconstruction, vertical and/or horizontal.
          In nabu pipeline, this is handled by "translation_movements_file" in [reconstruction] section.
    """

    _shifts_estimators_default_kwargs = {
        "phase_cross_correlation": {"upsample_factor": 10, "overlap_ratio": 0.3},
        "DetectorTranslationAlongBeam": {"peak_fit_radius": 10, "padding_mode": "edge"},
        "estimate_shifts": {},
    }

    def __init__(
        self,
        projs_stack1,
        projs_stack2,
        angles1_rad,
        angles2_rad,
        indices1=None,
        indices2=None,
        n_projs_tot=None,
        n_calc_threads=None,
        reference="begin",
        shifts_estimator="phase_cross_correlation",
        shifts_estimator_kwargs=None,
    ):
        """
        Parameters
        ----------
        projs_stack1: numpy.ndarray
            Stack of projections, with shape (n_projs, n_rows, n_cols).
            It has to be of the same shape as 'projs_stack2'.
            Projection number 'i' in 'projs_stack1' will be compared with projection number 'i' in 'projs_stack2'
        projs_stack2: numpy.ndarray
            Stack of projections, with shape (n_projs, n_rows, n_cols).
            It has to be of the same shape as 'projs_stack1'.
            Projection number 'i' in 'projs_stack1' will be compared with projection number 'i' in 'projs_stack2'
        angles1_rad: numpy.ndarray or list of float
            Angles (in radians) of each projection, i.e, projection number 'i' in 'projs_stack1' was acquired at angle theta=angles1_rad[i]
        angles2_rad: numpy.ndarray or list of float
            Angles (in radians) of each projection, i.e, projection number 'i' in 'projs_stack2' was acquired at angle theta=angles2_rad[i]
        indices1: numpy.ndarray or list of int, optional
            Indices corresponding to each projection in 'projs_stack1'.
            It is used to calculate the curvilinear coordinate for the fit.
        indices2: numpy.ndarray or list of int, optional
            Indices corresponding to each projection in 'projs_stack2'.
            It is used to calculate the curvilinear coordinate for the fit.
            It is mostly important if projections in 'projs_stack2' are "return projections" (see Notes below for what this means)
        n_calc_threads: int, optional
            Number of threads to use for calculating phase cross correlation on pairs of images.
            Default is to use all available threads.

        Notes
        -----
        "Return projections" is the name of extra projections that might be acquired at the end of the scan.
        For example, for a 180-degrees scan with rotation angles [0, ..., 179.8], extra projections can be saved
        at angles [180, 90, 0]  (the rotation stage rewinds to its original angular position).
        These extra projection serve to check whether the sample/stage moved during the scan.
        In this case, angles2_rad = np.radians([180, 90, 0]).

        This class works by fitting the measured displacements (in detector space) with a model.
        This model uses a "normalized coordinate" built upon projection angles & indices.
        Each pair of radios (projs_stack1[i], projs_stack2[i]) has angles (angles1_rad[i], angles2_rad[i])
        and normalized coordinates (a1[i], a2[i])
        where a1 = normalize_coordinates(angles1_rad) and a2 = normalize_coordinates(angles2_rad)
        """
        self._set_projs_pairs(projs_stack1, projs_stack2, angles1_rad, angles2_rad)
        self._setup_normalized_coordinates(indices1, indices2, reference, n_projs_tot)
        self._configure_shifts_estimator(shifts_estimator, shifts_estimator_kwargs)

        self.e_theta = np.array([np.cos(self.angles1), -np.sin(self.angles1)]).T
        self._n_threads = n_calc_threads or max(1, get_num_threads() // 2)

        # Default value before fit
        self.shifts_vu = None
        self._coeffs = None
        self._coeffs_v = None
        self._deg_xy = None
        self._deg_z = None

    def _set_projs_pairs(self, projs_stack1, projs_stack2, angles1, angles2):
        if projs_stack1.shape != projs_stack2.shape:
            raise ValueError(
                f"'projs_stack1' and 'projs_stack2' must have the same shape - have {projs_stack1.shape} and {projs_stack2.shape}"
            )
        if len(angles1) != len(angles2):
            raise ValueError("'angles1' and 'angles2' must have the same size")
        if len(angles1) != projs_stack1.shape[0] or len(angles2) != projs_stack2.shape[0]:
            raise ValueError(
                "There must be as many values in (angles1, angles2) as there are projections in (projs_stack1, projs_stack2"
            )
        self.projs_stack1 = projs_stack1
        self.projs_stack2 = projs_stack2
        self.angles1 = np.array(angles1)
        self.angles2 = np.array(angles2)
        self.n_pairs = self.angles1.size
        # Now determine if the angular spacing between projs_stack1[i] and projs_stack1[i]
        self.pair_types = []
        gaps = []
        for i, (a1, a2) in enumerate(zip(self.angles1, self.angles2)):
            gap = np.mod(np.abs(a2 - a1), 2 * np.pi)
            if np.isclose(gap, 0, atol=1e-1):
                # same angle: probably "return projection"
                self.pair_types.append(PairType.RETURN)
            elif np.isclose(gap, np.pi, atol=1e-1):
                # opposed by 180 degrees
                self.pair_types.append(PairType.OPPOSITE)
            else:
                raise ValueError(
                    f"Projections pair number {i} are spaced by {np.degrees(gap)} degrees - don't know what to do with them"
                )
            gaps.append(gap)
        if np.std([pt.value for pt in self.pair_types]) > 0:
            raise NotImplementedError(
                "Mixing pairs (projection, opposite_projection) and (projection, return_projection) is not supported"
            )
        self.is_return = any([pt == PairType.RETURN for pt in self.pair_types])
        self.gaps = np.array(gaps)
        self._pair_types = np.array([pt.value for pt in self.pair_types])

    def _setup_normalized_coordinates(self, indices1, indices2, reference, n_projs_tot):
        self.indices1 = np.array(indices1) if indices1 is not None else None
        self.indices2 = np.array(indices2) if indices2 is not None else None
        self.n_projs_tot = n_projs_tot
        if n_projs_tot is None and indices1 is not None:
            self.n_projs_tot = np.max(indices1)  # best guess
        self.reference = reference
        # TODO find a better way
        distance_to_pi = abs(self.angles2.max() - np.pi)
        distance_to_twopi = abs(self.angles2.max() - 2 * np.pi)
        self._angle_max = 2 * np.pi if distance_to_twopi < distance_to_pi else np.pi
        self.a1 = self.normalize_coordinates(self.angles1, part=1)
        self.a2 = self.normalize_coordinates(self.angles2, part=2)
        self.a_all = np.concatenate([self.a1, self.a2])

    def normalize_coordinates(self, angles, part=1):
        """
        Get the "curvilinear coordinates" that are used (instead of projection angles in radians or degrees) for fit.
        These coordinates depend on:
           - how we normalize (wrt total number of angles, or wrt angle max)
           - the reference projection (start or end)

        Parameters
        ----------
        angles: array
            Array with projection angles
        part: int, optional
            Which part of the scan the provided angles belong to.
            Using "part=1" (resp. part=2) means that these angles correspond to "angles1_rad" (resp. angles2_rad)

        """
        # Currently this will work for
        #   - 360° scan with only pairs of opposite projs
        #   - 180° scan + pairs of return projections only  (we normalize only the angles of regular projs)
        # TODO consider other normalizations
        if part not in [1, 2]:
            raise ValueError("Expected 'part' to be either 1 or 2")

        def _normalize_with_reference(a):
            if self.reference == "end":
                return 1 - a
            return a

        # "Outward projections", always normalize with angle max
        if part == 1:  # noqa: SIM114
            return _normalize_with_reference(angles / self._angle_max)

        # Opposite projections (360° scan), normalize also with angle max
        elif not (self.is_return):
            return _normalize_with_reference(angles / self._angle_max)

        # Now, here, we are in the case "180° scan with return projections"
        #   - The regular projections have coordinate [0, ..., 1] (or almost 1)
        #   - The subsequent return projections have coordinates > 1: [1.01, ...]
        # We assume that "stack1" is all outward projs, "stack2" is all return projs (see NotImplementedError in _set_projs_pairs)
        n_outward_projs = self.angles1.size
        n_return_projs = self.angles2.size
        if self.indices2 is not None and self.n_projs_tot is not None:
            return _normalize_with_reference(self.indices2 / self.n_projs_tot)
        else:
            # This case is tricky, we should probably throw an error
            a_all = np.arange(n_outward_projs + n_return_projs) / n_outward_projs
            return _normalize_with_reference(a_all[-n_outward_projs:])

    def _configure_shifts_estimator(self, shifts_estimator, shifts_estimator_kwargs):
        check_supported(shifts_estimator, list(self._shifts_estimators_default_kwargs.keys()), "shifts estimator")
        shifts_estimator_kwargs = shifts_estimator_kwargs or {}
        self.shifts_estimator = shifts_estimator
        if self.shifts_estimator == "phase_cross_correlation" and phase_cross_correlation is None:
            warn(
                "shift estimator was set to 'phase_cross_correlation' but it requires scikit-image which is not available. Falling back to 'DetectorTranslationAlongBeam'",
                Warning,
            )
            self.shifts_estimator = "DetectorTranslationAlongBeam"
            shifts_estimator_kwargs.pop("overlap_ratio", None)  # Don't use this kwarg for DetectorTranslationAlongBeam
        self._shifts_estimator_kwargs = self._shifts_estimators_default_kwargs[self.shifts_estimator].copy()
        self._shifts_estimator_kwargs.update(shifts_estimator_kwargs)

    def _find_shifts(self, img1, img2):
        if self.shifts_estimator == "estimate_shifts":
            # estimate_shifts recovers the shifts in scipy convention (scipy.ndimage.shift),
            # but there is a sign difference wrt scikit-image.
            return -estimate_shifts(img1, img2, **self._shifts_estimator_kwargs)
        elif self.shifts_estimator == "phase_cross_correlation" and phase_cross_correlation is not None:
            return phase_cross_correlation(img1, img2, **self._shifts_estimator_kwargs)[0]
        else:
            return RadiosShiftEstimator().find_shift(np.stack([img1, img2]), [0, 1], **self._shifts_estimator_kwargs)

    def compute_detector_shifts(self):
        """This function computes the shifts between two images of all pairs."""

        def _comp_shift(i):
            img2 = self.projs_stack2[i]
            if self.pair_types[i] == PairType.OPPOSITE:
                img2 = img2[:, ::-1]
            return self._find_shifts(self.projs_stack1[i], img2)

        with ThreadPool(self._n_threads) as tp:
            shifts = tp.map(_comp_shift, range(self.n_pairs))

        self.shifts_vu = np.array(shifts)

    def _compute_detector_shifts_if_needed(self, recalculate_shifts):
        if recalculate_shifts or (self.shifts_vu is None):
            self.compute_detector_shifts()

    def get_model_matrix(self, do_cor_estimation=True, degree=1):
        """
        Compute the model matrix for horizontal components (x, y)
        For degree 1:
        M = [cos(theta) * (a^+ - a) ;  -sin(theta) * (a^+ - a) ; 2 ]
        This matrix needs three ingredients:
          - The angles "theta" for which pairs of radios are compared. We take the "angles1_rad" provided at this class instanciation.
          - The corresponding normalized coordinate "a" : a = normalize_coordinates(angles1_rad)
          - Normalized coordinate "a_plus" of each second radio in a pair.

        In other words, the pair of radios (projs_stack1[i], projs_stack2[i]) have angles (angles1_rad[i], angles2_rad[i])
        and normalized coordinates (a[i], a_plus[i])

        The resulting matrix strongly depends on how the angles are ordered/normalized.
        """
        angles = self.angles1
        cos_theta = np.cos(angles)
        sin_theta = np.sin(angles)
        ap = self.a2
        a = self.a1

        M = np.zeros((self.n_pairs, 2 * degree + int(do_cor_estimation)), dtype=np.float64)
        i_col = 0
        for d in range(degree, 0, -1):  # eg. [2, 1]. No 0 !
            columns = np.vstack([(ap**d - a**d) * cos_theta, -(ap**d - a**d) * sin_theta]).T
            M[:, i_col : i_col + 2] = columns
            i_col += 2
        if do_cor_estimation:
            M[:, -1] = 2
        return M

    def _get_vdm_matrix(self, a, degree):
        vdm_mat = np.stack([a**d for d in range(degree, 0, -1)], axis=1)
        return vdm_mat

    def apply_fit_horiz(self, angles=None, angles_normalized=None):
        """
        Apply the fitted parameters to get the sample displacement in (x, y)

        Parameters
        -----------
        angles: array, optional
            Angles the fit is applied onto.
        angles_normalized: array, optional
            Normalized angles the fit is applied onto. If provided, takes precedence over 'angles' (see notes below)

        Returns
        -------
        txy: array
            Array of shape (n_provided_angles, 2) where txy[:, 0] is the motion x-component, and txy[:, 1] is the motion y-component

        Notes
        ------
        The fit is assumed to have been done beforehand on a series of detector shifts measurements.
        Once the fit is done, coefficients are extracted and stored by this class instance.
        The parameter 'angles' provided to this function is normalized before applying the fit.
        For degree 2, applying the fit is roughly: t_x = alpha_x * a^2 + beta_x * a
        where 'a' is the normalized angle coordinate, and (alpha_x, beta_x) the coefficients extracted from the fit.
        """
        if self._coeffs is None:
            raise RuntimeError("Need to do estimate_horizontal_motion() first")
        if angles is None and angles_normalized is None:
            raise ValueError("Need to provide either 'angles' or 'angles_normalized'")
        if angles_normalized is None:
            angles_normalized = self.normalize_coordinates(angles)

        # See get_model_matrix()
        end = -1 if self._coeffs.size % 2 == 1 else None
        coeffs_x = self._coeffs[:end:2]
        coeffs_y = self._coeffs[1:end:2]

        vdm_mat = self._get_vdm_matrix(angles_normalized, self._deg_xy)
        return np.stack([vdm_mat.dot(coeffs_x), vdm_mat.dot(coeffs_y)], axis=1)

    def apply_fit_vertic(self, angles=None, angles_normalized=None):
        if self._coeffs_v is None:
            raise RuntimeError("Need to do estimate_vertical_motion() first")
        if angles is None and angles_normalized is None:
            raise ValueError("Need to provide either 'angles' or 'angles_normalized'")
        if angles_normalized is None:
            angles_normalized = self.normalize_coordinates(angles)
        vdm_mat = self._get_vdm_matrix(angles_normalized, self._deg_z)
        coeffs_z = self._coeffs_v
        return vdm_mat.dot(coeffs_z)

    def estimate_horizontal_motion(self, degree=1, cor=None, recalculate_shifts=False):
        """
        Estimation of the horizontal motion component.

        Parameters
        -----------
        degree: int (default=1).
            Degree of the polynomial model of the motion in the horizontal plane,
            for both x and y components.
        cor: float, optional
            Center of rotation, relative to the middle of the image.
            If None (default), it will be estimated along with the horizontal movement components.
            If provided (scalar value), use this value and estimate only the horizontal movement components.
        recalculate_shifts: bool, optional
            Whether to re-calculate detector shifts (usually with phase cross-correlation) if already calculated
        """
        do_cor_estimation = cor is None

        # Get "Delta u" estimated from pairs of projections
        self._compute_detector_shifts_if_needed(recalculate_shifts)

        # Build model matrix
        M = self.get_model_matrix(do_cor_estimation=do_cor_estimation, degree=degree)

        # Build parameters vector
        b = self.shifts_vu[:, 1] if do_cor_estimation else self.shifts_vu[:, 1] - 2 * cor * self._pair_types

        # Least-square fit, i.e  coeffs = pinv(M) * b
        self._coeffs = np.linalg.lstsq(M, b, rcond=None)[0]
        self._deg_xy = degree

        # Evaluate coefficients on current angles
        txy = self.apply_fit_horiz(angles_normalized=self.a_all)
        c = self._coeffs[-1] if do_cor_estimation else cor

        return txy, c

    estimate_cor_and_horizontal_motion = estimate_horizontal_motion

    def estimate_vertical_motion(self, degree=1, recalculate_shifts=False):
        """Estimation of the motion vertical component."""

        # Get "Delta v" estimated from pairs of projections
        self._compute_detector_shifts_if_needed(recalculate_shifts)

        # Model matrix is simple here: v = t_z  (parallel geometry)
        mat = np.zeros([self.n_pairs, degree])
        for d in range(degree, 0, -1):
            mat[:, degree - d] = self.a2**d - self.a1**d
        self._coeffs_v = np.linalg.lstsq(mat, self.shifts_vu[:, 0], rcond=None)[0]
        self._deg_z = degree

        tz = self.apply_fit_vertic(angles_normalized=self.a_all)
        return tz

    def convert_sample_motion_to_detector_shifts(self, t_xy, t_z, angles, cor=0):
        """
        Convert vectors of motion (t_x, t_y, t_z), from the sample domain,
        to vectors of motion (t_u, t_v) in the detector domain

        Parameters
        ----------
        t_xy: numpy.ndarray
            Sample horizontal shifts with shape (n_angles, 2).
            The first (resp. second) column are the x-shifts (resp. y-shifts)
        t_z: numpy.ndarray
            Sample vertical shifts, with the size n_angles
        angles: numpy.ndarray
            Rotation angle (in degree) corresponding to each component
        cor: float, optional
            Center of rotation
        """
        e_theta = np.array([np.cos(angles), -np.sin(angles)]).T
        dotp = np.sum(t_xy * e_theta, axis=1)
        shifts_u = dotp + cor
        shifts_v = t_z.copy()
        return np.stack([shifts_v, shifts_u], axis=1)

    def apply_fit_to_get_detector_displacements(self, cor=None):
        # This should be equal to:
        # txy2 = self.apply_fit_horiz(angles_normalized=self.a2)
        # txy1 = self.apply_fit_horiz(angles_normalized=self.a1)
        # shifts_u = np.sum((txy2 - txy1) * self.e_theta, axis=1) + 2 * cor * (1 - self.is_return)
        M = self.get_model_matrix(do_cor_estimation=(cor is None), degree=self._deg_xy)
        shifts_u = M.dot(self._coeffs) + 2 * (cor if cor is not None and not (self.is_return) else 0)

        tz2 = self.apply_fit_vertic(angles_normalized=self.a2)
        tz1 = self.apply_fit_vertic(angles_normalized=self.a1)
        shifts_v = tz2 - tz1

        shifts_vu = np.stack([shifts_v, shifts_u], axis=1)
        return shifts_vu

    def get_max_fit_error(self, cor=None):
        """
        Get the maximum error of the fit of displacement (in pixel units), projected in the detector domain ;
        i.e compare shifts_u (measured via phase cross correlation) to M.dot(coeffs) (model fit)
        """
        shifts_vu_modelled = self.apply_fit_to_get_detector_displacements(cor=cor)
        err_max_vu = np.max(np.abs(shifts_vu_modelled - self.shifts_vu), axis=0)
        return err_max_vu

    def plot_detector_shifts(self, cor=None):
        """
        Plot the detector shifts, i.e difference of u-movements between theta and theta^+.
        This can be used to compare the fit against measured shifts between pairs of projections.

        The sample movements were inferred from pairs of projections:
        projs1[i] at angles1[i], and projs2[i] at angles2[i]
        From these pairs of projections, a model of motion is built and we can generate:
          - The motion in sample domain (tx(theta), ty(theta), tz(theta)) for arbitrary theta
          - The motion in detector domain (t_u(theta), t_v(theta)) (for arbitrary theta) which is the parallel projection of the above

        What was used for the fit is t_u(theta^+) - t_u(theta).
        This function will plot this "difference" between t_u(theta^+) and t_u(theta).
        """
        estimated_shifts_vu = self.apply_fit_to_get_detector_displacements(cor=cor)
        gt_shifts_u = None
        gt_shifts_v = None

        fig, ax = plt.subplots(2)
        t_axis_vals = np.degrees(self.angles1)
        t_axis_label = "Angle (deg)"

        # Horizontal diff-movements on detector
        subplot = ax[0]
        subplot.plot(t_axis_vals, self.shifts_vu[:, 1], ".", label="Measured (%s)" % self.shifts_estimator)
        subplot.plot(t_axis_vals, estimated_shifts_vu[:, 1], ".-", label="Fit")
        if gt_shifts_u is not None:
            subplot.plot(self.angles1, gt_shifts_u, label="Ground Truth")
        subplot.set_xlabel(t_axis_label)
        subplot.set_ylabel("shift (pix)")
        subplot.legend()
        subplot.set_title("Horizontal shifts on the detector")

        # Vertical diff-movements on detector
        subplot = ax[1]
        subplot.plot(t_axis_vals, self.shifts_vu[:, 0], ".", label="Measured (%s)" % self.shifts_estimator)
        subplot.plot(t_axis_vals, estimated_shifts_vu[:, 0], ".-", label="Fit")
        if gt_shifts_v is not None:
            subplot.plot(t_axis_vals, gt_shifts_v, label="Ground truth")
        subplot.set_xlabel(t_axis_label)
        subplot.set_ylabel("shift (pix)")
        subplot.legend()
        subplot.set_title("Vertical shifts on the detector")

        plt.show()

    def plot_movements(self, cor=None, angles_rad=None, gt_xy=None, gt_z=None):
        """
        Plot the movements in the sample and detector domain, for a given vector of angles.
        Mind the difference with plot_sample_shifts(): in this case we plot proj(txy(theta))
        whereas plot_sample_shifts() plots proj(txy(theta^+)) - proj(txy(theta)),  which can be used to compare with measured shifts between projections.
        """
        if plt is None:
            raise ImportError("Need matplotlib")
        if self._deg_xy is None:
            raise RuntimeError("Need to estimate shifts first")

        if angles_rad is None:
            angles_rad = self.angles1
        angles_deg = np.degrees(angles_rad)

        txy = self.apply_fit_horiz(angles=angles_rad)
        tz = self.apply_fit_vertic(angles=angles_rad)
        estimated_shifts_vu = self.convert_sample_motion_to_detector_shifts(txy, tz, angles_rad, cor=cor or 0)

        gt_shifts_vu = None
        if gt_xy is not None:
            if gt_z is None or gt_z.shape[0] != gt_xy.shape[0] or gt_xy.shape[0] != len(angles_rad):
                raise ValueError("gt_xy has to be provided with gt_z, of the same size as 'angles_rad'")
            gt_shifts_vu = self.convert_sample_motion_to_detector_shifts(gt_xy, gt_z, angles_rad, cor=cor or 0)

        fig, ax = plt.subplots(2, 2)

        # Horizontal movements on detector
        subplot = ax[0, 0]
        subplot.plot(angles_deg, estimated_shifts_vu[:, 1], ".-", label="Fit")
        if gt_shifts_vu is not None:
            subplot.plot(angles_deg, gt_shifts_vu[:, 1], label="Ground Truth")
        subplot.set_xlabel("Angle (deg)")
        subplot.set_ylabel("shift (pix)")
        subplot.legend()
        subplot.set_title("Horizontal movements projected onto the detector")

        # Vertical movements on detector
        subplot = ax[1, 0]
        subplot.plot(angles_deg, estimated_shifts_vu[:, 0], ".-", label="Fit")
        if gt_shifts_vu is not None:
            subplot.plot(angles_deg, gt_shifts_vu[:, 0], label="Ground truth")
        subplot.set_xlabel("Angle (deg)")
        subplot.set_ylabel("shift (pix)")
        subplot.legend()
        subplot.set_title("Vertical movements projected onto the detector")

        # Horizontal movements in sample domain
        subplot = ax[0, 1]
        subplot.scatter(txy[:, 0], txy[:, 1], label="Fit", s=1)
        if gt_xy is not None:
            subplot.scatter(gt_xy[:, 0], gt_xy[:, 1], label="Ground Truth", s=1)
        subplot.set_xlabel("x (pix)")
        subplot.set_ylabel("y (pix)")
        subplot.legend()
        subplot.set_title("Sample movement in horizontal plane")

        # Vertical movements in sample domain
        subplot = ax[1, 1]
        subplot.plot(angles_deg, tz, ".-", label="Fit")
        if gt_z is not None:
            subplot.plot(angles_deg, gt_z, ".", label="Ground truth")
        subplot.set_xlabel("Angle (deg)")
        subplot.set_ylabel("z position (pix)")
        subplot.legend()
        subplot.set_title("Sample vertical movement")

        plt.show()
