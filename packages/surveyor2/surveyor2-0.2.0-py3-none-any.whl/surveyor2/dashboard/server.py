"""Dashboard server for viewing video quality reports in a web interface."""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ..core.types.cli import DashboardArgs


def load_report(report_path: Path) -> Optional[Dict[str, Any]]:
    """Load a single report JSON file."""
    try:
        with open(report_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Failed to load {report_path}: {e}", file=sys.stderr)
        return None


def find_reports(path: Path) -> List[Tuple[str, Dict[str, Any]]]:
    """Find all report JSON files in the given path.
    
    Args:
        path: Either a single report file or a directory containing reports
        
    Returns:
        List of tuples (report_name, report_data)
    """
    reports = []
    
    if path.is_file():
        report = load_report(path)
        if report:
            reports.append((path.stem, report))
    elif path.is_dir():
        for json_file in sorted(path.glob("**/*.json")):
            report = load_report(json_file)
            if report and "reports" in report:
                relative_name = str(json_file.relative_to(path))
                reports.append((relative_name, report))
    
    return reports


def get_metric_info(metric_name: str) -> Dict[str, Any]:
    """Get metric metadata. All metrics are normalized to higher_is_better."""
    return {"higher_is_better": True}


def create_app(reports_list: List[Tuple[str, Dict[str, Any]]]):
    """Create the Flask application."""
    from flask import Flask, render_template, jsonify, send_file
    
    dashboard_dir = Path(__file__).parent
    app = Flask(
        __name__,
        template_folder=str(dashboard_dir / "templates"),
        static_folder=str(dashboard_dir / "static"),
    )
    
    app.config["REPORTS"] = reports_list
    
    @app.route("/")
    def index():
        """Main dashboard page."""
        return render_template("index.html", reports=reports_list)
    
    @app.route("/api/report/<int:report_idx>")
    def get_report(report_idx: int):
        """API endpoint to get report data."""
        if report_idx < 0 or report_idx >= len(reports_list):
            return jsonify({"error": "Invalid report index"}), 404
        
        report_name, report_data = reports_list[report_idx]
        
        video_pairs = []
        for item_report in report_data.get("reports", []):
            inputs = item_report.get("inputs", {})
            results = item_report.get("results", [])
            
            metric_data = {}
            for result in results:
                metric = result.get("generated", {})
                baseline = result.get("baseline", [])
                
                if metric.get("status") == "ok" and metric.get("score") is not None:
                    metric_name = metric.get("name")
                    
                    baseline_scores = [bm.get("score") for bm in baseline 
                                     if bm.get("status") == "ok" and bm.get("score") is not None]
                    baseline_avg = None
                    pct_diff = None
                    quality_label = None
                    
                    if baseline_scores:
                        baseline_avg = sum(baseline_scores) / len(baseline_scores)
                        gen_score = float(metric.get("score"))
                        if baseline_avg != 0:
                            pct_diff = ((gen_score - baseline_avg) / baseline_avg) * 100.0
                        
                        if len(baseline_scores) == 1:
                            try:
                                from ..core.registry import get_metric_cls
                                metric_cls = get_metric_cls(metric_name)
                                ranges = metric_cls.get_quality_ranges()
                                if ranges:
                                    for min_val, max_val, label in ranges:
                                        if min_val <= gen_score < max_val:
                                            quality_label = label
                                            break
                                        if gen_score == 1.0 and max_val == 1.0:
                                            quality_label = label
                                            break
                            except (KeyError, Exception):
                                pass
                    
                    metric_data[metric_name] = {
                        "generated_score": metric.get("score"),
                        "reference_score": baseline_avg,
                        "higher_is_better": get_metric_info(metric_name)["higher_is_better"],
                        "pct_diff": pct_diff,
                        "quality_label": quality_label,
                        "weight": 1.0
                    }
            
            composite = item_report.get("composite", {})
            composite_data = None
            composite_score = composite.get("score")
            if composite_score is not None:
                from ..core.report import Report
                temp_report = Report.from_json(json.dumps(item_report))
                composite_pct_diff = temp_report.get_composite_pct_diff()
                composite_data = {
                    "generated_score": composite_score,
                    "reference_score": None,
                    "higher_is_better": True,
                    "pct_diff": composite_pct_diff
                }
            
            video_pairs.append({
                "id": inputs.get("id", "unknown"),
                "prompt": inputs.get("prompt", ""),
                "video": inputs.get("video", ""),
                "reference": inputs.get("reference", ""),
                "metrics": metric_data,
                "composite": composite_data
            })
        
        return jsonify({
            "name": report_name,
            "video_pairs": video_pairs
        })
    
    @app.route("/video/<path:video_path>")
    def serve_video(video_path: str):
        """Serve video files."""
        video_path = "/" + video_path if not video_path.startswith("/") else video_path
        video_file = Path(video_path)
        if not video_file.exists():
            return "Video not found", 404
        return send_file(video_file, mimetype="video/mp4")
    
    return app


def dashboard_main(args: DashboardArgs) -> int:
    """Main entry point for the dashboard command."""
    try:
        from flask import Flask
    except ImportError:
        print("Error: Flask is required for the dashboard feature.", file=sys.stderr)
        print("Install it with: pip install flask", file=sys.stderr)
        return 1
    
    path = Path(args.path)
    if not path.exists():
        print(f"Error: Path not found: {args.path}", file=sys.stderr)
        return 1
    
    reports_list = find_reports(path)
    if not reports_list:
        print(f"Error: No valid reports found in {args.path}", file=sys.stderr)
        return 1
    
    print(f"Found {len(reports_list)} report(s)")
    
    app = create_app(reports_list)
    
    host = "0.0.0.0" if args.bind_all else "127.0.0.1"
    port = args.port
    
    print(f"\n{'='*60}")
    print(f"Starting Surveyor2 Dashboard")
    print(f"{'='*60}")
    print(f"URL: http://{host if host != '0.0.0.0' else 'localhost'}:{port}")
    if args.bind_all:
        print(f"Server is accessible from all network interfaces")
    else:
        print(f"Server is only accessible locally (use --bind-all to expose)")
    print(f"{'='*60}\n")
    
    try:
        app.run(host=host, port=port, debug=False)
    except KeyboardInterrupt:
        print("\nShutting down dashboard...")
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        return 1
    
    return 0
