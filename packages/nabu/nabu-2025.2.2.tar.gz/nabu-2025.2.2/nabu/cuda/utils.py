from warnings import warn
import numpy as np

from ..utils import check_supported
from ..resources.gpu import GPUDescription

try:
    from cupy import cuda, ndarray as cupy_ndarray

    __has_cupy__ = cuda.is_available()
    __cupy_error_msg__ = None
except ImportError as err:
    __has_cupy__ = False
    __cupy_error_msg__ = str(err)


# -----------------------------------------------------------------------------
# -------------------- Device management --------------------------------------
# -----------------------------------------------------------------------------


# TODO use existing context or stream
# cupy does not seem to be able to access contexts
def get_cuda_stream(device_id=None, force_create=False):
    """
    Notes
    ------
    In cupy, contexts/device/stream management is not so explicit.
    It seems that cupy wants to hide these things from user and handle it automatically.
    There are multiple issues:
      - cuda.get_current_stream() will always return device_id = -1
        (even when called with device_id != -1)
      - A Device object does not have a list of attached streams
      - A Stream object does not have its device, we have keep various objects references

    Solution so far:
      - Call Device(id).use() at program startup
      - Use cuda.runtime.getDevice()
      - Use cuda.stream.Stream()

    """
    if device_id is not None:
        dev = cuda.Device(device_id)
        dev.use()
    if force_create:
        return cuda.Stream(null=False, ptds=False)
    return cuda.Stream(null=False, ptds=True)


def detect_cuda_gpus():
    """
    Detect the available Nvidia CUDA GPUs on the current host.

    Returns
    --------
    gpus: dict
        Dictionary where the key is the GPU ID, and the value is a `cupy.cuda.Device` object.
    error_msg: str
        In the case where there is an error, the message is returned in this item.
        Otherwise, it is a None object.
    """
    gpus = {}
    error_msg = None
    if not (__has_cupy__):
        return {}, __cupy_error_msg__
    try:
        n_gpus = cuda.runtime.getDeviceCount()
    except Exception as exc:
        error_msg = str(exc)
    if error_msg is not None:
        return {}, error_msg
    for i in range(n_gpus):
        gpus[i] = cuda.Device(i)
    return gpus, None


def collect_cuda_gpus(on_error="warn"):
    """
    Return a dictionary of GPU ids and brief description of each CUDA-compatible
    GPU with a few fields.

    Parameters
    ----------
    on_error: str, optional
        What to do on error. Possible values:
          - "warn": print a warning
          - "raise": throw an error
    """
    gpus, error_msg = detect_cuda_gpus()
    if error_msg is not None:
        msg = "Failed to collect CUDA GPUs: %s" % error_msg
        if on_error == "warn":
            warn(msg, RuntimeWarning)
        elif on_error == "raise":
            raise RuntimeError(msg)
        return None
    cuda_gpus = {}
    for gpu_id, gpu in gpus.items():
        cuda_gpus[gpu_id] = GPUDescription(gpu).get_dict()
    return cuda_gpus


# -----------------------------------------------------------------------------
# -------------------- Data type utils  ---------------------------------------
# -----------------------------------------------------------------------------


_dtype_to_ctype_cuda = {
    np.bool_: "bool",
    np.byte: "signed char",  # same as int8
    np.ubyte: "unsigned char",  # same as uint8
    np.short: "short",  # same as int16
    np.ushort: "unsigned short",  # same as uint16
    np.intc: "int",  # typically int32
    np.uintc: "unsigned int",  # typically uint32
    np.int_: "long",  # platform-dependent, usually int64 on 64-bit Linux
    np.uint: "unsigned long",  # same logic as above
    np.longlong: "long long",  # explicitly int64
    np.ulonglong: "unsigned long long",  # explicitly uint64
    np.half: "half",  # not standard C, sometimes `_Float16` or compiler extension
    np.float16: "half",  # same as above
    np.single: "float",  # float32
    np.float32: "float",
    np.double: "double",  # float64
    np.float64: "double",
    np.longdouble: "long double",  # platform-dependent extended precision
    np.csingle: "complex64",  # "float _Complex",  # complex64
    np.complex64: "complex64",  # "float _Complex",
    np.cdouble: "complex128",  # "double _Complex",  # complex128
    np.complex128: "complex128",  # "double _Complex",
    np.clongdouble: "long double _Complex",  # complex256 on some platforms
}


def dtype_to_ctype(dtype):
    dtype = np.dtype(dtype).type  # Normalize
    return _dtype_to_ctype_cuda.get(dtype, None)


def to_int2(arr):
    """
    Convert a 1D array of length 2 into a "int2" data type.
    Beware, the first coordinate is x ! (as opposed to usual python/numpy/C convention)
    """
    res = np.zeros(1, dtype=int2_t)
    res["x"] = arr[0]
    res["y"] = arr[1]
    return res


# -----------------------------------------------------------------------------
# ---------------------- Array & Textures utils -------------------------------
# -----------------------------------------------------------------------------


def create_texture(shape, dtype, from_image=None, address_mode="border", filter_mode="linear", normalized_coords=False):
    """
    Create a texture object.

    Parameters
    ----------
    shape: tuple of int
        Image shape
    dtype: numpy.dtype
        Data type
    from_image: numpy.ndarray, optional
        Image to be used as a texture. If provided, above parameters are replaced with image properties.
    address_mode: str, optional
        Which address mode to use. Can be:
           - "border" (default): extension with zeros
           - "clamp": extension with edges
           - "mirror": extension with mirroring
           - "wrap": periodic extension
    filter_mode: str, optional
        Which filter mode to use when accessing texture at non-integer coordinates.
        Can be "linear" or "nearest"
        Default is (bi)linear filtering.
    normalized_coords: bool, optional
        Whether to use normalized coordinates. Default is False.

    Returns
    --------
    tex_obj: cupy.cuda.texture.TextureObject
        Texture object that can be passed to kernels (accessed in source code with 'cudaTextureObject_t' type)
    cu_arr: cupy.cuda.texture.CUDAarray
        Cuda array that bakes the texture

    Notes
    -----
      - Two-dimensional images default to single-chanel textures.
      - It will allocate memory for the underlying "cuda array" object
    """
    if from_image is not None:
        shape = from_image.shape
        dtype = from_image.dtype
    if len(shape) > 2:
        raise NotImplementedError("Textures > 2D are not supported yet")
    dtype_kind_to_format_kind = {
        "f": cuda.runtime.cudaChannelFormatKindFloat,
        "u": cuda.runtime.cudaChannelFormatKindUnsigned,
        "i": cuda.runtime.cudaChannelFormatKindSigned,
    }
    check_supported(np.dtype(dtype).kind, dtype_kind_to_format_kind, "data type")
    address_modes = {
        "border": cuda.runtime.cudaAddressModeBorder,  # mode="zeros"
        "clamp": cuda.runtime.cudaAddressModeClamp,  # mode="edges"
        "mirror": cuda.runtime.cudaAddressModeMirror,  # mirror
        "wrap": cuda.runtime.cudaAddressModeWrap,  # periodic
    }
    check_supported(address_mode, address_modes, "address mode")
    filter_modes = {
        "linear": cuda.runtime.cudaFilterModeLinear,
        "nearest": cuda.runtime.cudaFilterModePoint,
    }
    check_supported(filter_mode, filter_modes, "filter mode")

    tex_format = dtype_kind_to_format_kind[np.dtype(dtype).kind]
    nbits = np.dtype(dtype).itemsize * 8
    ch_desc = cuda.texture.ChannelFormatDescriptor(nbits, 0, 0, 0, tex_format)

    # /!\ From the documentation:
    # /!\ The memory allocation of CUDAarray is done outside of CuPy's memory management (enabled by default)
    # due to CUDA's limitation. Users of CUDAarray should be cautious about any out-of-memory possibilities.
    cu_arr = cuda.texture.CUDAarray(ch_desc, width=shape[1], height=shape[0], flags=cuda.runtime.cudaArrayDefault)

    if from_image is not None:
        # NB. For 2D textures, copy_from expects shape (height, nch*width); nch=1 here
        cu_arr.copy_from(from_image)

    res_desc = cuda.texture.ResourceDescriptor(cuda.runtime.cudaResourceTypeArray, cuArr=cu_arr)

    read_mode = cuda.runtime.cudaReadModeNormalizedFloat if normalized_coords else cuda.runtime.cudaReadModeElementType
    tex_desc = cuda.texture.TextureDescriptor(
        addressModes=(address_modes[address_mode], address_modes[address_mode]),
        filterMode=filter_modes[filter_mode],
        readMode=read_mode,
        normalizedCoords=normalized_coords,
    )

    tex_obj = cuda.texture.TextureObject(res_desc, tex_desc)

    return tex_obj, cu_arr


int2_t = np.dtype({"names": ["x", "y"], "formats": [np.int32, np.int32]})


def cupy_array_from_ptr(ptr, shape, dtype, owner_reference):
    size_bytes = np.prod(shape) * np.dtype(dtype).itemsize
    arr_cupy_mem = cuda.UnownedMemory(ptr, size_bytes, owner_reference)  # TODO device_id ?
    arr_cupy_memptr = cuda.MemoryPointer(arr_cupy_mem, offset=0)
    return cupy_ndarray(shape, dtype=dtype, memptr=arr_cupy_memptr)  # pylint: disable=E1123


def copy_to_cuarray_with_offset(dst_cuarray, src_array, offset_x=0, offset_y=0):
    """
    Copy a cupy.ndarray into a CUDA Array (matrix-like data structures that bakes textures).

    Copies a matrix ('height' rows of 'width' bytes each)
    from the memory area pointed to by 'src' to the CUDA array 'dst' starting at the upper left corner (wOffset, hOffset) [...]
    'spitch' is the width in memory in bytes of the 2D array pointed to by 'src', including any padding added to the end of each row.
      - 'wOffset' + 'width' must not exceed the width of the CUDA array 'dst'.
      - 'width' must not exceed 'spitch'.


    NB: for copies without offset, we can just use dst_cuarray.copy_from(src_cupyarray)
    """

    if isinstance(src_array, np.ndarray):
        memcpy_kind = cuda.runtime.memcpyHostToDevice
        src_array_ptr = src_array.ctypes.data
    else:
        memcpy_kind = cuda.runtime.memcpyDeviceToDevice
        src_array_ptr = src_array.data.ptr

    nbytes_per_item = np.dtype(src_array.dtype).itemsize
    h, w = src_array.shape

    w_offset = offset_x * nbytes_per_item
    h_offset = offset_y
    spitch = src_array.strides[-2]
    width = w * nbytes_per_item
    height = h

    cuda.runtime.memcpy2DToArray(
        dst_cuarray.ptr,  # intptr_t dst,
        w_offset,  # size_t wOffset : horizontal offset, probably in bytes
        h_offset,  # size_t hOffset : vertical offset, probably in pixels
        src_array_ptr,  # intptr_t src
        spitch,  # size_t spitch : source width in bytes (!) incl. padding (see cudaMallocPitch)
        width,  # size_t width : width of the matrix transfer, in bytes (!)
        height,  # size_t height : height of the matrix transfer, in pixels
        memcpy_kind,  # int kind: Type of transfer
    )


"""
def pycuda_to_cupy(arr_pycuda):
    arr_cupy_mem = cupy.cuda.UnownedMemory(arr_pycuda.ptr, arr_pycuda.size, arr_pycuda)
    arr_cupy_memptr = cupy.cuda.MemoryPointer(arr_cupy_mem, offset=0)
    return cupy.ndarray(arr_pycuda.shape, dtype=arr_pycuda.dtype, memptr=arr_cupy_memptr)  # pylint: disable=E1123


def cupy_to_pycuda(arr_cupy):
    return garray.empty(arr_cupy.shape, arr_cupy.dtype, gpudata=arr_cupy.data.ptr)
"""
