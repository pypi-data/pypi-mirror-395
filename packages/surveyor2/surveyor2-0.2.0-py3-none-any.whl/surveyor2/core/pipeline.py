from __future__ import annotations
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import time

from .metrics_base import Metric
from .parser import parse_metrics_block
from .report import MetricEntry
from .utils import with_progress, colorize, Colors
from .types import MetricConfig, InputItem, Video


@dataclass
class MetricInstance:
    inst: Metric
    settings: Dict[str, Any]
    params: Dict[str, Any]
    init_ms: int


class MetricsPipeline:
    """
    Pipeline for running metrics in batch mode:
    - Non-reference metrics run on all videos at once
    - Reference metrics run on all pairs at once
    """

    def __init__(
        self, *, metrics_block: List[MetricConfig] = [], silent: bool = False
    ):
        self._silent = silent
        self._instances: List[MetricInstance] = []
        self._parse_errors: List[str] = []
        self._initialize_metrics(metrics_block)

    def _initialize_metrics(self, metrics_block: List[MetricConfig]) -> None:
        """Parse and initialize all metrics once."""
        parsed, parse_errors = parse_metrics_block(metrics_block)
        self._parse_errors = list(parse_errors)
        
        for m in parsed:
            t0 = time.time()
            try:
                inst = m.cls()  # type: ignore[call-arg]
                inst.init(m.settings)
                init_ms = int((time.time() - t0) * 1000)
                self._instances.append(
                    MetricInstance(inst=inst, settings=m.settings, params=m.params, init_ms=init_ms)
                )
            except Exception as e:
                metric_name = getattr(m.cls, 'name', 'metric')
                error_details = str(e)
                
                if not self._silent:
                    warning_msg = f"⚠ Metric '{metric_name}' failed to initialize and will not run"
                    print(colorize(warning_msg, Colors.YELLOW))
                    
                    if error_details:
                        print(colorize(f"  Reason: {error_details}", Colors.YELLOW))
                    
                    exc_type = type(e).__name__
                    if exc_type in ('ModuleNotFoundError', 'ImportError'):
                        print(colorize(f"  Missing dependency - check your environment", Colors.YELLOW))
                
                self._parse_errors.append(f"{metric_name}: {error_details}")

    def teardown(self) -> None:
        """Teardown all metrics."""
        for instance in self._instances:
            try:
                instance.inst.teardown()
            except Exception:
                pass
    
    def _run_metrics_batch(
        self,
        metric_instances: List[MetricInstance],
        videos: List[Video],
        references: List[Optional[Video]],
        desc: str,
    ) -> List[Dict[str, MetricEntry]]:
        """
        Helper to run a list of metrics on a batch of videos.
        
        Returns list of dicts mapping metric_name -> MetricEntry for each video/pair.
        """
        results_per_item: List[Dict[str, MetricEntry]] = [{} for _ in videos]
        
        metric_iterator = with_progress(
            metric_instances,
            desc=desc,
            unit="metric",
            position=0,
            silent=self._silent
        )
        
        for metric_instance in metric_iterator:
            metric_name = metric_instance.inst.name
            if hasattr(metric_iterator, "set_description"):
                metric_iterator.set_description(f"Metric: {metric_name}")
            
            # Prepare batch data - merge metric params with video metadata
            params_list = []
            for video, reference in zip(videos, references):
                params = dict(metric_instance.params)
                # Add video metadata to params
                params["video"] = video.video_path
                if video.prompt:
                    params["prompt"] = video.prompt
                # Add reference path if present
                if reference is not None:
                    params["reference"] = reference.video_path
                params_list.append(params)
            
            # Run metric
            t0 = time.time()
            try:
                batch_results = metric_instance.inst.evaluate_batch(videos, references, params_list)
                eval_ms = int((time.time() - t0) * 1000)
                
                # Store results as MetricEntry objects
                for idx, result in enumerate(batch_results):
                    try:
                        name, score, extras = result
                        
                        # Check if this is an error result (has error in extras)
                        error_msg = extras.get("error") if isinstance(extras, dict) else None
                        is_error = error_msg is not None
                        
                        results_per_item[idx][metric_name] = MetricEntry(
                            name=name,
                            score=float(score) if score is not None else None,
                            extras=extras,
                            status="error" if is_error else "ok",
                            error=error_msg,
                            timing_ms=metric_instance.init_ms // len(videos) + eval_ms // len(videos),
                            settings=metric_instance.settings,
                            params=metric_instance.params,
                        )
                    except Exception as ex:
                        results_per_item[idx][metric_name] = MetricEntry(
                            name=metric_name,
                            score=None,
                            extras={},
                            status="error",
                            error=f"result parsing failed: {ex}",
                            settings=metric_instance.settings,
                            params=metric_instance.params,
                        )
            except Exception as ex:
                # If batch evaluation fails, add error to all results
                for idx in range(len(videos)):
                    results_per_item[idx][metric_name] = MetricEntry(
                        name=metric_name,
                        score=None,
                        extras={},
                        status="error",
                        error=f"batch evaluate failed: {ex}",
                        settings=metric_instance.settings,
                        params=metric_instance.params,
                    )
        
        return results_per_item

    def run_non_reference_metrics(
        self,
        videos: List[Video],
    ) -> Tuple[List[Dict[str, MetricEntry]], List[str]]:
        """Run all non-reference metrics on a list of videos."""
        non_ref_instances = [
            inst for inst in self._instances
            if not inst.inst.requires_reference
        ]
        
        if not non_ref_instances:
            return [{} for _ in videos], list(self._parse_errors)
        
        references = [None] * len(videos)
        results = self._run_metrics_batch(
            non_ref_instances, videos, references, "Non-ref metrics"
        )
        return results, list(self._parse_errors)
    
    def run_reference_metrics(
        self,
        video_pairs: List[Tuple[Video, Video]],
    ) -> Tuple[List[Dict[str, MetricEntry]], List[str]]:
        """Run all reference metrics on a list of video pairs."""
        ref_instances = [
            inst for inst in self._instances
            if inst.inst.requires_reference
        ]
        
        if not ref_instances:
            return [{} for _ in video_pairs], list(self._parse_errors)
        
        videos = [v for v, _ in video_pairs]
        references = [r for _, r in video_pairs]
        
        results = self._run_metrics_batch(
            ref_instances, videos, references, "Reference metrics"
        )
        return results, list(self._parse_errors)
