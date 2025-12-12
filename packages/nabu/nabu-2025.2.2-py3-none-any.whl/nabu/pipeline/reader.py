from multiprocessing.pool import ThreadPool
import numpy as np

from nabu.utils import get_num_threads
from ..misc.binning import binning as image_binning
from ..io.reader import NXTomoReader, EDFStackReader


#
# NXTomoReader with binning
#
def bin_image_stack(src_stack, dst_stack, binning_factor=(2, 2), num_threads=8):
    def _apply_binning(img_res_tuple):
        img, res = img_res_tuple
        res[:] = image_binning(img, binning_factor)

    if dst_stack is None:
        dst_stack = np.zeros((src_stack.shape[0],) + image_binning(src_stack[0], binning_factor).shape, dtype="f")

    with ThreadPool(num_threads) as tp:
        tp.map(_apply_binning, zip(src_stack, dst_stack))
    return dst_stack


def NXTomoReaderBinning(binning_factor, *nxtomoreader_args, num_threads=None, **nxtomoreader_kwargs):
    [
        nxtomoreader_kwargs.pop(kwarg, None)
        for kwarg in ["processing_func", "processing_func_args", "processing_func_kwargs"]
    ]
    nxtomoreader_kwargs["processing_func"] = bin_image_stack
    nxtomoreader_kwargs["processing_func_kwargs"] = {
        "binning_factor": binning_factor,
        "num_threads": num_threads or get_num_threads(),
    }

    return NXTomoReader(
        *nxtomoreader_args,
        **nxtomoreader_kwargs,
    )


#
# NXTomoReader with distortion correction
#


def apply_distortion_correction_on_images_stack(src_stack, dst_stack, distortion_corrector, num_threads=8):
    _, subregion = distortion_corrector.get_actual_shapes_source_target()
    src_x_start, src_x_end, src_z_start, src_z_end = subregion
    if dst_stack is None:
        dst_stack = np.zeros([src_stack.shape[0], src_z_end - src_z_start, src_x_end - src_x_start], "f")

    def apply_corrector(i_img_tuple):
        i, img = i_img_tuple
        dst_stack[i] = distortion_corrector.transform(img)

    with ThreadPool(num_threads) as tp:
        tp.map(apply_corrector, enumerate(src_stack))

    return dst_stack


def NXTomoReaderDistortionCorrection(distortion_corrector, *nxtomoreader_args, num_threads=None, **nxtomoreader_kwargs):
    [
        nxtomoreader_kwargs.pop(kwarg, None)
        for kwarg in ["processing_func", "processing_func_args", "processing_func_kwargs"]
    ]
    nxtomoreader_kwargs["processing_func"] = apply_distortion_correction_on_images_stack
    nxtomoreader_kwargs["processing_func_args"] = [distortion_corrector]
    nxtomoreader_kwargs["processing_func_kwargs"] = {"num_threads": num_threads or get_num_threads()}

    return NXTomoReader(
        *nxtomoreader_args,
        **nxtomoreader_kwargs,
    )


#
# EDF Reader with binning
#


def EDFStackReaderBinning(binning_factor, *edfstackreader_args, **edfstackreader_kwargs):
    [
        edfstackreader_kwargs.pop(kwarg, None)
        for kwarg in ["processing_func", "processing_func_args", "processing_func_kwargs"]
    ]
    edfstackreader_kwargs["processing_func"] = image_binning
    edfstackreader_kwargs["processing_func_args"] = [binning_factor]

    return EDFStackReader(
        *edfstackreader_args,
        **edfstackreader_kwargs,
    )


#
# EDF Reader with distortion correction
#


def apply_distortion_correction_on_image(image, distortion_corrector):
    return distortion_corrector.transform(image)


def EDFStackReaderDistortionCorrection(distortion_corrector, *edfstackreader_args, **edfstackreader_kwargs):
    [
        edfstackreader_kwargs.pop(kwarg, None)
        for kwarg in ["processing_func", "processing_func_args", "processing_func_kwargs"]
    ]
    edfstackreader_kwargs["processing_func"] = apply_distortion_correction_on_image
    edfstackreader_kwargs["processing_func_args"] = [distortion_corrector]

    return EDFStackReader(
        *edfstackreader_args,
        **edfstackreader_kwargs,
    )


def load_darks_flats(
    dataset_info, sub_region, processing_func=None, processing_func_args=None, processing_func_kwargs=None
):
    """
    Load the (reduced) darks and flats and crop them to the sub-region currently used.
    At this stage, dataset_info.flats should be a dict in the form {num: array}

    Parameters
    ----------
    sub_region: 2-tuple of 3-tuples of int
        Tuple in the form ((start_y, end_y), (start_x, end_x))
    """
    (start_y, end_y), (start_x, end_x) = sub_region

    processing_func_args = processing_func_args or []
    processing_func_kwargs = processing_func_kwargs or {}

    def proc(img):
        if processing_func is None:
            return img
        return processing_func(img, *processing_func_args, **processing_func_kwargs)

    res = {
        "flats": {k: proc(flat_k)[start_y:end_y, start_x:end_x] for k, flat_k in dataset_info.flats.items()},
        "darks": {k: proc(dark_k)[start_y:end_y, start_x:end_x] for k, dark_k in dataset_info.darks.items()},
    }
    return res
