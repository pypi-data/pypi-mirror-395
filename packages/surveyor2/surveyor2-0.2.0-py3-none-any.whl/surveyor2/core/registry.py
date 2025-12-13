# vqeval/core/registry.py
from __future__ import annotations
from typing import Dict, Type, List, Any
from .metrics_base import Metric

_REGISTRY: Dict[str, Type[Metric]] = {}


def register(metric_cls: Type[Metric]) -> Type[Metric]:
    name = getattr(metric_cls, "name", None)
    if not name:
        raise ValueError("Metric must define .name")
    _REGISTRY[name] = metric_cls
    return metric_cls


def get_metric_cls(name: str) -> Type[Metric]:
    if name not in _REGISTRY:
        raise KeyError(f"Metric {name} is not registered")
    return _REGISTRY[name]


def get_higher_is_better(name: str) -> bool:
    """All metrics are normalized so higher is always better."""
    return True


def list_metrics() -> list[str]:
    return sorted(_REGISTRY.keys())


def describe_metric(metric_cls: Type[Metric]) -> Dict[str, Any]:
    """
    Return a structured description of one metric:
    {
      "name": "...",
      "enabled_by_default": True,
      "settings": {
         "device": {"required": False, "default": "cuda"},
         "window_size": {"required": False, "default": 11},
         "foo": {"required": True, "default": None}
      },
      "params": ["prompt", "stride"]
    }
    """
    settings_req = metric_cls.get_settings()
    settings_def = metric_cls.get_setting_defaults()

    out_settings: Dict[str, Dict[str, Any]] = {}
    for k, is_req in settings_req.items():
        out_settings[k] = {
            "required": bool(is_req),
            "default": settings_def.get(k, None),
        }

    return {
        "name": getattr(metric_cls, "name", metric_cls.__name__),
        "enabled_by_default": getattr(metric_cls, "enabled_by_default", True),
        "settings": out_settings,
        "params": sorted(list(metric_cls.get_params())),
    }


def describe_all_metrics() -> List[Dict[str, Any]]:
    """
    Describe all registered metrics (for UI/CLI listing).
    """
    names = list_metrics()
    return [describe_metric(get_metric_cls(n)) for n in names]


def print_registered_metrics() -> None:
    """Print all registered metrics with their settings and params."""
    catalog = describe_all_metrics()
    if not catalog:
        print("No metrics registered.")
        return

    catalog.sort(key=lambda d: d["name"])
    for m in catalog:
        enabled_status = "enabled by default" if m.get("enabled_by_default", True) else "disabled by default"
        print(f"- {m['name']} ({enabled_status})")
        if m["settings"]:
            print("    settings:")
            for k in sorted(m["settings"].keys()):
                meta = m["settings"][k]
                req = "required" if meta.get("required") else "optional"
                default = meta.get("default", None)
                if default is None and not meta.get("required"):
                    print(f"      {k}: ({req})")
                else:
                    print(f"      {k}: ({req}), default={default!r}")
        else:
            print("    settings: {}")
        if m.get("params"):
            print("    params:", ", ".join(sorted(m["params"])))
        else:
            print("    params: {}")
