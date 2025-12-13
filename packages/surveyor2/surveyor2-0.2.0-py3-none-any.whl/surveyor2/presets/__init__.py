"""Metrics presets for Surveyor2.

This module provides pre-configured ProfileConfig presets for common metric combinations.
Presets are stored as Python scripts in this directory, each containing a class that inherits from ProfilePreset.
"""

from __future__ import annotations
import importlib
import pkgutil
from pathlib import Path
from typing import Dict, Optional
from abc import ABC, abstractmethod
from ..core.types.config import ProfileConfig


class ProfilePreset(ABC):
    """Base class for metric presets.
    
    Subclasses should implement the get_preset() method to return a ProfileConfig instance.
    """

    @abstractmethod
    def get_preset(self) -> ProfileConfig:
        """Get the ProfileConfig for this preset.
        
        Returns:
            ProfileConfig instance configured with the preset's metrics and aggregation settings
        """
        pass

    @property
    def name(self) -> str:
        """Get the name of this preset (defaults to class name in lowercase)."""
        return self.__class__.__name__.lower()

    @property
    def description(self) -> str:
        """Get the description of this preset (defaults to class docstring)."""
        doc = self.__class__.__doc__
        if doc:
            # Extract the first non-empty line from the docstring
            lines = [line.strip() for line in doc.split('\n') if line.strip()]
            if lines:
                return lines[0]
        return "No description available."

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"


# Registry of available presets (maps preset name -> preset instance)
_PRESETS: Dict[str, ProfilePreset] = {}
_PRESET_MODULES: Dict[str, str] = {}


def _discover_presets() -> None:
    """Discover and load all preset classes."""
    if _PRESETS:
        return  # Already loaded

    # Get the directory containing this __init__.py
    presets_dir = Path(__file__).parent

    # Import all modules in this directory (except __init__.py and __pycache__)
    for module_info in pkgutil.iter_modules([str(presets_dir)]):
        module_name = module_info.name
        if module_name == "__init__":
            continue

        try:
            # Import the module
            full_module_name = f"{__name__}.{module_name}"
            module = importlib.import_module(full_module_name)

            # Look for classes that inherit from ProfilePreset
            # Use getattr with default to avoid AttributeError, and check module's __dict__
            # to only consider attributes defined in the module itself
            for attr_name in getattr(module, "__all__", None) or dir(module):
                if attr_name.startswith("_"):
                    continue  # Skip private attributes
                try:
                    attr = getattr(module, attr_name)
                    if (
                        isinstance(attr, type)
                        and issubclass(attr, ProfilePreset)
                        and attr is not ProfilePreset
                        and attr.__module__ == full_module_name  # Only classes defined in this module
                    ):
                        # Found a preset class, instantiate it
                        preset_instance = attr()
                        preset_name = preset_instance.name
                        _PRESETS[preset_name] = preset_instance
                        _PRESET_MODULES[preset_name] = full_module_name
                except (AttributeError, TypeError):
                    # Skip attributes that can't be checked
                    continue
        except Exception as e:
            # Skip modules that fail to load
            import warnings
            warnings.warn(
                f"Failed to load preset '{module_name}': {e}",
                UserWarning,
            )


def list_presets() -> list[str]:
    """List all available preset names.

    Returns:
        List of preset names (e.g., ['basic', 'perceptual', 'comprehensive'])
    """
    _discover_presets()
    return sorted(_PRESETS.keys())


def get_preset(name: str) -> ProfileConfig:
    """Get a preset configuration by name.

    Args:
        name: Name of the preset (e.g., 'basic', 'perceptual')

    Returns:
        ProfileConfig instance for the requested preset

    Raises:
        ValueError: If the preset name is not found
    """
    _discover_presets()
    if name not in _PRESETS:
        available = ", ".join(list_presets())
        raise ValueError(
            f"Preset '{name}' not found. Available presets: {available}"
        )
    preset_instance = _PRESETS[name]
    return preset_instance.get_preset()


def load_preset(name: str) -> ProfileConfig:
    """Load a preset by name (alias for get_preset).

    Args:
        name: Name of the preset

    Returns:
        ProfileConfig instance for the requested preset

    Raises:
        ValueError: If the preset name is not found
    """
    return get_preset(name)


def get_preset_instance(name: str) -> ProfilePreset:
    """Get a preset instance by name.

    Args:
        name: Name of the preset

    Returns:
        ProfilePreset instance

    Raises:
        ValueError: If the preset name is not found
    """
    _discover_presets()
    if name not in _PRESETS:
        available = ", ".join(list_presets())
        raise ValueError(
            f"Preset '{name}' not found. Available presets: {available}"
        )
    return _PRESETS[name]


__all__ = [
    "ProfilePreset",
    "list_presets",
    "get_preset",
    "load_preset",
    "get_preset_instance",
    "ProfileConfig",
]

