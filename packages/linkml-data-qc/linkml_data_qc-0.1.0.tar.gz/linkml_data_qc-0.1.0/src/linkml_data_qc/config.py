"""Configuration models for LinkML data QC compliance analysis.

Supports configurable weights and minimum thresholds for compliance scoring.
Configuration can be loaded from YAML files.

Example - Creating a basic config:

    >>> config = QCConfig()
    >>> config.default_weight
    1.0
    >>> config.default_min_compliance is None
    True

Example - Config with slot-specific settings:

    >>> config = QCConfig(
    ...     slots={
    ...         "term": SlotQCConfig(weight=2.0, min_compliance=80.0),
    ...         "description": SlotQCConfig(weight=0.5)
    ...     }
    ... )
    >>> config.get_weight("any_path", "term")
    2.0
    >>> config.get_min_compliance("any_path", "term")
    80.0
    >>> config.get_weight("any_path", "description")
    0.5

Example - Config with path-specific overrides:

    >>> config = QCConfig(
    ...     slots={"term": SlotQCConfig(weight=2.0)},
    ...     paths={"critical[].term": PathQCConfig(weight=5.0, min_compliance=95.0)}
    ... )
    >>> config.get_weight("critical[]", "term")  # path override wins
    5.0
    >>> config.get_weight("other[]", "term")  # falls back to slot config
    2.0
    >>> config.get_weight("other[]", "name")  # falls back to default
    1.0

Example YAML config file::

    default_weight: 1.0
    default_min_compliance: null

    slots:
      term:
        weight: 2.0
        min_compliance: 80.0
      description:
        weight: 0.5

    paths:
      "phenotypes[].phenotype_term.term":
        weight: 3.0
        min_compliance: 95.0

"""

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class SlotQCConfig(BaseModel):
    """Configuration for a specific slot across all paths.

    Example:
        >>> cfg = SlotQCConfig(weight=2.0, min_compliance=80.0)
        >>> cfg.weight
        2.0
        >>> cfg.min_compliance
        80.0

    Example with defaults:
        >>> cfg = SlotQCConfig()
        >>> cfg.weight
        1.0
        >>> cfg.min_compliance is None
        True
    """

    weight: float = Field(default=1.0, ge=0.0, description="Weight for scoring (higher = more important)")
    min_compliance: float | None = Field(
        default=None,
        ge=0.0,
        le=100.0,
        description="Minimum required compliance percentage (null = no minimum)",
    )


class PathQCConfig(BaseModel):
    """Configuration for a specific path pattern.

    Example:
        >>> cfg = PathQCConfig(weight=3.0, min_compliance=90.0)
        >>> cfg.weight
        3.0
    """

    weight: float = Field(default=1.0, ge=0.0, description="Weight for scoring")
    min_compliance: float | None = Field(
        default=None,
        ge=0.0,
        le=100.0,
        description="Minimum required compliance percentage",
    )


class QCConfig(BaseModel):
    """Root configuration for QC compliance analysis.

    Precedence (highest to lowest):
    1. Path-specific config (exact match on normalized path + slot)
    2. Slot-specific config
    3. Default values

    Example - Precedence demonstration:
        >>> config = QCConfig(
        ...     default_weight=1.0,
        ...     slots={"term": SlotQCConfig(weight=2.0)},
        ...     paths={"critical[].term": PathQCConfig(weight=10.0)}
        ... )
        >>> # Path-specific wins for exact match
        >>> config.get_weight("critical[]", "term")
        10.0
        >>> # Falls back to slot config
        >>> config.get_weight("other[]", "term")
        2.0
        >>> # Falls back to default
        >>> config.get_weight("other[]", "name")
        1.0

    Example - Default config:
        >>> config = QCConfig.default()
        >>> config.default_weight
        1.0
        >>> len(config.slots)
        0
    """

    default_weight: float = Field(default=1.0, ge=0.0, description="Default weight for unspecified paths/slots")
    default_min_compliance: float | None = Field(
        default=None,
        description="Default minimum compliance (null = no minimum)",
    )

    slots: dict[str, SlotQCConfig] = Field(
        default_factory=dict,
        description="Per-slot configuration (applies to all occurrences)",
    )

    paths: dict[str, PathQCConfig] = Field(
        default_factory=dict,
        description="Per-path configuration (overrides slot config)",
    )

    def get_weight(self, path: str, slot_name: str) -> float:
        """Get the weight for a specific path+slot combination.

        Args:
            path: Normalized path (e.g., 'pathophysiology[].cell_types[]')
            slot_name: Name of the slot (e.g., 'term')

        Returns:
            Weight value, checking path config first, then slot config, then default.

        Example:
            >>> config = QCConfig(slots={"email": SlotQCConfig(weight=1.5)})
            >>> config.get_weight("person", "email")
            1.5
            >>> config.get_weight("person", "name")
            1.0
        """
        # Full path includes slot name
        full_path = f"{path}.{slot_name}"

        # Check path-specific config first (highest precedence)
        if full_path in self.paths:
            return self.paths[full_path].weight

        # Check slot-specific config
        if slot_name in self.slots:
            return self.slots[slot_name].weight

        # Fall back to default
        return self.default_weight

    def get_min_compliance(self, path: str, slot_name: str) -> float | None:
        """Get the minimum compliance threshold for a specific path+slot.

        Args:
            path: Normalized path
            slot_name: Name of the slot

        Returns:
            Minimum compliance percentage, or None if no minimum set.

        Example:
            >>> config = QCConfig(slots={"term": SlotQCConfig(min_compliance=80.0)})
            >>> config.get_min_compliance("items[]", "term")
            80.0
            >>> config.get_min_compliance("items[]", "other") is None
            True
        """
        full_path = f"{path}.{slot_name}"

        # Check path-specific config first
        if full_path in self.paths:
            return self.paths[full_path].min_compliance

        # Check slot-specific config
        if slot_name in self.slots:
            return self.slots[slot_name].min_compliance

        # Fall back to default
        return self.default_min_compliance

    @classmethod
    def from_yaml(cls, path: str | Path) -> "QCConfig":
        """Load configuration from a YAML file.

        Example:
            >>> import tempfile
            >>> import os
            >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            ...     _ = f.write('default_weight: 2.0\\nslots:\\n  term:\\n    weight: 3.0\\n')
            ...     temp_path = f.name
            >>> config = QCConfig.from_yaml(temp_path)
            >>> config.default_weight
            2.0
            >>> config.slots["term"].weight
            3.0
            >>> os.unlink(temp_path)
        """
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls.model_validate(data or {})

    @classmethod
    def default(cls) -> "QCConfig":
        """Create a default configuration with no weights or thresholds.

        Example:
            >>> config = QCConfig.default()
            >>> config.default_weight
            1.0
            >>> config.default_min_compliance is None
            True
        """
        return cls()

    def to_yaml(self, path: str | Path) -> None:
        """Save configuration to a YAML file.

        Example:
            >>> import tempfile
            >>> import os
            >>> config = QCConfig(default_weight=1.5)
            >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            ...     temp_path = f.name
            >>> config.to_yaml(temp_path)
            >>> loaded = QCConfig.from_yaml(temp_path)
            >>> loaded.default_weight
            1.5
            >>> os.unlink(temp_path)
        """
        with open(path, "w") as f:
            yaml.dump(self.model_dump(exclude_none=True), f, default_flow_style=False, sort_keys=False)


class ThresholdViolation(BaseModel):
    """A compliance threshold violation.

    Example:
        >>> v = ThresholdViolation(
        ...     path="items[].term",
        ...     slot_name="term",
        ...     actual_compliance=70.0,
        ...     min_required=80.0,
        ...     shortfall=10.0
        ... )
        >>> v.shortfall
        10.0
    """

    path: str = Field(..., description="Full path including slot (e.g., 'phenotypes[].term')")
    slot_name: str
    actual_compliance: float = Field(..., ge=0.0, le=100.0)
    min_required: float = Field(..., ge=0.0, le=100.0)
    shortfall: float = Field(..., description="How far below threshold (min_required - actual)")


def check_thresholds(
    aggregated_scores: list[Any],  # list[AggregatedPathScore]
    config: QCConfig,
) -> list[ThresholdViolation]:
    """Check aggregated scores against configured thresholds.

    Args:
        aggregated_scores: List of AggregatedPathScore from analysis
        config: QC configuration with thresholds

    Returns:
        List of threshold violations (empty if all thresholds met)

    Example:
        >>> from linkml_data_qc.models import AggregatedPathScore
        >>> scores = [
        ...     AggregatedPathScore(
        ...         path="items[]", slot_name="term", parent_class="Item",
        ...         populated=7, total=10, percentage=70.0
        ...     )
        ... ]
        >>> config = QCConfig(slots={"term": SlotQCConfig(min_compliance=80.0)})
        >>> violations = check_thresholds(scores, config)
        >>> len(violations)
        1
        >>> violations[0].shortfall
        10.0
    """
    violations = []

    for agg in aggregated_scores:
        min_compliance = config.get_min_compliance(agg.path, agg.slot_name)
        if min_compliance is not None and agg.percentage < min_compliance:
            violations.append(
                ThresholdViolation(
                    path=f"{agg.path}.{agg.slot_name}",
                    slot_name=agg.slot_name,
                    actual_compliance=agg.percentage,
                    min_required=min_compliance,
                    shortfall=min_compliance - agg.percentage,
                )
            )

    return violations
