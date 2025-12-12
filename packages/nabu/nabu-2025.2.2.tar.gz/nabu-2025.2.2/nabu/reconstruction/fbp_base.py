import warnings
import numpy as np
from ..utils import updiv, nextpow2, convert_index, deprecation_warning
from ..processing.processing_base import ProcessingBase
from .filtering import SinoFilter
from .sinogram import SinoMult
from .sinogram import get_extended_sinogram_width


def rot_center_is_in_middle_of_roi(rot_center, roi, tol=2.0):
    # NB. tolerance should be at least 2,
    # because in halftomo the extended sinogram width is 2*sino_width - int(2 * XXXX)
    #   (where  XXX depends on whether the CoR is on the left or on the right)
    #  because of the int(2 * stuff), we can have a jump of at most two pixels.
    #
    start_x, end_x, start_y, end_y = roi
    return (
        abs((start_x + end_x - 1) / 2 - rot_center) - 0.5 < tol
        and abs((start_y + end_y - 1) / 2 - rot_center) - 0.5 < tol
    )


class BackprojectorBase:
    """
    Base class for backprojectors.
    """

    backend = "numpy"
    default_padding_mode = "zeros"
    kernel_name = "backproj"
    default_extra_options = {
        "padding_mode": None,  # deprecated
        "axis_correction": None,
        "centered_axis": False,
        "clip_outer_circle": False,
        "scale_factor": None,
        "filter_cutoff": 1.0,
        "outer_circle_value": 0.0,
        "crop_filtered_data": True,
    }

    kernel_filename = None
    backend_processing_class = ProcessingBase
    SinoFilterClass = SinoFilter
    SinoMultClass = SinoMult
    _sino_filter_other_options = {}

    def __init__(
        self,
        sino_shape,
        slice_shape=None,
        angles=None,
        rot_center=None,
        padding_mode=None,
        halftomo=False,
        filter_name=None,
        slice_roi=None,
        scale_factor=None,
        extra_options=None,
        backend_options=None,
    ):
        """
        Initialize a Backprojector.

        Parameters
        -----------
        sino_shape: tuple
            Shape of the sinogram, in the form `(n_angles, detector_width)`
            (for backprojecting one sinogram) or `(n_sinos, n_angles, detector_width)`.
        slice_shape: int or tuple, optional
            Shape of the slice. By default, the slice shape is (n_x, n_x) where
            `n_x = detector_width`
        angles: array-like, optional
            Rotation angles in radians.
            By default, angles are equispaced between [0, pi[.
        rot_center: float, optional
            Rotation axis position. Default is `(detector_width - 1)/2.0`
        padding_mode: str, optional
            Padding mode when filtering the sinogram. Can be "zeros" (default) or "edges".
        filter_name: str, optional
            Name of the filter for filtered-backprojection.
        slice_roi: tuple, optional.
            Whether to backproject in a restricted area.
            If set, it must be in the form (start_x, end_x, start_y, end_y).
            `end_x` and `end_y` are non inclusive ! For example if the detector has
            2048 pixels horizontally, then you can choose `start_x=0` and `end_x=2048`.
            If one of the value is set to None, it is replaced with a default value
            (0 for start, n_x and n_y for end)
        scale_factor: float, optional
            Scaling factor for backprojection.
            For example, to get the linear absorption coefficient in 1/cm,
            this factor has to be set as the pixel size in cm.
            DEPRECATED - please use this parameter in "extra_options"
        extra_options: dict, optional
            Advanced extra options.
             See the "Extra options" section for more information.
        backend_options: dict, optional
            OpenCL/Cuda options passed to the OpenCLProcessing or CudaProcessing class.

        Other Parameters
        -----------------
        extra_options: dict, optional
            Dictionary with a set of advanced options. The default are the following:
                - "padding_mode": "zeros"
                   Padding mode when filtering the sinogram. Can be "zeros" or "edges".
                   DEPRECATED - please use "padding_mode" directly in parameters.
                - "axis_correction": None
                    Whether to set a correction for the rotation axis.
                    If set, this should be an array with as many elements as the number
                    of angles. This is useful when there is an horizontal displacement
                    of the rotation axis.
                - centered_axis: bool
                    Whether to "center" the slice on the rotation axis position.
                    If set to True, then the reconstructed region is centered on the rotation axis.
                - scale_factor: float
                    Scaling factor for backprojection.
                    For example, to get the linear absorption coefficient in 1/cm,
                    this factor has to be set as the pixel size in cm.
                - clip_outer_circle: False
                    Whether to set to zero the pixels outside the reconstruction mask
                - filter_cutoff: float
                    Cut-off frequency usef for Fourier filter. Default is 1.0
        """
        self._processing = self.backend_processing_class(**(backend_options or {}))
        self._configure_extra_options(scale_factor, padding_mode, extra_options=extra_options)
        self._check_textures_availability()
        self._init_geometry(sino_shape, slice_shape, angles, rot_center, halftomo, slice_roi)
        self._init_filter(filter_name)
        self._allocate_memory()
        self._compute_angles()
        self._compile_kernels()

    def _configure_extra_options(self, scale_factor, padding_mode, extra_options=None):
        extra_options = extra_options or {}
        # compat.
        scale_factor = None
        if scale_factor is not None:
            deprecation_warning(
                "Please use the parameter 'scale_factor' in the 'extra_options' dict",
                do_print=True,
                func_name="fbp_scale_factor",
            )
        scale_factor = extra_options.get("scale_factor", None) or scale_factor or 1.0
        #
        if "padding_mode" in extra_options:
            deprecation_warning(
                "Please use 'padding_mode' directly in Backprojector arguments, not in 'extra_options'",
                do_print=True,
                func_name="fbp_padding_mode",
            )
        #
        self._backproj_scale_factor = scale_factor
        self._axis_array = None
        self.extra_options = self.default_extra_options.copy()
        self.extra_options.update(extra_options)
        self.padding_mode = padding_mode or self.extra_options["padding_mode"] or self.default_padding_mode
        self._axis_array = self.extra_options["axis_correction"]

    def _init_geometry(self, sino_shape, slice_shape, angles, rot_center, halftomo, slice_roi):
        if slice_shape is not None and slice_roi is not None:
            raise ValueError("slice_shape and slice_roi cannot be used together")
        self.sino_shape = sino_shape
        if len(sino_shape) == 2:
            n_angles, dwidth = sino_shape
        else:
            raise ValueError("Expected 2D sinogram")
        self.dwidth = dwidth
        self.halftomo = halftomo
        if rot_center is None:
            if halftomo:
                raise ValueError("Need to know 'rot_center' when using halftomo")
            rot_center = (self.dwidth - 1) / 2.0
        self.rot_center = rot_center
        self._set_slice_shape(slice_shape)
        self.axis_pos = self.rot_center
        self._set_angles(angles, n_angles)
        self._set_slice_roi(slice_roi)
        if self.extra_options["centered_axis"]:
            self.offsets = {
                "x": self.rot_center - (self.n_x - 1) / 2.0,
                "y": self.rot_center - (self.n_y - 1) / 2.0,
            }
        #
        self._set_axis_corr()

    def _set_slice_shape(self, slice_shape):
        if not (self.halftomo):
            n_x = n_y = self.dwidth
        else:
            n_x = n_y = get_extended_sinogram_width(self.dwidth, self.rot_center)
        if slice_shape is not None:
            if np.isscalar(slice_shape):
                slice_shape = (slice_shape, slice_shape)
            n_y, n_x = slice_shape
        self.n_x = n_x
        self.n_y = n_y
        self.slice_shape = (n_y, n_x)

    def _set_angles(self, angles, n_angles):
        self.n_angles = n_angles
        if angles is None:
            angles = n_angles
        if np.isscalar(angles):
            end_angle = np.pi if not (self.halftomo) else 2 * np.pi
            take_end_angle = self.halftomo
            angles = np.linspace(0, end_angle, angles, take_end_angle)
        else:
            assert len(angles) == self.n_angles, "expected %d angles but got %d" % (len(angles), self.n_angles)
        self.angles = angles

    def _set_slice_roi(self, slice_roi):
        self.offsets = {"x": 0, "y": 0}
        self.slice_roi = slice_roi
        if slice_roi is None:
            return
        start_x, end_x, start_y, end_y = slice_roi
        # convert negative indices
        start_x = convert_index(start_x, self.n_x, 0)
        start_y = convert_index(start_y, self.n_y, 0)
        end_x = convert_index(end_x, self.n_x, self.n_x)
        end_y = convert_index(end_y, self.n_y, self.n_y)
        self.slice_shape = (end_y - start_y, end_x - start_x)
        if self.extra_options["centered_axis"] and not (
            rot_center_is_in_middle_of_roi(self.rot_center, (start_x, end_x, start_y, end_y))
        ):
            warnings.warn(
                "Using 'centered_axis' when doing a non-centered ROI reconstruction might have side effects: 'start_xy' and 'end_xy' have a different meaning",
                RuntimeWarning,
            )
            # self.extra_options["centered_axis"] = False
        self.n_x = self.slice_shape[-1]
        self.n_y = self.slice_shape[-2]
        self.offsets = {"x": start_x, "y": start_y}

    def _allocate_memory(self):
        # 1D textures are not supported in pyopencl
        self.h_msin = np.zeros((1, self.n_angles), "f")
        self.h_cos = np.zeros((1, self.n_angles), "f")
        # self._d_sino = self._processing.allocate_array("d_sino", self.sino_shape, "f")
        self._processing.init_arrays_to_none(["_d_slice", "d_sino"])

    def _compute_angles(self):
        self.h_cos[0] = np.cos(self.angles).astype("f")
        self.h_msin[0] = (-np.sin(self.angles)).astype("f")
        self._d_msin = self._processing.set_array("d_msin", self.h_msin[0])
        self._d_cos = self._processing.set_array("d_cos", self.h_cos[0])
        if self._axis_correction is not None:
            self._d_axcorr = self._processing._set_array("d_axcorr", self._axis_correction)

    def _set_axis_corr(self):
        axcorr = self.extra_options["axis_correction"]
        self._axis_correction = axcorr
        if axcorr is None:
            return
        if len(axcorr) != self.n_angles:
            raise ValueError("Expected %d angles but got %d" % (self.n_angles, len(axcorr)))
        self._axis_correction = np.zeros((1, self.n_angles), dtype=np.float32)
        self._axis_correction[0, :] = axcorr[:]  # pylint: disable=E1136

    def _get_filter_init_extra_options(self):
        return {}

    def _init_filter(self, filter_name):
        self.filter_name = filter_name
        if filter_name in ["None", "none"]:
            self.sino_filter = None
            return

        # TODO
        if not (self.extra_options.get("crop_filtered_data", True)):
            warnings.warn("crop_filtered_data = False is not supported for FBP yet", RuntimeWarning)
        #
        sinofilter_other_kwargs = self._get_filter_init_extra_options()
        self.sino_filter = self.SinoFilterClass(
            self.sino_shape,
            filter_name=self.filter_name,
            padding_mode=self.padding_mode,
            extra_options={"cutoff": self.extra_options.get("filter_cutoff", 1.0)},
            **sinofilter_other_kwargs,
        )
        if self.halftomo:
            # When doing half-tomography, each projections is seen "twice".
            # SinoFilter normalizes with pi/n_angles, but in half-tomography here n_angles is somehow halved.
            # TODO it should even be "n_turns", where n_turns can be computed from the angles
            self.sino_filter.set_filter(self.sino_filter.filter_f * (self.n_angles / np.pi * 2))

    def reset_rot_center(self, rot_center):
        """
        Define a new center of rotation for the current backprojector.
        """
        self.rot_center = rot_center
        self.axis_pos = rot_center
        proj_arg_idx = 4
        self.kern_proj_args[proj_arg_idx] = np.float32(rot_center)
        if self.extra_options["centered_axis"]:
            self.offsets = {
                "x": self.rot_center - (self.n_x - 1) / 2.0,
                "y": self.rot_center - (self.n_y - 1) / 2.0,
            }
            self.kern_proj_args[proj_arg_idx + 3] = np.float32(self.offsets["x"])
            self.kern_proj_args[proj_arg_idx + 4] = np.float32(self.offsets["y"])

    # Try to factorize some code between Cuda and OpenCL
    # Not ideal, as cuda uses "grid" = n_blocks_launched,
    # while OpenCL uses "global_size" = n_threads_launched
    def _get_kernel_options(self):
        sourcemodule_options = []
        # We use blocks of 16*16 (see why in kernel doc), and one thread
        # handles 2 pixels per dimension.
        block = (16, 16, 1)
        # The Cuda kernel is optimized for 16x16 threads blocks
        # If one of the dimensions is smaller than 16, it has to be addapted
        if self.n_x < 16 or self.n_y < 16:
            tpb_x = min(int(nextpow2(self.n_x)), 16)
            tpb_y = min(int(nextpow2(self.n_y)), 16)
            block = (tpb_x, tpb_y, 1)
            sourcemodule_options.append("-DSHARED_SIZE=%d" % (tpb_x * tpb_y))
        grid = (updiv(updiv(self.n_x, block[0]), 2), updiv(updiv(self.n_y, block[1]), 2))
        shared_size = int(np.prod(block)) * 2
        if self._axis_correction is not None:
            sourcemodule_options.append("-DDO_AXIS_CORRECTION")
            shared_size += int(np.prod(block))
        shared_size *= 4  # sizeof(float32)
        self._kernel_options = {
            "kernel_name": self.kernel_name,
            "sourcemodule_options": sourcemodule_options,
            "grid": grid,
            "block": block,
            "shared_size": shared_size,
        }

    def _prepare_kernel_args(self):
        self._get_kernel_options()
        self.kern_proj_args = [
            None,  # output d_slice holder
            None,  # placeholder for sino (OpenCL or Cuda+no-texture)
            np.int32(self.n_angles),
            np.int32(self.dwidth),
            np.float32(self.axis_pos),
            np.int32(self.n_x),
            np.int32(self.n_y),
            np.float32(self.offsets["x"]),
            np.float32(self.offsets["y"]),
            self._d_cos,
            self._d_msin,
            np.float32(self._backproj_scale_factor),
        ]
        if self._axis_correction is not None:
            self.kern_proj_args.insert(-1, self._d_axcorr)
        self.kern_proj_kwargs = {
            "grid": self._kernel_options["grid"],
            "block": self._kernel_options["block"],
        }
        if self.extra_options.get("clip_outer_circle", False):
            self._clip_circle_args = [
                np.int32(self.slice_shape[1]),
                np.int32(self.slice_shape[0]),
                np.float32((self.slice_shape[1] - 1) / 2),
                np.float32((self.slice_shape[0] - 1) / 2),
                np.float32(self.extra_options.get("outer_circle_value", 0)),
            ]

    def _set_output(self, output, check=False):
        self._output_is_ndarray = isinstance(output, np.ndarray)
        if output is None or self._output_is_ndarray:
            self._processing.allocate_array("_d_slice", self.slice_shape, dtype=np.float32)
            output = self._processing._d_slice  # pylint: disable=E1101
        elif check:
            assert output.dtype == np.float32
            assert output.shape == self.slice_shape, "Expected output shape %s but got %s" % (
                self.slice_shape,
                output.shape,
            )
        return output

    def _set_kernel_slice_arg(self, d_slice):
        self.kern_proj_args[0] = d_slice

    def backproj(self, sino, output=None, do_checks=True):
        if self.halftomo and self.rot_center < self.dwidth:
            sino = self.sino_mult.prepare_sino(sino)
        self._transfer_to_texture(sino)
        d_slice = self._set_output(output, check=do_checks)
        self._set_kernel_slice_arg(d_slice)
        self.gpu_projector(*self.kern_proj_args, **self.kern_proj_kwargs)
        if self.extra_options["clip_outer_circle"]:
            self._clip_circle_kernel(d_slice, *self._clip_circle_args, **self._clip_circle_kwargs)
        if output is not None and not (self._output_is_ndarray):
            return output
        else:
            return self._get_slice_into(output)

    def _get_slice_into(self, output):
        return self._processing._d_slice.get(output)

    def filtered_backprojection(self, sino, output=None):
        #
        if isinstance(sino, self._processing.array_class):
            d_sino = sino
        else:
            d_sino = self._processing.to_device("d_sino", sino)
        #
        if self.sino_filter is not None:
            filt_kwargs = {}
            # if a new device array was allocated for sinogram, then the filtering can overwrite it,
            # since it won't affect user argument
            if id(d_sino) != id(sino):
                # if id(d_sino) != id(sino) and self.extra_options.get("crop_filtered_data", True):
                filt_kwargs = {"output": d_sino}
            #
            sino_to_backproject = self.sino_filter(d_sino, **filt_kwargs)
        else:
            sino_to_backproject = d_sino
        return self.backproj(sino_to_backproject, output=output)

    fbp = filtered_backprojection  # shorthand

    def __repr__(self):
        res = "%s(sino_shape=%s, slice_shape=%s, rot_center=%.2f, halftomo=%s)" % (
            self.__class__.__name__,
            str(self.sino_shape),
            str(self.slice_shape),
            self.rot_center,
            self.halftomo,
        )
        return res
