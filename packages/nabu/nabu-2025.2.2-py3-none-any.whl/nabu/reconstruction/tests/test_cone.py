import logging
import pytest
import numpy as np
from scipy.ndimage import gaussian_filter, shift
from nabu.utils import subdivide_into_overlapping_segment, clip_circle
from nabu.testutils import __do_long_tests__, generate_tests_scenarios

try:
    import astra

    __has_astra__ = True
except ImportError:
    __has_astra__ = False
from nabu.cuda.utils import __has_cupy__

if __has_cupy__:
    from nabu.reconstruction.cone import ConebeamReconstructor, NumpyConebeamReconstructor
if __has_astra__:
    from astra.extrautils import clipCircle


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.vol_shape = (128, 126, 126)
    cls.n_angles = 180
    cls.prj_width = 192  # detector larger than the sample
    cls.src_orig_dist = 1000
    cls.orig_det_dist = 100
    cls.volume, cls.cone_data = generate_hollow_cube_cone_sinograms(
        cls.vol_shape, cls.n_angles, cls.src_orig_dist, cls.orig_det_dist, prj_width=cls.prj_width
    )
    if __has_cupy__:
        ...


@pytest.mark.skipif(not (__has_cupy__ and __has_astra__), reason="Need cupy and astra for this test")
@pytest.mark.usefixtures("bootstrap")
class TestCone:
    def _create_cone_reconstructor(self, relative_z_position=None):
        return ConebeamReconstructor(
            self.cone_data.shape,
            self.src_orig_dist,
            self.orig_det_dist,
            relative_z_position=relative_z_position,
            volume_shape=self.volume.shape,
            # cuda_options={"ctx": self.ctx},
        )

    def test_simple_cone_reconstruction(self):
        C = self._create_cone_reconstructor()
        res = C.reconstruct(self.cone_data)
        delta = np.abs(res - self.volume)

        # Can we do better ? We already had to lowpass-filter the volume!
        # First/last slices are OK
        assert np.max(delta[:8]) < 1e-5
        assert np.max(delta[-8:]) < 1e-5
        # Middle region has a relatively low error
        assert np.max(delta[40:-40]) < 0.11
        # Transition zones between "zero" and "cube" has a large error
        assert np.max(delta[10:25]) < 0.2
        assert np.max(delta[-25:-10]) < 0.2
        # End of transition zones have a smaller error
        assert np.max(delta[25:40]) < 0.125
        assert np.max(delta[-40:-25]) < 0.125

    def test_against_explicit_astra_calls(self):
        C = self._create_cone_reconstructor()

        res = C.reconstruct(self.cone_data)
        #
        # Check that ConebeamReconstructor is consistent with these calls to astra
        #
        # "vol_geom" shape layout is (y, x, z). But here this geometry is used for the reconstruction
        # (i.e sinogram -> volume)and not for projection (volume -> sinograms).
        # So we assume a square slice. Mind that this is a particular case.
        vol_geom = astra.create_vol_geom(self.vol_shape[2], self.vol_shape[2], self.vol_shape[0])

        angles = np.linspace(0, 2 * np.pi, self.n_angles, True)
        proj_geom = astra.create_proj_geom(
            "cone",
            1.0,
            1.0,
            self.cone_data.shape[0],
            self.prj_width,
            angles,
            self.src_orig_dist,
            self.orig_det_dist,
        )
        sino_id = astra.data3d.create("-sino", proj_geom, data=self.cone_data)
        rec_id = astra.data3d.create("-vol", vol_geom)

        cfg = astra.astra_dict("FDK_CUDA")
        cfg["ReconstructionDataId"] = rec_id
        cfg["ProjectionDataId"] = sino_id
        alg_id = astra.algorithm.create(cfg)
        astra.algorithm.run(alg_id)

        res_astra = astra.data3d.get(rec_id)

        # housekeeping
        astra.algorithm.delete(alg_id)
        astra.data3d.delete(rec_id)
        astra.data3d.delete(sino_id)

        assert (
            np.max(np.abs(res - res_astra)) < 5e-4
        ), "ConebeamReconstructor results are inconsistent with plain calls to astra"

    def test_projection_full_vs_partial(self):
        """
        In the ideal case, all the data volume (and reconstruction) fits in memory.
        In practice this is rarely the case, so we have to reconstruct the volume slabs by slabs.
        The slabs should be slightly overlapping to avoid "stitching" artefacts at the edges.
        """
        # Astra seems to duplicate the projection data, even if all GPU memory is handled externally
        # Let's try with (n_z * n_y * n_x + 2 * n_a * n_z * n_x) * 4  <  mem_limit
        # 256^3 seems OK with n_a = 200 (180 MB)
        n_z = n_y = n_x = 256
        n_a = 200
        src_orig_dist = 1000
        orig_det_dist = 100

        volume, cone_data = generate_hollow_cube_cone_sinograms(
            vol_shape=(n_z, n_y, n_x), n_angles=n_a, src_orig_dist=src_orig_dist, orig_det_dist=orig_det_dist
        )
        C_full = ConebeamReconstructor(
            cone_data.shape, src_orig_dist, orig_det_dist
        )  # , cuda_options={"ctx": self.ctx})

        vol_geom = astra.create_vol_geom(n_y, n_x, n_z)

        proj_geom = astra.create_proj_geom("cone", 1.0, 1.0, n_z, n_x, C_full.angles, src_orig_dist, orig_det_dist)
        proj_id, projs_full_geom = astra.create_sino3d_gpu(volume, proj_geom, vol_geom)
        astra.data3d.delete(proj_id)

        # Do the same slab-by-slab
        inner_slab_size = 64
        overlap = 16
        slab_size = inner_slab_size + overlap * 2
        slabs = subdivide_into_overlapping_segment(n_z, slab_size, overlap)

        projs_partial_geom = np.zeros_like(projs_full_geom)
        for slab in slabs:
            z_min, z_inner_min, z_inner_max, z_max = slab
            rel_z_pos = (z_min + z_max) / 2 - n_z / 2
            subvolume = volume[z_min:z_max, :, :]
            C = ConebeamReconstructor(
                (z_max - z_min, n_a, n_x),
                src_orig_dist,
                orig_det_dist,
                relative_z_position=rel_z_pos,
                # cuda_options={"ctx": self.ctx},
            )
            proj_id, projs = astra.create_sino3d_gpu(subvolume, C.proj_geom, C.vol_geom)
            astra.data3d.delete(proj_id)

            projs_partial_geom[z_inner_min:z_inner_max] = projs[z_inner_min - z_min : z_inner_max - z_min]

        error_profile = [
            np.max(np.abs(proj_partial - proj_full))
            for proj_partial, proj_full in zip(projs_partial_geom, projs_full_geom)
        ]
        assert np.all(np.isclose(error_profile, 0.0, atol=0.0375)), "Mismatch between full-cone and slab geometries"

    def test_cone_reconstruction_magnified_vs_demagnified(self):
        """
        This will only test the astra toolbox.
        When reconstructing a volume from cone-beam data, the volume "should" have a smaller shape than the projection
        data shape (because of cone magnification).
        But astra provides the same results when backprojecting on a "de-magnified grid" and the original grid shape.
        """
        n_z = n_y = n_x = 256
        n_a = 500
        src_orig_dist = 1000
        orig_det_dist = 100
        magnification = 1 + orig_det_dist / src_orig_dist
        angles = np.linspace(0, 2 * np.pi, n_a, True)

        volume, cone_data = generate_hollow_cube_cone_sinograms(
            vol_shape=(n_z, n_y, n_x),
            n_angles=n_a,
            src_orig_dist=src_orig_dist,
            orig_det_dist=orig_det_dist,
            apply_filter=False,
        )
        rec_original_grid = astra_cone_beam_reconstruction(
            cone_data, angles, src_orig_dist, orig_det_dist, demagnify_volume=False
        )
        rec_reduced_grid = astra_cone_beam_reconstruction(
            cone_data, angles, src_orig_dist, orig_det_dist, demagnify_volume=True
        )

        m_z = (n_z - int(n_z / magnification)) // 2
        m_y = (n_y - int(n_y / magnification)) // 2
        m_x = (n_x - int(n_x / magnification)) // 2

        assert np.allclose(rec_original_grid[m_z:-m_z, m_y:-m_y, m_x:-m_x], rec_reduced_grid)

    def test_reconstruction_full_vs_partial(self):
        n_z = n_y = n_x = 256
        n_a = 500
        src_orig_dist = 1000
        orig_det_dist = 100
        angles = np.linspace(0, 2 * np.pi, n_a, True)

        volume, cone_data = generate_hollow_cube_cone_sinograms(
            vol_shape=(n_z, n_y, n_x),
            n_angles=n_a,
            src_orig_dist=src_orig_dist,
            orig_det_dist=orig_det_dist,
            apply_filter=False,
        )

        rec_full_volume = astra_cone_beam_reconstruction(cone_data, angles, src_orig_dist, orig_det_dist)

        rec_partial = np.zeros_like(rec_full_volume)
        inner_slab_size = 64
        overlap = 18
        slab_size = inner_slab_size + overlap * 2
        slabs = subdivide_into_overlapping_segment(n_z, slab_size, overlap)
        for slab in slabs:
            z_min, z_inner_min, z_inner_max, z_max = slab
            m1, m2 = z_inner_min - z_min, z_max - z_inner_max
            C = ConebeamReconstructor((z_max - z_min, n_a, n_x), src_orig_dist, orig_det_dist)
            rec = C.reconstruct(
                cone_data[z_min:z_max],
                relative_z_position=((z_min + z_max) / 2) - n_z / 2,  #  (z_min + z_max)/2.
            )
            rec_partial[z_inner_min:z_inner_max] = rec[m1 : (-m2) or None]

        # Compare volumes in inner circle
        for i in range(n_z):
            clipCircle(rec_partial[i])
            clipCircle(rec_full_volume[i])

        diff = np.abs(rec_partial - rec_full_volume)
        err_max_profile = np.max(diff, axis=(-1, -2))
        err_median_profile = np.median(diff, axis=(-1, -2))

        assert np.max(err_max_profile) < 2e-3
        assert np.max(err_median_profile) < 5.1e-6

    def test_reconstruction_horizontal_translations(self):
        n_z = n_y = n_x = 256
        n_a = 500
        src_orig_dist = 1000
        orig_det_dist = 50

        volume, cone_data = generate_hollow_cube_cone_sinograms(
            vol_shape=(n_z, n_y, n_x),
            n_angles=n_a,
            src_orig_dist=src_orig_dist,
            orig_det_dist=orig_det_dist,
            apply_filter=False,
        )

        # Apply horizontal translations on projections. This could have been done directly with astra
        shift_min, shift_max = -2, 5
        shifts_float = (shift_max - shift_min) * np.random.rand(n_a) - shift_min
        shifts_int = np.random.randint(shift_min, high=shift_max + 1, size=n_a)

        reconstructor_args = [
            cone_data.shape,
            src_orig_dist,
            orig_det_dist,
        ]
        reconstructor_kwargs = {
            "volume_shape": volume.shape,
            # "cuda_options": {"ctx": self.ctx},
        }
        cone_reconstructor = ConebeamReconstructor(*reconstructor_args, **reconstructor_kwargs)
        rec = cone_reconstructor.reconstruct(cone_data)

        # Translations done with floating-point shift values give a blurring of the image that cannot be recovered.
        # Error tolerance has to be higher for these shifts.
        for shift_type, shifts, err_tol in [
            ("integer shifts", shifts_int, 5e-3),
            ("float shifts", shifts_float, 1.6e-1),
        ]:
            cone_data_shifted = np.zeros_like(cone_data)
            [shift(cone_data[:, i, :], (0, shifts[i]), output=cone_data_shifted[:, i, :]) for i in range(n_a)]

            # Reconstruct with horizontal shifts
            cone_reconstructor_with_correction = ConebeamReconstructor(
                *reconstructor_args,
                **reconstructor_kwargs,
                extra_options={"axis_correction": -shifts},
            )

            rec_with_correction = cone_reconstructor_with_correction.reconstruct(cone_data_shifted)

            metric = lambda img: np.max(np.abs(clip_circle(img, radius=int(0.85 * img.shape[1] // 2))))
            error_profile = np.array([metric(rec[i] - rec_with_correction[i]) for i in range(n_z)])
            assert error_profile.max() < err_tol, "Max error with %s is too high" % shift_type

    def test_padding_mode(self):
        n_z = n_y = n_x = 256
        n_a = 500
        src_orig_dist = 1000
        orig_det_dist = 50

        volume, cone_data = generate_hollow_cube_cone_sinograms(
            vol_shape=(n_z, n_y, n_x),
            n_angles=n_a,
            src_orig_dist=src_orig_dist,
            orig_det_dist=orig_det_dist,
            apply_filter=False,
        )
        reconstructor_args = [
            cone_data.shape,
            src_orig_dist,
            orig_det_dist,
        ]
        reconstructor_kwargs = {
            "volume_shape": volume.shape,
            # "cuda_options": {"ctx": self.ctx},
        }
        cone_reconstructor_zero_padding = ConebeamReconstructor(*reconstructor_args, **reconstructor_kwargs)
        rec_z = cone_reconstructor_zero_padding.reconstruct(cone_data)

        for padding_mode in ["edges"]:
            cone_reconstructor = ConebeamReconstructor(
                *reconstructor_args, padding_mode=padding_mode, **reconstructor_kwargs
            )
            rec = cone_reconstructor.reconstruct(cone_data)

            metric = lambda img: np.max(np.abs(clip_circle(img, radius=int(0.85 * 128))))
            error_profile = np.array([metric(rec[i] - rec_z[i]) for i in range(n_z)])

            # import matplotlib.pyplot as plt
            # plt.figure()
            # plt.plot(np.arange(n_z), error_profile)
            # plt.legend([padding_mode])
            # plt.show()

            assert error_profile.max() < 3.1e-2, "Max error for padding=%s is too high" % padding_mode
            if padding_mode != "zeros":
                assert not (np.allclose(rec[n_z // 2], rec_z[n_z // 2])), (
                    "Reconstruction should be different when padding_mode=%s" % padding_mode
                )

    def test_roi(self):
        n_z = n_y = n_x = 256
        n_a = 500
        src_orig_dist = 1000
        orig_det_dist = 50

        volume, cone_data = generate_hollow_cube_cone_sinograms(
            vol_shape=(n_z, n_y, n_x),
            n_angles=n_a,
            src_orig_dist=src_orig_dist,
            orig_det_dist=orig_det_dist,
            apply_filter=False,
            rot_center_shift=10,
        )

        reconstructor_args = [
            cone_data.shape,
            src_orig_dist,
            orig_det_dist,
        ]
        reconstructor_kwargs = {
            "volume_shape": volume.shape,
            "rot_center": (n_x - 1) / 2 + 10,
            # "cuda_options": {"ctx": self.ctx},
        }
        cone_reconstructor_full = ConebeamReconstructor(*reconstructor_args, **reconstructor_kwargs)
        ref = cone_reconstructor_full.reconstruct(cone_data)

        # roi is in the form (start_x, end_x, start_y, end_y)
        for roi in ((20, -20, 10, -10), (0, n_x, 0, n_y), (50, -50, 15, -15)):
            # convert negative indices
            start_x, end_x, start_y, end_y = roi
            if start_y < 0:
                start_y += n_y
            if start_x < 0:
                start_x += n_x

            cone_reconstructor = ConebeamReconstructor(*reconstructor_args, slice_roi=roi, **reconstructor_kwargs)
            rec = cone_reconstructor.reconstruct(cone_data)

            assert np.allclose(rec, ref[:, roi[2] : roi[3], roi[0] : roi[1]]), "Something wrong with roi=%s" % (
                str(roi)
            )

    def test_fdk_preweight(self, caplog):
        """
        Check that nabu's FDK pre-weighting give the same results as astra
        """
        shapes = [
            {"n_z": 256, "n_x": 256, "n_a": 500},
            # {"n_z": 250, "n_x": 340, "n_a": 250}, # Astra reconstruction is incorrect in this case!
        ]
        src_orig_dist = 1000
        orig_det_dist = 50

        rot_centers_from_middle = [0]
        if __do_long_tests__:
            rot_centers_from_middle.extend([10, -15])

        params_list = generate_tests_scenarios({"shape": shapes, "rot_center": rot_centers_from_middle})

        for params in params_list:
            n_z = params["shape"]["n_z"]
            n_x = n_y = params["shape"]["n_x"]
            n_a = params["shape"]["n_a"]
            rc = params["rot_center"]
            volume, cone_data = generate_hollow_cube_cone_sinograms(
                vol_shape=(n_z, n_y, n_x),
                n_angles=n_a,
                src_orig_dist=src_orig_dist,
                orig_det_dist=orig_det_dist,
                apply_filter=False,
                rot_center_shift=rc,
            )

            reconstructor_args = [(n_z, n_a, n_x), src_orig_dist, orig_det_dist]
            reconstructor_kwargs_base = {
                "volume_shape": volume.shape,
                "rot_center": (n_x - 1) / 2 + rc,
                # "cuda_options": {"ctx": self.ctx},
            }
            reconstructor_kwargs_astra = {"padding_mode": "zeros", "extra_options": {"use_astra_fdk": True}}
            reconstructor_kwargs_nabu = {"padding_mode": "zeros", "extra_options": {"use_astra_fdk": False}}
            reconstructor_astra = ConebeamReconstructor(
                *reconstructor_args, **{**reconstructor_kwargs_base, **reconstructor_kwargs_astra}
            )
            assert reconstructor_astra._use_astra_fdk is True, "reconstructor_astra should use native astra FDK"
            reconstructor_nabu = ConebeamReconstructor(
                *reconstructor_args, **{**reconstructor_kwargs_base, **reconstructor_kwargs_nabu}
            )
            ref = reconstructor_astra.reconstruct(cone_data)
            res = reconstructor_nabu.reconstruct(cone_data)

            reconstructor_kwargs_nabu = {"padding_mode": "edges", "extra_options": {"use_astra_fdk": False}}
            cb_ep = ConebeamReconstructor(
                *reconstructor_args, **{**reconstructor_kwargs_base, **reconstructor_kwargs_nabu}
            )
            res_ep = cb_ep.reconstruct(cone_data)  # noqa: F841

            assert np.max(np.abs(res - ref)) < 2e-3, "Wrong FDK results for parameters: %s" % (str(params))

            # Test with edges padding - only nabu can do that
            reconstructor_kwargs_nabu["padding_mode"] = "edges"
            reconstructor_nabu = ConebeamReconstructor(
                *reconstructor_args, **{**reconstructor_kwargs_base, **reconstructor_kwargs_nabu}
            )
            reconstructor_nabu.reconstruct(cone_data)
            # result is slightly different than "res" in the borders, which is expected
            # it would be good to test it as well, but it's outside of the scope of this test

            with caplog.at_level(logging.WARNING):
                reconstructor_kwargs_nabu = {"padding_mode": "edges", "extra_options": {"use_astra_fdk": True}}
                ConebeamReconstructor(*reconstructor_args, **{**reconstructor_kwargs_base, **reconstructor_kwargs_nabu})
                assert "cannot use native astra FDK" in caplog.text

    def test_reconstruct_noncontiguous_data(self):
        n_z = 206
        n_y = n_x = 256
        n_a = 500
        src_orig_dist = 1000
        orig_det_dist = 50

        volume, cone_data = generate_hollow_cube_cone_sinograms(
            vol_shape=(n_z, n_y, n_x),
            n_angles=n_a,
            src_orig_dist=src_orig_dist,
            orig_det_dist=orig_det_dist,
            apply_filter=False,
            rot_center_shift=10,
        )
        cone_reconstructor = ConebeamReconstructor(
            cone_data.shape,
            src_orig_dist,
            orig_det_dist,
            volume_shape=volume.shape,
            rot_center=(n_x - 1) / 2 + 10,
            # cuda_options={"ctx": self.ctx},
            extra_options={"use_astra_fdk": False},
        )
        ref = cone_reconstructor.reconstruct(cone_data)

        radios = cone_reconstructor.cuda.allocate_array("_radios", (n_a, n_z, n_x))
        for i in range(n_a):
            radios[i].set(cone_data[:, i, :])

        sinos_discontig = radios.transpose((1, 0, 2))
        assert cone_reconstructor.cuda.is_contiguous(sinos_discontig) is False
        res = cone_reconstructor.reconstruct(sinos_discontig)
        assert np.allclose(res, ref), "Reconstructing non-contiguous data failed"

    def test_cone_clip_circle(self):
        n_z = 206
        n_y = n_x = 256
        n_a = 500
        src_orig_dist = 1000
        orig_det_dist = 50

        volume, cone_data = generate_hollow_cube_cone_sinograms(
            vol_shape=(n_z, n_y, n_x),
            n_angles=n_a,
            src_orig_dist=src_orig_dist,
            orig_det_dist=orig_det_dist,
            apply_filter=False,
            rot_center_shift=10,
        )
        init_args = [cone_data.shape, src_orig_dist, orig_det_dist]
        init_kwargs = {
            "volume_shape": volume.shape,
            "rot_center": (n_x - 1) / 2 + 10,
            "extra_options": {"use_astra_fdk": False, "clip_outer_circle": True},
        }

        # for cone_reconstructor_cls in [ConebeamReconstructor, NumpyConebeamReconstructor]:
        for cone_reconstructor_cls in [NumpyConebeamReconstructor]:
            for out_circle_value in [0, np.nan]:
                init_kwargs["extra_options"]["outer_circle_value"] = out_circle_value
                cone_reconstructor = cone_reconstructor_cls(*init_args, **init_kwargs)
                rec = cone_reconstructor.reconstruct(cone_data)
                for i in range(rec.shape[0]):
                    err_msg = f"Something wrong with clip_circle for {cone_reconstructor.__class__.__name__} with outer value {out_circle_value} at slice number {i}"
                    assert np.allclose(clip_circle(rec[i], out_value=out_circle_value), rec[i], equal_nan=True), err_msg

    def _test_numpy_cone(self, cor_shift, padding_mode):
        d1 = 1000
        d2 = 10

        rot_center = None
        neg_cor_shift = None
        cube, sinos = generate_hollow_cube_cone_sinograms((256, 256, 200), 200, d1, d2, rot_center_shift=cor_shift)

        if cor_shift is not None:
            rot_center = (sinos.shape[-1] - 1) / 2 + cor_shift
            neg_cor_shift = -cor_shift
        rec0 = astra_cone_beam_reconstruction(
            sinos, np.linspace(0, 2 * np.pi, sinos.shape[1], True), d1, d2, cor_shift=neg_cor_shift
        )

        cone_reconstructor = NumpyConebeamReconstructor(
            sinos.shape, d1, d2, rot_center=rot_center, padding_mode=padding_mode
        )
        rec = cone_reconstructor.reconstruct(sinos)

        err_profile = np.max(np.abs(rec - rec0), axis=(1, 2))
        tol = 2e-3

        if padding_mode not in ["zeros", "constant"]:
            # Astra does not support natively padding mode other than zeros
            # Here we ignore the region close to the edges, since edges-padding gives a different result
            err_profile = np.max(np.abs(rec[:, 50:-50, 50:-50] - rec0[:, 50:-50, 50:-50]), axis=(1, 2))[50:-50]
            tol = 0.15

        assert (
            np.max(err_profile) < tol
        ), f"NumpyConebeamReconstructor: FDK reconstruction failed for cor_shift={cor_shift}, padding_mode={padding_mode}"

    def test_numpy_cone(self):
        test_cases = {
            "cor_shift": [None, 6.5],
            "padding_mode": ["zeros", "edges"],
        }
        params_list = generate_tests_scenarios(test_cases)

        for params in params_list:
            self._test_numpy_cone(params["cor_shift"], params["padding_mode"])


def generate_hollow_cube_cone_sinograms(
    vol_shape,
    n_angles,
    src_orig_dist,
    orig_det_dist,
    prj_width=None,
    apply_filter=True,
    rot_center_shift=None,
):
    # Adapted from Astra toolbox python samples

    n_z, n_y, n_x = vol_shape
    vol_geom = astra.create_vol_geom(n_y, n_x, n_z)

    prj_width = prj_width or n_x
    # prj_height = n_z
    angles = np.linspace(0, 2 * np.pi, n_angles, True)

    proj_geom = astra.create_proj_geom("cone", 1.0, 1.0, n_z, prj_width, angles, src_orig_dist, orig_det_dist)
    if rot_center_shift is not None:
        proj_geom = astra.geom_postalignment(proj_geom, (-rot_center_shift, 0))
    # magnification = 1 + orig_det_dist / src_orig_dist

    # hollow cube
    cube = np.zeros(astra.geom_size(vol_geom), dtype="f")

    d = int(min(n_x, n_y) / 2 * (1 - np.sqrt(2) / 2))
    cube[20:-20, d:-d, d:-d] = 1
    cube[40:-40, d + 20 : -(d + 20), d + 20 : -(d + 20)] = 0

    # d = int(min(n_x, n_y) / 2 * (1 - np.sqrt(2) / 2) * magnification)
    # d1 = d + 10
    # d2 = d + 20
    # cube[40:-40, d1:-d1, d1:-d1] = 1
    # cube[60:-60, d2 : -d2, d2 : -d2] = 0

    # High-frequencies yield cannot be accurately retrieved
    if apply_filter:
        cube = gaussian_filter(cube, (1.0, 1.0, 1.0))

    proj_id, proj_data = astra.create_sino3d_gpu(cube, proj_geom, vol_geom)
    astra.data3d.delete(proj_id)  # (n_z, n_angles, n_x)

    return cube, proj_data


def astra_cone_beam_reconstruction(
    cone_data, angles, src_orig_dist, orig_det_dist, demagnify_volume=False, cor_shift=None
):
    """
    Handy (but data-inefficient) function to reconstruct data from cone-beam geometry
    """

    n_z, n_a, n_x = cone_data.shape

    proj_geom = astra.create_proj_geom("cone", 1.0, 1.0, n_z, n_x, angles, src_orig_dist, orig_det_dist)
    if cor_shift is not None:
        proj_geom = astra.geom_postalignment(proj_geom, (cor_shift, 0))
    sino_id = astra.data3d.create("-sino", proj_geom, data=cone_data)

    m = 1 + orig_det_dist / src_orig_dist if demagnify_volume else 1.0
    n_z_vol, n_y_vol, n_x_vol = int(n_z / m), int(n_x / m), int(n_x / m)
    vol_geom = astra.create_vol_geom(n_y_vol, n_x_vol, n_z_vol)
    rec_id = astra.data3d.create("-vol", vol_geom)

    cfg = astra.astra_dict("FDK_CUDA")
    cfg["ReconstructionDataId"] = rec_id
    cfg["ProjectionDataId"] = sino_id
    alg_id = astra.algorithm.create(cfg)

    astra.algorithm.run(alg_id)

    rec = astra.data3d.get(rec_id)

    astra.data3d.delete(sino_id)
    astra.data3d.delete(rec_id)
    astra.algorithm.delete(alg_id)

    return rec
