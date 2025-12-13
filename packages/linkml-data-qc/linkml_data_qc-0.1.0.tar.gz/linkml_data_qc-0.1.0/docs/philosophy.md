# The Gap Between Valid Data and Quality Data

This document explores the conceptual foundations of data quality assessment and explains
why measuring completeness requires fundamentally different approaches than binary validation.

## The Limits of Binary Validation

Most data validation systems operate on a pass/fail model. A record either conforms to a schema
or it doesn't. An email field contains a valid email address, or it's rejected. A date falls
within an acceptable range, or it fails validation. This binary approach is computationally
tractable and provides clear, actionable signals: fix this error, then proceed.

But binary validation answers only one question: *"Is this data structurally acceptable?"*

It cannot answer the questions that matter most for real-world use:

- Is this data *useful* for its intended purpose?
- Does this dataset contain *enough* information to support analysis?
- Are we making *progress* toward a well-curated knowledge base?
- Which areas of our data need the *most* attention?

These questions require measurement on a continuum, not binary classification.

## Data Quality as a Multidimensional Concept

The foundational work by [Wang and Strong (1996)](http://web.mit.edu/tdqm/www/tdqmpub/beyondaccuracy_files/beyondaccuracy.html)
established that data quality is fundamentally about **"fitness for use"**—a definition that
emphasizes the consumer's perspective rather than abstract correctness. Their research identified
15 dimensions of data quality organized into four categories:

| Category | Dimensions | Focus |
|----------|------------|-------|
| **Intrinsic** | Accuracy, Believability, Objectivity, Reputation | Quality inherent to the data itself |
| **Contextual** | Completeness, Relevancy, Timeliness, Value-added, Appropriate amount | Quality relative to the task at hand |
| **Representational** | Interpretability, Ease of understanding, Conciseness, Consistency | How data is presented and formatted |
| **Accessibility** | Access, Security | How easily data can be obtained |

Notice that *validity*—the concern of schema validators—maps primarily to the Intrinsic
category. But *completeness* is a Contextual dimension: whether data is complete depends
entirely on what you're trying to do with it.

## Completeness: The Missing Middle Ground

Completeness is particularly interesting because it occupies the gap between validation
and curation:

**Validation asks:** "Does this field contain a valid value?"
**Completeness asks:** "Is this field populated at all?"
**Curation asks:** "Is this field populated with the *right* information?"

A customer record with an email field containing `test@example.com` passes validation
(it's a syntactically valid email) but may fail completeness expectations in different ways:

- It might be a placeholder that needs replacement
- The field might be present but contextually irrelevant
- The surrounding record might lack other important fields

This is why [data quality frameworks](https://icedq.com/6-data-quality-dimensions)
distinguish between:

- **Required fields** — Must be present; absence is a validation error
- **Optional fields** — May be absent without affecting validity
- **Recommended fields** — *Should* be present for quality data, but absence isn't fatal

The third category is crucial. Recommended fields encode institutional knowledge about
what makes data *useful*, not just *acceptable*. They represent the difference between
a minimal skeleton that passes validation and a rich record that serves its purpose well.

## Why Binary Approaches Fail for Completeness

Consider a biomedical knowledge base with 10,000 disease entries. A binary completeness
check might report:

```
❌ 3,247 entries missing description field
❌ 1,892 entries missing ontology term binding
✓ All entries have required name field
```

This tells you something, but not enough:

- Are the missing descriptions concentrated in rare diseases (where information is scarce)?
- Is the 80% completion rate for ontology terms good or bad for your use case?
- Which specific areas should curators prioritize?
- Are things getting better or worse over time?

What you need is a *measurement* approach that produces continuous scores, supports
aggregation at multiple levels, and enables tracking over time. This is precisely what
distinguishes quality *assessment* from validation.

## The Measurement Problem

[Data quality monitoring](https://www.anomalo.com/blog/continuous-monitoring-for-data-quality-solutions-for-reliable-data/)
in production systems typically involves setting thresholds:

- Alert if completeness drops below 90%
- Fail the pipeline if null rates exceed 5%
- Block deployment if any critical field falls below threshold

But threshold-setting is itself a nuanced problem:

1. **Different fields have different importance.** A missing description is less critical
   than a missing identifier. Simple percentage calculations treat all fields equally.

2. **Context matters.** 70% completeness might be excellent for a newly created dataset
   but unacceptable for a mature knowledge base.

3. **Aggregation level matters.** Global completeness masks local problems. A dataset
   might be 95% complete overall while specific categories hover at 40%.

4. **Thresholds need calibration.** Initial thresholds often prove too strict or too
   lenient once real data flows through the system.

This suggests that completeness measurement should be:

- **Weighted** — More important fields contribute more to the score
- **Hierarchical** — Scores at global, category, and item levels
- **Configurable** — Thresholds and weights adjustable per context
- **Transparent** — Individual contributions visible for debugging

## From Measurement to Quality Gates

The [FAIR Data Maturity Model](https://datascience.codata.org/articles/10.5334/dsj-2020-041)
provides a useful analogy. Rather than asking "Is this data FAIR?" (binary), it asks
"How FAIR is this data?" (continuous) across multiple indicators, each scored on a
maturity scale.

Similarly, completeness assessment works best as a [quality gate](https://www.infoq.com/articles/pipeline-quality-gates/)
that enforces minimum standards while providing visibility into the full picture:

```
┌─────────────────────────────────────────────────────────┐
│ Hard Validation          │ Completeness Assessment     │
│ (Binary: Pass/Fail)      │ (Continuous: 0-100%)        │
├──────────────────────────┼─────────────────────────────┤
│ Required fields present? │ What % of recommended       │
│ Types correct?           │ fields are populated?       │
│ Values in range?         │ Which areas need work?      │
│ References resolve?      │ Are we improving over time? │
└──────────────────────────┴─────────────────────────────┘
```

The left side blocks bad data from entering the system. The right side measures
how *good* the data that passes validation actually is.

## Field Classification in Practice

Effective completeness tracking requires thoughtful field classification:

| Classification | Validation Behavior | Completeness Behavior |
|---------------|--------------------|-----------------------|
| **Required** | Reject if missing | Not tracked (always 100%) |
| **Recommended** | Accept if missing | Tracked and scored |
| **Optional** | Accept if missing | Not tracked |
| **Conditional** | Depends on context | May be tracked based on context |

The key insight is that "recommended" fields encode domain expertise about data quality.
A disease entry *can* exist with just a name, but a *useful* disease entry includes
descriptions, ontology term bindings, and evidence citations. Schema designers capture
this knowledge by marking fields as recommended.

## Weighted Scoring

Not all recommended fields matter equally. [Industry practice](https://www.collibra.com/blog/the-6-dimensions-of-data-quality)
suggests weighting fields by business impact:

```
weighted_compliance = Σ(populated_count × weight) / Σ(total_count × weight) × 100
```

This allows fine-grained prioritization:

- Ontology term bindings might be critical for interoperability (weight: 2.0)
- Free-text descriptions are nice to have (weight: 0.5)
- Machine-readable synonyms are highly valued (weight: 1.5)

Weights reflect organizational priorities and use-case requirements, making completeness
measurement contextual—exactly as Wang and Strong's framework suggests it should be.

## Hierarchical Analysis

Aggregate scores hide important details. A dataset at 85% global completeness might have:

- 100% completeness for well-curated categories
- 40% completeness for newly added categories
- A handful of items with 0% completeness dragging down averages

Hierarchical scoring reveals these patterns:

```
Global Compliance: 85.0%
├── Category A: 100.0%
├── Category B: 95.0%
├── Category C: 42.0%    ← Problem area
│   ├── Item C.1: 80.0%
│   ├── Item C.2: 25.0%  ← Worst offender
│   └── Item C.3: 20.0%
└── Category D: 88.0%
```

This transforms completeness from a single number into actionable intelligence:
*these specific items need attention*.

## The Role of Thresholds

Thresholds convert continuous measurements back into actionable signals. Rather than
asking "what's our completeness percentage?" (interesting but not actionable), thresholds
answer "is our completeness *acceptable*?" (actionable).

Effective threshold design recognizes:

- **Path-specific thresholds**: Critical paths (e.g., `diseases[].ontology_term`)
  might require 90% while others accept 60%
- **Violation reporting**: When thresholds are breached, report the gap so teams
  know how much work is needed
- **Progressive tightening**: Start with achievable thresholds, then raise them as
  data quality improves

## Entropy and Data Quality Degradation

Information theory offers another lens on completeness. [Shannon entropy](http://www.infonomics.ltd.uk/blog/2014/05/08/how-information-entropy-teaches-us-to-improve-data-quality/)
measures the information content of a message. A fully-populated record with rich
metadata has high information content; a sparse record with only required fields has low
information content.

More practically, data quality degrades over time unless actively maintained. Records
become stale. Field semantics drift. New requirements emerge that existing data doesn't
satisfy. Continuous completeness monitoring detects these trends before they become crises.

## Connecting to Curation Workflows

Completeness measurement is most valuable when it connects to curation workflows:

1. **Identify gaps**: Which items have the lowest completeness?
2. **Prioritize work**: Given limited curator time, which gaps matter most?
3. **Track progress**: Is curation effort actually improving completeness?
4. **Enforce standards**: Prevent merging data that would regress quality

This positions completeness assessment as infrastructure for data stewardship, not just
a metric to report.

## Summary: Two Complementary Approaches

| Aspect | Validation | Completeness Assessment |
|--------|------------|------------------------|
| **Question** | Is this data acceptable? | Is this data useful? |
| **Output** | Pass/Fail | Percentage (0-100%) |
| **Scope** | Required constraints | Recommended fields |
| **Action** | Block bad data | Guide curation effort |
| **Granularity** | Per-record | Hierarchical/aggregated |
| **Weights** | Equal (all required) | Configurable by importance |

Both are necessary. Validation ensures data integrity. Completeness assessment measures
data utility. Together, they provide a complete picture of data quality.

---

## How This Applies to LinkML

In LinkML schemas, the distinction between required and recommended fields is explicit:

- **Required fields** (`required: true`) — Enforced by LinkML validators
- **Recommended fields** (`recommended: true`) — Not enforced, but tracked by this tool

This makes LinkML particularly well-suited for completeness assessment: the schema itself
encodes which fields matter for quality, and the tool can automatically discover and
measure them without additional configuration.

For implementation details, path notation syntax, and configuration options, see
the [Reference](../cli-reference.md) and [How-To](../how-to/configuration.md) sections.

## Further Reading

- Wang, R. Y. & Strong, D. M. (1996). [Beyond Accuracy: What Data Quality Means to Data Consumers](http://web.mit.edu/tdqm/www/tdqmpub/beyondaccuracy_files/beyondaccuracy.html). *Journal of Management Information Systems*, 12(4), 5-33.
- RDA Working Group (2020). [FAIR Data Maturity Model](https://datascience.codata.org/articles/10.5334/dsj-2020-041). *Data Science Journal*.
- DAMA-NL (2020). [Dimensions of Data Quality](https://www.dama-nl.org/wp-content/uploads/2020/09/DDQ-Dimensions-of-Data-Quality-Research-Paper-version-1.2-d.d.-3-Sept-2020.pdf). Research Paper.
- [TDWG Biodiversity Data Quality Interest Group](https://www.tdwg.org/community/bdq/) — Framework for assessing fitness for use in biodiversity data.
