from __future__ import annotations
from typing import List, Optional, Callable
import html

from .report import BatchReport, Report, MetricEntry
from .registry import get_higher_is_better


def _esc(value: object) -> str:
    """HTML-escape any value for safe embedding."""
    try:
        return html.escape(str(value), quote=True)
    except Exception:
        return html.escape(repr(value), quote=True)


def _render_metric_row(
    m: MetricEntry, get_higher_is_better_fn: Callable[[str], bool]
) -> str:
    score = "" if m.score is None else f"{float(m.score):.4f}"
    status = m.status
    cls = "ok" if status == "ok" else "error"
    err = _esc(m.error) if m.error else ""
    timing = "" if m.timing_ms is None else f"{float(m.timing_ms):.1f} ms"
    # Extract optional baseline and pct diff from extras
    baseline = None
    pct = None
    pct_cls = ""
    try:
        if isinstance(m.extras, dict):
            b = m.extras.get("baseline") or {}
            if isinstance(b, dict):
                bav = b.get("avg")
                if bav is not None:
                    baseline = f"{float(bav):.4f}"
            p = m.extras.get("pct_diff")
            if p is not None:
                pct_val = float(p)
                pct = f"{pct_val:.2f}%"
                higher_is_better = get_higher_is_better_fn(m.name)
                if higher_is_better:
                    # For metrics where bigger is better: positive is good, negative is bad
                    if pct_val > 0:
                        pct_cls = " positive"
                    elif pct_val < 0:
                        pct_cls = " negative"
                else:
                    # For metrics where smaller is better: negative is good, positive is bad
                    if pct_val < 0:
                        pct_cls = " positive"
                    elif pct_val > 0:
                        pct_cls = " negative"
    except Exception:
        pass
    baseline_html = baseline or ""
    pct_html = pct or ""
    return (
        f'<tr class="metric {cls}">'
        f'<td class="name">{_esc(m.name)}</td>'
        f'<td class="score">{score}</td>'
        f'<td class="baseline">{baseline_html}</td>'
        f'<td class="pctdiff{pct_cls}">{pct_html}</td>'
        f'<td class="status">{_esc(status)}</td>'
        f'<td class="timing">{timing}</td>'
        f'<td class="error">{err}</td>'
        "</tr>"
    )


def _render_report_block(rpt: Report, index: int) -> str:
    inputs = rpt.inputs
    # Extract fields from InputItem dataclass (or use defaults if inputs is None)
    title = _esc(getattr(inputs, "id", None) or getattr(inputs, "video", None) or f"item {index}")
    video = _esc(getattr(inputs, "video", ""))
    reference = _esc(getattr(inputs, "reference", ""))
    prompt = _esc(getattr(inputs, "prompt", ""))
    composite = rpt.composite or {}
    composite_score = composite.get("score")
    composite_html = (
        f'<span class="composite">composite={composite_score:.4f}</span>'
        if composite.get("enabled") and composite_score is not None
        else ""
    )

    metric_rows = "\n".join(
        _render_metric_row(m, get_higher_is_better) for m in rpt.metrics
    )

    info_lines: List[str] = []
    if video:
        info_lines.append(f"<div><b>video</b>: {video}</div>")
    if reference:
        info_lines.append(f"<div><b>reference</b>: {reference}</div>")
    if prompt:
        info_lines.append(f"<div><b>prompt</b>: {prompt}</div>")
    info_html = "\n".join(info_lines)

    return f"""
    <section class=\"report\" id=\"report-{index}\">
      <h2>Item {index}: {title} {composite_html}</h2>
      <div class=\"inputs\">{info_html}</div>
      <table class=\"metrics\">
        <thead>
          <tr><th>metric</th><th>score</th><th>baseline (ref avg)</th><th>%Δ</th><th>status</th><th>time</th><th>error</th></tr>
        </thead>
        <tbody>
          {metric_rows}
        </tbody>
      </table>
    </section>
    """


def render_batch_report_html(batch: BatchReport, title: Optional[str] = None) -> str:
    """Render a complete, self-contained HTML report for a BatchReport."""
    page_title = title or "Surveyor2 Report"

    # Calculate baseline averages and percentage changes for summary
    # Note: baseline is calculated per-prompt as average of reference videos metrics
    baseline_summary = {}
    pct_diff_summary = {}

    for report in batch.reports:
        for metric in report.metrics:
            if metric.status != "ok" or metric.score is None:
                continue
            name = metric.name
            if isinstance(metric.extras, dict):
                baseline = metric.extras.get("baseline", {})
                pct_diff = metric.extras.get("pct_diff")

                if isinstance(baseline, dict) and baseline.get("avg") is not None:
                    if name not in baseline_summary:
                        baseline_summary[name] = []
                    baseline_summary[name].append(float(baseline["avg"]))

                if pct_diff is not None:
                    if name not in pct_diff_summary:
                        pct_diff_summary[name] = []
                    pct_diff_summary[name].append(float(pct_diff))

    # Summary table (per-metric min/max/avg + baseline avg + avg %Δ)
    summary_rows: List[str] = []
    for name in sorted((batch.summary or {}).keys()):
        s = batch.summary[name]

        # Calculate baseline average for this metric
        baseline_avg = ""
        if name in baseline_summary and baseline_summary[name]:
            baseline_avg = (
                f"{sum(baseline_summary[name]) / len(baseline_summary[name]):.4f}"
            )

        # Calculate average percentage change for this metric
        avg_pct_diff = ""
        avg_pct_cls = ""
        if name in pct_diff_summary and pct_diff_summary[name]:
            avg_pct_val = sum(pct_diff_summary[name]) / len(pct_diff_summary[name])
            avg_pct_diff = f"{avg_pct_val:.2f}%"
            higher_is_better = get_higher_is_better(name)
            if higher_is_better:
                # For metrics where bigger is better: positive is good, negative is bad
                if avg_pct_val > 0:
                    avg_pct_cls = " positive"
                elif avg_pct_val < 0:
                    avg_pct_cls = " negative"
            else:
                # For metrics where smaller is better: negative is good, positive is bad
                if avg_pct_val < 0:
                    avg_pct_cls = " positive"
                elif avg_pct_val > 0:
                    avg_pct_cls = " negative"

        summary_rows.append(
            "<tr>"
            f'<td class="name">{_esc(name)}</td>'
            f"<td class=\"min\">{float(s['min']):.4f}</td>"
            f"<td class=\"max\">{float(s['max']):.4f}</td>"
            f"<td class=\"avg\">{float(s['avg']):.4f}</td>"
            f'<td class="baseline">{baseline_avg}</td>'
            f'<td class="pctdiff{avg_pct_cls}">{avg_pct_diff}</td>'
            "</tr>"
        )

    # Add composite summary as last row if available
    comp = batch.composite_summary or {}
    if comp:
        summary_rows.append(
            '<tr class="composite-row">'
            f'<td class="name"><strong>composite</strong></td>'
            f"<td class=\"min\"><strong>{float(comp['min']):.4f}</strong></td>"
            f"<td class=\"max\"><strong>{float(comp['max']):.4f}</strong></td>"
            f"<td class=\"avg\"><strong>{float(comp['avg']):.4f}</strong></td>"
            f'<td class="baseline"><strong>—</strong></td>'
            f'<td class="pctdiff"><strong>—</strong></td>'
            "</tr>"
        )

    summary_table = (
        (
            '<table class="summary">\n'
            "  <thead><tr><th>metric</th><th>min</th><th>max</th><th>avg</th><th>baseline (ref avg)</th><th>%Δ</th></tr></thead>\n"
            "  <tbody>" + "\n".join(summary_rows) + "</tbody>\n"
            "</table>"
        )
        if summary_rows
        else '<div class="empty">No metric scores to summarize.</div>'
    )

    # Errors table
    errors_rows: List[str] = []
    for err_obj in batch.errors or []:
        err_id = _esc(err_obj.get("id", "unknown"))
        metric = _esc(err_obj.get("metric_name") or "—")
        error_text = _esc(err_obj.get("error", ""))
        errors_rows.append(
            "<tr>"
            f'<td class="id">{err_id}</td>'
            f'<td class="metric">{metric}</td>'
            f'<td class="error">{error_text}</td>'
            "</tr>"
        )
    errors_table = (
        (
            '<section class="errors">'
            "<h2>Errors</h2>"
            '<table class="errors-table">\n'
            "  <thead><tr><th>ID</th><th>Metric</th><th>Error</th></tr></thead>\n"
            "  <tbody>" + "\n".join(errors_rows) + "</tbody>\n"
            "</table>"
            "</section>"
        )
        if errors_rows
        else ""
    )

    report_blocks = "\n".join(
        _render_report_block(rpt, i) for i, rpt in enumerate(batch.reports, start=1)
    )

    style = """
    <style>
      :root { --bg: #0f172a; --fg: #e2e8f0; --muted:#94a3b8; --accent:#22d3ee; --ok:#22c55e; --err:#ef4444; }
      html, body { margin:0; padding:0; background:var(--bg); color:var(--fg); font: 14px/1.5 system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, sans-serif; }
      header { padding: 16px 24px; border-bottom: 1px solid #1f2937; }
      header h1 { margin: 0 0 6px 0; font-size: 18px; }
      header .meta { color: var(--muted); }
      main { padding: 20px 24px 40px; max-width: 1100px; margin: 0 auto; }
      .summary { margin: 16px 0; }
      .errors { margin: 24px 0; padding: 16px; border: 1px solid #dc2626; border-radius: 10px; background: #1a0a0a; }
      .errors h2 { margin: 0 0 12px 0; font-size: 16px; color: var(--err); }
      .errors-table td.error { color: var(--err); }
      table { width: 100%; border-collapse: collapse; background: #0b1220; border: 1px solid #1f2937; border-radius: 8px; overflow: hidden; }
      thead { background: #111827; color: var(--muted); }
      th, td { padding: 8px 10px; border-bottom: 1px solid #1f2937; text-align: left; }
      .composite-row { background: #1a1f35; border-top: 2px solid var(--accent); }
      .composite-row td { color: var(--accent); padding: 10px; }
      .report { margin: 28px 0; padding: 16px; border: 1px solid #1f2937; border-radius: 10px; background: #0b1220; }
      .report h2 { margin: 0 0 8px 0; font-size: 16px; }
      .report .inputs { color: var(--muted); margin-bottom: 8px; }
      .metric.ok .status { color: var(--ok); }
      .metric.error .status { color: var(--err); font-weight: 600; }
      .metric .error { color: var(--err); }
      .composite { color: var(--accent); margin-left: 8px; font-weight: 600; }
      .empty { color: var(--muted); font-style: italic; }
      .pctdiff { text-align: right; }
      .pctdiff.positive { color: var(--ok); }
      .pctdiff.negative { color: var(--err); }
      .baseline { text-align: right; color: var(--muted); }
      footer { color: var(--muted); padding: 18px 24px; border-top: 1px solid #1f2937; }
      a { color: var(--accent); text-decoration: none; }
    </style>
    """

    run_meta = batch.run or {}
    started_at = _esc(run_meta.get("started_at", ""))
    count = _esc(run_meta.get("count", len(batch.reports)))
    cfg_hash = _esc(run_meta.get("config_hash", ""))

    return f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{_esc(page_title)}</title>
  {style}
</head>
<body>
  <header>
    <h1>{_esc(page_title)}</h1>
    <div class=\"meta\">started_at: {started_at} · items: {count} · config: {cfg_hash}</div>
  </header>
  <main>
    <section class=\"summary\">{summary_table}</section>
    {errors_table}
    {report_blocks}
  </main>
  <footer>Generated by Surveyor2</footer>
</body>
</html>
"""
