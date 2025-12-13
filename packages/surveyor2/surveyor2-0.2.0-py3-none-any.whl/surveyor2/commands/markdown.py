"""Markdown command for generating markdown summary tables from JSON reports."""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from ..core.types.cli import MarkdownArgs


def format_score(value: float) -> str:
    """Format a score value with 4 decimal places."""
    return f"{value:.4f}"


def generate_markdown_table(data: Dict[str, Any]) -> str:
    """Generate a markdown summary table from report data."""
    lines: List[str] = []

    errors = data.get("errors", [])
    if errors:
        lines.append(f"⚠️ **Surveyor2 run complete. {len(errors)} errors occured.**")
        lines.append("")

    baseline_summary = {}
    pct_diff_summary = {}

    reports = data.get("reports", [])
    for report in reports:
        metrics = report.get("metrics", [])
        for metric in metrics:
            if metric.get("status") != "ok" or metric.get("score") is None:
                continue
            name = metric.get("name")
            extras = metric.get("extras", {})

            if isinstance(extras, dict):
                baseline = extras.get("baseline", {})
                pct_diff = extras.get("pct_diff")

                if isinstance(baseline, dict) and baseline.get("avg") is not None:
                    if name not in baseline_summary:
                        baseline_summary[name] = []
                    baseline_summary[name].append(float(baseline["avg"]))

                if pct_diff is not None:
                    if name not in pct_diff_summary:
                        pct_diff_summary[name] = []
                    pct_diff_summary[name].append(float(pct_diff))

    # Summary table
    summary = data.get("summary", {})
    if summary:
        lines.append("## Surveyor2 Metrics Summary")
        lines.append("")

        has_baseline = bool(baseline_summary)

        if has_baseline:
            lines.append("| Metric | Min | Max | Avg | Baseline (ref avg) | %Δ |")
            lines.append("|--------|-----|-----|-----|-------------------|----|")
        else:
            lines.append("| Metric | Min | Max | Avg |")
            lines.append("|--------|-----|-----|-----|")

        for metric_name in sorted(summary.keys()):
            stats = summary[metric_name]
            min_val = format_score(stats["min"])
            max_val = format_score(stats["max"])
            avg_val = format_score(stats["avg"])

            if has_baseline:
                baseline_avg = ""
                if metric_name in baseline_summary and baseline_summary[metric_name]:
                    baseline_avg = format_score(
                        sum(baseline_summary[metric_name])
                        / len(baseline_summary[metric_name])
                    )

                # Calculate average percentage change for this metric
                avg_pct_diff = ""
                if metric_name in pct_diff_summary and pct_diff_summary[metric_name]:
                    avg_pct_val = sum(pct_diff_summary[metric_name]) / len(
                        pct_diff_summary[metric_name]
                    )
                    avg_pct_diff = f"{avg_pct_val:.2f}%"

                lines.append(
                    f"| {metric_name} | {min_val} | {max_val} | {avg_val} | {baseline_avg} | {avg_pct_diff} |"
                )
            else:
                lines.append(f"| {metric_name} | {min_val} | {max_val} | {avg_val} |")

        composite = data.get("composite_summary", {})
        if composite:
            min_val = format_score(composite["min"])
            max_val = format_score(composite["max"])
            avg_val = format_score(composite["avg"])
            if has_baseline:
                lines.append(
                    f"| **composite** | **{min_val}** | **{max_val}** | **{avg_val}** | **—** | **—** |"
                )
            else:
                lines.append(
                    f"| **composite** | **{min_val}** | **{max_val}** | **{avg_val}** |"
                )
    else:
        lines.append("## Metrics Summary")
        lines.append("")
        lines.append("No metric scores to summarize.")

    return "\n".join(lines)


def markdown_main(args: MarkdownArgs) -> int:
    """Main entry point for the markdown command."""
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}", file=sys.stderr)
        return 1

    markdown = generate_markdown_table(data)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(markdown)
            print(f"Markdown table written to: {args.output}")
        except Exception as e:
            print(f"Error writing output file: {e}", file=sys.stderr)
            return 1
    else:
        print(markdown)

    return 0
