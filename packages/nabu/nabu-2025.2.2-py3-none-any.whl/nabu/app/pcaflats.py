import sys
import os
import numpy as np
import h5py
from .utils import parse_params_values
from ..utils import is_writeable
from .cli_configs import PCAFlatsConfig
from .. import version
from ..preproc.flatfield import PCAFlatsDecomposer
from ..io.reader import NXDarksFlats


def get_flats_darks_in_nx(filename):
    dfreader = NXDarksFlats(filename)
    darks = np.concatenate([d for d in dfreader.get_raw_darks()], axis=0)
    flats = np.concatenate([f for f in dfreader.get_raw_flats()], axis=0)
    entry = dfreader.flats_reader.data_path.lstrip("/").split("/")[0]
    return flats, darks, entry


def get_flats_darks_from_h5(filename):
    flats = []
    darks = []
    with h5py.File(filename, "r") as f:
        for k, v in f.items():
            if k == "1.1":
                detector_name = decode_bytes(f["1.1/technique/tomoconfig/detector"][()][0])
            else:
                try:
                    image_key = v["technique/image_key"][()]
                except:
                    raise NotImplementedError(
                        "Legacy h5 file format is not handled. The entry of the h5 file should contain a 'technique/image_key' group."
                    )
                if image_key == 2:  # Darks
                    darks.append(v[f"instrument/{detector_name}/data"][()])
                elif image_key == 1:  # Flats
                    flats.append(v[f"instrument/{detector_name}/data"][()])

    flats = np.concatenate([f for f in flats], axis=0)
    darks = np.concatenate([d for d in darks], axis=0)
    return flats, darks, "entry0000"  # TODO this will be problematic on the reconstruction side


def pcaflats_decomposition(
    flats, darks, pcaflats_filename="PCAFlats.h5", overwrite=False, entry="entry0000", nsigma=3.0
):
    """Compute the PCS decomposition of a series of flats and darks, possibly taken from various scans."""
    try:
        decomposer = PCAFlatsDecomposer(flats, darks, nsigma=nsigma)
        decomposer.save_decomposition(pcaflats_filename, overwrite=overwrite, entry=entry)
        success = True
    except:
        success = False
        raise ValueError("An error occured in the PCA deccomposition.")
    return success


def decode_bytes(content):
    if isinstance(content, bytes):
        return content.decode()
    else:
        return content


def main(argv=None):
    """Compute PCA Flats on a series of datasets (h5 or NX)."""
    if argv is None:
        argv = sys.argv[1:]

    args = parse_params_values(
        PCAFlatsConfig,
        parser_description=f"Compute a PCA Decomposition of flats acquired from various datasets..",
        program_version="nabu " + version,
        user_args=argv,
    )

    # Get "where to write".
    if args["output_filename"] is None:
        abspath = os.path.abspath("./PCAFlats.hdf5")
    else:
        abspath = os.path.abspath(args["output_filename"])

    pcaflats_dir = os.path.dirname(abspath)
    pcaflats_filename = os.path.basename(abspath)

    if is_writeable(pcaflats_dir):
        output_path = os.path.join(pcaflats_dir, pcaflats_filename)
    else:
        raise ValueError(f"Output dir {pcaflats_dir} is not writeable.")

    # raise error if file exists and overwrite=False
    if not args["overwrite"] and os.path.exists(output_path):
        raise FileExistsError(f"Output file {output_path} already exists. Use --overwrite to overwrite it.")

    # Collect raw darks and flats
    flats_stack = []
    darks_stack = []

    for dataset in args["datasets"]:
        filename = os.path.basename(dataset)
        kind = filename.split(".")[-1]
        if kind == "nx":
            flats, darks, entry = get_flats_darks_in_nx(dataset)
        elif kind in ("h5", "hdf5"):
            flats, darks, entry = get_flats_darks_from_h5(dataset)

        flats_stack.append(flats)
        darks_stack.append(darks)

    flats = np.concatenate(flats_stack, axis=0)
    darks = np.concatenate(darks_stack, axis=0)

    exit(
        pcaflats_decomposition(
            flats, darks, pcaflats_filename=output_path, overwrite=args["overwrite"], entry=entry, nsigma=args["nsigma"]
        )
    )


if __name__ == "__main__":
    main()
