import sys
import numpy as np
import h5py
from .. import version
from ..utils import DictToObj
from ..resources.logger import Logger
from .cli_configs import CreateDistortionMapHorizontallyMatchedFromPolyConfig
from .utils import parse_params_values


def create_distortion_maps_entry_point(user_args=None):
    """This application builds  two arrays. Let us call them map_x and map_z. Both are 2D arrays with shape given by (nz, nx).
    These maps are meant to be used to generate a corrected detector image, using them to obtain  the pixel (i,j) of the corrected
    image by interpolating the raw data at position ( map_z(i,j), map_x(i,j) ).

    This map is determined by a user given  polynomial  P(rs) in the radial variable  rs = sqrt( (z-center_z)**2 + (x-center_x)**2 ) / (nx/2)
    where center_z and center_x give the center around which the deformation is centered.

    The perfect  position (zp,xp) , that would be observed on a perfect detector, of a photon observed at pixel (z,x) of the distorted detector is:

       (zp, xp) = (center_z,  center_x) +  P(rs) *  ( z - center_z  , x - center_x )

    The polynomial is given by P(rs) = rs *(1 + c2 * rs**2 + c4 * rs**4)

    The map is rescaled and shifted so that a perfect match is realised at the borders of a horizontal line passing by the center. This ensures coherence
    with the procedure of pixel size calibration which is performed moving a needle horizontally and reading the motor positions at the extreme positions.

    The maps are written in the target file, creating it as hdf5 file,  in the datasets

        "/coords_source_x"
        "/coords_source_z"

    The URLs of these two maps can be used for the detector correction of type "map_xz"
    in the nabu configuration file as in this example

         [dataset]
         ...
         detector_distortion_correction = map_xz
         detector_distortion_correction_options = map_x="silx:./map_coordinates.h5?path=/coords_source_x" ;  map_z="silx:./map_coordinates.h5?path=/coords_source_z"

    """

    if user_args is None:
        user_args = sys.argv[1:]
        args_dict = parse_params_values(
            CreateDistortionMapHorizontallyMatchedFromPolyConfig,
            parser_description=create_maps_x_and_z.__doc__,
            program_version="nabu " + version,
            user_args=user_args,
        )

    logger = Logger("create_distortion_maps", level=user_args["loglevel"], logfile="create_distortion_maps.log")

    coords_source_x, coords_source_z, new_axis_pos = create_maps_x_and_z(args_dict)  # pylint: disable=E0606

    with h5py.File(args_dict["target_file"], "w") as f:
        f["coords_source_x"] = coords_source_x
        f["coords_source_z"] = coords_source_z

    if new_axis_pos is not None:
        logger.info("New axis position at %e it was previously  %e " % (new_axis_pos, args_dict["axis_pos"]))

    return 0


def create_maps_x_and_z(args_dict):
    """This method is meant for those applications which wants to use the functionalities of the poly2map
    entry point through a standard python API.
    The argument arg_dict must contain the keys that you can find in cli_configs.py:
                    CreateDistortionMapHorizontallyMatchedFromPolyConfig
    Look at this files for variables and their meaning and defaults
    Parameters::
       args_dict : dict
             a dictionary containing keys : center_x, center_z, nz, nx,  c2, c4, axis_pos
    return:
           max_x, map_z, new_rot_pos

    """
    args = DictToObj(args_dict)

    nz, nx = args.nz, args.nx
    center_x, center_z = (args.center_x, args.center_z)

    c4 = args.c4
    c2 = args.c2

    polynomial = np.poly1d([c4, 0, c2, 0, 1, 0.0])
    # change of variable
    cofv = np.poly1d([1.0 / (nx / 2), 0])
    polynomial = nx / 2 * polynomial(cofv)

    left_border = 0 - center_x
    right_border = nx - 1 - center_x

    def get_rescaling_shift(left_border, right_border, polynomial):
        dl = polynomial(left_border)
        dr = polynomial(right_border)

        rescaling = (dr - dl) / (right_border - left_border)
        shift = -left_border * rescaling + dl
        return rescaling, shift

    final_grid_rescaling, final_grid_shift = get_rescaling_shift(left_border, right_border, polynomial)

    coords_z, coords_x = np.indices([nz, nx])

    coords_z = ((coords_z - center_z) * final_grid_rescaling).astype("d")
    coords_x = ((coords_x - center_x) * final_grid_rescaling + final_grid_shift).astype("d")

    distances_goal = np.sqrt(coords_z * coords_z + coords_x * coords_x)

    distances_unknown = distances_goal

    pp_deriv = polynomial.deriv()

    # iteratively finding the positions to interpolated at by newton method
    for i in range(10):
        errors = polynomial(distances_unknown) - distances_goal
        derivative = pp_deriv(distances_unknown)
        distances_unknown = distances_unknown - errors / derivative

    distances_data_sources = distances_unknown

    # avoid 0/0
    distances_data_sources[distances_goal < 1] = 1
    distances_goal[distances_goal < 1] = 1

    coords_source_z = coords_z * distances_data_sources / distances_goal + center_z
    coords_source_x = coords_x * distances_data_sources / distances_goal + center_x

    new_axis_pos = None

    if args.axis_pos is not None:
        # here we search on the central line a point new_axis_pos
        # such  that
        # coords_source_x[ i_central_y,  nuova_axis_pos ] == axis_pos
        #
        n_y, n_x = coords_source_x.shape
        x_coordinates_central_line = coords_source_x[n_y // 2]

        if np.any(np.less_equal(np.diff(x_coordinates_central_line), 0)):
            message = """ Error in the coordinates map, the X coordinates are not monotonous on the central line """
            raise ValueError(message)
        i1 = np.searchsorted(x_coordinates_central_line, args.axis_pos)
        i1 = np.clip(i1, 1, n_x - 1)
        i0 = i1 - 1
        val0 = x_coordinates_central_line[i0]
        val1 = x_coordinates_central_line[i1]
        fract = (args.axis_pos - val0) / (val1 - val0)
        new_axis_pos = i0 * (1 - fract) + i1 * fract

    return coords_source_x, coords_source_z, new_axis_pos
