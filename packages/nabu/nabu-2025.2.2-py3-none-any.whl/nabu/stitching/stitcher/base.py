from copy import copy
from nabu.stitching.config import SingleAxisStitchingConfiguration
from tomoscan.esrf import NXtomoScan
from tomoscan.volumebase import VolumeBase
from tomoscan.identifier import BaseIdentifier


def get_obj_constant_side_length(obj: NXtomoScan | VolumeBase, axis: int) -> int:
    """
    Return the tomography object length that will be constant over 1D stitching.
    In the case of a stitching along axis 0 this will be:
        * the projection width for pre-processing
        * volume.shape[2] for post-processing

    In the case of a stitching along axis 1 this will be:
        * the projection height for pre-processing
    """
    if isinstance(obj, NXtomoScan):
        if axis == 0:
            return obj.dim_1
        elif axis in (1, 2):
            return obj.dim_2
        else:
            raise ValueError(f"Axis ({axis}) not handled. Should be in (0, 1, 2)")
    elif isinstance(obj, VolumeBase) and axis == 0:
        return obj.get_volume_shape()[-1]
    else:
        raise TypeError(f"obj type ({type(obj)}) and axis == {axis} is not handled")


class _StitcherBase:
    """
    Any stitcher base class
    """

    def __init__(self, configuration, progress=None) -> None:
        if not isinstance(configuration, SingleAxisStitchingConfiguration):
            raise TypeError

        # flag to check if the serie has been ordered yet or not
        self._configuration = copy(configuration)
        # copy configuration because we will edit it
        self._frame_composition = None
        self._progress = progress
        self._overlap_kernels = []
        # kernels to create the stitching on overlaps.

    @property
    def serie_label(self) -> str:
        """return serie name for logs"""
        raise NotImplementedError("Base class")

    @property
    def reading_orders(self):
        """
        as scan can be take on one direction or the order (rotation goes from X to Y then from Y to X)
        we might need to read data from one direction or another
        """
        return self._reading_orders

    def order_input_tomo_objects(self):
        """
        order inputs tomo objects
        """
        raise NotImplementedError("Base class")

    def check_inputs(self):
        """
        order inputs tomo objects
        """
        raise NotImplementedError("Base class")

    def pre_processing_computation(self):
        """
        some specific pre-processing that can be call before retrieving the data
        """
        pass

    @staticmethod
    def param_is_auto(param):
        return param in ("auto", ("auto",))

    def stitch(self, store_composition: bool = True) -> BaseIdentifier:
        """
        Apply expected stitch from configuration and return the DataUrl of the object created

        :param bool store_composition: if True then store the composition used for stitching in frame_composition.
                                       So it can be reused by third part (like tomwer) to display composition made
        """
        raise NotImplementedError("base class")

    @property
    def frame_composition(self):
        return self._frame_composition

    @staticmethod
    def from_abs_pos_to_rel_pos(abs_position: tuple):
        """
        return relative position from on object to the other but in relative this time
        :param tuple abs_position: tuple containing the absolute positions
        :return: len(abs_position) - 1 relative position
        :rtype: tuple
        """
        return tuple([pos_obj_b - pos_obj_a for (pos_obj_a, pos_obj_b) in zip(abs_position[:-1], abs_position[1:])])

    @staticmethod
    def from_rel_pos_to_abs_pos(rel_positions: tuple, init_pos: int):
        """
        return absolute positions from a tuple of relative position and an initial position
        :param tuple rel_positions: tuple containing the absolute positions
        :return: len(rel_positions) + 1 relative position
        :rtype: tuple
        """
        abs_pos = [
            init_pos,
        ]
        for rel_pos in rel_positions:
            abs_pos.append(abs_pos[-1] + rel_pos)
        return abs_pos

    def _compute_shifts(self):
        """
        after this stage the final shifts must be determine
        """
        raise NotImplementedError("base class")
