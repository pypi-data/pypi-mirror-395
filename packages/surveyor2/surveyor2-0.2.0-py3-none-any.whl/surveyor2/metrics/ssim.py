from __future__ import annotations
import numpy as np
from typing import Mapping, Any, Optional, Set, List, Tuple
from ..core.metrics_base import Metric
from ..core.registry import register
from ..core.types import Video, MetricResult


@register
class SSIM(Metric):
    """
    Structural Similarity (simplified global SSIM, not windowed).
    - Computes luminance/contrast/structure over the entire frame,
      averages over channels, then averages over frames.
    - Fast, dependency-free; you can replace with a windowed version later.
    """

    name = "ssim"
    requires_reference = True
    higher_is_better = True
    enabled_by_default = False

    @classmethod
    def get_settings(cls) -> dict[str, bool]:
        # constants configurable but optional
        return {"c1": False, "c2": False}

    @classmethod
    def get_setting_defaults(cls) -> dict[str, Any]:
        # Defaults per Wang et al. (scaled for data in [0,1]):
        # C1=(0.01)^2, C2=(0.03)^2
        return {"c1": 0.01**2, "c2": 0.03**2}

    @classmethod
    def get_quality_ranges(cls) -> List[Tuple[float, float, str]]:
        return [
            (0.0, 0.5, "poor"),
            (0.5, 0.7, "fair"),
            (0.7, 0.85, "good"),
            (0.85, 1.0, "excellent"),
        ]

    def init(self, settings: Mapping[str, Any]) -> None:
        self.c1 = float(settings.get("c1", 0.01**2))
        self.c2 = float(settings.get("c2", 0.03**2))

    def _ssim_frame(self, a: np.ndarray, b: np.ndarray) -> float:
        # Inputs: HxWxC, uint8 or float. Normalize to [0,1].
        a = a.astype(np.float32) / 255.0 if a.dtype != np.float32 else np.clip(a, 0, 1)
        b = b.astype(np.float32) / 255.0 if b.dtype != np.float32 else np.clip(b, 0, 1)

        # Compute per-channel global stats
        if a.ndim == 2:
            a = a[..., None]
        if b.ndim == 2:
            b = b[..., None]

        mu_a = a.mean(axis=(0, 1), keepdims=True)
        mu_b = b.mean(axis=(0, 1), keepdims=True)
        var_a = ((a - mu_a) ** 2).mean(axis=(0, 1), keepdims=True)
        var_b = ((b - mu_b) ** 2).mean(axis=(0, 1), keepdims=True)
        cov_ab = ((a - mu_a) * (b - mu_b)).mean(axis=(0, 1), keepdims=True)

        num = (2 * mu_a * mu_b + self.c1) * (2 * cov_ab + self.c2)
        den = (mu_a**2 + mu_b**2 + self.c1) * (var_a + var_b + self.c2) + 1e-12
        ssim_c = num / den  # per-channel
        ssim_val = float(np.mean(ssim_c))
        # Clip to [0,1] for stability on weird inputs
        return float(max(0.0, min(1.0, ssim_val)))

    def evaluate(
        self, video: Video, reference: Optional[Video], params: Mapping[str, Any]
    ) -> MetricResult:
        assert reference is not None, "SSIM requires a reference video"
        A = list(video)
        B = list(reference)
        n = min(len(A), len(B))
        if n == 0:
            return (self.name, float("nan"), {"note": "no overlapping frames"})

        vals = [self._ssim_frame(a, b) for a, b in zip(A[:n], B[:n])]
        score = float(np.mean(vals))
        normalized_score = self.normalize(score)
        return (self.name, normalized_score, {"per_frame": vals, "paired_frames": n})
