from nabu.stitching.stitcher.pre_processing import PreProcessingStitching
from nabu.stitching.stitcher.post_processing import PostProcessingStitching
from .dumper import (
    PreProcessingStitchingDumper,
    PostProcessingStitchingDumperNoDD,
    PostProcessingStitchingDumperWithCache,
)
from nabu.stitching.stitcher.single_axis import _SingleAxisMetaClass


class PreProcessingZStitcher(
    PreProcessingStitching,
    dumper_cls=PreProcessingStitchingDumper,
    axis=0,
):

    def check_inputs(self):
        """
        insure input data is coherent
        """
        super().check_inputs()

        for scan_0, scan_1 in zip(self.series[0:-1], self.series[1:]):
            if scan_0.dim_1 != scan_1.dim_1:
                raise ValueError(
                    f"projections width are expected to be the same. Not the case for {scan_0} ({scan_0.dim_1} and {scan_1} ({scan_1.dim_1}))"
                )


class PostProcessingZStitcher(
    PostProcessingStitching,
    metaclass=_SingleAxisMetaClass,
    dumper_cls=PostProcessingStitchingDumperWithCache,
    axis=0,
):
    @property
    def serie_label(self) -> str:
        return "z-series"


class PostProcessingZStitcherNoDD(
    PostProcessingStitching,
    metaclass=_SingleAxisMetaClass,
    dumper_cls=PostProcessingStitchingDumperNoDD,
    axis=0,
):
    @property
    def serie_label(self) -> str:
        return "z-series"
