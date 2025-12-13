# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LinkML Data QC is a compliance analysis tool for LinkML data files. It measures how well data populates `recommended: true` slots defined in LinkML schemas, providing hierarchical scoring, configurable weights/thresholds, and multiple output formats.

The project uses `uv` for dependency management and `just` as the command runner.

## IMPORTANT INSTRUCTIONS

- We use test driven development, write tests first before implementing a feature
- Do not 'cheat' by making mock tests (unless asked)
- If functionality does not work, keep trying, do not relax the test just to get poor code in
- Always run tests
- Use docstrings

We make heavy use of doctests, these serve as both docs and tests. `just test` will include these, or do `just doctest` just to run doctests.

In general AVOID try/except blocks, except when truly called for (e.g., interfacing with external systems). For wrapping deterministic code, these are ALMOST NEVER required - if you think you need them, it's likely a bad smell that your logic is wrong.

## Essential Commands

### Testing and Quality
- `just test` - Run all tests, type checking, and formatting checks
- `just pytest` - Run Python tests only
- `just doctest` - Run doctests only
- `just mypy` - Run type checking
- `just format` - Run ruff linting/formatting checks
- `uv run pytest tests/test_foo.py::test_bar` - Run a specific test

### Running the CLI
- `uv run linkml-data-qc --help` - Show CLI help

### Documentation
- `just _serve` - Run local documentation server with mkdocs

## Project Architecture

### Core Structure
- **src/linkml_data_qc/** - Main package
  - `analyzer.py` - ComplianceAnalyzer class, core recursive analysis logic
  - `cli.py` - CLI interface entry point
  - `config.py` - QCConfig for weights and thresholds
  - `formatters.py` - JSON, CSV, Text output formatters
  - `introspector.py` - SchemaIntrospector for LinkML schema analysis
  - `models.py` - Pydantic data models (ComplianceReport, etc.)
- **tests/** - Test suite using pytest
- **docs/** - MkDocs-managed documentation

### Key Concepts
- **Recommended slots**: LinkML slots marked with `recommended: true` are tracked
- **Path notation**: Uses jq-style `[]` for list aggregation (e.g., `pathophysiology[].cell_types[].term`)
- **Weight precedence**: Path-specific > slot-specific > default

### Technology Stack
- **Python 3.10+** with `uv` for dependency management
- **LinkML** for schema introspection (linkml-runtime)
- **Pydantic** for data models and validation
- **pytest** for testing, **mypy** for type checking, **ruff** for linting

## Development Workflow

1. Dependencies managed via `uv` - use `uv add` for new dependencies
2. All commands run through `just` or `uv run`
3. Dynamic versioning from git tags
4. Documentation auto-deployed to GitHub Pages at https://linkml.github.io/linkml-data-qc
