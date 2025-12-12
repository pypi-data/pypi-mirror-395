import numpy as np
from .flatfield import FlatFieldArrays, load_images_from_dataurl_dict


class FlatFieldArraysVariableRegion(FlatFieldArrays):
    _full_shape = True

    def _check_frame_shape(self, frames, frames_type):
        # in helical the flat is the whole one and its shape does not necesseraly match the smaller frames.
        # Therefore no check is done to allow this.
        pass

    def _check_radios_and_indices_congruence(self, radios_indices):
        """At variance with parent class, preprocesing is done with on a fraction of the radios,
        whose length may vary. So we don't enforce here that the length is always the same
        """
        pass

    def _normalize_radios(self, radios, sub_indexes, sub_regions_per_radio):
        """
        Apply a flat-field normalization, with the current parameters, to a stack
        of radios.
        The processing is done in-place, meaning that the radios content is overwritten.
        """
        if len(sub_regions_per_radio) != len(sub_indexes):
            message = f""" The length of sub_regions_per_radio,which is {len(sub_regions_per_radio)} , 
            does not correspond to the length of sub_indexes which is {len(sub_indexes)}
            """
            raise ValueError(message)
        # do_flats_distortion_correction = self.distortion_correction is not None

        # whole_dark = self.get_dark()
        for i, (idx, sub_r) in enumerate(zip(sub_indexes, sub_regions_per_radio)):
            start_x, end_x, start_y, end_y = sub_r
            slice_x = slice(start_x, end_x)
            slice_y = slice(start_y, end_y)

            self.normalize_single_radio(radios[i], idx, dtype=np.float32, slice_y=slice_y, slice_x=slice_x)

        return radios


class FlatFieldDataVariableRegionUrls(FlatFieldArraysVariableRegion):
    def __init__(
        self,
        radios_shape: tuple,
        flats: dict,
        darks: dict,
        radios_indices=None,
        interpolation: str = "linear",
        distortion_correction=None,
        nan_value=1.0,
        radios_srcurrent=None,
        flats_srcurrent=None,
        **chunk_reader_kwargs,
    ):
        flats_arrays_dict = load_images_from_dataurl_dict(flats, **chunk_reader_kwargs)
        darks_arrays_dict = load_images_from_dataurl_dict(darks, **chunk_reader_kwargs)

        _flats_indexes = list(flats_arrays_dict.keys())
        _flats_indexes.sort()

        self.flats_indexes = np.array(_flats_indexes)
        self.flats_stack = np.array([flats_arrays_dict[i] for i in self.flats_indexes], "f")

        flats_arrays_dict = dict([[indx, flat] for indx, flat in zip(self.flats_indexes, self.flats_stack)])

        super().__init__(
            radios_shape,
            flats_arrays_dict,
            darks_arrays_dict,
            radios_indices=radios_indices,
            interpolation=interpolation,
            distortion_correction=distortion_correction,
            nan_value=nan_value,
            radios_srcurrent=radios_srcurrent,
            flats_srcurrent=flats_srcurrent,
        )
        self._sorted_flat_indices = np.array(self._sorted_flat_indices, "i")
