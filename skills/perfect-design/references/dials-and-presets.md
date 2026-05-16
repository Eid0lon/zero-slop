# Dials and Presets

All dials are integers from `0` to `10`.

## Dials

| Dial | Default | Meaning |
| --- | ---: | --- |
| `CRAFT_STRICTNESS` | 9 | How severe the premium bar is. `10` treats weak hierarchy and vague direction as blockers. |
| `DENSITY` | 6 | Information density. Higher favors operational, scan-friendly UI. |
| `BRAND_SPECIFICITY` | 8 | How much the interface must feel tied to this exact product/domain. |
| `HIERARCHY_CONTRAST` | 9 | Required clarity of reading path, priority, and action order. |
| `INTERACTION_DEPTH` | 6 | Expected statefulness, keyboard flow, feedback, and workflow ergonomics. |
| `MOTION_DISCIPLINE` | 8 | Higher means motion must be purposeful, restrained, and reduced-motion safe. |
| `CONTENT_PRECISION` | 9 | Required specificity of labels, claims, empty states, errors, and CTAs. |
| `SYSTEM_COHERENCE` | 9 | Token, component, spacing, radius, color, and state consistency. |
| `A11Y_RIGOR` | 10 | Accessibility expectations. `10` treats focus, keyboard, contrast, and labels as hard gates. |
| `DISTINCTIVENESS` | 7 | How much the layout and art direction must avoid template sameness. |

## Gate Formula

Use these defaults for non-economy judging:

```text
minimum_panel_average = clamp(7.6 + CRAFT_STRICTNESS * 0.16, 8.0, 9.4)
minimum_lowest_score = clamp(7.2 + CRAFT_STRICTNESS * 0.13, 7.5, 9.0)
minimum_premium_score = clamp(78 + CRAFT_STRICTNESS * 1.5, 82, 94)
```

Hard blockers override formulas.

## Presets

### Operational SaaS

```text
CRAFT_STRICTNESS=10
DENSITY=8
BRAND_SPECIFICITY=6
HIERARCHY_CONTRAST=9
INTERACTION_DEPTH=8
MOTION_DISCIPLINE=9
CONTENT_PRECISION=9
SYSTEM_COHERENCE=10
A11Y_RIGOR=10
DISTINCTIVENESS=5
```

Bias: compact, fast, clear, power-user friendly. Avoid oversized heroes and decorative surfaces.

### Developer Tool

```text
CRAFT_STRICTNESS=10
DENSITY=7
BRAND_SPECIFICITY=8
HIERARCHY_CONTRAST=9
INTERACTION_DEPTH=8
MOTION_DISCIPLINE=9
CONTENT_PRECISION=10
SYSTEM_COHERENCE=10
A11Y_RIGOR=10
DISTINCTIVENESS=6
```

Bias: code examples, command flows, logs, real artifacts, keyboard efficiency, exact copy.

### Dashboard

```text
CRAFT_STRICTNESS=10
DENSITY=9
BRAND_SPECIFICITY=5
HIERARCHY_CONTRAST=10
INTERACTION_DEPTH=8
MOTION_DISCIPLINE=10
CONTENT_PRECISION=9
SYSTEM_COHERENCE=10
A11Y_RIGOR=10
DISTINCTIVENESS=4
```

Bias: data first, comparison, filters, stable tables, clear thresholds.

### Editorial

```text
CRAFT_STRICTNESS=9
DENSITY=5
BRAND_SPECIFICITY=10
HIERARCHY_CONTRAST=10
INTERACTION_DEPTH=6
MOTION_DISCIPLINE=7
CONTENT_PRECISION=9
SYSTEM_COHERENCE=9
A11Y_RIGOR=10
DISTINCTIVENESS=9
```

Bias: typography, sequence, imagery, pacing, strong point of view.

### Commerce

```text
CRAFT_STRICTNESS=10
DENSITY=8
BRAND_SPECIFICITY=8
HIERARCHY_CONTRAST=9
INTERACTION_DEPTH=8
MOTION_DISCIPLINE=9
CONTENT_PRECISION=10
SYSTEM_COHERENCE=10
A11Y_RIGOR=10
DISTINCTIVENESS=6
```

Bias: product comparison, price clarity, trustworthy checkout, real images, no fake urgency.

### Portfolio

```text
CRAFT_STRICTNESS=9
DENSITY=5
BRAND_SPECIFICITY=10
HIERARCHY_CONTRAST=9
INTERACTION_DEPTH=6
MOTION_DISCIPLINE=7
CONTENT_PRECISION=9
SYSTEM_COHERENCE=9
A11Y_RIGOR=10
DISTINCTIVENESS=10
```

Bias: work evidence, personal point of view, varied rhythm, proof over generic self-description.
