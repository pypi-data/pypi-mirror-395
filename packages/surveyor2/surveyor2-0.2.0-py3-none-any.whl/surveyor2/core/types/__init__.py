from __future__ import annotations

# Import from submodules
from .base import Frame, Video, MetricResult
from .config import (
    InputItem,
    InputsConfig,
    AggregateConfig,
    MetricConfig,
    ProfileConfig,
)
from .cli import ProfileArgs, ScaffoldArgs, InputsArgs, ExportArgs

__all__ = [
    # Base types
    "Frame",
    "Video",
    "MetricResult",
    # Config types
    "InputItem",
    "InputsConfig",
    "AggregateConfig",
    "MetricConfig",
    "ProfileConfig",
    # CLI types
    "ProfileArgs",
    "ScaffoldArgs",
    "InputsArgs",
    "ExportArgs",
]
