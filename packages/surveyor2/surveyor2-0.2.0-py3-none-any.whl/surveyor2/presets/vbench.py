"""VBench metrics preset: Default VBench evaluation dimensions.

VBench is a comprehensive evaluation benchmark for text-to-video generation models.
This preset includes the default-enabled VBench quality dimensions.
"""

from ..core.types.config import ProfileConfig, MetricConfig, AggregateConfig
from . import ProfilePreset

# VBench dimensions enabled by default
VBENCH_DEFAULT_DIMENSIONS = [
    "subject_consistency",
    "background_consistency",
    "temporal_flickering",
    "motion_smoothness",
    "imaging_quality",
    "overall_consistency",
]


class VBench(ProfilePreset):
    """VBench metrics preset with default-enabled dimensions.
    
    VBench is a comprehensive evaluation benchmark for text-to-video generation models.
    This preset includes the default-enabled VBench quality dimensions.
    """

    def get_preset(self) -> ProfileConfig:
        """Get the VBench metrics preset with default-enabled dimensions."""
        return ProfileConfig(
            metrics=[
                MetricConfig(
                    name=f"vbench_{dimension}",
                    settings={"device": "cuda"},
                    params={},
                )
                for dimension in VBENCH_DEFAULT_DIMENSIONS
            ],
            aggregate=AggregateConfig(
                weights={f"vbench_{dim}": 1.0 for dim in VBENCH_DEFAULT_DIMENSIONS}
            ),
        )

