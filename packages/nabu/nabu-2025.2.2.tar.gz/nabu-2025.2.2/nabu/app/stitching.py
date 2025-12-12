import logging
from pprint import pformat

from tqdm import tqdm
from nabu.stitching.slurm_utils import split_stitching_configuration_to_slurm_job
from .cli_configs import StitchingConfig
from ..pipeline.config import parse_nabu_config_file
from nabu.stitching.single_axis_stitching import stitching
from nabu.stitching.utils.post_processing import StitchingPostProcAggregation
from nabu.stitching.config import dict_to_config_obj
from .utils import parse_params_values

try:
    from sluurp.executor import submit
except ImportError:
    has_sluurp = False
else:
    has_sluurp = True

_logger = logging.getLogger(__name__)


def main():
    args = parse_params_values(
        StitchingConfig,
        parser_description="Run stitching from a configuration file. Configuration can be obtain from `stitching-config`",
    )
    logging.basicConfig(level=args["loglevel"].upper())

    conf_dict = parse_nabu_config_file(args["input-file"], allow_no_value=True)

    stitching_config = dict_to_config_obj(conf_dict)
    assert stitching_config.axis is not None, "axis must be defined to know how to stitch"
    _logger.info(" when loaded axis is %s", stitching_config.axis)
    stitching_config.settle_inputs()
    if args["only_create_master_file"]:
        # option to ease creation of the master in the following cases:
        # * user has submitted all the job but has been kicked out of the cluster
        # * only a few slurm job for some random version (cluster update...) and user want to retrigger only those job and process the aggregation only. On those cases no need to redo it all.
        tomo_objs = []
        for _, sub_config in split_stitching_configuration_to_slurm_job(stitching_config, yield_configuration=True):
            tomo_objs.append(sub_config.get_output_object().get_identifier().to_str())

        post_processing = StitchingPostProcAggregation(
            existing_objs_ids=tomo_objs,
            stitching_config=stitching_config,
        )
        post_processing.process()

    elif stitching_config.slurm_config.partition in (None, ""):
        # case 1: run locally
        _logger.info("run stitching locally with: %s", pformat(stitching_config.to_dict()))

        main_progress = tqdm(total=100, desc="stitching", leave=True)
        stitching(stitching_config, progress=main_progress)
    else:
        if not has_sluurp:
            raise ImportError(
                "sluurp not install. Please install it to distribute stitching on slurm (pip install slurm)"
            )
        main_progress = tqdm(total=100, position=0, desc="stitching")

        # case 2: run on slurm
        # note: to speed up we could do shift research on pre processing and run it only once (if manual of course). Here it will be run for all part
        _logger.info(f"will distribute stitching")

        futures = {}
        # 2.1 launch jobs
        slurm_job_progress_bars: dict = {}

        # set job name
        final_output_object_identifier = stitching_config.get_output_object().get_identifier().to_str()
        stitching_config.slurm_config.job_name = f"stitching-{final_output_object_identifier}"

        for i_job, (job, sub_config) in enumerate(
            split_stitching_configuration_to_slurm_job(stitching_config, yield_configuration=True)
        ):
            _logger.info(f"submit job nb {i_job}: handles {sub_config.slices}")
            output_object = sub_config.get_output_object().get_identifier().to_str()
            futures[output_object] = submit(job, timeout=999999)
            # note on total=100: we only consider percentage in this case (providing advancement from slurm jobs)
            slurm_job_progress_bars[job] = tqdm(
                total=100,
                position=i_job + 1,
                desc=f"   part {str(i_job).ljust(3)}",
                delay=0.5,  # avoid to mess with terminal and (near) future logs
                bar_format="{l_bar}{bar}",  # avoid using 'r_bar' as 'total' is set to 100 (percentage)
                leave=False,
            )

        main_progress.n = 50
        # 2.2 wait for future to be done and concatenate the result
        post_processing = StitchingPostProcAggregation(
            futures=futures,
            stitching_config=stitching_config,
            progress_bars=slurm_job_progress_bars,
        )
        post_processing.process()

    exit(0)


if __name__ == "__main__":
    main()
