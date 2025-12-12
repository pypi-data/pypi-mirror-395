import numpy as np
from ..cuda.processing import CudaProcessing
from ..processing.muladd_cuda import CudaMulAdd
from .shift import VerticalShift


class CudaVerticalShift(VerticalShift):
    def __init__(self, radios_shape, shifts, **cuda_options):
        """
        Vertical Shifter, Cuda backend.
        """
        super().__init__(radios_shape, shifts)
        self.cuda_processing = CudaProcessing(**(cuda_options or {}))
        self._init_cuda_arrays()

    def _init_cuda_arrays(self):
        interp_infos_arr = np.zeros((len(self.interp_infos), 2), "f")
        self._d_interp_infos = self.cuda_processing.to_device("_d_interp_infos", interp_infos_arr)
        self._d_radio_new = self.cuda_processing.allocate_array("_d_radio_new", self.radios_shape[1:], "f")
        self._d_radio = self.cuda_processing.allocate_array("_d_radio", self.radios_shape[1:], "f")
        self.muladd_kernel = CudaMulAdd()  # ctx=self.cuda_processing.ctx)

    def apply_vertical_shifts(self, radios, iangles, output=None):
        """
        Parameters
        ----------
        radios: 3D cupy array
            The input radios. If the optional parameter is not given, they are modified in-place
        iangles:  a sequence of integers
            Must have the same length as radios.
            It contains the index at which the shift is found in `self.shifts`
            given by `shifts` argument in the initialisation of the object.
        output: 3D cupy array, optional
            If given, it will be modified to contain the shifted radios.
            Must be of the same shape of `radios`.
        """
        self._check(radios, iangles)
        n_a, n_z, n_x = radios.shape
        assert n_z == self.radios_shape[1]
        x_slice = slice(0, n_x)  # slice(None, None)

        def nonempty_subregion(region):
            if region is None:
                return True
            z_slice = region[0]
            return z_slice.stop - z_slice.start > 0

        d_radio_new = self._d_radio_new
        d_radio = self._d_radio

        for ia in iangles:
            d_radio_new.fill(0)
            d_radio[:] = radios[ia, :, :]  # mul-add kernel won't work with pycuda view # TODO try with cupy ?
            S0, f = self.interp_infos[ia]
            f = np.float32(f)

            s0 = S0
            if s0 > 0:
                # newradio[:-s0] = radio[s0:] * (1 - f)
                dst_region = (slice(0, n_z - s0), x_slice)
                other_region = (slice(s0, n_z), x_slice)
            elif s0 == 0:
                # newradio[:] = radio[s0:] * (1 - f)
                dst_region = None
                other_region = (slice(s0, n_z), x_slice)
            else:
                # newradio[-s0:] = radio[:s0] * (1 - f)
                dst_region = (slice(-s0, n_z), x_slice)
                other_region = (slice(0, n_z + s0), x_slice)

            if all([nonempty_subregion(reg) for reg in [dst_region, other_region]]):
                self.muladd_kernel(
                    d_radio_new,
                    d_radio,
                    1,
                    1 - f,
                    dst_region=dst_region,
                    other_region=other_region,
                )

            s0 = S0 + 1
            if s0 > 0:
                # newradio[:-s0] += radio[s0:] * f
                dst_region = (slice(0, n_z - s0), x_slice)
                other_region = (slice(s0, n_z), x_slice)
            elif s0 == 0:
                # newradio[:] += radio[s0:] * f
                dst_region = None
                other_region = (slice(s0, n_z), x_slice)
            else:
                # newradio[-s0:] += radio[:s0] * f
                dst_region = (slice(-s0, n_z), x_slice)
                other_region = (slice(0, n_z + s0), x_slice)

            if all([nonempty_subregion(reg) for reg in [dst_region, other_region]]):
                self.muladd_kernel(d_radio_new, d_radio, 1, f, dst_region=dst_region, other_region=other_region)

            if output is None:
                radios[ia, :, :] = d_radio_new[:, :]
            else:
                output[ia, :, :] = d_radio_new[:, :]
