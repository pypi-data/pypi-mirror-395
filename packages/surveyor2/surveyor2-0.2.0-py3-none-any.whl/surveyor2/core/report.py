from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Callable, Tuple
import time, json, hashlib, pathlib, os, sys

from .types import InputItem


@dataclass
class MetricEntry:
    """Result of a single metric evaluation."""

    name: str
    score: Optional[float] = None
    status: str = "ok"  # "ok" | "error"
    settings: Dict[str, Any] = field(default_factory=dict)
    params: Dict[str, Any] = field(default_factory=dict)
    extras: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    timing_ms: Optional[float] = None


@dataclass
class MetricResults:
    """Results for a single metric: generated result and baseline results."""
    
    generated: MetricEntry
    baseline: List[MetricEntry] = field(default_factory=list)
    
    def get_baseline_average(self) -> Optional[float]:
        """Get the average baseline score."""
        scores = [m.score for m in self.baseline if m.status == "ok" and m.score is not None]
        return sum(scores) / len(scores) if scores else None
    
    def get_pct_diff(self) -> Optional[float]:
        """Calculate percentage difference between generated and baseline average."""
        if self.generated.status != "ok" or self.generated.score is None:
            return None
        avg = self.get_baseline_average()
        if avg is None or avg == 0:
            return None
        return ((self.generated.score - avg) / avg) * 100.0
    
    def get_quality_label(self) -> Optional[str]:
        """Get quality label for single-reference metrics."""
        from .registry import get_metric_cls
        
        if self.generated.status != "ok" or self.generated.score is None:
            return None
        
        if len(self.baseline) != 1:
            return None
        
        try:
            metric_cls = get_metric_cls(self.generated.name)
            ranges = metric_cls.get_quality_ranges()
            if not ranges:
                return None
            
            score = self.generated.score
            for min_val, max_val, label in ranges:
                if min_val <= score < max_val:
                    return label
                if score == 1.0 and max_val == 1.0:
                    return label
            return None
        except (KeyError, Exception):
            return None
    
    def get_score(self, use_baseline: bool = False) -> Optional[float]:
        """Get score (generated or baseline average). Scores are already normalized."""
        if use_baseline:
            return self.get_baseline_average()
        else:
            if self.generated.status != "ok" or self.generated.score is None:
                return None
            return self.generated.score


@dataclass
class Report:
    """Container for all results of one evaluation run."""

    run: Dict[str, Any] = field(default_factory=dict)
    inputs: Optional[InputItem] = None
    results: List[MetricResults] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    # --- helpers ---
    @staticmethod
    def now_utc() -> str:
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    @staticmethod
    def config_hash(cfg: dict) -> str:
        blob = json.dumps(cfg, sort_keys=True, ensure_ascii=False).encode()
        return hashlib.sha256(blob).hexdigest()[:8]

    def add_generated_result(self, entry: MetricEntry) -> None:
        """Add a generated metric result."""
        self.results.append(MetricResults(generated=entry))

    def add_baseline_result(self, entry: MetricEntry) -> None:
        """Add a baseline result for a metric (matched by name)."""
        for result in self.results:
            if result.generated.name == entry.name:
                result.baseline.append(entry)
                return
    
    def get_baseline_average(self, metric_name: str) -> Optional[float]:
        """Get the average baseline score for a specific metric."""
        for result in self.results:
            if result.generated.name == metric_name:
                return result.get_baseline_average()
        return None
    
    @property
    def metrics(self) -> List[MetricEntry]:
        return [r.generated for r in self.results]

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)

    def add_error(self, msg: str) -> None:
        self.errors.append(msg)

    def _compute_weighted_total(self, weights: Dict[str, float], use_baseline: bool = False) -> Tuple[float, float]:
        """Compute weighted total and total weight for composite score."""
        total = 0.0
        total_w = 0.0
        
        for result in self.results:
            score = result.get_score(use_baseline)
            if score is None:
                continue
            
            w = float(weights.get(result.generated.name, 1.0))
            total += w * score
            total_w += w
        
        return total, total_w

    def get_composite(self, weights: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """Compute weighted average score across all ok metrics."""
        weights = weights or {}
        total, total_w = self._compute_weighted_total(weights, use_baseline=False)
        return {
            "score": (total / total_w) if total_w > 0 else None,
            "weights": weights,
            "enabled": bool(self.results),
        }

    def get_metric_pct_diff(self, metric_name: str) -> Optional[float]:
        """Calculate percentage difference for a specific metric."""
        for result in self.results:
            if result.generated.name == metric_name:
                return result.get_pct_diff()
        return None

    def get_composite_pct_diff(self, weights: Optional[Dict[str, float]] = None) -> Optional[float]:
        """Calculate percentage difference for composite score from reference composite."""
        weights = weights or {}
        gen_total, total_w = self._compute_weighted_total(weights, use_baseline=False)
        ref_total, _ = self._compute_weighted_total(weights, use_baseline=True)
        
        if total_w > 0 and ref_total != 0:
            gen_composite = gen_total / total_w
            ref_composite = ref_total / total_w
            return ((gen_composite - ref_composite) / ref_composite) * 100.0
        
        return None

    def print(
        self,
        index: int,
        parse_errors: List[str],
        colorize: Callable[[str, str], str],
        format_pct_diff: Callable[[Optional[float], bool], str],
        colors: Any,
        get_higher_is_better: Callable[[str], bool],
        weights: Optional[Dict[str, float]] = None,
    ) -> bool:
        """Print a single report. Returns True if there were errors."""
        print(f"== Surveyor2 report [{index}] ==")
        print(f"started_at: {self.run.get('started_at')}")
        print(f"device:     {self.run.get('device')}")

        print(f"video:      {self.inputs.video}")

        if parse_errors:
            print("parse_errors:")
            for e in parse_errors:
                print(f"  - {e}")

        print("metrics:")
        for result in self.results:
            m = result.generated
            status = getattr(m, "status", "ok")
            score = getattr(m, "score", None)
            err = getattr(m, "error", None)

            if status != "ok" or err:
                error_msg = err if err else "error"
                print(f"  - {m.name}: {error_msg}")
            elif score is not None and not (isinstance(score, float) and (score != score)):
                score_str = f"{score:.4f}"
                
                quality_label = result.get_quality_label()
                if quality_label:
                    quality_colors = {
                        "poor": colors.RED,
                        "fair": colors.YELLOW,
                        "good": colors.GREEN,
                        "excellent": colors.CYAN,
                    }
                    quality_color = quality_colors.get(quality_label, colors.GREY)
                    quality_str = colorize(quality_label, quality_color)
                    print(f"  - {m.name}: {score_str} ({quality_str})")
                else:
                    pct_diff = result.get_pct_diff()
                    pct_diff_str = format_pct_diff(pct_diff, get_higher_is_better(m.name))
                    if pct_diff_str:
                        print(f"  - {m.name}: {score_str} ({pct_diff_str})")
                    else:
                        print(f"  - {m.name}: {score_str}")
            else:
                print(f"  - {m.name}: nan")

        composite = self.get_composite(weights)
        if composite.get("enabled"):
            composite_score = composite.get("score")
            composite_pct_diff = self.get_composite_pct_diff(weights)
            
            if composite_score is not None:
                score_str = f"{composite_score:.4f}"
                pct_diff_str = format_pct_diff(composite_pct_diff, True)
                if pct_diff_str:
                    print(f"  composite: {colorize(score_str, colors.CYAN)} ({pct_diff_str})")
                else:
                    print(f"  composite: {colorize(score_str, colors.CYAN)}")
            else:
                print(f"  composite: {composite_score}")

        print()
        return bool(self.errors)

    def to_json(self, indent: int = 2, weights: Optional[Dict[str, float]] = None) -> str:
        d = asdict(self)
        d["composite"] = self.get_composite(weights)
        return json.dumps(d, indent=indent, ensure_ascii=False)

    @classmethod
    def from_json(cls, s: str) -> Report:
        d = json.loads(s)
        results_raw = d.get("results", [])
        results = [
            MetricResults(
                generated=MetricEntry(**r.get("generated", {})),
                baseline=[MetricEntry(**b) for b in r.get("baseline", [])]
            )
            for r in results_raw
        ]
        
        return cls(
            run=d.get("run", {}),
            inputs=d.get("inputs"),
            results=results,
            warnings=d.get("warnings", []),
            errors=d.get("errors", [])
        )


@dataclass
class BatchReport:
    """
    Aggregated result of evaluating multiple inputs.
    - reports: list of per-item Report objects
    - summary: per-metric statistics across reports: { metric: {min, max, avg} }
    """

    run: Dict[str, Any] = field(default_factory=dict)
    reports: List[Report] = field(default_factory=list)

    def get_summary(self) -> Dict[str, Dict[str, float]]:
        scores_by_metric: Dict[str, List[float]] = {}
        for rpt in self.reports:
            for result in rpt.results:
                m = result.generated
                if m.status == "ok" and m.score is not None:
                    scores_by_metric.setdefault(m.name, []).append(float(m.score))

        out: Dict[str, Dict[str, float]] = {}
        for name, vals in scores_by_metric.items():
            if not vals:
                continue
            vmin = min(vals)
            vmax = max(vals)
            avg = sum(vals) / float(len(vals))
            out[name] = {"min": vmin, "max": vmax, "avg": avg}
        return out

    def get_composite_summary(self, weights: Optional[Dict[str, float]] = None) -> Dict[str, float]:
        composite_scores: List[float] = []
        for rpt in self.reports:
            try:
                composite = rpt.get_composite(weights)
                if composite.get("enabled"):
                    s = composite.get("score")
                    if s is not None:
                        composite_scores.append(float(s))
            except Exception:
                pass
        if composite_scores:
            return {
                "min": min(composite_scores),
                "max": max(composite_scores),
                "avg": sum(composite_scores) / float(len(composite_scores)),
            }
        return {}

    def get_composite_pct_diff_summary(self, weights: Optional[Dict[str, float]] = None) -> Optional[float]:
        """Calculate average percentage difference for composite scores across all reports."""
        pct_diffs: List[float] = []
        for rpt in self.reports:
            try:
                pct_diff = rpt.get_composite_pct_diff(weights)
                if pct_diff is not None:
                    pct_diffs.append(float(pct_diff))
            except Exception:
                pass
        if pct_diffs:
            return sum(pct_diffs) / float(len(pct_diffs))
        return None

    def get_errors(self) -> List[Dict[str, Any]]:
        all_errors: List[Dict[str, Any]] = []
        for rpt in self.reports:
            input_id = rpt.inputs.id or "unknown"

            for result in rpt.results:
                m = result.generated
                if m.status == "error" or m.error is not None:
                    all_errors.append(
                        {"id": input_id, "metric_name": m.name, "error": m.error}
                    )
                for baseline_m in result.baseline:
                    if baseline_m.status == "error" or baseline_m.error is not None:
                        all_errors.append(
                            {"id": input_id, "metric_name": baseline_m.name, "error": baseline_m.error}
                        )

            for err in rpt.errors:
                all_errors.append({"id": input_id, "metric_name": None, "error": err})

        return all_errors

    def print(
        self,
        parse_errors: List[str],
        colorize: Callable[[str, str], str],
        format_pct_diff: Callable[[Optional[float], bool], str],
        colors: Any,
        get_higher_is_better: Callable[[str], bool],
        weights: Optional[Dict[str, float]] = None,
    ) -> bool:
        """Print all reports and summary. Returns True if there were any errors."""
        any_errors = False
        for i, report in enumerate(self.reports):
            has_errors = report.print(
                i,
                parse_errors,
                colorize,
                format_pct_diff,
                colors,
                get_higher_is_better,
                weights,
            )
            any_errors = any_errors or has_errors

        self.print_summary(colorize, format_pct_diff, colors, get_higher_is_better, weights)
        return any_errors

    def print_summary(
        self,
        colorize: Callable[[str, str], str],
        format_pct_diff: Callable[[Optional[float], bool], str],
        colors: Any,
        get_higher_is_better: Callable[[str], bool],
        weights: Optional[Dict[str, float]] = None,
    ) -> None:
        """Print batch-level summary statistics."""
        print("== Batch summary (min/max/avg) ==")
        
        pct_diff_summary: Dict[str, List[float]] = {}
        quality_label_summary: Dict[str, List[str]] = {}
        
        for rpt in self.reports:
            for result in rpt.results:
                if result.generated.status == "ok" and result.generated.score is not None:
                    pct_diff = result.get_pct_diff()
                    if pct_diff is not None:
                        pct_diff_summary.setdefault(result.generated.name, []).append(pct_diff)
                    
                    quality_label = result.get_quality_label()
                    if quality_label:
                        quality_label_summary.setdefault(result.generated.name, []).append(quality_label)
        
        summary = self.get_summary()
        for name in sorted(summary.keys()):
            s = summary[name]
            min_val = f"{s['min']:.4f}"
            max_val = f"{s['max']:.4f}"
            avg_val = f"{s['avg']:.4f}"
            
            if name in quality_label_summary and quality_label_summary[name]:
                quality_labels = quality_label_summary[name]
                most_common = max(set(quality_labels), key=quality_labels.count)
                quality_colors = {
                    "poor": colors.RED,
                    "fair": colors.YELLOW,
                    "good": colors.GREEN,
                    "excellent": colors.CYAN,
                }
                quality_color = quality_colors.get(most_common, colors.GREY)
                quality_str = colorize(most_common, quality_color)
                print(f"- {name}: min={min_val}, max={max_val}, avg={avg_val} ({quality_str})")
            else:
                avg_pct_diff = None
                if name in pct_diff_summary and pct_diff_summary[name]:
                    avg_pct_diff = sum(pct_diff_summary[name]) / float(len(pct_diff_summary[name]))
                
                pct_diff_str = format_pct_diff(avg_pct_diff, get_higher_is_better(name))
                if pct_diff_str:
                    print(f"- {name}: min={min_val}, max={max_val}, avg={avg_val} ({pct_diff_str})")
                else:
                    print(f"- {name}: min={min_val}, max={max_val}, avg={avg_val}")
        
        composite_summary = self.get_composite_summary(weights)
        if composite_summary:
            min_val = colorize(f"{composite_summary['min']:.4f}", colors.CYAN)
            max_val = colorize(f"{composite_summary['max']:.4f}", colors.CYAN)
            avg_val = colorize(f"{composite_summary['avg']:.4f}", colors.CYAN)
            composite_pct_diff = self.get_composite_pct_diff_summary(weights)
            pct_diff_str = format_pct_diff(composite_pct_diff, True)
            if pct_diff_str:
                print(f"composite: min={min_val}, max={max_val}, avg={avg_val} ({pct_diff_str})")
            else:
                print(f"composite: min={min_val}, max={max_val}, avg={avg_val}")

    def to_json(self, indent: int = 2, weights: Optional[Dict[str, float]] = None) -> str:
        d = asdict(self)
        d["summary"] = self.get_summary()
        d["composite_summary"] = self.get_composite_summary(weights)
        d["errors"] = self.get_errors()
        return json.dumps(d, indent=indent, ensure_ascii=False)

    @classmethod
    def from_json(cls, s: str) -> "BatchReport":
        d = json.loads(s)
        reports: List[Report] = []
        for r in d.get("reports", []):
            reports.append(Report.from_json(json.dumps(r)))
        d["reports"] = reports
        d.pop("summary", None)
        d.pop("composite_summary", None)
        d.pop("errors", None)
        return cls(**d)
