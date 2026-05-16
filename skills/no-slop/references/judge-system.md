# Multi-Agent Judge System

The judge panel is active by default. Disable it only with `-e` or `--economy`.

## Operating Principle

The panel is adversarial, clinical, and strict. It is not a brainstorming group. It looks for reasons the work should not ship.

Judges must:

- Score independently.
- Refuse vague praise.
- Name concrete blockers.
- Cite file paths, UI regions, or screenshots when possible.
- Compare the work against the active dials and preset.
- Force another improvement pass when gates fail.

## Required Panel

Run 4-6 judges. Use all six for redesign, prevention, or high-risk UI. Use at least four for small fixes.

1. `Visual Forensics Judge`: palette, typography, composition, rhythm, hierarchy, visual cliches.
2. `Product UX Judge`: user job, workflow clarity, information architecture, first viewport, task completion.
3. `Design-System Judge`: tokens, components, state consistency, code/style architecture.
4. `Accessibility and Responsive Judge`: contrast, focus, keyboard, labels, reduced motion, mobile overflow.
5. `Copy and Brand Judge`: specificity, voice, CTA clarity, fake proof, brand coherence.
6. `Motion and Interaction Judge`: motion purpose, feedback, loading/empty/error states, reduced-motion behavior.

## Subagent Launch Contract

When subagent tools are available and economy mode is false, launch the judges in parallel after the scan and again after fix/redesign output.

Give each judge only:

- Target path or relevant files.
- Current mode.
- Active preset and dials.
- Scan summary and screenshots if available.
- The judge's role.

Do not give judges the intended answer. Do not ask them to be nice. Ask them to find blockers.

Prompt template:

```text
You are the {judge_name} for no-slop.

Mode: {mode}
Preset: {preset}
Dials: {dials}
Target: {target}

Evaluate the UI/code with maximum severity. Find generic AI-slop, weak design decisions, accessibility risks, brand incoherence, and anything that should block shipping.

Return only:
- score: 0-10
- verdict: PASS | FAIL
- blockers: concrete issues with file/line or UI region when possible
- forced_improvements: ordered list
- one_sentence_reason: cold summary
```

## Missing Subagent Tools

If economy mode is false but subagent tools are unavailable, the gate cannot be marked `PASS`.

Use:

```text
JUDGE_PANEL_UNAVAILABLE
```

Then provide the deterministic local judge table as a precheck only. The result may guide remediation, but it is not a completed non-economy judge pass. To complete the workflow, either:

- rerun with subagent tools available, or
- rerun explicitly with `--economy`, accepting `ECONOMY_REVIEW`.

## Aggregation

Compute:

```text
panel_average = average(judge_scores)
lowest_judge = min(judge_scores)
allowed_slop_score = from dials-and-presets.md
```

Gate passes only when all are true:

- `slop_score <= allowed_slop_score`
- `panel_average >= minimum_panel_average`
- `lowest_judge >= minimum_lowest_judge`
- no hard blocker exists

Hard blockers:

- Accessibility blocker.
- Broken mobile or text overlap.
- Deceptive pattern.
- Fake production proof.
- Placeholder content in production surface.
- Primary workflow unclear or blocked.
- Severe token violation across shared components.
- Severe hierarchy collapse above the fold.
- Severe brand incoherence.

## Failure Protocol

For `--scan`:

- Report gate failure and required fixes.
- Do not edit.

For `--fix` or `--redesign`:

1. Apply the smallest improvement pass that addresses hard blockers first.
2. Re-scan changed files.
3. Re-run judges.
4. If the gate still fails after a reasonable pass, stop and return `BLOCKED`, with exact remaining blockers.

For `--prevent`:

- Do not generate UI code until the design contract passes.
- If the contract fails twice, stop and ask for missing product/brand constraints or propose a stricter default contract.

## Economy Fallback

When `--economy` is set, do not launch subagents. Instead:

- Apply the same rubric locally.
- Produce a self-judge table with the six judge roles.
- Mark the gate as `ECONOMY_REVIEW`, not as a full panel pass.

Economy mode is a cost optimization, not a quality downgrade.

`JUDGE_PANEL_UNAVAILABLE` is not economy mode. It is a blocked non-economy run.
