from .double_flatfield import (
    DoubleFlatField,
    check_shape,
    get_2D_3D_shape,
)
from ..misc.binning import binning


class DoubleFlatFieldVariableRegion(DoubleFlatField):
    def __init__(
        self,
        shape,
        result_url=None,
        binning_x=None,
        binning_z=None,
        detector_corrector=None,
    ):
        """This class provides the division by the double flat field.
        At variance with the standard class, it store as member the
        whole field, and performs the division by the proper region
        according to the positionings of the processed radios
        which is passed by the argument array sub_regions_per_radio to
        the method apply_double_flatfield_for_sub_regions
        """

        self.radios_shape = get_2D_3D_shape(shape)
        self.n_angles = self.radios_shape[0]
        self.shape = self.radios_shape[1:]
        self._init_filedump(result_url, None, detector_corrector)

        data = self._load_dff_full_dump()

        if (binning_z, binning_x) != (1, 1):
            print(" (binning_z, binning_x) ", (binning_z, binning_x))

            self.data = binning(data)

        else:
            self.data = data

    def _load_dff_full_dump(self):
        res = self.reader.get_data(self.result_url)
        if self.detector_corrector is not None:
            self.detector_corrector.set_full_transformation()
            res = self.detector_corrector.transform(res, do_full=True)

        return res

    def apply_double_flatfield_for_sub_regions(self, radios, sub_regions_per_radio):
        """
        Apply the "double flatfield" filter on a chunk of radios.
        The processing is done in-place !
        """
        my_double_ff = self.data

        for i in range(radios.shape[0]):
            s_x, e_x, s_y, e_y = sub_regions_per_radio[i]

            dff = my_double_ff[s_y:e_y, s_x:e_x]

            check_shape(radios[i].shape, dff.shape, "radios")

            radios[i] /= dff
        return radios
