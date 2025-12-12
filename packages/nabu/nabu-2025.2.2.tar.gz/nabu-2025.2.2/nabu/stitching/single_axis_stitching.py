from .y_stitching import y_stitching
from .z_stitching import z_stitching
from tomoscan.identifier import BaseIdentifier
from nabu.stitching.config import (
    SingleAxisStitchingConfiguration,
    PreProcessedYStitchingConfiguration,
    PreProcessedZStitchingConfiguration,
    PostProcessedZStitchingConfiguration,
)


def stitching(configuration: SingleAxisStitchingConfiguration, progress=None) -> BaseIdentifier:
    """
    Apply stitching from provided configuration.
    Stitching will be applied along a single axis at the moment.

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
    if isinstance(configuration, (PreProcessedYStitchingConfiguration,)):
        return y_stitching(configuration=configuration, progress=progress)
    elif isinstance(configuration, (PreProcessedZStitchingConfiguration, PostProcessedZStitchingConfiguration)):
        return z_stitching(configuration=configuration, progress=progress)
    else:
        raise NotImplementedError(f"configuration type ({type(configuration)}) is not handled")
