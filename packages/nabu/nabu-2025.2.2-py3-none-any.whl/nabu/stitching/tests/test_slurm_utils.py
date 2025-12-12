import os
import pytest
from tomoscan.esrf import NXtomoScan
from tomoscan.esrf.volume import HDF5Volume
from tomoscan.esrf.scan.utils import cwd_context
from nabu.stitching.config import PreProcessedZStitchingConfiguration, SlurmConfig
from nabu.stitching.overlap import OverlapStitchingStrategy
from nabu.stitching.slurm_utils import (
    split_slices,
    get_working_directory,
    split_stitching_configuration_to_slurm_job,
)
from tomoscan.esrf.mock import MockNXtomo

try:
    import sluurp  # noqa: F401
except ImportError:
    has_sluurp = False
else:
    has_sluurp = True


def test_split_slices():
    """test split_slices function"""
    assert tuple(split_slices(slice(0, 100, 1), n_parts=4)) == (
        slice(0, 25, 1),
        slice(25, 50, 1),
        slice(50, 75, 1),
        slice(75, 100, 1),
    )

    assert tuple(split_slices(slice(0, 50, 2), n_parts=3)) == (
        slice(0, 17, 2),
        slice(17, 34, 2),
        slice(34, 50, 2),
    )

    assert tuple(split_slices(slice(0, 100, 1), n_parts=1)) == (slice(0, 100, 1),)

    assert tuple(split_slices(("first", "middle", "last"), 2)) == (
        ("first", "middle"),
        ("last",),
    )
    assert tuple(
        split_slices(
            (
                10,
                12,
                13,
            ),
            4,
        )
    ) == ((10,), (12,), (13,))

    with pytest.raises(TypeError):
        next(split_slices("dsad", 12))


def test_get_working_directory():
    """test get_working_directory function"""
    assert get_working_directory(NXtomoScan("/this/is/my/hdf5file.hdf5", "entry")) == "/this/is/my"
    assert get_working_directory(HDF5Volume("/this/is/my/volume.hdf5", "entry")) == "/this/is/my"


@pytest.mark.skipif(not has_sluurp, reason="sluurp not installed")
def test_split_stitching_configuration_to_slurm_job(tmp_path):
    """
    test split_stitching_configuration_to_slurm_job behavior

    This test is stitching two existing NXtomo (scan1 and scan2 contained in inputs_dir) and create a final_nx_tomo.nx to the output_dir

    The stitching will be split in two slurm jobs.
    One will create output_dir/final_nx_tomo/final_nx_tomo_part_0.nx and the second output_dir/final_nx_tomo/final_nx_tomo_part_1.nx
    then the concatenation (not tested here) will create a output_dir/final_nx_tomo.nx redirecting to the sub parts

    This test only focus on checking each sub configuration is as expected
    """

    inputs_dir = tmp_path / "inputs"
    inputs_dir.mkdir()
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()

    with cwd_context(inputs_dir):
        # the current working directory context help to check file path are moved to absolute.
        # which is important because those jobs will be launched on slurm
        scan_1 = MockNXtomo(
            os.path.join("scan_1"),
            n_proj=10,
            n_ini_proj=10,
            dim=100,
        ).scan

        scan_2 = MockNXtomo(
            os.path.join("scan_2"),
            n_proj=10,
            n_ini_proj=10,
            dim=100,
        ).scan

        n_jobs = 2

        raw_config = PreProcessedZStitchingConfiguration(
            axis_0_pos_px=None,
            axis_0_pos_mm=None,
            axis_0_params={},
            axis_1_pos_px=None,
            axis_1_pos_mm=None,
            axis_1_params={},
            axis_2_pos_px=None,
            axis_2_pos_mm=None,
            axis_2_params={},
            stitching_strategy=OverlapStitchingStrategy.MEAN,
            overwrite_results=True,
            slurm_config=SlurmConfig(
                partition="par-test",
                mem="45G",
                n_jobs=n_jobs,
                other_options="",
                preprocessing_command="source /my/venv",
                clean_script=True,
            ),
            slices=slice(0, 120, 1),
            input_scans=(scan_1, scan_2),
            output_file_path=os.path.join("../outputs/", "final_nx_tomo.nx"),
            output_data_path="stitched_entry",
            output_nexus_version=None,
            slice_for_cross_correlation="middle",
            pixel_size=None,
        )

        sbatch_script_jobs = []
        stitching_configurations = []
        for job, configuration in split_stitching_configuration_to_slurm_job(raw_config, yield_configuration=True):
            sbatch_script_jobs.append(job)
            stitching_configurations.append(configuration)

        assert len(stitching_configurations) == n_jobs == len(sbatch_script_jobs)
        for i_sub_config, sub_config in enumerate(stitching_configurations):
            assert isinstance(sub_config, type(raw_config))
            assert sub_config.slurm_config is None
            assert sub_config.output_file_path == os.path.join(
                output_dir, "final_nx_tomo", f"final_nx_tomo_part_{i_sub_config}.nx"
            )
        assert raw_config.output_file_path == os.path.join(output_dir, "final_nx_tomo.nx")
