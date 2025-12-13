"""Similarity metrics preset: Comprehensive similarity evaluation metrics.

This preset includes pixel-level, structural, perceptual, and temporal similarity metrics
for comprehensive video quality assessment: PSNR, SSIM, VMAF, LPIPS, and T-LPIPS.
"""

from ..core.types.config import ProfileConfig, MetricConfig, AggregateConfig
from . import ProfilePreset


class Similarity(ProfilePreset):
    """Similarity metrics preset: Comprehensive similarity evaluation metrics.
    
    This preset includes pixel-level, structural, perceptual, and temporal similarity metrics
    for comprehensive video quality assessment: PSNR, SSIM, VMAF, LPIPS, and T-LPIPS.
    """

    def get_preset(self) -> ProfileConfig:
        """Get the similarity metrics preset."""
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
                MetricConfig(
                    name="vmaf",
                    settings={"model": "auto"},
                    params={},
                ),
                MetricConfig(
                    name="lpips",
                    settings={"device": "auto", "backbone": "vgg", "batch_size": 8},
                    params={},
                ),
                MetricConfig(
                    name="t_lpips",
                    settings={"device": "auto", "backbone": "vgg", "batch_size": 8},
                    params={},
                ),
            ],
            aggregate=AggregateConfig(
                weights={
                    "psnr": 1.0,
                    "ssim": 1.0,
                    "vmaf": 1.0,
                    "lpips": 1.0,
                    "t_lpips": 1.0,
                }
            ),
        )

