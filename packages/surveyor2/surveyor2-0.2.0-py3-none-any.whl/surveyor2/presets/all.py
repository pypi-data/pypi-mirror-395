"""All metrics preset: Comprehensive evaluation with all available metrics.

This preset includes all available metrics for the most comprehensive video quality assessment.
Includes pixel-level metrics (PSNR, SSIM), perceptual metrics (LPIPS, TLPIPS), 
CLIP-based metrics (CLIPScore), temporal metrics (TOF), all VBench dimensions, and VMAF.
"""

from ..core.types.config import ProfileConfig, MetricConfig, AggregateConfig
from . import ProfilePreset

# All VBench dimensions (10 total)
VBENCH_ALL_DIMENSIONS = [
    "subject_consistency",
    "background_consistency",
    "temporal_flickering",
    "motion_smoothness",
    "dynamic_degree",
    "aesthetic_quality",
    "imaging_quality",
    "human_action",
    "temporal_style",
    "overall_consistency",
]


class All(ProfilePreset):
    """All metrics preset: Comprehensive evaluation with all available metrics.
    
    This preset includes all available metrics for the most comprehensive video quality assessment.
    Includes pixel-level metrics (PSNR, SSIM), perceptual metrics (LPIPS, TLPIPS), 
    CLIP-based metrics (CLIPScore), temporal metrics (TOF), all VBench dimensions, and VMAF.
    """

    def get_preset(self) -> ProfileConfig:
        """Get the all metrics preset with all available metrics."""
        metrics = []
        weights = {}
        
        # Pixel-level metrics
        metrics.extend([
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
        ])
        weights.update({"psnr": 1.0, "ssim": 1.0})
        
        # Perceptual metrics
        metrics.extend([
            MetricConfig(
                name="lpips",
                settings={"device": "cuda"},
                params={},
            ),
            MetricConfig(
                name="t_lpips",
                settings={"device": "cuda"},
                params={},
            ),
        ])
        weights.update({"lpips": 1.0, "t_lpips": 1.0})
        
        # CLIP-based metrics
        metrics.append(
            MetricConfig(
                name="clipscore",
                settings={"device": "cuda"},
                params={},
            )
        )
        weights["clipscore"] = 1.0
        
        # Temporal metrics
        metrics.append(
            MetricConfig(
                name="tof",
                settings={},
                params={},
            )
        )
        weights["tof"] = 1.0
        
        # All VBench dimensions
        for dimension in VBENCH_ALL_DIMENSIONS:
            metrics.append(
                MetricConfig(
                    name=f"vbench_{dimension}",
                    settings={"device": "cuda"},
                    params={},
                )
            )
            weights[f"vbench_{dimension}"] = 1.0
        
        # VMAF
        metrics.append(
            MetricConfig(
                name="vmaf",
                settings={},
                params={},
            )
        )
        weights["vmaf"] = 1.0
        
        return ProfileConfig(
            metrics=metrics,
            aggregate=AggregateConfig(weights=weights),
        )

