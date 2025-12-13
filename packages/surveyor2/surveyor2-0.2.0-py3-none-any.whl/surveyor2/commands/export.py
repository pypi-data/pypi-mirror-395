"""Export command for generating CSV, HTML, or Markdown reports from JSON reports."""

import csv
import json
import sys
from io import StringIO
from pathlib import Path
from typing import Any, Dict, List

from ..core.types.cli import ExportArgs


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
        generated_results = report.get("generated_results", [])
        baseline_results = report.get("baseline_results", [])
        
        baseline_by_name: Dict[str, List[float]] = {}
        for metric_idx, metric in enumerate(generated_results):
            if metric_idx < len(baseline_results):
                metric_name = metric.get("name")
                for bm in baseline_results[metric_idx]:
                    if bm.get("status") == "ok" and bm.get("score") is not None:
                        baseline_by_name.setdefault(metric_name, []).append(float(bm.get("score")))
        
        for metric in generated_results:
            if metric.get("status") != "ok" or metric.get("score") is None:
                continue
            name = metric.get("name")
            
            if name in baseline_by_name:
                baseline_scores = baseline_by_name[name]
                baseline_avg = sum(baseline_scores) / len(baseline_scores)
                if name not in baseline_summary:
                    baseline_summary[name] = []
                baseline_summary[name].append(baseline_avg)
                
                gen_score = float(metric.get("score"))
                if baseline_avg != 0:
                    pct_diff = ((gen_score - baseline_avg) / baseline_avg) * 100.0
                    if name not in pct_diff_summary:
                        pct_diff_summary[name] = []
                    pct_diff_summary[name].append(pct_diff)

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


def generate_csv_report(data: Dict[str, Any]) -> str:
    """Generate a CSV report with metric scores for each generated video."""
    output = StringIO()
    writer = csv.writer(output)

    reports = data.get("reports", [])
    
    if not reports:
        return output.getvalue()

    # Get all unique metric names across all reports
    metric_names = set()
    for report in reports:
        generated_results = report.get("generated_results", [])
        for metric in generated_results:
            metric_name = metric.get("name", "")
            if metric_name:
                metric_names.add(metric_name)
    metric_names = sorted(metric_names)

    # Build header: Video ID/Path, then all metric names, then composite
    header = ["video"]
    header.extend(metric_names)
    header.append("composite")
    writer.writerow(header)

    # Write each report as a row with just the scores
    for report in reports:
        inputs = report.get("inputs", {})
        # Use video ID if available, otherwise use video path
        video_id = inputs.get("id") or inputs.get("video", "")
        
        row = [video_id]

        # Create a map of metric name to metric data
        generated_results = report.get("generated_results", [])
        metrics_map = {m.get("name"): m for m in generated_results}

        # Fill in metric scores in consistent order
        for metric_name in metric_names:
            if metric_name in metrics_map:
                metric = metrics_map[metric_name]
                score = metric.get("score")
                # Only include score if status is ok and score is not None
                if metric.get("status") == "ok" and score is not None:
                    row.append(format_score(score))
                else:
                    row.append("")
            else:
                # Metric not present for this report
                row.append("")

        # Add composite score
        composite = report.get("composite", {})
        composite_score = composite.get("score")
        if composite_score is not None:
            row.append(format_score(composite_score))
        else:
            row.append("")

        writer.writerow(row)

    return output.getvalue()


def export_main(args: ExportArgs) -> int:
    """Main entry point for the export command."""
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}", file=sys.stderr)
        return 1

    # Generate output based on format
    try:
        if args.format == "markdown":
            output_content = generate_markdown_table(data)
        elif args.format == "csv":
            output_content = generate_csv_report(data)
        else:
            print(f"Error: Unknown format: {args.format}. Supported formats: csv, markdown", file=sys.stderr)
            return 1
    except Exception as e:
        print(f"Error generating {args.format} report: {e}", file=sys.stderr)
        return 1

    # Write or print output
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output_content)
            print(f"{args.format.upper()} report written to: {args.output}")
        except Exception as e:
            print(f"Error writing output file: {e}", file=sys.stderr)
            return 1
    else:
        print(output_content)

    return 0

