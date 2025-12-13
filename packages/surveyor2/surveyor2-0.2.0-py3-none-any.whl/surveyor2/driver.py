from __future__ import annotations
import json, pathlib, sys, os
from typing import Any, Dict, Tuple, List, Optional

from .core.pipeline import MetricsPipeline
from .core.report import Report, BatchReport, MetricEntry
from .core.parser import build_default_metrics_config_from_registry
from .core.registry import print_registered_metrics, get_higher_is_better
from .core.utils import with_progress, Colors, colorize, format_percentage_diff
from .core.types import InputItem, InputsConfig, ProfileArgs, ProfileConfig, Frame, MetricConfig, Video
from .metrics import *


def load_raw_config(p: str) -> Dict[str, Any]:
    """Load config file as raw dictionary."""
    path = pathlib.Path(p)
    text = path.read_text()
    if path.suffix.lower() in {".yaml", ".yml"}:
        try:
            import yaml
        except Exception:
            raise RuntimeError(
                "YAML config requested but PyYAML is not installed. pip install pyyaml"
            )
        return yaml.safe_load(text)
    elif path.suffix.lower() == ".json":
        return json.loads(text)
    else:
        raise ValueError(
            f"Unsupported config extension: {path.suffix} (use .yaml/.yml or .json)"
        )


def load_inputs_config(p: str) -> InputsConfig:
    """Load and parse inputs config file."""
    raw_data = load_raw_config(p)
    return InputsConfig.from_dict(raw_data)


def load_metrics_config(p: str) -> ProfileConfig:
    """Load and parse metrics config file."""
    raw_data = load_raw_config(p)
    return ProfileConfig.from_dict(raw_data)


def _prepare_all_videos_and_pairs(
    inputs_list: List[InputItem]
) -> Tuple[List[Video], List[Tuple[Video, Video]], Dict]:
    """
    Prepare all videos and pairs for metric evaluation.
    
    For each prompt/input:
    - 1 generated video
    - N reference videos (can be 0)
    
    Returns:
        all_videos: List of Video objects
        all_pairs: List of (Video, Video) tuples for reference metrics
        metadata: Dictionary with mappings for organizing results later
    """
    all_videos: List[Video] = []
    all_pairs: List[Tuple[Video, Video]] = []
    metadata = {
        "input_to_videos": {},  # input_idx -> list of video indices in all_videos
        "input_to_pairs": {},   # input_idx -> list of pair indices in all_pairs
        "num_inputs": len(inputs_list),
    }
    
    for input_idx, item in enumerate(inputs_list):
        if not item.video:
            raise ValueError(f"inputs[{input_idx}].video is required")
        
        metadata["input_to_videos"][input_idx] = []
        metadata["input_to_pairs"][input_idx] = []
        
        # Load generated video
        gen_video = Video.from_path(item.video, max_frames=item.max_frames, prompt=item.prompt)
        
        # Add generated video to all_videos
        video_idx = len(all_videos)
        all_videos.append(gen_video)
        metadata["input_to_videos"][input_idx].append(video_idx)
        
        # Load reference videos
        ref_videos: List[Video] = []
        if item.reference:
            ref_list = item.reference if isinstance(item.reference, list) else [item.reference]
            for ref_uri in ref_list:
                try:
                    ref_video = Video.from_path(ref_uri, max_frames=item.max_frames, prompt=item.prompt)
                    
                    # Add reference video to all_videos
                    video_idx = len(all_videos)
                    all_videos.append(ref_video)
                    metadata["input_to_videos"][input_idx].append(video_idx)
                    
                    ref_videos.append(ref_video)
                except Exception:
                    continue
        
        # Create pairs for reference-based metrics
        # 1. Generated vs each reference
        for ref_video in ref_videos:
            pair_idx = len(all_pairs)
            all_pairs.append((gen_video, ref_video))
            metadata["input_to_pairs"][input_idx].append(pair_idx)
        
        # 2. References vs each other (for baseline statistics)
        if len(ref_videos) >= 2:
            for i in range(len(ref_videos)):
                for j in range(i + 1, len(ref_videos)):
                    pair_idx = len(all_pairs)
                    all_pairs.append((ref_videos[i], ref_videos[j]))
                    metadata["input_to_pairs"][input_idx].append(pair_idx)
    
    return all_videos, all_pairs, metadata


def run_profile(
    inputs_list: List[InputItem], 
    profile_config: ProfileConfig, 
    silent: bool = False
) -> Tuple[BatchReport, List[str]]:
    """
    Drives the pipeline using a prompt-based architecture.
    
    For each prompt/input:
    - 1 generated video
    - 0 or more reference videos
    
    Metrics are run in two phases:
    1. Non-reference metrics on ALL videos (generated + references)
    2. Reference metrics on ALL pairs (gen vs refs, refs vs refs)

    Args:
        inputs_list: List of InputItem objects (one per prompt)
        profile_config: ProfileConfig object with metrics and aggregation settings
        silent: If True, disable all printing and progress bars

    Returns:
        Tuple of (BatchReport, parse_errors)
    """
    if not isinstance(inputs_list, list) or not inputs_list:
        raise ValueError("inputs_list must be a non-empty list of input items")

    weights = profile_config.aggregate.weights

    pipe = MetricsPipeline(metrics_block=profile_config.metrics, silent=silent)
    if not silent:
        print(f"Metrics pipeline initialized with {len(profile_config.metrics)} metrics")
        print(f"Processing {len(inputs_list)} prompts")

    # Phase 1: Load all videos and prepare all pairs
    if not silent:
        print("Loading videos and preparing pairs...")
    
    all_videos, all_pairs, metadata = _prepare_all_videos_and_pairs(inputs_list)
    
    if not silent:
        print(f"  Total videos: {len(all_videos)} (generated + references)")
        print(f"  Total pairs: {len(all_pairs)} (for reference metrics)")

    # Phase 2: Run non-reference metrics on ALL videos
    if not silent:
        print("Running non-reference metrics on all videos...")
    
    video_results, parse_errors = pipe.run_non_reference_metrics(videos=all_videos)

    # Phase 3: Run reference metrics on ALL pairs
    if not silent:
        print("Running reference metrics on all pairs...")
    
    pair_results, parse_errors_ref = pipe.run_reference_metrics(video_pairs=all_pairs)
    
    all_parse_errors = list(set(parse_errors + parse_errors_ref))

    # Phase 4: Organize results into reports for each prompt/input
    if not silent:
        print("Organizing results into reports...")
    
    reports = []
    for input_idx in range(metadata["num_inputs"]):
        item = inputs_list[input_idx]
        
        # Create report for this input
        report = Report(
            run={
                "started_at": Report.now_utc(),
                "config_hash": Report.config_hash({}),
            },
            inputs=item,
        )
        
        # Get the generated video for this input (first video in the input's video list)
        input_video_indices = metadata["input_to_videos"][input_idx]
        gen_video_idx = input_video_indices[0]  # First is always generated
        ref_video_indices = input_video_indices[1:]  # Rest are references
        
        # Get the pairs for this input
        # First N pairs are gen vs each ref, then refs vs each other
        input_pair_indices = metadata["input_to_pairs"][input_idx]
        num_refs = len(ref_video_indices)
        gen_vs_ref_pairs = input_pair_indices[:num_refs] if num_refs > 0 else []
        ref_vs_ref_pairs = input_pair_indices[num_refs:] if len(input_pair_indices) > num_refs else []
        
        # Add generated results: non-reference metrics from generated video
        for metric_entry in video_results[gen_video_idx].values():
            report.add_generated_result(metric_entry)
        
        # Add generated results: reference metrics from gen vs ref pairs
        for pair_idx in gen_vs_ref_pairs:
            for metric_entry in pair_results[pair_idx].values():
                report.add_generated_result(metric_entry)
        
        # Add baseline results: non-reference metrics from reference videos
        for ref_video_idx in ref_video_indices:
            for metric_entry in video_results[ref_video_idx].values():
                report.add_baseline_result(metric_entry)
        
        # Add baseline results: reference metrics from gen vs ref pairs
        for pair_idx in gen_vs_ref_pairs:
            for metric_entry in pair_results[pair_idx].values():
                report.add_baseline_result(metric_entry)
        
        # Add baseline results: reference metrics from ref vs ref pairs
        for pair_idx in ref_vs_ref_pairs:
            for metric_entry in pair_results[pair_idx].values():
                report.add_baseline_result(metric_entry)
        
        # Attach input metadata
        report.inputs.video = item.video
        if item.reference:
            ref_list = item.reference if isinstance(item.reference, list) else [item.reference]
            report.inputs.reference = ref_list[0] if ref_list else None
            report.inputs.reference_videos = ref_list
        report.inputs.max_frames = item.max_frames
        report.inputs.index = input_idx
        if item.id is not None:
            report.inputs.id = item.id
        if item.prompt is not None:
            report.inputs.prompt = item.prompt
        
        reports.append(report)

    try:
        pipe.teardown()
    except Exception:
        pass

    batch = BatchReport(
        run={
            "started_at": Report.now_utc(),
            "count": len(reports),
        },
        reports=reports,
    )

    return batch, all_parse_errors


def run_main(args: ProfileArgs) -> int:
    """Main entry point for the run command."""
    if args.list:
        print_registered_metrics()
        return 0

    if not args.inputs:
        import sys

        print("Error: provide --inputs", file=sys.stderr)
        return 1

    inputs_cfg = load_inputs_config(args.inputs)
    if not inputs_cfg.inputs:
        raise SystemExit("inputs file must contain non-empty 'inputs: [...]'")

    inputs_list: List[InputItem] = inputs_cfg.inputs

    # Handle metrics config: preset takes precedence over metrics file
    if args.preset:
        if args.metrics:
            print(
                "Error: Cannot specify both --preset and --metrics. Use one or the other.",
                file=sys.stderr,
            )
            return 1
        from surveyor2.presets import get_preset

        try:
            metrics_config = get_preset(args.preset)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    elif args.metrics:
        metrics_config = load_metrics_config(args.metrics)
    else:
        metrics_config = build_default_metrics_config_from_registry()

    batch, parse_errors = run_profile(inputs_list, metrics_config, silent=args.silent)

    weights = metrics_config.aggregate.weights if metrics_config.aggregate else None
    any_errors = batch.print(
        parse_errors,
        colorize,
        format_percentage_diff,
        Colors,
        get_higher_is_better,
        weights,
    )

    if args.report_json:
        p = pathlib.Path(args.report_json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(batch.to_json(weights=weights))

    return 0 if not any_errors else 1
