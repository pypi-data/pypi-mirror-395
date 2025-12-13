# Configuration Guide

This guide covers how to configure linkml-data-qc with weights and thresholds.

## Configuration File Format

Create a YAML configuration file to customize analysis behavior:

```yaml
# qc_config.yaml

# Default weight applied to all slots (default: 1.0)
default_weight: 1.0

# Default minimum compliance threshold (default: null = no threshold)
default_min_compliance: null

# Per-slot configuration
slots:
  term:
    weight: 2.0           # This slot is twice as important
    min_compliance: 80.0  # Must be at least 80% populated

  description:
    weight: 0.5           # Less important
    min_compliance: null  # No minimum required

  evidence:
    weight: 1.5
    min_compliance: 70.0

# Path-specific overrides (highest precedence)
paths:
  "phenotypes[].phenotype_term.term":
    weight: 3.0
    min_compliance: 95.0
```

## Using Configuration Files

Pass the configuration file with the `-c` option:

```bash
linkml-data-qc data/ -s schema.yaml -t Disease -c qc_config.yaml
```

## Configuration Precedence

When determining weight or threshold for a slot, linkml-data-qc uses this precedence order:

1. **Path-specific config** (highest priority) - Exact path match
2. **Slot-specific config** - Applies to all occurrences of a slot
3. **Default values** - Fallback when no specific config

### Example

Given this config:

```yaml
default_weight: 1.0

slots:
  term:
    weight: 2.0

paths:
  "phenotypes[].phenotype_term.term":
    weight: 3.0
```

The weights would be:

| Path | Slot | Weight | Reason |
|------|------|--------|--------|
| `(root)` | `description` | 1.0 | Default |
| `(root)` | `term` | 2.0 | Slot config |
| `pathophysiology[]` | `term` | 2.0 | Slot config |
| `phenotypes[].phenotype_term` | `term` | 3.0 | Path config |

## Weight Configuration

### What Weights Do

Weights affect the **weighted compliance** score. Higher-weighted slots contribute more to the final score.

### Weighted Compliance Formula

```
weighted_compliance = Σ(populated × weight) / Σ(total × weight) × 100
```

### Example

With these results:

| Slot | Populated | Total | Weight |
|------|-----------|-------|--------|
| term | 8 | 10 | 2.0 |
| description | 5 | 10 | 0.5 |

**Unweighted compliance:**
```
(8 + 5) / (10 + 10) = 13/20 = 65%
```

**Weighted compliance:**
```
(8×2.0 + 5×0.5) / (10×2.0 + 10×0.5)
= (16 + 2.5) / (20 + 5)
= 18.5/25
= 74%
```

The higher weight on `term` (which has better compliance) pulls up the weighted score.

## Threshold Configuration

### What Thresholds Do

Thresholds define minimum acceptable compliance levels. When `--fail-on-violations` is used, any slot below its threshold causes exit code 1.

### Setting Thresholds

```yaml
slots:
  term:
    min_compliance: 80.0  # At least 80% of term slots must be populated
```

### Checking for Violations

```bash
linkml-data-qc data/ -s schema.yaml -t Disease \
    -c config.yaml \
    --fail-on-violations
```

If any configured threshold is violated, the command exits with code 1.

### Violation Output

When violations occur, they're reported in the output:

```
Threshold Violations (2):
  pathophysiology[].term: 60.0% < 80.0% (shortfall: 20.0%)
  phenotypes[].description: 45.0% < 50.0% (shortfall: 5.0%)
```

## Common Configuration Patterns

### Strict Ontology Terms

Ontology term bindings are critical for interoperability:

```yaml
slots:
  term:
    weight: 3.0
    min_compliance: 90.0
  ontology_id:
    weight: 3.0
    min_compliance: 90.0
```

### Relaxed Descriptions

Free-text descriptions are nice but not critical:

```yaml
slots:
  description:
    weight: 0.5
    min_compliance: null  # No minimum
  notes:
    weight: 0.3
    min_compliance: null
```

### Critical Nested Fields

Some nested paths are more important than others:

```yaml
paths:
  "phenotypes[].phenotype_term.term":
    weight: 3.0
    min_compliance: 95.0
  "phenotypes[].phenotype_term.description":
    weight: 0.5
    min_compliance: null
```

### Release vs Development

Maintain separate configs for different contexts:

```yaml
# dev_config.yaml - relaxed for development
default_min_compliance: null
slots:
  term:
    min_compliance: 50.0

# release_config.yaml - strict for releases
default_min_compliance: 60.0
slots:
  term:
    min_compliance: 90.0
```

```bash
# During development
linkml-data-qc data/ -s schema.yaml -t Disease -c dev_config.yaml

# For releases
linkml-data-qc data/ -s schema.yaml -t Disease -c release_config.yaml --fail-on-violations
```

## Path Notation

Paths use dot notation with array brackets:

| Pattern | Meaning |
|---------|---------|
| `(root)` | The root object |
| `pathophysiology[]` | All items in pathophysiology list |
| `phenotypes[].phenotype_term` | All phenotype_term objects in phenotypes |
| `phenotypes[].phenotype_term.term` | The term slot in nested objects |

Path configs must match the aggregated path format (using `[]` not numeric indices).

## Validation

linkml-data-qc validates your configuration file on load. Invalid YAML or unknown keys will cause an error.
