# ruff: noqa
from ..fullfield.nabu_config import *
import copy

## keep the text below for future inclusion in the documentation
# start_z, end_z , start_z_mm, end_z_mm
# ----------------------------------------------------------------
# By default, all the volume is reconstructed slice by slice, along the axis 'z'.
# ** option 1) you can set
#     start_z_mm=0
#     end_z_mm  = 0
#
#     Now, concerning start_z and end_z,  Use positive integers, with start_z < end_z
#               The reconstructed vertical region will be
#                   slice start = first doable + start_z
#                   slice end   = first doable + end_z
#                or less if such range needs to be clipped to the doable one
#
#                As an example start_z= 10, end_z = 20
#                for reconstructing 10 slices close to scan start.
#                NOTE: we are proceeding in the direction of the scan so that, in millimiters,
#                       the start may be above or below the end
#      To reconstruct the whole doable volume set
#
#        start_z= 0
#        end_z  =-1
#
# ** option 2) using start_z_mm, end_z_mm
#               Use positive floats, in millimiters. They indicate the height above the sample stage
#             The values of start_z and end_z are not used in this case


help_start_end_z = """ If  start_z_mm , end_z_mm are seto to zero, then start_z and end_z will be effective unless  end_z_fract  is different from zero. In this latter case the vertical range will be given in terms o the fractional position between the first doable and last doable slices.
Otherwhise, if start_z_mm and end_z_mm are not zero,  the slices whose height above the sample stage, in millimiters, between start_z_mm and end_z_mm are reconstructed
"""

# we need to deepcopy this in order not to mess the original nabu_config of the full-field pipeline
nabu_config = copy.deepcopy(nabu_config)

nabu_config["preproc"]["processes_file"] = {
    "default": "",
    "help": "Path tgo the file where some operations should be stored for later use. By default it is 'xxx_nabu_processes.h5'",
    "validator": optional_file_location_validator,
    "type": "required",
}
nabu_config["preproc"]["double_flatfield"]["default"] = 1


nabu_config["reconstruction"].update(
    {
        "dz_per_proj": {
            "default": 0,
            "help": " A positive DZPERPROJ means that the rotation axis is going up. Alternatively the vertical translations, can be given through an array using the variable z_per_proj_file",
            "validator": float_validator,
            "type": "optional",
        },
        "z_per_proj_file": {
            "default": "",
            "help": "Alternative to dz_per_proj. A file where each line has one value: vertical displacements of the axis. There should be as many values as there are projection images.",
            "validator": optional_file_location_validator,
            "type": "optional",
        },
        "dx_per_proj": {
            "default": 0,
            "help": " A positive value means that the rotation axis is going on the rigth. Alternatively the horizontal translations, can be given through an array using the variable x_per_proj_file",
            "validator": float_validator,
            "type": "optional",
        },
        "x_per_proj_file": {
            "default": "",
            "help": "Alternative to dx_per_proj. A file where each line has one value: horizontal displacements of the axis. There should be as many values as there are projection images.",
            "validator": optional_file_location_validator,
            "type": "optional",
        },
        "axis_to_the_center": {
            "default": "1",
            "help": "Whether to shift start_x and start_y so to have the axis at the center",
            "validator": boolean_validator,
            "type": "optional",
        },
        "auto_size": {
            "default": "1",
            "help": "Wether to set automatically start_x end_x start_y end_y ",
            "validator": boolean_validator,
            "type": "optional",
        },
        "use_hbp": {
            "default": "0",
            "help": "Wether to use hbp routine instead of the backprojector from fbp ",
            "validator": boolean_validator,
            "type": "optional",
        },
        "fan_source_distance_meters": {
            "default": 1.0e9,
            "help": "For HBP, for the description of the fan geometry, the source to axis distance. Defaults to a large value which implies parallel geometry",
            "validator": float_validator,
            "type": "optional",
        },
        "start_z_mm": {
            "default": "0",
            "help": help_start_end_z,
            "validator": float_validator,
            "type": "optional",
        },
        "end_z_mm": {
            "default": "0",
            "help": " To determine the reconstructed vertical range: the height in millimiters above the stage below which slices are reconstructed ",
            "validator": float_validator,
            "type": "optional",
        },
        "start_z_fract": {
            "default": "0",
            "help": help_start_end_z,
            "validator": float_validator,
            "type": "optional",
        },
        "end_z_fract": {
            "default": "0",
            "help": " To determine the reconstructed vertical range: the height in fractional position between first doable slice and last doable slice  above the stage below which slices are reconstructed ",
            "validator": float_validator,
            "type": "optional",
        },
        "start_z": {
            "default": "0",
            "help": "the first slice of the reconstructed range. Numbered going in the direction of the scan and starting with number zero for the first doable slice",
            "validator": slice_num_validator,
            "type": "optional",
        },
        "end_z": {
            "default": "-1",
            "help": "the "
            "end"
            " slice of the reconstructed range. Numbered going in the direction of the scan and starting with number zero for the first doable slice",
            "validator": slice_num_validator,
            "type": "optional",
        },
    }
)
nabu_config["pipeline"].update(
    {
        "skip_after_flatfield_dump": {
            "default": "0",
            "help": "When the writing of the flatfielded data is activated, if this option is set, then the phase and reconstruction steps are skipped",
            "validator": boolean_validator,
            "type": "optional",
        },
    }
)
nabu_config["reconstruction"].update(
    {
        "angular_tolerance_steps": {
            "default": "3.0",
            "help": "the angular tolerance, an angular width expressed in units of an angular step, which is tolerated in the criteria for deciding if a slice is reconstructable or not",
            "validator": float_validator,
            "type": "advanced",
        },
        "redundancy_angle_deg": {
            "default": "0",
            "help": "Can be 0,180 or 360. If there are dead detector regions (notably scintillator junction (stripes) which need to be complemented at +-360 for local tomo or +- 180 for conventional tomo. This may have an impact on the doable vertical span (you can check it with the --dry-run 1 option)",
            "validator": float_validator,
            "type": "advanced",
        },
        "enable_halftomo": {
            "default": "0",
            "help": "nabu-helical applies the same treatment for half-tomo as for full-tomo. Always let this key to zero",
            "validator": boolean_validator,
            "type": "advanced",
        },
        "helical_halftomo": {
            "default": "1",
            "help": "Wether to consider doable slices those which are contributed by an angular span greater or equal to 360, instead of just 180 or more",
            "validator": boolean_validator,
            "type": "advanced",
        },
    }
)
