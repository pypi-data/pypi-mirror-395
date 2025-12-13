"""Utility functions for surveyor2."""

from __future__ import annotations
from typing import Any, Iterable, TypeVar, Optional
import os, sys

T = TypeVar("T")


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GREY = "\033[90m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def colorize(text: str, color: str) -> str:
    """Apply color to text if terminal supports it."""
    if os.getenv("NO_COLOR") or not sys.stdout.isatty():
        return text
    return f"{color}{text}{Colors.END}"


def format_percentage_diff(
    pct_diff: Optional[float], higher_is_better: bool = True
) -> str:
    """
    Format percentage difference with color coding.
    All metrics are normalized so higher is always better.

    Args:
        pct_diff: Percentage difference value
        higher_is_better: Kept for compatibility, always True
    """
    if pct_diff is None:
        return ""

    pct_str = f"{pct_diff:+.2f}%"
    
    if abs(pct_diff) < 5.0:
        if pct_diff > 0:
            return colorize(f"{pct_str} (better)", Colors.GREY)
        elif pct_diff < 0:
            return colorize(f"{pct_str} (worse)", Colors.GREY)
        else:
            return colorize(f"{pct_str} (same)", Colors.GREY)
    
    if pct_diff > 0:
        return colorize(f"{pct_str} (better)", Colors.GREEN)
    elif pct_diff < 0:
        return colorize(f"{pct_str} (worse)", Colors.RED)
    else:
        return f"{pct_str} (same)"


def torch_resolve_device(device_setting: str, metric_name: str = "metric") -> str:
    try:
        import torch
    except ImportError as e:
        raise RuntimeError(f"{metric_name} requires 'torch' package.") from e

    if device_setting == "auto":
        if torch.cuda.is_available():
            return "cuda"
        else:
            if not os.getenv("NO_COLOR") and sys.stderr.isatty():
                msg = f"{Colors.YELLOW}⚠ CUDA not available for {metric_name}. Falling back to CPU.{Colors.END}"
            else:
                msg = f"⚠ CUDA not available for {metric_name}. Falling back to CPU."
            print(msg, file=sys.stderr)
            return "cpu"
    return device_setting


def with_progress(
    iterable: Iterable[T],
    desc: str = "Processing",
    unit: str = "item",
    total: int | None = None,
    position: int | None = None,
    silent: bool = False,
) -> Iterable[T]:
    """
    Wrap an iterable with tqdm progress bar if available, otherwise return as-is.

    Args:
        iterable: The iterable to wrap
        desc: Description for the progress bar
        unit: Unit label for the progress bar
        total: Total number of items (if known, improves accuracy)
        position: Position for nested progress bars (0=top, 1=below, etc.)
                  If None, auto-detects nesting level
        silent: If True, disable progress bars and return iterable as-is

    Returns:
        The iterable wrapped with tqdm if available, otherwise the original iterable
    """
    if silent:
        return iterable
    
    try:
        from tqdm import tqdm

        # Auto-detect nesting level if position not specified
        if position is None:
            try:
                # Count active tqdm instances to determine position
                if hasattr(tqdm, "_instances"):
                    position = len(
                        [inst for inst in tqdm._instances if inst is not None]
                    )
                else:
                    position = 0
            except Exception:
                position = 0

        return tqdm(
            iterable, desc=desc, unit=unit, total=total, position=position, leave=False
        )
    except ImportError:
        return iterable
