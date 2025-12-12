import numpy as np


def is_fullturn_scan(angles_rad, tol=None):
    """
    Return True if the angles correspond to a full-turn (360 degrees) scan.
    """
    angles_rad = np.sort(angles_rad)
    if tol is None:
        tol = np.min(np.abs(np.diff(angles_rad))) * 1.1
    return np.abs((angles_rad.max() - angles_rad.min()) - (2 * np.pi)) < tol
