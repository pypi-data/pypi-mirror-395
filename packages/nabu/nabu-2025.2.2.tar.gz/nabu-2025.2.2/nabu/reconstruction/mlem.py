from multiprocessing import get_context
from multiprocessing.pool import Pool
import numpy as np
from .fbp_base import BackprojectorBase


# See notes in MLEMReconstructor.__init__
cct = None

try:
    # importing cupy normally won't mess with multiprocessing
    # (i.e it won't create a unsollicited context before fork())
    import cupy

    __has_cupy__ = True
except:
    __has_cupy__ = False


class CCTMLEMReconstructor:
    """
    A reconstructor for MLEM reconstruction using the CorrCT toolbox.

    Parameters
    ----------
    data_vwu_shape : tuple
        Shape of the input data, expected to be (n_slices, n_angles, n_dets). Raises an error if the shape is not 3D.
    angles_rad : numpy.ndarray
        Angles in radians for the projections. Must match the second dimension of `data_vwu_shape`.
    shifts_vu : numpy.ndarray, optional.
        Shifts in the v and u directions for each angle. If provided, must have the same number of cols as `angles_rad`. Each col is (tv,tu)
    cor : float, optional
        Center of rotation, which will be adjusted based on the sinogram width.
    n_iterations : int, optional
        Number of iterations for the MLEM algorithm. Default is 50.
    extra_options : dict, optional
        Additional options for the reconstruction process. Default options include:
        - scale_factor (float, default is 1.0): Scale factor for the reconstruction.
        - compute_shifts (boolean, default is False): Whether to compute shifts.
        - tomo_consistency (boolean, default is False): Whether to enforce tomographic consistency.
        - v_min_for_v_shifts (number, default is 0): Minimum value for vertical shifts.
        - v_max_for_v_shifts (number, default is None): Maximum value for vertical shifts.
        - v_min_for_u_shifts (number, default is 0): Minimum value for horizontal shifts.
        - v_max_for_u_shifts (number, default is None): Maximum value for horizontal shifts.
    """

    implementation = "corrct"
    default_extra_options = {
        "compute_shifts": False,
        "tomo_consistency": False,
        "v_min_for_v_shifts": 0,
        "v_max_for_v_shifts": None,
        "v_min_for_u_shifts": 0,
        "v_max_for_u_shifts": None,
        "scale_factor": 1.0,
    }

    def __init__(
        self,
        data_vwu_shape,
        angles_rad,
        shifts_uv=None,
        cor=None,  # absolute
        n_iterations=50,
        extra_options=None,
    ):

        # Do it here, since importing *anything* from corrct will spawn a Cuda context.
        # This will crash if called from within a subprocess without clean context management
        global cct  # noqa: PLW0603
        import corrct as cct

        #
        self.angles_rad = angles_rad
        self.n_iterations = n_iterations
        self.scale_factor = extra_options.get("scale_factor", 1.0)

        self._configure_extra_options(extra_options)
        self._set_sino_shape(data_vwu_shape)
        self._set_shifts(shifts_uv, cor)

    def _configure_extra_options(self, extra_options):
        self.extra_options = self.default_extra_options.copy()
        self.extra_options.update(extra_options or {})

    def _set_sino_shape(self, sinos_shape):
        if len(sinos_shape) != 3:
            raise ValueError("Expected a 3D shape")
        self.sinos_shape = sinos_shape
        self.n_sinos, self.n_angles, self.prj_width = sinos_shape
        if self.n_angles != len(self.angles_rad):
            raise ValueError(
                f"Number of angles ({len(self.angles_rad)}) does not match size of sinograms ({self.n_angles})."
            )

    def _set_shifts(self, shifts_uv, cor):
        if shifts_uv is None:
            self.shifts_vu = None
        else:
            if shifts_uv.shape[0] != self.n_angles:
                raise ValueError(
                    f"Number of shifts given ({shifts_uv.shape[0]}) does not mathc the number of projections ({self.n_angles})."
                )
            self.shifts_vu = -shifts_uv.copy().T[::-1]
        if cor is None:
            self.cor = 0.0
        else:
            self.cor = (
                -cor + (self.sinos_shape[-1] - 1) / 2.0
            )  # convert absolute to relative in the ASTRA convention, which is opposite to Nabu relative convention.

    def reset_rot_center(self, cor):
        self.cor = -cor + (self.sinos_shape[-1] - 1) / 2.0

    def reconstruct(self, data_vwu, x0=None):
        """
        data_align_vwu: numpy.ndarray or cupy array
            Raw data, with shape (n_sinograms, n_angles, width)
        output: optional
            Output array. If not provided, a new numpy array is returned
        """
        if not isinstance(data_vwu, np.ndarray):
            data_vwu = data_vwu.get()
        # data_vwu /= data_vwu.mean()

        # MLEM recons
        self.vol_geom_align = cct.models.VolumeGeometry.get_default_from_data(data_vwu)
        if self.shifts_vu is not None:
            self.prj_geom_align = cct.models.ProjectionGeometry.get_default_parallel()
            # Vertical shifts were handled in pipeline. Set them to ZERO
            self.shifts_vu[:, 0] = 0.0
            self.prj_geom_align.set_detector_shifts_vu(self.shifts_vu, self.cor)
        else:
            self.prj_geom_align = None

        variances_align = cct.processing.compute_variance_poisson(data_vwu)
        self.weights_align = cct.processing.compute_variance_weight(variances_align, normalized=True)  # , use_std=True
        self.data_term_align = cct.data_terms.DataFidelity_wl2(self.weights_align)
        solver = cct.solvers.MLEM(verbose=True, data_term=self.data_term_align)
        self.solver_opts = dict(lower_limit=0)  # , x_mask=cct.processing.circular_mask(vol_geom_align.shape_xyz[:-2])

        with cct.projectors.ProjectorUncorrected(
            self.vol_geom_align, self.angles_rad, rot_axis_shift_pix=self.cor, prj_geom=self.prj_geom_align
        ) as A:
            rec, _ = solver(A, data_vwu, iterations=self.n_iterations, x0=x0, **self.solver_opts)
        return rec * self.scale_factor


# COMPAT.
MLEMReconstructor = CCTMLEMReconstructor
# -


def _has_corrct(x):
    # should be run from within a Process
    try:
        # ruff: noqa: F401
        import corrct

        avail = True
    except (ImportError, RuntimeError, OSError, NameError):
        avail = False
    return avail


def has_corrct(safe=True):
    """
    corrct will create a cuda context upon importing any module.
    On the other hand, python will crash if creating a subprocess when cuda is already initialized.
    So to check whether corrct is available, we do the "try import" in a subprocess
    """
    if not safe:
        return _has_corrct(None)
    try:
        ctx = get_context("spawn")
        with Pool(1, context=ctx) as p:
            v = p.map(_has_corrct, [1])[0]
    except AssertionError:
        # Can get AssertionError: daemonic processes are not allowed to have children
        # if the calling code is already a subprocess
        return _has_corrct(None)
    return v


class NabuMLEMReconstructor:

    implementation = "nabu"
    default_extra_options = BackprojectorBase.default_extra_options.copy()

    def __init__(
        self,
        sino_shape,
        slice_shape=None,
        angles=None,
        rot_center=None,
        halftomo=False,
        extra_options=None,
        cuda_options=None,
    ):

        self._configure_extra_options(extra_options)
        if not (__has_cupy__):
            raise ImportError("Need cupy to use this class")

        # do it here to avoid creating cuda context at module import
        from cupy import ElementwiseKernel
        from .fbp import Backprojector
        from .projection import Projector

        self.backproj = Backprojector(
            sino_shape,
            slice_shape=slice_shape,
            angles=angles,
            rot_center=rot_center,
            halftomo=halftomo,
            filter_name="none",
            extra_options=self.extra_options,
            backend_options=cuda_options,
        )
        self.slice_shape = self.backproj.slice_shape
        self.proj = Projector(
            self.slice_shape,
            self.backproj.angles,
            rot_center=rot_center,
            detector_width=None,  # TODO
            normalize=False,  # ?
            extra_options=self.extra_options,
            cuda_options=cuda_options,
        )

        self._update_projection_kernel = ElementwiseKernel(
            "float32 proj, float32 proj_data, float32 eps",
            "float32 proj_inv",
            "proj_inv = proj_data / ((fabsf(proj) > eps) ? (proj) : (1.0f))",
            name="update_projection",
        )
        cuda = self.proj.cuda_processing
        self.cuda = cuda
        ones = np.ones(sino_shape, "f")
        self._oinv = cuda.to_device("oinv", (1.0 / self.backproj.backproj(ones)).astype("f"))
        self._x = cuda.allocate_array("x", self._oinv.shape)
        self._y = cuda.allocate_array("y", self._x.shape)
        self._proj = cuda.allocate_array("proj", sino_shape)
        self._proj_inv = cuda.allocate_array("proj_inv", sino_shape)

    def _configure_extra_options(self, extra_options):
        self.extra_options = self.default_extra_options.copy()
        self.extra_options.update(extra_options or {})
        # Always use "centered_axis" for iterative reconstruction
        self.extra_options["centered_axis"] = True
        # If using "clip_outer_circle", don't put zeros outside - use ones because MLEM is multiplicative
        self._old_outer_circle_value = self.extra_options.get("outer_circle_value", None)
        self.extra_options["outer_circle_value"] = 1.0
        # These parameters are not needed for Backprojector and Projector
        self.extra_options.pop("padding_mode", None)
        self._scale_factor = self.extra_options.pop("scale_factor", None)
        #

    def reconstruct(self, sino, n_iterations=10, output=None, eps=1e-6):
        if isinstance(sino, np.ndarray):
            sino = self.cuda.to_device("sino", sino)

        # data should not contain negative values
        cupy.clip(sino, eps, None, out=sino)

        x = self._x
        y = self._y
        proj = self._proj
        proj_inv = self._proj_inv
        oinv = self._oinv

        if output is not None:
            self.cuda.check_array(output, x.shape)
            x = output

        proj_inv[:] = sino[:]
        x.fill(1)  # update is multiplicative, start with ones (not zeros)

        for k in range(n_iterations):
            # proj = P(x)
            self.proj.projection(x, output=proj)

            self._update_projection_kernel(proj, sino, eps, proj_inv)

            # x *= B(proj_inv) * oinv
            self.backproj.backproj(proj_inv, output=y)
            x *= y
            x *= oinv

        if self._scale_factor is not None:
            x *= self._scale_factor

        if self.extra_options["clip_outer_circle"]:
            # clip outer circle has to be done last.
            # The outside value was modified to be 1 during iterative reconstruction ; restore it for the final circle clip
            self.backproj._clip_circle_args[-1] = np.float32(self._old_outer_circle_value or 0)
            self.backproj._clip_circle_kernel(x, *self.backproj._clip_circle_args, **self.backproj._clip_circle_kwargs)
            self.backproj._clip_circle_args[-1] = self.extra_options["outer_circle_value"]

        return x
