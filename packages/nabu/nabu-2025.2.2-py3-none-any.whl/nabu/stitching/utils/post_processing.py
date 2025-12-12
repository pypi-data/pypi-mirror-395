import os
import logging
from nabu import version as nabu_version
from nabu.stitching.config import (
    PreProcessedSingleAxisStitchingConfiguration,
    PostProcessedSingleAxisStitchingConfiguration,
    SingleAxisStitchingConfiguration,
)
from nabu.stitching.stitcher.single_axis import PROGRESS_BAR_STITCH_VOL_DESC
from nabu.io.writer import get_datetime
from tomoscan.factory import Factory as TomoscanFactory
from silx.io.dictdump import dicttonx
from nxtomo.application.nxtomo import NXtomo
from tomoscan.utils.volume import concatenate as concatenate_volumes
from tomoscan.esrf.volume import HDF5Volume
from contextlib import AbstractContextManager
from threading import Thread
from time import sleep

_logger = logging.getLogger(__name__)


class StitchingPostProcAggregation:
    """
    for remote stitching each process will stitch a part of the volume or projections.
    Then once all are finished we want to aggregate them all to a final volume or NXtomo.

    This is the goal of this class.
    Please be careful with API. This is already inheriting from a tomwer class

    :param stitching_config: configuration of the stitching configuration
    :param futures: futures that just run
    :param existing_objs: futures that just run
    :param progress_bars: tqdm progress bars for each jobs
    """

    def __init__(
        self,
        stitching_config: SingleAxisStitchingConfiguration,
        futures: tuple | None = None,
        existing_objs_ids: tuple | None = None,
        progress_bars: dict | None = None,
    ) -> None:
        if not isinstance(stitching_config, (SingleAxisStitchingConfiguration)):
            raise TypeError(f"stitching_config should be an instance of {SingleAxisStitchingConfiguration}")
        if not ((existing_objs_ids is None) ^ (futures is None)):
            raise ValueError("Either existing_objs or futures should be provided (can't provide both)")
        if progress_bars is not None and not isinstance(progress_bars, dict):
            raise TypeError(f"'progress_bars' should be None or an instance of a dict. Got {type(progress_bars)}")
        self._futures = futures
        self._stitching_config = stitching_config
        self._existing_objs_ids = existing_objs_ids
        self._progress_bars = progress_bars or {}

    @property
    def futures(self):
        return self._futures

    @property
    def progress_bars(self) -> dict:
        return self._progress_bars

    def retrieve_tomo_objects(self) -> tuple:
        """
        Return tomo objects to be stitched together. Either from future or from existing_objs
        """
        if self._existing_objs_ids is not None:
            scan_ids = self._existing_objs_ids
        else:
            results = {}
            _logger.info(
                f"wait for slurm job to be completed. Advancement will be created once slurm job output file will be available"
            )
            for obj_id, future in self.futures.items():
                results[obj_id] = future.result()

            failed = tuple(
                filter(
                    lambda x: x.exception() is not None,
                    self.futures.values(),
                )
            )
            if len(failed) > 0:
                # if some job failed: useless to do the concatenation
                exceptions = " ; ".join([f"{job} : {job.exception()}" for job in failed])
                raise RuntimeError(f"some job failed. Won't do the concatenation. Exceptiosn are {exceptions}")

            canceled = tuple(
                filter(
                    lambda x: x.cancelled(),
                    self.futures.values(),
                )
            )
            if len(canceled) > 0:
                # if some job canceled: useless to do the concatenation
                raise RuntimeError(f"some job failed. Won't do the concatenation. Jobs are {' ; '.join(canceled)}")
            scan_ids = results.keys()
        return [TomoscanFactory.create_tomo_object_from_identifier(scan_id) for scan_id in scan_ids]

    def dump_stitching_config_as_nx_process(self, file_path: str, data_path: str, overwrite: bool, process_name: str):
        dict_to_dump = {
            process_name: {
                "config": self._stitching_config.to_dict(),
                "program": "nabu-stitching",
                "version": nabu_version,
                "date": get_datetime(),
            },
            f"{process_name}@NX_class": "NXprocess",
        }

        dicttonx(
            dict_to_dump,
            h5file=file_path,
            h5path=data_path,
            update_mode="replace" if overwrite else "add",
            mode="a",
        )

    @property
    def stitching_config(self) -> SingleAxisStitchingConfiguration:
        return self._stitching_config

    def process(self) -> None:
        """
        main function
        """

        # concatenate result
        _logger.info("all job succeeded. Concatenate results")
        if isinstance(self._stitching_config, PreProcessedSingleAxisStitchingConfiguration):
            # 1: case of a pre-processing stitching
            with self.follow_progress():
                scans = self.retrieve_tomo_objects()
            nx_tomos = []
            for scan in scans:
                if not os.path.exists(scan.master_file):
                    raise RuntimeError(
                        f"output file not created ({scan.master_file}). Stitching failed. "
                        "Please check slurm .out files to have more information. Most likely the slurm configuration is invalid. "
                        "(partition name not existing...)"
                    )
                nx_tomos.append(
                    NXtomo().load(
                        file_path=scan.master_file,
                        data_path=scan.entry,
                    )
                )
            final_nx_tomo = NXtomo.concatenate(nx_tomos)
            final_nx_tomo.save(
                file_path=self.stitching_config.output_file_path,
                data_path=self.stitching_config.output_data_path,
                overwrite=self.stitching_config.overwrite_results,
            )

            # dump NXprocess if possible
            parts = self.stitching_config.output_data_path.split("/")
            process_name = parts[-1] + "_stitching"
            if len(parts) < 2:
                data_path = "/"
            else:
                data_path = "/".join(parts[:-1])

            self.dump_stitching_config_as_nx_process(
                file_path=self.stitching_config.output_file_path,
                data_path=data_path,
                process_name=process_name,
                overwrite=self.stitching_config.overwrite_results,
            )

        elif isinstance(self.stitching_config, PostProcessedSingleAxisStitchingConfiguration):
            # 2: case of a post-processing stitching
            with self.follow_progress():
                outputs_sub_volumes = self.retrieve_tomo_objects()
            concatenate_volumes(
                output_volume=self.stitching_config.output_volume,
                volumes=tuple(outputs_sub_volumes),
                axis=1,
            )

            if isinstance(self.stitching_config.output_volume, HDF5Volume):
                parts = self.stitching_config.output_volume.metadata_url.data_path().split("/")
                process_name = parts[-1] + "_stitching"
                if len(parts) < 2:
                    data_path = "/"
                else:
                    data_path = "/".join(parts[:-1])

                self.dump_stitching_config_as_nx_process(
                    file_path=self.stitching_config.output_volume.metadata_url.file_path(),
                    data_path=data_path,
                    process_name=process_name,
                    overwrite=self.stitching_config.overwrite_results,
                )
        else:
            raise TypeError(f"stitching_config type ({type(self.stitching_config)}) not handled")

    def follow_progress(self) -> AbstractContextManager:
        return SlurmStitchingFollowerContext(
            output_files_to_progress_bars={
                job._get_output_file_path(): progress_bar for (job, progress_bar) in self.progress_bars.items()
            }
        )


class SlurmStitchingFollowerContext(AbstractContextManager):
    """Util class to provide user feedback from stitching done on slurm"""

    def __init__(self, output_files_to_progress_bars: dict):
        self._update_thread = SlurmStitchingFollowerThread(file_to_progress_bar=output_files_to_progress_bars)

    def __enter__(self) -> None:
        self._update_thread.start()

    def __exit__(self, *args, **kwargs):
        self._update_thread.join(timeout=1.5)
        for progress_bar in self._update_thread.file_to_progress_bar.values():
            progress_bar.close()  # close to clean display as leave == False


class SlurmStitchingFollowerThread(Thread):
    """
    Thread to check progression of stitching slurm job(s)
    Read slurm jobs .out file each 'delay time' and look for a tqdm line at the end.
    If it exists then deduce progress from it.

    file_to_progress_bar provide for each slurm .out file the progress bar to update
    """

    def __init__(self, file_to_progress_bar: dict, delay_time: float = 0.5) -> None:
        super().__init__()
        self._stop_run = False
        self._wait_time = delay_time
        self._file_to_progress_bar = file_to_progress_bar
        self._first_run = True

    @property
    def file_to_progress_bar(self) -> dict:
        return self._file_to_progress_bar

    def run(self) -> None:
        while not self._stop_run:
            for file_path, progress_bar in self._file_to_progress_bar.items():
                if self._first_run:
                    # make sure each progress bar have been refreshed at least one
                    progress_bar.refresh()

                if not os.path.exists(file_path):
                    continue
                with open(file_path, "r") as f:
                    try:
                        last_line = f.readlines()[-1]
                    except IndexError:
                        continue
                    advancement = self.cast_progress_line_from_log(line=last_line)
                    if advancement is not None:
                        progress_bar.n = advancement
                        progress_bar.refresh()

            self._first_run = False

            sleep(self._wait_time)

    def join(self, timeout: float | None = None) -> None:
        self._stop_run = True
        return super().join(timeout)

    @staticmethod
    def cast_progress_line_from_log(line: str) -> float | None:
        """Try to retrieve from a line from log the advancement (in percentage)"""
        if PROGRESS_BAR_STITCH_VOL_DESC not in line or "%" not in line:
            return None

        str_before_percentage = line.split("%")[0].split(" ")[-1]
        try:
            advancement = float(str_before_percentage)
        except ValueError:
            _logger.debug(f"Failed to retrieve advancement from log file. Value got is {str_before_percentage}")
            return None
        else:
            return advancement
