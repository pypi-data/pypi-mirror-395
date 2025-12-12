from os import path
from tempfile import mkdtemp
from shutil import rmtree
import pytest
import numpy as np
from silx.io import get_data
from nxtomo.nxobject.nxdetector import ImageKey
from nabu.testutils import generate_nx_dataset
from nabu.resources.nxflatfield import update_dataset_info_flats_darks
from nabu.resources.dataset_analyzer import HDF5DatasetAnalyzer


test_nxflatfield_scenarios = [
    {
        "name": "simple",
        "flats_pos": [slice(1, 6)],
        "darks_pos": [slice(0, 1)],
        "output_dir": None,
    },
    {
        "name": "simple_with_save",
        "flats_pos": [slice(1, 6)],
        "darks_pos": [slice(0, 1)],
        "output_dir": None,
    },
    {
        "name": "multiple_with_save",
        "flats_pos": [slice(0, 10), slice(30, 40)],
        "darks_pos": [slice(95, 100)],
        "output_dir": path.join("{tempdir}", "output_reduced"),
    },
]


# parametrize with fixture and "params=" will launch a new class for each scenario.
# the attributes set to "cls" will remain for all the tests done in this class
# with the current scenario.
@pytest.fixture(scope="class", params=test_nxflatfield_scenarios)
def bootstrap(request):
    cls = request.cls
    cls.n_projs = 265
    cls.params = request.param
    cls.tempdir = mkdtemp(prefix="nabu_")
    yield
    rmtree(cls.tempdir)


@pytest.mark.usefixtures("bootstrap")
class TestNXFlatField:
    _reduction_func = {"flats": np.median, "darks": np.mean}

    def get_nx_filename(self):
        return path.join(self.tempdir, "dataset_" + self.params["name"] + ".nx")

    def get_image_key(self):
        keys = np.zeros(self.n_projs, np.int32)
        for what, val in [("flats_pos", ImageKey.FLAT_FIELD.value), ("darks_pos", ImageKey.DARK_FIELD.value)]:
            for pos in self.params[what]:
                keys[pos.start : pos.stop] = val
        return keys

    @staticmethod
    def check_image_key(dataset_info, frame_type, expected_slices):
        data_slices = dataset_info.get_data_slices(frame_type)
        assert set(map(str, data_slices)) == set(map(str, expected_slices))

    def test_nxflatfield(self):
        dataset_fname = self.get_nx_filename()
        image_key = self.get_image_key()
        generate_nx_dataset(dataset_fname, image_key)

        dataset_info = HDF5DatasetAnalyzer(dataset_fname)

        # When parsing a "raw" dataset, flats/darks are a series of images.
        # dataset_info.flats is a dictionary where each key is the index of the frame.
        # For example dataset_info.flats.keys() = [10, 11, 12, 13, ..., 19, 1200, 1201, 1202, ..., 1219]
        for frame_type in ["darks", "flats"]:
            self.check_image_key(dataset_info, frame_type, self.params[frame_type + "_pos"])

        output_dir = self.params.get("output_dir", None)
        if output_dir is not None:
            output_dir = output_dir.format(tempdir=self.tempdir)
        update_dataset_info_flats_darks(dataset_info, True, loading_mode="load_if_present", output_dir=output_dir)
        # After reduction (median/mean), the flats/darks are located in another file.
        # median(series_1) goes to entry/flats/idx1, mean(series_2) goes to entry/flats/idx2, etc.
        assert set(dataset_info.flats.keys()) == set(s.start for s in self.params["flats_pos"])  # noqa: C401
        assert set(dataset_info.darks.keys()) == set(s.start for s in self.params["darks_pos"])  # noqa: C401

        # Check that the computations were correct
        # Loads the entire volume in memory ! So keep the data volume small for the tests
        data_volume = get_data(dataset_info.dataset_hdf5_url)
        expected_flats = {}
        for s in self.params["flats_pos"]:
            expected_flats[s.start] = self._reduction_func["flats"](data_volume[s.start : s.stop], axis=0)
        expected_darks = {}
        for s in self.params["darks_pos"]:
            expected_darks[s.start] = self._reduction_func["darks"](data_volume[s.start : s.stop], axis=0)

        flats = dataset_info.flats
        for idx in flats:
            assert np.allclose(flats[idx], expected_flats[idx])
        darks = dataset_info.darks
        for idx in darks:
            assert np.allclose(darks[idx], expected_darks[idx])
