"""CLI interface for linkml-data-qc."""

from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from .analyzer import ComplianceAnalyzer
from .formatters import (
    CSVFormatter,
    JSONFormatter,
    TextFormatter,
    create_multi_file_report,
)

app = typer.Typer(
    help="LinkML Data QC: Analyze data files for recommended field compliance.",
    no_args_is_help=True,
)


@app.command()
def analyze(
    data_path: Annotated[
        list[Path],
        typer.Argument(help="Data file(s) or directory to analyze"),
    ],
    schema: Annotated[
        Path,
        typer.Option("-s", "--schema", help="Path to LinkML schema YAML"),
    ],
    target_class: Annotated[
        str,
        typer.Option("-t", "--target-class", help="Target class name for validation"),
    ],
    config: Annotated[
        Optional[Path],
        typer.Option("-c", "--config", help="Path to QC configuration YAML file"),
    ] = None,
    output_format: Annotated[
        str,
        typer.Option("-f", "--format", help="Output format: json, csv, text"),
    ] = "text",
    output: Annotated[
        Optional[Path],
        typer.Option("-o", "--output", help="Output file (default: stdout)"),
    ] = None,
    min_compliance: Annotated[
        Optional[float],
        typer.Option("--min-compliance", help="Minimum global compliance percentage (exit 1 if below)"),
    ] = None,
    fail_on_violations: Annotated[
        bool,
        typer.Option("--fail-on-violations", help="Exit with error code if any threshold violations occur"),
    ] = False,
    pattern: Annotated[
        str,
        typer.Option("--pattern", help="Glob pattern for directory search"),
    ] = "*.yaml",
    dashboard: Annotated[
        Optional[Path],
        typer.Option("--dashboard", help="Generate single dashboard PNG image"),
    ] = None,
    dashboard_dir: Annotated[
        Optional[Path],
        typer.Option("--dashboard-dir", help="Generate HTML dashboard site in directory (for GitHub Pages)"),
    ] = None,
):
    """Analyze LinkML data files for recommended field compliance."""
    # Collect data files
    data_files: list[Path] = []
    for path in data_path:
        if path.is_dir():
            data_files.extend(path.glob(pattern))
        elif path.exists():
            data_files.append(path)
        else:
            typer.echo(f"Warning: {path} does not exist, skipping", err=True)

    if not data_files:
        typer.echo("No data files found", err=True)
        raise typer.Exit(1)

    # Create analyzer with optional config
    if config:
        analyzer = ComplianceAnalyzer.with_config_file(str(schema), str(config))
    else:
        analyzer = ComplianceAnalyzer(str(schema))

    # Analyze all files
    reports = [analyzer.analyze_file(str(f), target_class) for f in sorted(data_files)]

    # Format output
    if len(reports) == 1:
        if output_format == "json":
            result = JSONFormatter.format(reports[0])
        elif output_format == "csv":
            result = CSVFormatter.format(reports[0])
        elif output_format == "text":
            result = TextFormatter.format(reports[0])
        else:
            typer.echo(f"Unknown format: {output_format}", err=True)
            raise typer.Exit(1)
    else:
        multi = create_multi_file_report(reports)
        if output_format == "json":
            result = JSONFormatter.format_multi(multi)
        elif output_format == "csv":
            result = CSVFormatter.format_multi(multi)
        elif output_format == "text":
            result = TextFormatter.format_multi(multi)
        else:
            typer.echo(f"Unknown format: {output_format}", err=True)
            raise typer.Exit(1)

    # Output
    if output:
        output.write_text(result)
        typer.echo(f"Report written to {output}", err=True)
    else:
        typer.echo(result)

    # Generate dashboard if requested
    if dashboard:
        try:
            from .dashboard import VIZ_AVAILABLE, create_dashboard

            if not VIZ_AVAILABLE:
                typer.echo(
                    "Dashboard generation requires viz extras. Install with: pip install linkml-data-qc[viz]",
                    err=True,
                )
                raise typer.Exit(1)

            # Use first report for single file, or create combined view for multiple
            if len(reports) == 1:
                create_dashboard(reports[0], output_path=str(dashboard))
            else:
                # For multiple files, create dashboard for the aggregated view
                from .dashboard import plot_comparison

                fig = plot_comparison(reports)
                fig.savefig(str(dashboard), dpi=150, bbox_inches="tight")
                import matplotlib.pyplot as plt

                plt.close(fig)

            typer.echo(f"Dashboard saved to {dashboard}", err=True)
        except ImportError:
            typer.echo(
                "Dashboard generation requires viz extras. Install with: pip install linkml-data-qc[viz]",
                err=True,
            )
            raise typer.Exit(1)

    # Generate HTML dashboard directory if requested
    if dashboard_dir:
        try:
            from .html_dashboard import (
                generate_html_dashboard,
                generate_html_dashboard_multi,
            )

            if len(reports) == 1:
                output_path = generate_html_dashboard(reports[0], dashboard_dir)
            else:
                output_path = generate_html_dashboard_multi(reports, dashboard_dir)

            typer.echo(f"HTML dashboard generated at {output_path}/index.html", err=True)
        except ImportError as e:
            typer.echo(
                f"Dashboard generation requires viz extras. Install with: pip install linkml-data-qc[viz]\nError: {e}",
                err=True,
            )
            raise typer.Exit(1)

    # Check for threshold violations
    all_violations = []
    for r in reports:
        all_violations.extend(r.threshold_violations)

    if all_violations and fail_on_violations:
        typer.echo(f"\n{len(all_violations)} threshold violation(s) found:", err=True)
        for v in all_violations[:5]:
            typer.echo(f"  {v.path}: {v.actual_compliance:.1f}% < {v.min_required:.1f}%", err=True)
        if len(all_violations) > 5:
            typer.echo(f"  ... and {len(all_violations) - 5} more", err=True)
        raise typer.Exit(1)

    # Exit code based on global threshold
    if min_compliance is not None:
        total_checks = sum(r.total_checks for r in reports)
        total_populated = sum(r.total_populated for r in reports)
        avg = (total_populated / total_checks * 100) if total_checks > 0 else 100.0
        if avg < min_compliance:
            typer.echo(
                f"Compliance {avg:.1f}% is below threshold {min_compliance}%",
                err=True,
            )
            raise typer.Exit(1)


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
