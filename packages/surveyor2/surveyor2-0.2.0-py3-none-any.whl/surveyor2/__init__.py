"""Surveyor2 - Video quality evaluation framework."""

# Main API
from .driver import run_profile, load_inputs_config, load_metrics_config
from .core.report import BatchReport, Report

# Core types for API usage
from .core.types import (
    InputItem,
    InputsConfig,
    AggregateConfig,
    MetricConfig,
    ProfileConfig,
)

# Presets
from .presets import list_presets, get_preset

__all__ = [
    # Main API
    "run_profile",
    "load_inputs_config",
    "load_metrics_config",
    "BatchReport",
    "Report",
    # Types
    "InputItem",
    "InputsConfig",
    "AggregateConfig",
    "MetricConfig",
    "ProfileConfig",
    # Presets
    "list_presets",
    "get_preset",
]

