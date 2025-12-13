# CI/CD Integration Guide

This guide shows how to integrate linkml-data-qc into your CI/CD pipeline to enforce data quality standards.

## GitHub Actions

### Basic Quality Gate

Add a step to your workflow that fails if compliance drops below a threshold:

```yaml
# .github/workflows/data-quality.yml
name: Data Quality Check

on: [push, pull_request]

jobs:
  check-compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install linkml-data-qc
        run: pip install linkml-data-qc

      - name: Check data quality
        run: |
          linkml-data-qc data/ \
            -s schema.yaml \
            -t Disease \
            --min-compliance 70
```

### With Configuration File

For more control, use a configuration file to set per-slot thresholds:

```yaml
# .github/workflows/data-quality.yml
- name: Check data quality with config
  run: |
    linkml-data-qc data/ \
      -s schema.yaml \
      -t Disease \
      -c qc_config.yaml \
      --fail-on-violations
```

Where `qc_config.yaml` defines your requirements:

```yaml
# qc_config.yaml
default_weight: 1.0

slots:
  term:
    weight: 2.0
    min_compliance: 80.0
  description:
    weight: 0.5
    min_compliance: 50.0
```

### Save Reports as Artifacts

Store compliance reports for later analysis:

```yaml
- name: Generate compliance report
  run: |
    linkml-data-qc data/ \
      -s schema.yaml \
      -t Disease \
      -f json \
      -o compliance_report.json

- name: Upload compliance report
  uses: actions/upload-artifact@v4
  with:
    name: compliance-report
    path: compliance_report.json
```

### Track Compliance Over Time

Append to a JSONL log for trend analysis:

```yaml
- name: Log compliance
  run: |
    linkml-data-qc data/ \
      -s schema.yaml \
      -t Disease \
      -f json >> compliance_log.jsonl

    git config user.name "github-actions"
    git config user.email "actions@github.com"
    git add compliance_log.jsonl
    git commit -m "Update compliance log" || true
    git push
```

## GitLab CI

```yaml
# .gitlab-ci.yml
data-quality:
  stage: test
  image: python:3.11
  script:
    - pip install linkml-data-qc
    - linkml-data-qc data/ -s schema.yaml -t Disease --min-compliance 70
  artifacts:
    paths:
      - compliance_report.json
    when: always
```

## Pre-commit Hook

Use as a pre-commit hook to catch issues before they're committed:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: linkml-data-qc
        name: Check data quality
        entry: linkml-data-qc data/ -s schema.yaml -t Disease --min-compliance 70
        language: system
        pass_filenames: false
        always_run: true
```

## Exit Codes

linkml-data-qc uses standard exit codes:

| Code | Meaning |
|------|---------|
| `0` | Success - all checks passed |
| `1` | Failure - compliance below threshold or violations detected |

This makes it easy to use in any CI system that checks exit codes.

## Best Practices

### 1. Start with Low Thresholds

Begin with achievable targets and increase over time:

```bash
# Week 1: Establish baseline
linkml-data-qc data/ -s schema.yaml -t Disease --min-compliance 50

# After improvements
linkml-data-qc data/ -s schema.yaml -t Disease --min-compliance 70
```

### 2. Use Per-Slot Thresholds for Critical Fields

Some fields matter more than others:

```yaml
# qc_config.yaml
slots:
  ontology_term:
    min_compliance: 95.0  # Critical for interoperability
  description:
    min_compliance: 60.0  # Nice to have
```

### 3. Generate Multiple Formats

Produce both human-readable and machine-readable outputs:

```bash
# For developers
linkml-data-qc data/ -s schema.yaml -t Disease -f text

# For downstream tools
linkml-data-qc data/ -s schema.yaml -t Disease -f json -o report.json

# For spreadsheet analysis
linkml-data-qc data/ -s schema.yaml -t Disease -f csv -o report.csv
```

### 4. Separate Release Checks

Use stricter thresholds for releases:

```yaml
# For PRs
- name: PR quality check
  run: linkml-data-qc data/ -s schema.yaml -t Disease --min-compliance 60

# For releases
- name: Release quality check
  if: startsWith(github.ref, 'refs/tags/')
  run: linkml-data-qc data/ -s schema.yaml -t Disease --min-compliance 80
```

## Troubleshooting

### "compliance below threshold" error

Your data doesn't meet the minimum compliance requirement. Options:

1. Lower the threshold temporarily
2. Add missing recommended fields to your data
3. Investigate which specific fields are missing with `-f text` output

### "threshold violations" error

Specific slots are below their configured thresholds. Check the output for details:

```bash
linkml-data-qc data/ -s schema.yaml -t Disease -c config.yaml -f text
```

Look for the "Threshold Violations" section in the output.
