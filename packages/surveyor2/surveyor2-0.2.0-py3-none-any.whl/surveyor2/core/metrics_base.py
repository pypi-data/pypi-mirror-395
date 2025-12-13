# vqeval/core/metrics_base.py
from __future__ import annotations
from typing import Dict, Any, Set, Mapping, Optional, List, Tuple
from .types import Video, MetricResult
from .utils import with_progress


class Metric:
    """
    Base class for all metrics:
      - Declarative settings/params
      - init() once, evaluate() many, teardown() at end
      - All metrics normalize their scores during evaluation
      - All metrics have higher_is_better = True after normalization
    
    Subclasses must define:
      - name: str
      - requires_reference: bool
      - get_settings(), get_setting_defaults(), get_params(), normalize()
      - init(), evaluate(), teardown()
    
    Optionally can define:
      - evaluate_batch(): for efficient batch processing
      - supports_batch: bool to indicate batch support
    """

    name: str
    requires_reference: bool = False
    higher_is_better: bool = True
    enabled_by_default: bool = True
    supports_batch: bool = False

    @classmethod
    def get_settings(cls) -> Dict[str, bool]:
        """Return settings dict mapping setting names to whether they're required."""
        return {}

    @classmethod
    def get_setting_defaults(cls) -> Dict[str, Any]:
        """Return default values for settings."""
        return {}

    @classmethod
    def get_params(cls) -> Set[str]:
        """Return set of parameter names this metric accepts."""
        return set()

    @classmethod
    def normalize(cls, value: float) -> float:
        """Normalize a metric value to [0, 1] range where higher is always better. Default: return value as-is."""
        return value

    @classmethod
    def get_quality_ranges(cls) -> Optional[List[Tuple[float, float, str]]]:
        """Return quality ranges for interpreting single-reference results.
        
        Returns list of (min, max, label) tuples, or None if not applicable.
        Example: [(0.0, 0.3, 'poor'), (0.3, 0.6, 'fair'), (0.6, 1.0, 'good')]
        """
        return None

    def init(self, settings: Mapping[str, Any]) -> None:
        """Initialize the metric with given settings."""
        pass

    def evaluate(
        self, video: Video, reference: Optional[Video], params: Mapping[str, Any]
    ) -> MetricResult:
        """
        Evaluate a video and return (name, normalized_score, extras). Must be implemented by subclass.
        The score returned should already be normalized via the normalize() classmethod.
        
        Args:
            video: Video object containing frames, path, and prompt
            reference: Optional reference Video object
            params: Parameters for this evaluation (can include prompt, video path, etc.)
        """
        raise NotImplementedError

    def evaluate_batch(
        self, 
        videos: List[Video], 
        references: List[Optional[Video]], 
        params_list: List[Mapping[str, Any]]
    ) -> List[MetricResult]:
        """
        Evaluate multiple video pairs in batch. 
        
        Default implementation calls evaluate() sequentially.
        Subclasses can override this for efficient batch processing (e.g., batched GPU inference).
        
        Args:
            videos: List of Video objects
            references: List of optional reference Video objects
            params_list: List of parameter dicts for each video pair
            
        Returns:
            List of MetricResult tuples (name, score, extras) for each video pair
        """
        results = []
        video_iterator = with_progress(
            zip(videos, references, params_list),
            desc=f"Evaluating {self.name}",
            unit="video",
            total=len(videos),
            position=1,
        )
        for video, reference, params in video_iterator:
            try:
                result = self.evaluate(video, reference, params)
                results.append(result)
            except Exception as e:
                results.append(self._error_result(f"evaluate failed: {e}"))
        return results

    def teardown(self) -> None:
        """Clean up metric resources."""
        pass

    def _error_result(self, error_message: str) -> MetricResult:
        """
        Helper method to return a standardized error result.
        
        Args:
            error_message: Error message to include in the result
            
        Returns:
            MetricResult tuple with NaN score and error in extras
        """
        return (self.name, float("nan"), {"error": error_message})
