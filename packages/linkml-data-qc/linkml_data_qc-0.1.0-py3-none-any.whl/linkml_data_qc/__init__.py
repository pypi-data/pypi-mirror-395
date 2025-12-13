"""LinkML Data QC - Compliance analysis for recommended fields.

This module provides tools to analyze LinkML data files for compliance with
recommended field requirements. It calculates compliance percentages at various
levels of the data tree, allowing you to identify areas where recommended
ontology term bindings or other recommended fields are missing.

Example usage - analyzing a single file:

    >>> from linkml_data_qc import ComplianceAnalyzer
    >>> analyzer = ComplianceAnalyzer("tests/data/test_schema.yaml")
    >>> report = analyzer.analyze_file("tests/data/person_good.yaml", "Person")
    >>> report.global_compliance
    100.0
    >>> report.total_checks
    8
    >>> report.total_populated
    8

Analyzing a file with missing recommended fields:

    >>> report = analyzer.analyze_file("tests/data/person_poor.yaml", "Person")
    >>> report.global_compliance
    12.5
    >>> report.total_populated
    1
    >>> report.total_checks
    8

Using QCConfig for weights and thresholds:

    >>> from linkml_data_qc import QCConfig, SlotQCConfig
    >>> config = QCConfig(
    ...     default_weight=1.0,
    ...     slots={"description": SlotQCConfig(weight=2.0, min_compliance=80.0)}
    ... )
    >>> analyzer = ComplianceAnalyzer("tests/data/test_schema.yaml", config)
    >>> report = analyzer.analyze_file("tests/data/person_good.yaml", "Person")
    >>> report.weighted_compliance
    100.0

Checking threshold violations:

    >>> report = analyzer.analyze_file("tests/data/person_poor.yaml", "Person")
    >>> len(report.threshold_violations)
    1
    >>> report.threshold_violations[0].path
    'friends[].description'
    >>> report.threshold_violations[0].actual_compliance
    0.0

CLI usage::

    uv run linkml-data-qc tests/data/person_good.yaml \\
        -s tests/data/test_schema.yaml -t Person -f text

"""

try:
    from linkml_data_qc._version import __version__, __version_tuple__
except ImportError:  # pragma: no cover
    __version__ = "0.0.0"
    __version_tuple__ = (0, 0, 0)

from .analyzer import ComplianceAnalyzer, analyze_directory
from .config import PathQCConfig, QCConfig, SlotQCConfig
from .formatters import (
    CSVFormatter,
    JSONFormatter,
    TextFormatter,
    create_multi_file_report,
)
from .introspector import ClassSlotMap, SchemaIntrospector, SlotInfo
from .models import (
    AggregatedPathScore,
    ComplianceReport,
    MultiFileReport,
    PathCompliance,
    SlotCompliance,
    ThresholdViolation,
)

# Dashboard module is available but requires optional viz dependencies
# Access via: from linkml_data_qc import dashboard
# or: from linkml_data_qc.dashboard import create_dashboard
from . import dashboard

__all__ = [
    # Main analyzer
    "ComplianceAnalyzer",
    "analyze_directory",
    # Configuration
    "QCConfig",
    "SlotQCConfig",
    "PathQCConfig",
    # Schema introspection
    "SchemaIntrospector",
    "SlotInfo",
    "ClassSlotMap",
    # Data models
    "SlotCompliance",
    "PathCompliance",
    "AggregatedPathScore",
    "ThresholdViolation",
    "ComplianceReport",
    "MultiFileReport",
    # Formatters
    "JSONFormatter",
    "CSVFormatter",
    "TextFormatter",
    "create_multi_file_report",
    # Dashboard (requires optional viz dependencies)
    "dashboard",
]
