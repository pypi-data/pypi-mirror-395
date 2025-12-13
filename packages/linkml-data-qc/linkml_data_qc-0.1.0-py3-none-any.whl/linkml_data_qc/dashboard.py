"""Dashboard visualization for compliance reports.

This module provides visualization functions for ComplianceReport objects.
Visualization dependencies (matplotlib, seaborn) are optional - the module
can be imported without them, but functions will raise ImportError if called.

Install visualization dependencies with::

    pip install linkml-data-qc[viz]

Example - Creating a simple dashboard::

    from linkml_data_qc import ComplianceAnalyzer
    from linkml_data_qc.dashboard import create_dashboard
    analyzer = ComplianceAnalyzer("schema.yaml")
    report = analyzer.analyze_file("data.yaml", "MyClass")
    fig = create_dashboard(report, output_path="dashboard.png")

Example - Individual plots::

    from linkml_data_qc.dashboard import plot_slot_bars, plot_compliance_gauge
    fig1 = plot_compliance_gauge(report)
    fig2 = plot_slot_bars(report, show_thresholds=True)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matplotlib.figure import Figure

    from .models import ComplianceReport

# Check if visualization libraries are available
try:
    import matplotlib.pyplot as plt
    import seaborn as sns

    VIZ_AVAILABLE = True
except ImportError:
    VIZ_AVAILABLE = False
    plt = None  # type: ignore
    sns = None  # type: ignore


def _require_viz() -> None:
    """Raise ImportError if visualization libraries are not available."""
    if not VIZ_AVAILABLE:
        raise ImportError(
            "Visualization libraries not available. "
            "Install with: pip install linkml-data-qc[viz]"
        )


def plot_compliance_gauge(
    report: ComplianceReport,
    *,
    title: str | None = None,
    use_weighted: bool = False,
    figsize: tuple[float, float] = (6, 4),
) -> Figure:
    """Create a gauge/meter visualization of overall compliance.

    Args:
        report: ComplianceReport to visualize
        title: Custom title (defaults to "Compliance: X%")
        use_weighted: If True, show weighted compliance; otherwise global
        figsize: Figure size as (width, height)

    Returns:
        matplotlib Figure object
    """
    _require_viz()

    compliance = report.weighted_compliance if use_weighted else report.global_compliance
    label = "Weighted" if use_weighted else "Global"

    fig, ax = plt.subplots(figsize=figsize)

    # Create a horizontal bar gauge
    colors = _get_compliance_color(compliance)

    # Background bar (gray)
    ax.barh([0], [100], color="#e0e0e0", height=0.5)
    # Compliance bar
    ax.barh([0], [compliance], color=colors, height=0.5)

    # Add compliance percentage text
    ax.text(50, 0, f"{compliance:.1f}%", ha="center", va="center", fontsize=24, fontweight="bold")

    # Styling
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.5, 0.5)
    ax.set_yticks([])
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel("Compliance %")

    if title:
        ax.set_title(title)
    else:
        ax.set_title(f"{label} Compliance: {report.file_path}")

    # Add threshold markers if configured
    ax.axvline(x=80, color="orange", linestyle="--", alpha=0.7, label="Good (80%)")
    ax.axvline(x=95, color="green", linestyle="--", alpha=0.7, label="Excellent (95%)")

    plt.tight_layout()
    return fig


def plot_slot_bars(
    report: ComplianceReport,
    *,
    show_thresholds: bool = False,
    figsize: tuple[float, float] | None = None,
) -> Figure:
    """Create a bar chart showing compliance by slot.

    Args:
        report: ComplianceReport to visualize
        show_thresholds: If True, add threshold lines from config
        figsize: Figure size (auto-calculated if None)

    Returns:
        matplotlib Figure object
    """
    _require_viz()

    slots = list(report.summary_by_slot.keys())
    values = list(report.summary_by_slot.values())

    if not slots:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, "No slot data available", ha="center", va="center", transform=ax.transAxes)
        ax.set_title("Slot Compliance")
        return fig

    # Auto-size based on number of slots
    if figsize is None:
        figsize = (max(6, len(slots) * 0.8), 5)

    fig, ax = plt.subplots(figsize=figsize)

    # Color bars by compliance level
    colors = [_get_compliance_color(v) for v in values]

    bars = ax.bar(slots, values, color=colors, edgecolor="black", linewidth=0.5)

    # Add value labels on bars
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1,
            f"{val:.0f}%",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    # Add threshold lines if requested
    if show_thresholds:
        # Get thresholds from aggregated scores
        threshold_map = {}
        for agg in report.aggregated_scores:
            if agg.min_compliance is not None:
                threshold_map[agg.slot_name] = agg.min_compliance

        for i, slot in enumerate(slots):
            if slot in threshold_map:
                threshold = threshold_map[slot]
                ax.hlines(
                    threshold,
                    i - 0.4,
                    i + 0.4,
                    colors="red",
                    linestyles="--",
                    linewidth=2,
                )

    ax.set_ylabel("Compliance %")
    ax.set_xlabel("Slot")
    ax.set_title(f"Slot Compliance: {report.file_path}")
    ax.set_ylim(0, 105)

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    return fig


def plot_path_heatmap(
    report: ComplianceReport,
    *,
    figsize: tuple[float, float] | None = None,
) -> Figure:
    """Create a heatmap showing compliance by path and slot.

    Uses aggregated path scores to show compliance across normalized paths.

    Args:
        report: ComplianceReport to visualize
        figsize: Figure size (auto-calculated if None)

    Returns:
        matplotlib Figure object
    """
    _require_viz()

    if not report.aggregated_scores:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, "No aggregated path data available", ha="center", va="center", transform=ax.transAxes)
        ax.set_title("Path Compliance Heatmap")
        return fig

    # Build matrix: rows = paths, columns = slots
    paths = sorted(set(agg.path for agg in report.aggregated_scores))
    slots = sorted(set(agg.slot_name for agg in report.aggregated_scores))

    # Create lookup
    data_map = {(agg.path, agg.slot_name): agg.percentage for agg in report.aggregated_scores}

    # Build matrix
    import numpy as np

    matrix = np.full((len(paths), len(slots)), np.nan)
    for i, path in enumerate(paths):
        for j, slot in enumerate(slots):
            if (path, slot) in data_map:
                matrix[i, j] = data_map[(path, slot)]

    # Auto-size
    if figsize is None:
        figsize = (max(6, len(slots) * 1.2), max(4, len(paths) * 0.5))

    fig, ax = plt.subplots(figsize=figsize)

    # Create heatmap
    cmap = sns.color_palette("RdYlGn", as_cmap=True)
    im = ax.imshow(matrix, cmap=cmap, aspect="auto", vmin=0, vmax=100)

    # Labels
    ax.set_xticks(range(len(slots)))
    ax.set_xticklabels(slots, rotation=45, ha="right")
    ax.set_yticks(range(len(paths)))
    ax.set_yticklabels(paths)

    # Add text annotations
    for i in range(len(paths)):
        for j in range(len(slots)):
            val = matrix[i, j]
            if not np.isnan(val):
                text_color = "white" if val < 50 else "black"
                ax.text(j, i, f"{val:.0f}%", ha="center", va="center", color=text_color, fontsize=8)

    ax.set_title(f"Path × Slot Compliance: {report.file_path}")
    plt.colorbar(im, ax=ax, label="Compliance %")
    plt.tight_layout()
    return fig


def plot_threshold_violations(
    report: ComplianceReport,
    *,
    figsize: tuple[float, float] = (8, 5),
) -> Figure:
    """Create a visualization of threshold violations.

    Shows which paths/slots fell below their minimum thresholds.

    Args:
        report: ComplianceReport to visualize
        figsize: Figure size

    Returns:
        matplotlib Figure object
    """
    _require_viz()

    violations = report.threshold_violations

    if not violations:
        fig, ax = plt.subplots(figsize=figsize)
        ax.text(
            0.5,
            0.5,
            "No threshold violations!",
            ha="center",
            va="center",
            transform=ax.transAxes,
            fontsize=16,
            color="green",
        )
        ax.set_title("Threshold Violations")
        ax.axis("off")
        return fig

    fig, ax = plt.subplots(figsize=figsize)

    # Sort by shortfall (biggest violations first)
    violations = sorted(violations, key=lambda v: v.shortfall, reverse=True)

    labels = [f"{v.path}" for v in violations]
    actuals = [v.actual_compliance for v in violations]
    required = [v.min_required for v in violations]
    shortfalls = [v.shortfall for v in violations]

    y_pos = range(len(violations))

    # Plot actual compliance (red bars)
    ax.barh(y_pos, actuals, color="salmon", edgecolor="darkred", label="Actual")

    # Plot required threshold markers
    for i, req in enumerate(required):
        ax.plot([req, req], [i - 0.4, i + 0.4], color="darkgreen", linewidth=3, label="Required" if i == 0 else "")

    # Add shortfall annotations
    for i, (actual, shortfall) in enumerate(zip(actuals, shortfalls)):
        ax.text(
            actual + 1,
            i,
            f"-{shortfall:.1f}%",
            va="center",
            fontsize=9,
            color="darkred",
            fontweight="bold",
        )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Compliance %")
    ax.set_xlim(0, 105)
    ax.set_title(f"Threshold Violations ({len(violations)})")
    ax.legend(loc="lower right")

    plt.tight_layout()
    return fig


def plot_comparison(
    reports: list[ComplianceReport],
    *,
    figsize: tuple[float, float] | None = None,
) -> Figure:
    """Create a comparison bar chart of multiple reports.

    Args:
        reports: List of ComplianceReport objects to compare
        figsize: Figure size (auto-calculated if None)

    Returns:
        matplotlib Figure object
    """
    _require_viz()
    import numpy as np

    if not reports:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, "No reports to compare", ha="center", va="center", transform=ax.transAxes)
        return fig

    # Get all unique slots across reports
    all_slots: set[str] = set()
    for report in reports:
        all_slots.update(report.summary_by_slot.keys())
    slots = sorted(all_slots)

    if figsize is None:
        figsize = (max(8, len(slots) * 1.5), 6)

    fig, ax = plt.subplots(figsize=figsize)

    # Bar positions
    x = np.arange(len(slots))
    width = 0.8 / len(reports)

    # Color palette for different reports
    colors = sns.color_palette("husl", len(reports))

    for i, report in enumerate(reports):
        values = [report.summary_by_slot.get(slot, 0) for slot in slots]
        offset = (i - len(reports) / 2 + 0.5) * width
        label = report.file_path.split("/")[-1] if "/" in report.file_path else report.file_path
        ax.bar(x + offset, values, width, label=label, color=colors[i], edgecolor="black", linewidth=0.5)

    ax.set_ylabel("Compliance %")
    ax.set_xlabel("Slot")
    ax.set_title("Compliance Comparison by Slot")
    ax.set_xticks(x)
    ax.set_xticklabels(slots, rotation=45, ha="right")
    ax.set_ylim(0, 105)
    ax.legend(loc="upper right")

    plt.tight_layout()
    return fig


def create_dashboard(
    report: ComplianceReport,
    *,
    output_path: str | None = None,
    figsize: tuple[float, float] = (14, 10),
) -> Figure:
    """Create a comprehensive dashboard with multiple panels.

    Includes:
    - Compliance gauge (top left)
    - Slot bars (top right)
    - Path heatmap (bottom left)
    - Threshold violations (bottom right)

    Args:
        report: ComplianceReport to visualize
        output_path: Optional path to save the dashboard image
        figsize: Overall figure size

    Returns:
        matplotlib Figure object
    """
    _require_viz()

    fig = plt.figure(figsize=figsize)

    # Create grid layout
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

    # Top left: Compliance gauge
    ax1 = fig.add_subplot(gs[0, 0])
    _draw_gauge_in_ax(ax1, report)

    # Top right: Slot bars
    ax2 = fig.add_subplot(gs[0, 1])
    _draw_slot_bars_in_ax(ax2, report)

    # Bottom left: Path heatmap (if we have path data)
    ax3 = fig.add_subplot(gs[1, 0])
    _draw_heatmap_in_ax(ax3, report)

    # Bottom right: Violations or summary
    ax4 = fig.add_subplot(gs[1, 1])
    _draw_violations_in_ax(ax4, report)

    # Main title
    fig.suptitle(f"QC Dashboard: {report.file_path}", fontsize=14, fontweight="bold")

    if output_path:
        fig.savefig(output_path, dpi=150, bbox_inches="tight")

    return fig


def _get_compliance_color(value: float) -> str:
    """Get color based on compliance value."""
    if value >= 95:
        return "#2ecc71"  # Green
    elif value >= 80:
        return "#f39c12"  # Orange
    elif value >= 60:
        return "#e74c3c"  # Red
    else:
        return "#c0392b"  # Dark red


def _draw_gauge_in_ax(ax, report: ComplianceReport) -> None:
    """Draw compliance gauge in an existing axes."""
    compliance = report.global_compliance
    weighted = report.weighted_compliance

    # Background bars
    ax.barh([0.3], [100], color="#e0e0e0", height=0.25, label="Global")
    ax.barh([-0.3], [100], color="#e0e0e0", height=0.25, label="Weighted")

    # Compliance bars
    ax.barh([0.3], [compliance], color=_get_compliance_color(compliance), height=0.25)
    ax.barh([-0.3], [weighted], color=_get_compliance_color(weighted), height=0.25)

    # Labels
    ax.text(compliance / 2, 0.3, f"Global: {compliance:.1f}%", ha="center", va="center", fontsize=10, fontweight="bold")
    ax.text(weighted / 2, -0.3, f"Weighted: {weighted:.1f}%", ha="center", va="center", fontsize=10, fontweight="bold")

    ax.set_xlim(0, 100)
    ax.set_ylim(-0.7, 0.7)
    ax.set_yticks([])
    ax.set_xlabel("Compliance %")
    ax.set_title("Overall Compliance")


def _draw_slot_bars_in_ax(ax, report: ComplianceReport) -> None:
    """Draw slot bars in an existing axes."""
    slots = list(report.summary_by_slot.keys())
    values = list(report.summary_by_slot.values())

    if not slots:
        ax.text(0.5, 0.5, "No slot data", ha="center", va="center", transform=ax.transAxes)
        ax.set_title("Slot Compliance")
        return

    colors = [_get_compliance_color(v) for v in values]
    bars = ax.bar(slots, values, color=colors, edgecolor="black", linewidth=0.5)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f"{val:.0f}%", ha="center", va="bottom", fontsize=8)

    ax.set_ylabel("Compliance %")
    ax.set_ylim(0, 105)
    ax.set_title("Slot Compliance")
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")


def _draw_heatmap_in_ax(ax, report: ComplianceReport) -> None:
    """Draw path heatmap in an existing axes."""
    if not report.aggregated_scores:
        ax.text(0.5, 0.5, "No path data\n(single object analyzed)", ha="center", va="center", transform=ax.transAxes)
        ax.set_title("Path × Slot Heatmap")
        ax.axis("off")
        return

    import numpy as np

    paths = sorted(set(agg.path for agg in report.aggregated_scores))
    slots = sorted(set(agg.slot_name for agg in report.aggregated_scores))

    data_map = {(agg.path, agg.slot_name): agg.percentage for agg in report.aggregated_scores}

    matrix = np.full((len(paths), len(slots)), np.nan)
    for i, path in enumerate(paths):
        for j, slot in enumerate(slots):
            if (path, slot) in data_map:
                matrix[i, j] = data_map[(path, slot)]

    cmap = sns.color_palette("RdYlGn", as_cmap=True)
    ax.imshow(matrix, cmap=cmap, aspect="auto", vmin=0, vmax=100)

    ax.set_xticks(range(len(slots)))
    ax.set_xticklabels(slots, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(paths)))
    ax.set_yticklabels(paths, fontsize=8)
    ax.set_title("Path × Slot Heatmap")


def _draw_violations_in_ax(ax, report: ComplianceReport) -> None:
    """Draw threshold violations in an existing axes."""
    violations = report.threshold_violations

    if not violations:
        # Show summary stats instead
        ax.text(
            0.5,
            0.6,
            "No Threshold Violations",
            ha="center",
            va="center",
            transform=ax.transAxes,
            fontsize=14,
            color="green",
            fontweight="bold",
        )
        ax.text(
            0.5,
            0.4,
            f"Total checks: {report.total_checks}\nPopulated: {report.total_populated}",
            ha="center",
            va="center",
            transform=ax.transAxes,
            fontsize=10,
        )
        ax.set_title("Status")
        ax.axis("off")
        return

    violations = sorted(violations, key=lambda v: v.shortfall, reverse=True)[:5]  # Top 5

    labels = [v.slot_name for v in violations]
    actuals = [v.actual_compliance for v in violations]
    shortfalls = [v.shortfall for v in violations]

    y_pos = range(len(violations))
    ax.barh(y_pos, actuals, color="salmon", edgecolor="darkred")

    for i, (actual, shortfall) in enumerate(zip(actuals, shortfalls)):
        ax.text(actual + 1, i, f"-{shortfall:.1f}%", va="center", fontsize=8, color="darkred")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel("Compliance %")
    ax.set_xlim(0, 105)
    ax.set_title(f"Threshold Violations ({len(report.threshold_violations)})")
