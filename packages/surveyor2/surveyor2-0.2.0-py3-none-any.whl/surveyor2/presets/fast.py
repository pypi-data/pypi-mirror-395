"""Fast metrics preset: Quick evaluation with key temporal and quality metrics.

This preset includes fast-running metrics for temporal consistency and imaging quality.
"""

from ..core.types.config import ProfileConfig, MetricConfig, AggregateConfig
from . import ProfilePreset


class Fast(ProfilePreset):
    """Fast metrics preset: Quick evaluation with key temporal and quality metrics.
    
    This preset includes fast-running metrics for temporal consistency and imaging quality.
    """

    def get_preset(self) -> ProfileConfig:
        """Get the fast metrics preset."""
        return ProfileConfig(
            metrics=[
                MetricConfig(
                    name="t_lpips",
                    settings={"device": "cuda"},
                    params={},
                ),
                MetricConfig(
                    name="tof",
                    settings={},
                    params={},
                ),
                MetricConfig(
                    name="vbench_imaging_quality",
                    settings={"device": "cuda"},
                    params={},
                ),
                MetricConfig(
                    name="vbench_temporal_flickering",
                    settings={"device": "cuda"},
                    params={},
                ),
            ],
            aggregate=AggregateConfig(
                weights={
                    "t_lpips": 1.0,
                    "tof": 1.0,
                    "vbench_imaging_quality": 1.0,
                    "vbench_temporal_flickering": 1.0,
                }
            ),
        )

