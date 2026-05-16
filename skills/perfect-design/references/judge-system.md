# Premium Judge System

The judge panel is active by default. Disable it only with `-e` or `--economy`.

## Operating Principle

Judges are brutal, specific, and shipment-oriented. They are looking for reasons a senior design engineer would reject the work.

Judges must:

- Score independently.
- Avoid praise padding.
- Cite files, UI regions, screenshots, or exact states.
- Treat actual screenshots as stronger evidence than deterministic scanner scores.
- Compare against the Design Contract, dials, preset, and no-slop result.
- Name blockers before minor polish.
- Force another pass when gates fail.

## Required Judges

Use 4-6 judges. Use all six for create/redesign/high-risk UI.

1. `Art Direction Judge`: visual identity, typography, palette, rhythm, composition, distinctiveness.
2. `Product UX Judge`: user job, IA, first viewport, workflow completion, decision path.
3. `Interaction Judge`: states, keyboard, command patterns, feedback, motion purpose.
4. `Design System Judge`: tokens, components, implementation coherence, maintainability.
5. `Accessibility and Responsive Judge`: WCAG, focus, labels, contrast, mobile, reduced motion.
6. `Content and Proof Judge`: copy specificity, product evidence, claims, empty/error states, brand voice.

## Prompt Template

```text
You are the {judge_name} for perfect-design.

Mode: {mode}
Preset: {preset}
Dials: {dials}
Target: {target}
Design Contract: {contract_summary}
No-slop summary: {no_slop_summary}
Changed files/screenshots: {evidence}

Evaluate with maximum severity. Decide whether this feels like a senior design engineer shipped it.

Return only:
- score: 0-10
- verdict: PASS | FAIL
- blockers: concrete blockers with file/line or UI region when possible
- forced_improvements: ordered list
- one_sentence_reason: blunt summary
```

## Gate

Use `dials-and-presets.md` for thresholds.

Gate passes only when:

- panel average >= minimum panel average
- lowest judge >= minimum lowest score
- premium score >= minimum premium score
- no hard blocker exists
- no-slop gate passes or limitation is explicitly recorded
- desktop and mobile screenshots show no clipping or primary-workflow overflow

## Failure Protocol

For editable modes:

1. Fix hard blockers first.
2. Re-run no-slop gate.
3. Re-run judges.
4. Continue until pass or explicit blocker.

For scan/judge-only modes:

- Report failures and stop.

If subagent tools are unavailable:

```text
JUDGE_PANEL_UNAVAILABLE
```

Do not claim a full pass.
