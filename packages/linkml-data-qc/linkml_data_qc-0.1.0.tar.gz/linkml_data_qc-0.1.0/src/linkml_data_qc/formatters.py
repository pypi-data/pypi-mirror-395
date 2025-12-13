"""Output formatters for compliance reports.

This module provides formatters to render ComplianceReport and MultiFileReport
objects in various output formats: JSON, CSV, and human-readable text.

Example - JSON formatting:

    >>> from linkml_data_qc import ComplianceAnalyzer
    >>> analyzer = ComplianceAnalyzer("tests/data/test_schema.yaml")
    >>> report = analyzer.analyze_file("tests/data/person_good.yaml", "Person")
    >>> json_output = JSONFormatter.format(report)
    >>> '"global_compliance": 100.0' in json_output
    True

Example - Text formatting:

    >>> text_output = TextFormatter.format(report, show_details=False)
    >>> "Global Compliance: 100.0%" in text_output
    True

Example - CSV formatting:

    >>> csv_output = CSVFormatter.format(report)
    >>> "file,path,class,slot,populated,total,percentage" in csv_output
    True

Example - Creating multi-file reports:

    >>> from linkml_data_qc import analyze_directory
    >>> reports = analyze_directory(
    ...     "tests/data/test_schema.yaml",
    ...     "tests/data",
    ...     "Person",
    ...     pattern="person_*.yaml"
    ... )
    >>> multi = create_multi_file_report(reports)
    >>> multi.files_analyzed
    2

Example - Path normalization:

    >>> _normalize_path("items[0].subitems[2].field")
    'items[].subitems[].field'
    >>> _normalize_path("simple.path")
    'simple.path'

"""

import csv
import io
from collections import defaultdict

from .models import ComplianceReport, MultiFileReport


class JSONFormatter:
    """Format reports as JSON.

    Example:
        >>> from linkml_data_qc.models import ComplianceReport
        >>> report = ComplianceReport(
        ...     file_path="test.yaml",
        ...     target_class="Test",
        ...     schema_path="schema.yaml",
        ...     global_compliance=80.0,
        ...     weighted_compliance=85.0,
        ...     total_checks=10,
        ...     total_populated=8
        ... )
        >>> output = JSONFormatter.format(report)
        >>> '"global_compliance": 80.0' in output
        True
    """

    @staticmethod
    def format(report: ComplianceReport) -> str:
        """Format a single report as JSON.

        Example:
            >>> from linkml_data_qc import ComplianceAnalyzer
            >>> analyzer = ComplianceAnalyzer("tests/data/test_schema.yaml")
            >>> report = analyzer.analyze_file("tests/data/person_good.yaml", "Person")
            >>> json_str = JSONFormatter.format(report)
            >>> '"target_class": "Person"' in json_str
            True
        """
        return report.model_dump_json(indent=2)

    @staticmethod
    def format_multi(report: MultiFileReport) -> str:
        """Format a multi-file report as JSON.

        Example:
            >>> from linkml_data_qc.models import MultiFileReport
            >>> multi = MultiFileReport(
            ...     files_analyzed=2,
            ...     reports=[],
            ...     global_compliance=90.0,
            ...     weighted_compliance=92.0
            ... )
            >>> json_str = JSONFormatter.format_multi(multi)
            >>> '"files_analyzed": 2' in json_str
            True
        """
        return report.model_dump_json(indent=2)


class CSVFormatter:
    """Format reports as CSV.

    Example:
        >>> from linkml_data_qc import ComplianceAnalyzer
        >>> analyzer = ComplianceAnalyzer("tests/data/test_schema.yaml")
        >>> report = analyzer.analyze_file("tests/data/person_good.yaml", "Person")
        >>> csv_str = CSVFormatter.format(report)
        >>> csv_str.startswith("file,path,class,slot,populated,total,percentage")
        True
    """

    @staticmethod
    def format(report: ComplianceReport) -> str:
        """Format a single report as CSV.

        Each row represents one slot compliance check at a specific path.

        Example:
            >>> from linkml_data_qc import ComplianceAnalyzer
            >>> analyzer = ComplianceAnalyzer("tests/data/test_schema.yaml")
            >>> report = analyzer.analyze_file("tests/data/person_good.yaml", "Person")
            >>> csv_str = CSVFormatter.format(report)
            >>> lines = csv_str.strip().split("\\n")
            >>> len(lines) > 1  # header + data rows
            True
        """
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["file", "path", "class", "slot", "populated", "total", "percentage"])
        for ps in report.path_scores:
            for ss in ps.slot_scores:
                writer.writerow(
                    [
                        report.file_path,
                        ps.path,
                        ps.parent_class,
                        ss.slot_name,
                        ss.populated,
                        ss.total,
                        f"{ss.percentage:.1f}",
                    ]
                )
        return output.getvalue()

    @staticmethod
    def format_multi(report: MultiFileReport) -> str:
        """Format a multi-file report as CSV."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["file", "path", "class", "slot", "populated", "total", "percentage"])
        for r in report.reports:
            for ps in r.path_scores:
                for ss in ps.slot_scores:
                    writer.writerow(
                        [
                            r.file_path,
                            ps.path,
                            ps.parent_class,
                            ss.slot_name,
                            ss.populated,
                            ss.total,
                            f"{ss.percentage:.1f}",
                        ]
                    )
        return output.getvalue()


class TextFormatter:
    """Format reports as human-readable text with tree structure.

    Example:
        >>> from linkml_data_qc import ComplianceAnalyzer
        >>> analyzer = ComplianceAnalyzer("tests/data/test_schema.yaml")
        >>> report = analyzer.analyze_file("tests/data/person_good.yaml", "Person")
        >>> text = TextFormatter.format(report, show_details=False)
        >>> "Compliance Report:" in text
        True
        >>> "Global Compliance:" in text
        True
    """

    @staticmethod
    def format(report: ComplianceReport, show_details: bool = True) -> str:
        """Format a single report as human-readable text.

        Args:
            report: The compliance report to format
            show_details: If True, include detailed per-path scores

        Example:
            >>> from linkml_data_qc import ComplianceAnalyzer
            >>> analyzer = ComplianceAnalyzer("tests/data/test_schema.yaml")
            >>> report = analyzer.analyze_file("tests/data/person_good.yaml", "Person")
            >>> text = TextFormatter.format(report, show_details=False)
            >>> "Summary by Slot:" in text
            True
        """
        lines = [
            f"Compliance Report: {report.file_path}",
            f"Target Class: {report.target_class}",
            f"Global Compliance: {report.global_compliance:.1f}% ({report.total_populated}/{report.total_checks})",
            f"Weighted Compliance: {report.weighted_compliance:.1f}%",
        ]

        if report.config_path:
            lines.append(f"Config: {report.config_path}")

        lines.extend(["", "Summary by Slot:"])
        for slot, pct in sorted(report.summary_by_slot.items()):
            lines.append(f"  {slot}: {pct:.1f}%")

        # Show threshold violations if any
        if report.threshold_violations:
            lines.extend(["", f"Threshold Violations ({len(report.threshold_violations)}):"])
            for v in report.threshold_violations:
                lines.append(
                    f"  {v.path}: {v.actual_compliance:.1f}% < {v.min_required:.1f}% "
                    f"(shortfall: {v.shortfall:.1f}%)"
                )

        # Aggregated scores by list path (the main summary view)
        if report.aggregated_scores:
            lines.extend(["", "Aggregated Scores by List Path:"])
            # Group by path for cleaner display
            current_path = None
            for agg in report.aggregated_scores:
                # Extract base path (without slot) for grouping
                base_path = agg.path
                if current_path != base_path:
                    current_path = base_path
                lines.append(
                    f"  {agg.path}.{agg.slot_name}: {agg.percentage:.1f}% "
                    f"({agg.populated}/{agg.total})"
                )

        # Detailed per-item scores (optional, can be verbose)
        if show_details:
            lines.extend(["", "Detailed Path Scores:"])
            for ps in report.path_scores:
                lines.append(f"  {ps.path} ({ps.parent_class}): {ps.overall_percentage:.1f}%")
                for ss in ps.slot_scores:
                    status = "OK" if ss.percentage == 100 else "MISSING"
                    lines.append(f"    - {ss.slot_name}: {status}")

        return "\n".join(lines)

    @staticmethod
    def format_multi(report: MultiFileReport) -> str:
        """Format a multi-file report as human-readable text.

        Example:
            >>> from linkml_data_qc.models import MultiFileReport
            >>> multi = MultiFileReport(
            ...     files_analyzed=2,
            ...     reports=[],
            ...     global_compliance=90.0,
            ...     weighted_compliance=92.0
            ... )
            >>> text = TextFormatter.format_multi(multi)
            >>> "Multi-File Compliance Report" in text
            True
            >>> "Files Analyzed: 2" in text
            True
        """
        lines = [
            "Multi-File Compliance Report",
            f"Files Analyzed: {report.files_analyzed}",
            f"Global Compliance: {report.global_compliance:.1f}%",
            f"Weighted Compliance: {report.weighted_compliance:.1f}%",
            "",
            "Summary by Slot (across all files):",
        ]
        for slot, pct in sorted(report.summary_by_slot.items()):
            lines.append(f"  {slot}: {pct:.1f}%")

        # Show threshold violations if any
        if report.threshold_violations:
            lines.extend(["", f"Threshold Violations ({len(report.threshold_violations)}):"])
            for v in report.threshold_violations[:10]:  # Show first 10
                lines.append(
                    f"  {v.path}: {v.actual_compliance:.1f}% < {v.min_required:.1f}%"
                )
            if len(report.threshold_violations) > 10:
                lines.append(f"  ... and {len(report.threshold_violations) - 10} more")

        lines.extend(["", "Summary by Path (across all files):"])
        for path, pct in sorted(report.summary_by_path.items()):
            lines.append(f"  {path}: {pct:.1f}%")

        lines.extend(["", "Per-File Compliance:"])
        for r in report.reports:
            lines.append(f"  {r.file_path}: {r.global_compliance:.1f}%")

        return "\n".join(lines)


def create_multi_file_report(reports: list[ComplianceReport]) -> MultiFileReport:
    """Aggregate multiple reports into a single MultiFileReport.

    Args:
        reports: List of ComplianceReport objects to aggregate

    Returns:
        MultiFileReport with aggregated statistics

    Example - Empty input:
        >>> multi = create_multi_file_report([])
        >>> multi.files_analyzed
        0
        >>> multi.global_compliance
        100.0

    Example - With reports:
        >>> from linkml_data_qc import analyze_directory
        >>> reports = analyze_directory(
        ...     "tests/data/test_schema.yaml",
        ...     "tests/data",
        ...     "Person",
        ...     pattern="person_*.yaml"
        ... )
        >>> multi = create_multi_file_report(reports)
        >>> multi.files_analyzed
        2
        >>> 0 <= multi.global_compliance <= 100
        True
    """
    if not reports:
        return MultiFileReport(
            files_analyzed=0,
            reports=[],
            global_compliance=100.0,
            weighted_compliance=100.0,
            summary_by_slot={},
            summary_by_path={},
            threshold_violations=[],
        )

    # Aggregate by slot
    slot_totals: dict[str, tuple[int, int]] = defaultdict(lambda: (0, 0))
    for r in reports:
        for ps in r.path_scores:
            for ss in ps.slot_scores:
                pop, tot = slot_totals[ss.slot_name]
                slot_totals[ss.slot_name] = (pop + ss.populated, tot + ss.total)

    summary_by_slot = {
        slot: (pop / tot * 100 if tot > 0 else 100.0)
        for slot, (pop, tot) in slot_totals.items()
    }

    # Aggregate by path+slot (normalized without indices)
    # Key includes slot name: "pathophysiology[].cell_types[].term"
    path_slot_totals: dict[str, tuple[int, int]] = defaultdict(lambda: (0, 0))
    for r in reports:
        for ps in r.path_scores:
            # Normalize path by removing array indices
            normalized_path = _normalize_path(ps.path)
            for ss in ps.slot_scores:
                # Include slot name in the key for unambiguous paths
                key = f"{normalized_path}.{ss.slot_name}"
                pop, tot = path_slot_totals[key]
                path_slot_totals[key] = (pop + ss.populated, tot + ss.total)

    summary_by_path = {
        path: (pop / tot * 100 if tot > 0 else 100.0)
        for path, (pop, tot) in path_slot_totals.items()
    }

    # Global compliance (unweighted)
    total_checks = sum(r.total_checks for r in reports)
    total_populated = sum(r.total_populated for r in reports)
    global_compliance = (total_populated / total_checks * 100) if total_checks > 0 else 100.0

    # Weighted compliance (aggregate from individual reports' aggregated scores)
    weighted_populated = 0.0
    weighted_total = 0.0
    for r in reports:
        for agg in r.aggregated_scores:
            weighted_populated += agg.populated * agg.weight
            weighted_total += agg.total * agg.weight
    weighted_compliance = (weighted_populated / weighted_total * 100) if weighted_total > 0 else 100.0

    # Collect all threshold violations
    all_violations = []
    for r in reports:
        all_violations.extend(r.threshold_violations)

    return MultiFileReport(
        files_analyzed=len(reports),
        reports=reports,
        global_compliance=global_compliance,
        weighted_compliance=weighted_compliance,
        summary_by_slot=summary_by_slot,
        summary_by_path=summary_by_path,
        threshold_violations=all_violations,
    )


def _normalize_path(path: str) -> str:
    """Remove array indices from path for aggregation.

    Uses jq-style [] notation for list aggregation.

    Args:
        path: Path with numeric indices like 'items[0].subitems[2]'

    Returns:
        Normalized path with [] notation like 'items[].subitems[]'

    Example:
        >>> _normalize_path("items[0].subitems[2].field")
        'items[].subitems[].field'
        >>> _normalize_path("simple.path.no.indices")
        'simple.path.no.indices'
        >>> _normalize_path("root[0]")
        'root[]'
        >>> _normalize_path("a[10].b[20].c[30]")
        'a[].b[].c[]'
    """
    import re

    return re.sub(r"\[\d+\]", "[]", path)
