from bisect import bisect_left
from fnmatch import fnmatch
from functools import partial
import os
from functools import lru_cache
from itertools import product
import warnings
from time import time
import posixpath
import numpy as np


def nextpow2(N, dtype=np.int32):
    return 2 ** np.ceil(np.log2(N)).astype(dtype)


def previouspow2(N, dtype=np.int32):
    return 2 ** np.floor(np.log2(N)).astype(dtype)


def updiv(a, b):
    return (a + (b - 1)) // b


def convert_index(idx, idx_max, default_val):
    """
    Convert an index (possibly negative or None) to a non-negative integer.

    Parameters
    ----------
    idx: int or None
        Index
    idx_max: int
        Maximum value (upper bound) for the index.
    default_val: int
        Default value if idx is None

    Examples
    ---------
    Given an integer `M`, `J = convert_index(i, M, XX)` returns an integer in the
    mathematical range [0, M] (or Python `range(0, M)`). `J` can then be used
    to define an upper bound of a range.
    """
    if idx is None:
        return default_val
    if idx > idx_max:
        return idx_max
    if idx < 0:
        return idx % idx_max
    return idx


def get_folder_path(foldername=""):
    _file_dir = os.path.dirname(os.path.abspath(__file__))
    package_dir = _file_dir
    return os.path.join(package_dir, foldername)


def get_cuda_srcfile(filename):
    src_relpath = os.path.join("cuda", "src")
    cuda_src_folder = get_folder_path(foldername=src_relpath)
    return os.path.join(cuda_src_folder, filename)


def get_opencl_srcfile(filename):
    src_relpath = os.path.join("opencl", "src")
    src_folder = get_folder_path(foldername=src_relpath)
    return os.path.join(src_folder, filename)


def get_resource_file(filename, subfolder=None):
    subfolder = subfolder or []
    relpath = os.path.join("resources", *subfolder)
    abspath = get_folder_path(foldername=relpath)
    return os.path.join(abspath, filename)


def check_array(array, expected_shape, expected_dtype="f", array_name="array", check_contiguous=True):
    if array.shape != expected_shape:
        raise ValueError(f"Expected array with shape {expected_shape} for {array_name}, but got {array.shape}")
    if array.dtype != np.dtype(expected_dtype):
        raise ValueError(f"Expected array with data type {expected_dtype} for {array_name}, but got {array.dtype}")
    if check_contiguous and (not (isinstance(array, np.ndarray)) or not (array.flags["C_CONTIGUOUS"])):
        raise ValueError(f"Expected C-Contiguous array for {array_name}")


def indices_to_slices(indices):
    """
    From a series of integer indices, return corresponding slice() objects.

    Parameters
    ----------
    indices: collection of sorted unique integers
        Arrays indices

    Examples
    --------
    slices_from_indices([0, 1, 2, 3]) returns [slice(0, 4)]
    slices_from_indices([8, 9, 10, 14, 15, 16]) returns [slice(8, 11), slice(15, 17)]
    """
    jumps = np.where(np.diff(indices) > 1)[0]
    if len(jumps) == 0:
        return [slice(indices[0], indices[-1] + 1)]
    jumps = np.hstack([-1, jumps, len(indices) - 1])
    slices = []
    for i in range(len(jumps) - 1):
        slices.append(slice(indices[jumps[i] + 1], indices[jumps[i + 1]] + 1))  # noqa: PERF401
    return slices


def merge_slices(slice1, slice2):
    """
    Merge two slicing operations in one.

    Examples
    --------
    array = numpy.arange(200)
    array[slice(133, 412, 2)][slice(31, 35, 2)] # gives [195 199]
    array[merge_slices(slice(133, 412, 2), slice(31, 35, 2))]  # gives [195 199]
    """
    step1 = slice1.step or 1
    step2 = slice2.step or 1
    step = step1 * step2
    if step == 1:
        step = None

    start = slice1.start + step1 * (slice2.start or 0)
    if slice2.stop is None:
        stop = slice1.stop
    else:
        stop = min(slice1.stop, slice1.start + step1 * slice2.stop)
    return slice(start, stop, step)


def compacted_views(slices_):
    """
    From a list of slice objects, returns the slice objects corresponding to a compact view.

    If "array" is obtained with
        array = np.hstack([big_array[slice1], big_array[slice2]])
    Then, compacted_views([slice1, slice2]) returns [slice3, slice4] where
      - slice3 are the indices, in 'array', corresponding to indices of slice1 in 'big_array'
      - slice4 are the indices, in 'array', corresponding to indices of slice2 in 'big_array'

    Example
    -------
    compacted_views([slice(1, 26), slice(526, 551)]) gives [slice(0, 25), slice(25, 50)]

    """
    prev_start = 0
    r = []
    for s in slices_:
        start = prev_start
        stop = start + (s.stop - s.start)
        r.append(slice(start, stop))
        prev_start = stop
    return r


def get_size_from_sliced_dimension(length, slice_):
    """
    From a given array size, returns the size of the array once it is accessed using a slice.

    Examples
    --------
    If data.shape = (3500, 2160, 2560)
    get_size_from_sliced_dimension(data.shape[0], None) returns 3500
    get_size_from_sliced_dimension(data.shape[0], slice(100, 200)) returns 100
    """
    return np.arange(length)[slice_].size


def get_shape_from_sliced_dims(shape, slices_):
    """
    Same as get_size_from_sliced_dimension() but in 3D
    """
    return tuple(get_size_from_sliced_dimension(length, slice_) for length, slice_ in zip(shape, slices_))


def get_available_threads():
    try:
        n_threads = len(os.sched_getaffinity(0))
    except AttributeError:
        n_threads = int(os.environ.get("SLURM_CPUS_PER_TASK", os.cpu_count()))
    return n_threads


def list_match_queries(available, queries):
    """
    Given a list of strings, return all items matching any of one elements of "queries"
    """
    matches = []
    if isinstance(queries, str):
        queries = [queries]
    for a in available:
        for q in queries:
            if fnmatch(a, q):
                matches.append(a)  # noqa: PERF401
    return matches


def is_writeable(location):
    """
    Return True if a file/location is writeable.
    """
    return os.access(location, os.W_OK)


def is_int(num, eps=1e-7):
    return abs(num - int(num)) < eps


def is_scalar(stuff):
    if isinstance(stuff, str):
        return False
    return np.isscalar(stuff)


def _sizeof(Type):
    """
    return the size (in bytes) of a scalar type, like the C behavior
    """
    return np.dtype(Type).itemsize


class _DefaultFormat(dict):
    """
    https://docs.python.org/3/library/stdtypes.html
    """

    def __missing__(self, key):
        return key


def safe_format(str_, **kwargs):
    """
    Alternative to str.format(), but does not throw a KeyError when fields are missing.
    """
    return str_.format_map(_DefaultFormat(**kwargs))


def get_ftype(url):
    """
    return supposed filetype of an url
    """
    if hasattr(url, "file_path"):
        return os.path.splitext(url.file_path())[-1].replace(".", "")
    else:
        return os.path.splitext(url)[-1].replace(".", "")


def get_2D_3D_shape(shape):
    if len(shape) == 2:
        return (1,) + shape
    return shape


def get_subregion(sub_region):
    ymin, ymax = None, None
    if sub_region is None:
        xmin, xmax, ymin, ymax = None, None, None, None
    elif len(sub_region) == 2:
        first_part, second_part = sub_region
        if np.iterable(first_part) and np.iterable(second_part):
            xmin, xmax = first_part
            ymin, ymax = second_part
        else:
            xmin, xmax = sub_region
    elif len(sub_region) == 4:
        xmin, xmax, ymin, ymax = sub_region
    else:
        raise ValueError("Expected parameter in the form (a, b, c, d) or ((a, b), (c, d))")
    return xmin, xmax, ymin, ymax


def get_3D_subregion(sub_region):
    if sub_region is None:
        xmin, xmax, ymin, ymax, zmin, zmax = None, None, None, None, None, None
    elif len(sub_region) == 3:
        first_part, second_part, third_part = sub_region
        xmin, xmax = first_part
        ymin, ymax = second_part
        zmin, zmax = third_part
    elif len(sub_region) == 6:
        xmin, xmax, ymin, ymax, zmin, zmax = sub_region
    else:
        raise ValueError(
            "Expected parameter in the form (xmin, xmax, ymin, ymax, zmin, zmax) or ((xmin, xmax), (ymin, ymax), (zmin, zmax))"
        )
    return xmin, xmax, ymin, ymax, zmin, zmax


def to_3D_array(arr):
    """
    Turn an array to a (C-Contiguous) 3D array with the layout (n_arrays, n_y, n_x).
    """
    if arr.ndim == 3:
        return arr
    return np.tile(arr, (1, 1, 1))


def view_as_images_stack(img):
    """
    View an image (2D array) as a stack of one image (3D array).
    No data is duplicated.
    """
    return img.reshape((1,) + img.shape)


def rescale_integers(items, new_tot):
    """
    From a given sequence of integers, create a new sequence
    where the sum of all items must be equal to "new_tot".
    The relative contribution of each item to the new total is approximately kept.

    Parameters
    ----------
    items: array-like
        Sequence of integers
    new_tot: int
        Integer indicating that the sum of the new array must be equal to this value
    """
    cur_items = np.array(items)
    new_items = np.ceil(cur_items / cur_items.sum() * new_tot).astype(np.int64)
    excess = new_items.sum() - new_tot
    i = 0
    while excess > 0:
        ind = i % new_items.size
        if cur_items[ind] > 0:
            new_items[ind] -= 1
            excess -= 1
        i += 1
    return new_items.tolist()


def merged_shape(shapes, axis=0):
    n_img = sum(shape[axis] for shape in shapes)
    if axis == 0:
        return (n_img,) + shapes[0][1:]
    elif axis == 1:
        return (shapes[0][0], n_img, shapes[0][2])
    elif axis == 2:
        return shapes[0][:2] + (n_img,)
    else:
        raise ValueError


def is_device_backend(backend):
    return backend.lower() in ["cuda", "opencl"]


def get_decay(curve, cutoff=1e3, vmax=None):
    """
    Assuming a decreasing curve, get the first point below a certain threshold.

    Parameters
    ----------
    curve: numpy.ndarray
        A 1D array
    cutoff: float, optional
        Threshold. Default is 1000.
    vmax: float, optional
        Curve maximum value
    """
    if vmax is None:
        vmax = curve.max()
    return int(np.argmax(np.abs(curve) < vmax / cutoff))


@lru_cache(maxsize=1)
def generate_powers():
    """
    Generate a list of powers of [2, 3, 5, 7],
    up to (2**15)*(3**9)*(5**6)*(7**5).
    """
    primes = [2, 3, 5, 7]
    maxpow = {2: 15, 3: 9, 5: 6, 7: 5}
    valuations = []
    for prime in primes:
        # disallow any odd number (for R2C transform), and any number
        # not multiple of 4 (Ram-Lak filter behaves strangely when
        # dwidth_padded/2 is not even)
        minval = 2 if prime == 2 else 0
        valuations.append(range(minval, maxpow[prime] + 1))
    powers = product(*valuations)
    res = []
    for pw in powers:
        res.append(np.prod(list(map(lambda x: x[0] ** x[1], zip(primes, pw)))))  # noqa: PERF401
    return np.unique(res)


def calc_padding_lengths1D(length, length_padded):
    """
    Compute the padding lengths at both side along one dimension.

    Parameters
    ----------
    length: int
        Number of elements along one dimension of the original array
    length_padded: tuple
        Number of elements along one dimension of the padded array

    Returns
    -------
    pad_lengths: tuple
        A tuple under the form (padding_left, padding_right). These are the
        lengths needed to pad the original array.
    """
    pad_left = (length_padded - length) // 2
    pad_right = length_padded - length - pad_left
    return (pad_left, pad_right)


def calc_padding_lengths(shape, shape_padded):
    """
    Multi-dimensional version of calc_padding_lengths1D.
    Please refer to the documentation of calc_padding_lengths1D.
    """
    assert len(shape) == len(shape_padded)
    padding_lengths = []
    for dim_len, dim_len_padded in zip(shape, shape_padded):
        pad0, pad1 = calc_padding_lengths1D(dim_len, dim_len_padded)
        padding_lengths.append((pad0, pad1))
    return tuple(padding_lengths)


def partition_dict(dict_, n_partitions):
    keys = np.sort(list(dict_.keys()))
    res = []
    for keys_arr in np.array_split(keys, n_partitions):
        d = {}
        for key in keys_arr:
            d[key] = dict_[key]
        res.append(d)
    return res


def first_dict_item(dict_):
    keys = sorted(dict_.keys())
    return dict_[keys[0]]


def first_generator_item(gen):
    return next(iter(gen))  # instead of list(gen)[0]


def subsample_dict(dic, subsampling_factor):
    """
    Subsample a dict where keys are integers.
    """
    res = {}
    indices = sorted(dic.keys())
    for i in indices[::subsampling_factor]:
        res[i] = dic[i]
    return res


def compare_dicts(dic1, dic2):  # noqa: PLR0911
    """
    Compare two dictionaries. Return None if and only iff the dictionaries are the same.

    Parameters
    ----------
    dic1: dict
        First dictionary
    dic2: dict
        Second dictionary

    Returns
    -------
    res: result which can be the following:

       - None: it means that dictionaries are the same
       - empty string (""): the dictionaries do not have the same keys
       - nonempty string: path to the first differing items
    """
    if set(dic1.keys()) != set(dic2.keys()):
        return ""
    for key, val1 in dic1.items():
        val2 = dic2[key]
        if isinstance(val1, dict):
            res = compare_dicts(val1, val2)
            if res is not None:
                return posixpath.join(key, res)
        # str
        elif isinstance(val1, str):
            if val1 != val2:
                return key
        # Scalars
        elif np.isscalar(val1):
            if not np.isclose(val1, val2):
                return key
        # NoneType
        elif val1 is None:
            if val2 is not None:
                return key
        # Array-like
        elif np.iterable(val1):
            arr1 = np.array(val1)
            arr2 = np.array(val2)
            if arr1.ndim != arr2.ndim or arr1.dtype != arr2.dtype or not np.allclose(arr1, arr2):
                return key
        else:
            raise ValueError("Don't know what to do with type %s" % str(type(val1)))
    return None


def remove_items_from_list(list_, items_to_remove):
    """
    Remove items from a list and return the removed elements.

    Parameters
    ----------
    list_: list
        List containing items to remove
    items_to_remove: list
        List of items to remove

    Returns
    --------
    reduced_list: list
        List with removed items
    removed_items: dict
        Dictionary where the keys are the indices of removed items, and values are the items
    """
    removed_items = {}
    res = []
    for i, val in enumerate(list_):
        if val in items_to_remove:
            removed_items[i] = val
        else:
            res.append(val)
    return res, removed_items


def restore_items_in_list(list_, removed_items):
    """
    Undo the effect of the function `remove_items_from_list`

    Parameters
    ----------
    list_: list
        List where items were removed
    removed_items: dict
        Dictionary where the keys are the indices of removed items, and values are the items
    """
    for idx, val in removed_items.items():
        list_.insert(idx, val)


def split_list(lst, n):
    """
    Split a list into n roughly equal parts, similar to numpy.array_split.

    Parameters
    -----------
    lst: list
        The list to split
    n: int
        Number of parts

    Returns
    --------
    list of lists: The split parts
    """
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n)]


def search_sorted(arr, val):
    """
    Binary search that returns the "nearest" index given a query,
    i.e find "i" that minimizes   abs(arr[i] - val)
    It does not return the "insersion point" contrarily to numpy.searchsorted() or bisect_left
    """
    pos = bisect_left(arr, val)
    if pos == len(arr):
        return len(arr) - 1
    return pos - 1 if abs(val - arr[pos - 1]) < abs(arr[pos] - val) else pos


def check_supported(param_value, available, param_desc):
    if param_value not in available:
        raise ValueError("Unsupported %s '%s'. Available are: %s" % (param_desc, param_value, str(available)))


def check_supported_enum(param_value, enum_cls, param_desc):
    available = enum_cls.values()
    return check_supported(param_value, available, param_desc)


def check_shape(shape, expected_shape, name):
    if shape != expected_shape:
        raise ValueError("Expected %s shape %s but got %s" % (name, str(expected_shape), str(shape)))


def copy_dict_items(dict_, keys):
    """
    Perform a shallow copy of a subset of a dictionary.
    The subset if done by a list of keys.
    """
    res = {key: dict_[key] for key in keys}
    return res


def recursive_copy_dict(dict_):
    """
    Perform a shallow copy of a dictionary of dictionaries.
    This is NOT a deep copy ! Only reference to objects are kept.
    """
    if not (isinstance(dict_, dict)):
        res = dict_
    else:
        res = {k: recursive_copy_dict(v) for k, v in dict_.items()}
    return res


def subdivide_into_overlapping_segment(N, window_width, half_overlap):
    """
    Divide a segment into a number of possibly-overlapping sub-segments.

    Parameters
    ----------
    N: int
        Total segment length
    window_width: int
        Length of each segment
    half_overlap: int
        Half-length of the overlap between each sub-segment.

    Returns
    -------
    segments: list
        A list where each item is in the form
        (left_margin_start, inner_segment_start, inner_segment_end, right_margin_end)
    """
    if half_overlap > 0 and half_overlap >= window_width // 2:
        raise ValueError("overlap must be smaller than window_width")
    w_in = window_width - 2 * half_overlap
    n_segments = N // w_in
    inner_start = w_in * np.arange(n_segments)
    inner_end = w_in * (np.arange(n_segments) + 1)
    margin_left_start = np.maximum(inner_start - half_overlap, 0)
    margin_right_end = np.minimum(inner_end + half_overlap, N)
    segments = [
        (left_start, i_start, i_end, right_end)
        for left_start, i_start, i_end, right_end in zip(
            margin_left_start.tolist(), inner_start.tolist(), inner_end.tolist(), margin_right_end.tolist()
        )
    ]
    if N % w_in:
        # additional sub-segment
        new_margin_left_start = inner_end[-1] - half_overlap
        new_inner_start = inner_end[-1]
        new_inner_end = N
        segments.append((new_margin_left_start, new_inner_start, new_inner_end, new_inner_end))
    return segments


def get_num_threads(n=None):
    """
    Get a number of threads (ex. to be used by fftw). If the argument is None, returns the total number of CPU threads.
    If the argument is negative, the total number of available threads plus this number is returned.

    Parameters
    -----------
    n: int, optional
       - If an positive integer `n` is provided, then `n` threads are used
       - If a negative integer `n` is provided, then `n_avail + n` threads are used
         (so -1 to use all available threads minus one)
    """
    n_avail = get_available_threads()
    if n is None or n == 0:
        return n_avail
    if n < 0:
        return max(1, n_avail + n)
    else:
        return min(n_avail, n)


class DictToObj:
    """utility class to transform a dictionary into an object with dictionary items as members.
    Example:

    >>> a=DictToObj( dict(i=1,j=1))
    ... a.j+a.i

    """

    def __init__(self, dictio):
        self.__dict__ = dictio


def remove_parenthesis_or_brackets(input_str):
    """
    Clear a string from left and/or right parentheses or brackets.
    """
    if (input_str.startswith("(") and input_str.endswith(")")) or (
        input_str.startswith("[") and input_str.endswith("]")
    ):
        input_str = input_str[1:-1]
    return input_str


def filter_str_def(elmt):
    """Clean element if it is a string defined from a text file.
    Remove characters that could have been put on the left or right, and strip empty spaces.
    """
    if elmt is None:
        return None
    assert isinstance(elmt, str)
    elmt = elmt.lstrip(" ").rstrip(" ")
    elmt = elmt.lstrip("'").lstrip('"')
    elmt = elmt.rstrip("'").rstrip('"')
    elmt = elmt.lstrip(" ").rstrip(" ")
    for character in ("'", '"'):
        if elmt.startswith(character) and elmt.endswith(character):
            elmt = elmt[1:-1]
    return elmt


def convert_str_to_tuple(input_str: str, none_if_empty: bool = False):
    """
    :param str input_str: string to convert
    :param bool none_if_empty: if true and the conversion is an empty tuple
                               return None instead of an empty tuple
    """
    if isinstance(input_str, tuple):
        return input_str
    if not isinstance(input_str, str):
        raise TypeError(f"input_str should be a string not {type(input_str)}, {input_str}")
    input_str = input_str.lstrip(" ").lstrip("(").lstrip("[").lstrip(" ").rstrip(" ")
    input_str = remove_parenthesis_or_brackets(input_str)
    input_str = input_str.replace("\n", ",")

    elmts = input_str.split(",")
    elmts = [filter_str_def(elmt) for elmt in elmts]
    rm_empty_str = lambda a: a != ""
    elmts = list(filter(rm_empty_str, elmts))
    if none_if_empty and len(elmts) == 0:
        return None
    else:
        return tuple(elmts)


def concatenate_dict(dict_1, dict_2) -> dict:
    """update dict which has dict as values. And we want concatenate those values to"""
    res = dict_1.copy()
    for key in dict_2:
        if key in dict_1:
            res[key].update(dict_2[key])
        else:
            res[key] = dict_2[key]
    return res


class BaseClassError(BaseException):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Base class")


def MissingComponentError(msg):
    class MissingComponentCls:
        def __init__(self, *args, **kwargs):
            raise RuntimeError(msg)

    return MissingComponentCls


# ------------------------------------------------------------------------------
# ------------------------ Image (move elsewhere ?) ----------------------------
# ------------------------------------------------------------------------------


def generate_coords(img_shp, center=None):
    l_r, l_c = float(img_shp[0]), float(img_shp[1])
    R, C = np.mgrid[:l_r, :l_c]  # np.indices is faster
    if center is None:
        center0, center1 = l_r / 2.0, l_c / 2.0
    else:
        center0, center1 = center
    R += 0.5 - center0
    C += 0.5 - center1
    return R, C


def clip_circle(img, center=None, radius=None, out_value=0):
    R, C = generate_coords(img.shape, center)
    if radius is None:
        radius = R.shape[-1] // 2
    M = R**2 + C**2
    res = np.zeros_like(img)
    if out_value != 0:
        res.fill(out_value)
    res[M < radius**2] = img[M < radius**2]
    return res


def extend_image_onepixel(img):
    # extend of one pixel
    img2 = np.zeros((img.shape[0] + 2, img.shape[1] + 2), dtype=img.dtype)
    img2[0, 1:-1] = img[0]
    img2[-1, 1:-1] = img[-1]
    img2[1:-1, 0] = img[:, 0]
    img2[1:-1, -1] = img[:, -1]
    # middle
    img2[1:-1, 1:-1] = img
    # corners
    img2[0, 0] = img[0, 0]
    img2[-1, 0] = img[-1, 0]
    img2[0, -1] = img[0, -1]
    img2[-1, -1] = img[-1, -1]
    return img2


def median2(img):
    """
    3x3 median filter for 2D arrays, with "reflect" boundary mode.
    Roughly same speed as scipy median filter, but more memory demanding.
    """
    img2 = extend_image_onepixel(img)
    img3 = np.array(
        [
            img2[0:-2, 0:-2],
            img2[0:-2, 1:-1],
            img2[0:-2, 2:],
            img2[1:-1, 0:-2],
            img2[1:-1, 1:-1],
            img2[1:-1, 2:],
            img2[2:, 0:-2],
            img2[2:, 1:-1],
            img2[2:, 2:],
        ]
    )
    return np.median(img3, axis=0)


# ------------------------------------------------------------------------------
# ---------------------------- Decorators --------------------------------------
# ------------------------------------------------------------------------------


def no_decorator(func):
    return func


_warnings = {}


def measure_time(func):
    def wrapper(*args, **kwargs):
        t0 = time()
        res = func(*args, **kwargs)
        el = time() - t0
        return el, res

    return wrapper


def wip(func):
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        if func_name not in _warnings:
            _warnings[func_name] = 1
            print("Warning: function %s is a work in progress, it is likely to change in the future")
        return func(*args, **kwargs)

    return wrapper


def warning(msg):
    def decorator(func):
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            if func_name not in _warnings:
                _warnings[func_name] = 1
                print(msg)
                res = func(*args, **kwargs)
                return res
            return None

        return wrapper

    return decorator


def deprecated(msg, do_print=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            deprecation_warning(msg, do_print=do_print, func_name=func.__name__)
            res = func(*args, **kwargs)
            return res

        return wrapper

    return decorator


def deprecated_class(msg, do_print=False):
    def decorator(cls):
        class Wrapper:
            def __init__(self, *args, **kwargs):
                deprecation_warning(msg, do_print=do_print, func_name=cls.__name__)
                self.wrapped = cls(*args, **kwargs)

            # This is so ugly :-(
            def __getattr__(self, name):
                return getattr(self.wrapped, name)

        return Wrapper

    return decorator


def deprecation_warning(message, do_print=True, func_name=None):
    func_name_msg = str("%s: " % func_name) if func_name is not None else ""
    func_name = func_name or "None"
    if _warnings.get(func_name, False):
        return
    warnings.warn(message, DeprecationWarning)
    if do_print:
        print("Deprecation warning: %s%s" % (func_name_msg, message))
    _warnings[func_name] = 1


def _docstring(dest, origin):
    """Implementation of docstring decorator.

    It patches dest.__doc__.
    """
    if not isinstance(dest, type) and isinstance(origin, type):
        # func is not a class, but origin is, get the method with the same name
        try:
            origin = getattr(origin, dest.__name__)
        except AttributeError:
            raise ValueError("origin class has no %s method" % dest.__name__)

    dest.__doc__ = origin.__doc__
    return dest


def docstring(origin):
    """Decorator to initialize the docstring from another source.

    This is useful to duplicate a docstring for inheritance and composition.

    If origin is a method or a function, it copies its docstring.
    If origin is a class, the docstring is copied from the method
    of that class which has the same name as the method/function
    being decorated.

    :param origin:
        The method, function or class from which to get the docstring
    :raises ValueError:
        If the origin class has not method n case the
    """
    return partial(_docstring, origin=origin)


from warnings import catch_warnings

# FIX for python < 3.11
# catch_warnings() does not have "action=XX" kwarg for python < 3.11
from sys import version_info

if version_info.major == 3 and version_info.minor < 11:  # noqa: YTT204 - not sure about this

    def dummy(*args, **kwargs):
        pass

    catch_warnings_old = catch_warnings

    def catch_warnings(*args, **kwargs):  # pylint: disable=E0102
        action = kwargs.pop("action", None)
        return catch_warnings_old(record=(dummy if action == "ignore" else False))


# ---
