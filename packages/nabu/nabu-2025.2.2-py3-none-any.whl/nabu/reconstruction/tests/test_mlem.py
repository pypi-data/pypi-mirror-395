import pytest
import numpy as np
from scipy.ndimage import shift
from nabu.testutils import get_data

from nabu.cuda.utils import __has_cupy__
from nabu.reconstruction.mlem import MLEMReconstructor, NabuMLEMReconstructor, has_corrct

__have_corrct__ = has_corrct(safe=True)
try:
    import astra

    __has_astra__ = True
except:
    __has_astra__ = False


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    datafile = get_data("test_mlem.npz")
    cls.data_wvu = datafile["data_wvu"]
    cls.angles_rad = datafile["angles_rad"]
    cls.pixel_size_cm = datafile["pixel_size"] * 1e4  # pixel_size originally in um
    cls.true_cor = datafile["true_cor"]
    cls.mlem_cor_None_nosh = datafile["mlem_cor_None_nosh"]
    cls.mlem_cor_truecor_nosh = datafile["mlem_cor_truecor_nosh"]
    cls.mlem_cor_truecor_shifts_v0 = datafile["mlem_cor_truecor_shifts_v0"]
    cls.shifts_uv_v0 = datafile["shifts_uv_v0"]
    cls.shifts_uv = datafile["shifts_uv"]

    cls.tol = 1.3e-4


@pytest.mark.skipif(not (__has_cupy__ and __have_corrct__), reason="Need cupy and corrct for this test")
@pytest.mark.usefixtures("bootstrap")
class TestMLEMReconstructor:
    """These tests test the general MLEM reconstruction algorithm
    and the behavior of the reconstruction with respect to horizontal shifts.
    Only horizontal shifts are tested here because vertical shifts are handled outside
    the reconstruction object, but in the embedding reconstruction pipeline. See FullFieldReconstructor
    It is compared against a reference reconstruction generated with the `rec_mlem` function
    defined in the `generate_test_data.py` script.
    """

    def _rec_mlem(self, cor, shifts_uv, data_wvu, angles_rad):
        n_angles, n_z, n_x = data_wvu.shape

        mlem = MLEMReconstructor(
            (n_z, n_angles, n_x),
            angles_rad,
            shifts_uv=shifts_uv,
            cor=cor,
            n_iterations=50,
            extra_options={"centered_axis": True, "clip_outer_circle": True, "scale_factor": 1 / self.pixel_size_cm},
        )
        rec_mlem = mlem.reconstruct(data_wvu.swapaxes(0, 1))
        return rec_mlem

    def test_simple_mlem_recons_cor_None_nosh(self):
        slice_index = 25
        rec = self._rec_mlem(None, None, self.data_wvu, self.angles_rad)[slice_index]
        delta = np.abs(rec - self.mlem_cor_None_nosh)
        assert np.max(delta) < self.tol

    def test_simple_mlem_recons_cor_truecor_nosh(self):
        slice_index = 25
        rec = self._rec_mlem(self.true_cor, None, self.data_wvu, self.angles_rad)[slice_index]
        delta = np.abs(rec - self.mlem_cor_truecor_nosh)
        assert np.max(delta) < 2.6e-4

    def test_compare_with_fbp(self):
        from nabu.reconstruction.fbp import Backprojector

        def _rec_fbp(cor, shifts_uv, data_wvu, angles_rad):
            n_angles, n_z, n_x = data_wvu.shape

            if shifts_uv is None:
                fbp = Backprojector(
                    (n_angles, n_x),
                    angles=angles_rad,
                    rot_center=cor,
                    halftomo=False,
                    padding_mode="edges",
                    extra_options={
                        "centered_axis": True,
                        "clip_outer_circle": True,
                        "scale_factor": 1 / self.pixel_size_cm,
                    },
                )
            else:
                fbp = Backprojector(
                    (n_angles, n_x),
                    angles=angles_rad,
                    rot_center=cor,
                    halftomo=False,
                    padding_mode="edges",
                    extra_options={
                        "centered_axis": True,
                        "clip_outer_circle": True,
                        "scale_factor": 1 / self.pixel_size_cm,  # convert um to cm
                        "axis_correction": shifts_uv[:, 0],
                    },
                )

            rec_fbp = np.zeros((n_z, n_x, n_x), "f")
            for i in range(n_z):
                rec_fbp[i] = fbp.fbp(data_wvu[:, i])

            return rec_fbp

        fbp = _rec_fbp(self.true_cor, None, self.data_wvu, self.angles_rad)[25]
        mlem = self._rec_mlem(self.true_cor, None, self.data_wvu, self.angles_rad)[25]
        delta = np.abs(fbp - mlem)
        assert (
            np.max(delta) < 400
        )  # These two should not be really equal. But the test should test that both algo FBP and MLEM behave similarly.

    def test_mlem_zeroshifts_equal_noshifts(self):
        shifts = np.zeros((len(self.angles_rad), 2))
        rec_nosh = self._rec_mlem(self.true_cor, None, self.data_wvu, self.angles_rad)
        rec_zerosh = self._rec_mlem(self.true_cor, shifts, self.data_wvu, self.angles_rad)
        delta = np.abs(rec_nosh - rec_zerosh)
        assert np.max(delta) < self.tol

    def test_mlem_recons_with_u_shifts(self):
        slice_index = 25
        rec = self._rec_mlem(self.true_cor, self.shifts_uv_v0, self.data_wvu, self.angles_rad)[slice_index]
        delta = np.abs(rec - self.mlem_cor_truecor_shifts_v0)
        assert np.max(delta) < self.tol


@pytest.fixture(scope="class")
def bootstrap_nabu_mlem(request):
    cls = request.cls
    cls.sino = get_data("mri_sino500.npz")["data"]


def astra_mlem(sino, rec_shape, n_it):
    vol_geom = astra.create_vol_geom(rec_shape)
    proj_geom = astra.create_proj_geom("parallel", 1.0, sino.shape[-1], np.linspace(0, np.pi, sino.shape[0], False))

    rec_id = astra.data2d.create("-vol", vol_geom)
    sinogram_id = astra.data2d.create("-sino", proj_geom)
    astra.data2d.store(sinogram_id, sino)
    astra.data2d.store(rec_id, np.ones(rec_shape, "f"))  # !

    cfg = astra.astra_dict("EM_CUDA")
    cfg["ReconstructionDataId"] = rec_id
    cfg["ProjectionDataId"] = sinogram_id

    alg_id = astra.algorithm.create(cfg)
    astra.algorithm.run(alg_id, n_it)

    rec = astra.data2d.get(rec_id)

    astra.algorithm.delete(alg_id)
    astra.data2d.delete(rec_id)
    astra.data2d.delete(sinogram_id)

    return rec


@pytest.mark.skipif(not (__has_cupy__ and __has_astra__), reason="Need astra for this test")
@pytest.mark.usefixtures("bootstrap_nabu_mlem")
class TestNabuMLEM:

    def test_mlem_simple(self):
        n_it = 50

        sino = self.sino
        mlem = NabuMLEMReconstructor(sino.shape)
        rec = mlem.reconstruct(sino, n_iterations=n_it).get()
        ref = astra_mlem(sino, mlem.slice_shape, n_it)

        err_max = np.max(np.abs(rec - ref))
        tol = 4.5e-2
        assert err_max < tol, f"MLEM error is too high: {err_max} > {tol}"

    def test_mlem_rotcenter(self):
        subsampling = 2
        n_it = 50
        # has to be int for this test. Don't choose a too high value to avoid cropping the sinogram content
        cor_offset = 10

        sino0 = self.sino[::subsampling]

        mlem0 = NabuMLEMReconstructor(sino0.shape)
        rec0 = mlem0.reconstruct(sino0, n_iterations=n_it).get()
        rec0_crop = rec0[cor_offset // 2 : -cor_offset // 2, cor_offset // 2 : -cor_offset // 2]

        sino = sino0[:, cor_offset:]
        rot_center = (sino0.shape[-1] - 1) / 2 - cor_offset
        mlem = NabuMLEMReconstructor(sino.shape, rot_center=rot_center)
        rec = mlem.reconstruct(sino, n_iterations=n_it).get()

        err_max = np.max(np.abs(rec - rec0_crop))
        tol = 0.5  # proj/backproj are not really translation-invariant after all
        assert err_max < tol

    def test_mlem_translations(self):
        n_iterations = 50

        mlem0 = NabuMLEMReconstructor(self.sino.shape)
        rec0 = mlem0.reconstruct(self.sino, n_iterations=n_iterations).get()

        # translations are in pixel units
        transl_min = -11
        transl_max = 20.5
        rng_seed = 10
        rng = np.random.Generator(np.random.PCG64(seed=rng_seed))
        x_translations = rng.uniform(low=transl_min, high=transl_max, size=self.sino.shape[0]).astype("f")

        def _sino_horizonal_shifts(sino):
            sino_shifted = sino.copy()
            for i in range(sino.shape[0]):
                sino_shifted[i] = shift(sino[i], x_translations[i], order=2)
            return sino_shifted

        sino_shifted = _sino_horizonal_shifts(self.sino)

        mlem = NabuMLEMReconstructor(self.sino.shape, extra_options={"axis_correction": x_translations})
        rec = mlem.reconstruct(sino_shifted, n_iterations=n_iterations).get()

        err_max = np.max(np.abs(rec - rec0))
        tol = 4.0  # small errors accumulate when doing iterative. Still quite good looking
        assert err_max < tol, f"Wrong reconstruction with x-translations, using seed={rng_seed}"
