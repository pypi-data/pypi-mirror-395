"""Pydantic models for LinkML data compliance analysis results.

This module defines the data models used to represent compliance analysis
results at various levels of granularity.

Example - Creating a SlotCompliance:

    >>> sc = SlotCompliance(
    ...     path="person.address",
    ...     slot_name="city",
    ...     populated=1,
    ...     total=1,
    ...     percentage=100.0
    ... )
    >>> sc.slot_name
    'city'
    >>> sc.percentage
    100.0

Example - Creating a PathCompliance with multiple slots:

    >>> pc = PathCompliance(
    ...     path="person.address",
    ...     parent_class="Address",
    ...     item_count=1,
    ...     slot_scores=[
    ...         SlotCompliance(path="person.address", slot_name="street",
    ...                        populated=1, total=1, percentage=100.0),
    ...         SlotCompliance(path="person.address", slot_name="city",
    ...                        populated=0, total=1, percentage=0.0),
    ...     ],
    ...     overall_percentage=50.0
    ... )
    >>> pc.parent_class
    'Address'
    >>> len(pc.slot_scores)
    2

Example - Creating an AggregatedPathScore:

    >>> aps = AggregatedPathScore(
    ...     path="friends[]",
    ...     slot_name="email",
    ...     parent_class="Person",
    ...     populated=3,
    ...     total=5,
    ...     percentage=60.0,
    ...     weight=1.5,
    ...     min_compliance=80.0
    ... )
    >>> aps.percentage
    60.0
    >>> aps.weight
    1.5

Example - Creating a ThresholdViolation:

    >>> tv = ThresholdViolation(
    ...     path="friends[].email",
    ...     slot_name="email",
    ...     actual_compliance=60.0,
    ...     min_required=80.0,
    ...     shortfall=20.0
    ... )
    >>> tv.shortfall
    20.0

"""

from datetime import datetime
from pydantic import BaseModel, Field


class SlotCompliance(BaseModel):
    """Compliance measurement for a single recommended slot at a path.

    Example:
        >>> sc = SlotCompliance(
        ...     path="(root)",
        ...     slot_name="description",
        ...     populated=1,
        ...     total=1,
        ...     percentage=100.0
        ... )
        >>> sc.populated
        1
    """

    path: str = Field(..., description="Data path, e.g., 'pathophysiology.cell_types'")
    slot_name: str = Field(..., description="Name of recommended slot")
    populated: int = Field(..., ge=0, description="Count of items with slot populated")
    total: int = Field(..., ge=0, description="Total items at this path")
    percentage: float = Field(..., ge=0, le=100, description="Compliance percentage")


class PathCompliance(BaseModel):
    """Aggregated compliance for all recommended slots at a specific data path.

    Example:
        >>> pc = PathCompliance(
        ...     path="(root)",
        ...     parent_class="Person",
        ...     item_count=1,
        ...     slot_scores=[],
        ...     overall_percentage=100.0
        ... )
        >>> pc.parent_class
        'Person'
    """

    path: str = Field(..., description="Data path in the tree")
    parent_class: str = Field(..., description="LinkML class at this path")
    item_count: int = Field(..., ge=0, description="Number of items at this path")
    slot_scores: list[SlotCompliance] = Field(default_factory=list)
    overall_percentage: float = Field(..., ge=0, le=100)


class AggregatedPathScore(BaseModel):
    """Aggregated compliance across all items at a list path.

    Uses jq-style [] notation to indicate aggregation over list members.
    E.g., 'pathophysiology[].description' aggregates across all pathophysiology items.
    E.g., 'pathophysiology[].cell_types[].term' aggregates across all nested items.

    Example:
        >>> aps = AggregatedPathScore(
        ...     path="items[]",
        ...     slot_name="name",
        ...     parent_class="Item",
        ...     populated=8,
        ...     total=10,
        ...     percentage=80.0
        ... )
        >>> aps.percentage
        80.0
        >>> aps.weight  # default weight
        1.0
    """

    path: str = Field(
        ...,
        description="Aggregated path using [] notation, e.g., 'pathophysiology[].cell_types[]'",
    )
    slot_name: str = Field(..., description="Name of the recommended slot")
    parent_class: str = Field(..., description="LinkML class at this path")
    populated: int = Field(..., ge=0, description="Sum of populated across all items")
    total: int = Field(..., ge=0, description="Sum of total across all items")
    percentage: float = Field(..., ge=0, le=100, description="Compliance percentage")
    weight: float = Field(default=1.0, ge=0.0, description="Configured weight for this path+slot")
    min_compliance: float | None = Field(
        default=None,
        description="Configured minimum compliance threshold (if any)",
    )


class ThresholdViolation(BaseModel):
    """A compliance threshold violation.

    Example:
        >>> tv = ThresholdViolation(
        ...     path="items[].description",
        ...     slot_name="description",
        ...     actual_compliance=50.0,
        ...     min_required=80.0,
        ...     shortfall=30.0
        ... )
        >>> tv.actual_compliance < tv.min_required
        True
    """

    path: str = Field(..., description="Full path including slot (e.g., 'phenotypes[].term')")
    slot_name: str
    actual_compliance: float = Field(..., ge=0.0, le=100.0)
    min_required: float = Field(..., ge=0.0, le=100.0)
    shortfall: float = Field(..., description="How far below threshold (min_required - actual)")


class ComplianceReport(BaseModel):
    """Complete compliance analysis report for a data file.

    Example:
        >>> report = ComplianceReport(
        ...     file_path="data.yaml",
        ...     target_class="Person",
        ...     schema_path="schema.yaml",
        ...     global_compliance=75.0,
        ...     weighted_compliance=80.0,
        ...     total_checks=20,
        ...     total_populated=15
        ... )
        >>> report.global_compliance
        75.0
        >>> report.total_checks - report.total_populated  # missing fields
        5
    """

    file_path: str = Field(..., description="Path to analyzed data file")
    target_class: str = Field(..., description="Root LinkML class for validation")
    schema_path: str = Field(..., description="Path to LinkML schema")
    global_compliance: float = Field(..., ge=0, le=100, description="Overall compliance percentage (unweighted)")
    weighted_compliance: float = Field(
        ...,
        ge=0,
        le=100,
        description="Weighted compliance percentage (using configured weights)",
    )
    total_checks: int = Field(..., ge=0, description="Total compliance checks performed")
    total_populated: int = Field(..., ge=0, description="Total fields that were populated")
    path_scores: list[PathCompliance] = Field(
        default_factory=list,
        description="Detailed per-item scores (e.g., pathophysiology[0], pathophysiology[1])",
    )
    aggregated_scores: list[AggregatedPathScore] = Field(
        default_factory=list,
        description="Aggregated scores at list level (e.g., pathophysiology[].description)",
    )
    threshold_violations: list[ThresholdViolation] = Field(
        default_factory=list,
        description="List of paths that fell below their minimum compliance threshold",
    )
    summary_by_slot: dict[str, float] = Field(
        default_factory=dict,
        description="Slot name -> overall compliance percentage",
    )
    recommended_slots: list[str] = Field(
        default_factory=list,
        description="List of recommended slots found in schema",
    )
    config_path: str | None = Field(
        default=None,
        description="Path to QC config file used (if any)",
    )
    timestamp: datetime = Field(default_factory=datetime.now)


class MultiFileReport(BaseModel):
    """Aggregated report across multiple data files.

    Example:
        >>> mfr = MultiFileReport(
        ...     files_analyzed=3,
        ...     reports=[],
        ...     global_compliance=85.0,
        ...     weighted_compliance=87.5
        ... )
        >>> mfr.files_analyzed
        3
    """

    files_analyzed: int = Field(..., ge=0)
    reports: list[ComplianceReport] = Field(default_factory=list)
    global_compliance: float = Field(..., ge=0, le=100, description="Unweighted compliance")
    weighted_compliance: float = Field(..., ge=0, le=100, description="Weighted compliance")
    summary_by_slot: dict[str, float] = Field(
        default_factory=dict,
        description="Slot name -> overall compliance percentage across all files",
    )
    summary_by_path: dict[str, float] = Field(
        default_factory=dict,
        description="Path -> overall compliance percentage across all files",
    )
    threshold_violations: list[ThresholdViolation] = Field(
        default_factory=list,
        description="Aggregated threshold violations across all files",
    )
