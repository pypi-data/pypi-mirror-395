from tomoscan.identifier import BaseIdentifier
from nabu.stitching.stitcher.y_stitcher import PreProcessingYStitcher as PreProcessYStitcher
from nabu.stitching.config import PreProcessedYStitchingConfiguration


def y_stitching(configuration: PreProcessedYStitchingConfiguration, progress=None) -> BaseIdentifier:
    """
    Apply stitching from provided configuration.
    Stitching will be applied along the first axis - 1 (aka y).

    like:
                    axis 0
                      ^
                      |
    x-ray             |
    -------->          ------> axis 2
                     /
                    /
                     axis 1
    """
    if isinstance(configuration, PreProcessedYStitchingConfiguration):
        stitcher = PreProcessYStitcher(configuration=configuration, progress=progress)
    else:
        raise TypeError(
            f"configuration is expected to be in {(PreProcessedYStitchingConfiguration, )}. {type(configuration)} provided"
        )
    return stitcher.stitch()
