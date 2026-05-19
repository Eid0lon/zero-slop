---
name: perfect-ux
description: Beta research-backed UX engineering skill for auditing, mapping, improving, and judging product experiences so real users can complete important jobs with clarity, confidence, accessibility, recovery, and measurable friction reduction. Use when Codex works on UX flows, IA, forms, onboarding, dashboards, commerce, AI tools, CRUD, editors, settings, service design, microcopy, accessibility, usability testing, or any interface that must feel effortless instead of merely attractive. Composes with perfect-design, no-slop, and reality-skill.
---

# Perfect UX

Status: beta.

Perfect UX is the user-success layer. `perfect-design` makes the interface coherent and product-specific; `no-slop` blocks generic AI residue; `reality-skill` makes workflows real. Perfect UX asks: can the intended user understand what to do, finish the job, recover from problems, trust the system, and get faster over time?

## Command Interface

Use `references/command-interface.md`.

Primary commands:

```bash
perfect-ux --contract [brief-or-target]
perfect-ux --map [brief-or-target]
perfect-ux --audit [target]
perfect-ux --fix [target]
perfect-ux --harden [target]
perfect-ux --judge [target]
perfect-ux --verify [target]
perfect-ux -e --audit [target]
```

Short flags:

- `-c`, `--contract`: write the UX Contract before code.
- `-m`, `--map`: map jobs, entry points, decisions, states, and recovery paths.
- `-a`, `--audit`: find UX friction, ambiguity, accessibility blockers, trust gaps, and missing evidence.
- `-f`, `--fix`: make the smallest coherent UX improvement pass.
- `--harden`: add resilience, edge states, keyboard paths, recovery, and proof.
- `-j`, `--judge`: run the strict UX judge panel.
- `--verify`: prove the primary journey with build, tests, browser, accessibility, and task evidence.
- `-e`, `--economy`: disable live subagent judges only when the user explicitly accepts a lower-cost review.

Default mode:

- Existing UI target: `--audit`.
- Editable request on an existing target: `--fix`.
- Brief without target: `--contract`.

## First Action

Load `steps/step-00-command-router.md`.

Step 00 parses command flags, discovers the product surface, resolves UX dials, loads only relevant references, and routes to contract, map, audit, fix, harden, judge, or verify.

## Core References

Load only what the task needs:

- `references/command-interface.md`: grammar, precedence, output contracts.
- `references/dials-and-presets.md`: UX dials, presets, and pass thresholds.
- `references/research-synthesis.md`: compressed research from NN/g, W3C/WAI, WCAG, GOV.UK, Apple HIG, Material, Fluent, Baymard, web.dev, design systems, and Human-AI guidance.
- `references/research-source-ledger.md`: source map and what each source contributes.
- `references/ux-contract.md`: pre-code contract and rejection rules.
- `references/ux-gates.md`: the hard UX gates used for audit, fix, harden, and judge.
- `references/journey-playbook.md`: jobs, IA, flow mapping, decision paths, onboarding, dashboards, commerce, AI tools, and expert use.
- `references/interaction-playbook.md`: controls, forms, feedback, validation, recovery, keyboard, motion, mobile, and performance feel.
- `references/content-and-trust.md`: UX writing, labels, claims, AI uncertainty, empty states, errors, consent, and trust boundaries.
- `references/measurement-and-research.md`: usability testing, analytics, task metrics, research method choice, and evidence loops.
- `references/ecosystem-contract.md`: ownership and composition with sibling skills.
- `references/judge-system.md`: judge protocol and gate formula.
- `references/verification-playbook.md`: build/browser/accessibility/task verification.
- `references/self-coaching.md`: internal checklist for stuck or ambiguous UX decisions.

## Non-Negotiables

- Always write or infer a UX Contract before changing UX.
- Always identify the primary user, job, start point, completion condition, decision moments, risks, recovery paths, and evidence needed.
- Inspect existing routes, state, data, forms, controls, labels, errors, focus behavior, analytics hooks, tests, and design-system primitives before editing.
- Prefer reducing friction over adding explanatory chrome. If users need instructions, first simplify the object, flow, label, layout, or feedback.
- Do not accept a pretty screen as UX evidence. Use task completion, state coverage, keyboard access, error recovery, performance feel, and trust as gates.
- Do not hide hard choices behind generic labels like `Get started`, `Submit`, `Continue`, `Learn more`, or `AI powered` when the next action or risk can be named.
- Do not ship dead ends, ambiguous disabled controls, form loss after errors, invisible focus, keyboard traps, unexplained waits, fake progress, fake certainty, or unsupported claims.
- For AI tools, expose input constraints, model boundaries, sources when available, confidence or uncertainty where appropriate, user control, review/edit paths, and failure recovery.
- For dashboards, organize around decisions and operational questions, not decorative metrics.
- For commerce and checkout, prioritize price clarity, availability, shipping, returns, comparison, validation, and trust over persuasion effects.
- For forms, preserve input, validate near the field, keep focus manageable, explain recovery, and avoid placeholder-only labels.
- Compose with `reality-skill` when actions, data, persistence, or integrations must be real. Compose with `perfect-design` when visual direction changes. Compose with `no-slop` before and after material UI work.
- Judge with subagents by default. If live judges are unavailable and economy mode is false, mark `JUDGE_PANEL_UNAVAILABLE`; never claim a full pass.
- Iterate until the UX gate passes. If blocked, name the exact blocker and the user harm.

## Required State

Maintain this state throughout the workflow:

```text
command:
target:
mode:
economy_mode:
preset:
dials:
project_type:
primary_user:
primary_job:
start_point:
completion_condition:
journey_map:
ux_contract:
friction_score_before:
ux_score_before:
blocking_gates:
research_evidence:
files_changed:
implementation_strategy:
judge_panel:
judge_gate:
verification:
ux_score_after:
remaining_risk:
ship_decision:
```

## UX Contract

Before editing, write or infer a compact contract:

```text
User:
Context:
Primary job:
Starting point:
Completion condition:
Decision moments:
Inputs required:
System feedback required:
Failure/recovery paths:
Accessibility constraints:
Mobile/responsive constraints:
Performance constraints:
Trust/safety constraints:
Evidence to verify:
Forbidden friction:
```

Ask the user only when multiple high-impact jobs conflict and a wrong choice would waste the implementation. Otherwise infer conservatively from code and product context.

## Local CLI Helper

For deterministic prechecks:

```bash
python skills/perfect-ux/scripts/perfect_ux_cli.py --audit <target>
python skills/perfect-ux/scripts/perfect_ux_cli.py --contract "brief text"
python skills/perfect-ux/scripts/perfect_ux_cli.py --json --audit <target>
python skills/perfect-ux/scripts/perfect_ux_cli.py --preset ai-tool --dial ERROR_RECOVERY=10 --audit <target>
```

The CLI catches common UX risk signals. It is not a replacement for reading code, rendered browser walkthroughs, usability evidence, sibling skills, or live judge panels.

## Done Means

- The primary job can be understood and completed.
- The path has clear entry, decision, action, feedback, completion, and recovery states.
- Labels, copy, and IA reveal the system model without filler explanation.
- Forms and controls are accessible, keyboard-operable, responsive, and resilient to messy input.
- Important waits, failures, empty states, disabled states, and success states are visible and actionable.
- Trust-sensitive claims are supported, scoped, disabled, or rewritten honestly.
- Performance does not create perceptual friction through layout shift, sluggish interaction, or unstable content.
- Verification ran, or the exact blocker and unverified risk are stated.
