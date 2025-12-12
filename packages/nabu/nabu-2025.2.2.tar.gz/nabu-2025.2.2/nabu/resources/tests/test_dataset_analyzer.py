import pytest
from nabu.testutils import get_dummy_nxtomo_info
from nabu.resources.dataset_analyzer import analyze_dataset


@pytest.fixture(scope="class")
def bootstrap_nx(request):
    cls = request.cls
    cls.nx_fname, cls.data_desc, cls.image_key, cls.projs_vals, cls.darks_vals, cls.flats1_vals, cls.flats2_vals = (
        get_dummy_nxtomo_info()
    )


@pytest.mark.usefixtures("bootstrap_nx")
class TestNXDataset:

    def test_exclude_projs_angular_range(self):
        dataset_info_with_all_projs = analyze_dataset(self.nx_fname)

        # Test exclude angular range - angles min and max in degrees
        angular_ranges_to_test = [(0, 15), (5, 6), (50, 58.5)]
        for angular_range in angular_ranges_to_test:
            angle_min, angle_max = angular_range
            dataset_info = analyze_dataset(
                self.nx_fname,
                extra_options={"exclude_projections": {"type": "angular_range", "range": [angle_min, angle_max]}},
            )
            excluded_projs_indices = dataset_info.get_excluded_projections_indices()
            # Check that get_excluded_projections_indices() angles are correct
            for excluded_proj_index in excluded_projs_indices:
                frame_angle_deg = dataset_info.dataset_scanner.frames[excluded_proj_index].rotation_angle
                assert angle_min <= frame_angle_deg <= angle_max

            assert set(dataset_info_with_all_projs.projections.keys()) - set(dataset_info.projections.keys()) == set(
                excluded_projs_indices
            )
