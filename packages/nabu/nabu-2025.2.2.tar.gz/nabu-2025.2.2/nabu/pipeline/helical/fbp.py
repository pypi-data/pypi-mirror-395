import numpy as np
from ...reconstruction.fbp import Backprojector
from .filtering import HelicalSinoFilter


class BackprojectorHelical(Backprojector):
    """This is the Backprojector derived class for helical reconstruction.
    The modifications are detailed here :

         * the backprojection is decoupled from the filtering. This allows, in the pipeline,
           for doing first a filtering using backprojector_object.sino_filter subobject,
           then calling backprojector_object.backprojection only after reweighting the result of
           the filter_sino method of sino_filter subobject.
         * the angles can be reset on the fly, and the class can work with a variable number of projection.
           As a matter of fact, with the helical_chunked_regridded.py pipeline, the reconstruction is done
           each time with the same set of angles, this because of the regridding mechanism. The feature
           might return useful in the future if alternative approaches are developed again.
         *
    """

    def __init__(self, *args, **kwargs):
        """This became needed after the _d_sino allocation was removed from the base class"""
        super().__init__(*args, **kwargs)
        self._d_sino = self._processing.allocate_array("d_sino", self.sino_shape, "f")

    def set_custom_angles_and_axis_corrections(self, angles_rad, x_per_proj):
        """To arbitrarily change angles

        Parameters
        ----------
        angles_rad: array of floats
           one angle per each projection in radians

        x_per_proj: array of floats
           each entry is the axis shift for a projection, in pixels.

        """
        self.n_provided_angles = len(angles_rad)
        self._axis_correction = np.zeros((1, self.n_angles), dtype=np.float32)

        self._axis_correction[0, : self.n_provided_angles] = -x_per_proj

        self.angles[: self.n_provided_angles] = angles_rad

        self._compute_angles_again()

        self.kern_proj_args[1] = self.n_provided_angles
        self.kern_proj_args[6] = self.offsets["x"]
        self.kern_proj_args[7] = self.offsets["y"]

    def _compute_angles_again(self):
        """to update angles dependent auxiliary arrays"""
        self.h_cos[0] = np.cos(self.angles).astype("f")
        self.h_msin[0] = (-np.sin(self.angles)).astype("f")
        self._d_msin[:] = self.h_msin[0]
        self._d_cos[:] = self.h_cos[0]
        if self._axis_correction is not None:
            self._d_axcorr[:] = self._axis_correction

    def _init_filter(self, filter_name):
        """To use the HelicalSinoFilter which is derived from SinoFilter
        with a slightly different padding scheme
        """
        self.filter_name = filter_name
        self.sino_filter = HelicalSinoFilter(
            self.sino_shape,
            filter_name=self.filter_name,
            padding_mode=self.padding_mode,
            cuda_options={"ctx": self.cuda_processing.ctx},
        )

    def backprojection(self, sino, output=None):
        """Redefined here to do backprojection only, compare to the base class method."""
        self._d_sino[:] = sino
        res = self.backproj(self._d_sino, output=output)
        return res

    def _init_geometry(self, sino_shape, slice_shape, angles, rot_center, slice_roi):
        """this is identical to _init_geometry of the base class with the
        exception that self.extra_options["centered_axis"] is not considered
        and as a consequence  self.offsets is not set here and the one of  _set_slice_roi
        is kept.
        """
        if slice_shape is not None and slice_roi is not None:
            raise ValueError("slice_shape and slice_roi cannot be used together")
        self.sino_shape = sino_shape
        if len(sino_shape) == 2:
            n_angles, dwidth = sino_shape
        else:
            raise ValueError("Expected 2D sinogram")
        self.dwidth = dwidth
        self.rot_center = rot_center or (self.dwidth - 1) / 2.0
        self._set_slice_shape(
            slice_shape,
        )
        self.axis_pos = self.rot_center
        self._set_angles(angles, n_angles)
        self._set_slice_roi(slice_roi)
        self._set_axis_corr()

    def _set_slice_shape(self, slice_shape):
        """this is identical to the _set_slice_shape ofthe base class
        with the exception that n_y,n_x default to the largest possible reconstructible slice
        """

        n_y = self.dwidth + abs(self.dwidth - 1 - self.rot_center * 2)
        n_x = self.dwidth + abs(self.dwidth - 1 - self.rot_center * 2)

        if slice_shape is not None:
            if np.isscalar(slice_shape):
                slice_shape = (slice_shape, slice_shape)
            n_y, n_x = slice_shape

        self.n_x = n_x
        self.n_y = n_y
        self.slice_shape = (n_y, n_x)

    def _set_slice_roi(self, slice_roi):
        """Automatically tune the offset to in all cases."""
        self.slice_roi = slice_roi
        if slice_roi is None:
            off = -(self.dwidth - 1 - self.rot_center * 2)
            if off < 0:
                self.offsets = {"x": off, "y": off}
            else:
                self.offsets = {"x": 0, "y": 0}
        else:
            start_x, end_x, start_y, end_y = slice_roi
            # convert negative indices
            slice_width, _ = self.slice_shape

            off = min(0, -(self.dwidth - 1 - self.rot_center * 2))

            if end_x < start_x:
                start_x = off
                end_x = off + slice_width

            if end_y < start_y:
                start_y = off
                end_y = off + slice_width

            self.slice_shape = (end_y - start_y, end_x - start_x)

            self.n_x = self.slice_shape[-1]
            self.n_y = self.slice_shape[-2]

            self.offsets = {"x": start_x, "y": start_y}
