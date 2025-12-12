from os import path
import numpy as np
from scipy.ndimage import gaussian_filter
from silx.io.url import DataUrl
from ..utils import check_shape, get_2D_3D_shape
from ..io.reader import HDF5Reader
from ..io.writer import NXProcessWriter
from .ccd import Log


class DoubleFlatField:
    _default_h5_path = "/entry/double_flatfield/results"
    _small = 1e-7

    def __init__(
        self,
        shape,
        result_url=None,
        sub_region=None,
        detector_corrector=None,
        input_is_mlog=True,
        output_is_mlog=False,
        average_is_on_log=False,
        sigma_filter=None,
        filter_mode="reflect",
        log_clip_min=None,
        log_clip_max=None,
    ):
        """
        Init double flat field by summing a series of urls and considering the same subregion of them.

        Parameters
        ----------
        shape: tuple
            Expected shape of radios chunk to process
        result_url: url, optional
            where the double-flatfield is stored after being computed, and
            possibly read (instead of re-computed) before processing the images.
        sub_region: tuple, optional
            If provided, this must be a tuple in the form
            (start_x, end_x, start_y, end_y). Each image will be cropped to this
            region. This is used to specify a chunk of files.
            Each of the parameters can be None, in this case the default start
            and end are taken in each dimension.
        input_is_mlog:  boolean, default True
            the input is considred as minus logarithm of normalised radios
        output_is_mlog:  boolean, default True
            the output is considred as minus logarithm of normalised radios
        average_is_on_log : boolean, False
            the minus logarithm of the data is averaged
            the clipping value that is applied prior to the logarithm
        sigma_filter: optional
            if given a high pass filter is applied by signal -gaussian_filter(signal,sigma,filter_mode)
        filter_mode: optional, default 'reflect'
            the padding scheme applied a the borders ( same as scipy.ndimage.filtrs.gaussian_filter)

        """
        self.radios_shape = get_2D_3D_shape(shape)
        self.n_angles = self.radios_shape[0]
        self.shape = self.radios_shape[1:]
        self._log_clip_min = log_clip_min
        self._log_clip_max = log_clip_max
        self._init_filedump(result_url, sub_region, detector_corrector)
        self._init_processing(input_is_mlog, output_is_mlog, average_is_on_log, sigma_filter, filter_mode)
        self._computed = False

    def _load_dff_dump(self):
        res = self.reader.get_data(self.result_url)
        if self.detector_corrector is not None:
            if res.ndim == 2:
                res = self.detector_corrector.transform(res)
            else:
                for i in range(res.shape[0]):
                    res[i] = self.detector_corrector.transform(res[i])

        if res.ndim == 3 and res.shape[0] == 1:
            res = res.reshape(res.shape[1], res.shape[2])
        if res.shape != self.shape:
            raise ValueError(
                "Data in %s has shape %s, but expected %s"
                % (self.result_url.file_path(), str(res.shape), str(self.shape))
            )
        return res

    def _init_filedump(self, result_url, sub_region, detector_corrector=None):
        if isinstance(result_url, str):
            result_url = DataUrl(file_path=result_url, data_path=self._default_h5_path)
        self.sub_region = sub_region
        self.detector_corrector = detector_corrector
        self.result_url = result_url
        self.writer = None
        self.reader = None
        if self.result_url is None:
            return
        if path.exists(result_url.file_path()):
            if detector_corrector is None:
                adapted_subregion = sub_region
            else:
                adapted_subregion = self.detector_corrector.get_adapted_subregion(sub_region)
            self.reader = HDF5Reader(sub_region=adapted_subregion)
        else:
            self.writer = NXProcessWriter(self.result_url.file_path())

    def _init_processing(self, input_is_mlog, output_is_mlog, average_is_on_log, sigma_filter, filter_mode):
        self.input_is_mlog = input_is_mlog
        self.output_is_mlog = output_is_mlog
        self.average_is_on_log = average_is_on_log
        self.sigma_filter = sigma_filter
        if self.sigma_filter is not None and abs(float(self.sigma_filter)) < 1e-4:
            self.sigma_filter = None
        self.filter_mode = filter_mode
        proc = lambda x, o: np.copyto(o, x)
        self._mlog = Log((1,) + self.shape, clip_min=self._log_clip_min, clip_max=self._log_clip_max)

        if self.input_is_mlog:
            if not self.average_is_on_log:
                proc = lambda x, o: np.exp(-x, out=o)
        else:
            if self.average_is_on_log:
                proc = self._proc_mlog

        postproc = lambda x: x
        if self.output_is_mlog:
            if not self.average_is_on_log:
                postproc = self._proc_mlog
        else:
            if self.average_is_on_log:
                postproc = lambda x: np.exp(-x)

        self.proc = proc
        self.postproc = postproc

    def _proc_mlog(self, x, o):
        o[:] = x[:]
        self._mlog.take_logarithm(o)
        return o

    def compute_double_flatfield(self, radios, recompute=False):
        """
        Read the radios and generate the "double flat field" by averaging
        and possibly other processing.

        Parameters
        ----------
        radios: array
            Input radios chunk.
        recompute: bool, optional
            Whether to recompute the double flatfield if already computed.
        """
        if self._computed and not (recompute):
            return self.doubleflatfield  # pylint: disable=E0203
        acc = np.zeros(radios[0].shape, "f")
        tmpdat = np.zeros(radios[0].shape, "f")
        for ima in radios:
            self.proc(ima, tmpdat)
            acc += tmpdat

        acc /= radios.shape[0]

        if self.sigma_filter is not None:
            acc = acc - gaussian_filter(acc, self.sigma_filter, mode=self.filter_mode)
        self.doubleflatfield = self.postproc(acc)
        # Handle small values to avoid issues when dividing
        self.doubleflatfield[np.abs(self.doubleflatfield) < self._small] = 1.0
        self.doubleflatfield = self.doubleflatfield.astype("f")

        if self.writer is not None:
            self.writer.write(self.doubleflatfield, "double_flatfield")
        self._computed = True
        return self.doubleflatfield

    def get_double_flatfield(self, radios=None, compute=False):
        """
        Get the double flat field or a subregion of it.

        Parameters
        ----------
        radios: array, optional
            Input radios chunk
        compute: bool, optional
            Whether to compute the double flatfield anyway even if a dump file
            exists.
        """
        if self.reader is None:
            if radios is None:
                raise ValueError("result_url was not provided. Please provide 'radios' to this function")
            return self.compute_double_flatfield(radios)

        if radios is not None and compute:
            res = self.compute_double_flatfield(radios)
        else:
            res = self._load_dff_dump()
            self._computed = True
        return res

    def apply_double_flatfield(self, radios):
        """
        Apply the "double flatfield" filter on a chunk of radios.
        The processing is done in-place !
        """
        check_shape(radios.shape, self.radios_shape, "radios")
        dff = self.get_double_flatfield(radios=radios)
        for i in range(self.n_angles):
            radios[i] /= dff
        return radios
