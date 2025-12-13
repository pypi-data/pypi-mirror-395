"""Configuration dataclasses for Surveyor2."""

from __future__ import annotations
from typing import Dict, Any, Optional, Union, List
from dataclasses import dataclass, field
import pathlib

__all__ = [
    "InputItem",
    "InputsConfig",
    "AggregateConfig",
    "MetricConfig",
    "ProfileConfig",
]


@dataclass
class InputItem:
    """
    Represents a single input item for video evaluation.

    Attributes:
        video: Path to the video file to evaluate
        reference: Path(s) to reference video(s) for comparison metrics
        max_frames: Maximum number of frames to process (optional)
        id: Unique identifier for this input item (optional)
        prompt: Text prompt describing the expected content (optional, for text-based metrics)
    """

    video: str
    reference: Optional[Union[str, List[str]]] = None
    max_frames: Optional[int] = None
    id: Optional[str] = None
    prompt: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> InputItem:
        """Create InputItem from dictionary (e.g., from YAML/JSON)."""
        video = data["video"]
        reference = data.get("reference")

        reference_paths = None
        if reference is not None:
            if isinstance(reference, str):
                reference_paths = [reference]
            elif isinstance(reference, list):
                reference_paths = reference
            else:
                raise ValueError(f"Invalid reference type: {type(reference)}")

        return cls(
            video=video,
            reference=reference_paths,
            max_frames=data.get("max_frames"),
            id=data.get("id"),
            prompt=data.get("prompt"),
        )


@dataclass
class InputsConfig:
    """
    Configuration for inputs (from YAML/JSON inputs file).
    Contains a list of InputItem objects.

    Example YAML:
        inputs:
          - id: video_001
            video: gen/001.mp4
            reference: ref/001.mp4
            prompt: "A cat playing with a ball"
    """

    inputs: List[InputItem] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> InputsConfig:
        """Create InputsConfig from dictionary (e.g., from YAML/JSON)."""
        inputs_raw = data.get("inputs", [])
        if not isinstance(inputs_raw, list):
            raise ValueError("Config must contain 'inputs' list")
        inputs = [InputItem.from_dict(item) for item in inputs_raw]
        return cls(inputs=inputs)


@dataclass
class AggregateConfig:
    """
    Configuration for metric aggregation.

    Attributes:
        weights: Optional weights for computing composite scores (metric_name -> weight)

    Example YAML:
        aggregate:
          weights:
            psnr: 1.0
            ssim: 2.0
            lpips: 1.5
    """

    weights: Optional[Dict[str, float]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AggregateConfig:
        """Create AggregateConfig from dictionary."""
        return cls(weights=data.get("weights"))


@dataclass
class MetricConfig:
    """
    Configuration for a single metric.

    Attributes:
        name: Metric identifier (e.g., "psnr", "ssim", "vmaf")
        settings: Metric-specific settings (e.g., device, model parameters)
        params: Runtime parameters passed to metric evaluation

    Example YAML:
        - name: psnr
          settings: { max_pixel: 255.0 }
          params: {}
    """

    name: str
    settings: Dict[str, Any] = field(default_factory=dict)
    params: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MetricConfig:
        """Create MetricConfig from dictionary."""
        name = data.get("name")
        if not name or not isinstance(name, str):
            raise ValueError("Metric config must have a 'name' field")

        return cls(
            name=str(name).strip(),
            settings=data.get("settings") or {},
            params=data.get("params") or {},
        )


@dataclass
class ProfileConfig:
    """
    Configuration for metrics (from YAML/JSON metrics file).
    Contains metric definitions and optional aggregation settings.

    Example YAML:
        metrics:
          - name: psnr
            settings: { max_pixel: 255.0 }
            params: {}
          - name: ssim
            settings: {}
            params: {}
        aggregate:
          weights: { psnr: 1, ssim: 1 }
    """

    metrics: List[MetricConfig] = field(default_factory=list)
    aggregate: AggregateConfig = field(default_factory=AggregateConfig)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProfileConfig:
        """Create MetricsConfig from dictionary (e.g., from YAML/JSON)."""
        metrics_raw = data.get("metrics", [])
        if not isinstance(metrics_raw, list):
            raise ValueError("Config must contain 'metrics' list")

        metrics = [MetricConfig.from_dict(m) for m in metrics_raw]

        aggregate_data = data.get("aggregate", {})
        aggregate = (
            AggregateConfig.from_dict(aggregate_data)
            if aggregate_data
            else AggregateConfig()
        )

        return cls(metrics=metrics, aggregate=aggregate)
