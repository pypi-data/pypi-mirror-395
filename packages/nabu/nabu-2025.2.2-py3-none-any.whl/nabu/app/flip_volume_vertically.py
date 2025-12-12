import os
from math import ceil
import tempfile
from warnings import warn
import numpy as np
from tomoscan.esrf.volume import TIFFVolume, JP2KVolume, MultiTIFFVolume, RawVolume, HDF5Volume, EDFVolume
from tomoscan.esrf.volume.singleframebase import VolumeSingleFrameBase
from tomoscan.io import HDF5File
from ..utils import check_supported
from ..resources.utils import get_available_ram_GB
from ..io.utils import get_first_hdf5_entry
from .utils import parse_params_values
from .cli_configs import FlipVolumeVerticallyConfig


def _infer_h5_data_path(file_path):
    entry = get_first_hdf5_entry(file_path)
    with HDF5File(file_path, "r") as f:
        if "reconstruction" in f[entry]:
            # Assume the file was created by nabu
            res = f"{entry}/reconstruction"
        else:
            # Assume NXTomo file
            res = f"{entry}/instrument/detector/data"
    return res


def get_volume_reader(volume_path, volume_type, file_prefix, h5_data_path=None):
    volume_readers = {
        "tiff3d": MultiTIFFVolume,
        "tiff": TIFFVolume,
        "hdf5": HDF5Volume,
        "h5": HDF5Volume,  # alias
        "edf": EDFVolume,
        "jp2": JP2KVolume,
        "jpeg2000": JP2KVolume,  # alias
        "vol": RawVolume,
        "raw": RawVolume,  # alias
    }
    check_supported(volume_type, list(volume_readers.keys()), "volume type")
    reader_cls = volume_readers[volume_type]

    if issubclass(reader_cls, VolumeSingleFrameBase):
        if file_prefix in [None, ""]:
            raise ValueError(f"Need 'file_prefix' volume type '{volume_type}'")
        reader_init_kwargs = {
            "folder": volume_path,
            "volume_basename": file_prefix,
        }
    else:
        reader_init_kwargs = {"file_path": volume_path}
        if reader_cls == HDF5Volume:
            h5_data_path = h5_data_path or _infer_h5_data_path(volume_path)
            reader_init_kwargs["data_path"] = h5_data_path
    reader_init_kwargs["overwrite"] = True
    reader = reader_cls(**reader_init_kwargs)
    return reader


def flip_singleframe_volume_vertically(volume):
    """
    Flip up<->down the volume for "single-frame" volumes (tiff, edf, jpeg2000)
    """
    files = list(volume.browse_data_files())
    n_files = len(files)
    scheme = volume.data_url.scheme()
    for i in range(n_files // 2):
        data_up = volume.read_file(files[i])
        data_down = volume.read_file(files[n_files - 1 - i])
        volume.save_frame(data_down, files[i], scheme)
        volume.save_frame(data_up, files[n_files - 1 - i], scheme)


def _get_tmpdir_capacity_GB(tmp_dir):
    stat = os.statvfs(tmp_dir)
    tmp_dir_capacity_available_GB = stat.f_frsize * stat.f_bavail / 1e9
    return tmp_dir_capacity_available_GB


def flip_multiframe_volume_vertically(volume, mem_fraction=0.25):
    """
    Flip up<->down the volume for "multi-frame" volumes (hdf5, tiff3d, raw)
    """

    vol_shape = volume.get_volume_shape()
    vol_nbytes_GB = np.prod(vol_shape) * 4 / 1e9  # assume 4 bytes/voxel
    mem_used_GB = mem_fraction * get_available_ram_GB()

    if vol_nbytes_GB < mem_used_GB:
        # We can use the naive approach: load everything in RAM, flip, write
        volume.load_data()
        volume.data = volume.data[::-1, :, :]
        volume.save_data()

    else:
        # Load/write by chunks.
        # Use numpy memory maps as a buffer
        tmp_dir = tempfile.gettempdir()
        tmp_dir_capacity_available_GB = _get_tmpdir_capacity_GB(tmp_dir)
        if tmp_dir_capacity_available_GB < vol_nbytes_GB:
            raise RuntimeError("Not enough RAM nor tmp space to invert the volume with current implementation")
        tmpfile = os.path.join(tmp_dir, os.path.basename(volume.file_path) + ".swp")
        warn(f"Not enough RAM to flip volume in-place, using temporary file {tmpfile}", RuntimeWarning)

        def _get_mmap(mode):
            return np.memmap(
                tmpfile,
                dtype=np.float32,
                mode=mode,
                offset=0,
                shape=vol_shape,
            )

        n_chunks = ceil(vol_nbytes_GB / mem_used_GB)
        chunk_size = vol_shape[0] // n_chunks
        try:
            buffer = _get_mmap("w+")
            for i in range(n_chunks):
                i_start = i * chunk_size
                i_stop = min((i + 1) * chunk_size, vol_shape[0])
                buffer[i_start:i_stop] = volume.load_chunk((slice(i_start, i_stop), slice(None), slice(None)))
            buffer.flush()
            del buffer
            buffer = _get_mmap("r")
            volume.data = buffer[::-1]
            volume.save_data()
        finally:
            os.remove(tmpfile)


def flip_volume_vertically(volume_path, volume_type, file_prefix, h5_data_path=None, mem_fraction=0.25):
    mem_fraction = np.clip(mem_fraction, 0.0, 1.0)
    volume = get_volume_reader(volume_path, volume_type, file_prefix, h5_data_path=h5_data_path)
    if isinstance(volume, VolumeSingleFrameBase):
        flip_singleframe_volume_vertically(volume)
    else:
        flip_multiframe_volume_vertically(volume, mem_fraction=mem_fraction)


def flip_volume_vertically_app():
    args = parse_params_values(FlipVolumeVerticallyConfig, parser_description="Flip a volume upside-down, in-place")
    flip_volume_vertically(args["input"], args["vol_type"].lower(), args["file_prefix"])
    exit(0)
