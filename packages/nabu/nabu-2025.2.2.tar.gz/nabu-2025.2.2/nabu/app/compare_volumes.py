from math import ceil
from posixpath import join
import numpy as np
from tomoscan.io import HDF5File
from .cli_configs import CompareVolumesConfig
from ..utils import clip_circle
from .utils import parse_params_values
from ..io.utils import get_first_hdf5_entry, hdf5_entry_exists
from ..io.reader import get_hdf5_dataset_shape


def idx_1d_to_3d(idx, shape):
    nz, ny, nx = shape
    x = idx % nx
    idx2 = (idx - x) // nx
    y = idx2 % ny
    z = (idx2 - y) // ny
    return (z, y, x)


def compare_volumes(fname1, fname2, h5_path, chunk_size, do_stats, stop_at_thresh, clip_outer_circle=False):
    result = None
    f1 = HDF5File(fname1, "r")
    f2 = HDF5File(fname2, "r")
    try:
        # Check that data is in the provided hdf5 path
        for fname in [fname1, fname2]:
            if not hdf5_entry_exists(fname, h5_path):
                result = "File %s do not has data in %s" % (fname, h5_path)
                return
        # Check shapes
        shp1 = get_hdf5_dataset_shape(fname1, h5_path)
        shp2 = get_hdf5_dataset_shape(fname2, h5_path)
        if shp1 != shp2:
            result = "Volumes do not have the same shape: %s vs %s" % (shp1, shp2)
            return
        # Compare volumes
        n_steps = ceil(shp1[0] / chunk_size)
        for i in range(n_steps):
            start = i * chunk_size
            end = min((i + 1) * chunk_size, shp1[0])
            data1 = f1[h5_path][start:end, :, :]
            data2 = f2[h5_path][start:end, :, :]
            abs_diff = np.abs(data1 - data2)
            if clip_outer_circle:
                for j in range(abs_diff.shape[0]):
                    abs_diff[j] = clip_circle(abs_diff[j], radius=0.9 * min(abs_diff.shape[1:]))
            coord_argmax = idx_1d_to_3d(np.argmax(abs_diff), data1.shape)
            if do_stats:
                mean = np.mean(abs_diff)
                std = np.std(abs_diff)
                maxabs = np.max(abs_diff)
                print("Chunk %d: mean = %e std = %e max = %e" % (i, mean, std, maxabs))
            if stop_at_thresh is not None and abs_diff[coord_argmax] > stop_at_thresh:
                coord_argmax_absolute = (start + coord_argmax[0],) + coord_argmax[1:]
                result = "abs_diff[%s] = %e" % (coord_argmax_absolute, abs_diff[coord_argmax])
                return
    except Exception as exc:
        result = "Error: %s" % (str(exc))
        raise
    finally:
        f1.close()
        f2.close()
    return result


def compare_volumes_cli():
    args = parse_params_values(
        CompareVolumesConfig, parser_description="A command-line utility for comparing two volumes."
    )

    fname1 = args["volume1"]
    fname2 = args["volume2"]
    h5_path = args["hdf5_path"]
    if h5_path == "":
        entry = args["entry"].strip() or None
        if entry is None:
            entry = get_first_hdf5_entry(fname1)
        h5_path = join(entry, "reconstruction/results/data")
    do_stats = bool(args["statistics"])
    chunk_size = args["chunk_size"]
    stop_at_thresh = args["stop_at"] or None
    if stop_at_thresh is not None:
        stop_at_thresh = float(stop_at_thresh)

    res = compare_volumes(fname1, fname2, h5_path, chunk_size, do_stats, stop_at_thresh)
    if res is not None:
        print(res)

    return 0


if __name__ == "__main__":
    compare_volumes_cli()
