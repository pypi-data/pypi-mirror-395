"""
gpu.py: general-purpose utilities for GPU
"""

from ..utils import check_supported

try:
    from cupy.cuda import Device as CudaDevice
    from cupy.cuda.runtime import getDeviceProperties

    __has_cupy__ = True
except ImportError:
    __has_cupy__ = False
    CudaDevice = type(None)
try:
    from pyopencl import Device as CLDevice

    __has_pyopencl__ = True
except ImportError:
    CLDevice = type(None)
    __has_pyopencl__ = False

#
# silx.opencl.common.Device cannot be supported as long as
# silx.opencl instantiates the "ocl" singleton in __init__,
# leaving opencl contexts all over the place in some cases
#


class GPUDescription:
    """
    Simple description of a Graphical Processing Unit.
    This class is designed to be simple to understand, and to be serializable
    for being used by dask.distributed.
    """

    def __init__(self, device, vendor=None, device_id=None):
        """
        Create a description from a device.

        Parameters
        ----------
        device: `cupy.cuda.Device` or `pyopencl.Device`
            Class describing a GPU device.
        """
        is_cuda_device = isinstance(device, CudaDevice)
        is_cl_device = isinstance(device, CLDevice)

        if is_cuda_device:
            self._init_from_cuda_device(device)
        elif is_cl_device:
            self._init_from_cl_device(device)
            self._set_other_attrs(vendor, device_id)
        else:
            raise ValueError("Expected `cupy.cuda.device.Device` or `pyopencl.Device`")

    def _init_from_cuda_device(self, device):
        attrs = getDeviceProperties(device.id)
        self._dict = {
            "type": "cuda",
            "name": attrs["name"].decode(),
            "memory_GB": device.mem_info[1] / 1e9,  # legacy (that was what pyuda reported)
            "memory_avail_GB": device.mem_info[0] / 1e9,
            "memory_total_GB": device.mem_info[1] / 1e9,
            "compute_capability": device.compute_capability,  # /!\ went from tuple (eg. (7, 0)) to str (eg. "70")
            "device_id": device.id,
        }

    def _init_from_cl_device(self, device):
        self._dict = {
            "type": "opencl",
            "name": device.name,
            "memory_GB": device.global_mem_size / 1e9,  # legacy
            "memory_avail_GB": device.global_mem_size / 1e9,  # not supported by pyopencl (?)
            "memory_total_GB": device.global_mem_size / 1e9,  #
            "vendor": device.vendor,
        }

    def _set_other_attrs(self, vendor, device_id):
        if vendor is not None:
            self._dict["vendor"] = vendor
        if device_id is not None:
            self._dict["device_id"] = device_id  # device ID for OpenCL (!= platform ID)

    def _dict_to_self(self):
        for key, val in self._dict.items():
            setattr(self, key, val)

    def get_dict(self):
        return self._dict


GPU_PICK_METHODS = ["cuda", "auto"]


def pick_gpus(method, cuda_gpus, opencl_platforms, n_gpus):
    check_supported(method, GPU_PICK_METHODS, "GPU picking method")
    if method == "cuda":
        return pick_gpus_nvidia(cuda_gpus, n_gpus)
    elif method == "auto":
        return pick_gpus_auto(cuda_gpus, opencl_platforms, n_gpus)
    else:
        return []


# TODO Fix this function, it is broken:
#  - returns something when n_gpus = 0
#  - POCL increments device_id by 1 !
def pick_gpus_auto(cuda_gpus, opencl_platforms, n_gpus):
    """
    Pick `n_gpus` devices with the best available driver.

    This function browse the visible Cuda GPUs and Opencl platforms to pick
    the GPUs with the best driver.
    A worker might see several implementations of a GPU driver.
    For example with Nvidia hardware, we can see:
      - The Cuda implementation (nvidia-cuda-toolkit)
      - OpenCL implementation by Nvidia (nvidia-opencl-icd)
      - OpenCL implementation by Portable OpenCL

    Parameters
    ----------
    cuda_gpu: dict
        Dictionary where each key is an ID, and the value is a dictionary
        describing some attributes of the GPU (obtained with `GPUDescription`)
    opencl_platforms: dict
        Dictionary where each key is the platform name, and the value is a list
        of dictionary descriptions.
    n_gpus: int
        Number of GPUs to pick.
    """

    def gpu_equal(gpu1, gpu2):
        # TODO find a better test ?
        # Some information are not always available depending on the opencl vendor !
        return (gpu1["device_id"] == gpu2["device_id"]) and (gpu1["name"] == gpu2["name"])

    def is_in_gpus(avail_gpus, query_gpu):
        for gpu in avail_gpus:  # noqa: SIM110
            if gpu_equal(gpu, query_gpu):
                return True
        return False

    # If some Nvidia hardware is visible, add it without question.
    # In the case we don't want it, we should either re-run resources discovery
    # with `try_cuda=False`, or mask individual devices with CUDA_VISIBLE_DEVICES.
    chosen_gpus = list(cuda_gpus.values())
    if len(chosen_gpus) >= n_gpus:
        return chosen_gpus
    for platform, gpus in opencl_platforms.items():  # noqa: PERF102
        for gpu_id, gpu in gpus.items():  # noqa: PERF102
            if not (is_in_gpus(chosen_gpus, gpu)):
                # TODO prioritize some OpenCL implementations ?
                chosen_gpus.append(gpu)
    if len(chosen_gpus) < n_gpus:
        raise ValueError("Not enough GPUs: could only collect %d/%d" % (len(chosen_gpus), n_gpus))
    return chosen_gpus


def pick_gpus_nvidia(cuda_gpus, n_gpus):
    """
    Pick one or more Nvidia GPUs.
    """
    if len(cuda_gpus) < n_gpus:
        raise ValueError("Not enough Nvidia GPU: requested %d, but can get only %d" % (n_gpus, len(cuda_gpus)))
    # Sort GPUs by computing capabilities, pick the "best" ones
    gpus_cc = []
    for gpu_id, gpu in cuda_gpus.items():
        cc = gpu["compute_capability"]
        gpus_cc.append((gpu_id, cc[0] + 0.1 * cc[1]))
    gpus_cc_sorted = sorted(gpus_cc, key=lambda x: x[1], reverse=True)
    res = []
    for i in range(n_gpus):
        res.append(cuda_gpus[gpus_cc_sorted[i][0]])  # noqa: PERF401
    return res
