"""Tests for LinkML data QC compliance analyzer."""

import json
from pathlib import Path

import pytest

from linkml_data_qc import (
    AggregatedPathScore,
    CSVFormatter,
    ComplianceAnalyzer,
    ComplianceReport,
    JSONFormatter,
    QCConfig,
    SchemaIntrospector,
    SlotQCConfig,
    TextFormatter,
    ThresholdViolation,
    analyze_directory,
    create_multi_file_report,
)

ROOT_DIR = Path(__file__).parent.parent
SCHEMA_PATH = ROOT_DIR / "tests" / "data" / "test_schema.yaml"
DATA_DIR = ROOT_DIR / "tests" / "data"


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def introspector():
    return SchemaIntrospector(str(SCHEMA_PATH))


@pytest.fixture
def analyzer():
    return ComplianceAnalyzer(str(SCHEMA_PATH))


@pytest.fixture
def good_report(analyzer):
    return analyzer.analyze_file(str(DATA_DIR / "person_good.yaml"), "Person")


@pytest.fixture
def poor_report(analyzer):
    return analyzer.analyze_file(str(DATA_DIR / "person_poor.yaml"), "Person")


# ============================================================================
# Schema Introspection Tests
# ============================================================================


def test_introspector_finds_recommended_slots(introspector):
    """Should identify all recommended slots in schema."""
    assert introspector.recommended_slots == {"description", "email", "street", "city"}


@pytest.mark.parametrize(
    "class_name,expected_recommended",
    [
        ("Person", {"description", "email"}),
        ("Address", {"street", "city"}),
    ],
)
def test_introspector_class_recommended_slots(introspector, class_name, expected_recommended):
    """Each class should have correct recommended slots."""
    info = introspector.get_class_slots(class_name)
    assert set(info.recommended_slots) == expected_recommended


@pytest.mark.parametrize(
    "class_name,expected_traversable",
    [
        ("Person", {"address", "friends"}),
        ("Address", set()),  # Address has no inlined class slots
    ],
)
def test_introspector_traversable_slots(introspector, class_name, expected_traversable):
    """Should identify slots that lead to other classes."""
    traversable = introspector.get_traversable_slots(class_name)
    slot_names = {s.name for s in traversable}
    assert slot_names == expected_traversable


@pytest.mark.parametrize(
    "name,is_class",
    [
        ("Person", True),
        ("Address", True),
        ("Container", True),
        ("string", False),
        ("integer", False),
        ("NotAClass", False),
    ],
)
def test_introspector_is_class(introspector, name, is_class):
    """Should correctly identify classes vs non-classes."""
    assert introspector.is_class(name) == is_class


# ============================================================================
# Compliance Analysis Tests
# ============================================================================


@pytest.mark.parametrize(
    "data_file,expected_compliance,expected_populated,expected_total",
    [
        ("person_good.yaml", 100.0, 8, 8),
        ("person_poor.yaml", 12.5, 1, 8),
    ],
)
def test_analyze_file_compliance(analyzer, data_file, expected_compliance, expected_populated, expected_total):
    """Should calculate correct compliance metrics for each file."""
    report = analyzer.analyze_file(str(DATA_DIR / data_file), "Person")
    assert isinstance(report, ComplianceReport)
    assert report.global_compliance == expected_compliance
    assert report.total_populated == expected_populated
    assert report.total_checks == expected_total


@pytest.mark.parametrize(
    "data_file,slot_name,expected_compliance",
    [
        ("person_good.yaml", "description", 100.0),
        ("person_good.yaml", "email", 100.0),
        ("person_good.yaml", "street", 100.0),
        ("person_good.yaml", "city", 100.0),
        ("person_poor.yaml", "description", 0.0),
        ("person_poor.yaml", "street", 0.0),
        ("person_poor.yaml", "city", 0.0),
    ],
)
def test_summary_by_slot(analyzer, data_file, slot_name, expected_compliance):
    """Summary by slot should have correct percentages."""
    report = analyzer.analyze_file(str(DATA_DIR / data_file), "Person")
    assert slot_name in report.summary_by_slot
    assert report.summary_by_slot[slot_name] == expected_compliance


def test_path_scores_structure(good_report):
    """Path scores should have valid structure."""
    assert len(good_report.path_scores) > 0
    for ps in good_report.path_scores:
        assert ps.path
        assert ps.parent_class
        assert ps.item_count >= 0
        assert 0 <= ps.overall_percentage <= 100
        for ss in ps.slot_scores:
            assert ss.slot_name
            assert ss.total >= 0
            assert ss.populated >= 0
            assert ss.populated <= ss.total
            assert 0 <= ss.percentage <= 100


def test_recommended_slots_in_report(good_report):
    """Report should list recommended slots from schema."""
    assert "description" in good_report.recommended_slots
    assert "email" in good_report.recommended_slots


# ============================================================================
# Aggregated Scores Tests
# ============================================================================


def test_aggregated_scores_exist(good_report):
    """Report should include aggregated scores for list paths."""
    assert len(good_report.aggregated_scores) > 0


def test_aggregated_scores_use_bracket_notation(good_report):
    """Aggregated paths should use [] notation without numeric indices."""
    for agg in good_report.aggregated_scores:
        assert "[]" in agg.path, f"Path {agg.path} should contain []"
        path_without_brackets = agg.path.replace("[]", "")
        assert not any(c.isdigit() for c in path_without_brackets), \
            f"Path {agg.path} should not have numeric indices"


def test_aggregated_scores_structure(good_report):
    """Aggregated scores should have valid structure."""
    for agg in good_report.aggregated_scores:
        assert isinstance(agg, AggregatedPathScore)
        assert agg.path
        assert agg.slot_name
        assert agg.parent_class
        assert agg.total >= agg.populated >= 0
        assert 0 <= agg.percentage <= 100
        assert agg.weight >= 0


# ============================================================================
# Formatter Tests
# ============================================================================


@pytest.mark.parametrize(
    "formatter,expected_content",
    [
        (JSONFormatter, ['"global_compliance"', '"path_scores"', '"summary_by_slot"']),
        (TextFormatter, ["Compliance Report", "Global Compliance", "Summary by Slot"]),
        (CSVFormatter, ["file,path,class,slot,populated,total,percentage"]),
    ],
)
def test_formatters_single_report(good_report, formatter, expected_content):
    """Each formatter should produce expected content."""
    output = formatter.format(good_report)
    for content in expected_content:
        assert content in output


def test_json_formatter_valid_json(good_report):
    """JSON formatter should produce valid JSON."""
    json_out = JSONFormatter.format(good_report)
    parsed = json.loads(json_out)
    assert parsed["global_compliance"] == 100.0
    assert "path_scores" in parsed
    assert "aggregated_scores" in parsed


def test_csv_formatter_has_data_rows(good_report):
    """CSV formatter should have header and data rows."""
    csv_out = CSVFormatter.format(good_report)
    lines = csv_out.strip().split("\n")
    assert len(lines) > 1  # header + at least one data row


# ============================================================================
# Configuration Tests
# ============================================================================


def test_default_config():
    """Default config should have weight 1.0 and no thresholds."""
    config = QCConfig.default()
    assert config.default_weight == 1.0
    assert config.default_min_compliance is None
    assert len(config.slots) == 0
    assert len(config.paths) == 0


@pytest.mark.parametrize(
    "slot_weight,path,slot_name,expected_weight",
    [
        (2.0, "any_path", "description", 2.0),
        (1.5, "other[]", "description", 1.5),
        (None, "any_path", "unknown", 1.0),  # falls back to default
    ],
)
def test_config_get_weight(slot_weight, path, slot_name, expected_weight):
    """Config should return correct weight based on precedence."""
    slots = {"description": SlotQCConfig(weight=slot_weight)} if slot_weight else {}
    config = QCConfig(default_weight=1.0, slots=slots)
    assert config.get_weight(path, slot_name) == expected_weight


@pytest.mark.parametrize(
    "min_compliance,path,slot_name,expected",
    [
        (80.0, "items[]", "description", 80.0),
        (95.0, "other[]", "description", 95.0),
        (None, "items[]", "unknown", None),  # no threshold set
    ],
)
def test_config_get_min_compliance(min_compliance, path, slot_name, expected):
    """Config should return correct min_compliance based on precedence."""
    slots = {"description": SlotQCConfig(min_compliance=min_compliance)} if min_compliance else {}
    config = QCConfig(slots=slots)
    assert config.get_min_compliance(path, slot_name) == expected


@pytest.mark.parametrize(
    "min_compliance,data_file,expect_violations",
    [
        (80.0, "person_poor.yaml", True),   # 0% < 80%, should violate
        (0.0, "person_poor.yaml", False),   # 0% >= 0%, no violation
        (80.0, "person_good.yaml", False),  # 100% >= 80%, no violation
    ],
)
def test_threshold_violations(min_compliance, data_file, expect_violations):
    """Should detect violations when compliance is below threshold."""
    config = QCConfig(
        slots={"description": SlotQCConfig(min_compliance=min_compliance)}
    )
    analyzer = ComplianceAnalyzer(str(SCHEMA_PATH), config)
    report = analyzer.analyze_file(str(DATA_DIR / data_file), "Person")

    description_violations = [
        v for v in report.threshold_violations if v.slot_name == "description"
    ]

    if expect_violations:
        assert len(description_violations) > 0
        for v in description_violations:
            assert isinstance(v, ThresholdViolation)
            assert v.actual_compliance < v.min_required
            assert v.shortfall > 0
    else:
        assert len(description_violations) == 0


def test_weighted_compliance_with_config():
    """Weighted compliance should be calculated with config weights."""
    config = QCConfig(
        slots={"description": SlotQCConfig(weight=2.0)}
    )
    analyzer = ComplianceAnalyzer(str(SCHEMA_PATH), config)
    report = analyzer.analyze_file(str(DATA_DIR / "person_good.yaml"), "Person")
    assert 0 <= report.weighted_compliance <= 100


def test_violations_in_json_output():
    """JSON output should include threshold_violations array."""
    config = QCConfig(
        slots={"description": SlotQCConfig(min_compliance=99.0)}
    )
    analyzer = ComplianceAnalyzer(str(SCHEMA_PATH), config)
    report = analyzer.analyze_file(str(DATA_DIR / "person_poor.yaml"), "Person")
    json_out = JSONFormatter.format(report)
    parsed = json.loads(json_out)

    assert "threshold_violations" in parsed
    assert "weighted_compliance" in parsed


# ============================================================================
# Directory Analysis Tests
# ============================================================================


def test_analyze_directory():
    """Should analyze all matching files in directory."""
    reports = analyze_directory(
        str(SCHEMA_PATH),
        str(DATA_DIR),
        "Person",
        pattern="person_*.yaml"
    )
    assert len(reports) == 2
    assert all(isinstance(r, ComplianceReport) for r in reports)


# ============================================================================
# Multi-File Report Tests
# ============================================================================


@pytest.fixture
def multi_report():
    reports = analyze_directory(
        str(SCHEMA_PATH),
        str(DATA_DIR),
        "Person",
        pattern="person_*.yaml"
    )
    return create_multi_file_report(reports)


def test_multi_file_report_aggregation(multi_report):
    """Should aggregate multiple reports correctly."""
    assert multi_report.files_analyzed == 2
    assert len(multi_report.reports) == 2
    assert 0 <= multi_report.global_compliance <= 100
    assert len(multi_report.summary_by_slot) > 0


def test_multi_file_report_empty_input():
    """Should handle empty input gracefully."""
    multi = create_multi_file_report([])
    assert multi.files_analyzed == 0
    assert multi.global_compliance == 100.0


@pytest.mark.parametrize(
    "formatter,expected_content",
    [
        (JSONFormatter, ['"files_analyzed"', '"global_compliance"']),
        (TextFormatter, ["Multi-File Compliance Report", "Files Analyzed"]),
    ],
)
def test_multi_file_formatters(multi_report, formatter, expected_content):
    """Multi-file formatters should produce expected content."""
    output = formatter.format_multi(multi_report)
    for content in expected_content:
        assert content in output


def test_multi_file_json_valid(multi_report):
    """Multi-file JSON should be valid and parseable."""
    json_out = JSONFormatter.format_multi(multi_report)
    parsed = json.loads(json_out)
    assert parsed["files_analyzed"] == 2
    assert "global_compliance" in parsed
    assert "summary_by_slot" in parsed


# ============================================================================
# Edge Cases and Integration Tests
# ============================================================================


@pytest.mark.parametrize(
    "value,expected",
    [
        ("hello", True),
        ("", False),
        ("   ", False),
        (None, False),
        ([], False),
        ([1, 2], True),
        ({}, False),
        ({"key": "val"}, True),
        (0, True),  # zero is populated
        (False, True),  # False is populated
    ],
)
def test_is_populated(analyzer, value, expected):
    """_is_populated should correctly identify populated values."""
    assert analyzer._is_populated(value) == expected
