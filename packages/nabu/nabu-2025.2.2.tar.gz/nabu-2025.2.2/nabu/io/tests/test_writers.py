from os import path
from tempfile import TemporaryDirectory
import pytest
import numpy as np
from nabu.io.writer import NXProcessWriter
from nabu.io.reader import import_h5_to_dict
from nabu.testutils import get_data


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls._tmpdir = TemporaryDirectory(prefix="nabu_")
    cls.tempdir = cls._tmpdir.name
    cls.sino_data = get_data("mri_sino500.npz")["data"].astype(np.uint16)
    cls.data = cls.sino_data
    yield
    # teardown
    cls._tmpdir.cleanup()


@pytest.fixture(scope="class")
def bootstrap_h5(request):
    cls = request.cls
    cls._tmpdir = TemporaryDirectory(prefix="nabu_")
    cls.tempdir = cls._tmpdir.name
    cls.data = get_data("mri_sino500.npz")["data"].astype(np.uint16)
    cls.h5_config = {
        "key1": "value1",
        "some_int": 1,
        "some_float": 1.0,
        "some_dict": {
            "numpy_array": np.ones((5, 6), dtype="f"),
            "key2": "value2",
        },
    }
    yield
    # teardown
    cls._tmpdir.cleanup()


@pytest.mark.usefixtures("bootstrap_h5")
class TestNXWriter:
    def test_write_simple(self):
        fname = path.join(self.tempdir, "sino500.h5")
        writer = NXProcessWriter(fname, entry="entry0000")
        writer.write(self.data, "test_write_simple")

    def test_write_with_config(self):
        fname = path.join(self.tempdir, "sino500_cfg.h5")
        writer = NXProcessWriter(fname, entry="entry0000")
        writer.write(self.data, "test_write_with_config", config=self.h5_config)

    def test_overwrite(self):
        fname = path.join(self.tempdir, "sino500_overwrite.h5")
        writer = NXProcessWriter(fname, entry="entry0000", overwrite=True)
        writer.write(self.data, "test_overwrite", config=self.h5_config)

        writer2 = NXProcessWriter(fname, entry="entry0001", overwrite=True)
        writer2.write(self.data, "test_overwrite", config=self.h5_config)

        # overwrite entry0000
        writer3 = NXProcessWriter(fname, entry="entry0000", overwrite=True)
        new_data = self.data.copy()
        new_data += 1
        new_config = self.h5_config.copy()
        new_config["key1"] = "modified value"
        writer3.write(new_data, "test_overwrite", config=new_config)

        res = import_h5_to_dict(fname, "/")
        assert "entry0000" in res
        assert "entry0001" in res
        assert np.allclose(res["entry0000"]["test_overwrite"]["results"]["data"], self.data + 1)
        rec_cfg = res["entry0000"]["test_overwrite"]["configuration"]
        assert rec_cfg["key1"] == "modified value"

    def test_no_overwrite(self):
        fname = path.join(self.tempdir, "sino500_no_overwrite.h5")
        writer = NXProcessWriter(fname, entry="entry0000", overwrite=False)
        writer.write(self.data, "test_no_overwrite")

        writer2 = NXProcessWriter(fname, entry="entry0000", overwrite=False)
        with pytest.raises((RuntimeError, OSError)):
            writer2.write(self.data, "test_no_overwrite")

        # message = "Error should have been raised for trying to overwrite, but got the following: %s" % str(ex.value)
