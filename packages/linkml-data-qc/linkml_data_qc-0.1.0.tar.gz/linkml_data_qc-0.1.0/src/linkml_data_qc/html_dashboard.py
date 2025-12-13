"""HTML dashboard generator for compliance reports.

Generates a static HTML site with multiple PNG visualizations that can be
deployed to GitHub Pages or any static hosting.

Example CLI usage:
    linkml-data-qc data.yaml -s schema.yaml -t MyClass --dashboard-dir ./qc_dashboard/

Example Python usage:
    from linkml_data_qc.html_dashboard import generate_html_dashboard
    generate_html_dashboard(report, output_dir="./qc_dashboard")
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import ComplianceReport

# Check if visualization libraries are available
try:
    import matplotlib.pyplot as plt

    from .dashboard import (
        VIZ_AVAILABLE,
        plot_compliance_gauge,
        plot_comparison,
        plot_path_heatmap,
        plot_slot_bars,
        plot_threshold_violations,
    )
except ImportError:
    VIZ_AVAILABLE = False


def _require_viz() -> None:
    """Raise ImportError if visualization libraries are not available."""
    if not VIZ_AVAILABLE:
        raise ImportError(
            "Visualization libraries not available. "
            "Install with: pip install linkml-data-qc[viz]"
        )


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QC Dashboard - {title}</title>
    <style>
        :root {{
            --green: #2ecc71;
            --orange: #f39c12;
            --red: #e74c3c;
            --dark-red: #c0392b;
            --bg: #f5f6fa;
            --card-bg: #ffffff;
            --text: #2c3e50;
            --text-light: #7f8c8d;
            --border: #dcdde1;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            padding: 2rem;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        header {{
            text-align: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--border);
        }}
        h1 {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}
        .subtitle {{
            color: var(--text-light);
            font-size: 0.95rem;
        }}
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        .card {{
            background: var(--card-bg);
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .card h3 {{
            font-size: 0.85rem;
            color: var(--text-light);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
        }}
        .card .value {{
            font-size: 2rem;
            font-weight: 700;
        }}
        .card .value.good {{ color: var(--green); }}
        .card .value.warning {{ color: var(--orange); }}
        .card .value.bad {{ color: var(--red); }}
        .card .detail {{
            font-size: 0.85rem;
            color: var(--text-light);
            margin-top: 0.25rem;
        }}
        .charts {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        .chart-card {{
            background: var(--card-bg);
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .chart-card h2 {{
            font-size: 1.1rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--border);
        }}
        .chart-card img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        .violations {{
            background: #fff5f5;
            border-left: 4px solid var(--red);
        }}
        .violations.none {{
            background: #f0fff4;
            border-left-color: var(--green);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }}
        th, td {{
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        th {{
            background: var(--bg);
            font-weight: 600;
        }}
        tr:hover {{
            background: var(--bg);
        }}
        .slot-table .bar {{
            height: 8px;
            border-radius: 4px;
            background: var(--border);
        }}
        .slot-table .bar-fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 0.3s;
        }}
        footer {{
            text-align: center;
            padding-top: 2rem;
            border-top: 1px solid var(--border);
            color: var(--text-light);
            font-size: 0.85rem;
        }}
        footer a {{
            color: var(--text);
        }}
        @media (max-width: 768px) {{
            body {{ padding: 1rem; }}
            .charts {{ grid-template-columns: 1fr; }}
            h1 {{ font-size: 1.5rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>QC Dashboard</h1>
            <p class="subtitle">{subtitle}</p>
        </header>

        <section class="summary-cards">
            <div class="card">
                <h3>Global Compliance</h3>
                <div class="value {global_class}">{global_compliance:.1f}%</div>
                <div class="detail">{total_populated}/{total_checks} fields populated</div>
            </div>
            <div class="card">
                <h3>Weighted Compliance</h3>
                <div class="value {weighted_class}">{weighted_compliance:.1f}%</div>
                <div class="detail">Based on configured weights</div>
            </div>
            <div class="card">
                <h3>Threshold Violations</h3>
                <div class="value {violations_class}">{violation_count}</div>
                <div class="detail">{violations_detail}</div>
            </div>
            <div class="card">
                <h3>Recommended Slots</h3>
                <div class="value">{slot_count}</div>
                <div class="detail">Tracked across schema</div>
            </div>
        </section>

        <section class="charts">
            <div class="chart-card">
                <h2>Overall Compliance</h2>
                <img src="gauge.png" alt="Compliance Gauge">
            </div>
            <div class="chart-card">
                <h2>Compliance by Slot</h2>
                <img src="slot_bars.png" alt="Slot Compliance">
            </div>
        </section>

        {heatmap_section}

        {violations_section}

        <section class="chart-card">
            <h2>Slot Compliance Details</h2>
            <table class="slot-table">
                <thead>
                    <tr>
                        <th>Slot</th>
                        <th>Compliance</th>
                        <th style="width: 40%">Progress</th>
                    </tr>
                </thead>
                <tbody>
                    {slot_rows}
                </tbody>
            </table>
        </section>

        <footer>
            <p>Generated by <a href="https://github.com/linkml/linkml-data-qc">linkml-data-qc</a> on {timestamp}</p>
            {config_info}
        </footer>
    </div>
</body>
</html>
"""

HEATMAP_SECTION = """
        <section class="charts">
            <div class="chart-card" style="grid-column: 1 / -1;">
                <h2>Path × Slot Heatmap</h2>
                <img src="path_heatmap.png" alt="Path Heatmap">
            </div>
        </section>
"""

VIOLATIONS_SECTION = """
        <section class="chart-card violations {violations_card_class}">
            <h2>Threshold Violations</h2>
            {violations_content}
        </section>
"""


def _get_compliance_class(value: float) -> str:
    """Get CSS class based on compliance value."""
    if value >= 95:
        return "good"
    elif value >= 80:
        return "warning"
    else:
        return "bad"


def _get_bar_color(value: float) -> str:
    """Get bar color based on compliance value."""
    if value >= 95:
        return "#2ecc71"
    elif value >= 80:
        return "#f39c12"
    elif value >= 60:
        return "#e74c3c"
    else:
        return "#c0392b"


def generate_html_dashboard(
    report: ComplianceReport,
    output_dir: str | Path,
    *,
    title: str | None = None,
) -> Path:
    """Generate an HTML dashboard with multiple PNG visualizations.

    Creates a directory containing:
    - index.html - Main dashboard page
    - gauge.png - Compliance gauge chart
    - slot_bars.png - Slot compliance bar chart
    - path_heatmap.png - Path × Slot heatmap (if applicable)
    - violations.png - Threshold violations chart (if violations exist)
    - report.json - Raw report data

    Args:
        report: ComplianceReport to visualize
        output_dir: Directory to write dashboard files
        title: Optional custom title

    Returns:
        Path to the output directory
    """
    _require_viz()

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate PNG charts
    _generate_charts(report, output_path)

    # Generate HTML
    html_content = _generate_html(report, title)
    (output_path / "index.html").write_text(html_content)

    # Save raw report data as JSON
    report_data = {
        "file_path": report.file_path,
        "target_class": report.target_class,
        "schema_path": report.schema_path,
        "global_compliance": report.global_compliance,
        "weighted_compliance": report.weighted_compliance,
        "total_checks": report.total_checks,
        "total_populated": report.total_populated,
        "summary_by_slot": report.summary_by_slot,
        "threshold_violations": [
            {
                "path": v.path,
                "slot_name": v.slot_name,
                "actual_compliance": v.actual_compliance,
                "min_required": v.min_required,
                "shortfall": v.shortfall,
            }
            for v in report.threshold_violations
        ],
        "recommended_slots": report.recommended_slots,
        "config_path": report.config_path,
    }
    (output_path / "report.json").write_text(json.dumps(report_data, indent=2))

    return output_path


def generate_html_dashboard_multi(
    reports: list[ComplianceReport],
    output_dir: str | Path,
    *,
    title: str | None = None,
    max_detail_files: int = 10,
) -> Path:
    """Generate an HTML dashboard comparing multiple reports.

    Files are sorted by compliance (worst first) to prioritize curation.
    Only generates detailed charts for the top N worst files to save space.

    Args:
        reports: List of ComplianceReport objects to compare
        output_dir: Directory to write dashboard files
        title: Optional custom title
        max_detail_files: Maximum number of files to generate detailed charts for

    Returns:
        Path to the output directory
    """
    _require_viz()

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Sort reports by compliance (worst first) for prioritization
    sorted_reports = sorted(reports, key=lambda r: r.global_compliance)

    # Generate comparison chart (slot-level across all files)
    fig = plot_comparison(sorted_reports[:20])  # Limit to 20 for readability
    fig.savefig(output_path / "comparison.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # Generate detailed charts only for worst N files
    worst_reports = sorted_reports[:max_detail_files]
    for i, report in enumerate(worst_reports):
        fig = plot_slot_bars(report, show_thresholds=True)
        fig.savefig(output_path / f"detail_{i}.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    # Generate comparison HTML
    html_content = _generate_comparison_html(sorted_reports, title, max_detail_files)
    (output_path / "index.html").write_text(html_content)

    # Save JSON report for all files
    all_reports_data = [
        {
            "file": Path(r.file_path).name,
            "global_compliance": r.global_compliance,
            "weighted_compliance": r.weighted_compliance,
            "total_checks": r.total_checks,
            "total_populated": r.total_populated,
            "violations": len(r.threshold_violations),
        }
        for r in sorted_reports
    ]
    (output_path / "reports.json").write_text(json.dumps(all_reports_data, indent=2))

    return output_path


def _generate_charts(report: ComplianceReport, output_path: Path) -> None:
    """Generate all PNG charts for the dashboard."""
    # Compliance gauge
    fig = plot_compliance_gauge(report)
    fig.savefig(output_path / "gauge.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # Slot bars
    fig = plot_slot_bars(report, show_thresholds=True)
    fig.savefig(output_path / "slot_bars.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # Path heatmap (only if we have aggregated scores)
    if report.aggregated_scores:
        fig = plot_path_heatmap(report)
        fig.savefig(output_path / "path_heatmap.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    # Violations chart (only if we have violations)
    if report.threshold_violations:
        fig = plot_threshold_violations(report)
        fig.savefig(output_path / "violations.png", dpi=150, bbox_inches="tight")
        plt.close(fig)


def _generate_html(report: ComplianceReport, title: str | None) -> str:
    """Generate the HTML content for the dashboard."""
    # Prepare slot rows
    slot_rows = []
    for slot, pct in sorted(report.summary_by_slot.items(), key=lambda x: x[1]):
        color = _get_bar_color(pct)
        slot_rows.append(
            f"""<tr>
                <td><code>{slot}</code></td>
                <td>{pct:.1f}%</td>
                <td>
                    <div class="bar">
                        <div class="bar-fill" style="width: {pct}%; background: {color};"></div>
                    </div>
                </td>
            </tr>"""
        )

    # Heatmap section
    heatmap_section = HEATMAP_SECTION if report.aggregated_scores else ""

    # Violations section
    if report.threshold_violations:
        violations_content = '<img src="violations.png" alt="Threshold Violations">'
        violations_card_class = ""
        violations_detail = f"{len(report.threshold_violations)} slot(s) below threshold"
    else:
        violations_content = "<p style='padding: 2rem; text-align: center; color: #2ecc71;'>No threshold violations detected.</p>"
        violations_card_class = "none"
        violations_detail = "All thresholds met"

    violations_section = VIOLATIONS_SECTION.format(
        violations_card_class=violations_card_class,
        violations_content=violations_content,
    )

    # Config info
    config_info = ""
    if report.config_path:
        config_info = f"<p>Configuration: <code>{report.config_path}</code></p>"

    # Build subtitle
    file_name = Path(report.file_path).name
    subtitle = f"{file_name} • {report.target_class} • Schema: {Path(report.schema_path).name}"

    return HTML_TEMPLATE.format(
        title=title or file_name,
        subtitle=subtitle,
        global_compliance=report.global_compliance,
        global_class=_get_compliance_class(report.global_compliance),
        weighted_compliance=report.weighted_compliance,
        weighted_class=_get_compliance_class(report.weighted_compliance),
        total_populated=report.total_populated,
        total_checks=report.total_checks,
        violation_count=len(report.threshold_violations),
        violations_class="bad" if report.threshold_violations else "good",
        violations_detail=violations_detail,
        slot_count=len(report.recommended_slots),
        slot_rows="\n".join(slot_rows),
        heatmap_section=heatmap_section,
        violations_section=violations_section,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
        config_info=config_info,
    )


def _generate_comparison_html(
    reports: list[ComplianceReport],
    title: str | None,
    max_detail_files: int = 10,
) -> str:
    """Generate HTML for multi-file comparison dashboard.

    Args:
        reports: List of reports (should be pre-sorted by compliance, worst first)
        title: Optional dashboard title
        max_detail_files: Number of worst files with detailed charts
    """
    # Build file comparison table with priority indicators
    file_rows = []
    for i, report in enumerate(reports):
        file_name = Path(report.file_path).name
        global_class = _get_compliance_class(report.global_compliance)
        violations = len(report.threshold_violations)
        # Add priority badge for worst files
        priority_badge = ""
        if i < max_detail_files:
            priority_badge = f'<span class="priority-badge">#{i + 1}</span> '
        file_rows.append(
            f"""<tr class="{'priority-row' if i < max_detail_files else ''}">
                <td>{priority_badge}<code>{file_name}</code></td>
                <td class="{global_class}">{report.global_compliance:.1f}%</td>
                <td>{report.weighted_compliance:.1f}%</td>
                <td>{report.total_populated}/{report.total_checks}</td>
                <td>{"" if violations == 0 else violations}</td>
            </tr>"""
        )

    # Calculate totals
    total_checks = sum(r.total_checks for r in reports)
    total_populated = sum(r.total_populated for r in reports)
    avg_compliance = (total_populated / total_checks * 100) if total_checks > 0 else 100.0
    total_violations = sum(len(r.threshold_violations) for r in reports)

    # Build detail charts section for worst files
    detail_charts = []
    worst_count = min(max_detail_files, len(reports))
    for i in range(worst_count):
        report = reports[i]
        file_name = Path(report.file_path).name
        detail_charts.append(
            f"""<div class="detail-card">
                <h3>#{i + 1}: {file_name} ({report.global_compliance:.1f}%)</h3>
                <img src="detail_{i}.png" alt="Detail for {file_name}">
            </div>"""
        )

    detail_section = ""
    if detail_charts:
        detail_section = f"""
        <section class="chart-card">
            <h2>Priority Files - Detailed View</h2>
            <p class="priority-note">Showing the {worst_count} files with lowest compliance for prioritized curation.</p>
            <div class="detail-grid">
                {"".join(detail_charts)}
            </div>
        </section>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QC Dashboard - {title or "Comparison"}</title>
    <style>
        :root {{
            --green: #2ecc71;
            --orange: #f39c12;
            --red: #e74c3c;
            --bg: #f5f6fa;
            --card-bg: #ffffff;
            --text: #2c3e50;
            --text-light: #7f8c8d;
            --border: #dcdde1;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            padding: 2rem;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        header {{ text-align: center; margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 2px solid var(--border); }}
        h1 {{ font-size: 2rem; margin-bottom: 0.5rem; }}
        .subtitle {{ color: var(--text-light); }}
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        .card {{
            background: var(--card-bg);
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .card h3 {{ font-size: 0.85rem; color: var(--text-light); text-transform: uppercase; margin-bottom: 0.5rem; }}
        .card .value {{ font-size: 2rem; font-weight: 700; }}
        .card .value.good {{ color: var(--green); }}
        .card .value.warning {{ color: var(--orange); }}
        .card .value.bad {{ color: var(--red); }}
        .chart-card {{
            background: var(--card-bg);
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }}
        .chart-card h2 {{ font-size: 1.1rem; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border); }}
        .chart-card img {{ width: 100%; height: auto; display: block; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
        th, td {{ padding: 0.75rem; text-align: left; border-bottom: 1px solid var(--border); }}
        th {{ background: var(--bg); font-weight: 600; }}
        tr:hover {{ background: var(--bg); }}
        .good {{ color: var(--green); font-weight: 600; }}
        .warning {{ color: var(--orange); font-weight: 600; }}
        .bad {{ color: var(--red); font-weight: 600; }}
        .priority-badge {{
            display: inline-block;
            background: var(--red);
            color: white;
            padding: 0.15rem 0.4rem;
            border-radius: 3px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-right: 0.3rem;
        }}
        .priority-row {{
            background: #fff5f5;
        }}
        .priority-row:hover {{
            background: #ffe5e5;
        }}
        .priority-note {{
            color: var(--text-light);
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }}
        .detail-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 1.5rem;
            margin-top: 1rem;
        }}
        .detail-card {{
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 1rem;
            background: var(--bg);
        }}
        .detail-card h3 {{
            font-size: 0.9rem;
            margin-bottom: 0.75rem;
            color: var(--red);
        }}
        .detail-card img {{
            width: 100%;
            height: auto;
        }}
        footer {{ text-align: center; padding-top: 2rem; border-top: 1px solid var(--border); color: var(--text-light); font-size: 0.85rem; }}
        footer a {{ color: var(--text); }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>QC Dashboard - Multi-File Comparison</h1>
            <p class="subtitle">{len(reports)} files analyzed (sorted by compliance, lowest first)</p>
        </header>

        <section class="summary-cards">
            <div class="card">
                <h3>Files Analyzed</h3>
                <div class="value">{len(reports)}</div>
            </div>
            <div class="card">
                <h3>Average Compliance</h3>
                <div class="value {_get_compliance_class(avg_compliance)}">{avg_compliance:.1f}%</div>
            </div>
            <div class="card">
                <h3>Total Checks</h3>
                <div class="value">{total_populated}/{total_checks}</div>
            </div>
            <div class="card">
                <h3>Total Violations</h3>
                <div class="value {"bad" if total_violations else "good"}">{total_violations}</div>
            </div>
        </section>

        <section class="chart-card">
            <h2>Slot Compliance Comparison</h2>
            <img src="comparison.png" alt="File Comparison">
        </section>

        {detail_section}

        <section class="chart-card">
            <h2>All Files (Sorted by Priority)</h2>
            <p class="priority-note">Files with lowest compliance are listed first to prioritize curation efforts.</p>
            <table>
                <thead>
                    <tr>
                        <th>File</th>
                        <th>Global</th>
                        <th>Weighted</th>
                        <th>Populated</th>
                        <th>Violations</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(file_rows)}
                </tbody>
            </table>
        </section>

        <footer>
            <p>Generated by <a href="https://github.com/linkml/linkml-data-qc">linkml-data-qc</a> on {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
        </footer>
    </div>
</body>
</html>
"""
    return html
