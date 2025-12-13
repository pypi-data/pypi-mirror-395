from __future__ import annotations
from typing import Mapping, Any, Optional, Set, List, Tuple
import warnings
import logging
import numpy as np

# Suppress warnings from CLIP/open_clip
warnings.filterwarnings("ignore", message=".*Model configuration not found.*")
warnings.filterwarnings("ignore", message=".*SimpleTokenizer.*")
warnings.filterwarnings(
    "ignore", category=UserWarning, message=".*Model configuration not found.*"
)
warnings.filterwarnings("ignore", category=UserWarning, message=".*SimpleTokenizer.*")
warnings.filterwarnings("ignore", module="open_clip")
warnings.filterwarnings("ignore", module="clip")

# Suppress logging warnings from open_clip/clip
logging.getLogger("open_clip").setLevel(logging.ERROR)
logging.getLogger("clip").setLevel(logging.ERROR)
logging.getLogger().addFilter(
    lambda record: "Model configuration not found" not in record.getMessage()
)

from ..core.metrics_base import Metric
from ..core.registry import register
from ..core.types import Video, MetricResult
from ..core.utils import torch_resolve_device

_OPENCLIP_ERR = (
    "CLIPScore requires 'torch' and either 'open_clip_torch' or 'clip'. "
    "Install with: pip install torch open_clip_torch  (or pip install clip)."
)


def _load_openclip(model_name: str, device: str):
    import open_clip

    model, _, preprocess = open_clip.create_model_and_transforms(
        model_name, pretrained="laion2b_s34b_b79k", device=device
    )
    tokenizer = open_clip.get_tokenizer(model_name)
    return model, preprocess, tokenizer


def _load_clip(device: str):
    import clip

    model, preprocess = clip.load("ViT-B/32", device=device)
    return model, preprocess, clip.tokenize


def _frames_to_tensor(frames: List[np.ndarray], preprocess, device: str):
    # preprocess expects PIL Image; convert np array → PIL
    from PIL import Image
    import torch

    imgs = []
    for f in frames:
        if f.dtype != np.uint8:
            arr = np.clip(f, 0, 1)
            arr = (arr * 255.0).astype(np.uint8)
        else:
            arr = f
        if arr.ndim == 2:
            arr = np.stack([arr] * 3, axis=-1)
        img = Image.fromarray(arr)
        imgs.append(preprocess(img))
    batch = torch.stack(imgs, dim=0).to(device)
    return batch


@register
class CLIPScore(Metric):
    """
    Average cosine similarity between prompt embedding and per-frame CLIP image embeddings.
    Settings:
      - device: 'auto' | 'cpu' | 'cuda' (default 'auto')
      - model: open_clip model name or 'clip' (default 'ViT-B/32')
      - batch_size: int (default 16)
      - backend: 'openclip' | 'clip' | 'auto' (default 'auto')
    Params:
      - prompt: required at runtime (string)
    """

    name = "clipscore"
    requires_reference = False
    higher_is_better = True
    enabled_by_default = False
    supports_batch = True

    @classmethod
    def get_settings(cls) -> dict[str, bool]:
        return {"device": False, "model": False, "batch_size": False, "backend": False}

    @classmethod
    def get_setting_defaults(cls) -> dict[str, Any]:
        return {
            "device": "auto",
            "model": "ViT-B/32",
            "batch_size": 16,
            "backend": "auto",
        }

    def init(self, settings: Mapping[str, Any]) -> None:
        self.device = torch_resolve_device(str(settings.get("device", "auto")), "CLIPScore")
        self.model_name = str(settings.get("model", "ViT-B/32"))
        self.batch_size = int(settings.get("batch_size", 16))
        backend = str(settings.get("backend", "auto"))

        # Try open_clip first unless user forces 'clip'
        self.backend = None
        self.model = None
        self.preprocess = None
        self.tokenizer = None

        try:
            import torch  # noqa: F401
        except Exception as e:
            raise RuntimeError(_OPENCLIP_ERR) from e

        if backend in ("auto", "openclip"):
            try:
                self.model, self.preprocess, self.tokenizer = _load_openclip(
                    self.model_name, self.device
                )
                self.backend = "openclip"
            except Exception:
                if backend == "openclip":
                    raise
        if self.backend is None:
            try:
                self.model, self.preprocess, self.tokenizer = _load_clip(self.device)
                self.backend = "clip"
            except Exception as e:
                raise RuntimeError(_OPENCLIP_ERR) from e

        # put model in eval
        try:
            import torch

            self.model.eval()
            # Some open_clip models return (features, logit_scale); we just use features.
            self.torch = torch
        except Exception as e:
            raise RuntimeError(_OPENCLIP_ERR) from e

    def _embed_text(self, prompt: str):
        if not prompt:
            raise ValueError("CLIPScore requires 'prompt' param")
        
        with self.torch.no_grad():
            if self.backend == "openclip":
                tokens = self.tokenizer([prompt])
                tokens = tokens.to(self.device)
                txt = self.model.encode_text(tokens)
            else:
                try:
                    tokens = self.tokenizer([prompt], truncate=True).to(self.device)
                    txt = self.model.encode_text(tokens)
                except (TypeError, RuntimeError) as e:
                    if "too long" in str(e).lower() or "context length" in str(e).lower():
                        words = prompt.split()
                        truncated_prompt = ' '.join(words[:75])
                        tokens = self.tokenizer([truncated_prompt]).to(self.device)
                        txt = self.model.encode_text(tokens)
                    else:
                        raise
            txt = txt / txt.norm(dim=-1, keepdim=True)
        return txt  # [1,D]

    def _embed_images(self, frames: List[np.ndarray]):
        batch = _frames_to_tensor(frames, self.preprocess, self.device)
        with self.torch.no_grad():
            img = self.model.encode_image(batch)
            img = img / img.norm(dim=-1, keepdim=True)
        return img  # [B,D]

    def evaluate(
        self,
        video: Video,
        reference: Optional[Video],
        params: Mapping[str, Any],
    ) -> MetricResult:
        prompt = str(params.get("prompt", ""))
        if not prompt:
            raise ValueError("CLIPScore requires 'prompt' in the inputs item")
        txt = self._embed_text(prompt)

        frames = list(video)
        n = len(frames)
        if n == 0:
            return (self.name, float("nan"), {"note": "no frames", "prompt": prompt})

        sims = []
        bs = max(1, self.batch_size)
        for i in range(0, n, bs):
            img = self._embed_images(frames[i : i + bs])
            # cosine similarity with broadcast: [B,D] · [1,D] -> [B]
            sim = (img @ txt.T).squeeze(-1)
            sims.extend(sim.detach().cpu().tolist())

        score = float(np.mean(sims))
        normalized_score = self.normalize(score)
        return (
            self.name,
            normalized_score,
            {"per_frame": sims, "prompt": prompt, "backend": self.backend},
        )

    def evaluate_batch(
        self, 
        videos: List[Video], 
        references: List[Optional[Video]], 
        params_list: List[Mapping[str, Any]]
    ) -> List[MetricResult]:
        results = []
        for video, reference, params in zip(videos, references, params_list):
            prompt = str(params.get("prompt", ""))
            if not prompt:
                results.append((self.name, float("nan"), {"error": "CLIPScore requires 'prompt' in the inputs item"}))
                continue
            
            txt = self._embed_text(prompt)
            frames = list(video)
            n = len(frames)
            if n == 0:
                results.append((self.name, float("nan"), {"note": "no frames", "prompt": prompt}))
                continue

            sims = []
            bs = max(1, self.batch_size)
            for i in range(0, n, bs):
                img = self._embed_images(frames[i : i + bs])
                sim = (img @ txt.T).squeeze(-1)
                sims.extend(sim.detach().cpu().tolist())

            score = float(np.mean(sims))
            normalized_score = self.normalize(score)
            results.append((
                self.name,
                normalized_score,
                {"per_frame": sims, "prompt": prompt, "backend": self.backend},
            ))
        
        return results
