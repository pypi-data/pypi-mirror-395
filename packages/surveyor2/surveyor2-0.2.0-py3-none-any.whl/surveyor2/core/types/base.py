"""Base types for Surveyor2."""

from __future__ import annotations
from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass
import numpy as np
import pathlib

__all__ = ["Frame", "Video", "MetricResult"]

# Basic video processing types
Frame = np.ndarray  # H x W x C, dtype=uint8
MetricResult = Tuple[str, float, Dict[str, Any]]  # (metric_name, score, extras)


@dataclass
class Video:
    """Container for video data with metadata."""
    frames: List[Frame]  # List of H x W x C uint8 frames
    video_path: str  # Path to original video file
    prompt: Optional[str] = None  # Prompt used to generate the video

    def __iter__(self):
        """Make Video iterable, yielding frames."""
        return iter(self.frames)
    
    def __len__(self):
        """Return number of frames."""
        return len(self.frames)
    
    def __getitem__(self, idx):
        """Allow indexing into frames."""
        return self.frames[idx]

    @classmethod
    def from_path(
        cls, uri: str | pathlib.Path, *, max_frames: int | None = None, prompt: Optional[str] = None
    ) -> "Video":
        """
        Decode video from file path and return Video instance.
        Best-effort decoder using imageio. Returns Video with list of HxWxC uint8 frames.
        If imageio is unavailable, raises a clear error.
        """
        try:
            import imageio
        except Exception:
            raise RuntimeError(
                "Video decoding requires imageio. Install with: pip install 'imageio[ffmpeg]'"
            )

        path = uri
        reader = imageio.get_reader(path)
        frames = []
        for i, frame in enumerate(reader):
            frame = frame if frame.ndim == 3 else frame[..., None]
            if frame.shape[2] == 4:  # RGBA -> RGB
                frame = frame[..., :3]
            frames.append(frame.astype(np.uint8))
            if max_frames is not None and len(frames) >= max_frames:
                break
        reader.close()
        return cls(frames=frames, video_path=str(path), prompt=prompt)
