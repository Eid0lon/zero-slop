# Perfect UX Judge System

The judge panel is active by default. Disable it only with `-e` or `--economy`.

## Operating Principle

Judges are strict, user-harm oriented, and evidence-seeking. They are looking for reasons a real user would fail, hesitate, mistrust the system, abandon the task, or need support.

Judges must:

- Score independently.
- Avoid praise padding.
- Cite files, UI regions, screenshots, task steps, or exact states.
- Treat rendered browser evidence and task walkthroughs as stronger than code scans.
- Compare against the UX Contract, dials, preset, and verification evidence.
- Name blockers before minor polish.
- Force another pass when gates fail.

## Required Judges

Use 4-6 judges. Use all six for high-risk UX, forms, checkout, onboarding, AI tools, dashboards, admin tools, or public services.

1. `User Need Judge`: user, context, job clarity, task value, and completion condition.
2. `Journey and IA Judge`: entry, orientation, navigation, hierarchy, decision path, and return path.
3. `Interaction and Recovery Judge`: controls, forms, validation, feedback, errors, undo, retry, and state coverage.
4. `Accessibility and Mobile Judge`: keyboard, focus, semantics, labels, contrast, touch, responsive stability, reduced motion.
5. `Content and Trust Judge`: labels, microcopy, claims, AI uncertainty, privacy, consent, data source, and honest boundaries.
6. `Measurement and Evidence Judge`: task proof, metrics, tests, analytics plan, research assumptions, and verification quality.

## Prompt Template

```text
You are the {judge_name} for perfect-ux.

Mode: {mode}
Preset: {preset}
Dials: {dials}
Target: {target}
UX Contract: {contract_summary}
Journey map: {journey_summary}
Sibling skill summaries: {sibling_summary}
Changed files/screenshots/browser evidence: {evidence}

Evaluate with maximum severity. Decide whether a real user can complete the primary job with clarity, confidence, accessibility, recovery, and trust.

Return only:
- score: 0-10
- verdict: PASS | FAIL
- blockers: concrete blockers with file/line, UI region, state, or journey step when possible
- forced_improvements: ordered list
- one_sentence_reason: blunt user-harm summary
```

## Gate

Use `dials-and-presets.md` for thresholds.

Gate passes only when:

- panel average >= minimum panel average
- lowest judge >= minimum lowest score
- UX score >= minimum UX score
- no hard UX gate blocker exists
- accessibility and keyboard gates pass
- primary journey verification ran or tool limitation is recorded
- sibling skill limitations are explicit

## Failure Protocol

For editable modes:

1. Fix hard blockers first.
2. Re-run deterministic precheck.
3. Re-run sibling skill checks when relevant.
4. Re-run judges.
5. Continue until pass or exact blocker.

For audit/judge-only modes:

- Report failures and stop.

If subagent tools are unavailable:

```text
JUDGE_PANEL_UNAVAILABLE
```

Do not claim a full pass.

