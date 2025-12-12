from enum import Enum
from packaging.version import parse as parse_version
import logging
import functools
import numpy
from tomoscan.scanbase import TomoScanBase
from tomoscan.volumebase import VolumeBase
from nxtomo.utils.transformation import build_matrix, DetYFlipTransformation
from scipy.fft import rfftn as local_fftn
from scipy.fft import irfftn as local_ifftn
from ..alignment import AlignmentAxis1, AlignmentAxis2, PaddedRawData
from ...misc import fourier_filters
from ...estimation.alignment import AlignmentBase
from ...resources.dataset_analyzer import HDF5DatasetAnalyzer
from ...resources.nxflatfield import update_dataset_info_flats_darks

try:
    import itk
except ImportError:
    has_itk = False
else:
    has_itk = True

_logger = logging.getLogger(__name__)


try:
    from skimage.registration import phase_cross_correlation
except ImportError:
    _logger.warning(
        "Unable to load skimage. Please install it if you want to use it for finding shifts from `find_relative_shifts`"
    )
    __has_sk_phase_correlation__ = False
else:
    __has_sk_phase_correlation__ = True


class ShiftAlgorithm(Enum):
    """All generic shift search algorithm"""

    NABU_FFT = "nabu-fft"
    SKIMAGE = "skimage"
    ITK_IMG_REG_V4 = "itk-img-reg-v4"
    NONE = "None"

    # In the case of shift search on radio along axis 2 (or axis x in image space) we can benefit from the existing
    # nabu algorithm such as growing-window or sliding-window
    CENTERED = "centered"
    GLOBAL = "global"
    SLIDING_WINDOW = "sliding-window"
    GROWING_WINDOW = "growing-window"
    SINO_COARSE_TO_FINE = "sino-coarse-to-fine"
    COMPOSITE_COARSE_TO_FINE = "composite-coarse-to-fine"

    @classmethod
    def from_value(cls, value):
        if value in ("", None):
            return ShiftAlgorithm.NONE
        else:
            return super().__new__(cls, value)


def find_frame_relative_shifts(
    overlap_upper_frame: numpy.ndarray,
    overlap_lower_frame: numpy.ndarray,
    estimated_shifts: tuple,
    overlap_axis: int,
    x_cross_correlation_function=None,
    y_cross_correlation_function=None,
    x_shifts_params: dict | None = None,
    y_shifts_params: dict | None = None,
):
    """
    :param overlap_axis: axis in [0, 1] on which the overlap exists. In image space. So 0 is aka y and 1 as x.
    """
    if overlap_axis not in (0, 1):
        raise ValueError(f"overlap_axis should be in (0, 1). Get {overlap_axis}")
    from nabu.stitching.config import (
        KEY_LOW_PASS_FILTER,
        KEY_HIGH_PASS_FILTER,
    )  # avoid cyclic import

    x_cross_correlation_function = ShiftAlgorithm.from_value(x_cross_correlation_function)
    y_cross_correlation_function = ShiftAlgorithm.from_value(y_cross_correlation_function)

    if x_shifts_params is None:
        x_shifts_params = {}

    if y_shifts_params is None:
        y_shifts_params = {}

    # apply filtering if any
    def _str_to_int(value):
        if isinstance(value, str):
            value = value.lstrip("'").lstrip('"')
            value = value.rstrip("'").rstrip('"')
            value = int(value)
        return value

    low_pass = _str_to_int(x_shifts_params.get(KEY_LOW_PASS_FILTER, y_shifts_params.get(KEY_LOW_PASS_FILTER, None)))
    high_pass = _str_to_int(x_shifts_params.get(KEY_HIGH_PASS_FILTER, y_shifts_params.get(KEY_HIGH_PASS_FILTER, None)))
    if high_pass is None and low_pass is None:
        pass
    else:
        if low_pass is None:
            low_pass = 1
        if high_pass is None:
            high_pass = 20
        _logger.info(f"filter image for shift search (low_pass={low_pass}, high_pass={high_pass})")
        img_filter = fourier_filters.get_bandpass_filter(
            overlap_upper_frame.shape[-2:],
            cutoff_lowpass=low_pass,
            cutoff_highpass=high_pass,
            use_rfft=True,
            data_type=overlap_upper_frame.dtype,
        )
        overlap_upper_frame = local_ifftn(
            local_fftn(overlap_upper_frame, axes=(-2, -1)) * img_filter, axes=(-2, -1)
        ).real
        overlap_lower_frame = local_ifftn(
            local_fftn(overlap_lower_frame, axes=(-2, -1)) * img_filter, axes=(-2, -1)
        ).real

    # compute shifts
    initial_shifts = numpy.array(estimated_shifts).copy()
    extra_shifts = numpy.array([0.0, 0.0])

    def skimage_proxy(img1, img2):
        if not __has_sk_phase_correlation__:
            raise ValueError("scikit-image not installed. Cannot do phase correlation from it")
        else:
            found_shift, _, _ = phase_cross_correlation(reference_image=img1, moving_image=img2, space="real")
            return -found_shift

    shift_methods = {
        ShiftAlgorithm.NABU_FFT: functools.partial(
            find_shift_correlate, img1=overlap_upper_frame, img2=overlap_lower_frame
        ),
        ShiftAlgorithm.SKIMAGE: functools.partial(skimage_proxy, img1=overlap_upper_frame, img2=overlap_lower_frame),
        ShiftAlgorithm.ITK_IMG_REG_V4: functools.partial(
            find_shift_with_itk, img1=overlap_upper_frame, img2=overlap_lower_frame
        ),
        ShiftAlgorithm.NONE: functools.partial(lambda: (0.0, 0.0)),
    }

    res_algo = {}
    for shift_alg in set((x_cross_correlation_function, y_cross_correlation_function)):  # noqa: C405
        if shift_alg not in shift_methods:
            raise ValueError(f"requested image alignment function not handled ({shift_alg})")
        try:
            res_algo[shift_alg] = shift_methods[shift_alg]()
        except Exception as e:
            _logger.error(f"Failed to find shift from {shift_alg.value}. Error is {e}")
            res_algo[shift_alg] = (0, 0)

    extra_shifts = (
        res_algo[y_cross_correlation_function][0],
        res_algo[x_cross_correlation_function][1],
    )

    final_rel_shifts = numpy.array(extra_shifts) + initial_shifts
    return tuple([int(shift) for shift in final_rel_shifts])


def find_volumes_relative_shifts(
    upper_volume: VolumeBase,
    lower_volume: VolumeBase,
    overlap_axis: int,
    estimated_shifts,
    dim_axis_1: int,
    dtype,
    flip_ud_upper_frame: bool = False,
    flip_ud_lower_frame: bool = False,
    slice_for_shift: int | str = "middle",
    x_cross_correlation_function=None,
    y_cross_correlation_function=None,
    x_shifts_params: dict | None = None,
    y_shifts_params: dict | None = None,
    alignment_axis_2="center",
    alignment_axis_1="center",
):
    """

    :param int dim_axis_1: axis 1 dimension (to handle axis 1 alignment)
    """
    if y_shifts_params is None:
        y_shifts_params = {}

    if x_shifts_params is None:
        x_shifts_params = {}
    # convert from overlap_axis (3D acquisition space) to overlap_axis_proj_space.
    if overlap_axis == 1:
        raise NotImplementedError("finding projection shift along axis 1 is not handled for projections")
    elif overlap_axis == 0:
        overlap_axis_proj_space = 0
    elif overlap_axis == 2:
        overlap_axis_proj_space = 1
    else:
        raise ValueError(f"Stitching is done in 3D space. Expect axis to be in [0,2]. Get {overlap_axis}")

    alignment_axis_2 = AlignmentAxis2(alignment_axis_2)
    alignment_axis_1 = AlignmentAxis1(alignment_axis_1)
    assert dim_axis_1 > 0, "dim_axis_1 <= 0"

    if isinstance(slice_for_shift, str):
        if slice_for_shift == "first":
            slice_for_shift = 0
        elif slice_for_shift == "last":
            slice_for_shift = dim_axis_1
        elif slice_for_shift == "middle":
            slice_for_shift = dim_axis_1 // 2
        else:
            raise ValueError("invalid slice provided to search shift", slice_for_shift)

    def get_slice_along_axis_1(volume: VolumeBase, index: int):
        assert isinstance(index, int), f"index should be an int, {type(index)} provided"
        volume_shape = volume.get_volume_shape()
        if alignment_axis_1 is AlignmentAxis1.BACK:
            front_empty_width = dim_axis_1 - volume_shape[1]
            if index < front_empty_width:
                return PaddedRawData.get_empty_frame(shape=(volume_shape[0], volume_shape[2]), dtype=dtype)
            else:
                return volume.get_slice(index=index - front_empty_width, axis=1)
        elif alignment_axis_1 is AlignmentAxis1.FRONT:
            if index >= volume_shape[1]:
                return PaddedRawData.get_empty_frame(shape=(volume_shape[0], volume_shape[2]), dtype=dtype)
            else:
                return volume.get_slice(index=index, axis=1)
        elif alignment_axis_1 is AlignmentAxis1.CENTER:
            front_empty_width = (dim_axis_1 - volume_shape[1]) // 2
            back_empty_width = dim_axis_1 - front_empty_width
            if index < front_empty_width or index > back_empty_width:
                return PaddedRawData.get_empty_frame(shape=(volume_shape[0], volume_shape[2]), dtype=dtype)
            else:
                return volume.get_slice(index=index - front_empty_width, axis=1)
        else:
            raise TypeError(f"unmanaged alignment mode {alignment_axis_1.value}")

    upper_frame = get_slice_along_axis_1(upper_volume, index=slice_for_shift)
    lower_frame = get_slice_along_axis_1(lower_volume, index=slice_for_shift)
    if flip_ud_upper_frame:
        upper_frame = numpy.flipud(upper_frame.copy())
    if flip_ud_lower_frame:
        lower_frame = numpy.flipud(lower_frame.copy())

    from nabu.stitching.config import KEY_WINDOW_SIZE  # avoid cyclic import

    w_window_size = int(y_shifts_params.get(KEY_WINDOW_SIZE, 400))
    start_overlap = max(estimated_shifts[0] // 2 - w_window_size // 2, 0)
    end_overlap = min(estimated_shifts[0] // 2 + w_window_size // 2, upper_frame.shape[0], lower_frame.shape[0])

    if start_overlap == 0:
        overlap_upper_frame = upper_frame[-end_overlap:]
    else:
        overlap_upper_frame = upper_frame[-end_overlap:-start_overlap]
    overlap_lower_frame = lower_frame[start_overlap:end_overlap]

    # align if necessary
    if overlap_upper_frame.shape[1] != overlap_lower_frame.shape[1]:
        overlap_frame_width = min(overlap_upper_frame.shape[1], overlap_lower_frame.shape[1])
        if alignment_axis_2 is AlignmentAxis2.CENTER:
            upper_frame_left_pos = overlap_upper_frame.shape[1] // 2 - overlap_frame_width // 2
            upper_frame_right_pos = upper_frame_left_pos + overlap_frame_width
            overlap_upper_frame = overlap_upper_frame[:, upper_frame_left_pos:upper_frame_right_pos]

            lower_frame_left_pos = overlap_lower_frame.shape[1] // 2 - overlap_frame_width // 2
            lower_frame_right_pos = lower_frame_left_pos + overlap_frame_width
            overlap_lower_frame = overlap_lower_frame[:, lower_frame_left_pos:lower_frame_right_pos]
        elif alignment_axis_2 is AlignmentAxis2.LEFT:
            overlap_upper_frame = overlap_upper_frame[:, :overlap_frame_width]
            overlap_lower_frame = overlap_lower_frame[:, :overlap_frame_width]
        elif alignment_axis_2 is AlignmentAxis2.RIGTH:
            overlap_upper_frame = overlap_upper_frame[:, -overlap_frame_width:]
            overlap_lower_frame = overlap_lower_frame[:, -overlap_frame_width:]
        else:
            raise ValueError(f"Alignement {alignment_axis_2.value} is not handled")

    if not overlap_upper_frame.shape == overlap_lower_frame.shape:
        raise ValueError(f"Fail to get consistant overlap ({overlap_upper_frame.shape} vs {overlap_lower_frame.shape})")

    return find_frame_relative_shifts(
        overlap_upper_frame=overlap_upper_frame,
        overlap_lower_frame=overlap_lower_frame,
        estimated_shifts=estimated_shifts,
        x_cross_correlation_function=x_cross_correlation_function,
        y_cross_correlation_function=y_cross_correlation_function,
        x_shifts_params=x_shifts_params,
        y_shifts_params=y_shifts_params,
        overlap_axis=overlap_axis_proj_space,
    )


from nabu.pipeline.estimators import estimate_cor


def find_projections_relative_shifts(
    upper_scan: TomoScanBase,
    lower_scan: TomoScanBase,
    estimated_shifts: tuple,
    axis: int,
    flip_ud_upper_frame: bool = False,
    flip_ud_lower_frame: bool = False,
    projection_for_shift: int | str = "middle",
    invert_order: bool = False,
    x_cross_correlation_function=None,
    y_cross_correlation_function=None,
    x_shifts_params: dict | None = None,
    y_shifts_params: dict | None = None,
) -> tuple:
    """
    deduce the relative shift between the two scans.
    Expected behavior:
    * compute expected overlap area from z_translations and (sample) pixel size
    * call an (optional) cross correlation function from the overlap area to compute the x shift and polish the y shift from `projection_for_shift`

    :param TomoScanBase scan_0:
    :param TomoScanBase scan_1:
    :param tuple estimated_shifts: 'a priori' shift estimation
    :param int axis: axis on which the overlap / stitching is happening. In the 3D space (sample, detector referential)
    :param bool flip_ud_upper_frame: is the upper frame flipped
    :param bool flip_ud_lower_frame: is the lower frame flipped
    :param projection_for_shift: index for the projection to use (in projection space or scan space?). If str must be in (`middle`, `first`, `last`)
    :param bool invert_order: are projections inverted between the two scans (case if rotation angle are inverted)
    :param str x_cross_correlation_function: optional method to refine x shift from computing cross correlation. For now valid values are: ("skimage", "nabu-fft")
    :param str y_cross_correlation_function: optional method to refine y shift from computing cross correlation. For now valid values are: ("skimage", "nabu-fft")
    :param x_shifts_params: parameters to find the shift over x
    :param y_shifts_params: parameters to find the shift over y
    :return: relative shift of scan_1 with scan_0 as reference: (y_shift, x_shift)
    :rtype: tuple

    :warning: this function will flip left-right and up-down frames by default. So it will return shift according to this information
    """
    if x_shifts_params is None:
        x_shifts_params = {}
    if y_shifts_params is None:
        y_shifts_params = {}

    # convert from overlap_axis (3D acquisition space) to overlap_axis_proj_space.
    if axis == 1:
        axis_proj_space = 1
    elif axis == 0:
        axis_proj_space = 0
    elif axis == 2:
        raise NotImplementedError(
            "finding projection shift along axis 1 (x-ray direction) is not handled for projections"
        )
    else:
        raise ValueError(f"Stitching is done in 3D space. Expect axis to be in [0,2]. Get {axis}")

    x_cross_correlation_function = ShiftAlgorithm.from_value(x_cross_correlation_function)
    y_cross_correlation_function = ShiftAlgorithm.from_value(y_cross_correlation_function)

    # { handle specific use case (finding shift on scan) - when using nabu COR algorithms (for axis 2)
    if x_cross_correlation_function in (
        ShiftAlgorithm.SINO_COARSE_TO_FINE,
        ShiftAlgorithm.COMPOSITE_COARSE_TO_FINE,
        ShiftAlgorithm.CENTERED,
        ShiftAlgorithm.GLOBAL,
        ShiftAlgorithm.GROWING_WINDOW,
        ShiftAlgorithm.SLIDING_WINDOW,
    ):
        cor_options = x_shifts_params.copy()
        cor_options.pop("img_reg_method", None)
        # remove all none numeric options because estimate_cor will call 'literal_eval' on them

        upper_scan_dataset_info = HDF5DatasetAnalyzer(
            location=upper_scan.master_file, extra_options={"hdf5_entry": upper_scan.entry}
        )
        update_dataset_info_flats_darks(upper_scan_dataset_info, flatfield_mode=1)

        upper_scan_pos = estimate_cor(
            method=x_cross_correlation_function.value,
            dataset_info=upper_scan_dataset_info,
            cor_options=cor_options,
        )
        lower_scan_dataset_info = HDF5DatasetAnalyzer(
            location=lower_scan.master_file, extra_options={"hdf5_entry": lower_scan.entry}
        )
        update_dataset_info_flats_darks(lower_scan_dataset_info, flatfield_mode=1)
        lower_scan_pos = estimate_cor(
            method=x_cross_correlation_function.value,
            dataset_info=lower_scan_dataset_info,
            cor_options=cor_options,
        )

        estimated_shifts = [
            estimated_shifts[0],
            (lower_scan_pos - upper_scan_pos),
        ]
        x_cross_correlation_function = ShiftAlgorithm.NONE

    # } else we will compute shift from the flat projections

    def get_flat_fielded_proj(
        scan: TomoScanBase, proj_index: int, reverse: bool, transformation_matrix: numpy.ndarray | None
    ):
        first_proj_idx = sorted(lower_scan.projections.keys(), reverse=reverse)[proj_index]
        ff = scan.flat_field_correction(
            (scan.projections[first_proj_idx],),
            (first_proj_idx,),
        )[0]
        assert ff.ndim == 2, f"expects a single 2D frame. Get something with {ff.ndim} dimensions"
        if transformation_matrix is not None:
            assert (
                transformation_matrix.ndim == 2
            ), f"expects a 2D transformation matrix. Get a {transformation_matrix.ndim} D"
            if numpy.isclose(transformation_matrix[2, 2], -1):
                transformation_matrix[2, :] = 0
                transformation_matrix[0, 2] = 0
                transformation_matrix[2, 2] = 1
                ff = numpy.flipud(ff)
        return ff

    if isinstance(projection_for_shift, str):
        if projection_for_shift.lower() == "first":
            projection_for_shift = 0
        elif projection_for_shift.lower() == "last":
            projection_for_shift = -1
        elif projection_for_shift.lower() == "middle":
            projection_for_shift = len(upper_scan.projections) // 2
        else:
            try:
                projection_for_shift = int(projection_for_shift)
            except ValueError:
                raise ValueError(
                    f"{projection_for_shift} cannot be cast to an int and is not one of the possible ('first', 'last', 'middle')"
                )
    elif not isinstance(projection_for_shift, (int, numpy.number)):
        raise TypeError(
            f"projection_for_shift is expected to be an int. Not {type(projection_for_shift)} - {projection_for_shift}"
        )

    upper_scan_transformations = list(upper_scan.get_detector_transformations(tuple()))
    if flip_ud_upper_frame:
        upper_scan_transformations.append(DetYFlipTransformation(flip=True))
    upper_scan_trans_matrix = build_matrix(upper_scan_transformations)
    lower_scan_transformations = list(lower_scan.get_detector_transformations(tuple()))
    if flip_ud_lower_frame:
        lower_scan_transformations.append(DetYFlipTransformation(flip=True))
    lower_scan_trans_matrix = build_matrix(lower_scan_transformations)
    upper_proj = get_flat_fielded_proj(
        upper_scan,
        projection_for_shift,
        reverse=False,
        transformation_matrix=upper_scan_trans_matrix,
    )
    lower_proj = get_flat_fielded_proj(
        lower_scan,
        projection_for_shift,
        reverse=invert_order,
        transformation_matrix=lower_scan_trans_matrix,
    )

    from nabu.stitching.config import KEY_WINDOW_SIZE  # avoid cyclic import

    if axis_proj_space == 0:
        w_window_size = int(y_shifts_params.get(KEY_WINDOW_SIZE, 400))
    else:
        w_window_size = int(x_shifts_params.get(KEY_WINDOW_SIZE, 400))
    start_overlap = max(estimated_shifts[axis_proj_space] // 2 - w_window_size // 2, 0)
    end_overlap = min(
        estimated_shifts[axis_proj_space] // 2 + w_window_size // 2,
        upper_proj.shape[axis_proj_space],
        lower_proj.shape[axis_proj_space],
    )
    o_upper_sel = numpy.array(range(-end_overlap, -start_overlap))
    overlap_upper_frame = numpy.take_along_axis(
        upper_proj,
        o_upper_sel[:, None] if axis_proj_space == 0 else o_upper_sel[None, :],
        axis=axis_proj_space,
    )
    o_lower_sel = numpy.array(range(start_overlap, end_overlap))
    overlap_lower_frame = numpy.take_along_axis(
        lower_proj,
        o_lower_sel[:, None] if axis_proj_space == 0 else o_upper_sel[None, :],
        axis=axis_proj_space,
    )

    if not overlap_upper_frame.shape == overlap_lower_frame.shape:
        raise ValueError(f"Fail to get consistent overlap ({overlap_upper_frame.shape} vs {overlap_lower_frame.shape})")

    return find_frame_relative_shifts(
        overlap_upper_frame=overlap_upper_frame,
        overlap_lower_frame=overlap_lower_frame,
        estimated_shifts=estimated_shifts,
        x_cross_correlation_function=x_cross_correlation_function,
        y_cross_correlation_function=y_cross_correlation_function,
        x_shifts_params=x_shifts_params,
        y_shifts_params=y_shifts_params,
        overlap_axis=axis_proj_space,
    )


def find_shift_correlate(img1, img2, padding_mode="reflect"):
    alignment = AlignmentBase()
    cc = alignment._compute_correlation_fft(
        img1,
        img2,
        padding_mode,
    )

    img_shape = cc.shape  # Because cc.shape can differ from img_2.shape (e.g. in case of odd nb of cols)
    cc_vs = numpy.fft.fftfreq(img_shape[-2], 1 / img_shape[-2])
    cc_hs = numpy.fft.fftfreq(img_shape[-1], 1 / img_shape[-1])

    (f_vals, fv, fh) = alignment.extract_peak_region_2d(cc, cc_vs=cc_vs, cc_hs=cc_hs)
    shifts_vh = alignment.refine_max_position_2d(f_vals, fv, fh)
    return -shifts_vh


def find_shift_with_itk(img1: numpy.ndarray, img2: numpy.ndarray) -> tuple:
    # created from https://examples.itk.org/src/registration/common/perform2dtranslationregistrationwithmeansquares/documentation
    # return (y_shift, x_shift). For now shift are integers as only integer shift are handled.
    if not img1.dtype == img2.dtype:
        raise ValueError("the two images are expected to have the same type")
    if not img1.ndim == img2.ndim == 2:
        raise ValueError("the two images are expected to 2D numpy arrays")

    if not has_itk:
        _logger.warning("itk is not installed. Please install it to find shift with it")
        return (0, 0)

    if parse_version(itk.Version.GetITKVersion()) < parse_version("4.9.0"):
        _logger.error("ITK 4.9.0 is required to find shift with it.")
        return (0, 0)

    pixel_type = itk.ctype("float")
    img1 = numpy.ascontiguousarray(img1, dtype=numpy.float32)
    img2 = numpy.ascontiguousarray(img2, dtype=numpy.float32)

    dimension = 2
    image_type = itk.Image[pixel_type, dimension]

    fixed_image = itk.PyBuffer[image_type].GetImageFromArray(img1)
    moving_image = itk.PyBuffer[image_type].GetImageFromArray(img2)

    transform_type = itk.TranslationTransform[itk.D, dimension]
    initial_transform = transform_type.New()

    optimizer = itk.RegularStepGradientDescentOptimizerv4.New(
        LearningRate=4,
        MinimumStepLength=0.001,
        RelaxationFactor=0.5,
        NumberOfIterations=200,
    )

    metric = itk.MeanSquaresImageToImageMetricv4[image_type, image_type].New()

    registration = itk.ImageRegistrationMethodv4.New(
        FixedImage=fixed_image,
        MovingImage=moving_image,
        Metric=metric,
        Optimizer=optimizer,
        InitialTransform=initial_transform,
    )

    moving_initial_transform = transform_type.New()
    initial_parameters = moving_initial_transform.GetParameters()
    initial_parameters[0] = 0
    initial_parameters[1] = 0
    moving_initial_transform.SetParameters(initial_parameters)
    registration.SetMovingInitialTransform(moving_initial_transform)

    identity_transform = transform_type.New()
    identity_transform.SetIdentity()
    registration.SetFixedInitialTransform(identity_transform)

    registration.SetNumberOfLevels(1)
    registration.SetSmoothingSigmasPerLevel([0])
    registration.SetShrinkFactorsPerLevel([1])

    registration.Update()

    transform = registration.GetTransform()
    final_parameters = transform.GetParameters()
    translation_along_x = final_parameters.GetElement(0)
    translation_along_y = final_parameters.GetElement(1)

    return numpy.round(translation_along_y), numpy.round(translation_along_x)


def from_slice_to_n_elements(slice_: slice | tuple):
    """Return the number of element in a slice or in a tuple"""
    if isinstance(slice_, slice):
        return (slice_.stop - slice_.start) / (slice_.step or 1)
    else:
        return len(slice_)
