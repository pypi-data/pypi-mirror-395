"""Tests for dashboard visualization module.

These tests verify the dashboard functions work correctly when
visualization dependencies are available.
"""

import pytest

from linkml_data_qc import ComplianceAnalyzer
from linkml_data_qc.models import (
    AggregatedPathScore,
    ComplianceReport,
    PathCompliance,
    SlotCompliance,
    ThresholdViolation,
)


@pytest.fixture
def sample_report() -> ComplianceReport:
    """Create a sample ComplianceReport for testing."""
    return ComplianceReport(
        file_path="test.yaml",
        target_class="TestClass",
        schema_path="schema.yaml",
        global_compliance=75.0,
        weighted_compliance=70.0,
        total_checks=20,
        total_populated=15,
        path_scores=[
            PathCompliance(
                path="items[0]",
                parent_class="Item",
                item_count=1,
                slot_scores=[
                    SlotCompliance(path="items[0]", slot_name="name", populated=1, total=1, percentage=100.0),
                    SlotCompliance(path="items[0]", slot_name="description", populated=1, total=1, percentage=100.0),
                    SlotCompliance(path="items[0]", slot_name="meaning", populated=0, total=1, percentage=0.0),
                ],
                overall_percentage=66.7,
            ),
            PathCompliance(
                path="items[1]",
                parent_class="Item",
                item_count=1,
                slot_scores=[
                    SlotCompliance(path="items[1]", slot_name="name", populated=1, total=1, percentage=100.0),
                    SlotCompliance(path="items[1]", slot_name="description", populated=0, total=1, percentage=0.0),
                    SlotCompliance(path="items[1]", slot_name="meaning", populated=1, total=1, percentage=100.0),
                ],
                overall_percentage=66.7,
            ),
        ],
        aggregated_scores=[
            AggregatedPathScore(
                path="items[]",
                slot_name="name",
                parent_class="Item",
                populated=2,
                total=2,
                percentage=100.0,
                weight=1.0,
                min_compliance=None,
            ),
            AggregatedPathScore(
                path="items[]",
                slot_name="description",
                parent_class="Item",
                populated=1,
                total=2,
                percentage=50.0,
                weight=2.0,
                min_compliance=80.0,
            ),
            AggregatedPathScore(
                path="items[]",
                slot_name="meaning",
                parent_class="Item",
                populated=1,
                total=2,
                percentage=50.0,
                weight=3.0,
                min_compliance=70.0,
            ),
        ],
        threshold_violations=[
            ThresholdViolation(
                path="items[].description",
                slot_name="description",
                actual_compliance=50.0,
                min_required=80.0,
                shortfall=30.0,
            ),
            ThresholdViolation(
                path="items[].meaning",
                slot_name="meaning",
                actual_compliance=50.0,
                min_required=70.0,
                shortfall=20.0,
            ),
        ],
        summary_by_slot={"name": 100.0, "description": 50.0, "meaning": 50.0},
        recommended_slots=["name", "description", "meaning"],
        config_path=None,
    )


@pytest.fixture
def real_report() -> ComplianceReport:
    """Create a real report from test data."""
    analyzer = ComplianceAnalyzer("tests/data/test_schema.yaml")
    return analyzer.analyze_file("tests/data/person_poor.yaml", "Person")


class TestDashboardImport:
    """Test that dashboard module handles missing dependencies gracefully."""

    def test_can_import_dashboard_module(self):
        """Dashboard module should be importable even without viz libs."""
        from linkml_data_qc import dashboard

        assert hasattr(dashboard, "plot_compliance_gauge")
        assert hasattr(dashboard, "plot_slot_bars")
        assert hasattr(dashboard, "plot_path_heatmap")
        assert hasattr(dashboard, "create_dashboard")

    def test_viz_available_check(self):
        """Should be able to check if viz libs are available."""
        from linkml_data_qc.dashboard import VIZ_AVAILABLE

        # In dev environment, viz should be available
        assert VIZ_AVAILABLE is True


class TestComplianceGauge:
    """Tests for compliance gauge visualization."""

    def test_plot_compliance_gauge_returns_figure(self, sample_report):
        """Gauge plot should return a matplotlib Figure."""
        from linkml_data_qc.dashboard import plot_compliance_gauge

        fig = plot_compliance_gauge(sample_report)

        import matplotlib.pyplot as plt

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_gauge_with_custom_title(self, sample_report):
        """Gauge should accept custom title."""
        from linkml_data_qc.dashboard import plot_compliance_gauge

        fig = plot_compliance_gauge(sample_report, title="Custom Title")

        import matplotlib.pyplot as plt

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_gauge_weighted_vs_global(self, sample_report):
        """Gauge should support both weighted and global compliance."""
        from linkml_data_qc.dashboard import plot_compliance_gauge

        fig_global = plot_compliance_gauge(sample_report, use_weighted=False)
        fig_weighted = plot_compliance_gauge(sample_report, use_weighted=True)

        import matplotlib.pyplot as plt

        assert isinstance(fig_global, plt.Figure)
        assert isinstance(fig_weighted, plt.Figure)
        plt.close(fig_global)
        plt.close(fig_weighted)


class TestSlotBars:
    """Tests for slot-level bar chart."""

    def test_plot_slot_bars_returns_figure(self, sample_report):
        """Slot bars plot should return a matplotlib Figure."""
        from linkml_data_qc.dashboard import plot_slot_bars

        fig = plot_slot_bars(sample_report)

        import matplotlib.pyplot as plt

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_slot_bars_shows_thresholds(self, sample_report):
        """Slot bars should optionally show threshold lines."""
        from linkml_data_qc.dashboard import plot_slot_bars

        fig = plot_slot_bars(sample_report, show_thresholds=True)

        import matplotlib.pyplot as plt

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_slot_bars_with_real_report(self, real_report):
        """Slot bars should work with real analysis report."""
        from linkml_data_qc.dashboard import plot_slot_bars

        fig = plot_slot_bars(real_report)

        import matplotlib.pyplot as plt

        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestPathHeatmap:
    """Tests for path-level heatmap."""

    def test_plot_path_heatmap_returns_figure(self, sample_report):
        """Path heatmap should return a matplotlib Figure."""
        from linkml_data_qc.dashboard import plot_path_heatmap

        fig = plot_path_heatmap(sample_report)

        import matplotlib.pyplot as plt

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_heatmap_empty_paths(self):
        """Heatmap should handle reports with no path scores gracefully."""
        from linkml_data_qc.dashboard import plot_path_heatmap

        empty_report = ComplianceReport(
            file_path="empty.yaml",
            target_class="Empty",
            schema_path="schema.yaml",
            global_compliance=100.0,
            weighted_compliance=100.0,
            total_checks=0,
            total_populated=0,
            path_scores=[],
            aggregated_scores=[],
            threshold_violations=[],
            summary_by_slot={},
            recommended_slots=[],
            config_path=None,
        )

        fig = plot_path_heatmap(empty_report)

        import matplotlib.pyplot as plt

        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestThresholdViolations:
    """Tests for threshold violation visualization."""

    def test_plot_violations_returns_figure(self, sample_report):
        """Violations plot should return a matplotlib Figure."""
        from linkml_data_qc.dashboard import plot_threshold_violations

        fig = plot_threshold_violations(sample_report)

        import matplotlib.pyplot as plt

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_violations_no_violations(self):
        """Should handle reports with no violations gracefully."""
        from linkml_data_qc.dashboard import plot_threshold_violations

        clean_report = ComplianceReport(
            file_path="clean.yaml",
            target_class="Clean",
            schema_path="schema.yaml",
            global_compliance=100.0,
            weighted_compliance=100.0,
            total_checks=10,
            total_populated=10,
            path_scores=[],
            aggregated_scores=[],
            threshold_violations=[],
            summary_by_slot={"name": 100.0},
            recommended_slots=["name"],
            config_path=None,
        )

        fig = plot_threshold_violations(clean_report)

        import matplotlib.pyplot as plt

        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestDashboard:
    """Tests for composite dashboard."""

    def test_create_dashboard_returns_figure(self, sample_report):
        """Dashboard should return a matplotlib Figure."""
        from linkml_data_qc.dashboard import create_dashboard

        fig = create_dashboard(sample_report)

        import matplotlib.pyplot as plt

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_dashboard_save_to_file(self, sample_report, tmp_path):
        """Dashboard should save to file when output_path provided."""
        from linkml_data_qc.dashboard import create_dashboard

        output_file = tmp_path / "dashboard.png"
        fig = create_dashboard(sample_report, output_path=str(output_file))

        assert output_file.exists()
        assert output_file.stat().st_size > 0

        import matplotlib.pyplot as plt

        plt.close(fig)

    def test_dashboard_with_real_report(self, real_report, tmp_path):
        """Dashboard should work with real analysis report."""
        from linkml_data_qc.dashboard import create_dashboard

        output_file = tmp_path / "real_dashboard.png"
        fig = create_dashboard(real_report, output_path=str(output_file))

        assert output_file.exists()

        import matplotlib.pyplot as plt

        plt.close(fig)


class TestMultipleReports:
    """Tests for comparing multiple reports."""

    def test_plot_comparison_bar(self, sample_report):
        """Should plot comparison of multiple reports."""
        from linkml_data_qc.dashboard import plot_comparison

        # Create a second report with different values
        report2 = ComplianceReport(
            file_path="test2.yaml",
            target_class="TestClass",
            schema_path="schema.yaml",
            global_compliance=90.0,
            weighted_compliance=85.0,
            total_checks=20,
            total_populated=18,
            path_scores=[],
            aggregated_scores=[],
            threshold_violations=[],
            summary_by_slot={"name": 100.0, "description": 80.0, "meaning": 90.0},
            recommended_slots=["name", "description", "meaning"],
            config_path=None,
        )

        fig = plot_comparison([sample_report, report2])

        import matplotlib.pyplot as plt

        assert isinstance(fig, plt.Figure)
        plt.close(fig)
