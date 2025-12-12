import numpy as np
from ..opencl.kernel import OpenCLKernel
from ..opencl.processing import OpenCLProcessing
from ..utils import get_opencl_srcfile
from .sinogram import SinoMult


class OpenCLSinoMult(SinoMult):
    def __init__(self, sino_shape, rot_center, **opencl_options):
        super().__init__(sino_shape, rot_center)
        self.opencl_processing = OpenCLProcessing(**opencl_options)
        self._init_kernel()

    def _init_kernel(self):
        self.halftomo_kernel = OpenCLKernel(
            "halftomo_prepare_sinogram",
            self.opencl_processing.queue,
            filename=get_opencl_srcfile("halftomo.cl"),
        )
        self.d_weights = self.opencl_processing.set_array("d_weights", self.weights)
        self._halftomo_kernel_other_args = [
            self.d_weights,
            np.int32(self.n_a),
            np.int32(self.n_x),
            np.int32(self.start_x),
            np.int32(self.end_x),
        ]
        self._global_size = (self.n_x, self.n_a)
        self._local_size = None  # (32, 32, 1)  # tune ?

    def prepare_sino(self, sino):
        sino = self.opencl_processing.set_array("d_sino", sino)
        ev = self.halftomo_kernel(
            sino,
            *self._halftomo_kernel_other_args,
            global_size=self._global_size,
            local_size=self._local_size,
        )
        if self.opencl_processing.device_type == "cpu":
            ev.wait()
        return sino
