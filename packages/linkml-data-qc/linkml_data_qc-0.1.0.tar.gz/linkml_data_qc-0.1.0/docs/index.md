# linkml-data-qc

A compliance analysis tool for LinkML data files. Measures how well your data populates `recommended: true` slots defined in LinkML schemas.

## Why linkml-data-qc?

When building knowledge bases with LinkML, certain fields may be marked as `recommended` in your schema - fields that should ideally be populated but aren't strictly required. This tool helps you:

- **Track data quality** across your knowledge base
- **Identify gaps** where recommended fields are missing
- **Enforce standards** with configurable thresholds in CI/CD
- **Prioritize curation** by finding low-compliance areas

## Quick Start

```bash
# Install
pip install linkml-data-qc

# Analyze a single file
linkml-data-qc data.yaml -s schema.yaml -t TargetClass

# Analyze a directory
linkml-data-qc data/ -s schema.yaml -t TargetClass --pattern "*.yaml"

# Fail CI if compliance drops below 70%
linkml-data-qc data/ -s schema.yaml -t TargetClass --min-compliance 70
```

## Features

- **Hierarchical scoring** - Compliance at global, path, and per-item levels
- **Aggregated list scoring** - Roll up scores using jq-style `[]` notation
- **Configurable weights** - Prioritize important fields
- **Threshold enforcement** - Set minimum compliance requirements
- **Multiple formats** - JSON, CSV, and human-readable text output
- **Visual dashboards** - Generate PNG dashboard images (optional viz extras)
- **CI/CD integration** - Exit codes for automated pipelines

## Visual Dashboard

Generate visual QC dashboards to quickly assess data quality:

```bash
pip install linkml-data-qc[viz]
linkml-data-qc data.yaml -s schema.yaml -t MyClass --dashboard qc_dashboard.png
```

![Example Dashboard](assets/dashboards/dashboard_example.png)

## Documentation

- **[Tutorials](notebooks/01_getting_started.ipynb)** - Step-by-step guides to get you started
- **[How-To Guides](how-to/ci-integration.md)** - Practical recipes for common tasks
- **[Reference](cli-reference.md)** - Complete CLI and API documentation
- **[Explanation](philosophy.md)** - Background concepts and design decisions

## Example Output

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
  phenotypes[].phenotype_term.term: 60.0% (3/5)
```
