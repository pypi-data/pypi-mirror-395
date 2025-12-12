from enum import Enum
import h5py
import numpy


class AlignmentAxis2(Enum):
    """Specific alignment names to help users orient themselves with specific labels"""

    CENTER = "center"
    LEFT = "left"
    RIGTH = "right"


class AlignmentAxis1(Enum):
    """Specific alignment names to help users orient themselves with specific labels"""

    FRONT = "front"
    CENTER = "center"
    BACK = "back"


class _Alignment(Enum):
    """Internal alignment to be used for 2D alignment"""

    LOWER_BOUNDARY = "lower boundary"
    HIGHER_BOUNDARY = "higher boundary"
    CENTER = "center"

    @classmethod
    def from_value(cls, value):
        # cast the AlignmentAxis1 and AlignmentAxis2 values to fit the generic definition.
        if value in ("front", "left", AlignmentAxis1.FRONT, AlignmentAxis2.LEFT):
            return _Alignment.LOWER_BOUNDARY
        elif value in ("back", "right", AlignmentAxis1.BACK, AlignmentAxis2.RIGTH):
            return _Alignment.HIGHER_BOUNDARY
        elif value in (AlignmentAxis1.CENTER, AlignmentAxis2.CENTER):
            return _Alignment.CENTER
        else:
            return super().__new__(cls, value)


def align_frame(
    data: numpy.ndarray, alignment: _Alignment, alignment_axis: int, new_aligned_axis_size: int, pad_mode="constant"
):
    """
    Align 2D array to extend if size along `alignment_axis` to `new_aligned_axis_size`.

    :param numpy.ndarray data: data (frame) to align (2D numpy array)
    :param alignment_axis: axis along which we want to align the frame. Must be in (0, 1)
    :param HAlignment alignment: alignment strategy
    :param int new_width: output data width
    """
    if alignment_axis not in (0, 1):
        raise ValueError(f"alignment_axis should be in (0, 1). Get {alignment_axis}")
    alignment = _Alignment.from_value(alignment)

    aligned_axis_size = data.shape[alignment_axis]

    if aligned_axis_size > new_aligned_axis_size:
        raise ValueError(
            f"data.shape[alignment_axis] ({data.shape[alignment_axis]}) > new_aligned_axis_size ({new_aligned_axis_size}). Unable to crop data"
        )
    elif aligned_axis_size == new_aligned_axis_size:
        return data
    else:
        if alignment is _Alignment.CENTER:
            lower_boundary = (new_aligned_axis_size - aligned_axis_size) // 2
            higher_boundary = (new_aligned_axis_size - aligned_axis_size) - lower_boundary
        elif alignment is _Alignment.LOWER_BOUNDARY:
            lower_boundary = 0
            higher_boundary = new_aligned_axis_size - aligned_axis_size
        elif alignment is _Alignment.HIGHER_BOUNDARY:
            lower_boundary = new_aligned_axis_size - aligned_axis_size
            higher_boundary = 0
        else:
            raise ValueError(f"alignment {alignment.value} is not handled")

        assert lower_boundary >= 0, f"pad size must be positive - lower boundary isn't ({lower_boundary})"
        assert higher_boundary >= 0, f"pad size must be positive - higher boundary isn't ({higher_boundary})"

        if alignment_axis == 1:
            return numpy.pad(
                data,
                pad_width=((0, 0), (lower_boundary, higher_boundary)),
                mode=pad_mode,
            )
        elif alignment_axis == 0:
            return numpy.pad(
                data,
                pad_width=((lower_boundary, higher_boundary), (0, 0)),
                mode=pad_mode,
            )
        else:
            raise ValueError("alignment_axis should be in (0, 1)")


def align_horizontally(data: numpy.ndarray, alignment: AlignmentAxis2, new_width: int, pad_mode="constant"):
    """
    Align data horizontally to make sure new data width will ne `new_width`.

    :param numpy.ndarray data: data to align
    :param HAlignment alignment: alignment strategy
    :param int new_width: output data width
    """
    alignment = AlignmentAxis2(alignment).value
    return align_frame(
        data=data, alignment=alignment, new_aligned_axis_size=new_width, pad_mode=pad_mode, alignment_axis=1
    )


class PaddedRawData:
    """
    Util class to extend a data when necessary
    Must to aplpy to a volume and to an hdf5dataset - array
    The idea behind is to avoid loading all the data in memory
    """

    def __init__(self, data: numpy.ndarray | h5py.Dataset, axis_1_pad_width: tuple) -> None:
        self._axis_1_pad_width = numpy.array(axis_1_pad_width)
        if not (self._axis_1_pad_width.size == 2 and self._axis_1_pad_width[0] >= 0 and self._axis_1_pad_width[1] >= 0):
            raise ValueError(f"'axis_1_pad_width' expects to positive elements. Get {axis_1_pad_width}")
        self._raw_data = data
        self._raw_data_end = None
        # note: for now we return only frames with zeros for padded frames.
        # in the future we could imagine having a method and miror existing volume or extend the closest frame, or get a mean value...
        self._empty_frame = None
        self._dtype = None
        self._shape = None
        self._raw_data_shape = self.raw_data.shape

    @staticmethod
    def get_empty_frame(shape, dtype):
        return numpy.zeros(
            shape=shape,
            dtype=dtype,
        )

    @property
    def empty_frame(self):
        if self._empty_frame is None:
            self._empty_frame = self.get_empty_frame(
                shape=(self.shape[0], 1, self.shape[2]),
                dtype=self.dtype,
            )
        return self._empty_frame

    @property
    def shape(self):
        if self._shape is None:
            self._shape = tuple(  # noqa: C409
                (
                    self._raw_data_shape[0],
                    numpy.sum(
                        numpy.array(self._axis_1_pad_width),
                    )
                    + self._raw_data_shape[1],
                    self._raw_data_shape[2],
                )
            )
        return self._shape

    @property
    def raw_data(self):
        return self._raw_data

    @property
    def raw_data_start(self):
        return self._axis_1_pad_width[0]

    @property
    def raw_data_end(self):
        if self._raw_data_end is None:
            self._raw_data_end = self._axis_1_pad_width[0] + self._raw_data_shape[1]
        return self._raw_data_end

    @property
    def dtype(self):
        if self._dtype is None:
            self._dtype = self.raw_data.dtype
        return self._dtype

    def __getitem__(self, args):
        if not isinstance(args, tuple) and len(args) == 3:
            raise ValueError("only handles 3D slicing")
        elif not (args[0] == slice(None, None, None) and args[2] == slice(None, None, None)):
            raise ValueError(
                "slicing only handled along axis 1. First and third tuple item are expected to be empty slice as slice(None, None, None)"
            )
        else:
            if numpy.isscalar(args[1]):
                args = (
                    args[0],
                    slice(args[1], args[1] + 1, 1),
                    args[2],
                )

            start = args[1].start
            if start is None:
                start = 0
            stop = args[1].stop
            if stop is None:
                stop = self.shape[1]
            step = args[1].step
            # some test
            if start < 0 or stop < 0:
                raise ValueError("only positive position are handled")
            if start >= stop:
                raise ValueError("start >= stop")
            if stop > self.shape[1]:
                raise ValueError("stop > self.shape[1]")
            if step not in (1, None):
                raise ValueError("for now PaddedVolume only handles steps of 1")

            first_part_array = None
            if start < self.raw_data_start and (stop - start > 0):
                stop_first_part = min(stop, self.raw_data_start)
                first_part_array = numpy.repeat(self.empty_frame, repeats=stop_first_part - start, axis=1)
                start = stop_first_part

            third_part_array = None
            if stop > self.raw_data_end and (stop - start > 0):
                if stop > self.shape[1]:
                    raise ValueError("requested slice is out of boundaries")
                start_third_part = max(start, self.raw_data_end)
                third_part_array = numpy.repeat(self.empty_frame, repeats=stop - start_third_part, axis=1)
                stop = self.raw_data_end

            if start >= self.raw_data_start and stop >= self.raw_data_start and (stop - start > 0):
                second_part_array = self.raw_data[:, start - self.raw_data_start : stop - self.raw_data_start, :]
            else:
                second_part_array = None

            parts = tuple(filter(lambda a: a is not None, (first_part_array, second_part_array, third_part_array)))
            return numpy.hstack(
                parts,
            )
