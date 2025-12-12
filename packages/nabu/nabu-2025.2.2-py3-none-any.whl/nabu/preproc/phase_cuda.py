import numpy as np

from ..processing.padding_cuda import CudaPadding
from ..utils import get_cuda_srcfile, check_supported, docstring
from ..cuda.processing import CudaProcessing
from ..processing.fft_cuda import get_fft_class
from .phase import PaganinPhaseRetrieval


class CudaPaganinPhaseRetrieval(PaganinPhaseRetrieval):
    supported_paddings = ["zeros", "constant", "edge"]

    @docstring(PaganinPhaseRetrieval)
    def __init__(
        self,
        shape,
        distance=0.5,
        energy=20,
        delta_beta=250.0,
        pixel_size=1e-6,
        padding="edge",
        cuda_options=None,
        fftw_num_threads=None,  # COMPAT.
        fft_num_threads=None,
        fft_backend="vkfft",
    ):
        """
        Please refer to the documentation of
        nabu.preproc.phase.PaganinPhaseRetrieval
        """
        padding = self._check_padding(padding)
        self.cuda_processing = CudaProcessing(**(cuda_options or {}))
        super().__init__(
            shape,
            distance=distance,
            energy=energy,
            delta_beta=delta_beta,
            pixel_size=pixel_size,
            padding=padding,
            use_rfft=True,
            fft_num_threads=False,
        )
        self._init_gpu_arrays()
        self._init_fft(fft_backend)
        self._init_padding_kernel()
        self._init_mult_kernel()

    def _check_padding(self, padding):
        check_supported(padding, self.supported_paddings, "padding")
        if padding == "zeros":
            padding = "constant"
        return padding

    def _init_gpu_arrays(self):
        self.d_paganin_filter = self.cuda_processing.to_device(
            "d_paganin_filter", np.ascontiguousarray(self.paganin_filter, dtype=np.float32)
        )

    # overwrite parent method, don't initialize any FFT plan
    def _get_fft(self, use_rfft, fft_num_threads):
        self.use_rfft = use_rfft

    def _init_fft(self, fft_backend):
        fft_cls = get_fft_class(backend=fft_backend)
        self.cufft = fft_cls(shape=self.data_padded.shape, dtype=np.float32, r2c=True)
        self.d_radio_padded = self.cuda_processing.allocate_array("d_radio_padded", self.cufft.shape, "f")
        self.d_radio_f = self.cuda_processing.allocate_array("d_radio_f", self.cufft.shape_out, np.complex64)

    def _init_padding_kernel(self):
        self.padding_kernel = CudaPadding(
            shape=self.shape,
            pad_width=(
                (self.pad_top_len, self.pad_bottom_len),
                (self.pad_left_len, self.pad_right_len),
            ),
            mode=self.padding,
        )

    def _init_mult_kernel(self):
        self.cpxmult_kernel = self.cuda_processing.kernel(
            "inplace_complexreal_mul_2Dby2D",
            filename=get_cuda_srcfile("ElementOp.cu"),
        )
        self.cpxmult_kernel_args = [
            self.d_radio_f,
            self.d_paganin_filter,
            self.shape_padded[1] // 2 + 1,
            self.shape_padded[0],
        ]

    def get_output(self, output):
        sub_region = slice(self.pad_top_len, -self.pad_bottom_len), slice(self.pad_left_len, -self.pad_right_len)
        if output is None:
            # copy D2H
            return self.d_radio_padded[sub_region].get()
        assert output.shape == self.shape
        assert output.dtype == np.float32
        output[:, :] = self.d_radio_padded[sub_region]
        return output

    def apply_filter(self, radio, output=None):
        d_radio = self.cuda_processing.set_array("d_radio", radio)
        self.padding_kernel(d_radio, output=self.d_radio_padded)
        self.cufft.fft(self.d_radio_padded, output=self.d_radio_f)
        self.cpxmult_kernel(*self.cpxmult_kernel_args)
        self.cufft.ifft(self.d_radio_f, output=self.d_radio_padded)

        return self.get_output(output)

    __call__ = apply_filter

    retrieve_phase = apply_filter
