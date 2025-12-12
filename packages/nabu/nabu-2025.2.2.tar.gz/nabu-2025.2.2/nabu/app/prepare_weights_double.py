import h5py
import numpy as np
from scipy.special import erf  # pylint: disable=all
import sys
import os
from scipy.ndimage import gaussian_filter
from nabu.resources.nxflatfield import update_dataset_info_flats_darks
from nabu.resources.dataset_analyzer import HDF5DatasetAnalyzer
from ..io.reader import load_images_from_dataurl_dict


def main(argv=None):
    """auxiliary program that can be called to create  default input detector profiles, for nabu helical,
    concerning the weights of the pixels and the "double flat" renormalisation denominator.
    The result is an hdf5 file that can be used as a "processes_file" in the nabu configuration and is used by nabu-helical.
    In particulars cases the user may have fancy masks and correction map and will provide its own processes file,
    and will not need this.

    This code, and in particular the auxiliary function below (that by the way tomwer can use)
    provide a default construction of such maps. The double-flat is set to one and
    the weight is build on the basis of the flat fields   from the dataset with an apodisation on the borders
    which allows to eliminate discontinuities in the contributions from the borders, above and below
    for the z-translations, and on the left or right border for half-tomo.

    The usage is ::

       nabu-helical-prepare-weights-double nexus_file_name entry_name

    Then the resulting file can be used as processes file in the configuration file of nabu-helical

    """
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) not in [2, 3, 4, 5, 6]:
        message = f""" Usage:
            nabu-helical-prepare-weights-double nexus_file_name entry_name [target_file name [transition_width_vertical [rotation_axis_position [transition_width_vertical]]]]
        """
        print(message)
        sys.exit(1)

    file_name = argv[0]
    if len(os.path.dirname(file_name)) == 0:
        # To make sure that other utility routines can succesfully deal with path within the current directory
        file_name = os.path.join(".", file_name)

    # still tere was some problem with relative path and how they are dealt with in nxtomomill
    # Better to use absolute path
    file_name = os.path.abspath(file_name)

    entry_name = argv[1]
    process_file_name = "double.h5"

    dataset_info = HDF5DatasetAnalyzer(file_name, extra_options={"h5_entry": entry_name})
    update_dataset_info_flats_darks(dataset_info, flatfield_mode=1)

    beam_profile = 0
    my_flats = load_images_from_dataurl_dict(dataset_info.flats)

    for flat in my_flats.values():
        beam_profile += flat
    beam_profile = beam_profile / len(list(dataset_info.flats.keys()))

    transition_width_vertical = 50.0

    # the following two line determines the horisontal transition
    # by default a transition on the right ( corresponds to an axis close to the right border)

    rotation_axis_position = beam_profile.shape[1] - 200
    transition_width_horizontal = 100.0

    if len(argv) in [3, 4, 5, 6]:
        process_file_name = argv[2]
        if len(argv) in [4, 5, 6]:
            transition_width_vertical = float(argv[3])
            if len(argv) in [5, 6]:
                rotation_axis_position = (beam_profile.shape[1] - 1) / 2 + float(argv[4])
                if len(argv) in [6]:
                    transition_width_horizontal = 2 * (float(argv[5]))

    create_heli_maps(
        beam_profile,
        process_file_name,
        entry_name,
        transition_width_vertical,
        rotation_axis_position,
        transition_width_horizontal,
    )

    # here we have been called by the cli. The return value 0 means OK
    return 0


def create_heli_maps(
    profile,
    process_file_name,
    entry_name,
    transition_width_vertical,
    rotation_axis_position,
    transition_width_horizontal,
):
    profile = profile / profile.max()
    profile = profile.astype("f")

    profile = gaussian_filter(profile, 10)

    def compute_border_v(L, m, w):
        x = np.arange(L)

        d = (x - L + m).astype("f")
        res_r = (1 - erf(d / w)) / 2

        d = (x - m).astype("f")
        res_l = (1 + erf(d / w)) / 2

        return res_r * res_l

    def compute_border_h(L, r, tw):
        if r > (L - 1) / 2:
            if tw > (L - r):
                tw = max(1.0, L - r)

            m = tw / 2
            w = tw / 5

            x = np.arange(L)

            d = (x - L + m).astype("f")
            res_r = (1 - erf(d / w)) / 2

            return res_r

        else:
            if tw > r:
                tw = max(1.0, r)

            m = tw / 2
            w = tw / 5

            x = np.arange(L)

            d = (x - m).astype("f")
            res_l = (1 + erf(d / w)) / 2

            return res_l

    with h5py.File(process_file_name, mode="a") as fd:
        path_weights = entry_name + "/weights_field/results/data"
        path_double = entry_name + "/double_flatfield/results/data"

        if path_weights in fd:
            del fd[path_weights]
        if path_double in fd:
            del fd[path_double]

        border = compute_border_h(profile.shape[1], rotation_axis_position, transition_width_horizontal)

        border_v = compute_border_v(
            profile.shape[0], round(transition_width_vertical / 2), transition_width_vertical / 5
        )

        fd[path_weights] = (profile * border) * border_v[:, None]
        fd[path_double] = np.ones_like(profile)
