from nabu.processing.muladd_cuda import CudaMulAdd
from ..processing.convolution_cuda import Convolution
from ..cuda.processing import CudaProcessing
from .unsharp import UnsharpMask


class CudaUnsharpMask(UnsharpMask):
    def __init__(self, shape, sigma, coeff, mode="reflect", method="gaussian", **cuda_options):
        """
        Unsharp Mask, cuda backend.
        """
        super().__init__(shape, sigma, coeff, mode=mode, method=method)
        self.cuda_processing = CudaProcessing(**(cuda_options or {}))
        self._init_convolution()
        self._init_mad_kernel()
        self.cuda_processing.init_arrays_to_none(["_d_out"])

    def _init_convolution(self):
        self.convolution = Convolution(
            self.shape,
            self._gaussian_kernel,
            mode=self.mode,
            extra_options={  # Use the lowest amount of memory
                "allocate_input_array": False,
                "allocate_output_array": False,
                "allocate_tmp_array": True,
            },
        )

    def _init_mad_kernel(self):
        self.mul_add = CudaMulAdd()

    def unsharp(self, image, output=None):
        if output is None:
            output = self.cuda_processing.allocate_array("_d_out", self.shape, "f")
        self.convolution(image, output=output)
        if self.method == "gaussian":
            # res = (1 + self.coeff) * image - self.coeff * image_b
            self.mul_add(output, image, -self.coeff, 1.0 + self.coeff)
        elif self.method == "log":
            # output = output * coeff + image   where output was image_blurred
            self.mul_add(output, image, self.coeff, 1.0)
        else:  # "imagej":
            # output = (image - coeff*image_blurred)/(1-coeff)  where output was image_blurred
            self.mul_add(output, image, -self.coeff / (1 - self.coeff), 1.0 / (1 - self.coeff))
        return output
