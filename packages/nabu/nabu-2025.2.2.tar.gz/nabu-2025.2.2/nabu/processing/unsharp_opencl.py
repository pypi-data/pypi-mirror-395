try:
    import pyopencl.array as parray  # noqa: F401
    from pyopencl.elementwise import ElementwiseKernel
    from ..opencl.processing import OpenCLProcessing

    __have_opencl__ = True
except ImportError:
    __have_opencl__ = False
from .unsharp import UnsharpMask


class OpenclUnsharpMask(UnsharpMask):
    def __init__(
        self,
        shape,
        sigma,
        coeff,
        mode="reflect",
        method="gaussian",
        **opencl_options,
    ):
        """
        NB: For now, this class is designed to use the lowest amount of GPU memory
        as possible. Therefore, the input and output image/volumes are assumed
        to be already on device.
        """
        if not (__have_opencl__):
            raise ImportError("Need pyopencl")
        super().__init__(shape, sigma, coeff, mode=mode, method=method)
        self.cl_processing = OpenCLProcessing(**(opencl_options or {}))
        self._init_convolution()
        self._init_mad_kernel()

    def _init_convolution(self):
        # Do it here because silx creates OpenCL contexts all over the place at import
        from silx.opencl.convolution import Convolution as CLConvolution

        self.convolution = CLConvolution(
            self.shape,
            self._gaussian_kernel,
            mode=self.mode,
            ctx=self.cl_processing.ctx,
            extra_options={  # Use the lowest amount of memory
                "allocate_input_array": False,
                "allocate_output_array": False,
                "allocate_tmp_array": True,
                "dont_use_textures": True,
            },
        )

    def _init_mad_kernel(self):
        # parray.Array.mul_add is out of place...
        self.mad_kernel = ElementwiseKernel(
            self.cl_processing.ctx,
            "float* array, float fac, float* other, float otherfac",
            "array[i] = fac * array[i] + otherfac * other[i]",
            name="mul_add",
        )

    def unsharp(self, image, output):
        # For now image and output are assumed to be already allocated on device
        assert isinstance(image, self.cl_processing.array_class)
        assert isinstance(output, self.cl_processing.array_class)
        self.convolution(image, output=output)
        if self.method == "gaussian":
            self.mad_kernel(output, -self.coeff, image, 1.0 + self.coeff)
        elif self.method == "log":
            self.mad_kernel(output, self.coeff, image, 1.0)
        else:  # "imagej":
            self.mad_kernel(output, -self.coeff / (1 - self.coeff), image, 1.0 / (1 - self.coeff))
        return output


# Alias
OpenCLUnsharpMask = OpenclUnsharpMask
