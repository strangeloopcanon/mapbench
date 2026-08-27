# MapBench map-drawing rubric v3

This rubric measures whether an image model can produce a correct, sufficiently complete, and readable map from a written request. It evaluates the generated map as a map, not its resemblance to a hidden reference design.

The four dimensions are mutually exclusive questions:

1. **Where is it?** — spatial construction
2. **What does it claim?** — factual and semantic correctness
3. **What is missing?** — coverage
4. **Can the reader decode it?** — cartographic legibility

## Dimensions

Each judge scores every dimension from 0 to 5 using whole numbers. A published aggregate may contain half-points when two non-adjudicated judge records are averaged. The aggregate raw score is recomputed from those averaged dimensions before the agreed cap is applied. See [`protocol.md`](protocol.md) for the aggregation and adjudication rules.

| Key | Dimension | Weight | Exclusive scope |
| --- | --- | ---: | --- |
| `spatial` | Spatial construction | 40 | The shapes, locations, extents, adjacency, containment, and direction of all mapped features: coastlines, landmasses, borders, territories, cities, rivers, routes, arrows, and events. Projection and framing belong here when they distort those relationships. This dimension asks only **where and in what shape**. |
| `factual` | Factual and semantic correctness | 25 | The identity, period, date, name, sovereignty, affiliation, category, and stated meaning of features that are present. Legend-to-map consistency and invented or garbled names belong here. This dimension asks only **what, who, and when**. |
| `coverage` | Required coverage | 15 | Whether the principal features explicitly requested by the prompt, or indispensable to its central subject, are present. This dimension measures omissions only; it does not judge the correctness of present features. |
| `legibility` | Cartographic legibility | 20 | Whether a reader can decode the information at normal viewing size: distinguishable fills and line types, clear boundaries and routes, readable labels, adequate contrast, usable hierarchy, sensible density, and absence of rendering artifacts. It judges communication, not truth or decorative beauty. |

Raw-score formula:

```text
8 x spatial
+ 5 x factual
+ 3 x coverage
+ 4 x legibility
= raw score out of 100
```

## Score anchors

### Spatial construction

- **5:** Important geometry and spatial relationships are correct; only negligible drawing imprecision.
- **4:** Minor local distortions that do not change the map's interpretation.
- **3:** One material spatial error, or several moderate errors; usable after correction.
- **2:** Multiple material spatial errors make the map misleading.
- **1:** The central geography, extent, or route structure is substantially wrong.
- **0:** No usable map geometry.

### Factual and semantic correctness

- **5:** Present features are correctly identified, dated, categorized, and explained.
- **4:** Minor naming or classification mistakes that do not change the main interpretation.
- **3:** One material factual error, or several moderate errors; usable after correction.
- **2:** Multiple material factual errors make the map misleading.
- **1:** The central subject, period, or political frame is wrong.
- **0:** The claims are unrelated or predominantly fabricated.

### Required coverage

- **5:** All principal requested features and the necessary supporting context are present.
- **4:** Complete central account with only minor supporting omissions.
- **3:** One principal omission, or several meaningful supporting omissions.
- **2:** Several principal requested features are missing.
- **1:** Only fragments of the requested content are present.
- **0:** The requested content is absent.

### Cartographic legibility

- **5:** Immediately readable and publication-ready at normal size.
- **4:** Clear and usable with minor local clutter or rendering defects.
- **3:** Readable overall, but several areas require effort or revision.
- **2:** Important information is difficult to distinguish or read.
- **1:** Most of the map cannot be decoded reliably.
- **0:** Visually unusable as a map.

## Single-fault assignment rule

Record each underlying defect once, according to the correction it requires:

| Defect | Score it under |
| --- | --- |
| A requested feature is absent | `coverage` |
| A present feature has the wrong location, shape, extent, adjacency, or direction | `spatial` |
| A present feature has the wrong identity, name, date, period, allegiance, category, or legend meaning | `factual` |
| Correct information is hard to read, distinguish, or trace | `legibility` |

Do not penalize an absent feature again for having no location, label, or styling. Do not penalize a false label again merely because it is visually prominent. Count two defects only when they require two independent corrections.

Examples:

- Missing Duchy of Warsaw: `coverage`.
- Duchy of Warsaw drawn in the wrong place: `spatial`.
- French Algeria shown in 1811: `factual`.
- A route travels in the wrong direction: `spatial`.
- Blue means "allied" in the legend but marks an enemy state: `factual`.
- Two correct categories use colors that cannot be distinguished: `legibility`.
- A correct label is unreadable: `legibility`.
- An invented or misspelled place name: `factual`.

## Material-error gate

A material error is a defect that would cause a reasonable reader to misunderstand the central geography, history, chronology, political control, route, or requested account. Minor distortions, small typographic blemishes, and optional contextual omissions are not material errors.

Apply the lowest applicable cap after calculating the raw score:

| Condition | Maximum final score |
| --- | ---: |
| No material errors | 100 |
| One material error | 74 |
| Two or more independent material errors | 59 |
| Central subject, period, or political frame is wrong | 39 |
| Not interpretable as the requested map, or wholesale fabrication | 20 |

The final score is the lower of the weighted raw score and the applicable cap. Graphic polish cannot compensate for a materially false map.

## Interpretation bands

| Final score | Interpretation |
| --- | --- |
| 90-100 | Excellent: accurate, complete, and publishable with ordinary review |
| 75-89 | Good: useful with minor corrections only |
| 60-74 | Usable draft: one material correction required |
| 40-59 | Misleading: multiple material corrections required |
| 21-39 | Substantive failure |
| 0-20 | Not a usable map |

## Evaluation protocol

- Judge the generated image against its saved prompt. The hidden reference supplies factual evidence, not a target layout or style.
- Inspect at normal size and with reasonable zoom.
- Do not use OCR, pixel matching, or survey-grade geometric tolerances.
- Do not reward ornament, texture, or resemblance to a conventional atlas unless it improves legibility.
- List every material error and assign it to exactly one dimension before scoring.
- Use the capped final score for ranking and the uncapped raw score only as a tie-breaker.

## Required record

```json
{
  "id": "MB001",
  "scores": {
    "spatial": 0,
    "factual": 0,
    "coverage": 0,
    "legibility": 0
  },
  "raw_total": 0,
  "material_errors": [
    {
      "dimension": "factual",
      "description": "Specific defect"
    }
  ],
  "cap_reason": "none",
  "cap": 100,
  "total": 0,
  "confidence": 0.0,
  "summary": "One concise judgment."
}
```
