# Premium Quality Rubric

Score each dimension from `0` to `5`.

| Score | Meaning |
| ---: | --- |
| 0 | Missing, broken, deceptive, inaccessible, or harmful. |
| 1 | Generic or fragile. Looks like a template. |
| 2 | Usable but ordinary; lacks product-specific decisions. |
| 3 | Solid and coherent. |
| 4 | Strong, polished, and verified. |
| 5 | Distinctive, precise, durable, and difficult to mistake for generated work. |

## Dimensions

1. Product model clarity.
2. First viewport and primary workflow.
3. Information architecture.
4. Visual hierarchy.
5. Typography and reading rhythm.
6. Palette and token coherence.
7. Component states and interaction quality.
8. Content precision and product proof.
9. Accessibility.
10. Responsive stability.
11. Motion and feedback.
12. Implementation quality.
13. Performance and media stability.
14. Distinctiveness without trend costume.

## Score

```text
premium_score = round((sum(dimension_scores) / 70) * 100)
```

## Hard Minimums

For `--create` and `--redesign`:

- Premium score at least active gate.
- No dimension below `3`.
- Product model, hierarchy, content proof, accessibility, responsive stability, and implementation quality each at least `4`.
- `no-slop` gate must pass or be explicitly unavailable.
- Live judge panel must pass unless economy mode is explicitly enabled.

For `--polish`:

- No dimension below `3`.
- Changed surface should improve by at least `8` premium points or remove all named blockers.

For `--judge`:

- Findings first.
- Block weak output without apology padding.

## Hard Blockers

- The product cannot be understood from the first viewport.
- Primary workflow is unclear or blocked.
- It looks like a generic AI template after copy/logo swap.
- Fake proof, fake metrics, fake screenshots, or placeholder content appear as real.
- Mobile layout overlaps, clips, or hides primary actions.
- Keyboard/focus is broken.
- Accessibility blocker.
- Token system is incoherent across shared components.
- Motion, scroll, or media harms usability/performance.
