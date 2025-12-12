from ..fullfield.dataset_validator import FullFieldDatasetValidator
from ...utils import copy_dict_items


class HelicalDatasetValidator(FullFieldDatasetValidator):
    """Allows more freedom in the choice of the slice indices"""

    # this in the fullfield base  class is instead True
    _check_also_z = False

    def _check_slice_indices(self):
        """Slice indices can be far beyond what fullfield pipeline accepts, no check here, but
        Nabu expects that rec_region is initialised here
        """

        what = ["start_x", "end_x", "start_y", "end_y", "start_z", "end_z"]

        self.rec_region = copy_dict_items(self.rec_params, what)
