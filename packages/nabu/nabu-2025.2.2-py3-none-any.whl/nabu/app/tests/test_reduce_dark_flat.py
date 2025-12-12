import os
import pytest
from nabu.app.reduce_dark_flat import reduce_dark_flat

#####
try:
    from tomoscan.tests.utils import NXtomoMockContext
except ImportError:
    from tomoscan.test.utils import NXtomoMockContext


@pytest.fixture
def hdf5_scan(tmp_path):
    """simple fixture to create a scan and provide it to another function"""
    test_dir = tmp_path / "my_hdf5_scan"
    with NXtomoMockContext(
        scan_path=str(test_dir),
        n_proj=10,
        n_ini_proj=10,
    ) as scan:
        yield scan


######


@pytest.mark.parametrize("dark_method", (None, "first", "mean"))
@pytest.mark.parametrize("flat_method", (None, "last", "median"))
def test_reduce_dark_flat_hdf5(tmp_path, hdf5_scan, dark_method, flat_method):
    """simply test output - processing is tested at tomoscan side"""
    # test with default url
    default_darks_path = os.path.join(hdf5_scan.path, hdf5_scan.get_dataset_basename() + "_darks.hdf5")
    default_flats_path = os.path.join(hdf5_scan.path, hdf5_scan.get_dataset_basename() + "_flats.hdf5")

    assert not os.path.exists(default_darks_path)
    assert not os.path.exists(default_flats_path)
    reduce_dark_flat(
        scan=hdf5_scan,
        dark_method=dark_method,
        flat_method=flat_method,
    )

    if dark_method is not None:
        assert os.path.exists(default_darks_path)
    else:
        assert not os.path.exists(default_darks_path)
    if flat_method is not None:
        assert os.path.exists(default_flats_path)
    else:
        assert not os.path.exists(default_flats_path)

    # make sure if already exists and no overwrite fails
    if dark_method is not None or flat_method is not None:
        with pytest.raises(KeyError):
            reduce_dark_flat(
                scan=hdf5_scan,
                dark_method=dark_method,
                flat_method=flat_method,
                overwrite=False,
            )

    # test with url provided by the user
    tuned_darks_path = os.path.join(tmp_path, "new_folder", "darks.hdf5")
    tuned_flats_path = os.path.join(tmp_path, "new_folder", "flats.hdf5")
    assert not os.path.exists(tuned_darks_path)
    assert not os.path.exists(tuned_flats_path)
    reduce_dark_flat(
        scan=hdf5_scan,
        dark_method=dark_method,
        flat_method=flat_method,
        output_reduced_darks_file=tuned_darks_path,
        output_reduced_flats_file=tuned_flats_path,
    )
    if dark_method is not None:
        assert os.path.exists(tuned_darks_path)
    else:
        assert not os.path.exists(tuned_darks_path)
    if flat_method is not None:
        assert os.path.exists(tuned_flats_path)
    else:
        assert not os.path.exists(tuned_flats_path)
