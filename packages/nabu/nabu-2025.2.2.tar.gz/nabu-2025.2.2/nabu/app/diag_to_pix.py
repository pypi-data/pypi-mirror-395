import os
from multiprocessing import Pool
import sys
import numpy as np
from scipy.ndimage import gaussian_filter
import h5py
from silx.io.dictdump import h5todict
from nxtomo.application.nxtomo import NXtomo
from .. import version
from ..utils import DictToObj, get_available_threads
from .utils import parse_params_values
from .cli_configs import DiagToPixConfig
from ..pipeline.estimators import oversample


"""
  The operations here below rely on diag objects which are found in the result of a nab-helical run with the diag_zpro_run set to a number > 0
  They are found in the configuration section of the nabu output, in several sequential dataset, with hdf5 dataset keys 
  which are 0,1,2.... corresponding to all the z-windows ( chunck) for which we have collected contributions at different angles
  which are nothing else but pieces of ready to use preprocessed radio , and this for different angles.
  In other words redundant contributions conccurring at the same prepocessed radiography but comming from different moment 
  of the helical scan are kept separate
  Forming pairs from contributions for same angle they should coincide where they both have signal ( part of them can be dark if the detector is out of view above or below)

  For each key there is a sequence of radio, the corresponding sequence of weights map, the corresponding z translation, and angles

  The number passed to diag_zpro_run object, is >1, and is interpreted by the diagnostic collection run 
  as the number of wished collecte angles between 0 and 180. Lets call it num_0_180

  The collection is not done here. Here we exploit the result of a previous collection to deduce, looking at the correlations, which correction
  we must bring to the pixel size

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

"""


def transform_images(diag, ovs):
    """Filter the radios, and oversample them along the vertical line.
    The method in general is similar to the composite cor finding.
    Several overlapping positions are used to match redundant contributions at
    different rotation stages ( theta and theta+360).
    But beforehand it is beneficial to remove low spatial frequencies.
    And we do oversampling on the fly.

    """
    assert len(ovs) == 2, "oversampling must be specified for both vertical and horizontal dimension"

    diag.radios[:] = diag.radios / diag.weights

    diag.radios = [oversample((ima - gaussian_filter(ima, 20, mode="nearest")), ovs) for ima in diag.radios]

    diag.weights = [oversample(ima, ovs) for ima in diag.weights]


def detailed_merit(diag, shift):
    # res will become the merit summed over all the pairs theta, theta+180
    # res = 0.0

    # need to account for the weight also. So this will become the used weight for the pairs theta, theta+180
    # res_w = 0.0

    ## The following two variables are very important information to be collected.
    ## On the the z translation over a 360 turn
    ## the other is the pixel size in mm.
    ## At the end of the script, the residual shift for perfect correlation
    ## will used to correct zpix_mm, doing a pro-rata with respect to
    ## the z observed translation over one turn
    observed_oneturn_total_shift_zpix_list = []
    zpix_mm = None

    n_angles_2pi = len(diag.radios) // 2
    # In accordance with the collection layout for diagnostics (diag_zpro_run parameter passed to nabu-helical)
    # there are n_angles_pi in [0,180[, and then again the same number of possibly valid radios
    # (check for nan in z translation) in [180,360[, [360,540[, 540,720[
    # So we have len(diag.radios) // 2 in the range [0,360[
    # because we have len(diag.radios)  in [0,720[

    detailed_merit_list = []  # one for each theta theta+360 pair
    detailed_weight_list = []  # one for each theta theta+360 pair

    for i in range(n_angles_2pi):
        # if we have something for both items of the pair, proceed
        if (not np.isnan(diag.zpix_transl[i])) and (not np.isnan(diag.zpix_transl[i + n_angles_2pi])):
            # because we have theta and theta + 360

            zpix_mm = diag.pixel_size_mm
            add, add_w = merit(
                diag.radios[i], diag.radios[i + n_angles_2pi], diag.weights[i], diag.weights[i + n_angles_2pi], shift
            )

            detailed_merit_list.append(add)
            detailed_weight_list.append(add_w)

            observed_oneturn_total_shift_zpix_list.append(diag.zpix_transl[i + n_angles_2pi] - diag.zpix_transl[i])

    return detailed_merit_list, detailed_weight_list, observed_oneturn_total_shift_zpix_list, zpix_mm


def merit(ima_a, ima_b, w_a, w_b, s):
    """A definition of the merit which accounts also for the data weight.
    calculates the merit for a given shift s.
    Comparison between a and b
    Considering signal ima and weight w
    """
    if s == 0:
        # return - abs(  (ima_a - ima_b)  * w_a * w_b      ).astype("d").mean(), (w_a * w_b).astype("d").mean()

        return (ima_a * ima_b * w_a * w_b).astype("d").sum(), (w_a * w_b).astype("d").sum()

    elif s > 0:
        # Keep the comment lines in case one wish to test L1
        # pi = abs(ima_b[s:] - ima_a[:-s])
        # pw = w_b[s:] * w_a[:-s]
        # return -  ( pi * pw      ).astype("d").mean(), (pw).astype("d").mean()

        pi = ima_b[s:] * ima_a[:-s]
        pw = w_b[s:] * w_a[:-s]
        return (pi * pw).astype("d").sum(), pw.astype("d").sum()
    else:
        # Keep the comment lines in case one wish to test L1
        # pi = abs(ima_a[-s:] - ima_b[:s])
        # pw = w_a[-s:] * w_b[:s]
        # return - ( pi * pw ).astype("d").mean(), pw.astype("d").mean()

        pi = ima_a[-s:] * ima_b[:s]
        pw = w_a[-s:] * w_b[:s]
        return (pi * pw).astype("d").sum(), pw.astype("d").sum()


def build_total_merit_list(diag, oversample_factor, args):
    # calculats the merit at all the tested extra adjustment shifts.

    transform_images(diag, [oversample_factor, 1])
    # h_ima = diag.radios[0].shape[0]
    # search_radius_v = min(oversample_factor * args.search_radius_v, h_ima - 1)
    search_radius_v = oversample_factor * args.search_radius_v

    shift_s = []
    for_all_shifts_detailed_merit_lists = []
    for_all_shifts_detailed_weight_lists = []

    observed_oneturn_total_shift_zpix_list, zpix_mm = None, None

    for shift in range(-search_radius_v, search_radius_v + 1):
        (
            detailed_merit_list,
            detailed_weight_list,
            found_observed_oneturn_total_shift_zpix_list,
            found_zpix_mm,
        ) = detailed_merit(diag, shift)

        if found_zpix_mm is not None:
            # the following two lines do not depend on the shift.
            # The shift is what we do prior to a comparison f images
            # while the two items below are a properties of the scan
            # in particular they depend on z_translation and angles from bliss
            zpix_mm = found_zpix_mm
            observed_oneturn_total_shift_zpix_list = found_observed_oneturn_total_shift_zpix_list

            # The merit and weight are the result of comparison, they depend on the shift
            for_all_shifts_detailed_merit_lists.append(detailed_merit_list)
            for_all_shifts_detailed_weight_lists.append(detailed_weight_list)
            shift_s.append(
                shift / oversample_factor
            )  # shift_s is stored in original pixel units. Images were oversampled

        else:
            # here there is nothing to append, not correspondance was found
            pass

    # now transposition: we want for each pair  theta, theta+360 a list which contains meritvalues for each adjustment shift
    # For each pair there is a list which runs over the shifts
    # Same thing for the weights
    for_all_pairs_detailed_merit_lists = zip(*for_all_shifts_detailed_merit_lists)
    for_all_pairs_detailed_weight_lists = zip(*for_all_shifts_detailed_weight_lists)

    return (
        for_all_pairs_detailed_merit_lists,
        for_all_pairs_detailed_weight_lists,
        observed_oneturn_total_shift_zpix_list,
        zpix_mm,
    )


def main(user_args=None):
    """Analyse the diagnostics and correct the pixel size"""

    if user_args is None:
        user_args = sys.argv[1:]

    args = DictToObj(
        parse_params_values(
            DiagToPixConfig,
            parser_description=main.__doc__,
            program_version="nabu " + version,
            user_args=user_args,
        )
    )

    oversample_factor = 4
    if args.nexus_source is None:
        args.nexus_source = args.nexus_target

    ## Read all the available diagnostics.
    ## Every key correspond to a chunk of the helical pipeline
    diag_url = os.path.join("/", args.entry_name, "reconstruction/configuration/diagnostics")
    diag_keys = []
    with h5py.File(args.diag_file, "r") as f:
        diag_keys = list(f[diag_url].keys())
        diag_keys = [diag_keys[i] for i in np.argsort(list(map(int, diag_keys)))]

    # The diag_keys are 0,1,2 ... corresponding to all the z-windows ( chunck) for which we have collected contributions at different angles
    # which are nothing else but pieces of ready to use preprocessed radio , and this for different angles.
    # Pairs should coincide where they both have signal ( part of them can be dark if the detector is out of view above or below)
    # For each key there is a sequence of radio, the corresponding sequence of weights map, the corresponding z translation, and angles

    zpix_mm = None

    argument_list = [
        (DictToObj(h5todict(args.diag_file, os.path.join(diag_url, my_key))), oversample_factor, args)
        for my_key in diag_keys
    ]

    ncpus = get_available_threads()
    with Pool(processes=ncpus) as pool:
        all_res_plus_infos = pool.starmap(build_total_merit_list, argument_list)

    _, zpix_mm = None, None

    # needs to flatten the result of pool.map
    for_all_pairs_detailed_merit_lists = []
    for_all_pairs_detailed_weight_lists = []
    observed_oneturn_total_shift_zpix_list = []
    zpix_mm = None

    for (
        tmp_merit_lists,
        tmp_weight_lists,
        tmp_observed_oneturn_total_shift_zpix_list,
        tmp_zpix_mm,
    ) in all_res_plus_infos:
        if tmp_zpix_mm is not None:
            # then each item of the composed list will be for a given pairs theta, theta+360
            # and each such item is a list where each item is for a given probed shift
            for_all_pairs_detailed_merit_lists.extend(tmp_merit_lists)
            for_all_pairs_detailed_weight_lists.extend(tmp_weight_lists)
            observed_oneturn_total_shift_zpix_list.extend(tmp_observed_oneturn_total_shift_zpix_list)

            zpix_mm = tmp_zpix_mm

    if zpix_mm is None:
        message = "No overlapping was found"
        raise RuntimeError(message)

    if len(for_all_pairs_detailed_merit_lists) == 0:
        message = "No diag was found"
        raise RuntimeError(message)

    # Now an important search step:
    # We find for which pair of theta theta+360 the observed translation has the bigger absolute value.
    # Then the search for the optimum is performed for the readjustment shift in the
    # range (-search_radius_v, search_radius_v + 1)
    # considered as readjustmnet for the foud ideal pair which has exactly a translation equal to this  maximal absolute observed translation
    # For all the others the readjustment is multiplied by the pro-rata factor
    # given by their smaller z-translation over the maximal one
    max_absolute_shift = abs(np.array(observed_oneturn_total_shift_zpix_list)).max()

    # gong to search for the best pixel size
    max_merit = None
    best_shift = None
    search_radius_v = oversample_factor * args.search_radius_v

    probed_shift_list = list(range(-search_radius_v, search_radius_v + 1))

    for shift in range(-search_radius_v, search_radius_v + 1):
        total_sum = 0
        total_weight = 0

        for merit_list, weight_list, one_turn_shift in zip(
            for_all_pairs_detailed_merit_lists,
            for_all_pairs_detailed_weight_lists,
            observed_oneturn_total_shift_zpix_list,
        ):
            # sanity check
            assert len(merit_list) == len(probed_shift_list), " this should not happen"
            assert len(weight_list) == len(probed_shift_list), " this should not happen"

            # pro_rata shift
            my_shift = shift * (one_turn_shift / max_absolute_shift)

            # doing interpolation with search sorted
            i1 = np.searchsorted(probed_shift_list, my_shift)

            if i1 > 0 and i1 < len(probed_shift_list):
                i0 = i1 - 1
                fract = (-my_shift + probed_shift_list[i1]) / (probed_shift_list[i1] - probed_shift_list[i0])

                total_sum += fract * merit_list[i0] + (1 - fract) * merit_list[i1]
                total_weight += fract * weight_list[i0] + (1 - fract) * weight_list[i1]

        if total_weight == 0:
            # this avoid 0/0 = nan
            total_weight = 1

        m = total_sum / total_weight

        if (max_merit is None) or ((not np.isnan(m)) and m > max_merit):
            max_merit = m
            best_shift = shift / oversample_factor

    print(" Best shift at ", best_shift)
    print(
        f" Over one turn the reference  shift was {max_absolute_shift}  pixels. But a residual shift of {best_shift} remains   "
    )
    # the formula below is already purged from the ovrsamplig factor. We did this when we recorded best_shift and the z shift
    # is registered when lloking at the z_translation and one does not fiddle aroud with  the oversamplig at that moment
    zpix_mm = zpix_mm * (max_absolute_shift) / (max_absolute_shift - best_shift)

    print(f"Corrected zpix_mm = {zpix_mm}")

    if args.nexus_target is not None:
        nx_tomo = NXtomo().load(args.nexus_source, args.entry_name)
        nx_tomo.instrument.detector.x_pixel_size = zpix_mm * 1.0e-3  # pixel size must be provided in SI  (meters)
        nx_tomo.instrument.detector.y_pixel_size = zpix_mm * 1.0e-3  # pixel size must be provided in SI  (meters)
        nx_tomo.save(file_path=args.nexus_target, data_path=args.entry_name, overwrite=True)

    return 0
