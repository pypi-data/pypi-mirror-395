from __future__ import annotations
from typing import Mapping, Any, Optional
import os
import io
import json
import warnings
import logging
import numpy as np
from pathlib import Path

# Suppress warnings from transformers and accelerate
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers.utils.hub")
warnings.filterwarnings("ignore", message=".*Special tokens have been added.*")
warnings.filterwarnings("ignore", message=".*TRANSFORMERS_CACHE.*")

# Suppress transformers logging (including the "Special tokens" warning)
try:
    from transformers import logging as transformers_logging
    transformers_logging.set_verbosity_error()
except ImportError:
    pass

# Suppress INFO level logging from accelerate
logging.getLogger("accelerate.utils.modeling").setLevel(logging.WARNING)

from ..core.metrics_base import Metric
from ..core.registry import register
from ..core.types import Video, MetricResult

# Get the package directory to locate assets
_PACKAGE_DIR = Path(__file__).parent.parent
_ASSETS_DIR = _PACKAGE_DIR / "assets" / "visionreward"
_QUESTIONS_PATH = _ASSETS_DIR / "questions.txt"
_WEIGHT_PATH = _ASSETS_DIR / "weight.json"

_VISIONREWARD_ERR = (
    "VisionReward requires 'torch', 'transformers', and 'decord' packages.\n"
    "Install with: pip install torch transformers decord"
)


@register
class VisionReward(Metric):
    """
    VisionReward: Fine-Grained Multi-Dimensional Human Preference Learning for Video Generation.
    
    VisionReward is a fine-grained, multi-dimensional reward model designed to capture human 
    preferences in videos. It breaks down subjective judgments into interpretable dimensions 
    with weighted scoring.
    
    Settings:
      - device: 'auto' | 'cpu' | 'cuda' (default 'auto')
      - model_path: HuggingFace model path (default: 'THUDM/VisionReward-Video')
      - use_bf16: Use bf16 precision (default: auto-detected based on GPU capability)
    
    Note: Requires 'prompt' in the input item (not a metric parameter).
    """

    name = "visionreward"
    requires_reference = False
    higher_is_better = True  # Higher VisionReward scores are better
    enabled_by_default = True

    @classmethod
    def get_settings(cls) -> dict[str, bool]:
        return {
            "device": False,
            "model_path": False,
            "use_bf16": False,
        }

    @classmethod
    def get_setting_defaults(cls) -> dict[str, Any]:
        return {
            "device": "auto",
            "model_path": "THUDM/VisionReward-Video",
            "use_bf16": None,  # None means auto-detect
        }

    @classmethod
    def get_params(cls) -> set[str]:
        return set()  # prompt comes from InputItem, not metric params

    def init(self, settings: Mapping[str, Any]) -> None:
        """Initialize VisionReward metric."""
        # Set TOKENIZERS_PARALLELISM to avoid fork warning
        # This must be set before importing/using tokenizers
        os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
        
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
            from decord import bridge
        except ImportError as e:
            raise RuntimeError(_VISIONREWARD_ERR) from e

        # Device setup
        self.device = str(settings.get("device", "auto"))
        if self.device == "auto":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = str(self.device)

        # Validate and load questions and weights from assets
        if not _QUESTIONS_PATH.exists():
            raise RuntimeError(
                f"VisionReward questions file not found: {_QUESTIONS_PATH}\n"
                f"Please ensure the surveyor2 package is properly installed with assets."
            )
        if not _WEIGHT_PATH.exists():
            raise RuntimeError(
                f"VisionReward weight file not found: {_WEIGHT_PATH}\n"
                f"Please ensure the surveyor2 package is properly installed with assets."
            )
        
        # Load questions and weights
        with open(_QUESTIONS_PATH, 'r') as f:
            self.questions = [line.strip() for line in f.readlines() if line.strip()]
        
        with open(_WEIGHT_PATH, 'r') as f:
            weight_data = json.load(f)
            self.weight = np.array(weight_data)
        
        # Model path
        self.model_path = str(settings.get("model_path", "THUDM/VisionReward-Video"))
        
        # Precision setup
        use_bf16_setting = settings.get("use_bf16")
        if use_bf16_setting is None:
            # Auto-detect: use bf16 if CUDA is available and GPU supports it (compute capability >= 8)
            if torch.cuda.is_available() and torch.cuda.get_device_capability()[0] >= 8:
                self.torch_type = torch.bfloat16
            else:
                self.torch_type = torch.float16
        elif use_bf16_setting:
            self.torch_type = torch.bfloat16
        else:
            self.torch_type = torch.float16
        
        # Initialize model and tokenizer
        self.torch = torch
        self.bridge = bridge
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True,
            )
            
            load_kwargs = {
                "torch_dtype": self.torch_type,
                "trust_remote_code": True,
                "low_cpu_mem_usage": True,
                "device_map": "auto",
            }
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                **load_kwargs
            ).eval().to(self.device)

    def _load_video(self, video_data: bytes, strategy: str = 'chat'):
        """Load video frames using decord. Exact copy from original inference script."""
        from decord import cpu, VideoReader
        
        self.bridge.set_bridge('torch')
        mp4_stream = video_data
        num_frames = 24
        decord_vr = VideoReader(io.BytesIO(mp4_stream), ctx=cpu(0))

        frame_id_list = None
        total_frames = len(decord_vr)
        if strategy == 'base':
            clip_end_sec = 60
            clip_start_sec = 0
            start_frame = int(clip_start_sec * decord_vr.get_avg_fps())
            end_frame = min(total_frames,
                            int(clip_end_sec * decord_vr.get_avg_fps())) if clip_end_sec is not None else total_frames
            frame_id_list = np.linspace(start_frame, end_frame - 1, num_frames, dtype=int)
        elif strategy == 'chat':
            timestamps = decord_vr.get_frame_timestamp(np.arange(total_frames))
            timestamps = [i[0] for i in timestamps]
            max_second = round(max(timestamps)) + 1
            frame_id_list = []
            for second in range(max_second):
                closest_num = min(timestamps, key=lambda x: abs(x - second))
                index = timestamps.index(closest_num)
                frame_id_list.append(index)
                if len(frame_id_list) >= num_frames:
                    break
        video_data = decord_vr.get_batch(frame_id_list)
        video_data = video_data.permute(3, 0, 1, 2)
        return video_data

    def _inference(self, video_path: str, query: str, temperature: float = 0.1) -> str:
        """Run inference on a single query. Exact copy from original inference script."""
        video_data = open(video_path, 'rb').read()
        strategy = 'chat'
        video = self._load_video(video_data, strategy=strategy)
        
        history = []

        inputs = self.model.build_conversation_input_ids(
            tokenizer=self.tokenizer,
            query=query,
            images=[video],
            history=history,
            template_version=strategy
        )
        inputs = {
            'input_ids': inputs['input_ids'].unsqueeze(0).to(self.device),
            'token_type_ids': inputs['token_type_ids'].unsqueeze(0).to(self.device),
            'attention_mask': inputs['attention_mask'].unsqueeze(0).to(self.device),
            'images': [[inputs['images'][0].to(self.device).to(self.torch_type)]],
        }
        gen_kwargs = {
            "max_new_tokens": 2048,
            "pad_token_id": 128002,
            "top_k": 1,
            "do_sample": False,
            "top_p": 0.1,
            "temperature": temperature,
        }
        with self.torch.no_grad():
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning, module="transformers.generation")
                outputs = self.model.generate(**inputs, **gen_kwargs)
            outputs = outputs[:, inputs['input_ids'].shape[1]]
        
        return self.tokenizer.decode(outputs[0])

    def _score(self, video_path: str, prompt: str) -> float:
        """Calculate VisionReward score for a video. Exact copy from original inference script."""
        queries = [question.replace('[[prompt]]', prompt) for question in self.questions]
        answers = []
        
        for query in queries:
            answer = self._inference(video_path, query)
            answers.append(answer)
        
        answers = np.array([1 if answer == 'yes' else -1 for answer in answers])
        score = np.mean(answers * self.weight).item()
        return score

    def evaluate(
        self, video: Video, reference: Optional[Video], params: Mapping[str, Any]
    ) -> MetricResult:
        """
        Evaluate a video using VisionReward.
        
        Args:
            video: Input video as an iterable of frames
            reference: Not used (VisionReward doesn't require reference videos)
            params: Parameters from pipeline (includes InputItem fields):
                - 'prompt': Text prompt for video evaluation (from InputItem)
                - 'video': Path to the original video file (automatically provided by pipeline)
        
        Returns:
            MetricResult tuple: (metric_name, score, extras_dict)
        """
        # Validate required parameters
        video_path = params.get("video")
        if not video_path:
            return self._error_result("Missing required parameter 'video' (video file path)")

        if not isinstance(video_path, str) or not os.path.exists(video_path):
            return self._error_result(f"Invalid video path: {video_path}")

        prompt = params.get("prompt")
        if not prompt:
            return self._error_result("Missing 'prompt' in input item. VisionReward requires a prompt to evaluate the video.")

        frames = list(video)  # Get frame count

        score = self._score(video_path, prompt)
        
        extras = {
            "prompt": prompt,
            "video_path": video_path,
            "device": self.device,
            "frames": len(frames),
            "num_questions": len(self.questions),
            "torch_dtype": str(self.torch_type),
        }
        
        return (self.name, score, extras)
