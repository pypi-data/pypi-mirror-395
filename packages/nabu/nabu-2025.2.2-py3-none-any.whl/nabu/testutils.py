from dataclasses import dataclass
from itertools import product
import tarfile
import os
import numpy as np
from scipy.signal.windows import gaussian
from silx.resources import ExternalResources
from silx.io.dictdump import nxtodict, dicttonx
from nxtomo.application.nxtomo import ImageKey

utilstest = ExternalResources(
    project="nabu", url_base="http://www.silx.org/pub/nabu/data/", env_key="NABU_DATA", timeout=60
)

__big_testdata_dir__ = os.environ.get("NABU_BIGDATA_DIR")
if __big_testdata_dir__ is None or not (os.path.isdir(__big_testdata_dir__)):
    __big_testdata_dir__ = None

__do_long_tests__ = os.environ.get("NABU_LONG_TESTS", False)  # noqa: PLW1508
if __do_long_tests__:
    try:
        __do_long_tests__ = bool(int(__do_long_tests__))
    except:
        __do_long_tests__ = False

__do_large_mem_tests__ = os.environ.get("NABU_LARGE_MEM_TESTS", False)  # noqa: PLW1508
if __do_large_mem_tests__:
    try:
        __do_large_mem_tests__ = bool(int(__do_large_mem_tests__))
    except:
        __do_large_mem_tests__ = False


def generate_tests_scenarios(configurations):
    """
    Generate "scenarios" of tests.

    The parameter is a dictionary where:
      - the key is the name of a parameter
      - the value is a list of possible parameters

    This function returns a list of dictionary where:
      - the key is the name of a parameter
      - the value is one value of this parameter
    """
    scenarios = [{key: val for key, val in zip(configurations.keys(), p_)} for p_ in product(*configurations.values())]
    return scenarios


def get_data(*dataset_path):
    """
    Get a dataset file from silx.org/pub/nabu/data
    dataset_args is a list describing a nested folder structures, ex.
    ["path", "to", "my", "dataset.h5"]
    """
    dataset_relpath = os.path.join(*dataset_path)
    dataset_downloaded_path = utilstest.getfile(dataset_relpath)
    return np.load(dataset_downloaded_path)


@dataclass
class SimpleNXTomoDescription:
    n_darks: int = 0
    n_flats1: int = 0
    n_projs: int = 0
    n_flats2: int = 0
    n_align: int = 0
    frame_shape: tuple = None
    dtype: np.dtype = np.uint16


def get_dummy_nxtomo_info():
    nx_fname = utilstest.getfile("dummy_nxtomo.nx")
    data_desc = SimpleNXTomoDescription(
        n_darks=10, n_flats1=11, n_projs=100, n_flats2=11, n_align=12, frame_shape=(11, 10), dtype=np.uint16
    )
    image_key = np.concatenate(
        [
            np.zeros(data_desc.n_darks, dtype=np.int32) + ImageKey.DARK_FIELD.value,
            np.zeros(data_desc.n_flats1, dtype=np.int32) + ImageKey.FLAT_FIELD.value,
            np.zeros(data_desc.n_projs, dtype=np.int32) + ImageKey.PROJECTION.value,
            np.zeros(data_desc.n_flats2, dtype=np.int32) + ImageKey.FLAT_FIELD.value,
            np.zeros(data_desc.n_align, dtype=np.int32) + ImageKey.ALIGNMENT.value,
        ]
    )
    projs_vals = np.arange(data_desc.n_projs) + data_desc.n_flats1 + data_desc.n_darks
    darks_vals = np.arange(data_desc.n_darks)
    flats1_vals = np.arange(data_desc.n_darks, data_desc.n_darks + data_desc.n_flats1)
    flats2_vals = np.arange(data_desc.n_darks, data_desc.n_darks + data_desc.n_flats2)
    return nx_fname, data_desc, image_key, projs_vals, darks_vals, flats1_vals, flats2_vals


def get_array_of_given_shape(img, shape, dtype):
    """
    From a given image, returns an array of the wanted shape and dtype.
    """

    # Tile image until it's big enough.
    # "fun" fact: using any(blabla) crashes but using any([blabla]) does not, because of variables re-evaluation
    while any([i_dim <= s_dim for i_dim, s_dim in zip(img.shape, shape)]):
        img = np.tile(img, (2, 2))
    if len(shape) == 1:
        arr = img[: shape[0], 0]
    elif len(shape) == 2:
        arr = img[: shape[0], : shape[1]]
    else:
        arr = np.tile(img, (shape[0], 1, 1))[: shape[0], : shape[1], : shape[2]]
    return np.ascontiguousarray(np.squeeze(arr), dtype=dtype)


def get_big_data(filename):
    if __big_testdata_dir__ is None:
        return None
    return np.load(os.path.join(__big_testdata_dir__, filename))


def uncompress_file(compressed_file_path, target_directory):
    if not tarfile.is_tarfile(compressed_file_path):
        raise ValueError(f"Invalid tar file: {compressed_file_path}")

    def is_safe_member(member, target_directory):
        """Ensure the member does not extract outside the target directory."""
        if not isinstance(member, tarfile.TarInfo):
            return False  # Reject any unexpected type

        abs_target = os.path.abspath(target_directory)
        member_path = os.path.abspath(os.path.join(target_directory, member.name))
        return member_path.startswith(abs_target)

    def get_valid_members(tar):
        members = [m for m in tar.getmembers() if is_safe_member(m, target_directory)]
        if not members:
            raise ValueError("No valid files to extract or archive contains unsafe paths.")
        for member in members:
            if not is_safe_member(member, target_directory):
                raise ValueError(f"Unsafe path detected: {member.name}")

    with tarfile.open(compressed_file_path, "r") as tar:
        tar.extractall(  # noqa: S202 - what can be done in addition of the above checks ?
            path=target_directory, members=get_valid_members(tar)
        )


def get_file(fname):
    downloaded_file = utilstest.getfile(fname)
    if ".tar" in fname:
        uncompress_file(downloaded_file, os.path.dirname(downloaded_file))
        downloaded_file = downloaded_file.split(".tar")[0]
    return downloaded_file


def compare_arrays(arr1, arr2, tol, diff=None, absolute_value=True, percent=None, method="max", return_residual=False):
    """
    Utility to compare two arrays.

    Parameters
    ----------
    arr1: numpy.ndarray
        First array to compare
    arr2: numpy.ndarray
        Second array to compare
    tol: float
        Tolerance indicating whether arrays are close to each other.
    diff: numpy.ndarray, optional
        Difference `arr1 - arr2`. If provided, this array is taken instead of `arr1`
        and `arr2`.
    absolute_value: bool, optional
        Whether to take absolute value of the difference.
    percent: float
        If set, a "relative" comparison is performed instead of a subtraction:
        `red(|arr1 - arr2|) / (red(|arr1|) * percent) < tol`
        where "red" is the reduction method (mean, max or median).
    method:
        Reduction method. Can be "max", "mean", or "median".

    Returns
    --------
    (is_close, residual) if return_residual is set to True
    is_close otherwise

    Examples
    --------
    When using method="mean" and absolute_value=True, this function computes
    the Mean Absolute Difference (MAD) metric.
    When also using percent=1.0, this computes the Relative Mean Absolute Difference
    (RMD) metric.
    """
    reductions = {
        "max": np.max,
        "mean": np.mean,
        "median": np.median,
    }
    if method not in reductions:
        raise ValueError("reduction method should be in %s" % str(list(reductions.keys())))
    if diff is None:
        diff = arr1 - arr2
    if absolute_value is not None:
        diff = np.abs(diff)
    residual = reductions[method](diff)
    if percent is not None:
        a1 = np.abs(arr1) if absolute_value else arr1
        residual /= reductions[method](a1)

    res = residual < tol
    if return_residual:
        res = res, residual
    return res


def gaussian_apodization_window(shape, fwhm_ratio=0.7):
    fwhm = fwhm_ratio * np.array(shape)
    sigma = fwhm / 2.355
    return np.outer(*[gaussian(n, s) for n, s in zip(shape, sigma)])


def compare_shifted_images(img1, img2, fwhm_ratio=0.7, return_upper_bound=False):
    """
    Compare two images that are slightly shifted from one another.
    Typically, tomography reconstruction wight slightly different CoR.
    Each image is Fourier-transformed, and the modulus is taken to get rid of the shift between the images.
    An apodization is done to filter the high frequencies that are usually less relevant.

    Parameters
    ----------
    img1: numpy.ndarray
        First image
    img2: numpy.ndarray
        Second image
    fwhm_ratio: float, optional
        Ratio defining the apodization in the frequency domain.
        A small value (eg. 0.2) means that essentually only the low frequencies will be compared.
        A value of 1.0 means no apodization
    return_upper_bound: bool, optional
        Whether to return a (coarse) upper bound of the comparison metric

    Notes
    -----
    This function roughly computes
        |phi(F(img1)) - phi(F(img2))|
    where F is the absolute value of the Fourier transform, and phi some shrinking function (here arcsinh).
    """

    def _fourier_transform(img):
        return np.arcsinh(np.abs(np.fft.fftshift(np.fft.fft2(img))))

    diff = _fourier_transform(img1) - _fourier_transform(img2)
    diff *= gaussian_apodization_window(img1.shape, fwhm_ratio=fwhm_ratio)
    res = np.abs(diff).max()
    if return_upper_bound:
        data_range = np.max(np.abs(img1))
        return res, np.arcsinh(np.prod(img1.shape) * data_range)
    else:
        return res


# To be improved
def generate_nx_dataset(out_fname, image_key, data_volume=None, rotation_angle=None):
    nx_template_file = get_file("dummy.nx.tar.gz")
    nx_dict = nxtodict(nx_template_file)
    nx_entry = nx_dict["entry"]

    def _get_field(dict_, path):
        path = path.strip("/")
        split_path = path.split("/")
        if len(split_path) == 1:
            return dict_[split_path[0]]
        return _get_field(dict_[split_path[0]], "/".join(split_path[1:]))

    for name in ["image_key", "image_key_control"]:
        nx_entry["data"][name] = image_key
        nx_entry["instrument"]["detector"][name] = image_key

    if rotation_angle is not None:
        nx_entry["data"]["rotation_angle"] = rotation_angle
        nx_entry["sample"]["rotation_angle"] = rotation_angle

    dicttonx(nx_dict, out_fname)
