"""
Base class for CudaKernel and OpenCLKernel
Should not be used directly
"""

from ..utils import updiv


class KernelBase:
    """
    A base class for OpenCL and Cuda kernels.

    Parameters
    -----------
    kernel_name: str
        Name of the CUDA kernel.
    filename: str, optional
        Path to the file name containing kernels definitions
    src: str, optional
        Source code of kernels definitions
    automation_params: dict, optional
        Automation parameters, see below

    Automation parameters
    ----------------------
    automation_params is a dictionary with the following keys and default values.
        guess_block: bool (True)
            If block is not specified during calls, choose a block size based on
            the size/dimensions of the first array.
            Mind that it is unlikely to be the optimal choice.
        guess_grid: bool (True):
            If the grid size is not specified during calls, choose a grid size
            based on the size of the first array.
        follow_device_ptr: bool (True)
            specify gpuarray.gpudata for all cuda GPUArrays (and pyopencl.array.data for pyopencl arrays).
            Otherwise, raise an error.
    """

    _default_automation_params = {
        "guess_block": True,
        "guess_grid": True,
        "follow_device_ptr": True,
    }

    def __init__(
        self,
        kernel_name,
        filename=None,
        src=None,
        automation_params=None,
        silent_compilation_warnings=False,
    ):
        self.check_filename_src(filename, src)
        self.set_automation_params(automation_params)
        self.silent_compilation_warnings = silent_compilation_warnings

    def check_filename_src(self, filename, src):
        err_msg = "Please provide either filename or src"
        if filename is None and src is None:
            raise ValueError(err_msg)
        if filename is not None and src is not None:
            raise ValueError(err_msg)
        if filename is not None:
            with open(filename) as fid:
                src = fid.read()
        self.filename = filename
        self.src = src

    def set_automation_params(self, automation_params):
        self.automation_params = self._default_automation_params.copy()
        self.automation_params.update(automation_params or {})

    @staticmethod
    def guess_grid_size(shape, block_size):
        # python: (z, y, x) -> cuda: (x, y, z)
        res = tuple(map(lambda x: updiv(x[0], x[1]), zip(shape[::-1], block_size)))
        if len(res) == 2:
            res += (1,)
        return res

    @staticmethod
    def guess_block_size(shape):
        """
        Guess a block size based on the shape of an array.
        """
        ndim = len(shape)
        if ndim == 1:
            return (128, 1, 1)
        if ndim == 2:
            return (32, 32, 1)
        else:
            return (16, 8, 8)

    def get_block_grid(self, *args, **kwargs):
        block = None
        grid = None
        if ("block" not in kwargs) or (kwargs["block"] is None):
            if self.automation_params["guess_block"]:
                block = self.guess_block_size(args[0].shape)
            else:
                raise ValueError("Please provide block size")
        else:
            block = kwargs["block"]
        if ("grid" not in kwargs) or (kwargs["grid"] is None):
            if self.automation_params["guess_grid"]:
                grid = self.guess_grid_size(args[0].shape, block)
            else:
                raise ValueError("Please provide block grid")
        else:
            grid = kwargs["grid"]
        self.last_block_size = block
        self.last_grid_size = grid
        return block, grid

    def follow_device_arr(self, args):
        raise ValueError("Base class")

    def _prepare_call(self, *args, **kwargs):
        block, grid = self.get_block_grid(*args, **kwargs)
        # pycuda crashes when any element of block/grid is not a python int (ex. numpy.int64).
        # A weird behavior once observed is "data.shape" returning (np.int64, int, int) (!).
        # Ensure that everything is a python integer.
        grid = tuple(int(x) for x in grid)
        if block is not None:
            block = tuple(int(x) for x in block)
        #
        args = self.follow_device_arr(args)

        return grid, block, args, kwargs
