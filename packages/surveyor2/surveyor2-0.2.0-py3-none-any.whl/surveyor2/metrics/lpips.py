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
    "LPIPS requires 'torch' and 'lpips' packages. "
    "Install with: pip install torch lpips"
)


def _to_torch_image_batch(frames: List[np.ndarray], device: str):
    try:
        import torch
    except Exception as e:
        raise RuntimeError(_TORCH_ERR) from e
    # frames: list of HxWxC uint8/float
    # Vectorized batch conversion for better performance
    frames_array = np.stack(frames, axis=0)  # B,H,W,C

    if frames_array.dtype != np.float32:
        frames_array = frames_array.astype(np.float32) / 255.0  # [0,1]
    else:
        frames_array = np.clip(frames_array, 0, 1)

    frames_array = frames_array * 2.0 - 1.0  # [-1,1] as expected by LPIPS
    frames_array = np.transpose(frames_array, (0, 3, 1, 2))  # B,C,H,W
    t = torch.from_numpy(frames_array).to(device, non_blocking=True)
    return t


@register
class LPIPS(Metric):
    """
    LPIPS (Learned Perceptual Image Patch Similarity), averaged over frames.
    Requires a reference video.
    Settings:
      - device (optional, default 'cuda' if available else 'cpu')
      - backbone (optional, default 'vgg')  # 'vgg'|'alex'|'squeeze'
      - batch_size (optional, default 8)
      - num_threads (optional, default None - uses all available CPU threads)
    """

    name = "lpips"
    requires_reference = True
    higher_is_better = True
    supports_batch = False

    @classmethod
    def get_settings(cls) -> dict[str, bool]:
        return {
            "device": False,
            "backbone": False,
            "batch_size": False,
            "num_threads": False,
        }

    @classmethod
    def get_setting_defaults(cls) -> dict[str, Any]:
        return {
            "device": "auto",
            "backbone": "vgg",
            "batch_size": 8,
            "num_threads": None,
        }

    @classmethod
    def normalize(cls, value: float) -> float:
        return 1.0 - value

    def init(self, settings: Mapping[str, Any]) -> None:
        try:
            import torch
            import lpips as _lpips
        except Exception as e:
            raise RuntimeError(_TORCH_ERR) from e

        self.device = torch_resolve_device(str(settings.get("device", "auto")), "LPIPS")

        self.backbone = str(settings.get("backbone", "vgg"))
        self.batch_size = int(settings.get("batch_size", 8))

        num_threads = settings.get("num_threads")
        if num_threads is not None:
            torch.set_num_threads(int(num_threads))
        elif self.device == "cpu":
            env_threads = os.environ.get(
                "OMP_NUM_THREADS", os.environ.get("MKL_NUM_THREADS")
            )
            if env_threads:
                torch.set_num_threads(int(env_threads))

        # Suppress LPIPS initialization logs
        with open(os.devnull, 'w') as devnull:
            with redirect_stdout(devnull), redirect_stderr(devnull):
                self._lpips = _lpips.LPIPS(net=self.backbone).to(self.device).eval()

        if self.device.startswith("cuda"):
            torch.backends.cudnn.benchmark = True

    def evaluate(
        self,
        video: Video,
        reference: Optional[Video],
        params: Mapping[str, Any],
    ) -> MetricResult:
        if reference is None:
            raise ValueError("LPIPS requires a reference video")
        A = list(video)
        B = list(reference)
        n = min(len(A), len(B))
        if n == 0:
            return (self.name, float("nan"), {"note": "no overlapping frames"})

        try:
            import torch
        except Exception as e:
            raise RuntimeError(_TORCH_ERR) from e

        per_frame = []
        bs = max(1, self.batch_size)
        for i in range(0, n, bs):
            a_batch = A[i : i + bs]
            b_batch = B[i : i + bs]
            xa = _to_torch_image_batch(a_batch, self.device)
            xb = _to_torch_image_batch(b_batch, self.device)
            with torch.no_grad():
                d = self._lpips(xa, xb).view(-1)
                if self.device.startswith("cuda"):
                    d = d.cpu()
                per_frame.extend(d.numpy().tolist())

        score = float(np.mean(per_frame))
        normalized_score = self.normalize(score)
        return (self.name, normalized_score, {"per_frame": per_frame, "paired_frames": n})
