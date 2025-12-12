import numpy as np
from ..utils import get_opencl_srcfile
from ..opencl.processing import OpenCLProcessing
from ..processing.padding_opencl import OpenCLPadding
from ..opencl.memcpy import OpenCLMemcpy2D
from .filtering import SinoFilter

try:
    from pyvkfft.opencl import VkFFTApp as clfft  # pylint: disable=E0401

    __has_vkfft__ = True
except:
    __has_vkfft__ = False


class OpenCLSinoFilter(SinoFilter):
    def __init__(
        self,
        sino_shape,
        filter_name=None,
        padding_mode="zeros",
        crop_filtered_data=True,
        extra_options=None,
        opencl_options=None,
    ):
        self._opencl_options = opencl_options or {}
        self.opencl = OpenCLProcessing(**self._opencl_options)
        self.queue = self.opencl.queue
        super().__init__(
            sino_shape,
            filter_name=filter_name,
            padding_mode=padding_mode,
            crop_filtered_data=crop_filtered_data,
            extra_options=extra_options,
        )
        if not (crop_filtered_data):
            raise NotImplementedError  # TODO
        self._init_kernels()

    def _init_fft(self):
        if not (__has_vkfft__):
            raise ImportError("Please install pyvkfft to use this class")
        self.fft = clfft(self.sino_padded_shape, np.float32, self.queue, r2c=True, ndim=1, inplace=False)

    def _allocate_memory(self):
        self.d_sino_padded = self.opencl.allocate_array("d_sino_padded", self.sino_padded_shape, dtype=np.float32)
        self.d_sino_f = self.opencl.allocate_array("d_sino_f", self.sino_f_shape, np.complex64)
        self.d_filter_f = self.opencl.allocate_array("d_filter_f", (self.sino_f_shape[-1],), dtype=np.complex64)

    def set_filter(self, h_filt, normalize=True):
        super().set_filter(h_filt, normalize=normalize)
        self.d_filter_f[:] = self.filter_f[:]

    def _init_kernels(self):
        # pointwise complex multiplication
        fname = get_opencl_srcfile("ElementOp.cl")
        if self.ndim == 2:
            kernel_name = "inplace_complex_mul_2Dby1D"
        else:
            kernel_name = "inplace_complex_mul_3Dby1D"
        self.mult_kernel = self.opencl.kernel(kernel_name, filename=fname)
        # padding
        self.padding_kernel = OpenCLPadding(
            self.sino_shape,
            ((0, 0), (self.pad_left, self.pad_right)),
            mode=self.padding_mode,
            opencl_options={"queue": self.queue},
        )
        # memcpy2D
        self.memcpy2D = OpenCLMemcpy2D(queue=self.queue)

    def filter_sino(self, sino, output=None):
        self._check_array(sino)
        sino = self.opencl.set_array("sino", sino)

        # Padding
        self.padding_kernel.pad(sino, output=self.d_sino_padded)

        # FFT
        self.fft.fft(self.d_sino_padded, self.d_sino_f)

        # multiply padded sinogram with filter in the Fourier domain
        self.mult_kernel(
            self.d_sino_f,
            self.d_filter_f,
            *(np.int32(self.d_sino_f.shape[::-1])),  # pylint: disable=E1133
            # local_size=None,
            global_size=self.d_sino_f.shape[::-1],
        )  # TODO tune block size ?

        # iFFT
        self.fft.ifft(self.d_sino_f, self.d_sino_padded)

        # return
        if output is None:
            res = self.opencl.allocate_array("output", self.sino_shape)
        else:
            res = output
        if self.ndim == 2:
            # res[:] = self.d_sino_padded[:, self.pad_left : self.pad_left + self.dwidth]
            self.memcpy2D(res, self.d_sino_padded, res.shape[::-1], src_offset_xy=(self.pad_left, 0))
        else:
            res[:] = self.d_sino_padded[:, :, self.pad_left : self.pad_left + self.dwidth]
        return res

    __call__ = filter_sino
