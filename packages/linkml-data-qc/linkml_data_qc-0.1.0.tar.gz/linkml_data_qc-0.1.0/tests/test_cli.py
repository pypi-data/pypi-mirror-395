"""CLI tests for linkml-data-qc.

These tests verify the CLI interface works correctly, separate from core logic tests.
Uses subprocess to test actual CLI invocation.
"""

import json
import os
import subprocess
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).parent.parent
SCHEMA_PATH = ROOT_DIR / "tests" / "data" / "test_schema.yaml"
DATA_DIR = ROOT_DIR / "tests" / "data"
GOOD_FILE = DATA_DIR / "person_good.yaml"
POOR_FILE = DATA_DIR / "person_poor.yaml"


def run_cli(*args: str, expect_error: bool = False) -> subprocess.CompletedProcess:
    """Run the CLI with given arguments."""
    # Disable color output to avoid ANSI escape codes in CI environments
    env = {"NO_COLOR": "1", "TERM": "dumb"}
    result = subprocess.run(
        ["uv", "run", "linkml-data-qc", *args],
        capture_output=True,
        text=True,
        cwd=ROOT_DIR,
        env={**os.environ, **env},
    )
    if not expect_error and result.returncode != 0:
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
    return result


# ============================================================================
# Basic CLI Tests
# ============================================================================


def test_cli_help():
    """CLI should show help with --help."""
    result = run_cli("--help")
    assert result.returncode == 0
    assert "Analyze LinkML data files" in result.stdout
    assert "--schema" in result.stdout
    assert "--target-class" in result.stdout


def test_cli_missing_required_args():
    """CLI should error when required args missing."""
    result = run_cli(str(GOOD_FILE), expect_error=True)
    assert result.returncode != 0
    assert "Missing option" in result.stderr or "required" in result.stderr.lower()


# ============================================================================
# Single File Analysis Tests
# ============================================================================


@pytest.mark.parametrize(
    "data_file,expected_compliance",
    [
        ("person_good.yaml", "100.0%"),
        ("person_poor.yaml", "12.5%"),
    ],
)
def test_cli_single_file_text_output(data_file, expected_compliance):
    """CLI should produce correct text output for single file."""
    result = run_cli(
        str(DATA_DIR / data_file),
        "-s", str(SCHEMA_PATH),
        "-t", "Person",
        "-f", "text",
    )
    assert result.returncode == 0
    assert "Compliance Report:" in result.stdout
    assert expected_compliance in result.stdout


def test_cli_single_file_json_output():
    """CLI should produce valid JSON output."""
    result = run_cli(
        str(GOOD_FILE),
        "-s", str(SCHEMA_PATH),
        "-t", "Person",
        "-f", "json",
    )
    assert result.returncode == 0
    parsed = json.loads(result.stdout)
    assert parsed["global_compliance"] == 100.0
    assert parsed["target_class"] == "Person"


def test_cli_single_file_csv_output():
    """CLI should produce CSV output with header."""
    result = run_cli(
        str(GOOD_FILE),
        "-s", str(SCHEMA_PATH),
        "-t", "Person",
        "-f", "csv",
    )
    assert result.returncode == 0
    assert "file,path,class,slot,populated,total,percentage" in result.stdout
    lines = result.stdout.strip().split("\n")
    assert len(lines) > 1  # header + data


# ============================================================================
# Output Format Tests
# ============================================================================


@pytest.mark.parametrize(
    "format_arg,expected_content",
    [
        ("text", "Compliance Report:"),
        ("json", '"global_compliance"'),
        ("csv", "file,path,class,slot"),
    ],
)
def test_cli_output_formats(format_arg, expected_content):
    """CLI should support all output formats."""
    result = run_cli(
        str(GOOD_FILE),
        "-s", str(SCHEMA_PATH),
        "-t", "Person",
        "-f", format_arg,
    )
    assert result.returncode == 0
    assert expected_content in result.stdout


def test_cli_invalid_format():
    """CLI should error on invalid format."""
    result = run_cli(
        str(GOOD_FILE),
        "-s", str(SCHEMA_PATH),
        "-t", "Person",
        "-f", "invalid",
        expect_error=True,
    )
    assert result.returncode != 0
    assert "Unknown format" in result.stderr


# ============================================================================
# Directory Analysis Tests
# ============================================================================


def test_cli_directory_analysis():
    """CLI should analyze directory with pattern."""
    result = run_cli(
        str(DATA_DIR),
        "-s", str(SCHEMA_PATH),
        "-t", "Person",
        "--pattern", "person_*.yaml",
        "-f", "text",
    )
    assert result.returncode == 0
    assert "Multi-File Compliance Report" in result.stdout
    assert "Files Analyzed: 2" in result.stdout


def test_cli_directory_json():
    """CLI should produce valid JSON for multi-file analysis."""
    result = run_cli(
        str(DATA_DIR),
        "-s", str(SCHEMA_PATH),
        "-t", "Person",
        "--pattern", "person_*.yaml",
        "-f", "json",
    )
    assert result.returncode == 0
    parsed = json.loads(result.stdout)
    assert parsed["files_analyzed"] == 2
    assert "global_compliance" in parsed


# ============================================================================
# Threshold and Exit Code Tests
# ============================================================================


@pytest.mark.parametrize(
    "min_compliance,data_file,expect_fail",
    [
        (50.0, "person_good.yaml", False),   # 100% >= 50%
        (50.0, "person_poor.yaml", True),    # 12.5% < 50%
        (10.0, "person_poor.yaml", False),   # 12.5% >= 10%
    ],
)
def test_cli_min_compliance_threshold(min_compliance, data_file, expect_fail):
    """CLI should exit with code 1 when below --min-compliance."""
    result = run_cli(
        str(DATA_DIR / data_file),
        "-s", str(SCHEMA_PATH),
        "-t", "Person",
        "--min-compliance", str(min_compliance),
        expect_error=expect_fail,
    )
    if expect_fail:
        assert result.returncode == 1
        assert "below threshold" in result.stderr
    else:
        assert result.returncode == 0


def test_cli_fail_on_violations_with_config(tmp_path):
    """CLI should exit with code 1 when --fail-on-violations and violations exist."""
    # Create a config with strict threshold
    config_file = tmp_path / "config.yaml"
    config_file.write_text("""
default_weight: 1.0
slots:
  description:
    min_compliance: 80.0
""")

    result = run_cli(
        str(POOR_FILE),
        "-s", str(SCHEMA_PATH),
        "-t", "Person",
        "-c", str(config_file),
        "--fail-on-violations",
        expect_error=True,
    )
    assert result.returncode == 1
    assert "violation" in result.stderr.lower()


def test_cli_no_fail_when_above_threshold(tmp_path):
    """CLI should exit 0 when compliance meets threshold."""
    config_file = tmp_path / "config.yaml"
    config_file.write_text("""
default_weight: 1.0
slots:
  description:
    min_compliance: 50.0
""")

    result = run_cli(
        str(GOOD_FILE),
        "-s", str(SCHEMA_PATH),
        "-t", "Person",
        "-c", str(config_file),
        "--fail-on-violations",
    )
    assert result.returncode == 0


# ============================================================================
# Output File Tests
# ============================================================================


def test_cli_output_to_file(tmp_path):
    """CLI should write output to file with -o."""
    output_file = tmp_path / "report.json"
    result = run_cli(
        str(GOOD_FILE),
        "-s", str(SCHEMA_PATH),
        "-t", "Person",
        "-f", "json",
        "-o", str(output_file),
    )
    assert result.returncode == 0
    assert output_file.exists()
    parsed = json.loads(output_file.read_text())
    assert parsed["global_compliance"] == 100.0


# ============================================================================
# Error Handling Tests
# ============================================================================


def test_cli_nonexistent_file():
    """CLI should handle nonexistent file gracefully."""
    result = run_cli(
        "/nonexistent/path/data.yaml",
        "-s", str(SCHEMA_PATH),
        "-t", "Person",
        expect_error=True,
    )
    assert result.returncode != 0


def test_cli_nonexistent_schema():
    """CLI should error on nonexistent schema."""
    result = run_cli(
        str(GOOD_FILE),
        "-s", "/nonexistent/schema.yaml",
        "-t", "Person",
        expect_error=True,
    )
    assert result.returncode != 0


# ============================================================================
# Multiple File Arguments Tests
# ============================================================================


def test_cli_multiple_files():
    """CLI should accept multiple file arguments."""
    result = run_cli(
        str(GOOD_FILE),
        str(POOR_FILE),
        "-s", str(SCHEMA_PATH),
        "-t", "Person",
        "-f", "text",
    )
    assert result.returncode == 0
    assert "Multi-File Compliance Report" in result.stdout
    assert "Files Analyzed: 2" in result.stdout


# ============================================================================
# Dashboard Tests
# ============================================================================


def test_cli_dashboard_single_file(tmp_path):
    """CLI should generate dashboard image for single file."""
    dashboard_file = tmp_path / "dashboard.png"
    result = run_cli(
        str(GOOD_FILE),
        "-s", str(SCHEMA_PATH),
        "-t", "Person",
        "--dashboard", str(dashboard_file),
    )
    assert result.returncode == 0
    assert dashboard_file.exists()
    assert dashboard_file.stat().st_size > 0
    assert "Dashboard saved to" in result.stderr


def test_cli_dashboard_multiple_files(tmp_path):
    """CLI should generate comparison dashboard for multiple files."""
    dashboard_file = tmp_path / "comparison.png"
    result = run_cli(
        str(GOOD_FILE),
        str(POOR_FILE),
        "-s", str(SCHEMA_PATH),
        "-t", "Person",
        "--dashboard", str(dashboard_file),
    )
    assert result.returncode == 0
    assert dashboard_file.exists()
    assert dashboard_file.stat().st_size > 0


# ============================================================================
# HTML Dashboard Directory Tests
# ============================================================================


def test_cli_dashboard_dir_single_file(tmp_path):
    """CLI should generate HTML dashboard directory for single file."""
    dashboard_dir = tmp_path / "qc_site"
    result = run_cli(
        str(POOR_FILE),
        "-s", str(SCHEMA_PATH),
        "-t", "Person",
        "--dashboard-dir", str(dashboard_dir),
    )
    assert result.returncode == 0
    assert (dashboard_dir / "index.html").exists()
    assert (dashboard_dir / "gauge.png").exists()
    assert (dashboard_dir / "slot_bars.png").exists()
    assert (dashboard_dir / "report.json").exists()
    assert "HTML dashboard generated" in result.stderr


def test_cli_dashboard_dir_multiple_files(tmp_path):
    """CLI should generate comparison HTML dashboard for multiple files."""
    dashboard_dir = tmp_path / "qc_multi"
    result = run_cli(
        str(GOOD_FILE),
        str(POOR_FILE),
        "-s", str(SCHEMA_PATH),
        "-t", "Person",
        "--dashboard-dir", str(dashboard_dir),
    )
    assert result.returncode == 0
    assert (dashboard_dir / "index.html").exists()
    assert (dashboard_dir / "comparison.png").exists()
    # Check HTML contains expected content
    html_content = (dashboard_dir / "index.html").read_text()
    assert "Multi-File Comparison" in html_content
    assert "person_good.yaml" in html_content
    assert "person_poor.yaml" in html_content


def test_cli_dashboard_dir_with_config(tmp_path):
    """CLI should include config info in HTML dashboard."""
    config_file = tmp_path / "config.yaml"
    config_file.write_text("""
default_weight: 1.0
slots:
  description:
    weight: 2.0
    min_compliance: 80.0
""")
    dashboard_dir = tmp_path / "qc_configured"
    result = run_cli(
        str(POOR_FILE),
        "-s", str(SCHEMA_PATH),
        "-t", "Person",
        "-c", str(config_file),
        "--dashboard-dir", str(dashboard_dir),
    )
    assert result.returncode == 0
    assert (dashboard_dir / "index.html").exists()
    # Should have violations chart since we set min_compliance
    html_content = (dashboard_dir / "index.html").read_text()
    assert "Threshold Violations" in html_content
