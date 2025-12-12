import os
import pytest
import numpy
import pint
from tqdm import tqdm

from nabu.stitching.y_stitching import y_stitching
from nabu.stitching.config import PreProcessedYStitchingConfiguration
from nxtomo.application.nxtomo import NXtomo
from nxtomo.nxobject.nxdetector import ImageKey
from tomoscan.esrf.scan.nxtomoscan import NXtomoScan

_ureg = pint.UnitRegistry()


def build_nxtomos(output_dir, flip_lr, flip_ud) -> tuple:
    r"""
    build two nxtomos in output_dir and return the list of NXtomos ready to be stitched
       /\
       |        ______________       ______________
       |       |~           ~~|      |~             |
       |       |~ nxtomo 1  ~~|      |~ nxtomo 0    |
    Z* |       |~ frame     ~~|      |~ frame       |
               |______________|      |______________|
    <-----------------------------------------------
                    90                     40      0
                    y (in acquisition space)
    * ~: represent the overlap area
    Z*: Z in esrf coordinate system (== Y in McStas coordinate system)
    """
    dark_data = numpy.array([0] * 64 * 120, dtype=numpy.float32).reshape((64, 120))
    flat_data = numpy.array([1] * 64 * 120, dtype=numpy.float32).reshape((64, 120))
    normalized_data = numpy.linspace(128, 1024, num=64 * 120, dtype=numpy.float32).reshape((64, 120))
    if flip_lr:
        dark_data = numpy.fliplr(dark_data)
        flat_data = numpy.fliplr(flat_data)
        normalized_data = numpy.fliplr(normalized_data)
    if flip_ud:
        dark_data = numpy.flipud(dark_data)
        flat_data = numpy.flipud(flat_data)
        normalized_data = numpy.flipud(normalized_data)

    raw_data = (normalized_data + dark_data) * (flat_data + dark_data)

    # create raw data
    scans = []
    slices = (slice(0, 80), slice(60, -1))
    frame_y_positions = (40, 90)
    for i_nxtomo, (my_slice, frame_y_position) in enumerate(zip(slices, frame_y_positions)):
        my_raw_data = raw_data[:, my_slice]
        assert my_raw_data.ndim == 2
        my_dark_data = dark_data[:, my_slice]
        assert my_dark_data.ndim == 2
        my_flat_data = flat_data[:, my_slice]
        assert my_flat_data.ndim == 2

        n_projs = 3
        nx_tomo = NXtomo()
        # warning: mapping esrf coordiante system to McStas
        nx_tomo.sample.z_translation = ([0] * (n_projs + 2)) * _ureg.meter
        nx_tomo.sample.x_translation = ([frame_y_position] * (n_projs + 2)) * _ureg.meter
        nx_tomo.sample.y_translation = ([0] * (n_projs + 2)) * _ureg.meter
        nx_tomo.sample.rotation_angle = numpy.linspace(0, 180, num=(n_projs + 2), endpoint=False) * _ureg.degree
        nx_tomo.instrument.detector.image_key_control = (
            ImageKey.DARK_FIELD,
            ImageKey.FLAT_FIELD,
            ImageKey.PROJECTION,
            ImageKey.PROJECTION,
            ImageKey.PROJECTION,
        )
        nx_tomo.instrument.detector.x_pixel_size = 1.0 * _ureg.meter
        nx_tomo.instrument.detector.y_pixel_size = 1.0 * _ureg.meter
        nx_tomo.instrument.detector.distance = 2.3 * _ureg.meter
        nx_tomo.energy = 19.2 * _ureg.keV
        nx_tomo.instrument.detector.data = numpy.stack(
            (
                my_dark_data,
                my_flat_data,
                my_raw_data,
                my_raw_data,
                my_raw_data,
            )
        )

        file_path = os.path.join(output_dir, f"nxtomo_{i_nxtomo}.nx")
        entry = f"entry000{i_nxtomo}"
        nx_tomo.save(file_path=file_path, data_path=entry)
        scans.append(NXtomoScan(scan=file_path, entry=entry))
    return scans, frame_y_positions, normalized_data


@pytest.mark.parametrize("flip_lr", (True, False))
@pytest.mark.parametrize("flip_ud", (True, False))
@pytest.mark.parametrize("progress", (None, "with_tqdm"))
def test_preprocessing_stitching(tmp_path, flip_lr, flip_ud, progress):
    if progress == "with_tqdm":
        progress = tqdm(total=100)

    nxtomo_dir = tmp_path / "nxtomos"
    nxtomo_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    output_file_path = os.path.join(output_dir, "nxtomo.nxs")

    nxtomos, _, normalized_data = build_nxtomos(
        output_dir=nxtomo_dir,
        flip_lr=flip_lr,
        flip_ud=flip_ud,
    )

    configuration = PreProcessedYStitchingConfiguration(
        input_scans=nxtomos,
        axis_0_pos_px=None,
        axis_1_pos_px=None,
        axis_2_pos_px=None,
        output_file_path=output_file_path,
        output_data_path="stitched_volume",
    )

    output_identifier = y_stitching(
        configuration=configuration,
        progress=progress,
    )
    created_nx_tomo = NXtomo().load(
        file_path=output_identifier.file_path,
        data_path=output_identifier.data_path,
        detector_data_as="as_numpy_array",
    )
    assert created_nx_tomo.instrument.detector.data.shape == (
        3,
        64,
        120,
    )  # 3 == number of projections, dark and flat will not be exported when doing the stitching
    # TODO: improve me: the relative tolerance is pretty high. This doesn't comes from the algorithm on itself
    # but more on the numerical calculation and the flat field normalization
    numpy.testing.assert_allclose(normalized_data, created_nx_tomo.instrument.detector.data[0], rtol=0.06)
