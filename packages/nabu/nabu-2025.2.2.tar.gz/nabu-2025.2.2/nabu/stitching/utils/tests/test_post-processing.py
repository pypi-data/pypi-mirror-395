# noqa: N999
import pytest

from nabu.stitching.stitcher.single_axis import PROGRESS_BAR_STITCH_VOL_DESC
from nabu.stitching.utils.post_processing import SlurmStitchingFollowerThread


@pytest.mark.parametrize(
    "test_case",
    {
        "dump configuration: 100%|": None,
        f"stitching : 100%|": None,
        f"{PROGRESS_BAR_STITCH_VOL_DESC}: 42%": 42.0,
        f"{PROGRESS_BAR_STITCH_VOL_DESC}: 56% toto: 23%": 56.0,
        "": None,
        "my%": None,
    }.items(),
)
def test_SlurmStitchingFollowerContext(test_case):
    """Test that the conversion from log lines created by tqdm can be read back"""
    str_to_test, expected_result = test_case
    assert SlurmStitchingFollowerThread.cast_progress_line_from_log(str_to_test) == expected_result
