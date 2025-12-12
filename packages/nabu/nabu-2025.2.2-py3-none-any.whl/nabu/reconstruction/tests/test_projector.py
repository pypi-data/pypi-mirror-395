import numpy as np
import pytest
from nabu.testutils import get_data
from nabu.cuda.utils import __has_cupy__

if __has_cupy__:
    from nabu.reconstruction.projection import Projector
try:
    import astra

    __has_astra__ = True
except ImportError:
    __has_astra__ = False


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    cls.image = get_data("brain_phantom.npz")["data"]
    cls.sino_ref = get_data("mri_sino500.npz")["data"]
    cls.n_angles, cls.dwidth = cls.sino_ref.shape
    cls.rtol = 1e-3
    if __has_cupy__:
        ...


@pytest.mark.skipif(not (__has_cupy__), reason="Need cupy for this test")
@pytest.mark.usefixtures("bootstrap")
class TestProjection:
    def check_result(self, img1, img2, err_msg):
        max_diff = np.max(np.abs(img1 - img2))
        assert max_diff / img1.max() < self.rtol, err_msg + " : max diff = %.3e" % max_diff

    def test_proj_simple(self):
        P = Projector(self.image.shape, self.n_angles)
        res = P(self.image)
        self.check_result(res, self.sino_ref, "Something wrong with simple projection")

    def test_input_output_kinds(self):
        P = Projector(self.image.shape, self.n_angles)

        # input on GPU, output on CPU
        d_img = P.cuda_processing.to_device("d_img", self.image)
        res = P(d_img)
        self.check_result(res, self.sino_ref, "Something wrong: input GPU, output CPU")

        # input on CPU, output on GPU
        out = P.cuda_processing.allocate_array("out", P.sino_shape, dtype="f")
        res = P(self.image, output=out)
        self.check_result(out.get(), self.sino_ref, "Something wrong: input CPU, output GPU")

        # input and output on GPU
        out.fill(0)
        P(d_img, output=out)
        self.check_result(out.get(), self.sino_ref, "Something wrong: input GPU, output GPU")

    def test_odd_size(self):
        image = self.image[:511, :]
        P = Projector(image.shape, self.n_angles - 1)
        res = P(image)  # noqa: F841
        # TODO check

    @pytest.mark.skipif(not (__has_astra__), reason="Need astra-toolbox for this test")
    def test_against_astra(self):
        def proj_astra(img, angles, rot_center=None):
            vol_geom = astra.create_vol_geom(img.shape)
            if np.isscalar(angles):
                angles = np.linspace(0, np.pi, angles, False)
            proj_geom = astra.create_proj_geom("parallel", 1.0, img.shape[-1], angles)
            if rot_center is not None:
                cor_shift = (img.shape[-1] - 1) / 2.0 - rot_center
                proj_geom = astra.geom_postalignment(proj_geom, cor_shift)

            projector_id = astra.create_projector("cuda", proj_geom, vol_geom)
            sinogram_id, sinogram = astra.create_sino(img, projector_id)

            astra.data2d.delete(sinogram_id)
            astra.projector.delete(projector_id)
            return sinogram

        # Center of rotation to test
        cors = [None, 255.5, 256, 260, 270.2, 300, 150]

        for cor in cors:
            res_astra = proj_astra(self.image, 500, rot_center=cor)
            res_nabu = Projector(self.image.shape, 500, rot_center=cor).projection(self.image)
            self.check_result(res_nabu, res_astra, "Projection with CoR = %s" % str(cor))
