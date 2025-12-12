import os
import copy
import numpy
from silx.io.url import DataUrl
from tomoscan.tomoobject import TomoObject
from tomoscan.esrf.scan.nxtomoscan import NXtomoScan
from tomoscan.esrf import EDFTomoScan
from tomoscan.esrf.volume import HDF5Volume, MultiTIFFVolume
from tomoscan.esrf.volume.singleframebase import VolumeSingleFrameBase
from ..app.bootstrap_stitching import _SECTIONS_COMMENTS
from ..pipeline.config import generate_nabu_configfile
from .config import (
    StitchingConfiguration,
    get_default_stitching_config,
    PreProcessedSingleAxisStitchingConfiguration,
    PostProcessedSingleAxisStitchingConfiguration,
    SLURM_SECTION,
)

try:
    from sluurp.job import SBatchScriptJob
except ImportError:
    has_sluurp = False
else:
    has_sluurp = True


def split_stitching_configuration_to_slurm_job(
    configuration: StitchingConfiguration, yield_configuration: bool = False
):
    """
    generator to split a StitchingConfiguration into several SBatchScriptJob.

    This will handle:
       * division into several jobs according to `slices` and `n_job`
       * creation of SBatchScriptJob handling slurm configuration and command to be launched

    :param StitchingConfiguration configuration: configuration of the stitching to launch (into several jobs)
    :param bool yield_configuration: if True then yield (SBatchScriptJob, StitchingConfiguration) else yield only SBatchScriptJob
    """
    if not isinstance(configuration, StitchingConfiguration):
        raise TypeError(
            f"configuration is expected to be an instance of {StitchingConfiguration}. {type(configuration)} provided."
        )
    if not has_sluurp:
        raise ImportError("sluurp not install. Please install it to distribute stitching on slurm (pip install sluurm)")

    slurm_configuration = configuration.slurm_config
    n_jobs = slurm_configuration.n_jobs
    stitching_type = configuration.stitching_type
    # cleqn slurm configurqtion
    slurm_configuration = slurm_configuration.to_dict()
    clean_script = slurm_configuration.pop("clean_scripts", False)
    slurm_configuration.pop("n_jobs", None)
    # for now other_options is not handled
    slurm_configuration.pop("other_options", None)

    if "memory" in slurm_configuration and isinstance(slurm_configuration["memory"], str):
        memory = slurm_configuration["memory"].lower().replace(" ", "")
        memory = memory.rstrip("b").rstrip("g")
        slurm_configuration["memory"] = memory
    # handle slices if None
    configuration.settle_inputs()

    slice_sub_parts = split_slices(slices=configuration.slices, n_parts=n_jobs)
    if isinstance(configuration, PreProcessedSingleAxisStitchingConfiguration):
        stitch_prefix = os.path.basename(os.path.splitext(configuration.output_file_path)[0])
        configuration.output_file_path = os.path.abspath(configuration.output_file_path)

    elif isinstance(configuration, PostProcessedSingleAxisStitchingConfiguration):
        stitch_prefix = os.path.basename(os.path.splitext(configuration.output_volume.file_path)[0])
        configuration.output_volume.file_path = os.path.abspath(configuration.output_volume.file_path)
    else:
        raise TypeError(f"{type(configuration)} not handled")

    for i_sub_part, slice_sub_part in enumerate(slice_sub_parts):
        sub_configuration = copy.deepcopy(configuration)
        # update slice
        sub_configuration.slices = slice_sub_part
        # remove slurm configuration because once on the partition we run it manually
        sub_configuration.slurm_config = None

        if isinstance(sub_configuration, PreProcessedSingleAxisStitchingConfiguration):
            original_output_file_path, file_extension = os.path.splitext(sub_configuration.output_file_path)
            sub_configuration.output_file_path = os.path.join(
                original_output_file_path,
                os.path.basename(original_output_file_path) + f"_part_{i_sub_part}" + file_extension,
            )
            output_obj = NXtomoScan(
                scan=sub_configuration.output_file_path,
                entry=sub_configuration.output_data_path,
            )
        elif isinstance(sub_configuration, PostProcessedSingleAxisStitchingConfiguration):
            if isinstance(sub_configuration.output_volume, (HDF5Volume, MultiTIFFVolume)):
                original_output_file_path, file_extension = os.path.splitext(sub_configuration.output_volume.file_path)
                sub_configuration.output_volume.file_path = os.path.join(
                    original_output_file_path,
                    os.path.basename(original_output_file_path) + f"_part_{i_sub_part}" + file_extension,
                )
            elif isinstance(sub_configuration.output_volume, VolumeSingleFrameBase):
                url = sub_configuration.output_volume.url
                original_output_folder = url.file_path()
                sub_part_url = DataUrl(
                    file_path=os.path.join(
                        original_output_folder,
                        os.path.basename(original_output_folder) + f"_part_{i_sub_part}",
                    ),
                    data_path=url.data_path(),
                    scheme=url.scheme(),
                    data_slice=url.data_slice(),
                )
                sub_configuration.output_volume.url = sub_part_url
            output_obj = sub_configuration.output_volume
        else:
            raise TypeError(f"{type(sub_configuration)} not handled")

        working_directory = get_working_directory(output_obj)
        if working_directory is not None:
            script_dir = working_directory
        else:
            script_dir = "./"

        # save sub part nabu configuration file
        slurm_script_name = f"{stitch_prefix}_part_{i_sub_part}.sh"
        nabu_script_name = f"{stitch_prefix}_part_{i_sub_part}.conf"

        os.makedirs(script_dir, exist_ok=True)
        default_config = get_default_stitching_config(stitching_type)
        default_config.pop(SLURM_SECTION, None)
        generate_nabu_configfile(
            fname=os.path.join(script_dir, nabu_script_name),
            default_config=default_config,
            comments=True,
            sections_comments=_SECTIONS_COMMENTS,
            prefilled_values=sub_configuration.to_dict(),
            options_level="advanced",
        )

        command = f"python3 -m nabu.app.stitching {os.path.join(script_dir, nabu_script_name)}"
        script = (command,)

        job = SBatchScriptJob(
            slurm_config=slurm_configuration,
            script=script,
            script_path=os.path.join(script_dir, slurm_script_name),
            clean_script=clean_script,
            working_directory=working_directory,
        )
        job.overwrite = True
        if yield_configuration:
            yield job, sub_configuration
        else:
            yield job


def split_slices(slices: slice | tuple, n_parts: int):
    if not isinstance(n_parts, int):
        raise TypeError(f"n_parts should be an int. {type(n_parts)} provided")
    if isinstance(slices, slice):
        assert isinstance(slices.start, int), "slices.start must be an integer"
        assert isinstance(slices.stop, int), "slices.stop must be an integer"
        start = stop = slices.start
        steps_size = int(numpy.ceil((slices.stop - slices.start) / n_parts))
        while stop < slices.stop:
            stop = min(start + steps_size, slices.stop)
            yield slice(start, stop, slices.step)
            start = stop
    elif isinstance(slices, (tuple, list)):
        start = stop = 0
        steps_size = int(numpy.ceil(len(slices) / n_parts))
        while stop < len(slices):
            stop = min(start + steps_size, len(slices))
            yield slices[start:stop]
            start = stop
    else:
        raise TypeError(f"slices type ({type(slices)}) is not handled. Must be a slice or an Iterable")


def get_working_directory(obj: TomoObject) -> str | None:  # noqa: PLR0911
    """
    return working directory for a specific TomoObject
    """
    if not isinstance(obj, TomoObject):
        raise TypeError(f"obj should be an instance of {TomoObject}. {type(obj)} provided")
    if isinstance(obj, (HDF5Volume, MultiTIFFVolume)):
        if obj.file_path is None:
            return None
        else:
            return os.path.abspath(os.path.dirname(obj.file_path))
    elif isinstance(obj, VolumeSingleFrameBase):
        if obj.data_url is not None:
            return os.path.abspath(obj.data_url.file_path())
        else:
            return None
    elif isinstance(obj, EDFTomoScan):
        return obj.path
    elif isinstance(obj, NXtomoScan):
        if obj.master_file is None:
            return None
        else:
            return os.path.abspath(os.path.dirname(obj.master_file))
    else:
        raise RuntimeError(f"obj type not handled ({type(obj)})")  # noqa: TRY004
