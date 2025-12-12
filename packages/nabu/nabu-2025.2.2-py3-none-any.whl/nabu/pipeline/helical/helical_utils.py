from ...resources.logger import LoggerOrPrint
import numpy as np

logger = LoggerOrPrint(None)


def find_mirror_indexes(angles_deg, tolerance_factor=1.0):
    """return a list of indexes where the ith element
    contains the index of the angles_deg array element which has the value the closest
    to angles_deg[i] + 180. It is used for padding in halftomo.

    Parameters
    -----------
    angles_deg: a nd.array of floats

    tolerance: float
       if the mirror positions are not within a distance less than tolerance from
       the ideal position a warning is raised

    """
    av_step = abs(np.diff(angles_deg).mean())
    tolerance = av_step * tolerance_factor

    tmp_mirror_angles_deg = angles_deg + 180

    mirror_angle_relative_indexes = (abs(abs(np.mod(tmp_mirror_angles_deg[:, None] - angles_deg, 360) - 180))).argmax(
        axis=-1
    )

    mirror_values = angles_deg[mirror_angle_relative_indexes]
    differences = abs(np.mod(mirror_values - angles_deg, 360) - 180)

    if differences.max() > tolerance:
        logger.warning(
            f"""In function  find_mirror_indexes the mirror position are far beyon tolerance from ideal position
                            tolerance is {tolerance} given by average step {av_step} and tolerance_factor {tolerance_factor}
                            and the maximum error is {differences.max()}
        """
        )

    return mirror_angle_relative_indexes
