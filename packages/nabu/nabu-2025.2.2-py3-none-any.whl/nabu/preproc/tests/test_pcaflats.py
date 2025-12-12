import os
import numpy as np
import pytest

import h5py
from nabu.testutils import utilstest
from nabu.preproc.flatfield import (
    PCAFlatsDecomposer,
    PCAFlatsNormalizer,
)


@pytest.fixture(scope="class")
def bootstrap_pcaflats(request):
    cls = request.cls
    # TODO: these tolerances for having the tests passed should be tighter.
    # Discrepancies between id11 code and nabu code are still mysterious.
    cls.mean_abs_tol = 1e-1
    cls.comps_abs_tol = 1e-2
    cls.projs, cls.flats, cls.darks = get_pcaflats_data("test_pcaflats.npz")
    cls.raw_projs = cls.projs.copy()  # Needed because flat correction is done inplace.
    ref_data = get_pcaflats_refdata("ref_pcaflats.npz")
    cls.mean = ref_data["mean"]
    cls.components_3 = ref_data["components_3"]
    cls.components_15 = ref_data["components_15"]
    cls.dark = ref_data["dark"]
    cls.normalized_projs_3 = ref_data["normalized_projs_3"]
    cls.normalized_projs_15 = ref_data["normalized_projs_15"]
    cls.normalized_projs_custom_mask = ref_data["normalized_projs_custom_mask"]
    cls.test_normalize_projs_custom_prop = ref_data["normalized_projs_custom_prop"]

    cls.h5_filename_3 = get_h5_pcaflats("pcaflat_3.h5")
    cls.h5_filename_15 = get_h5_pcaflats("pcaflat_15.h5")


def get_pcaflats_data(*dataset_path):
    """
    Get a dataset file from silx.org/pub/nabu/data
    dataset_args is a list describing a nested folder structures, ex.
    ["path", "to", "my", "dataset.h5"]
    """
    dataset_relpath = os.path.join(*dataset_path)
    dataset_downloaded_path = utilstest.getfile(dataset_relpath)
    data = np.load(dataset_downloaded_path)
    projs = data["projs"].astype(np.float32)
    flats = data["flats"].astype(np.float32)
    darks = data["darks"].astype(np.float32)

    return projs, flats, darks


def get_h5_pcaflats(*dataset_path):
    """
    Get a dataset file from silx.org/pub/nabu/data
    dataset_args is a list describing a nested folder structures, ex.
    ["path", "to", "my", "dataset.h5"]
    """
    dataset_relpath = os.path.join(*dataset_path)
    dataset_downloaded_path = utilstest.getfile(dataset_relpath)

    return dataset_downloaded_path


def get_pcaflats_refdata(*dataset_path):
    """
    Get a dataset file from silx.org/pub/nabu/data
    dataset_args is a list describing a nested folder structures, ex.
    ["path", "to", "my", "dataset.h5"]
    """
    dataset_relpath = os.path.join(*dataset_path)
    dataset_downloaded_path = utilstest.getfile(dataset_relpath)
    data = np.load(dataset_downloaded_path)

    return data


def get_decomposition(filename):
    with h5py.File(filename, "r") as f:
        # Load the dataset
        p_comps = f["entry0000/p_components"][()]
        p_mean = f["entry0000/p_mean"][()]
        dark = f["entry0000/dark"][()]
    return p_comps, p_mean, dark


@pytest.mark.usefixtures("bootstrap_pcaflats")
class TestPCAFlatsDecomposer:
    def test_decompose_flats(self):
        # Build 3-sigma basis
        pca = PCAFlatsDecomposer(self.flats, self.darks, nsigma=3)
        message = f"Found a discrepency between computed mean flat and reference."
        assert np.allclose(self.mean, pca.mean, atol=self.mean_abs_tol), message
        message = f"Found a discrepency between computed components and reference ones if nsigma=3."
        assert np.allclose(self.components_3, np.array(pca.components), atol=self.comps_abs_tol), message

        # Build 1.5-sigma basis
        pca = PCAFlatsDecomposer(self.flats, self.darks, nsigma=1.5)
        message = f"Found a discrepency between computed components and reference ones, if nsigma=1.5."
        assert np.allclose(self.components_15, np.array(pca.components), atol=self.comps_abs_tol), message

    def test_save_load_decomposition(self):
        pca = PCAFlatsDecomposer(self.flats, self.darks, nsigma=3)
        tmp_path = os.path.join(os.path.dirname(self.h5_filename_3), "PCA_Flats.h5")
        pca.save_decomposition(path=tmp_path)
        p_comps, p_mean, dark = get_decomposition(tmp_path)
        message = f"Found a discrepency between saved and loaded mean flat."
        assert np.allclose(self.mean, p_mean, atol=self.mean_abs_tol), message
        message = f"Found a discrepency between saved and loaded components if nsigma=3."
        assert np.allclose(self.components_3, p_comps, atol=self.comps_abs_tol), message
        message = f"Found a discrepency between saved and loaded dark."
        assert np.allclose(self.dark, dark, atol=self.comps_abs_tol), message
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@pytest.mark.usefixtures("bootstrap_pcaflats")
class TestPCAFlatsNormalizer:
    def test_load_pcaflats(self):
        """Tests that the structure of the output PCAFlat h5 file is correct."""
        p_comps, p_mean, dark = get_decomposition(self.h5_filename_3)
        # Check the shape of the loaded data
        assert p_comps.shape[1:] == p_mean.shape
        assert p_comps.shape[1:] == dark.shape

    def test_normalize_projs(self):
        p_comps, p_mean, dark = get_decomposition(self.h5_filename_3)
        pca = PCAFlatsNormalizer(p_comps, dark, p_mean)
        projs = self.raw_projs.copy()
        pca.normalize_radios(projs)
        assert np.allclose(projs, self.normalized_projs_3, atol=1e-2)
        p_comps, p_mean, dark = get_decomposition(self.h5_filename_15)
        pca = PCAFlatsNormalizer(p_comps, dark, p_mean)
        projs = self.raw_projs.copy()
        pca.normalize_radios(projs)
        assert np.allclose(projs, self.normalized_projs_15, atol=1e-2)

    def test_use_custom_mask(self):
        mask = np.zeros(self.mean.shape, dtype=bool)
        mask[:, :10] = True
        mask[:, -10:] = True
        p_comps, p_mean, dark = get_decomposition(self.h5_filename_3)

        pca = PCAFlatsNormalizer(p_comps, dark, p_mean)
        projs = self.raw_projs.copy()
        pca.normalize_radios(projs, mask=mask)
        assert np.allclose(projs, self.normalized_projs_custom_mask, atol=1e-2)

    def test_change_mask_prop(self):
        p_comps, p_mean, dark = get_decomposition(self.h5_filename_3)
        pca = PCAFlatsNormalizer(p_comps, dark, p_mean)
        projs = self.raw_projs.copy()
        pca.normalize_radios(projs, prop=0.05)
        assert np.allclose(projs, self.test_normalize_projs_custom_prop, atol=1e-2)
