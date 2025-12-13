"""Scaffold command for generating YAML scaffold files."""

import pathlib
import sys
from datetime import datetime

from ..core.parser import (
    describe_all_metrics,
    build_default_metrics_config_from_registry,
)
from ..core.types.cli import ScaffoldArgs
from ..metrics import *


def _yaml_scalar(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "null"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    if any(
        ch in s for ch in [":", "#", "{", "}", "[", "]", ",", " ", "\t", "\n", '"', "'"]
    ):
        return f'"{s}"'
    return s


def generate_scaffold_yaml_dynamic(include_all: bool = False) -> str:
    """
    Build a YAML scaffold from whatever metrics are currently registered.
    Required settings without defaults are emitted as commented placeholders.
    
    Args:
        include_all: If True, include all metrics regardless of enabled_by_default.
                     If False, only include metrics with enabled_by_default=True.
    """
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = []
    A = lines.append

    A(f"# Surveyor2 config scaffold (generated {now})")
    A("# Edit this file to point to your inputs and tweak metric settings.\n")

    A("# This scaffold includes only metrics and aggregation.")
    A("# Provide inputs in a separate file with 'inputs: [...]'.\n")

    A("metrics:")
    catalog = sorted(describe_all_metrics(), key=lambda d: d["name"])
    if not include_all:
        catalog = [m for m in catalog if m.get("enabled_by_default", True)]
    _default_cfg = build_default_metrics_config_from_registry()
    _defaults_by_name = {
        m.name: (m.settings or {}) for m in _default_cfg.metrics
    }
    if not catalog:
        A("  []")
    for m in catalog:
        name = m["name"]
        settings = m.get("settings", {})
        params = sorted(m.get("params", []))
        defaults_for_metric = _defaults_by_name.get(name, {})

        A(f"  - name: {name}")
        A("    settings:")

        if settings:
            for key in sorted(settings.keys()):
                meta = settings[key]
                required = bool(meta.get("required", False))
                default = meta.get("default", None)

                if key in defaults_for_metric:
                    A(f"      {key}: {_yaml_scalar(defaults_for_metric[key])}")
                elif required and default is None:
                    A(f"      # {key}: <REQUIRED>")
                elif default is None and not required:
                    A(f"      # {key}: <optional>")
                else:
                    A(f"      {key}: {_yaml_scalar(default)}")
        else:
            A("      {}")

        A("    params:")
        if params:
            for p in params:
                placeholder = ""
                if p.lower() in {"prompt", "caption", "text"}:
                    placeholder = "describe the intended content"
                A(f"      {p}: {_yaml_scalar(placeholder)}")
        else:
            A("      {}")
        A("")

    A("aggregate:")
    A("  # Optional: relative weights for a composite score (metric -> weight)")
    A("  weights:")
    for n in [m["name"] for m in catalog]:
        A(f"    {n}: 1")
    A("")

    return "\n".join(lines) + "\n"


def scaffold_main(args: ScaffoldArgs) -> int:
    """Main entry point for the scaffold command."""
    p = pathlib.Path(args.output)
    p.parent.mkdir(parents=True, exist_ok=True)
    include_all = getattr(args, "all", False)
    p.write_text(generate_scaffold_yaml_dynamic(include_all=include_all))
    print(f"Wrote scaffold to {p}")
    return 0
