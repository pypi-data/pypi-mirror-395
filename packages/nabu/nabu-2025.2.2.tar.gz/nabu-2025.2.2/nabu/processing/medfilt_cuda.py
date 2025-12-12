from os.path import dirname
import numpy as np
from ..utils import updiv, get_cuda_srcfile
from nabu.cuda.kernel import CudaKernel
from ..cuda.processing import CudaProcessing


class MedianFilter:
    """
    A class for performing median filter on GPU with CUDA
    """

    def __init__(
        self,
        shape,
        footprint=(3, 3),
        mode="reflect",
        threshold=None,
        cuda_options=None,
        abs_diff=False,
    ):
        """Constructor of Cuda Median Filter.

        Parameters
        ----------
        shape: tuple
            Shape of the array, in the format (n_rows, n_columns)
        footprint: tuple
            Size of the median filter, in the format (y, x).
        mode: str
            Boundary handling mode. Available modes are:
               - "reflect": cba|abcd|dcb
               - "nearest": aaa|abcd|ddd
               - "wrap": bcd|abcd|abc
               - "constant": 000|abcd|000

            Default is "reflect".
        threshold: float, optional
            Threshold for the "thresholded median filter".
            A thresholded median filter only replaces a pixel value by the median
            if this pixel value is greater or equal than median + threshold.
        abs_diff: bool, optional
            Whether to perform conditional threshold as abs(value - median)

        Notes
        ------
        Please refer to the documentation of the CudaProcessing class for
        the other parameters.
        """
        self.cuda_processing = CudaProcessing(**(cuda_options or {}))
        self._set_params(shape, footprint, mode, threshold, abs_diff)
        self.cuda_processing.init_arrays_to_none(["d_input", "d_output"])
        self._init_kernels()

    def _set_params(self, shape, footprint, mode, threshold, abs_diff):
        self.data_ndim = len(shape)
        if self.data_ndim == 2:
            ny, nx = shape
            nz = 1
        elif self.data_ndim == 3:
            nz, ny, nx = shape
        else:
            raise ValueError("Expected 2D or 3D data")
        self.shape = shape
        self.Nx = np.int32(nx)
        self.Ny = np.int32(ny)
        self.Nz = np.int32(nz)
        if len(footprint) != 2:
            raise ValueError("3D median filter is not implemented yet")
        if not ((footprint[0] & 1) and (footprint[1] & 1)):
            raise ValueError("Must have odd-sized footprint")
        self.footprint = footprint
        self._set_boundary_mode(mode)
        self.do_threshold = False
        self.abs_diff = abs_diff
        if threshold is not None:
            self.threshold = np.float32(threshold)
            self.do_threshold = True
        else:
            self.threshold = np.float32(0)

    def _set_boundary_mode(self, mode):
        self.mode = mode
        # Some code duplication from convolution
        self._c_modes_mapping = {
            "periodic": 2,
            "wrap": 2,
            "nearest": 1,
            "replicate": 1,
            "reflect": 0,
            "constant": 3,
        }
        mp = self._c_modes_mapping
        if self.mode.lower() not in mp:
            raise ValueError(
                """
                Mode %s is not available. Available modes are:
                %s
                """
                % (self.mode, str(mp.keys()))
            )
        if self.mode.lower() == "constant":
            raise NotImplementedError("mode='constant' is not implemented yet")
        self._c_conv_mode = mp[self.mode]

    def _init_kernels(self):
        fname = get_cuda_srcfile("medfilt.cu")
        nabu_cuda_dir = dirname(fname)
        self.medfilt_kernel = CudaKernel(
            "medfilt2d",
            filename=fname,
            options=(
                "-DUSED_CONV_MODE=%d" % self._c_conv_mode,
                "-DMEDFILT_X=%d" % self.footprint[1],
                "-DMEDFILT_Y=%d" % self.footprint[0],
                "-DDO_THRESHOLD=%d" % (int(self.do_threshold) + int(self.abs_diff)),
                f"-I{nabu_cuda_dir}",
            ),
        )
        # Blocks, grid
        self._block_size = {2: (32, 32, 1), 3: (16, 8, 8)}[self.data_ndim]  # TODO tune
        self._n_blocks = tuple([updiv(a, b) for a, b in zip(self.shape[::-1], self._block_size)])

    def medfilt2(self, image, output=None):
        """
        Perform a median filter on an image (or batch of images).

        Parameters
        -----------
        images: numpy.ndarray or cupy array
            2D image or 3D stack of 2D images
        output: numpy.ndarray or cupy array, optional
            Output of filtering. If provided, it must have the same shape
            as the input array.
        """
        self.cuda_processing.set_array("d_input", image)
        if output is not None:
            self.cuda_processing.set_array("d_output", output)
        else:
            self.cuda_processing.allocate_array("d_output", self.shape)
        self.medfilt_kernel(
            self.cuda_processing.d_input,
            self.cuda_processing.d_output,
            self.Nx,
            self.Ny,
            self.Nz,
            self.threshold,
            grid=self._n_blocks,
            block=self._block_size,
        )
        self.cuda_processing.recover_arrays_references(["d_input", "d_output"])
        if output is None:
            return self.cuda_processing.d_output.get()
        else:
            return output
