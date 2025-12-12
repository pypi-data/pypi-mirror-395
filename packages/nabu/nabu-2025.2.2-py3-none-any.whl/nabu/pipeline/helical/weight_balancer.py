import numpy as np
import math


class WeightBalancer:
    def __init__(self, rot_center, angles_rad):
        """This  class contains the method for rebalancing the weight  prior to
        backprojection. The weights of halfomo redundacy data ( the central part) are rebalanced.
        In a pipeline, the weights rebalanced by  the method balance_weight, have to be applied to the ramp-filtered
        data prior to backprojection.
        As a matter of fact the method balance_weights  could be called as a function, but in order to be  conformant
        to Nabu, we create this class and follow the scheme initialisation + application.

        Parameters
        ----------
        rot_center : float
                    the center of rotation in pixel units
        angles_rad :
                   the angles corresponding to the to be rebalanced projections

        """
        self.rot_center = rot_center
        self.my_angles_rad = angles_rad

    def balance_weights(self, radios_weights):
        """
        The parameter radios_weights is a stack having having the same weight as the stack of projections. It is modified in place, correcting
        the value of overlapping data, so that the sum is always one
        """
        radios_weights[:] = self._rebalance(radios_weights)

    def _rebalance(self, radios_weights):
        """rebalance the  weights,  within groups of equivalent (up to multiple of 180), data pixels"""

        balanced = np.zeros_like(radios_weights)
        n_span = int(math.ceil(self.my_angles_rad[-1] - self.my_angles_rad[0]) / np.pi)
        center = (radios_weights.shape[-1] - 1) / 2
        nloop = balanced.shape[0]

        for i in range(nloop):
            w_res = balanced[i]
            angle = self.my_angles_rad[i]

            for i_half_turn in range(-n_span - 1, n_span + 2):
                if i_half_turn == 0:
                    w_res[:] += radios_weights[i]
                    continue

                shifted_angle = angle + i_half_turn * np.pi

                insertion_index = np.searchsorted(self.my_angles_rad, shifted_angle)

                if insertion_index in [0, self.my_angles_rad.shape[0]]:
                    if insertion_index == 0:
                        if abs(self.my_angles_rad[0] - shifted_angle) > np.pi / 100:
                            continue
                        myimage = radios_weights[0]
                    else:
                        if abs(self.my_angles_rad[-1] - shifted_angle) > np.pi / 100:
                            continue
                        myimage = radios_weights[-1]
                else:
                    partition = shifted_angle - self.my_angles_rad[insertion_index - 1]
                    myimage = (1.0 - partition) * radios_weights[insertion_index - 1] + partition * radios_weights[
                        insertion_index
                    ]

                if i_half_turn % 2 == 0:
                    w_res[:] += myimage
                else:
                    myimage = np.fliplr(myimage)
                    w_res[:] += shift(myimage, (2 * self.rot_center - 2 * center))

        mask = np.equal(0, radios_weights)
        balanced[:] = radios_weights / balanced
        balanced[mask] = 0
        return balanced


def shift(arr, shift, fill_value=0.0):
    """trivial horizontal shift.
    Contrarily to scipy.ndimage.interpolation.shift, this shift does not cut the tails abruptly, but by interpolation
    """
    result = np.zeros_like(arr)

    num1 = math.floor(shift)
    num2 = num1 + 1
    partition = shift - num1

    for num, factor in zip([num1, num2], [(1 - partition), partition]):
        if num > 0:
            result[:, :num] += fill_value * factor
            result[:, num:] += arr[:, :-num] * factor
        elif num < 0:
            result[:, num:] += fill_value * factor
            result[:, :num] += arr[:, -num:] * factor
        else:
            result[:] += arr * factor

    return result
