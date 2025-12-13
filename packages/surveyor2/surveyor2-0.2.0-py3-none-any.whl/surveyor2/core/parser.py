from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Mapping, List, Tuple, Type, Optional
from .metrics_base import Metric
from .registry import (
    list_metrics as _list_metrics,
    get_metric_cls as _get_metric_cls,
    describe_metric,
    describe_all_metrics,
)
from .types import ProfileConfig, MetricConfig, AggregateConfig


class ParseError(Exception):
    """Fatal configuration error (e.g., unknown metric, missing required setting)."""


@dataclass
class MetricParameters:
    name: str
    cls: Type[Metric]
    settings: Dict[str, Any]
    params: Dict[str, Any]


def build_default_metrics_config_from_registry() -> ProfileConfig:
    """
    Build a default configuration using the registry descriptions.
    - Includes only metrics with enabled_by_default=True
    - Uses only settings that have explicit defaults
    - Sets aggregate weights to 1 per metric

    Returns:
        ProfileConfig object with enabled metrics and default settings
    """
    catalog = sorted(
        describe_all_metrics(), key=lambda d: d["name"]
    )  # [{name, enabled_by_default, settings:{k:{required,default}}, params:[...]}]

    # Filter to only metrics enabled by default
    enabled_metrics = [m for m in catalog if m.get("enabled_by_default", True)]

    # Build MetricConfig objects directly
    metric_configs: List[MetricConfig] = []
    for m in enabled_metrics:
        settings_meta = m.get("settings", {}) or {}
        defaults: Dict[str, Any] = {}
        for key, meta in settings_meta.items():
            # Only include keys that declare an explicit default
            if "default" in meta:
                defaults[key] = meta.get("default", None)

        metric_configs.append(
            MetricConfig(
                name=m["name"],
                settings=defaults,
                params={},
            )
        )

    # Build AggregateConfig directly
    weights = {m["name"]: 1.0 for m in enabled_metrics}
    aggregate = AggregateConfig(weights=weights)

    # Return MetricsConfig directly
    return ProfileConfig(
        metrics=metric_configs,
        aggregate=aggregate,
    )


# -----------------------
# Settings / params resolution
# -----------------------


def _norm_keys(d: Mapping[str, Any]) -> Dict[str, Any]:
    return {str(k).strip().lower(): v for k, v in d.items()}


def resolve_metric_settings(
    metric_cls: Type[Metric],
    provided: Mapping[str, Any],
) -> Tuple[Dict[str, Any], List[str]]:
    """
    Resolve init-time settings for a metric.
    - Fill defaults for optional keys (if provided by metric)
    - ERROR on missing required keys (returned in `errors`)
    - IGNORE unknown keys (no warnings)
    Returns: (resolved_settings, errors)
    """
    req_map = _norm_keys(metric_cls.get_settings())  # key -> required(bool)
    defaults = _norm_keys(metric_cls.get_setting_defaults())  # key -> default(any)
    prov = _norm_keys(provided)

    resolved: Dict[str, Any] = {}
    errors: List[str] = []

    # required / optional with defaults
    for key, is_required in req_map.items():
        if key in prov:
            resolved[key] = prov[key]
        elif is_required:
            errors.append(f"{metric_cls.__name__}: missing required setting '{key}'")
        else:
            if key in defaults:
                resolved[key] = defaults[key]

    # NOTE: unknown settings are silently ignored by design.

    return resolved, errors


def filter_metric_params(
    metric_cls: Type[Metric],
    provided: Mapping[str, Any],
) -> Dict[str, Any]:
    """
    Keep only params declared by metric_cls.get_params().
    Unknown params are silently dropped.
    """
    allowed = {p.lower() for p in metric_cls.get_params()}
    prov = _norm_keys(provided)
    return {k: v for k, v in prov.items() if k in allowed}


# -----------------------
# Parse a nested metrics block from JSON/YAML
# -----------------------


def parse_metrics_block(
    metrics_block: List[MetricConfig],
    *,
    allow_unknown_metrics: bool = False,
) -> Tuple[List[MetricParameters], List[str]]:
    """
    Input (typical JSON/YAML):
      metrics:
        - name: ssim
          settings: { device: cpu, window_size: 11 }
          params: {}
        - name: clipscore
          settings: { device: cuda, model: ViT-B/32 }
          params: { prompt: "a corgi surfing a wave" }

    Returns (parsed, errors):
      parsed: [
        {
          "name": "ssim",
          "cls": <SSIM class>,
          "settings": { "device": "cpu", "window_size": 11 },  # resolved with defaults
          "params": {}
        },
        ...
      ]
      errors: [ ... ]

    Behavior:
    - Unknown metric name -> error (unless allow_unknown_metrics=True, then skip).
    - Unknown settings are ignored (no warnings).
    - Missing required settings -> error for that metric.
    - Params are filtered to declared names; unknown params are dropped.
    """
    parsed: List[MetricParameters] = []
    errors: List[str] = []

    for item in metrics_block:
        name = item.name
        # resolve metric class
        try:
            metric_cls = _get_metric_cls(name)
        except KeyError:
            msg = f"unknown metric '{name}'"
            if allow_unknown_metrics:
                errors.append(msg + " (skipped)")
                continue
            errors.append(msg)
            continue

        # resolve settings (defaults, requireds)
        settings, err = resolve_metric_settings(metric_cls, item.settings)
        if err:
            errors.extend([f"{name}: {e}" for e in err])

        # filter params
        params = filter_metric_params(metric_cls, item.params)

        parsed.append(
            MetricParameters(
                name=name, cls=metric_cls, settings=settings, params=params
            )
        )

    return parsed, errors


# -----------------------
# Convenience for init() calls
# -----------------------


def build_init_map(parsed_metrics: List[MetricParameters]) -> Dict[str, Dict[str, Any]]:
    """
    Convert parsed metrics into { metric_name: resolved_settings } for easy init().
    If multiple entries share the same name, last one wins.
    """
    out: Dict[str, Dict[str, Any]] = {}
    for m in parsed_metrics:
        out[m.name] = m.settings
    return out
