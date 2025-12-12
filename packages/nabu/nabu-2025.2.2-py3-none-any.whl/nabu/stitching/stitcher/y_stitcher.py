from nabu.stitching.stitcher.pre_processing import PreProcessingStitching
from .dumper import PreProcessingStitchingDumper


class PreProcessingYStitcher(
    PreProcessingStitching,
    dumper_cls=PreProcessingStitchingDumper,
    axis=1,
):

    @property
    def serie_label(self) -> str:
        return "y-serie"
