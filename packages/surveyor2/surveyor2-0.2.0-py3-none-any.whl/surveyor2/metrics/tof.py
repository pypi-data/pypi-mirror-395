from __future__ import annotations
from typing import Mapping, Any, Optional, Set, List, Tuple
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..core.metrics_base import Metric
from ..core.registry import register
from ..core.types import Video, MetricResult

_FLOW_ERR = (
    "tOF requires 'torch' and 'torchvision' (for optical flow) or 'opencv-python'.\n"
    "Install with one of: pip install torch torchvision  OR  pip install opencv-python"
)


def _compute_optical_flow(
    a: np.ndarray, b: np.ndarray, backend: str
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Return (flow_x, flow_y) arrays for motion from a->b.
    Backends: 'opencv' (Farneback) or 'tvls' (torchvision TV-L1 if available).
    """
    if backend == "opencv":
        try:
            import cv2  # type: ignore
        except Exception as e:
            raise RuntimeError(_FLOW_ERR) from e
        g0 = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
        g1 = cv2.cvtColor(b, cv2.COLOR_RGB2GRAY)
        flow = cv2.calcOpticalFlowFarneback(
            g0,
            g1,
            None,
            pyr_scale=0.5,
            levels=3,
            winsize=15,
            iterations=3,
            poly_n=5,
            poly_sigma=1.2,
            flags=0,
        )
        return flow[..., 0], flow[..., 1]
    else:
        # torchvision TV-L1 fallback
        try:
            import torch
            import torchvision
        except Exception as e:
            raise RuntimeError(_FLOW_ERR) from e

        # Normalize to [0,1] and to CHW
        def to_t(x: np.ndarray) -> "torch.Tensor":
            x = x.astype(np.float32) / 255.0
            if x.ndim == 2:
                x = x[..., None]
            x = x.transpose(2, 0, 1)[None, ...]  # 1,C,H,W
            return torch.from_numpy(x)

        t0 = to_t(a)
        t1 = to_t(b)
        # TV-L1 returns flow in HW2
        of = torchvision.ops.tv_l1_optical_flow(t0, t1)[0].permute(1, 2, 0).numpy()
        return of[..., 0], of[..., 1]


@register
class TOF(Metric):
    """
    Temporal Optical Flow consistency (tOF).
    Measures how consistent motion is across consecutive frames by computing
    optical flow magnitudes and reporting the average magnitude difference
    between consecutive flow fields (lower difference = smoother/consistent).
    """

    name = "tof"
    requires_reference = False
    higher_is_better = True

    @classmethod
    def get_settings(cls) -> dict[str, bool]:
        return {"backend": False, "num_threads": False}

    @classmethod
    def get_setting_defaults(cls) -> dict[str, Any]:
        return {
            "backend": "opencv",
            "num_threads": None,
        }

    @classmethod
    def normalize(cls, value: float) -> float:
        # Normalize TOF and invert so higher normalized score = better
        # TOF typically ranges from 0 upwards, lower is better
        # Use exponential to amplify differences: e^(-k*value)
        import math
        k = 3.0  # steepness factor - higher = more sensitive to changes
        return math.exp(-k * value)

    def init(self, settings: Mapping[str, Any]) -> None:
        self.backend = str(settings.get("backend", "opencv")).lower()
        num_threads = settings.get("num_threads")
        if num_threads is None:
            import os

            # Auto-detect: use CPU count, but cap at reasonable number
            import multiprocessing

            self.num_threads = min(multiprocessing.cpu_count(), 8)
        else:
            self.num_threads = int(num_threads)

    def evaluate(
        self, video: Video, reference: Optional[Video], params: Mapping[str, Any]
    ) -> MetricResult:
        frames = list(video)
        n = len(frames)
        if n < 3:
            return (
                self.name,
                float("nan"),
                {"note": "need >= 3 frames for temporal flow consistency"},
            )

        # Compute all optical flows in parallel
        def compute_flow_pair(i: int) -> Tuple[int, np.ndarray]:
            fx, fy = _compute_optical_flow(frames[i], frames[i + 1], self.backend)
            mag = np.sqrt(fx * fx + fy * fy)
            return i, mag

        # Use threading for I/O-bound operations (OpenCV, torch ops)
        magnitudes = {}
        if self.num_threads > 1 and n > 2:
            with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
                futures = {
                    executor.submit(compute_flow_pair, i): i for i in range(n - 1)
                }
                for future in as_completed(futures):
                    i, mag = future.result()
                    magnitudes[i] = mag
        else:
            # Sequential fallback
            for i in range(n - 1):
                _, mag = compute_flow_pair(i)
                magnitudes[i] = mag

        # Compute differences sequentially (depends on previous magnitude)
        diffs: List[float] = []
        prev_mag = None
        for i in range(n - 1):
            mag = magnitudes[i]
            if prev_mag is not None:
                diffs.append(float(np.mean(np.abs(mag - prev_mag))))
            prev_mag = mag

        score = float(np.mean(diffs)) if diffs else float("nan")
        normalized_score = self.normalize(score) if diffs else float("nan")
        return (self.name, normalized_score, {"per_step_diff": diffs, "steps": len(diffs)})
