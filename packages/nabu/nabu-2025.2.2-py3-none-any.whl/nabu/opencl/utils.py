import numpy as np
from ..utils import check_supported, first_generator_item

try:
    import pyopencl as cl
    import pyopencl.array as parray

    __has_pyopencl__ = True
    __pyopencl_error_msg__ = None
except ImportError as err:
    __has_pyopencl__ = False
    __pyopencl_error_msg__ = str(err)
from ..resources.gpu import GPUDescription


def get_opencl_devices(
    device_type,
    vendor=None,
    name=None,
    order_by="global_mem_size",
    exclude_platforms=None,
    exclude_vendors=None,
    prefer_GPU=True,
):
    """
    List available OpenCL devices.

    Parameters
    ----------
    device_type: str
        Type of device, can be "CPU", "GPU" or "all".
    vendor: str, optional
        Filter devices by vendor, eg. "NVIDIA"
    name: Filter devices by names, eg. "GeForce RTX 3080"
    order_by: str, optional
        Order results in decreasing order of this value. Default is to sort by global memory size.
    exclude_platforms: str, optional
        Platforms to exclude, eg. "Portable Computing Language"
    exclude_vendors: str, optional
        Vendors to be excluded
    prefer_GPU: bool, optional
        Whether to put GPUs on top of the returned list, regardless of the "order_by" parameter.
        This can be useful when sorting by global memory size, as CPUs often have a bigger memory size.

    Returns
    -------
    devices: list of pyopencl.Device
        List of OpenCL devices matching the criteria, and ordered by the 'order_by' parameter.
        The list may be empty.

    """
    exclude_platforms = exclude_platforms or []
    exclude_vendors = exclude_vendors or []
    dev_type = {
        "cpu": cl.device_type.CPU,
        "gpu": cl.device_type.GPU,
        "accelerator": cl.device_type.ACCELERATOR,
        "all": cl.device_type.ALL,
        "any": cl.device_type.ALL,
    }
    device_type = device_type.lower()
    check_supported(device_type, dev_type.keys(), "device_type")

    devices = []
    for platform in cl.get_platforms():
        if vendor is not None and vendor.lower() not in platform.vendor.lower():
            continue
        if any(excluded_platform.lower() in platform.name.lower() for excluded_platform in exclude_platforms):
            continue
        if any(excluded_vendor.lower() in platform.vendor.lower() for excluded_vendor in exclude_vendors):
            continue
        for device in platform.get_devices():
            if device.type & dev_type[device_type] == 0:
                continue
            if name is not None and name.lower() not in device.name.lower():
                continue
            devices.append(device)
    if order_by is not None:
        devices = sorted(devices, key=lambda dev: getattr(dev, order_by), reverse=True)
    if prefer_GPU:
        # put GPUs devices on top of the list
        devices = [dev for dev in devices if dev.type & dev_type["gpu"] > 0] + [
            dev for dev in devices if dev.type & dev_type["gpu"] == 0
        ]
    return devices


def usable_opencl_devices():
    """
    Test the available OpenCL platforms/devices.

    Returns
    --------
    platforms: dict
        Dictionary where the key is the platform name, and the value is a list
        of `silx.opencl.common.Device` object.
    """
    platforms = {}
    for platform in cl.get_platforms():
        platforms[platform.name] = platform.get_devices()
    return platforms


def detect_opencl_gpus():
    """
    Get the available OpenCL-compatible GPUs.

    Returns
    --------
    gpus: dict
        Nested dictionary where the keys are OpenCL platform names,
        values are dictionary of GPU IDs and `silx.opencl.common.Device` object.
    error_msg: str
        In the case where there is an error, the message is returned in this item.
        Otherwise, it is a None object.
    """
    gpus = {}
    error_msg = None
    if not (__has_pyopencl__):
        return {}, __pyopencl_error_msg__
    try:
        platforms = usable_opencl_devices()
    except Exception as exc:
        error_msg = str(exc)
    if error_msg is not None:
        return {}, error_msg
    for platform_name, devices in platforms.items():
        for d_id, device in enumerate(devices):
            if device.type == cl.device_type.GPU:  # and bool(device.available):
                if platform_name not in gpus:
                    gpus[platform_name] = {}
                gpus[platform_name][d_id] = device
    return gpus, None


def collect_opencl_gpus():
    """
    Return a dictionary of platforms and brief description of each OpenCL-compatible
    GPU with a few fields
    """
    gpus_detected, error_msg = detect_opencl_gpus()
    if error_msg is not None:
        return None
    opencl_gpus = {}
    for platform, gpus in gpus_detected.items():
        for gpu_id, gpu in gpus.items():
            if platform not in opencl_gpus:
                opencl_gpus[platform] = {}
            opencl_gpus[platform][gpu_id] = GPUDescription(gpu, device_id=gpu_id).get_dict()
            opencl_gpus[platform][gpu_id]["platform"] = platform
    return opencl_gpus


def collect_opencl_cpus():
    """
    Return a dictionary of platforms and brief description of each OpenCL-compatible
    CPU with a few fields
    """
    opencl_cpus = {}
    platforms = usable_opencl_devices()
    for platform, devices in platforms.items():
        if "cuda" in platform.lower():
            continue
        opencl_cpus[platform] = {}
        for device_id, device in enumerate(devices):  # device_id might be inaccurate
            if device.type != cl.device_type.CPU:
                continue
            opencl_cpus[platform][device_id] = GPUDescription(device).get_dict()
            opencl_cpus[platform][device_id]["platform"] = platform
    return opencl_cpus


def get_opencl_context(device_type, **kwargs):
    """
    Create an OpenCL context. Please refer to 'get_opencl_devices' documentation
    """
    devices = get_opencl_devices(device_type, **kwargs)
    if devices == []:
        raise RuntimeError("No OpenCL device found for device_type='%s' and %s" % (device_type, str(kwargs)))
    return cl.Context([devices[0]])


def replace_array_memory(arr, new_shape):
    """
    Replace the underlying buffer data of a  `pyopencl.array.Array`.
    This function is dangerous !
    It should merely be used to clear memory, the array should not be used afterwise.
    """
    arr.data.release()
    arr.base_data = cl.Buffer(arr.context, cl.mem_flags.READ_WRITE, np.prod(new_shape) * arr.dtype.itemsize)
    arr.shape = new_shape
    # strides seems to be updated by pyopencl
    return arr


def pick_opencl_cpu_platform(opencl_cpus):
    """
    Pick the best OpenCL implementation for the opencl cpu.
    This function assume that there is only one opencl-enabled CPU on the
    current machine, but there might be several OpenCL implementations/vendors.


    Parameters
    ----------
    opencl_cpus: dict
        Dictionary with the available opencl-enabled CPUs.
        Usually obtained with collect_opencl_cpus().

    Returns
    -------
    cpu: dict
        A dictionary describing the CPU.
    """
    if len(opencl_cpus) == 0:
        raise ValueError("No CPU to pick")
    name2device = {}
    for platform, devices in opencl_cpus.items():
        for device_id, device_desc in devices.items():  # noqa: PERF102
            name2device.setdefault(device_desc["name"], [])
            name2device[device_desc["name"]].append(platform)
    if len(name2device) > 1:
        raise ValueError("Expected at most one CPU but got %d: %s" % (len(name2device), list(name2device.keys())))
    cpu_name = first_generator_item(name2device.keys())
    platforms = name2device[cpu_name]
    # Several platforms for the same CPU
    res = opencl_cpus[platforms[0]]
    if len(platforms) > 1:  # noqa: SIM102
        if "intel" in cpu_name.lower():
            for platform in platforms:
                if "intel" in platform.lower():
                    res = opencl_cpus[platform]
    #
    return res[first_generator_item(res.keys())]


def allocate_texture(ctx, shape, support_1D=False):
    """
    Allocate an OpenCL image ("texture").

    Parameters
    ----------
    ctx: OpenCL context
        OpenCL context
    shape: tuple of int
        Shape of the image. Note that pyopencl and OpenCL < 1.2
        do not support 1D images, so 1D images are handled as 2D with one row
    support_1D: bool, optional
         force the image to be 1D if the shape has only one dim
    """
    if len(shape) == 1 and not (support_1D):
        shape = (1,) + shape
    return cl.Image(
        ctx,
        cl.mem_flags.READ_ONLY | cl.mem_flags.USE_HOST_PTR,
        cl.ImageFormat(cl.channel_order.INTENSITY, cl.channel_type.FLOAT),
        hostbuf=np.zeros(shape[::-1], dtype=np.float32),
    )


def check_textures_availability(ctx):
    """
    Check whether textures are supported on the current OpenCL context.
    """
    try:
        dummy_texture = allocate_texture(ctx, (16, 16))
        # Need to further access some attributes (pocl)
        dummy_height = dummy_texture.height
        textures_available = True
        del dummy_texture, dummy_height
    except (cl.RuntimeError, cl.LogicError):
        textures_available = False
    # Nvidia Fermi GPUs (compute capability 2.X) do not support opencl read_imagef
    # There is no way to detect this until a kernel is compiled
    try:
        cc = ctx.devices[0].compute_capability_major_nv
        textures_available &= cc >= 3
    except (cl.LogicError, AttributeError):  # probably not a Nvidia GPU
        pass
    #
    return textures_available


def copy_to_texture(queue, dst_texture, src_array, dtype=np.float32):
    shape = src_array.shape
    if isinstance(src_array, parray.Array):
        return cl.enqueue_copy(queue, dst_texture, src_array.data, offset=0, origin=(0, 0), region=shape[::-1])
    elif isinstance(src_array, np.ndarray):
        if not (src_array.flags["C_CONTIGUOUS"] and src_array.dtype == dtype):
            src_array = np.ascontiguousarray(src_array, dtype=dtype)
        return cl.enqueue_copy(queue, dst_texture, src_array, origin=(0, 0), region=shape[::-1])
    else:
        raise TypeError("Unknown source array type")
