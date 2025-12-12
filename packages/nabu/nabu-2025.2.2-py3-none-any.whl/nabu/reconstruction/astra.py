# ruff: noqa
try:
    import astra

    __have_astra__ = True
except ImportError:
    __have_astra__ = False
    astra = None


class AstraReconstructor:
    """
    Base class for reconstructors based on the Astra toolbox
    """

    default_extra_options = {
        "axis_correction": None,
        "clip_outer_circle": False,
        "scale_factor": None,
        "filter_cutoff": 1.0,
        "outer_circle_value": 0.0,
    }

    def __init__(
        self,
        sinos_shape,
        angles=None,
        volume_shape=None,
        rot_center=None,
        pixel_size=None,
        padding_mode="zeros",
        filter_name=None,
        slice_roi=None,
        cuda_options=None,
        extra_options=None,
    ):
        self._configure_extra_options(extra_options)
        self._init_cuda(cuda_options)
        self._set_sino_shape(sinos_shape)
        self._orig_prog_geom = None
        self._init_geometry(
            source_origin_dist,
            origin_detector_dist,
            pixel_size,
            angles,
            volume_shape,
            rot_center,
            relative_z_position,
            slice_roi,
        )
        self._init_fdk(padding_mode, filter_name)
        self._alg_id = None
        self._vol_id = None
        self._proj_id = None

    def _configure_extra_options(self, extra_options):
        self.extra_options = self.default_extra_options.copy()
        self.extra_options.update(extra_options or {})

    def _init_cuda(self, cuda_options):
        cuda_options = cuda_options or {}
        self.cuda = CudaProcessing(**cuda_options)

    def _set_sino_shape(self, sinos_shape):
        if len(sinos_shape) != 3:
            raise ValueError("Expected a 3D shape")
        self.sinos_shape = sinos_shape
        self.n_sinos, self.n_angles, self.prj_width = sinos_shape

    def _set_pixel_size(self, pixel_size):
        if pixel_size is None:
            det_spacing_y = det_spacing_x = 1
        elif np.iterable(pixel_size):
            det_spacing_y, det_spacing_x = pixel_size
        else:
            # assuming scalar
            det_spacing_y = det_spacing_x = pixel_size
        self._det_spacing_y = det_spacing_y
        self._det_spacing_x = det_spacing_x

    def _set_slice_roi(self, slice_roi):
        self.slice_roi = slice_roi
        self._vol_geom_n_x = self.n_x
        self._vol_geom_n_y = self.n_y
        self._crop_data = True
        if slice_roi is None:
            return
        start_x, end_x, start_y, end_y = slice_roi
        if roi_is_centered(self.volume_shape[1:], (slice(start_y, end_y), slice(start_x, end_x))):
            # Astra can only reconstruct subregion centered around the origin
            self._vol_geom_n_x = self.n_x - start_x * 2
            self._vol_geom_n_y = self.n_y - start_y * 2
        else:
            raise NotImplementedError(
                "Astra supports only slice_roi centered around origin (got slice_roi=%s with n_x=%d, n_y=%d)"
                % (str(slice_roi), self.n_x, self.n_y)
            )

    def _init_geometry(
        self,
        source_origin_dist,
        origin_detector_dist,
        pixel_size,
        angles,
        volume_shape,
        rot_center,
        relative_z_position,
        slice_roi,
    ):
        if angles is None:
            self.angles = np.linspace(0, 2 * np.pi, self.n_angles, endpoint=True)
        else:
            self.angles = angles
        if volume_shape is None:
            volume_shape = (self.sinos_shape[0], self.sinos_shape[2], self.sinos_shape[2])
        self.volume_shape = volume_shape
        self.n_z, self.n_y, self.n_x = self.volume_shape
        self.source_origin_dist = source_origin_dist
        self.origin_detector_dist = origin_detector_dist
        self.magnification = 1 + origin_detector_dist / source_origin_dist
        self._set_slice_roi(slice_roi)
        self.vol_geom = astra.create_vol_geom(self._vol_geom_n_y, self._vol_geom_n_x, self.n_z)
        self.vol_shape = astra.geom_size(self.vol_geom)
        self._cor_shift = 0.0
        self.rot_center = rot_center
        if rot_center is not None:
            self._cor_shift = (self.sinos_shape[-1] - 1) / 2.0 - rot_center
        self._set_pixel_size(pixel_size)
        self._axis_corrections = self.extra_options.get("axis_correction", None)
        self._create_astra_proj_geometry(relative_z_position)

    def _create_astra_proj_geometry(self, relative_z_position):
        # This object has to be re-created each time, because once the modifications below are done,
        # it is no more a "cone" geometry but a "cone_vec" geometry, and cannot be updated subsequently
        # (see astra/functions.py:271)
        self.proj_geom = astra.create_proj_geom(
            "cone",
            self._det_spacing_x,
            self._det_spacing_y,
            self.n_sinos,
            self.prj_width,
            self.angles,
            self.source_origin_dist,
            self.origin_detector_dist,
        )
        self.relative_z_position = relative_z_position or 0.0
        # This will turn the geometry of type "cone" into a geometry of type "cone_vec"
        if self._orig_prog_geom is None:
            self._orig_prog_geom = self.proj_geom
        self.proj_geom = astra.geom_postalignment(self.proj_geom, (self._cor_shift, 0))
        # (src, detector_center, u, v) = (srcX, srcY, srcZ, dX, dY, dZ, uX, uY, uZ, vX, vY, vZ)
        vecs = self.proj_geom["Vectors"]

        # To adapt the center of rotation:
        # dX = cor_shift * cos(theta) - origin_detector_dist * sin(theta)
        # dY = origin_detector_dist * cos(theta) + cor_shift * sin(theta)
        if self._axis_corrections is not None:
            # should we check that dX and dY match the above formulas ?
            cor_shifts = self._cor_shift + self._axis_corrections
            vecs[:, 3] = cor_shifts * np.cos(self.angles) - self.origin_detector_dist * np.sin(self.angles)
            vecs[:, 4] = self.origin_detector_dist * np.cos(self.angles) + cor_shifts * np.sin(self.angles)

        # To adapt the z position:
        # Component 2 of vecs is the z coordinate of the source, component 5 is the z component of the detector position
        # We need to re-create the same inclination of the cone beam, thus we need to keep the inclination of the two z positions.
        # The detector is centered on the rotation axis, thus moving it up or down, just moves it out of the reconstruction volume.
        # We can bring back the detector in the correct volume position, by applying a rigid translation of both the detector and the source.
        # The translation is exactly the amount that brought the detector up or down, but in the opposite direction.
        vecs[:, 2] = -self.relative_z_position

    def _set_output(self, volume):
        if volume is not None:
            expected_shape = self.vol_shape  # if not (self._crop_data) else self._output_cropped_shape
            self.cuda.check_array(volume, expected_shape)
            self.cuda.set_array("output", volume)
        if volume is None:
            self.cuda.allocate_array("output", self.vol_shape)
        d_volume = self.cuda.get_array("output")
        z, y, x = d_volume.shape
        self._vol_link = astra.data3d.GPULink(d_volume.ptr, x, y, z, d_volume.strides[-2])
        self._vol_id = astra.data3d.link("-vol", self.vol_geom, self._vol_link)

    def _set_input(self, sinos):
        self.cuda.check_array(sinos, self.sinos_shape)
        self.cuda.set_array("sinos", sinos)  # self.cuda.sinos is now a GPU array
        # TODO don't create new link/proj_id if ptr is the same ?
        # But it seems Astra modifies the input sinogram while doing FDK, so this might be not relevant
        d_sinos = self.cuda.get_array("sinos")

        # self._proj_data_link = astra.data3d.GPULink(d_sinos.ptr, self.prj_width, self.n_angles, self.n_z, sinos.strides[-2])
        self._proj_data_link = astra.data3d.GPULink(
            d_sinos.ptr, self.prj_width, self.n_angles, self.n_sinos, d_sinos.strides[-2]
        )
        self._proj_id = astra.data3d.link("-sino", self.proj_geom, self._proj_data_link)

    def _preprocess_data(self):
        d_sinos = self.cuda.sinos
        for i in range(d_sinos.shape[0]):
            self.sino_filter.filter_sino(d_sinos[i], output=d_sinos[i])

    def _update_reconstruction(self):
        cfg = astra.astra_dict("BP3D_CUDA")
        cfg["ReconstructionDataId"] = self._vol_id
        cfg["ProjectionDataId"] = self._proj_id
        if self._alg_id is not None:
            astra.algorithm.delete(self._alg_id)
        self._alg_id = astra.algorithm.create(cfg)

    def reconstruct(self, sinos, output=None, relative_z_position=None):
        """
        sinos: numpy.ndarray or pycuda.gpuarray
            Sinograms, with shape (n_sinograms, n_angles, width)
        output: pycuda.gpuarray, optional
            Output array. If not provided, a new numpy array is returned
        relative_z_position: int, optional
            Position of the central slice of the slab, with respect to the full stack of slices.
            By default it is set to zero, meaning that the current slab is assumed in the middle of the stack
        """
        self._create_astra_proj_geometry(relative_z_position)
        self._set_input(sinos)
        self._set_output(output)
        self._preprocess_data()
        self._update_reconstruction()
        astra.algorithm.run(self._alg_id)
        #
        # NB: Could also be done with
        # from astra.experimental import direct_BP3D
        # projector_id = astra.create_projector("cuda3d", self.proj_geom, self.vol_geom, options=None)
        # direct_BP3D(projector_id, self._vol_link, self._proj_data_link)
        #
        result = self.cuda.get_array("output")
        if output is None:
            result = result.get()
        if self.extra_options.get("scale_factor", None) is not None:
            result *= np.float32(self.extra_options["scale_factor"])  # in-place for pycuda
        self.cuda.recover_arrays_references(["sinos", "output"])
        return result

    def __del__(self):
        if getattr(self, "_alg_id", None) is not None:
            astra.algorithm.delete(self._alg_id)
        if getattr(self, "_vol_id", None) is not None:
            astra.data3d.delete(self._vol_id)
        if getattr(self, "_proj_id", None) is not None:
            astra.data3d.delete(self._proj_id)
