# CLI Reference

Complete reference for the `linkml-data-qc` command-line interface.

## Synopsis

```bash
linkml-data-qc [OPTIONS] DATA_PATH...
```

## Description

Analyzes LinkML data files for compliance with recommended field requirements. Calculates what percentage of `recommended: true` slots are populated across your data.

## Arguments

| Argument | Description |
|----------|-------------|
| `DATA_PATH...` | One or more data files or directories to analyze. Required. |

## Options

### Required Options

| Option | Description |
|--------|-------------|
| `-s, --schema PATH` | Path to the LinkML schema YAML file. |
| `-t, --target-class TEXT` | Name of the target class to validate against. |

### Output Options

| Option | Default | Description |
|--------|---------|-------------|
| `-f, --format TEXT` | `text` | Output format: `json`, `csv`, or `text`. |
| `-o, --output PATH` | stdout | Write output to file instead of stdout. |
| `--dashboard PATH` | - | Generate single dashboard PNG image. Requires viz extras. |
| `--dashboard-dir PATH` | - | Generate HTML dashboard site in directory (for GitHub Pages). |

### Configuration Options

| Option | Description |
|--------|-------------|
| `-c, --config PATH` | Path to QC configuration YAML file for weights and thresholds. |
| `--pattern TEXT` | Glob pattern for directory search. Default: `*.yaml`. |

### Threshold Options

| Option | Description |
|--------|-------------|
| `--min-compliance FLOAT` | Minimum global compliance percentage. Exit with code 1 if below. |
| `--fail-on-violations` | Exit with code 1 if any configured threshold violations occur. |

### Other Options

| Option | Description |
|--------|-------------|
| `--help` | Show help message and exit. |

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success - all checks passed |
| `1` | Failure - compliance below threshold or violations detected |

## Examples

### Basic Analysis

Analyze a single file with text output:

```bash
linkml-data-qc data/Asthma.yaml -s schema.yaml -t Disease
```

### JSON Output

Get machine-readable JSON:

```bash
linkml-data-qc data/Asthma.yaml -s schema.yaml -t Disease -f json
```

### Analyze Directory

Analyze all YAML files in a directory:

```bash
linkml-data-qc data/ -s schema.yaml -t Disease --pattern "*.yaml"
```

### Multiple Files

Analyze specific files:

```bash
linkml-data-qc data/Asthma.yaml data/COPD.yaml -s schema.yaml -t Disease
```

### CI/CD Integration

Fail if global compliance drops below 70%:

```bash
linkml-data-qc data/ -s schema.yaml -t Disease --min-compliance 70
```

Fail if any configured threshold is violated:

```bash
linkml-data-qc data/ -s schema.yaml -t Disease \
    -c qc_config.yaml --fail-on-violations
```

### Save Output to File

Write JSON report to file:

```bash
linkml-data-qc data/ -s schema.yaml -t Disease \
    -f json -o compliance_report.json
```

### Generate Visual Dashboard

Create a dashboard image (requires `pip install linkml-data-qc[viz]`):

```bash
linkml-data-qc data/Asthma.yaml -s schema.yaml -t Disease \
    --dashboard qc_dashboard.png
```

Generate both report and dashboard:

```bash
linkml-data-qc data/ -s schema.yaml -t Disease \
    -f json -o report.json --dashboard dashboard.png
```

### Generate HTML Dashboard Site

Create a full HTML dashboard with multiple charts (for GitHub Pages):

```bash
linkml-data-qc data/Asthma.yaml -s schema.yaml -t Disease \
    --dashboard-dir ./qc_dashboard/
```

This generates:
- `index.html` - Main dashboard page
- `gauge.png` - Compliance gauge chart
- `slot_bars.png` - Slot compliance bar chart
- `path_heatmap.png` - Path × Slot heatmap
- `report.json` - Raw report data

Deploy to GitHub Pages:

```bash
# In your CI/CD pipeline
linkml-data-qc data/ -s schema.yaml -t Disease \
    -c qc_config.yaml \
    --dashboard-dir ./gh-pages/qc/

# Then push gh-pages/ to your GitHub Pages branch
```

### CSV for Spreadsheet Analysis

Export detailed results as CSV:

```bash
linkml-data-qc data/ -s schema.yaml -t Disease -f csv -o results.csv
```

## Configuration File Format

The optional configuration file allows you to set weights and minimum thresholds:

```yaml
# qc_config.yaml
default_weight: 1.0
default_min_compliance: null

# Per-slot configuration
slots:
  term:
    weight: 2.0           # Terms are twice as important
    min_compliance: 80.0  # Require at least 80%
  description:
    weight: 0.5           # Descriptions are nice-to-have
  evidence:
    weight: 1.5

# Per-path overrides (highest precedence)
paths:
  "phenotypes[].phenotype_term.term":
    weight: 3.0
    min_compliance: 95.0
```

### Configuration Precedence

1. **Path-specific config** - Highest priority, exact path match
2. **Slot-specific config** - Applies to all occurrences of a slot
3. **Default values** - Fallback when no specific config

## Output Formats

### Text Format (default)

Human-readable hierarchical output:

```
Compliance Report: data/Asthma.yaml
Target Class: Disease
Global Compliance: 65.3% (125/191)
Weighted Compliance: 71.2%

Summary by Slot:
  description: 78.4%
  term: 72.1%

Aggregated Scores by List Path:
  pathophysiology[].description: 100.0% (5/5)
  pathophysiology[].term: 80.0% (4/5)
```

### JSON Format

Complete structured output for programmatic use:

```json
{
  "file_path": "data/Asthma.yaml",
  "target_class": "Disease",
  "global_compliance": 65.3,
  "weighted_compliance": 71.2,
  "total_checks": 191,
  "total_populated": 125,
  "summary_by_slot": {"description": 78.4, "term": 72.1},
  "aggregated_scores": [...],
  "threshold_violations": [...]
}
```

### CSV Format

Flat format for spreadsheet analysis:

```csv
file,path,class,slot,populated,total,percentage
data/Asthma.yaml,(root),Disease,description,1,1,100.0
data/Asthma.yaml,pathophysiology[0],Pathophysiology,description,1,1,100.0
```

## See Also

- [Getting Started Tutorial](notebooks/01_getting_started.ipynb)
- [CI/CD Integration Guide](how-to/ci-integration.md)
- [Configuration Guide](how-to/configuration.md)
