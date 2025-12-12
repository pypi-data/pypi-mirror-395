from os import path
from tomoscan.esrf import TIFFVolume, MultiTIFFVolume, EDFVolume, JP2KVolume
from tomoscan.esrf.volume.singleframebase import VolumeSingleFrameBase
from ..utils import check_supported, get_num_threads
from ..resources.logger import LoggerOrPrint
from ..io.writer import NXProcessWriter, HSTVolVolume, NXVolVolume
from ..io.utils import convert_dict_values
from .params import files_formats


class WriterManager:
    """
    This class is a wrapper on top of all "writers".
    It will create the right "writer" with all the necessary options, and the histogram writer.

    The layout is the following.

       * Single-big-file volume formats (big-tiff, .vol):
           - no start index
           - everything is increasingly written in one file
       * Multiple-frames per file (HDF5 + master-file):
          - needs a start index (change file_prefix) for each partial file
          - needs a subdirectory for partial files
       * One-file-per-frame (tiff, edf, jp2)
          - start_index

    When saving intermediate steps (eg. sinogram): HDF5 format is always used.
    """

    _overwrite_warned = False
    _writer_classes = {
        "hdf5": NXVolVolume,
        "tiff": TIFFVolume,
        "bigtiff": MultiTIFFVolume,
        "jp2": JP2KVolume,
        "edf": EDFVolume,
        "vol": HSTVolVolume,
    }

    def __init__(
        self,
        output_dir,
        file_prefix,
        file_format="hdf5",
        overwrite=False,
        start_index=0,
        write_in_reverse_order=False,
        logger=None,
        metadata=None,
        histogram=False,
        extra_options=None,
    ):
        """
        Create a Writer from a set of parameters.

        Parameters
        ----------
        output_dir: str
            Directory where the file(s) will be written.
        file_prefix: str
            File prefix (without leading path)
        start_index: int, optional
            Index to start the files numbering (filename_0123.ext).
            Default is 0.
            Ignored for HDF5 extension.
        logger: nabu.resources.logger.Logger, optional
            Logger object
        metadata: dict, optional
            Metadata, eg. information on various processing steps. For HDF5, it will go to "configuration"
        histogram: bool, optional
            Whether to also write a histogram of data. If set to True, it will configure
            an additional "writer".
        extra_options: dict, optional
            Other advanced options to pass to Writer class.
        """
        self.extra_options = extra_options or {}
        self.write_in_reverse_order = write_in_reverse_order
        self._set_file_format(file_format)
        self.overwrite = overwrite
        self.start_index = start_index
        self.logger = LoggerOrPrint(logger)
        self.histogram = histogram
        self.output_dir = output_dir
        self.file_prefix = file_prefix
        self.metadata = convert_dict_values(metadata or {}, {None: "None"})
        self._init_writer()
        self._init_histogram_writer()

    def _set_file_format(self, file_format):
        check_supported(file_format, files_formats, "file format")
        self.file_format = files_formats[file_format]
        self._is_bigtiff = file_format in ["tiff", "tif"] and any(
            [self.extra_options.get(opt, False) for opt in ["tiff_single_file", "use_bigtiff"]]
        )
        if self._is_bigtiff:
            self.file_format = "bigtiff"

    @staticmethod
    def get_first_fname(vol_writer):
        if hasattr(vol_writer, "file_path"):
            return path.dirname(vol_writer.file_path)
        dirname = vol_writer.data_url.file_path()
        fname = vol_writer.data_url.data_path().format(
            volume_basename=vol_writer._volume_basename,
            index_zfill6=vol_writer.start_index,
            data_extension=vol_writer.extension or vol_writer.DEFAULT_DATA_EXTENSION,
        )
        return path.join(dirname, fname)

    @staticmethod
    def get_fname(vol_writer):
        if hasattr(vol_writer, "file_path"):
            # several frames per file - return the file itself
            return vol_writer.file_path
        # one file per frame - return the directory
        return vol_writer.data_url.file_path()

    def _init_writer(self):
        self._writer_was_already_initialized = self.extra_options.get("writer_initialized", False)
        if self.file_format in ["tiff", "edf", "jp2", "hdf5"]:
            writer_kwargs = {
                "folder": self.output_dir,
                "volume_basename": self.file_prefix,
                "start_index": self.start_index,
                "overwrite": self.overwrite,
            }
            if self.file_format == "hdf5":
                writer_kwargs["data_path"] = self.metadata.get("entry", "entry")
                writer_kwargs["process_name"] = self.metadata.get("process_name", "reconstruction")
                writer_kwargs["create_subfolder"] = self.extra_options.get("create_subfolder", True)
            elif self.file_format == "jp2":
                writer_kwargs["cratios"] = self.metadata.get("jpeg2000_compression_ratio", None)
                writer_kwargs["clip_values"] = self.metadata.get("float_clip_values", None)
                writer_kwargs["n_threads"] = get_num_threads()
        elif self.file_format in ["vol", "bigtiff"]:
            writer_kwargs = {
                "file_path": path.join(
                    self.output_dir, self.file_prefix + "." + self.file_format.replace("bigtiff", "tiff")
                ),
                "overwrite": self.overwrite,
                "append": self.extra_options.get("single_output_file_initialized", False),
            }
            if self.file_format == "vol":
                writer_kwargs["hst_metadata"] = self.extra_options.get("raw_vol_metadata", {})
        else:
            raise ValueError("Unsupported file format: %s" % self.file_format)
        self._h5_entry = self.metadata.get("entry", "entry")
        self.writer = self._writer_classes[self.file_format](**writer_kwargs)
        self.fname = self.get_fname(self.writer)
        if isinstance(self.writer, VolumeSingleFrameBase):
            self.writer.write_in_descending_order = self.write_in_reverse_order
            # In certain cases, tomoscan needs to remove any previous existing volume filess
            # and avoid calling 'clean_output_data' when writing downstream (for chunk processing)
            self.writer.skip_existing_data_files_removal = self._writer_was_already_initialized
        # ---
        if path.exists(self.fname):
            err = "File already exists: %s" % self.fname
            if self.overwrite:
                if not (self.__class__._overwrite_warned):
                    self.logger.warning(err + ". It will be overwritten as requested in configuration")
                    self.__class__._overwrite_warned = True
            else:
                self.logger.fatal(err)
                raise ValueError(err)

    def _init_histogram_writer(self):
        if not self.histogram:
            return
        separate_histogram_file = self.file_format != "hdf5"
        if separate_histogram_file:
            fmode = "w"
            hist_fname = path.join(self.output_dir, "histogram_%05d.hdf5" % self.start_index)
        else:
            fmode = "a"
            hist_fname = self.fname
        # Nabu's original NXProcessWriter has to be used here, as histogram is not 3D
        self.histogram_writer = NXProcessWriter(
            hist_fname,
            entry=self._h5_entry,
            filemode=fmode,
            overwrite=True,
        )

    def write_histogram(self, data, config=None, processing_index=1):
        if not (self.histogram):
            return
        self.histogram_writer.write(
            data,
            "histogram",
            processing_index=processing_index,
            config=config,
            is_frames_stack=False,
            direct_access=False,
        )

    def _write_metadata(self):
        self.writer.metadata = self.metadata
        self.writer.save_metadata()

    def write_data(self, data, metadata=None):
        if self.write_in_reverse_order and self.file_format == "hdf5":
            data = data[::-1, ...]
        self.writer.data = data
        if metadata is not None:
            self.writer.metadata = metadata
        self.writer.save()
        # self._write_metadata()
