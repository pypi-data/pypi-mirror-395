"""Presets command for listing available metric presets."""

from ..presets import list_presets, get_preset_instance, get_preset
from ..core.types.cli import PresetsArgs


def presets_main(args: PresetsArgs) -> int:
    """Main entry point for the presets command."""
    presets = list_presets()
    
    if not presets:
        print("No presets available.")
        return 0
    
    print("Available metric presets:")
    print()
    
    for preset_name in presets:
        try:
            preset_instance = get_preset_instance(preset_name)
            preset_config = get_preset(preset_name)
            metric_names = [m.name for m in preset_config.metrics]
            print(f"  {preset_name}")
            print(f"    Description: {preset_instance.description}")
            print(f"    Metrics: {', '.join(metric_names)}")
            print()
        except Exception as e:
            print(f"  {preset_name} (error loading: {e})")
            print()
    
    return 0

