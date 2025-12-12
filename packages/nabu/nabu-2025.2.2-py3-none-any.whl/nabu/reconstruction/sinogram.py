import numpy as np
from scipy.interpolate import interp1d
from ..utils import get_2D_3D_shape, check_supported, deprecated_class, deprecated


class SinoBuilder:
    """
    A class to build sinograms.
    """

    def __init__(
        self, sinos_shape=None, radios_shape=None, rot_center=None, halftomo=False, angles=None, interpolate=False
    ):
        """
        Initialize a SinoBuilder instance.

        Parameters
        ----------
        sinos_shape: tuple of int
            Shape of the stack of sinograms, in the form `(n_z, n_angles, n_x)`.
            If not provided, it is derived from `radios_shape`.
        radios_shape: tuple of int
            Shape of the chunk of radios, in the form `(n_angles, n_z, n_x)`.
            If not provided, it is derived from `sinos_shape`.
        rot_center: int or array
            Rotation axis position. A scalar indicates the same rotation axis position
            for all the projections.
        halftomo: bool
            Whether "half tomography" is enabled. Default is False.
        interpolate: bool, optional
            Only used if halftomo=True.
            Whether to re-grid the second part of sinograms to match projection k with projection k + n_a/2.
            This forces each pair of projection (k, k + n_a/2) to be separated by exactly 180 degrees.
        angles: array, optional
            Rotation angles (in radians). Used and required only when halftomo and interpolate are True.
        """
        self._get_shapes(sinos_shape, radios_shape)
        self.set_rot_center(rot_center)
        self._configure_halftomo(halftomo, interpolate, angles)

    def _get_shapes(self, sinos_shape, radios_shape=None):
        if (sinos_shape is None) and (radios_shape is None):
            raise ValueError("Need to provide sinos_shape and/or radios_shape")
        if sinos_shape is None:
            n_a, n_z, n_x = get_2D_3D_shape(radios_shape)
            sinos_shape = (n_z, n_a, n_x)
        elif len(sinos_shape) == 2:
            sinos_shape = (1,) + sinos_shape
        if radios_shape is None:
            n_z, n_a, n_x = get_2D_3D_shape(sinos_shape)
            radios_shape = (n_a, n_z, n_x)
        elif len(radios_shape) == 2:
            radios_shape = (1,) + radios_shape

        self.sinos_shape = sinos_shape
        self.radios_shape = radios_shape
        n_a, n_z, n_x = radios_shape
        self.n_angles = n_a
        self.n_z = n_z
        self.n_x = n_x

    def set_rot_center(self, rot_center):
        """
        Set the rotation axis position for the current radios/sinos stack.

        rot_center: int or array
            Rotation axis position. A scalar indicates the same rotation axis position
            for all the projections.
        """
        if rot_center is None:
            rot_center = (self.n_x - 1) / 2.0
        if not (np.isscalar(rot_center)):
            rot_center = np.array(rot_center)
            if rot_center.size != self.n_angles:
                raise ValueError(
                    "Expected rot_center to have %d elements but got %d" % (self.n_angles, rot_center.size)
                )
        self.rot_center = rot_center

    def _configure_halftomo(self, halftomo, interpolate, angles):
        self.halftomo = halftomo
        self.interpolate = interpolate
        self.angles = angles
        self._halftomo_flip = False
        if not self.halftomo:
            return
        if interpolate and (angles is None):
            raise ValueError("The parameter 'angles' has to be provided when using halftomo=True and interpolate=True")
        self.extended_sino_width = get_extended_sinogram_width(self.n_x, self.rot_center)
        # If CoR is on the left: "flip" the logic
        if self.rot_center < (self.n_x - 1) / 2:
            self.rot_center = self.n_x - 1 - self.rot_center
            self._halftomo_flip = True
        #

        if abs(self.rot_center - ((self.n_x - 1) / 2.0)) < 1:  # which tol ?
            raise ValueError("Half tomography: incompatible rotation axis position: %.2f" % self.rot_center)
        self.sinos_halftomo_shape = (self.n_z, (self.n_angles + 1) // 2, self.extended_sino_width)

    def _check_array_shape(self, array, kind="radio"):
        expected_shape = self.radios_shape if "radio" in kind else self.sinos_shape
        assert array.shape == expected_shape, "Expected radios shape %s, but got %s" % (expected_shape, array.shape)

    @property
    def output_shape(self):
        """
        Get the output sinograms shape.
        """
        if self.halftomo:
            return self.sinos_halftomo_shape
        return self.sinos_shape

    #
    # 2D
    #

    def _get_sino_simple(self, radios, i):
        return radios[:, i, :]  # view

    def _get_sino_halftomo(self, sino, output=None):
        # TODO output is ignored for now
        if self.interpolate:
            match_half_sinos_parts(sino, self.angles)
        elif self.n_angles & 1:
            # Odd number of projections - add one line in the end
            sino = np.vstack([sino, np.zeros_like(sino[-1])])
        if self._halftomo_flip:
            sino = sino[:, ::-1]

        if self.rot_center > self.n_x:
            # (hopefully rare) case where CoR is outside FoV
            result = _convert_halftomo_right(sino, self.extended_sino_width)
        else:
            # Standard case
            result = convert_halftomo(sino, self.extended_sino_width)

        if self._halftomo_flip:
            result = result[:, ::-1]
        return result

    def get_sino(self, radios, i, output=None):
        """
        The the sinogram at a given index.

        Parameters
        ----------
        radios: array
            3D array with shape (n_z, n_angles, n_x)
        i: int
            Sinogram index

        Returns
        -------
        sino: array
            Two dimensional array with shape (n_angles2, n_x2) where the dimensions
            are determined by the current settings.
        """
        sino = self._get_sino_simple(radios, i)
        if self.halftomo:
            return self._get_sino_halftomo(sino, output=None)
        else:
            return sino

    def convert_sino(self, sino, output=None):
        if not self.halftomo:
            return sino
        return self._get_sino_halftomo(sino, output=output)

    #
    # 3D
    #

    def _get_sinos_simple(self, radios, output=None):
        res = np.rollaxis(radios, 1, 0)  # view
        if output is not None:
            output[...] = res[...]  # copy
            return output
        return res

    def _get_sinos_halftomo(self, radios, output=None):
        n_a, n_z, n_x = radios.shape
        if output is None:
            output = np.zeros(self.sinos_halftomo_shape, dtype=np.float32)
        elif output.shape != self.output_shape:
            raise ValueError("Expected output shape to be %s, but got %s" % (str(output.shape), str(self.output_shape)))
        for i in range(n_z):
            sino = self._get_sino_simple(radios, i)
            output[i] = self._get_sino_halftomo(sino)
        return output

    def get_sinos(self, radios, output=None):
        if self.halftomo:
            return self._get_sinos_halftomo(radios, output=output)
        else:
            return self._get_sinos_simple(radios, output=output)

    @deprecated("Use get_sino() or get_sinos() instead", do_print=True)
    def radios_to_sinos(self, radios, output=None, copy=False):
        """
        DEPRECATED. Use get_sinos() or get_sino() instead.
        """
        return self.get_sinos(radios, output=output)


SinoProcessing = deprecated_class("'SinoProcessing' was renamed 'SinoBuilder'", do_print=True)(SinoBuilder)


class SinoMult:
    """
    A class for preparing a sinogram for half-tomography reconstruction, without stitching the two parts
    """

    def __init__(self, sino_shape, rot_center):
        self._set_shape(sino_shape)
        self._prepare_weights(rot_center)

    def _set_shape(self, sino_shape):
        _, self.n_a, self.n_x = get_2D_3D_shape(sino_shape)

    def _prepare_weights(self, rot_center):
        n_x = self.n_x
        middle = (n_x - 1) / 2.0
        if rot_center >= middle:
            overlap_width = int(2 * (n_x - 1 - rot_center))
            self.overlap_region = slice(-overlap_width, None)
            self.pad_left, self.pad_right = 0, n_x - overlap_width
        else:
            overlap_width = int(2 * rot_center)
            self.overlap_region = slice(0, overlap_width)
            self.pad_left, self.pad_right = n_x - overlap_width, 0
        weights = np.linspace(0, 1, overlap_width, endpoint=True)
        if rot_center >= middle:
            weights = weights[::-1]
        self.weights = np.ascontiguousarray(weights, dtype="f")
        overlap_region_indices = np.arange(self.n_x)[self.overlap_region]
        self.start_x = overlap_region_indices[0]
        self.end_x = overlap_region_indices[-1]
        self.extended_width = n_x + self.pad_left + self.pad_right

    def prepare_sino(self, sino):
        sino[:, self.overlap_region] *= self.weights
        return sino


def convert_halftomo(sino, extended_width, transition_width=None):
    """
    Converts a sinogram into a sinogram with extended FOV with the "half tomography"
    setting.
    """
    assert sino.ndim == 2
    assert (sino.shape[0] % 2) == 0
    na, nx = sino.shape

    na2 = na // 2
    r = extended_width // 2
    d = transition_width or nx - r
    res = np.zeros((na2, 2 * r), dtype="f")

    sino1 = sino[:na2, :]
    sino2 = sino[na2:, ::-1]
    res[:, : r - d] = sino1[:, : r - d]
    #
    w1 = np.linspace(0, 1, 2 * d, endpoint=True)
    res[:, r - d : r + d] = (1 - w1) * sino1[:, r - d :] + w1 * sino2[:, 0 : 2 * d]
    #
    res[:, r + d :] = sino2[:, 2 * d :]

    return res


# This function can have a cuda counterpart, see test_interpolation.py
def match_half_sinos_parts(sino, angles, output=None):
    """
    Modifies the lower part of the half-acquisition sinogram so that each projection pair is
    separated by exactly 180 degrees.
    This means that `new_sino[k]` and `new_sino[k + n_angles//2]` will be 180 degrees apart.

    Parameters
    ----------
    sino: numpy.ndarray
        Two dimensional array with the sinogram in the form (n_angles, n_x)
    angles: numpy.ndarray
        One dimensional array with the rotation angles.
    output: numpy.array, optional
        Output sinogram. By default, the array 'sino' is modified in-place.

    Notes
    -----
    This function assumes that the angles are in an increasing order.
    """
    n_a = angles.size
    n_a_2 = n_a // 2
    # sino_part1 = sino[:n_a_2, :]
    sino_part2 = sino[n_a_2:, :]
    angles = np.rad2deg(angles)  # more numerically stable ?
    angles_1 = angles[:n_a_2]
    angles_2 = angles[n_a_2:]
    angles_2_target = angles_1 + 180.0
    interpolator = interp1d(angles_2, sino_part2, axis=0, kind="linear", copy=False, fill_value="extrapolate")
    if output is None:
        output = sino
    else:
        output[:n_a_2, :] = sino[:n_a_2, :]
    output[n_a_2:, :] = interpolator(angles_2_target)
    return output


# EXPERIMENTAL
def _convert_halftomo_right(sino, extended_width):
    """
    Converts a sinogram into a sinogram with extended FOV with the "half tomography"
    setting, with a CoR outside the image support.
    """
    assert sino.ndim == 2
    na, nx = sino.shape
    assert (na % 2) == 0
    rotation_axis_position = extended_width // 2
    assert rotation_axis_position > nx

    sino2 = np.pad(sino, ((0, 0), (0, rotation_axis_position - nx)), mode="reflect")
    return convert_halftomo(sino2, extended_width)


def get_extended_sinogram_width(sino_width, rotation_axis_position):
    """
    Compute the width (in pixels) of the extended sinogram for half-acquisition setting.
    """
    middle = (sino_width - 1) / 2.0
    if rotation_axis_position >= middle:
        overlap_width = int(2 * (sino_width - 1 - rotation_axis_position))
    else:
        overlap_width = int(2 * rotation_axis_position)
    return 2 * sino_width - overlap_width


def prepare_half_tomo_sinogram(sino, rot_center, get_extended_sino=True):
    if get_extended_sino:
        sino = sino.copy()
    n_angles, n_x = sino.shape
    middle = (n_x - 1) / 2.0
    if rot_center >= middle:
        overlap_width = int(2 * (n_x - 1 - rot_center))
        overlap_region = slice(-overlap_width, None)
        pad_left, pad_right = 0, n_x - overlap_width
    else:
        overlap_width = int(2 * rot_center)
        overlap_region = slice(0, overlap_width)
        pad_left, pad_right = n_x - overlap_width, 0
    weights = np.linspace(0, 1, overlap_width, endpoint=True)
    if rot_center >= middle:
        weights = weights[::-1]
    sino[:, overlap_region] *= weights
    if get_extended_sino:
        return np.pad(sino, ((0, 0), (pad_left, pad_right)), mode="constant")
    return sino


class SinoNormalization:
    """
    A class for sinogram normalization utilities.
    """

    kinds = [
        "chebyshev",
        "subtraction",
        "division",
    ]
    operations = {"subtraction": np.subtract, "division": np.divide}

    def __init__(self, kind="chebyshev", sinos_shape=None, radios_shape=None, normalization_array=None):
        """
        Initialize a SinoNormalization class.

        Parameters
        -----------
        kind: str, optional
            Normalization type. They can be the following:
               - chebyshev: Each sinogram line is estimated by a Chebyshev polynomial
               of degree 2. This estimation is then subtracted from the sinogram.
               - subtraction: Each sinogram is subtracted with a user-provided array.
                 The array can be 1D (angle-independent) and 2D (angle-dependent)
               - division: same as previously, but with a division operation.
            Default is "chebyshev"
        sinos_shape: tuple, optional
            Shape of the sinogram or sinogram stack.
            Either this parameter or 'radios_shape' has to be provided.
        radios_shape: tuple, optional
            Shape of the projections or projections stack.
            Either this parameter or 'sinos_shape' has to be provided.
        normalization_array: numpy.ndarray, optional
            Normalization array when kind='subtraction' or kind='division'.
        """
        self._get_shapes(sinos_shape, radios_shape)
        self._set_kind(kind, normalization_array)

    _get_shapes = SinoBuilder._get_shapes

    def _set_kind(self, kind, normalization_array):
        check_supported(kind, self.kinds, "sinogram normalization kind")
        self.normalization_kind = kind
        self._normalization_instance_method = self._normalize_chebyshev  # default
        if kind in ["subtraction", "division"]:
            if not isinstance(normalization_array, np.ndarray):
                raise ValueError(
                    "Expected 'normalization_array' to be provided as a numpy array for normalization kind='%s'" % kind
                )
            if normalization_array.shape[-1] != self.sinos_shape[-1]:
                n_a, n_x = self.sinos_shape[-2:]
                raise ValueError("Expected normalization_array to have shape (%d, %d) or (%d, )" % (n_a, n_x, n_x))
            self.norm_operation = self.operations[kind]
            self._normalization_instance_method = self._normalize_op
        self.normalization_array = normalization_array

    #
    # Chebyshev normalization
    #

    def _normalize_chebyshev_2D(self, sino):
        output = sino  # inplace
        Nr, Nc = sino.shape
        J = np.arange(Nc)
        x = 2.0 * (J + 0.5 - Nc / 2) / Nc
        sum0 = Nc
        f2 = 3.0 * x * x - 1.0
        sum1 = (x**2).sum()
        sum2 = (f2**2).sum()
        for i in range(Nr):
            ff0 = sino[i, :].sum()
            ff1 = (x * sino[i, :]).sum()
            ff2 = (f2 * sino[i, :]).sum()
            output[i, :] = sino[i, :] - (ff0 / sum0 + ff1 * x / sum1 + ff2 * f2 / sum2)
        return output

    def _normalize_chebyshev_3D(self, sino):
        for i in range(sino.shape[0]):
            self._normalize_chebyshev_2D(sino[i])
        return sino

    def _normalize_chebyshev(self, sino):
        if sino.ndim == 2:
            self._normalize_chebyshev_2D(sino)
        else:
            self._normalize_chebyshev_3D(sino)
        return sino

    #
    # Array subtraction/division
    #

    def _normalize_op(self, sino):
        if sino.ndim == 2:
            self.norm_operation(sino, self.normalization_array, out=sino)
        else:
            for i in range(sino.shape[0]):
                self.norm_operation(sino[i], self.normalization_array, out=sino[i])
        return sino

    #
    # Dispatch
    #

    def normalize(self, sino):
        """
        Normalize a sinogram or stack of sinogram.
        The process is done in-place, meaning that the sinogram content is overwritten.
        """
        return self._normalization_instance_method(sino)
