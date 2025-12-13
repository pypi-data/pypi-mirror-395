from __future__ import annotations
from typing import Mapping, Any, Optional, Set, List
import warnings
import numpy as np
import os
from contextlib import redirect_stdout, redirect_stderr

# Suppress warnings from lpips and torchvision
warnings.filterwarnings("ignore", category=UserWarning, module="torchvision")
warnings.filterwarnings("ignore", category=FutureWarning, module="lpips")
warnings.filterwarnings("ignore", message=".*Model configuration not found.*")
warnings.filterwarnings("ignore", message=".*pretrained.*deprecated.*")
warnings.filterwarnings("ignore", message=".*weights.*deprecated.*")
warnings.filterwarnings("ignore", message=".*torch.load.*weights_only.*")

from ..core.metrics_base import Metric
from ..core.registry import register
from ..core.types import Video, MetricResult
from ..core.utils import torch_resolve_device

_TORCH_ERR = (
    "tLPIPS requires 'torch' and 'lpips' packages.\n"
    "Install with: pip install torch lpips"
)


def _to_torch_batch(frames: List[np.ndarray], device: str):
    try:
        import torch
    except Exception as e:
        raise RuntimeError(_TORCH_ERR) from e
    xs = []
    for f in frames:
        if f.dtype != np.float32:
            x = f.astype(np.float32) / 255.0
        else:
            x = np.clip(f, 0, 1)
        x = x * 2.0 - 1.0
        x = np.transpose(x, (2, 0, 1))
        xs.append(x)
    X = np.stack(xs, axis=0)
    return torch.from_numpy(X).to(device)


@register
class TLPIPS(Metric):
    """
    Temporal LPIPS (flicker): LPIPS between consecutive frames within the same video.
    Higher values indicate more temporal inconsistency (more flicker).
    """

    name = "t_lpips"
    requires_reference = False
    higher_is_better = True
    supports_batch = False

    @classmethod
    def get_settings(cls) -> dict[str, bool]:
        return {"device": False, "backbone": False, "batch_size": False}

    @classmethod
    def get_setting_defaults(cls) -> dict[str, Any]:
        return {"device": "auto", "backbone": "vgg", "batch_size": 8}

    @classmethod
    def normalize(cls, value: float) -> float:
        # Normalize TLPIPS and invert so higher normalized score = better
        # TLPIPS typically ranges from 0 to ~1, lower is better
        # Use exponential to amplify differences: e^(-k*value)
        import math
        k = 5.0  # steepness factor - higher = more sensitive to changes
        return math.exp(-k * value)

    def init(self, settings: Mapping[str, Any]) -> None:
        try:
            import torch
            import lpips as _lpips
        except Exception as e:
            raise RuntimeError(_TORCH_ERR) from e

        self.device = torch_resolve_device(str(settings.get("device", "auto")), "TLPIPS")

        self.backbone = str(settings.get("backbone", "vgg"))
        self.batch_size = int(settings.get("batch_size", 8))
        
        # Suppress LPIPS initialization logs
        with open(os.devnull, 'w') as devnull:
            with redirect_stdout(devnull), redirect_stderr(devnull):
                self._lpips = _lpips.LPIPS(net=self.backbone).to(self.device).eval()

    def evaluate(
        self, video: Video, reference: Optional[Video], params: Mapping[str, Any]
    ) -> MetricResult:
        frames = list(video)
        n = len(frames)
        if n < 2:
            return (
                self.name,
                float("nan"),
                {"note": "need >= 2 frames for temporal LPIPS"},
            )

        per_step: List[float] = []
        bs = max(1, self.batch_size)
        # We compute LPIPS over pairs (f_t, f_{t+1}). Batch these pairs.
        pairs: List[List[np.ndarray]] = []
        for i in range(n - 1):
            pairs.append([frames[i], frames[i + 1]])

        try:
            import torch
        except Exception as e:
            raise RuntimeError(_TORCH_ERR) from e

        for i in range(0, len(pairs), bs):
            chunk = pairs[i : i + bs]
            a = [p[0] for p in chunk]
            b = [p[1] for p in chunk]
            xa = _to_torch_batch(a, self.device)
            xb = _to_torch_batch(b, self.device)
            with torch.no_grad():
                d = self._lpips(xa, xb).view(-1).detach().cpu().numpy()
            per_step.extend(d.tolist())

        score = float(np.mean(per_step))
        normalized_score = self.normalize(score)
        return (self.name, normalized_score, {"per_step": per_step, "steps": len(per_step)})
