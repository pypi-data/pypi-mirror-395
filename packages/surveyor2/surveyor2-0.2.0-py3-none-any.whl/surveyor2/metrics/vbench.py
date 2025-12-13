from __future__ import annotations
from typing import Mapping, Any, Optional, List
import tempfile
import os
import warnings
import logging
from contextlib import redirect_stdout, redirect_stderr

from ..core.metrics_base import Metric
from ..core.registry import register
from ..core.types import Video, MetricResult
from ..core.utils import torch_resolve_device

_VBENCH_ERR = (
    "VBench metrics require the 'vbench' package.\n"
    "Install with: pip install vbench"
)

# VBench evaluation dimensions (10 key dimensions) with their configuration
VBENCH_DIMENSIONS = {
    "subject_consistency": {
        "higher_is_better": True,
        "enabled_by_default": True,
    },
    "background_consistency": {
        "higher_is_better": True,
        "enabled_by_default": True,
    },
    "temporal_flickering": {
        "higher_is_better": False,  # Lower flickering is better
        "enabled_by_default": True,
    },
    "motion_smoothness": {
        "higher_is_better": True,
        "enabled_by_default": True,
    },
    "dynamic_degree": {
        "higher_is_better": True,
        "enabled_by_default": False,
    },
    "aesthetic_quality": {
        "higher_is_better": True,
        "enabled_by_default": False,
    },
    "imaging_quality": {
        "higher_is_better": True,
        "enabled_by_default": True,
    },
    "human_action": {
        "higher_is_better": True,
        "enabled_by_default": False,
    },
    "temporal_style": {
        "higher_is_better": True,
        "enabled_by_default": False,
    },
    "overall_consistency": {
        "higher_is_better": True,
        "enabled_by_default": True,
    },
}


class VBenchMetricBase(Metric):
    """
    Base class for VBench metrics. Can be instantiated with any of the 10 key VBench dimensions.
    
    VBench is a comprehensive evaluation benchmark for text-to-video generation models.
    This implementation includes 10 key quality dimensions for video evaluation.
    """

    requires_reference = False
    supports_batch = True
    higher_is_better = True

    def __init__(self, dimension: str):
        """
        Initialize a VBench metric for a specific dimension.
        
        Args:
            dimension: One of the 10 key VBench evaluation dimensions
        """
        if dimension not in VBENCH_DIMENSIONS:
            raise ValueError(
                f"Invalid VBench dimension '{dimension}'. "
                f"Must be one of: {', '.join(VBENCH_DIMENSIONS.keys())}"
            )
        self.dimension = dimension
        self.name = f"vbench_{dimension}"
        self._vbench_kwargs = None

    @classmethod
    def get_settings(cls) -> dict[str, bool]:
        """Settings for VBench metric."""
        return {
            "device": False,
        }

    @classmethod
    def get_setting_defaults(cls) -> dict[str, Any]:
        """Default values for VBench settings."""
        return {
            "device": "auto",
        }

    def init(self, settings: Mapping[str, Any]) -> None:
        """Initialize the VBench evaluator for this dimension."""
        try:
            # Suppress warnings during VBench import
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                from vbench import VBench
                import vbench as vbench_module
        except ImportError as e:
            raise RuntimeError(_VBENCH_ERR) from e

        # Disable all VBench logging permanently
        logging.getLogger('vbench').setLevel(logging.CRITICAL + 1)

        self.device = torch_resolve_device(str(settings.get("device", "auto")), "VBench")
        
        # Auto-detect VBench package directory (internal - not user-configurable)
        # Note: full_info_dir is required by VBench constructor for initialization,
        # but we use mode='custom_input' to evaluate with custom prompts instead
        # of VBench's standard benchmark prompts
        import os
        self.full_info_dir = os.path.dirname(vbench_module.__file__)
        
        # Store VBench initialization kwargs for creating instances per evaluation
        self._vbench_kwargs = {
            "device": self.device,
            "full_info_dir": self.full_info_dir,
        }

    def _set_all_errors(self, video_info: List[Dict], results: List, error_msg: str) -> None:
        """Helper to set error result for all videos in video_info."""
        for info in video_info:
            if results[info["result_index"]] is None:
                results[info["result_index"]] = self._error_result(error_msg)
    
    def _parse_vbench_results(
        self, 
        output_dir: str, 
        eval_name: str, 
        video_info: List[Dict], 
        results: List
    ) -> None:
        """Parse VBench results file and populate results list."""
        import json
        import math
        
        results_file = os.path.join(output_dir, f"{eval_name}_eval_results.json")
        
        if not os.path.exists(results_file):
            self._set_all_errors(video_info, results, f"VBench results file not found: {results_file}")
            return
        
        with open(results_file, 'r') as f:
            vbench_results = json.load(f)
        
        if not vbench_results or self.dimension not in vbench_results:
            available_dims = list(vbench_results.keys()) if vbench_results else []
            self._set_all_errors(video_info, results, 
                f"Dimension '{self.dimension}' not in results. Available: {available_dims}")
            return
        
        dimension_result = vbench_results[self.dimension]
        
        # Handle list format: [avg_score, [score1, score2, ...]]
        if not isinstance(dimension_result, list) or len(dimension_result) <= 1:
            self._set_all_errors(video_info, results,
                f"Unexpected VBench result format: {type(dimension_result).__name__}")
            return
        
        per_video_results = dimension_result[1]
        
        if not isinstance(per_video_results, list):
            self._set_all_errors(video_info, results,
                f"Expected list of scores, got {type(per_video_results).__name__}")
            return
        
        if len(per_video_results) != len(video_info):
            self._set_all_errors(video_info, results,
                f"VBench returned {len(per_video_results)} scores but expected {len(video_info)}")
            return
        
        # Process individual video scores
        for info, score_data in zip(video_info, per_video_results):
            try:
                if isinstance(score_data, dict):
                    score = float(score_data.get("video_results", score_data))
                else:
                    score = float(score_data)
                
                if math.isnan(score):
                    results[info["result_index"]] = self._error_result(
                        f"VBench returned nan for {self.dimension}")
                else:
                    normalized_score = self.__class__.normalize(score)
                    extras = {
                        "dimension": self.dimension,
                        "prompt": info["prompt"],
                        "frames": len(info["frames"]),
                        "video_path": info["video_path"],
                    }
                    if isinstance(score_data, dict):
                        extras["vbench_metadata"] = score_data
                    results[info["result_index"]] = (self.name, normalized_score, extras)
            except (ValueError, TypeError, KeyError) as e:
                results[info["result_index"]] = self._error_result(
                    f"Failed to extract score from: {score_data}")

    def _evaluate_batch_internal(
        self, 
        videos: List[Video], 
        references: List[Optional[Video]], 
        params_list: List[Mapping[str, Any]]
    ) -> List[MetricResult]:
        """
        Internal method to evaluate multiple videos using VBench.
        
        Args:
            videos: List of Video objects
            references: List of optional reference Video objects (not used)
            params_list: List of parameter dicts, each containing:
                - 'prompt': Text prompt for text-to-video evaluation (required)
                - 'video': Path to the original video file (required)
        
        Returns:
            List of MetricResult tuples
        """
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                from vbench import VBench
        except ImportError:
            return [self._error_result("VBench not installed") for _ in videos]
        
        results = []
        video_info = []
        
        for idx, (video, params) in enumerate(zip(videos, params_list)):
            video_path = params.get("video")
            if not video_path:
                results.append(self._error_result("Missing required parameter 'video' (video file path)"))
                continue
            
            if not isinstance(video_path, str) or not os.path.exists(video_path):
                results.append(self._error_result(f"Invalid video path: {video_path}"))
                continue
            
            prompt = params.get("prompt")
            if not prompt:
                results.append(self._error_result("Missing required parameter 'prompt'"))
                continue
            
            frames = list(video)
            video_basename = os.path.basename(video_path)
            name, ext = os.path.splitext(video_basename)
            unique_filename = f"{name}_{idx}{ext}"
            
            video_info.append({
                "video_path": video_path,
                "video_filename": unique_filename,
                "video_basename": video_basename,
                "prompt": prompt,
                "frames": frames,
                "result_index": len(results)
            })
            results.append(None)
        
        if not video_info:
            return results
        
        with tempfile.TemporaryDirectory(prefix="vbench_output_") as output_dir:
            with tempfile.TemporaryDirectory(prefix="vbench_videos_") as video_temp_dir:
                try:
                    prompt_dict = {}
                    for info in video_info:
                        video_symlink = os.path.join(video_temp_dir, info["video_filename"])
                        os.symlink(info["video_path"], video_symlink)
                        prompt_dict[info["video_filename"]] = info["prompt"]
                    
                    vbench_kwargs = dict(self._vbench_kwargs)
                    vbench_kwargs["output_path"] = output_dir
                    vbench_instance = VBench(**vbench_kwargs)
                    
                    eval_name = f"eval_{self.dimension}"
                    
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        with open(os.devnull, 'w') as devnull:
                            with redirect_stdout(devnull), redirect_stderr(devnull):
                                vbench_instance.evaluate(
                                    videos_path=video_temp_dir,
                                    name=eval_name,
                                    prompt_list=prompt_dict,
                                    dimension_list=[self.dimension],
                                    mode="custom_input",
                                )
                    
                    self._parse_vbench_results(output_dir, eval_name, video_info, results)
                        
                except Exception as e:
                    self._set_all_errors(video_info, results, f"Evaluation failed: {str(e)}")
        
        return results

    def evaluate(
        self, video: Video, reference: Optional[Video], params: Mapping[str, Any]
    ) -> MetricResult:
        """
        Evaluate a video using the VBench dimension.
        
        Args:
            video: Input video as an iterable of frames
            reference: Not used (VBench doesn't require reference videos)
            params: Required parameters:
                - 'prompt': Text prompt for text-to-video evaluation (required)
                - 'video': Path to the original video file (required, automatically provided by pipeline)
        
        Returns:
            MetricResult tuple: (metric_name, score, extras_dict)
        """
        results = self._evaluate_batch_internal([video], [reference], [params])
        return results[0]

    def evaluate_batch(
        self, 
        videos: List[Video], 
        references: List[Optional[Video]], 
        params_list: List[Mapping[str, Any]]
    ) -> List[MetricResult]:
        """
        Evaluate multiple videos using VBench in batch mode.
        
        Args:
            videos: List of Video objects
            references: List of optional reference Video objects (not used)
            params_list: List of parameter dicts for each video
        
        Returns:
            List of MetricResult tuples
        """
        return self._evaluate_batch_internal(videos, references, params_list)


# Register all 10 VBench dimensions as separate metrics
def _create_vbench_metric_class(dimension: str) -> type:
    """Factory function to create a VBench metric class for a specific dimension."""
    
    class_name = f"VBench_{dimension.title().replace('_', '')}"
    
    class VBenchDimensionMetric(VBenchMetricBase):
        """Auto-generated VBench metric for a specific dimension."""
        
        name = f"vbench_{dimension}"
        dim_config = VBENCH_DIMENSIONS.get(dimension, {})
        enabled_by_default = dim_config.get("enabled_by_default", True)
        higher_is_better = True
        _original_higher_is_better = dim_config.get("higher_is_better", True)
        
        @classmethod
        def normalize(cls, value: float) -> float:
            normalized = max(0.0, min(1.0, value))
            if not cls._original_higher_is_better:
                normalized = 1.0 - normalized
            return normalized
        
        def __init__(self):
            super().__init__(dimension=dimension)
    
    VBenchDimensionMetric.__name__ = class_name
    VBenchDimensionMetric.__qualname__ = class_name
    
    # Register after class is fully configured
    register(VBenchDimensionMetric)
    
    return VBenchDimensionMetric


# Create and register all 10 VBench metric classes
_vbench_metric_classes = {}
for dim in VBENCH_DIMENSIONS.keys():
    _vbench_metric_classes[dim] = _create_vbench_metric_class(dim)


# Export the base class and all dimension-specific classes
__all__ = ["VBenchMetricBase"] + [cls.__name__ for cls in _vbench_metric_classes.values()]

