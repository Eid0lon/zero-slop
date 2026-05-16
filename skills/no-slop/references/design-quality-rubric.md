# Design Quality Rubric

Use this after scanning and before final delivery.

Score each dimension from 0 to 5.

| Score | Meaning |
| ---: | --- |
| 0 | Missing, harmful, inaccessible, deceptive, or broken. |
| 1 | Present but generic, fragile, or mostly decorative. |
| 2 | Usable but weak; needs product-specific decisions. |
| 3 | Solid and appropriate. |
| 4 | Strong, coherent, and verified. |
| 5 | Distinctive, precise, durable, and hard to mistake for template work. |

## Dimensions

1. Purpose and positioning.
2. Information hierarchy.
3. Brand and art direction.
4. Typography.
5. Component system and states.
6. Content and voice.
7. Accessibility.
8. Responsive behavior.
9. Motion and feedback.
10. Implementation quality.
11. Token coherence.
12. Product evidence.

## Hard Minimums

For `--scan`:

- Identify score, signatures, top blockers, and confidence.

For `--fix`:

- No dimension scored `0`.
- Accessibility, responsive behavior, implementation quality, and token coherence must each score at least `3`.
- AI-slop score must be below the active gate or reduced by at least 30% when legacy constraints make the gate impossible.

For `--redesign`:

- Average score at least `3.5`.
- Brand/art direction, hierarchy, content, and product evidence each score at least `3`.
- AI-slop score below the active gate.
- Judge panel passes.

For `--prevent`:

- Prevention contract scores at least `4` on purpose, hierarchy, accessibility plan, and copy precision before code generation.

## Rubric Checks

Purpose:

- Does the first viewport answer what this is and what the user can do?
- Is the primary job visible?
- Does the design match audience, domain, and risk?

Hierarchy:

- Can the eye find priority in three seconds?
- Are sections ordered by user decision, not template convention?
- Are primary and secondary actions visually distinct?

Brand:

- Do palette, type, radius, imagery, icon style, copy, and motion belong together?
- Is there a product/domain signal beyond logo text?

Content:

- Are CTAs specific?
- Are claims supported?
- Are empty, loading, error, and success states useful?

Accessibility:

- Is contrast likely WCAG AA?
- Are controls labeled?
- Is focus visible?
- Is keyboard navigation preserved?
- Is reduced motion respected?

Responsive:

- Does text fit on mobile?
- Do fixed-format elements have stable dimensions?
- Does first viewport avoid trapping the page?

Implementation:

- Are tokens semantic?
- Are utilities excessive?
- Are states complete?
- Are media dimensions stable?
- Do build/lint/type/test commands pass when available?
