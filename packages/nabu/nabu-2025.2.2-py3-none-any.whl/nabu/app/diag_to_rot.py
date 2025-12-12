import os
import sys
from multiprocessing import Pool
import numpy as np
from scipy.ndimage import gaussian_filter
import h5py
from silx.io.dictdump import h5todict
from nxtomo.application.nxtomo import NXtomo
from .. import version
from ..utils import get_available_threads, DictToObj
from ..pipeline.estimators import oversample
from .utils import parse_params_values
from .cli_configs import DiagToRotConfig


"""
  The operations here below rely on diag objects which are found in the result of a nab-helical run with the diag_zpro_run set to a number > 0
  They are found in the configuration section of the nabu output, in several sequential dataset, with hdf5 dataset keys 
  which are 0,1,2.... corresponding to all the z-windows ( chunck) for which we have collected contributions at different angles
  which are nothing else but pieces of ready to use preprocessed radio , and this for different angles.
  In other words redundant contributions conccurring at the same prepocessed radiography but comming from different moment 
  of the helical scan are kept separate.
  By forming pairs theta, theta +180
  These Pairs should coincide on an overlapping region after flipping one, 
  where they both have signal ( part of them can be dark if the detector is out of view above or below)
  For each key there is a sequence of radio, the corresponding sequence of weights map, the corresponding z translation, and angles

  The number passed to diag_zpro_run object, is >1, and is interpreted by the diagnostic collection run 
  as the number of wished collected angles between 0 and 180. Lets call it num_0_180

  The collection is not done here. Here we exploit the result of a previous collection to deduce, looking at the correlations, the cor

  An example of collection is this :

   |_____ diagnostics
   |               |  
                  |__ 0
                  |    |_ radios       (4*num_0_180, chunky, chunkx) 
                  |    |
                  |    |_ weights      (4*num_0_180, chunky, chunkx) 
                  |    |
                  |    |_ angles       ( 4*num_0_180,)
                       |
                       |_ searched_rad ( 2*num_0_180,)    these are all the searched angles between 0 and 360 in radians
                       |
                       |_ zmm_trans    (  4*num_0_180,)    the z translation in mm
                       |
                       |_ zpix_transl  (  4*num_0_180,)    the z translation in pix
                       |
                       |_ pixes_size_mm  scalar


   Here we follow the evolution of the rotation angle along the scan.
   The final result can be left in its detailed form, giving the found cor at every analysed scan position,
   or the result of the interpolation, giving the cor at the two extremal position of z_translation.

"""


def transform_images(diag, args):
    """
    Filter and transform the radios and the weights.

    Filter the radios, and oversample them along the horizontal line.
    The method in general is similar to the composite cor finding.
    Several overlapping positions are used to match redundant contributions at
    different rotation stages ( theta and theta+180).
    But beforehand it is beneficial to remove low spatial frequencies.
    And we do oversampling on the fly.

    Parameters
    ----------
       diag: object
         used member of diag are radios and weights
       args: object
         its member are the application parameters. Here we use only:
            low_pass, high_pass, ovs ( oversampling factor for the horizontal dimension )




    """

    diag.radios[:] = (diag.radios / diag.weights).astype("f")

    new_radios = []

    for ima in diag.radios:
        ima = gaussian_filter(ima, [0, args.low_pass], mode="nearest")
        ima = ima - gaussian_filter(ima, [0, args.high_pass], mode="nearest")
        new_radios.append(ima)

    diag.radios = [oversample(ima, [1, args.ovs]).astype("f") for ima in new_radios]

    diag.weights = [oversample(ima, [1, args.ovs]).astype("f") for ima in diag.weights]


def total_merit_list(arg_tuple):
    """
    builds three lists : all_merits, all_energies, all_z_transl

    For every pair (theta, theta+180 ) add an item to the list which contains:
    for "all_merits" a list of merit, one for every overlap in the overlap_list argument,
    for "all_energies", same logic, but calculating the implied energy, implied in the calculation of the merit,
    for "all_z_transl" we add the averaged z_transl for the considered pair
    Parameters:
       diag: object
         used member of diag are radios, weights and zpix_transl
       args: object
          containing the application parameters.
          Its used members are ovs, high_pass, low_pass
    """

    (diag, overlap_list, args) = arg_tuple

    orig_sy, ovsd_sx = diag.radios[0].shape

    all_merits = []
    all_energies = []
    all_z_transls = []

    # the following two lines are in accordance with the nabu collection layout for diagos
    # there are n_angles_pi in [0,180[, and then again the same number of possibly valid radios
    # (check for nan in z translation) in [180,360[, [360,540[, 540,720[
    n_angles_pi = len(diag.radios) // 4
    n_angles_2pi = len(diag.radios) // 2

    # check for (theta, theta+180 )pairs whose first radio of the pair in in [0,180[ or  [360,540[
    for i in list(range(n_angles_pi)) + list(range(n_angles_2pi, n_angles_2pi + n_angles_pi)):
        merits = []
        energies = []
        z_transl = []

        if (not np.isnan(diag.zpix_transl[i])) and (not np.isnan(diag.zpix_transl[i + n_angles_pi])):
            radio1 = diag.radios[i]
            radio2 = diag.radios[i + n_angles_pi]

            weight1 = diag.weights[i]
            weight2 = diag.weights[i + n_angles_pi]

            for overlap in overlap_list:
                if overlap <= ovsd_sx:
                    my_overlap = overlap
                    my_radio1 = radio1
                    my_radio2 = radio2
                    my_weight1 = weight1
                    my_weight2 = weight2
                else:
                    my_overlap = ovsd_sx - (overlap - ovsd_sx)
                    my_radio1 = np.fliplr(radio1)
                    my_radio2 = np.fliplr(radio2)
                    my_weight1 = np.fliplr(weight1)
                    my_weight2 = np.fliplr(weight2)

                radio_common_left = np.fliplr(my_radio1[:, ovsd_sx - my_overlap :])[
                    :, : -(args.ovs * args.high_pass * 2)
                ]
                radio_common_right = my_radio2[:, ovsd_sx - my_overlap : -(args.ovs * args.high_pass * 2)]
                diff_common = radio_common_right - radio_common_left

                weight_common_left = np.fliplr(my_weight1[:, ovsd_sx - my_overlap :])[
                    :, : -(args.ovs * args.high_pass * 2)
                ]
                weight_common_right = my_weight2[:, ovsd_sx - my_overlap : -(args.ovs * args.high_pass * 2)]
                weight_common = weight_common_right * weight_common_left

                if args.use_l1_norm:
                    merits.append(abs(diff_common * weight_common).astype("d").sum())
                    energies.append(abs(weight_common).astype("d").sum())
                else:
                    merits.append((diff_common * diff_common * weight_common).astype("d").sum())
                    energies.append(
                        (
                            (radio_common_left * radio_common_left + radio_common_right * radio_common_right)
                            * weight_common
                        )
                        .astype("d")
                        .sum()
                    )
        else:
            merits = [0] * (len(overlap_list))
            energies = [0] * (len(overlap_list))

        z_transl = 0.5 * (diag.zpix_transl[i] + diag.zpix_transl[i + n_angles_pi])
        all_z_transls.append(z_transl)

        all_merits.append(merits)
        all_energies.append(energies)

    return all_merits, all_energies, all_z_transls


def find_best_interpolating_line(args):
    (all_z_transl, index_overlap_list_a, index_overlap_list_b, all_energies, all_res) = args

    z_a = np.nanmin(all_z_transl)
    z_b = np.nanmax(all_z_transl)

    best_error = np.nan

    for index_ovlp_a in index_overlap_list_a:
        for index_ovlp_b in index_overlap_list_b:
            index_ovlps = np.interp(all_z_transl, [z_a, z_b], [index_ovlp_a, index_ovlp_b])
            indexes = (np.arange(all_energies.shape[0]))[~np.isnan(index_ovlps)].astype("i")

            index_ovlps = index_ovlps[~np.isnan(index_ovlps)]
            index_ovlps = np.round(index_ovlps).astype("i")

            diff_enes = all_res[(indexes, index_ovlps)]
            orig_enes = all_energies[(indexes, index_ovlps)]

            error = (diff_enes / (orig_enes + 1.0e-30)).astype("d").sum()

            if not (error > best_error):
                best_error = error
                best_error_pair = index_ovlp_a, index_ovlp_b

    return best_error, best_error_pair  # pylint: disable=E0606


def main(user_args=None):
    """Find the cor as a function f z translation and write an hdf5 which contains interpolable tables.
    This file can be used subsequently with the correct-rot utility.
    """

    if user_args is None:
        user_args = sys.argv[1:]

    args = DictToObj(
        parse_params_values(
            DiagToRotConfig,
            parser_description=main.__doc__,
            program_version="nabu " + version,
            user_args=user_args,
        )
    )

    if args.near is None:
        if args.original_scan is None:
            raise ValueError(
                "the parameter near was not provided but the original_scan parameter was not provided either"
            )
        if args.entry_name is None:
            raise ValueError(
                "the parameter near was not provided but the entry_name parameter  for the original scan was not provided either"
            )

        scan = NXtomo()
        scan.load(file_path=args.original_scan, data_path=args.entry_name)
        args.near = scan.instrument.detector.x_rotation_axis_pixel_position
    else:
        pass

    args.ovs = 4

    diag_url = os.path.join("/", args.entry_name, "reconstruction/configuration/diagnostics")

    diag_keys = []
    with h5py.File(args.diag_file, "r") as f:
        diag_keys = list(f[diag_url].keys())
        diag_keys = [diag_keys[i] for i in np.argsort(list(map(int, diag_keys)))]

    all_merits = []
    all_energies = []
    all_z_transls = []

    arguments_for_multiprocessing = []

    for i_key, my_key in enumerate(diag_keys):
        diag = DictToObj(h5todict(args.diag_file, os.path.join(diag_url, my_key)))

        args.original_shape = diag.radios[0].shape
        args.zpix_mm = diag.pixel_size_mm

        transform_images(diag, args)

        if i_key == 0:
            orig_sy, ovsd_sx = diag.radios[0].shape  # already transformed here, ovsd_sx is expanded
            args.ovsd_sx = ovsd_sx

            overlap_min = max(4, ovsd_sx - 2 * args.ovs * (args.near + args.near_width))
            overlap_max = min(2 * ovsd_sx - 4, ovsd_sx - 2 * args.ovs * (args.near - args.near_width))

            overlap_list = list(range(int(overlap_min), int(overlap_max) + 1))

            if overlap_min > overlap_max:
                message = f""" There is no safe search range in find_cor once the margins corresponding to the high_pass filter are discarded.
                May be the near value (which is the offset respect to the center of the image) is too big, or too negative,
                in short too close to the borders.
                """
                raise ValueError(message)

        arguments_for_multiprocessing.append((diag, overlap_list, args))  # pylint: disable=E0606

    ncpus = get_available_threads()
    with Pool(processes=ncpus) as pool:
        result_list = pool.map(total_merit_list, arguments_for_multiprocessing)

    for merits, energies, z_transls in result_list:
        all_z_transls.extend(z_transls)
        all_merits.extend(merits)
        all_energies.append(energies)

    n_pairings_with_data = 0
    for en, me in zip(all_merits, all_energies):
        if np.any(me):
            n_pairings_with_data += 1

    if args.linear_interpolation:
        if n_pairings_with_data < 2:
            message = f""" The diagnostics collection has probably been run over a too thin section of the scan
            or you scan does not allow to form pairs of theta, theta+360. I only found {n_pairings_with_data} pairings
            and this is not enough to do correlation + interpolation between sections
            """
            raise RuntimeError(message)
    elif n_pairings_with_data < 1:
        message = f""" The diagnostics collection has probably been run over a too thin section of the scan
            or you scan does not allow to form pairs of theta, theta+360. I only found {n_pairings_with_data}
            pairings
            """
        raise RuntimeError(message)

    # all_merits, all_energies, all_z_transls = zip( result_list )

    # merits, energies, z_transls = total_merit_list(diag, overlap_list, args)

    #     all_z_transls.extend(z_transls)
    #     all_merits.extend(merits)
    #     all_energies.append(energies)

    all_merits = np.array(all_merits)
    all_energies = np.array(all_energies)

    all_merits.shape = -1, len(overlap_list)
    all_energies.shape = -1, len(overlap_list)

    if args.linear_interpolation:
        do_linear_interpolation(args, overlap_list, all_merits, all_energies, all_z_transls)
    else:
        do_height_by_height(args, overlap_list, all_merits, all_energies, all_z_transls)

    return 0


def do_height_by_height(args, overlap_list, all_diff, all_energies, all_z_transl):
    # now we find the best cor for each chunk, or nan if no overlap is found
    # z_a = np.min(all_z_transl)
    # z_b = np.max(all_z_transl)

    grouped_diff = {}
    grouped_energy = {}

    for diff, energy, z in zip(all_diff, all_energies, all_z_transl):
        found = z
        for key in grouped_diff:
            if abs(key - z) < 2.0:  # these are in pixel units
                found = key
                break
        grouped_diff[found] = grouped_diff.get(found, np.zeros([len(overlap_list)], "f")) + diff
        grouped_energy[found] = grouped_energy.get(found, np.zeros([len(overlap_list)], "f")) + energy

    z_list = list(grouped_energy.keys())
    z_list.sort()

    cor_list = []
    for z in z_list:
        diff = grouped_diff[z]
        energy = grouped_energy[z]

        best_error = np.nan
        best_off = None

        if not np.isnan(z):
            for i_ovlp in range(len(overlap_list)):
                error = diff[i_ovlp] / (energy[i_ovlp] + 1.0e-30)

                if not (error > best_error):
                    best_error = error
                    best_off = i_ovlp

            if best_off is not None:
                offset = (args.ovsd_sx - overlap_list[best_off]) / args.ovs / 2
                sy, sx = args.original_shape
                cor_abs = (sx - 1) / 2 + offset
                cor_list.append(cor_abs)
            else:
                cor_list.append(np.nan)
        else:
            # no overlap  was available for that z
            cor_list.append(np.nan)

    with h5py.File(args.cor_file, "w") as f:
        my_mask = ~np.isnan(np.array(cor_list))
        f["cor"] = np.array(cor_list)[my_mask]
        f["z_pix"] = np.array(z_list)[my_mask]
        f["z_m"] = (np.array(z_list)[my_mask]) * args.zpix_mm * 1.0e-3


def do_linear_interpolation(args, overlap_list, all_res, all_energies, all_z_transl):
    # now we consider all the linear regressions of the offset with z_transl

    ncpus = get_available_threads()

    index_overlap_list = np.arange(len(overlap_list)).astype("i")
    arguments_list = [
        (all_z_transl, piece, index_overlap_list, all_energies, all_res)
        for piece in np.array_split(index_overlap_list, ncpus)
    ]

    with Pool(processes=ncpus) as pool:
        result_list = pool.map(find_best_interpolating_line, arguments_list)

    error_list = [tok[0] for tok in result_list]
    best_pos = np.argmin(error_list)
    best_error, best_error_pair = result_list[best_pos]

    # find the interpolated line
    i_ovlp_a, i_ovlp_b = best_error_pair
    offset_a = (args.ovsd_sx - overlap_list[i_ovlp_a]) / args.ovs / 2
    offset_b = (args.ovsd_sx - overlap_list[i_ovlp_b]) / args.ovs / 2

    sy, sx = args.original_shape

    cor_abs_a = (sx - 1) / 2 + offset_a
    cor_abs_b = (sx - 1) / 2 + offset_b

    z_a = np.nanmin(all_z_transl)
    z_b = np.nanmax(all_z_transl)

    with h5py.File(args.cor_file, "w") as f:
        f["cor"] = np.array([cor_abs_a, cor_abs_b])
        f["z_pix"] = np.array([z_a, z_b])
        f["z_m"] = np.array([z_a, z_b]) * args.zpix_mm * 1.0e-3
