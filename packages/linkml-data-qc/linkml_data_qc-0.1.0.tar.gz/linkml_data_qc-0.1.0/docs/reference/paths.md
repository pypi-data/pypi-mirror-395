# Path Notation Reference

This reference describes the path notation used by linkml-data-qc for hierarchical compliance scoring.

## Overview

linkml-data-qc traverses nested data structures and reports compliance at each level using a path notation. Paths identify specific locations in your data where recommended slots are checked.

## Path Syntax

### Root Object

The root object is denoted by `(root)`:

```
(root)
```

This represents the top-level object being analyzed.

### Dot Notation

Nested objects use dot notation:

```
disease_term.term
phenotypes.phenotype_term.term
```

### Array Indices

Individual array items use bracket notation with indices:

```
has_subtypes[0]           # First subtype
has_subtypes[1]           # Second subtype
pathophysiology[0].evidence[2]  # Third evidence in first pathophysiology
```

### Aggregated Paths

When reporting aggregate compliance across all items in an array, indices are replaced with `[]`:

```
has_subtypes[]            # All subtypes
pathophysiology[]         # All pathophysiology entries
phenotypes[].phenotype_term  # All phenotype_term objects in phenotypes
```

## Path Examples

Given this nested structure:

```yaml
name: Antiphospholipid Syndrome
disease_term:
  preferred_term: antiphospholipid syndrome
  term:
    id: MONDO:8000010
    label: antiphospholipid syndrome
has_subtypes:
  - name: Primary APS
    description: occurs in the absence of any other disease
    evidence:
      - reference: PMID:16338214
        supports: SUPPORT
        snippet: "..."
  - name: Secondary APS
    description: occurs with other autoimmune diseases
pathophysiology:
  - name: Antibody Production
    description: The immune system produces antibodies...
    cell_types:
      - preferred_term: B cell
        term:
          id: CL:0000236
          label: B cell
phenotypes:
  - name: Deep Vein Thrombosis
    phenotype_term:
      preferred_term: DVT
      term:
        id: HP:0002625
```

The following paths would be generated:

| Path | Description |
|------|-------------|
| `(root)` | The Disease object itself |
| `disease_term` | The disease_term object |
| `disease_term.term` | The nested term object |
| `has_subtypes[0]` | First subtype (Primary APS) |
| `has_subtypes[1]` | Second subtype (Secondary APS) |
| `has_subtypes[0].evidence[0]` | First evidence for Primary APS |
| `has_subtypes[]` | Aggregated: all subtypes |
| `has_subtypes[].evidence[]` | Aggregated: all evidence across all subtypes |
| `pathophysiology[0]` | First pathophysiology entry |
| `pathophysiology[0].cell_types[0]` | First cell type in first pathophysiology |
| `pathophysiology[].cell_types[]` | Aggregated: all cell types across all pathophysiology |
| `pathophysiology[].cell_types[].term` | Aggregated: all term objects in cell_types |
| `phenotypes[0].phenotype_term` | First phenotype's phenotype_term |
| `phenotypes[].phenotype_term` | Aggregated: all phenotype_term objects |
| `phenotypes[].phenotype_term.term` | Aggregated: all nested term objects |

## Aggregation Rules

### How Aggregation Works

When paths contain `[]`, compliance is calculated across all matching items:

```
pathophysiology[].description: 80.0% (4/5)
```

This means:
- 5 total pathophysiology items were checked
- 4 of them have a populated `description` slot
- Overall compliance for this path+slot combination is 80%

### Nesting Depth

Aggregation can occur at multiple levels:

```
has_subtypes[].evidence[].snippet: 90.0% (9/10)
```

This aggregates across:
- All items in `has_subtypes`
- All items in each `evidence` array
- Total of 10 evidence items, 9 with populated `snippet`

## Path Resolution in Configuration

Configuration files can target specific paths or slots:

```yaml
# Target all occurrences of a slot
slots:
  description:
    weight: 2.0
    min_compliance: 80.0

# Target a specific aggregated path
paths:
  "phenotypes[].phenotype_term.term":
    weight: 3.0
    min_compliance: 95.0
```

### Precedence

1. **Exact path match** - `paths:` entries match the full aggregated path
2. **Slot name match** - `slots:` entries match any occurrence of that slot name
3. **Default** - Falls back to `default_weight` and `default_min_compliance`

## Understanding Output

### Text Format

```
Aggregated Scores by List Path:
  has_subtypes[].description: 100.0% (3/3)
  has_subtypes[].evidence[].reference: 100.0% (10/10)
  has_subtypes[].evidence[].snippet: 90.0% (9/10)
  pathophysiology[].description: 100.0% (6/6)
  pathophysiology[].cell_types[].term: 66.7% (4/6)
```

### JSON Format

```json
{
  "aggregated_scores": [
    {
      "path": "has_subtypes[]",
      "slot_name": "description",
      "parent_class": "DiseaseSubtype",
      "populated": 3,
      "total": 3,
      "percentage": 100.0,
      "weight": 1.0
    },
    {
      "path": "pathophysiology[].cell_types[].term",
      "slot_name": "term",
      "parent_class": "CellTypeAnnotation",
      "populated": 4,
      "total": 6,
      "percentage": 66.7,
      "weight": 1.0
    }
  ]
}
```

## Traversal Behavior

### Which Slots Are Traversed

linkml-data-qc traverses slots that:

1. Have `inlined: true` or `inlined_as_list: true` in the schema
2. Have a `range` that is a class (not a primitive type)

### Multivalued Slots

Multivalued slots (lists) are traversed item by item:

- Each item gets its own indexed path (`items[0]`, `items[1]`, etc.)
- Aggregated paths summarize across all items (`items[]`)

### Non-Inlined References

Slots that reference other objects but aren't inlined are treated as scalar values and checked for population but not traversed.

## Common Patterns

### Flat Lists

```yaml
synonyms:
  - term1
  - term2
```

Paths: `(root)` checks if `synonyms` is populated (list is non-empty).

### Nested Objects

```yaml
disease_term:
  term:
    id: MONDO:123
```

Paths: `(root)`, `disease_term`, `disease_term.term`

### Lists of Objects

```yaml
phenotypes:
  - name: Phenotype1
    term: {...}
  - name: Phenotype2
    term: {...}
```

Paths: `phenotypes[0]`, `phenotypes[1]`, `phenotypes[]`, `phenotypes[].term`

### Deeply Nested Lists

```yaml
has_subtypes:
  - evidence:
      - reference: PMID:123
      - reference: PMID:456
```

Paths: `has_subtypes[0].evidence[0]`, `has_subtypes[0].evidence[1]`, `has_subtypes[].evidence[]`
