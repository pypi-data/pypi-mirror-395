"""Basic metrics preset: PSNR and SSIM.

This preset includes fundamental pixel-level metrics for video quality assessment.
"""

from ..core.types.config import ProfileConfig, MetricConfig, AggregateConfig
from . import ProfilePreset


class Basic(ProfilePreset):
    """Basic metrics preset: PSNR and SSIM.
    
    This preset includes fundamental pixel-level metrics for video quality assessment.
    """

    def get_preset(self) -> ProfileConfig:
        """Get the basic metrics preset."""
        return ProfileConfig(
            metrics=[
                MetricConfig(
                    name="psnr",
                    settings={"max_pixel": 255.0},
                    params={},
                ),
                MetricConfig(
                    name="ssim",
                    settings={},
                    params={},
                ),
            ],
            aggregate=AggregateConfig(
                weights={
                    "psnr": 1.0,
                    "ssim": 1.0,
                }
            ),
        )

