"""Prepare command for generating Surveyor2 inputs YAML file."""

import json
import os
import pathlib
import sys
from typing import Dict, List, Optional, Tuple

import yaml

from ..core.types.cli import InputsArgs


def load_prompts_jsonl(jsonl_path: str) -> Dict[str, str]:
    """
    Load prompts from JSONL file.

    Expected format for each line:
    {"id": "unique_id", "prompt": "text prompt"}

    Returns dict mapping id to prompt.

    Raises:
        ValueError: If any line is missing 'id' or 'prompt' keys
    """
    prompts = {}

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON on line {line_num}: {e}")

            if "id" not in data:
                raise ValueError(f"Missing 'id' key on line {line_num}")

            if "prompt" not in data:
                raise ValueError(f"Missing 'prompt' key on line {line_num}")

            prompts[data["id"]] = data["prompt"]

    return prompts


def find_video_files(directory: str) -> List[str]:
    """Find all .mp4 video files in directory and return absolute paths."""
    video_extensions = {".mp4"}
    video_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if pathlib.Path(file).suffix.lower() in video_extensions:
                abs_path = os.path.abspath(os.path.join(root, file))
                video_files.append(abs_path)

    return sorted(video_files)


def match_videos_with_prompts(
    generated_videos: List[str],
    reference_videos_dirs: List[str],
    prompts: Dict[str, str],
) -> List[Tuple[str, List[str], str, str]]:
    """
    Match generated videos with reference videos and prompts by id.

    Videos must start with their id (e.g., 'id_rest_of_name.mp4').
    Videos without matching prompts are skipped.

    Returns list of (generated_video, reference_video_paths[], prompt, prompt_id) tuples.

    Raises:
        ValueError: If no videos match any prompts
    """
    matches = []
    used_prompts = set()
    skipped_videos = []
    ref_videos_by_id: Dict[str, List[str]] = {}

    # Sort IDs by length (longest first) to avoid prefix matching issues
    # e.g., Video_10 should match before Video_1
    sorted_ids = sorted(prompts.keys(), key=len, reverse=True)
    
    for ref_dir in reference_videos_dirs:
        ref_videos = find_video_files(ref_dir)
        for ref_video in ref_videos:
            ref_basename = pathlib.Path(ref_video).stem
            for id in sorted_ids:
                if ref_basename.startswith(id):
                    ref_videos_by_id.setdefault(id, []).append(ref_video)
                    break

    for gen_video in generated_videos:
        gen_basename = pathlib.Path(gen_video).stem

        # Find matching prompt by checking if basename starts with id
        # Check longer IDs first to avoid prefix matching issues
        prompt = None
        prompt_id = None
        for id in sorted_ids:
            if gen_basename.startswith(id):
                prompt = prompts[id]
                prompt_id = id
                used_prompts.add(id)
                break

        if prompt is None:
            # Skip videos without matching prompts
            skipped_videos.append(gen_video)
            continue

        ref_videos = ref_videos_by_id.get(prompt_id, [])

        if not ref_videos:
            print(f"Warning: No reference videos found for id '{prompt_id}'")

        matches.append((gen_video, ref_videos, prompt, prompt_id))

    # Report skipped videos
    if skipped_videos:
        print(f"Info: Skipped {len(skipped_videos)} videos without matching prompts")

    # Check if all prompts were used
    unused_prompts = set(prompts.keys()) - used_prompts
    if unused_prompts:
        raise ValueError(
            f"{len(unused_prompts)} prompts not matched to any videos: {unused_prompts}. "
            f"Make sure generated videos start with these ids."
        )

    if not matches:
        raise ValueError("No videos matched any prompts")

    return matches


def generate_inputs_yaml(
    matches: List[Tuple[str, List[str], str, str]],
    generated_videos_dir: str,
    output_path: str,
) -> None:
    """Generate inputs YAML file from video matches."""

    inputs = []

    for gen_video, ref_videos, prompt, prompt_id in matches:
        entry = {"id": prompt_id, "video": gen_video, "prompt": prompt}

        if ref_videos:
            if len(ref_videos) == 1:
                entry["reference"] = ref_videos[0]
            else:
                entry["reference"] = ref_videos

        inputs.append(entry)

    # Create YAML structure
    yaml_data = {"inputs": inputs}

    # Write YAML file
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(
            yaml_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False
        )

    print(f"Generated inputs file: {output_path}")
    print(f"Processed {len(inputs)} videos")

    # Print summary
    with_ref = sum(1 for entry in inputs if "reference" in entry)
    print(f"  - {len(inputs)} videos with prompts")
    print(f"  - {with_ref} videos with reference videos")


def prepare_surveyor2_inputs(
    reference_videos_dirs: List[str],
    generated_videos_dir: str,
    prompts_file: str,
    output_path: Optional[str] = None,
    verbose: bool = False,
) -> str:
    """
    Generate Surveyor2 configuration files from video folders and prompts.

    This function creates:
    1. An inputs YAML file matching generated videos with reference videos and prompts

    Args:
        reference_videos_dirs: List of directories containing reference videos
        generated_videos_dir: Directory containing generated videos to evaluate
        prompts_file: JSONL file containing prompts (one JSON object per line)
        output_path: Path to output inputs.yaml file (default: inputs.yaml in current directory)
        verbose: Whether to print progress messages (default: True)

    Returns:
        Path to the generated inputs file

    Raises:
        FileNotFoundError: If any required input directory or file doesn't exist
        ValueError: If no generated videos are found
        RuntimeError: If config generation fails

    Example:
        >>> inputs_path = prepare_surveyor2_inputs(
        ...     reference_videos_dirs=["./reference_videos", "./reference_primes"],
        ...     generated_videos_dir="./generated_videos",
        ...     prompts_file="./prompts.jsonl",
        ...     output_path="./config/inputs.yaml"
        ... )
    """

    def log(message: str) -> None:
        if verbose:
            print(message)

    # Validate input paths
    for ref_dir in reference_videos_dirs:
        if not os.path.isdir(ref_dir):
            raise FileNotFoundError(f"Reference videos directory not found: {ref_dir}")

    if not os.path.isdir(generated_videos_dir):
        raise FileNotFoundError(
            f"Generated videos directory not found: {generated_videos_dir}"
        )

    if not os.path.isfile(prompts_file):
        raise FileNotFoundError(f"Prompts file not found: {prompts_file}")

    if output_path is None:
        output_path = "inputs.yaml"

    output_dir = os.path.dirname(output_path) or "."
    os.makedirs(output_dir, exist_ok=True)

    log(f"Loading prompts from {prompts_file}...")
    prompts = load_prompts_jsonl(prompts_file)
    log(f"Loaded {len(prompts)} prompts")

    log(f"Scanning for videos...")
    generated_videos = find_video_files(generated_videos_dir)
    log(f"Found {len(generated_videos)} generated videos")

    if not generated_videos:
        raise ValueError("No generated videos found")

    # Match videos with prompts
    log("Matching videos with references and prompts...")
    matches = match_videos_with_prompts(
        generated_videos, reference_videos_dirs, prompts
    )

    log(f"Generating inputs file...")
    generate_inputs_yaml(matches, generated_videos_dir, output_path)

    log(f"\nSuccess! Generated files:")
    log(f"  Inputs: {output_path}")
    log(f"\nTo run evaluation:")
    log(
        f"  surveyor2 profile --inputs {output_path} --report-json {os.path.splitext(output_path)[0]}_report.json"
    )

    return output_path


def inputs_main(args: InputsArgs) -> int:
    """Main entry point for the inputs command."""
    try:
        prepare_surveyor2_inputs(
            reference_videos_dirs=args.reference_videos,
            generated_videos_dir=args.generated_videos,
            prompts_file=args.prompts,
            output_path=args.output,
            verbose=True,
        )
        return 0
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
