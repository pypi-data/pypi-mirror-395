from tomoscan.identifier import BaseIdentifier
from nabu.stitching.stitcher.z_stitcher import PreProcessingZStitcher as PreProcessZStitcher
from nabu.stitching.stitcher.z_stitcher import (
    PostProcessingZStitcher as PostProcessZStitcher,
    PostProcessingZStitcherNoDD as PostProcessZStitcherNoDD,
)
from nabu.stitching.config import (
    PreProcessedZStitchingConfiguration,
    PostProcessedZStitchingConfiguration,
)


def z_stitching(
    configuration: PreProcessedZStitchingConfiguration | PostProcessedZStitchingConfiguration, progress=None
) -> BaseIdentifier:
    """
    Apply stitching from provided configuration. Along axis 0 (aka z)
    Return a DataUrl with the created NXtomo or Volume

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
    stitcher = None
    assert configuration.axis is not None
    if isinstance(configuration, PreProcessedZStitchingConfiguration):
        if configuration.axis == 0:
            stitcher = PreProcessZStitcher(configuration=configuration, progress=progress)
    elif isinstance(configuration, PostProcessedZStitchingConfiguration):
        assert configuration.axis == 0
        if configuration.duplicate_data:
            stitcher = PostProcessZStitcher(configuration=configuration, progress=progress)
        else:
            stitcher = PostProcessZStitcherNoDD(configuration=configuration, progress=progress)

    if stitcher is None:
        raise TypeError(
            f"configuration is expected to be in {(PreProcessedZStitchingConfiguration, PostProcessedZStitchingConfiguration)}. {type(configuration)} provided"
        )
    return stitcher.stitch()
