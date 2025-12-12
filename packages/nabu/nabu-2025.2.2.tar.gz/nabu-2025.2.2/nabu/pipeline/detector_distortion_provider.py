from ..resources.utils import extract_parameters
from ..io.detector_distortion import DetectorDistortionBase, DetectorDistortionMapsXZ
import silx.io


def DetectorDistortionProvider(detector_full_shape_vh=(0, 0), correction_type="", options=""):
    if correction_type == "identity":
        return DetectorDistortionBase(detector_full_shape_vh=detector_full_shape_vh)
    elif correction_type == "map_xz":
        options = options.replace("path=", "path_eq")
        user_params = extract_parameters(options)
        print(user_params, options)
        map_x = silx.io.get_data(user_params["map_x"].replace("path_eq", "path="))
        map_z = silx.io.get_data(user_params["map_z"].replace("path_eq", "path="))
        return DetectorDistortionMapsXZ(map_x=map_x, map_z=map_z)
    else:
        message = f"""
        Unknown correction type: {correction_type} requested
        """
        raise ValueError(message)
