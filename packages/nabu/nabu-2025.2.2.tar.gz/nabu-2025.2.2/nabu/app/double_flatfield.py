import numpy as np
from ..preproc.double_flatfield import DoubleFlatField
from ..preproc.flatfield import FlatField
from ..io.writer import NXProcessWriter
from ..resources.dataset_analyzer import analyze_dataset
from ..resources.nxflatfield import update_dataset_info_flats_darks
from ..resources.logger import Logger, LoggerOrPrint
from .cli_configs import DFFConfig
from .utils import parse_params_values


class DoubleFlatFieldChunks:
    def __init__(
        self,
        dataset_path,
        output_file,
        dataset_info=None,
        chunk_size=100,
        sigma=None,
        do_flatfield=True,
        h5_entry=None,
        logger=None,
    ):
        self.logger = LoggerOrPrint(logger)
        self.do_flatfield = bool(do_flatfield)
        if dataset_info is not None:
            self.dataset_info = dataset_info
        else:
            self.dataset_info = analyze_dataset(dataset_path, extra_options={"hdf5_entry": h5_entry}, logger=logger)
            if self.do_flatfield:
                update_dataset_info_flats_darks(self.dataset_info, flatfield_mode=True)

        self.chunk_size = min(chunk_size, self.dataset_info.radio_dims[-1])
        self.output_file = output_file
        self.sigma = sigma if sigma is not None and abs(sigma) > 1e-5 else None

    def _get_config(self):
        conf = {
            "dataset": self.dataset_info.location,
            "entry": self.dataset_info.hdf5_entry or None,
            "dff_sigma": self.sigma,
            "do_flatfield": self.do_flatfield,
        }
        return conf

    def _read_projections(self, chunk_size, start_idx=0):
        reader_kwargs = {"sub_region": (slice(None), slice(start_idx, start_idx + chunk_size), slice(None))}
        if self.dataset_info.kind == "edf":
            reader_kwargs = {"n_reading_threads": 4}
        self.reader = self.dataset_info.get_reader(**reader_kwargs)
        self.projections = self.reader.load_data()

    def _init_flatfield(self, start_z=None, end_z=None):
        if not self.do_flatfield:
            return
        chunk_size = end_z - start_z if start_z is not None else self.chunk_size
        self.flatfield = FlatField(
            (self.dataset_info.n_angles, chunk_size, self.dataset_info.radio_dims[0]),
            flats={k: arr[start_z:end_z, :] for k, arr in self.dataset_info.flats.items()},
            darks={k: arr[start_z:end_z, :] for k, arr in self.dataset_info.darks.items()},
            radios_indices=sorted(self.dataset_info.projections.keys()),
        )

    def _apply_flatfield(self, start_z=None, end_z=None):
        if self.do_flatfield:
            self._init_flatfield(start_z=start_z, end_z=end_z)
            self.flatfield.normalize_radios(self.projections)

    def _init_dff(self):
        self.double_flatfield = DoubleFlatField(
            self.projections.shape,
            input_is_mlog=False,
            output_is_mlog=False,
            average_is_on_log=self.sigma is not None,
            sigma_filter=self.sigma,
        )

    def compute_double_flatfield(self):
        """
        Compute the double flatfield for the current dataset.
        """
        n_z = self.dataset_info.radio_dims[-1]
        chunk_size = self.chunk_size
        n_steps = n_z // chunk_size
        extra_step = bool(n_z % chunk_size)
        res = np.zeros(self.dataset_info.radio_dims[::-1])
        for i in range(n_steps):
            self.logger.debug("Computing DFF batch %d/%d" % (i + 1, n_steps + int(extra_step)))
            subregion = (None, None, i * chunk_size, (i + 1) * chunk_size)
            self._read_projections(chunk_size, start_idx=i * chunk_size)
            self._apply_flatfield(start_z=i * chunk_size, end_z=(i + 1) * chunk_size)
            self._init_dff()
            dff = self.double_flatfield.compute_double_flatfield(self.projections, recompute=True)
            res[subregion[-2] : subregion[-1]] = dff[:]
        # Need to initialize objects with a different shape
        if extra_step:
            curr_idx = (i + 1) * self.chunk_size
            self.logger.debug("Computing DFF batch %d/%d" % (i + 2, n_steps + int(extra_step)))
            self._read_projections(n_z - curr_idx, start_idx=curr_idx)
            self._apply_flatfield(start_z=(i + 1) * chunk_size, end_z=n_z)
            self._init_dff()
            dff = self.double_flatfield.compute_double_flatfield(self.projections, recompute=True)
            res[curr_idx:] = dff[:]
        return res

    def write_double_flatfield(self, arr):
        """
        Write the double flatfield image to a file
        """
        writer = NXProcessWriter(
            self.output_file,
            entry=self.dataset_info.hdf5_entry or "entry",
            filemode="a",
            overwrite=True,
        )
        writer.write(arr, "double_flatfield", config=self._get_config())
        self.logger.info("Wrote %s" % writer.fname)
        return writer.fname


def dff_cli():
    args = parse_params_values(
        DFFConfig, parser_description="A command-line utility for computing the double flatfield of a dataset."
    )
    logger = Logger("nabu_double_flatfield", level=args["loglevel"], logfile="nabu_double_flatfield.log")

    output_file = args["output"]

    dff = DoubleFlatFieldChunks(
        args["dataset"],
        output_file,
        chunk_size=args["chunk_size"],
        sigma=args["sigma"],
        do_flatfield=bool(args["flatfield"]),
        h5_entry=args["entry"] or None,
        logger=logger,
    )
    dff_image = dff.compute_double_flatfield()
    dff.write_double_flatfield(dff_image)
    return 0


if __name__ == "__main__":
    dff_cli()
