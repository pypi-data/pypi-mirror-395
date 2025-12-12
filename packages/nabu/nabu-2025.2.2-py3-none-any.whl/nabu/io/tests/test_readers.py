from math import ceil
from tempfile import TemporaryDirectory
from tomoscan.io import HDF5File
import pytest
import numpy as np
from nxtomo.application.nxtomo import ImageKey
from tomoscan.esrf import EDFVolume
from nabu.pipeline.reader import NXTomoReaderBinning
from nabu.testutils import utilstest, __do_long_tests__, get_file, get_dummy_nxtomo_info
from nabu.utils import indices_to_slices, merge_slices
from nabu.io.reader import EDFStackReader, NXTomoReader, NXDarksFlats


@pytest.fixture(scope="class")
def bootstrap_nx_reader(request):
    cls = request.cls
    cls.nx_fname, cls.data_desc, cls.image_key, cls.projs_vals, cls.darks_vals, cls.flats1_vals, cls.flats2_vals = (
        get_dummy_nxtomo_info()
    )

    yield
    # teardown


@pytest.mark.usefixtures("bootstrap_nx_reader")
class TestNXReader:
    def test_incorrect_path(self):
        with pytest.raises(FileNotFoundError):
            reader = NXTomoReader("/invalid/path")
        with pytest.raises(KeyError):
            reader = NXTomoReader(self.nx_fname, "/bad/data/path")  # noqa: F841

    def test_simple_reads(self):
        """
        Test NXTomoReader with simplest settings
        """
        reader1 = NXTomoReader(self.nx_fname)
        data1 = reader1.load_data()
        assert data1.shape == (self.data_desc.n_projs,) + self.data_desc.frame_shape
        assert np.allclose(data1[:, 0, 0], self.projs_vals)

    def test_image_key(self):
        """
        Test the data selection using "image_key".
        """
        reader_projs = NXTomoReader(self.nx_fname, image_key=ImageKey.PROJECTION.value)
        data = reader_projs.load_data()
        assert np.allclose(data[:, 0, 0], self.projs_vals)

        reader_darks = NXTomoReader(self.nx_fname, image_key=ImageKey.DARK_FIELD.value)
        data_darks = reader_darks.load_data()
        assert np.allclose(data_darks[:, 0, 0], self.darks_vals)

        reader_flats = NXTomoReader(self.nx_fname, image_key=ImageKey.FLAT_FIELD.value)
        data_flats = reader_flats.load_data()
        assert np.allclose(data_flats[:, 0, 0], np.concatenate([self.flats1_vals, self.flats2_vals]))

    def test_data_buffer_and_subregion(self):
        """
        Test the "data_buffer" and "sub_region" parameters
        """
        data_desc = self.data_desc

        def _check_correct_shape_succeeds(shape, sub_region, test_description=""):
            err_msg = "Something wrong with the following test:" + test_description
            data_buffer = np.zeros(shape, dtype="f")
            reader1 = NXTomoReader(self.nx_fname, sub_region=sub_region)
            data1 = reader1.load_data(output=data_buffer)
            assert id(data1) == id(data_buffer), err_msg
            reader2 = NXTomoReader(self.nx_fname, sub_region=sub_region)
            data2 = reader2.load_data()
            assert np.allclose(data1, data2), err_msg

        test_cases = [
            {
                "description": "In the projections, read everything into the provided data buffer",
                "sub_region": None,
                "correct_shape": (data_desc.n_projs,) + data_desc.frame_shape,
                "wrong_shapes": [
                    (data_desc.n_projs - 1,) + data_desc.frame_shape,
                    (data_desc.n_projs - 1,) + (999, 998),
                    (data_desc.n_projs,) + (999, 998),
                ],
            },
            {
                "description": "In the projections, select a subset along dimension 0 (i.e take only several full frames). The correct output shape is: data_total[image_key==0][slice(10, 30)].shape",
                "sub_region": slice(10, 30),
                "correct_shape": (20,) + data_desc.frame_shape,
                "wrong_shapes": [
                    (data_desc.n_projs,) + data_desc.frame_shape,
                    (19,) + data_desc.frame_shape,
                ],
            },
            {
                "description": "In the projections, read several rows of all images, i.e extract several sinograms. The correct output shape is: data_total[image_key==0][:, slice(start_z, end_z), :].shape",
                "sub_region": (None, slice(3, 7), None),
                "correct_shape": (data_desc.n_projs, 4, data_desc.frame_shape[-1]),
                "wrong_shapes": [],
            },
        ]

        for test_case in test_cases:
            for wrong_shape in test_case["wrong_shapes"]:
                with pytest.raises(ValueError):  # noqa: PT012
                    data_buffer_wrong_shape = np.zeros(wrong_shape, dtype="f")
                    reader = NXTomoReader(
                        self.nx_fname,
                        sub_region=test_case["sub_region"],
                    )
                    reader.load_data(output=data_buffer_wrong_shape)
            _check_correct_shape_succeeds(test_case["correct_shape"], test_case["sub_region"], test_case["description"])

    def test_subregion_and_subsampling(self):
        data_desc = self.data_desc
        test_cases = [
            {
                # Read one full image out of two in all projections
                "sub_region": (slice(None, None, 2), None, None),
                "expected_shape": (self.projs_vals[::2].size,) + data_desc.frame_shape,
                "expected_values": self.projs_vals[::2],
            },
            {
                # Read one image fragment (several rows) out of two in all projections
                "sub_region": (slice(None, None, 2), slice(5, 8), None),
                "expected_shape": (self.projs_vals[::2].size, 3, data_desc.frame_shape[-1]),
                "expected_values": self.projs_vals[::2],
            },
        ]

        for test_case in test_cases:
            reader = NXTomoReader(self.nx_fname, sub_region=test_case["sub_region"])
            data = reader.load_data()
            assert data.shape == test_case["expected_shape"]
            assert np.allclose(data[:, 0, 0], test_case["expected_values"])

    def test_reading_with_binning_(self):
        from nabu.pipeline.reader import NXTomoReaderBinning

        reader_with_binning = NXTomoReaderBinning((2, 2), self.nx_fname)
        data = reader_with_binning.load_data()
        assert data.shape == (self.data_desc.n_projs,) + tuple(n // 2 for n in self.data_desc.frame_shape)

    def test_reading_with_distortion_correction(self):
        from nabu.io.detector_distortion import DetectorDistortionBase
        from nabu.pipeline.reader import NXTomoReaderDistortionCorrection

        data_desc = self.data_desc

        # (start_x, end_x, start_y, end_y)
        sub_region_xy = (None, None, 1, 6)

        distortion_corrector = DetectorDistortionBase(detector_full_shape_vh=data_desc.frame_shape)
        distortion_corrector.set_sub_region_transformation(target_sub_region=sub_region_xy)
        # adapted_subregion = distortion_corrector.get_adapted_subregion(sub_region_xy)
        sub_region = (slice(None, None), slice(*sub_region_xy[2:]), slice(*sub_region_xy[:2]))

        reader_distortion_corr = NXTomoReaderDistortionCorrection(
            distortion_corrector,
            self.nx_fname,
            sub_region=sub_region,
        )

        reader_distortion_corr.load_data()

    @pytest.mark.skipif(not (__do_long_tests__), reason="Need NABU_LONG_TESTS=1")
    def test_other_load_patterns(self):
        """
        Other data read patterns that are sometimes used by ChunkedPipeline
        Test cases already done in check_correct_shape_succeeds():
            - Read all frames in a provided buffer
            - Read a subset of all (full) projections
            - Read several rows of all projections (extract sinograms)
        """
        data_desc = self.data_desc

        test_cases = [
            {
                "description": "Select a subset along all dimensions. The correct output shape is data_total[image_key==0][slice_dim0, slice_dim1, slice_dim2].shape",
                "sub_region": (slice(10, 72, 2), slice(4, None), slice(2, 8)),
                "expected_shape": (31, 7, 6),
                "expected_values": self.projs_vals[slice(10, 72, 2)],
            },
            {
                "description": "Select several rows in all images (i.e extract sinograms), with binning",
                "sub_region": (slice(None, None), slice(3, 7), slice(None, None)),
                "binning": (2, 2),
                "expected_shape": (data_desc.n_projs, 4 // 2, data_desc.frame_shape[-1] // 2),
                "expected_values": self.projs_vals[:],
            },
            {
                "description": "Extract sinograms with binning + subsampling",
                "sub_region": (slice(None, None, 2), slice(1, 8), slice(None, None)),
                "binning": (2, 2),
                "expected_shape": (ceil(data_desc.n_projs / 2), 7 // 2, data_desc.frame_shape[-1] // 2),
                "expected_values": self.projs_vals[::2],
            },
        ]

        for test_case in test_cases:
            binning = test_case.get("binning", None)
            reader_cls = NXTomoReader
            init_args = [self.nx_fname]
            init_kwargs = {"sub_region": test_case["sub_region"]}
            if binning is not None:
                reader_cls = NXTomoReaderBinning
                init_args = [binning] + init_args
            reader = reader_cls(*init_args, **init_kwargs)
            data = reader.load_data()
            err_msg = "Something wrong with test: " + test_case["description"]
            assert data.shape == test_case["expected_shape"], err_msg
            assert np.allclose(data[:, 0, 0], test_case["expected_values"]), err_msg

    def test_load_exclude_projections(self):
        n_z, n_x = self.data_desc.frame_shape
        # projs_idx = np.where(self.image_key == 0)[0]
        projs_idx = np.arange(self.data_desc.n_projs, dtype=np.int64)
        excluded_projs_idx_1 = projs_idx[10:20]
        excluded_projs_idx_2 = np.concatenate([projs_idx[10:14], projs_idx[50:57]])

        set_to_nparray = lambda x: np.array(sorted(x))

        projs_idx1 = set_to_nparray(set(projs_idx) - set(excluded_projs_idx_1))
        projs_idx2 = set_to_nparray(set(projs_idx) - set(excluded_projs_idx_2))

        sub_regions_to_test = (
            (projs_idx1, None, None),
            (projs_idx1, slice(0, n_z // 2), None),
            (projs_idx2, None, None),
            (projs_idx2, slice(3, n_z // 2), None),
        )
        for sub_region in sub_regions_to_test:
            reader = NXTomoReader(self.nx_fname, sub_region=sub_region)
            data = reader.load_data()
            assert np.allclose(data[:, 0, 0], self.projs_vals[sub_region[0]])


@pytest.fixture(scope="class")
def bootstrap_edf_reader(request):
    cls = request.cls

    test_dir = utilstest.data_home
    cls._tmpdir = TemporaryDirectory(prefix="test_edf_stack_", dir=test_dir)
    cls.edf_dir = cls._tmpdir.name
    cls.n_projs = 100
    cls.frame_shape = (11, 12)
    cls.projs_vals = np.arange(cls.n_projs, dtype=np.uint16) + 10

    edf_vol = EDFVolume(folder=cls.edf_dir, volume_basename="edf_stack", overwrite=True)
    data_shape = (cls.n_projs,) + cls.frame_shape
    edf_vol.data = np.ones(data_shape, dtype=np.uint16) * cls.projs_vals.reshape(cls.n_projs, 1, 1)
    edf_vol.save_data()
    cls.filenames = list(edf_vol.browse_data_files())

    yield
    cls._tmpdir.cleanup()


@pytest.mark.usefixtures("bootstrap_edf_reader")
class TestEDFReader:
    def test_read_all_frames(self):
        """
        Simple test, read all the frames
        """
        reader = EDFStackReader(self.filenames)
        data = reader.load_data()
        expected_shape = (self.n_projs,) + self.frame_shape
        assert data.shape == expected_shape
        assert np.allclose(data[:, 0, 0], self.projs_vals)

        buffer_correct = np.zeros(expected_shape, dtype=np.float32)
        reader.load_data(output=buffer_correct)

        buffer_incorrect_1 = np.zeros((99, 11, 12), dtype=np.float32)
        with pytest.raises(ValueError):
            reader.load_data(output=buffer_incorrect_1)

        buffer_incorrect_2 = np.zeros((100, 11, 12), dtype=np.uint16)
        with pytest.raises(ValueError):
            reader.load_data(output=buffer_incorrect_2)

    def test_subregions_1(self):
        test_cases = [
            {
                "name": "read a handful of full frames",
                "sub_region": (slice(0, 48), slice(None, None), slice(None, None)),
                "expected_shape": (48,) + self.frame_shape,
                "expected_values": self.projs_vals[:48],
            },
            {
                "name": "read several lines of all frames (i.e extract a singoram)",
                "sub_region": (slice(None, None), slice(0, 6), slice(None, None)),
                "expected_shape": (self.n_projs, 6, self.frame_shape[-1]),
                "expected_values": self.projs_vals,
            },
            {
                "name": "read several lines of all frames (i.e extract a singoram), and a X-ROI",
                "sub_region": (slice(None, None), slice(3, 7), slice(2, 5)),
                "expected_shape": (self.n_projs, 4, 3),
                "expected_values": self.projs_vals,
            },
            {
                "name": "read several lines of all frames (i.e extract a singoram), with angular subsampling",
                "sub_region": (slice(None, None, 2), slice(3, 7), slice(2, 5)),
                "expected_shape": (ceil(self.n_projs / 2), 4, 3),
                "expected_values": self.projs_vals[::2],
            },
        ]
        for test_case in test_cases:
            reader = EDFStackReader(self.filenames, sub_region=test_case["sub_region"])
            data = reader.load_data()
            err_msg = "Something wrong with test: %s" % (test_case["name"])
            assert data.shape == test_case["expected_shape"], err_msg
            assert np.allclose(data[:, 0, 0], test_case["expected_values"]), err_msg

    @pytest.mark.skipif(not (__do_long_tests__), reason="Need NABU_LONG_TESTS=1")
    def test_reading_with_binning(self):
        from nabu.pipeline.reader import EDFStackReaderBinning

        reader_with_binning = EDFStackReaderBinning((2, 2), self.filenames)
        data = reader_with_binning.load_data()
        assert data.shape == (self.n_projs,) + tuple(n // 2 for n in self.frame_shape)

    @pytest.mark.skipif(not (__do_long_tests__), reason="Need NABU_LONG_TESTS=1")
    def test_reading_with_distortion_correction(self):
        from nabu.io.detector_distortion import DetectorDistortionBase
        from nabu.pipeline.reader import EDFStackReaderDistortionCorrection

        # (start_x, end_x, start_y, end_y)
        sub_region_xy = (None, None, 1, 6)

        distortion_corrector = DetectorDistortionBase(detector_full_shape_vh=self.frame_shape)
        distortion_corrector.set_sub_region_transformation(target_sub_region=sub_region_xy)
        # adapted_subregion = distortion_corrector.get_adapted_subregion(sub_region_xy)
        sub_region = (slice(None, None), slice(*sub_region_xy[2:]), slice(*sub_region_xy[:2]))

        reader_distortion_corr = EDFStackReaderDistortionCorrection(
            distortion_corrector,
            self.filenames,
            sub_region=sub_region,
        )

        reader_distortion_corr.load_data()


def test_indices_to_slices():
    slices1 = [slice(0, 4)]
    slices2 = [slice(11, 16)]
    slices3 = [slice(3, 5), slice(8, 20)]
    slices4 = [slice(2, 7), slice(18, 28), slice(182, 845)]
    idx = np.arange(1000)
    for slices in [slices1, slices2, slices3, slices4]:
        indices = np.hstack([idx[sl] for sl in slices])
        slices_calculated = indices_to_slices(indices)
        assert slices_calculated == slices, "Expected indices_to_slices() to return %s, but got %s" % (
            str(slices),
            str(slices_calculated),
        )


def test_merge_slices():
    idx = np.arange(10000)
    rnd = lambda x: np.random.randint(1, high=x)

    n_tests = 10
    for i in range(n_tests):
        start1 = rnd(1000)
        stop1 = start1 + rnd(1000)
        start2 = rnd(1000)
        stop2 = start2 + rnd(1000)
        step1 = rnd(4)
        step2 = rnd(4)
        slice1 = slice(start1, stop1, step1)
        slice2 = slice(start2, stop2, step2)

        assert np.allclose(idx[slice1][slice2], idx[merge_slices(slice1, slice2)])


@pytest.fixture(scope="class")
def bootstrap_nxdkrf(request):
    cls = request.cls

    cls.nx_file_path = get_file("bamboo_reduced.nx")

    yield
    # teardown


@pytest.mark.usefixtures("bootstrap_nxdkrf")
class TestDKRFReader:
    def test_darks(self):
        dkrf_reader = NXDarksFlats(self.nx_file_path)
        darks = dkrf_reader.get_raw_darks(as_multiple_array=True)
        reduced_darks = dkrf_reader.get_reduced_darks(method="mean")

        actual_darks = []
        with HDF5File(self.nx_file_path, "r") as f:
            actual_darks.append(f["entry0000/data/data"][slice(0, 1)])

        assert len(darks) == len(actual_darks)

        for i in range(len(darks)):
            assert np.allclose(darks[i], actual_darks[i])
            actual_reduced_darks = np.mean(actual_darks[i], axis=0)
            assert np.allclose(reduced_darks[i], actual_reduced_darks)

        assert np.allclose(list(dkrf_reader.get_reduced_darks(as_dict=True).keys()), [0])

    def test_flats(self):
        dkrf_reader = NXDarksFlats(self.nx_file_path)
        flats = dkrf_reader.get_raw_flats(as_multiple_array=True)
        reduced_flats = dkrf_reader.get_reduced_flats(method="median")

        actual_flats = []
        with HDF5File(self.nx_file_path, "r") as f:
            actual_flats.append(f["entry0000/data/data"][slice(1, 25 + 1)])
            actual_flats.append(f["entry0000/data/data"][slice(526, 550 + 1)])

        assert len(flats) == len(actual_flats)
        for i in range(len(flats)):
            assert np.allclose(flats[i], actual_flats[i])
            actual_reduced_flats = np.median(actual_flats[i], axis=0)
            assert np.allclose(reduced_flats[i], actual_reduced_flats)

        assert np.allclose(list(dkrf_reader.get_reduced_flats(as_dict=True).keys()), [1, 526])
