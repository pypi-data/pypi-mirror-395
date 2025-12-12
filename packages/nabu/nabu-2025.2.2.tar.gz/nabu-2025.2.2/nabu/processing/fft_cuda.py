import os
import warnings
from importlib import import_module
from functools import lru_cache
from multiprocessing import get_context
from multiprocessing.pool import Pool
from ..utils import BaseClassError, check_supported, no_decorator
from .fft_base import _BaseFFT, _BaseVKFFT
from ..cuda.processing import CudaProcessing

try:
    from pyvkfft.cuda import VkFFTApp as CudaVkFFTApp

    __has_vkfft__ = True
except (ImportError, OSError):
    __has_vkfft__ = False
    CudaVkFFTApp = BaseClassError

try:
    import cupy.fft as cupy_fft

    __has_cupy__ = True
except (ImportError, OSError):
    __has_cupy__ = False


n_cached_ffts = int(os.getenv("NABU_FFT_CACHE", "0"))


maybe_cached = lru_cache(maxsize=n_cached_ffts) if n_cached_ffts > 0 else no_decorator


@maybe_cached
def _get_vkfft_cuda(*args, **kwargs):
    return CudaVkFFTApp(*args, **kwargs)


def get_vkfft_cuda(slf, *args, **kwargs):
    return _get_vkfft_cuda(*args, **kwargs)


class VKCUFFT(_BaseVKFFT):
    """
    Cuda FFT, using VKFFT backend
    """

    implem = "vkfft"
    backend = "cuda"
    ProcessingCls = CudaProcessing
    get_fft_obj = get_vkfft_cuda

    def _init_backend(self, backend_options):
        super()._init_backend(backend_options)
        self._vkfft_other_init_kwargs = {"stream": self.processing.stream}


def _has_fft_implem(class_name, module_name, component_check=None):
    # should be run from within a Process
    try:
        mod = import_module(module_name)  # eg. 'import nabu.processing.fft_cuda'
        if component_check is not None and getattr(mod, component_check, False) is False:  # eg. '__has_vkfft__'
            return False
        fft_class = getattr(mod, class_name)

        from nabu.cuda.utils import get_cuda_stream

        _ = get_cuda_stream(force_create=True)
        _ = fft_class((16,), "f")
        avail = True
    except (ImportError, RuntimeError, OSError, NameError) as exc:
        avail = False
        print(exc)
    return avail


def has_fft_implem(name, safe=True):
    if not safe:
        return _has_fft_implem(name, "nabu.processing.fft_cuda")
    try:
        ctx = get_context("spawn")
        with Pool(1, context=ctx) as p:
            v = p.apply(_has_fft_implem, args=(name, "nabu.processing.fft_cuda"))
    except AssertionError:
        # Can get AssertionError: daemonic processes are not allowed to have children
        # if the calling code is already a subprocess
        return _has_fft_implem(name, "nabu.processing.fft_cuda")
    return v


@lru_cache(maxsize=2)
def has_vkfft(safe=True):
    return has_fft_implem("VKCUFFT", safe=safe)


@lru_cache(maxsize=2)
def has_cupyfft(safe=True):
    return has_fft_implem("CupyCUFFT", safe=safe)


@lru_cache(maxsize=2)
def get_fft_class(backend="vkfft"):
    backends = {
        "vkfft": VKCUFFT,
        "pyvkfft": VKCUFFT,
        "cupy": CupyCUFFT,
        "cufft": CupyCUFFT,
    }

    def get_fft_cls(asked_fft_backend):
        asked_fft_backend = asked_fft_backend.lower()
        check_supported(asked_fft_backend, list(backends.keys()), "Cuda FFT backend name")
        return backends[asked_fft_backend]

    asked_fft_backend_env = os.environ.get("NABU_FFT_BACKEND", "")
    if asked_fft_backend_env != "":
        return get_fft_cls(asked_fft_backend_env)

    avail_fft_implems = get_available_fft_implems()
    if len(avail_fft_implems) == 0:
        raise RuntimeError("Could not any Cuda FFT implementation. Please install pyvkfft and/or cupy")
    if backend not in avail_fft_implems:
        warnings.warn("Could not get FFT backend '%s'" % backend, RuntimeWarning)
        backend = avail_fft_implems[0]

    return get_fft_cls(backend)


@lru_cache(maxsize=1)
def get_available_fft_implems():
    avail_implems = []
    if has_vkfft(safe=True):
        avail_implems.append("vkfft")
    if has_cupyfft(safe=True):
        avail_implems.append("cupy")
    return avail_implems


class CupyCUFFT(_BaseFFT):

    implem = "cupy"
    backend = "cuda"
    ProcessingCls = CudaProcessing

    def _configure_batched_transform(self):
        # See documentation. Use this if we want to lessen the memory footprint at the expense of performances
        # cupy.fft.config.enable_nd_planning = False
        ...

    def _patch_cupy_ifft_kwargs(self, ifft_kwargs):
        """
        Patch cupy.irfft for odd-sized last dimensions.

        cupy irfft does not yield the same array shape as numpy/vkfft
          eg:   cupy.fft.irfft2(cp.fft(dz)).shape != np.fft.ifft2(np.fft.fft2(hz)
        numpy/vkfft are able to fall-back on the original array shape, but for cupy,
        we have to use the "s=" argument to fall back on the original data shape.
        """
        fft_ndim = len(self.axes)
        kwarg_key = "n" if fft_ndim == 1 else "s"

        transf_axis_shp = self.get_transformed_axes_shape()
        if len(transf_axis_shp) == 1:
            transf_axis_shp = transf_axis_shp[0]
        ifft_kwargs[kwarg_key] = transf_axis_shp

    def _compute_fft_plans(self):
        data_ndim = len(self.shape)
        fft_ndim = len(self.axes)
        fft_kwargs = {}
        if data_ndim > 1:
            if fft_ndim == 1:
                fft_kwargs = {"axis": self.axes[0]}
            else:
                fft_kwargs = {"axes": self.axes}
        ifft_kwargs = fft_kwargs.copy()
        self._patch_cupy_ifft_kwargs(ifft_kwargs)

        self._fft_kwargs = fft_kwargs
        self._ifft_kwargs = ifft_kwargs

        if fft_ndim == 1:
            fft_func = cupy_fft.fft if not (self.r2c) else cupy_fft.rfft
            ifft_func = cupy_fft.ifft if not (self.r2c) else cupy_fft.irfft
        elif fft_ndim == 2:
            fft_func = cupy_fft.fft2 if not (self.r2c) else cupy_fft.rfft2
            ifft_func = cupy_fft.ifft2 if not (self.r2c) else cupy_fft.irfft2
        else:
            fft_func = cupy_fft.fftn if not (self.r2c) else cupy_fft.rfftn
            ifft_func = cupy_fft.ifftn if not (self.r2c) else cupy_fft.irfftn
        self._fft_func = fft_func
        self._ifft_func = ifft_func

    def fft(self, array, output=None):
        out = self._fft_func(array, **self._fft_kwargs)
        if output is not None:
            output[:] = out[:]
        return output if output is not None else out

    def ifft(self, array, output=None):
        print(self._ifft_kwargs)
        out = self._ifft_func(array, **self._ifft_kwargs)
        if output is not None:
            output[:] = out[:]
        return output if output is not None else out
