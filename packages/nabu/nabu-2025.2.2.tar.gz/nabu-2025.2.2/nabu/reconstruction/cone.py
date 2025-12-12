import logging
from math import sqrt
import numpy as np
from ..cuda.processing import CudaProcessing
from ..reconstruction.filtering import SinoFilter
from ..reconstruction.filtering_cuda import CudaSinoFilter
from ..cuda.kernel import CudaKernel

from ..utils import clip_circle, docstring, get_cuda_srcfile, updiv, check_array

try:
    import astra

    # Note that astra.has_feature("cuda") will return True even if cuda is not present on the system
    # (it looks like a compile-time attribute)
    __have_astra__ = True
except ImportError:
    __have_astra__ = False


_logger = logging.getLogger(__name__)


class ConebeamReconstructor:
    """
    A reconstructor for cone-beam geometry using the astra toolbox.
    """

    # Admittedly not really fair, because astra does the BP3D.
    # But to support some features, we had to add many things. This is to distinguish with NumpyConebeamReconstructor below.
    implementation = "nabu"
    #

    default_extra_options = {
        "axis_correction": None,
        "clip_outer_circle": False,
        "scale_factor": None,
        "filter_cutoff": 1.0,
        "outer_circle_value": 0.0,
        # "use_astra_fdk": True,
        "use_astra_fdk": False,
        "crop_filtered_data": True,
    }

    def __init__(
        self,
        sinos_shape,
        source_origin_dist,
        origin_detector_dist,
        angles=None,
        volume_shape=None,
        rot_center=None,
        relative_z_position=None,
        pixel_size=None,
        padding_mode="zeros",
        filter_name=None,
        slice_roi=None,
        cuda_options=None,
        extra_options=None,
    ):
        """
        Initialize a cone beam reconstructor. This reconstructor works on slabs of data,
        meaning that one partial volume is obtained from one stack of sinograms.
        To reconstruct a full volume, the reconstructor must be called on a series of sinograms stacks, with
        an updated "relative_z_position" each time.

        Parameters
        -----------
        sinos_shape: tuple
            Shape of the sinograms stack, in the form (n_sinos, n_angles, prj_width)
        source_origin_dist: float
            Distance, in pixel units, between the beam source (cone apex) and the "origin".
            The origin is defined as the center of the sample
        origin_detector_dist: float
            Distance, in pixel units, between the center of the sample and the detector.
        angles: array, optional
            Rotation angles in radians. If provided, its length should be equal to sinos_shape[1].
        volume_shape: tuple of int, optional
            Shape of the output volume slab, in the form (n_z, n_y, n_x).
            If not provided, the output volume slab shape is (sinos_shape[0], sinos_shape[2], sinos_shape[2]).
        rot_center: float, optional
            Rotation axis position. Default is `(detector_width - 1)/2.0`
        relative_z_position: float, optional
            Position of the central slice of the slab, with respect to the full stack of slices.
            By default it is set to zero, meaning that the current slab is assumed in the middle of the stack
        axis_correction: array, optional
            Array of the same size as the number of projections. Each corresponds to a horizontal displacement.
        pixel_size: float or tuple, optional
            Size of the pixel. Possible options:
              - Nothing is provided (default): in this case, all lengths are normalized with respect to the pixel size,
                i.e 'source_origin_dist' and 'origin_detector_dist' should be expressed in pixels (and 'pixel_size' is set to 1).
              - A scalar number is provided: in this case it is the spacing between two pixels (in each dimension)
              - A tuple is provided: in this case it is the spacing between two pixels in both dimensions,
                vertically then horizontally, i.e (detector_spacing_y, detector_spacing_x)
        scale_factor: float, optional
            Post-reconstruction scale factor.
        padding_mode: str, optional
            How to pad the data before applying FDK. By default this is done by astra with zero-padding.
            If padding_mode is other than "zeros", it will be done by nabu and the padded data is passed to astra
            where no additional padding is done.
            Beware that in its current implementation, this option almost doubles the memory needed.
        slice_roi:
            Whether to reconstruct only a region of interest for each horizontal slice.
            This parameter must be in the form (start_x, end_x, start_y, end_y) with no negative values.
            Note that the current implementation just crops the final reconstructed volume,
            i.e there is no speed or memory benefit.
        use_astra_fdk: bool
            Whether to use the native Astra Toolbox FDK implementation.
            If set to False, the cone-beam pre-weighting and projections padding/filtering is done by nabu.
            Note that this parameter is automatically set to False if padding_mode != "zeros".

        Notes
        ------
        This reconstructor is using the astra toolbox [1]. Therefore the implementation uses Astra's
        reference frame, which is centered on the sample (source and detector move around the sample).
        For more information see Fig. 2 of paper [1].

        To define the cone-beam geometry, two distances are needed:
          - Source-origin distance (hereby d1)
          - Origin-detector distance (hereby d2)

        The magnification at distance d2 is m = 1+d2/d1, so given a detector pixel size p_s, the sample voxel size is p_s/m.

        To make things simpler, this class internally uses a different (but equivalent) geometry:
          - d2 is set to zero, meaning that the detector is (virtually) moved to the center of the sample
          - The detector is "re-scaled" to have a pixel size equal to the voxel size (p_s/m)

        Having the detector in the same plane as the sample center simplifies things when it comes to slab-wise reconstruction:
        defining a volume slab (in terms of z_min, z_max) is equivalent to define the detector bounds, like in parallel geometry.


        References
        -----------
        [1] Aarle, Wim & Palenstijn, Willem & Cant, Jeroen & Janssens, Eline & Bleichrodt,
        Folkert & Dabravolski, Andrei & De Beenhouwer, Jan & Batenburg, Kees & Sijbers, Jan. (2016).
        Fast and flexible X-ray tomography using the ASTRA toolbox.
        Optics Express. 24. 25129-25147. 10.1364/OE.24.025129.
        """
        self._configure_extra_options(extra_options)
        self._init_cuda(cuda_options)
        self._set_sino_shape(sinos_shape)
        self._orig_prog_geom = None
        self._use_astra_fdk = bool(self.extra_options.get("use_astra_fdk", True))
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
        self._setup_clip_circle()
        self._alg_id = None
        self._vol_id = None
        self._proj_id = None

    def _configure_extra_options(self, extra_options):
        self.extra_options = self.default_extra_options.copy()
        self.extra_options.update(extra_options or {})
        self._crop_filtered_data = self.extra_options.get("crop_filtered_data", True)

    def _init_cuda(self, cuda_options):
        cuda_options = cuda_options or {}
        self.cuda = CudaProcessing(**cuda_options)

    def _set_sino_shape(self, sinos_shape):
        if len(sinos_shape) != 3:
            raise ValueError("Expected a 3D shape")
        self.sinos_shape = sinos_shape
        self.n_sinos, self.n_angles, self.prj_width = sinos_shape

    def _init_fdk(self, padding_mode, filter_name):
        self.padding_mode = padding_mode
        if self._use_astra_fdk and padding_mode not in ["zeros", "constant", None, "none"]:
            self._use_astra_fdk = False
            _logger.warning("padding_mode was set to %s, cannot use native astra FDK" % padding_mode)
        if self._use_astra_fdk:
            return
        self.sino_filter = CudaSinoFilter(
            self.sinos_shape[1:],
            filter_name=filter_name,
            padding_mode=self.padding_mode,
            crop_filtered_data=self.extra_options.get("crop_filtered_data", True),
            # TODO (?) configure FFT backend
            extra_options={"cutoff": self.extra_options.get("filter_cutoff", 1.0)},
            # cuda_options={"ctx": self.cuda.ctx},
        )
        # In astra, FDK pre-weighting does the "n_a/(pi/2) multiplication"
        # TODO not sure where this "magnification **2" factor comes from ?
        mult_factor = self.n_angles / 3.141592 * 2 / (self.magnification**2)
        self.sino_filter.set_filter(self.sino_filter.filter_f * mult_factor, normalize=False)
        #

    def _setup_clip_circle(self):
        if not (self.extra_options["clip_outer_circle"]):
            return
        self._clip_circle_kernel = CudaKernel(
            "clip_circle",
            filename=get_cuda_srcfile("clip_circle.cu"),
        )
        slice_shape_xy = self.vol_shape[1:][::-1]
        self._clip_circle_block = (32, 32)
        self._clip_circle_kwargs = {
            "block": self._clip_circle_block,
            "grid": tuple([updiv(sz, blk) for sz, blk in zip(slice_shape_xy, self._clip_circle_block)]),
        }
        self._clip_circle_args = [
            np.int32(slice_shape_xy[0]),
            np.int32(slice_shape_xy[1]),
            np.float32((slice_shape_xy[0] - 1) / 2),
            np.float32((slice_shape_xy[1] - 1) / 2),
            np.float32(self.extra_options.get("outer_circle_value", 0)),
        ]

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
            # For FDK, astra can only reconstruct subregion centered around the origin
            self._vol_geom_n_x = self.n_x - start_x * 2
            self._vol_geom_n_y = self.n_y - start_y * 2
        else:
            raise NotImplementedError(
                "Cone-beam geometry supports only slice_roi centered around origin (got slice_roi=%s with n_x=%d, n_y=%d)"
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

        if not (self._crop_filtered_data) and hasattr(self, "sino_filter"):
            prj_width = self.sino_filter.sino_padded_shape[-1]
        else:
            prj_width = self.prj_width

        self.proj_geom = astra.create_proj_geom(
            "cone",
            self._det_spacing_x,
            self._det_spacing_y,
            self.n_sinos,
            prj_width,
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

    def reset_rot_center(self, rot_center):
        self.rot_center = rot_center
        self._cor_shift = (self.sinos_shape[-1] - 1) / 2.0 - rot_center
        self._create_astra_proj_geometry(self.relative_z_position)

    def _set_output(self, volume):
        if volume is not None:
            expected_shape = self.vol_shape  # if not (self._crop_data) else self._output_cropped_shape
            self.cuda.check_array(volume, expected_shape)
            self.cuda.set_array("output", volume)
        if volume is None:
            self.cuda.allocate_array("output", self.vol_shape)
        d_volume = self.cuda.get_array("output")
        z, y, x = d_volume.shape
        self._vol_link = astra.data3d.GPULink(d_volume.data.ptr, x, y, z, d_volume.strides[-2])
        self._vol_id = astra.data3d.link("-vol", self.vol_geom, self._vol_link)

    def _set_input(self, sinos):
        self.cuda.check_array(sinos, self.sinos_shape, check_contiguous=False)
        # TODO don't create new link/proj_id if ptr is the same ?
        # But it seems Astra modifies the input sinogram while doing FDK, so this might be not relevant
        d_sinos = self.cuda.set_array("sinos", sinos)  # self.cuda.sinos is now a GPU array

        self._reallocate_sinos = False
        if not (self.cuda.is_contiguous(d_sinos)) or not (self._crop_filtered_data):
            self._reallocate_sinos = True
            if self._crop_filtered_data:
                sinos_shape = self.sinos_shape
            # Sometimes, the user does not want to crop data after filtering
            # In this case, the backprojector input should be directly the filtered-but-uncropped data.
            # For cone-beam reconstruction, the FDK pre-weighting takes place on input sinogram (not filtered yet),
            # then filter, then 3D backprojection the un-cropped data.
            else:
                sinos_shape = (self.n_z,) + self.sino_filter.sino_padded_shape
            d_sinos = self.cuda.allocate_array("sinos_contig", sinos_shape)
        self._proj_data_link = astra.data3d.GPULink(
            d_sinos.data.ptr, d_sinos.shape[-1], self.n_angles, self.n_sinos, d_sinos.strides[-2]
        )
        self._proj_id = astra.data3d.link("-sino", self.proj_geom, self._proj_data_link)

    def _preprocess_data(self):
        if self._use_astra_fdk:
            return
        d_sinos = self.cuda.sinos
        fdk_preweighting(
            d_sinos, self._orig_prog_geom, relative_z_position=self.relative_z_position, cor_shift=self._cor_shift
        )
        d_sinos_filtered = d_sinos
        if self._reallocate_sinos:
            d_sinos_filtered = self.cuda.sinos_contig

        for i in range(d_sinos.shape[0]):
            self.sino_filter.filter_sino(d_sinos[i], output=d_sinos_filtered[i])

    def _update_reconstruction(self):
        if self._use_astra_fdk:
            cfg = astra.astra_dict("FDK_CUDA")
        else:
            cfg = astra.astra_dict("BP3D_CUDA")
        cfg["ReconstructionDataId"] = self._vol_id
        cfg["ProjectionDataId"] = self._proj_id
        if self._alg_id is not None:
            astra.algorithm.delete(self._alg_id)
        self._alg_id = astra.algorithm.create(cfg)

    def _clip_outer_circle(self):
        if not (self.extra_options["clip_outer_circle"]):
            return
        reconstructed_volume = self.cuda.get_array("output")
        for i in range(reconstructed_volume.shape[0]):
            self._clip_circle_kernel(reconstructed_volume[i], *self._clip_circle_args, **self._clip_circle_kwargs)

    def reconstruct(self, sinos, output=None, relative_z_position=None):
        """
        sinos: numpy.ndarray or cupy array
            Sinograms, with shape (n_sinograms, n_angles, width)
        output: cupy array, optional
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
        self._clip_outer_circle()
        result = self.cuda.get_array("output")
        if output is None:
            result = result.get()
        if self.extra_options.get("scale_factor", None) is not None:
            result *= np.float32(self.extra_options["scale_factor"])  # in-place for cupy
        self.cuda.recover_arrays_references(["sinos", "output"])
        return result

    def __del__(self):
        if getattr(self, "_alg_id", None) is not None:
            astra.algorithm.delete(self._alg_id)
        if getattr(self, "_vol_id", None) is not None:
            astra.data3d.delete(self._vol_id)
        if getattr(self, "_proj_id", None) is not None:
            astra.data3d.delete(self._proj_id)


class NumpyConebeamReconstructor(ConebeamReconstructor):

    implementation = "astra"

    """
    A simpler wrapper of astra cone-beam reconstruction,
    using astra's new built-in data splitting for FDK/BP3D when it doesn't fit in GPU memory.
    It's meant to reconstruct a single, huge numpy array.
    The class name is somewhat misleading: the final BP3D step is done on GPU, but all the rest is done on CPU.
    """

    def _init_cuda(self, cuda_options):
        cuda_options = cuda_options or {}
        # Let astra use the existing context
        # Do we actually need to set_gpu_index ? It looks like astra will attach to current context
        # Note that "GPUindex" is not used anymore, see https://github.com/astra-toolbox/astra-toolbox/issues/476
        # astra.set_gpu_index(self._device_id)
        ...

    def _init_fdk(self, padding_mode, filter_name):
        self._use_astra_fdk = True
        self.padding_mode = padding_mode
        self.filter_name = filter_name or "ramlak"
        self._astra_filter_name = self.filter_name.replace("ramlak", "ram-lak")

        self._prefilter_data = padding_mode not in ["zeros", "constant"] and self.filter_name not in ["none", None]
        if self._prefilter_data:
            self._use_astra_fdk = False
            self.sino_filter = SinoFilter(
                self.sinos_shape[1:],
                filter_name=self.filter_name,
                padding_mode=self.padding_mode,
                crop_filtered_data=self._crop_filtered_data,
                extra_options={"cutoff": self.extra_options.get("filter_cutoff", 1.0)},
            )
            self.sino_filter.filter_f /= np.pi / self.sino_filter.n_angles  # done by FDK pre-weighting
            self._astra_filter_name = "none"
            fdk_weights = get_fdk_weights(
                self.sinos_shape,
                self.source_origin_dist + self.origin_detector_dist,
                self.source_origin_dist,
                zshift=self.relative_z_position,
            )
            self._fdk_weights = fdk_weights.reshape(fdk_weights.shape[0], 1, fdk_weights.shape[1])  # for 3D mult

    def _setup_clip_circle(self):
        # astra currently does not allow to retrieve GPU pointer from a data3d ID
        # Thus we have to perform clip_circle() operation on numpy arrays
        ...

    def _set_output(self, volume):
        if volume is not None:
            check_array(volume, self.vol_shape, array_name="volume", check_contiguous=False)

        if (volume is None) or not (volume.flags["C_CONTIGUOUS"]):
            self._vol_id = astra.data3d.create(
                "-vol", self.vol_geom, data=volume
            )  # volume can be None -> astra fills with 0
            self._volume = astra.data3d.get_shared(self._vol_id)
        else:
            self._volume = volume
            self._vol_id = astra.data3d.link("-vol", self.vol_geom, self._volume)

    def _set_input(self, sinos):
        check_array(sinos, self.sinos_shape, array_name="sinos", check_contiguous=False)
        # Astra cannot filter the data with padding than zeros
        # New sinograms have to be allocated if any of these conditions is True:
        #   - input sinograms are not C-contiguous
        #   - crop_filtered_data=False
        allocate_new_sinos = False
        if not (sinos.flags["C_CONTIGUOUS"]) or (self._crop_filtered_data is False):
            allocate_new_sinos = True

        if allocate_new_sinos:
            sinos_shape = sinos.shape
            if self._prefilter_data:
                sinos_shape = (self.n_sinos,) + self.sino_filter.output_shape
            self._sinos = np.zeros(sinos_shape, dtype="f")
        else:
            self._sinos = sinos
        self._sinos1 = sinos

        self._proj_id = astra.data3d.link("-sino", self.proj_geom, self._sinos)

    def _update_reconstruction(self):
        if self._use_astra_fdk:
            cfg = astra.astra_dict("FDK_CUDA")
        else:
            cfg = astra.astra_dict("BP3D_CUDA")

        cfg.update(
            {
                "ReconstructionDataId": self._vol_id,
                "ProjectionDataId": self._proj_id,
                "FilterType": self._astra_filter_name,
                # TODO "FilterParameter" , "FilterD" (to customize cutoff)
            }
        )
        if self._alg_id is not None:
            astra.algorithm.delete(self._alg_id)
        self._alg_id = astra.algorithm.create(cfg)

    def _clip_outer_circle(self):
        if not (self.extra_options["clip_outer_circle"]):
            return
        reconstructed_volume = self._volume
        out_val = self.extra_options.get("outer_circle_value", 0)
        for i in range(reconstructed_volume.shape[0]):
            reconstructed_volume[i] = clip_circle(reconstructed_volume[i], out_value=out_val)

    def _preprocess_data(self):
        if self._use_astra_fdk:
            return
        if self._prefilter_data:
            # FDK pre-weighting
            self._sinos1 *= self._fdk_weights
            # Filtering
            for i in range(self._sinos.shape[0]):
                self.sino_filter.filter_sino(self._sinos1[i], output=self._sinos[i])

    @docstring(ConebeamReconstructor.reconstruct)
    def reconstruct(self, sinos, output=None, relative_z_position=None):
        self._create_astra_proj_geometry(relative_z_position)
        self._set_input(sinos)
        self._set_output(output)
        self._preprocess_data()
        self._update_reconstruction()
        astra.algorithm.run(self._alg_id)
        self._clip_outer_circle()

        result = self._volume  # astra.data3d.get(self._vol_id)

        if self.extra_options.get("scale_factor", None) is not None:
            result *= np.float32(self.extra_options["scale_factor"])  # in-place for cupy
        return result


def selection_is_centered(size, start, stop):
    """
    Return True if (start, stop) define a selection that is centered on the middle of the array.
    """
    if stop > 0:
        stop -= size
    return stop == -start


def roi_is_centered(shape, slice_):
    """
    Return True if "slice_" define a selection that is centered on the middle of the array.
    """
    return all([selection_is_centered(shp, s.start, s.stop) for shp, s in zip(shape, slice_)])


def fdk_preweighting(d_sinos, proj_geom, relative_z_position=0.0, cor_shift=0.0):
    discontiguous_sinograms = not (d_sinos.flags.c_contiguous)

    preweight_kernel = CudaKernel(
        "devFDK_preweight",
        filename=get_cuda_srcfile("cone.cu"),
        options=("-DRADIOS_LAYOUT",) if discontiguous_sinograms else (),
    )

    n_z, n_angles, n_x = d_sinos.shape
    det_origin = sqrt(proj_geom["DistanceOriginDetector"] ** 2 + cor_shift**2)

    block = (32, 16, 1)
    grid = (updiv(n_x, block[0]), updiv(n_angles, block[1]), 1)

    preweight_kernel(
        d_sinos,
        np.uint32(n_x),  # unsigned int projPitch,
        np.uint32(0),  # unsigned int startAngle,
        np.uint32(n_angles),  # unsigned int endAngle,
        np.float32(proj_geom["DistanceOriginSource"]),  # float fSrcOrigin,
        np.float32(det_origin),  # float fDetOrigin,
        np.float32(relative_z_position),  # float fZShift,
        np.float32(proj_geom["DetectorSpacingX"]),  # float fDetUSize,
        np.float32(proj_geom["DetectorSpacingY"]),  # float fDetVSize,
        np.int32(n_angles),  # dims.iProjAngles;
        np.int32(n_x),  # dims.iProjU; // number of detectors in the U direction
        np.int32(n_z),  # dims.iProjV // number of detectors in the V direction
        block=block,
        grid=grid,
    )


def get_fdk_weights(
    sinos_shape, source_origin_distance, origin_detector_distance, cor_shift=0, du=1, dv=1, normalize=True, zshift=0
):
    """
    Get the FDK weights in the radio domain.

    Parameters
    -----------
    sinos_shape: tuple of int
        Shape of the sinograms stack, in the form (n_sinograms, n_angles, n_x).
        The detector shape is (n_z, n_x) = (n_sinograms, n_x)
    source_origin_distance:
        Distance (positive) between X-ray focal point and "origin" (sample)
    origin_detector_distance:
        Distance (positive) between "origin" (sample) and detector
    cor_shift:
        Shift (signed) between center of detector, and projection of center of rotation
    du: float
        Horizontal pixel size
    dv: float
        Vertical pixel size
    zshift:
        Current sample elevation, i.e coordinate in v of the projection of center of sample onto the detector

    Returns
    -------
    weights: numpy.ndarray
        FDK pre-weights, to be applied through a multiplication of each radio image.

    Notes
    ------
    The parameters 'source_detector_distance', 'source_origin_distance', 'du', 'dv', 'zshift' and 'cor_shift' (!)
    need to be provided with the same physical length unit.
    All can be expressed in voxel units (i.e du = dv = 1) - the normalization should then be done at another stage.
    """
    nz, na, nx = sinos_shape

    V, U = np.indices((nz, nx), dtype=np.float64)
    V -= (nz - 1) / 2
    U -= (nx - 1) / 2

    u = U * du
    v = V * dv + zshift

    origin_detector_distance = sqrt(origin_detector_distance**2 + cor_shift**2)
    source_detector_distance = source_origin_distance + origin_detector_distance

    num = source_detector_distance**2 / (du * source_origin_distance)
    if normalize:
        num *= np.pi / 2 / na
    denom = np.sqrt(source_detector_distance**2 + u**2 + v**2)

    return num / denom
