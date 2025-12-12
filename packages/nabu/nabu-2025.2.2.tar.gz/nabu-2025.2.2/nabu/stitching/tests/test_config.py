import os
from tempfile import TemporaryDirectory
import pytest
from nabu.pipeline.config import (
    generate_nabu_configfile,
    _options_levels,
    parse_nabu_config_file,
)
from nabu.stitching.overlap import OverlapStitchingStrategy
from nabu.stitching import config as stiching_config


_stitching_types = [st.value for st in list(stiching_config.StitchingType)]
_stitching_types.append(None)


def nabu_config_to_dict(nabu_config):
    res = {}
    for section, section_content in nabu_config.items():
        res[section] = {}
        for key, values in section_content.items():
            res[section][key] = values["default"]
    return res


@pytest.mark.parametrize("stitching_type", _stitching_types)
@pytest.mark.parametrize("option_level", _options_levels.keys())
def test_stitching_config(stitching_type, option_level):
    """
    insure get_default_stitching_config is returning a dict
    and is coherent with the configuration classes
    """
    with TemporaryDirectory() as output_dir:
        nabu_dict = stiching_config.get_default_stitching_config(stitching_type)
        config = nabu_config_to_dict(nabu_dict)
        assert isinstance(config, dict)

        assert "stitching" in config
        assert "type" in config["stitching"]
        stitching_type = stiching_config.StitchingType(config["stitching"]["type"])
        if stitching_type is stiching_config.StitchingType.Z_POSTPROC:
            assert isinstance(
                stiching_config.dict_to_config_obj(config),
                stiching_config.PostProcessedSingleAxisStitchingConfiguration,
            )
        elif (
            stitching_type is stiching_config.StitchingType.Z_PREPROC
            or stitching_type is stiching_config.StitchingType.Y_PREPROC
        ):
            assert isinstance(
                stiching_config.dict_to_config_obj(config),
                stiching_config.PreProcessedSingleAxisStitchingConfiguration,
            )
        else:
            raise ValueError("not handled")

        # dump configuration to file
        output_file = os.path.join(output_dir, "config.conf")
        generate_nabu_configfile(
            fname=output_file,
            default_config=nabu_dict,
            comments=True,
            sections_comments=stiching_config.SECTIONS_COMMENTS,
            options_level=option_level,
            prefilled_values={},
        )

        # load configuration from file
        loaded_config = parse_nabu_config_file(output_file)
        config_class_instance = stiching_config.dict_to_config_obj(loaded_config)
        if stitching_type is stiching_config.StitchingType.Z_POSTPROC:
            assert isinstance(
                config_class_instance,
                stiching_config.PostProcessedSingleAxisStitchingConfiguration,
            )
        elif stitching_type is stiching_config.StitchingType.Z_PREPROC:
            assert isinstance(
                config_class_instance,
                stiching_config.PreProcessedSingleAxisStitchingConfiguration,
            )

        assert isinstance(config_class_instance.to_dict(), dict)


@pytest.mark.parametrize("stitching_strategy", [oss for oss in OverlapStitchingStrategy])
@pytest.mark.parametrize("overwrite_results", (True, "False", 0, "1"))
@pytest.mark.parametrize(
    "axis_shifts",
    (
        "",
        None,
        "None",
        "",  # noqa: PT014
        "skimage",
        "nabu-fft",
    ),
)
@pytest.mark.parametrize("axis_shifts_params", ("", {}, "window_size=200"))
@pytest.mark.parametrize(
    "slice_for_correlation",
    (
        "middle",
        "3",
    ),
)
@pytest.mark.parametrize("slices", ("middle", "0:26:2"))
@pytest.mark.parametrize(
    "input_scans",
    (
        "",
        "hdf5:scan:/data/scan.hdf5?path=entry; hdf5:scan:/data/scan.hdf5?path=entry1",
    ),
)
@pytest.mark.parametrize(
    "slurm_config",
    (
        {
            stiching_config.SLURM_MODULES_TO_LOADS: "tomotools",
            stiching_config.SLURM_PREPROCESSING_COMMAND: "",
            stiching_config.SLURM_CLEAN_SCRIPTS: True,
            stiching_config.SLURM_MEM: 56,
            stiching_config.SLURM_N_JOBS: 5,
            stiching_config.SLURM_PARTITION: "my_partition",
        },
    ),
)
def test_PreProcessedZStitchingConfiguration(
    stitching_strategy,
    overwrite_results,
    axis_shifts,
    axis_shifts_params,
    input_scans,
    slice_for_correlation,
    slices,
    slurm_config,
):
    """
    make sure configuration works well for PreProcessedZStitchingConfiguration
    """
    pre_process_config = stiching_config.PreProcessedZStitchingConfiguration.from_dict(
        {
            stiching_config.STITCHING_SECTION: {
                stiching_config.CROSS_CORRELATION_SLICE_FIELD: slice_for_correlation,
                stiching_config.AXIS_0_POS_PX: axis_shifts,
                stiching_config.AXIS_1_POS_PX: axis_shifts,
                stiching_config.AXIS_2_POS_PX: axis_shifts,
                stiching_config.AXIS_0_PARAMS: axis_shifts_params,
                stiching_config.AXIS_1_PARAMS: axis_shifts_params,
                stiching_config.AXIS_2_PARAMS: axis_shifts_params,
                stiching_config.STITCHING_STRATEGY_FIELD: stitching_strategy,
            },
            stiching_config.INPUTS_SECTION: {
                stiching_config.INPUT_DATASETS_FIELD: input_scans,
                stiching_config.STITCHING_SLICES: slices,
            },
            stiching_config.OUTPUT_SECTION: {
                stiching_config.OVERWRITE_RESULTS_FIELD: overwrite_results,
            },
            stiching_config.PRE_PROC_SECTION: {
                stiching_config.DATA_FILE_FIELD: "my_file.nx",
                stiching_config.DATA_PATH_FIELD: "entry",
                stiching_config.NEXUS_VERSION_FIELD: None,
            },
            stiching_config.SLURM_SECTION: slurm_config,
            stiching_config.NORMALIZATION_BY_SAMPLE_SECTION: {
                stiching_config.NORMALIZATION_BY_SAMPLE_MARGIN: 1,
                stiching_config.NORMALIZATION_BY_SAMPLE_SIDE: "right",
                stiching_config.NORMALIZATION_BY_SAMPLE_ACTIVE_FIELD: True,
                stiching_config.NORMALIZATION_BY_SAMPLE_METHOD: "mean",
                stiching_config.NORMALIZATION_BY_SAMPLE_WIDTH: 31,
            },
        },
    )

    from_dict = stiching_config.PreProcessedZStitchingConfiguration.from_dict(pre_process_config.to_dict())
    # workaround for scans because a new object is created each time
    # ???
    pre_process_config.settle_inputs  # noqa: B018
    assert len(from_dict.input_scans) == len(pre_process_config.input_scans)
    from_dict.input_scans = None
    pre_process_config.input_scans = None
    assert pre_process_config == from_dict


def test_PostProcessedZStitchingConfiguration():
    """
    make sure configuration works well for PostProcessedZStitchingConfiguration
    """
    pass


def test_description_dict():
    """
    make sure the description dict (used for generating the file) is working and generates a dict
    """
    assert isinstance(stiching_config.PreProcessedSingleAxisStitchingConfiguration.get_description_dict(), dict)
    assert isinstance(
        stiching_config.PostProcessedSingleAxisStitchingConfiguration.get_description_dict(),
        dict,
    )
