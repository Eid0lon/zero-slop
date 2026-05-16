# Dials and Presets

All dials are integers from 0 to 10. A dial is not decoration; it changes standards and design decisions.

## Dials

| Dial | Default | Meaning |
| --- | ---: | --- |
| `SLOP_TOLERANCE` | 1 | How much generic AI UI is tolerated. `0` means none. `10` means permissive, never recommended for production. |
| `STRICTNESS` | 9 | How severe scanning and judging should be. `10` treats weak hierarchy, vague copy, and token drift as blockers. |
| `VISUAL_DENSITY` | 5 | Information density. Low is spacious/editorial; high is compact/operational. |
| `MOTION_INTENSITY` | 2 | Motion budget. Low removes decorative motion; high allows expressive motion only when purposeful. |
| `BRAND_STRENGTH` | 7 | How strongly palette, type, shape, copy, and imagery must express a specific identity. |
| `HIERARCHY_SHARPNESS` | 8 | Required clarity of priority, scanning path, and visual contrast between levels. |
| `COPY_PRECISION` | 8 | Required specificity of labels, CTAs, claims, errors, and empty states. |
| `VARIANCE` | 6 | Expected variation in rhythm, composition, components, and content structure. Low favors systematic repetition; high demands more distinct sections. |

## Dial Effects

- Higher `STRICTNESS` lowers the allowed slop score and raises judge thresholds.
- Higher `SLOP_TOLERANCE` raises the allowed slop score but cannot waive accessibility, deception, broken layout, or fake content.
- Higher `VISUAL_DENSITY` penalizes oversized cards, oversized hero text, decorative whitespace, and low-information dashboards.
- Higher `MOTION_INTENSITY` permits richer motion, but `Motion Spam` remains a failure when motion lacks purpose or reduced-motion support.
- Higher `BRAND_STRENGTH` penalizes template palettes, stock copy, generic icons, and visual systems with no domain signal.
- Higher `HIERARCHY_SHARPNESS` penalizes flat type scales, equal-weight sections, repeated card grids, and unclear first viewports.
- Higher `COPY_PRECISION` penalizes buzzwords, vague CTAs, fake proof, generic testimonials, and placeholder content.
- Higher `VARIANCE` penalizes formulaic section repetition. Lower `VARIANCE` is acceptable for tables, forms, and operational screens.

## Gate Formula

Use this as the default non-economy judge gate:

```text
allowed_slop_score = clamp(12 + (SLOP_TOLERANCE * 3) - (STRICTNESS * 2), 8, 35)
minimum_panel_average = clamp(7.0 + (STRICTNESS * 0.2) - (SLOP_TOLERANCE * 0.1), 7.0, 9.2)
minimum_lowest_judge = clamp(6.5 + (STRICTNESS * 0.15) - (SLOP_TOLERANCE * 0.1), 6.5, 8.6)
```

Hard blockers override formulas:

- Accessibility blocker.
- Broken mobile layout or text overlap.
- Fake proof, placeholder production content, or deceptive pattern.
- First viewport fails to show the product, object, tool, place, game, or primary task when that matters.
- Judge panel flags `Brand Incoherence`, `Hierarchy Collapse`, or `Design Token Violation` as severe.

## Presets

### SaaS

```text
SLOP_TOLERANCE=1
STRICTNESS=9
VISUAL_DENSITY=5
MOTION_INTENSITY=2
BRAND_STRENGTH=7
HIERARCHY_SHARPNESS=8
COPY_PRECISION=9
VARIANCE=6
```

Bias: product proof above vague positioning. Avoid fake dashboards, fake metrics, generic gradients, and feature-card soup.

### Dashboard

```text
SLOP_TOLERANCE=0
STRICTNESS=10
VISUAL_DENSITY=8
MOTION_INTENSITY=1
BRAND_STRENGTH=5
HIERARCHY_SHARPNESS=9
COPY_PRECISION=8
VARIANCE=4
```

Bias: dense scanning, comparison, stable tables, clear filters, keyboard paths. Decorative heroes fail.

### Portfolio

```text
SLOP_TOLERANCE=1
STRICTNESS=8
VISUAL_DENSITY=4
MOTION_INTENSITY=4
BRAND_STRENGTH=9
HIERARCHY_SHARPNESS=8
COPY_PRECISION=8
VARIANCE=8
```

Bias: strong point of view, real work evidence, varied rhythm. Generic SaaS cards fail.

### E-commerce

```text
SLOP_TOLERANCE=0
STRICTNESS=10
VISUAL_DENSITY=7
MOTION_INTENSITY=2
BRAND_STRENGTH=7
HIERARCHY_SHARPNESS=9
COPY_PRECISION=10
VARIANCE=5
```

Bias: findability, comparison, price clarity, filters, checkout truth. Fake scarcity fails.

### Brutalist

```text
SLOP_TOLERANCE=1
STRICTNESS=8
VISUAL_DENSITY=7
MOTION_INTENSITY=1
BRAND_STRENGTH=10
HIERARCHY_SHARPNESS=9
COPY_PRECISION=8
VARIANCE=8
```

Bias: deliberate rawness. Sloppy spacing, bad contrast, and random borders are not brutalism.

### Minimal

```text
SLOP_TOLERANCE=0
STRICTNESS=10
VISUAL_DENSITY=4
MOTION_INTENSITY=1
BRAND_STRENGTH=6
HIERARCHY_SHARPNESS=10
COPY_PRECISION=10
VARIANCE=3
```

Bias: fewer elements, sharper intent. Empty generic whitespace fails.

### Editorial

```text
SLOP_TOLERANCE=1
STRICTNESS=8
VISUAL_DENSITY=5
MOTION_INTENSITY=3
BRAND_STRENGTH=9
HIERARCHY_SHARPNESS=9
COPY_PRECISION=9
VARIANCE=8
```

Bias: typography, sequence, imagery, voice. Template sections fail.

### AI Tool

```text
SLOP_TOLERANCE=0
STRICTNESS=10
VISUAL_DENSITY=7
MOTION_INTENSITY=2
BRAND_STRENGTH=7
HIERARCHY_SHARPNESS=9
COPY_PRECISION=10
VARIANCE=5
```

Bias: task controls, sources, constraints, confidence, failure recovery. A chat box alone fails unless it truly is the product.
