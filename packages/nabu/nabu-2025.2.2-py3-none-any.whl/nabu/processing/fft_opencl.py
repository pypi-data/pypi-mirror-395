from functools import lru_cache
import os
from multiprocessing import get_context
from multiprocessing.pool import Pool

from ..utils import BaseClassError, no_decorator
from .fft_base import _BaseVKFFT
from ..opencl.processing import OpenCLProcessing

try:
    from pyvkfft.opencl import VkFFTApp as OpenCLVkFFTApp

    __has_vkfft__ = True
except (ImportError, OSError):
    __has_vkfft__ = False
    vk_clfft = None
    OpenCLVkFFTApp = BaseClassError

n_cached_ffts = int(os.getenv("NABU_FFT_CACHE", "0"))
maybe_cached = lru_cache(maxsize=n_cached_ffts) if n_cached_ffts > 0 else no_decorator


@maybe_cached
def _get_vkfft_opencl(*args, **kwargs):
    return OpenCLVkFFTApp(*args, **kwargs)


def get_vkfft_opencl(slf, *args, **kwargs):
    return _get_vkfft_opencl(*args, **kwargs)


class VKCLFFT(_BaseVKFFT):
    """
    OpenCL FFT, using VKFFT backend
    """

    implem = "vkfft"
    backend = "opencl"
    ProcessingCls = OpenCLProcessing
    get_fft_obj = get_vkfft_opencl

    def _init_backend(self, backend_options):
        super()._init_backend(backend_options)
        self._vkfft_other_init_kwargs = {"queue": self.processing.queue}


def _has_vkfft(x):
    # should be run from within a Process
    try:
        from nabu.processing.fft_opencl import VKCLFFT, __has_vkfft__

        if not __has_vkfft__:
            return False
        _ = VKCLFFT((16,), "f")
        avail = True
    except (RuntimeError, OSError):
        avail = False
    return avail


def has_vkfft(safe=True):
    """
    Determine whether pyvkfft is available.
    This function cannot be tested from a notebook/console, a proper entry point has to be created (if __name__ == "__main__").
    """
    if not safe:
        return _has_vkfft(None)
    try:
        ctx = get_context("spawn")
        with Pool(1, context=ctx) as p:
            v = p.map(_has_vkfft, [1])[0]
    except AssertionError:
        # Can get AssertionError: daemonic processes are not allowed to have children
        # if the calling code is already a subprocess
        return _has_vkfft(None)
    return v
