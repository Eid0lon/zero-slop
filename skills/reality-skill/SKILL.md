---
name: reality-skill
description: Converts demo UIs into believable, end-to-end product workflows. Use when building, reviewing, or finishing apps, dashboards, CRUD flows, forms, onboarding, checkout, settings, auth-like surfaces, data tools, AI tools, integrations, or any UI that must behave like a real app instead of a static template. Composes after no-slop/perfect-design to make the interface operational, truthful, stateful, validated, persistent, and verifiable.
---

# Reality Skill

Reality Skill turns attractive screens into usable product workflows. It does not ask "does this look like an app?" It asks "can the intended user complete the job, recover from problems, and trust what the UI claims?"

Use this skill aggressively whenever a request says app, tool, dashboard, portal, editor, workflow, CRUD, form, checkout, onboarding, settings, upload, export, invite, generate, sync, connect, save, publish, deploy, analyze, or review.

## Command Interface

Use `references/command-interface.md`.

Primary commands:

```bash
reality --audit [target]
reality --fix [target]
reality --build [brief-or-target]
reality --harden [target]
reality --judge [target]
reality --verify [target]
reality -e --audit [target]
```

Short flags:

- `-a`, `--audit`: find dead actions, fake data, missing states, weak workflows.
- `-f`, `--fix`: make the smallest workflow-real implementation.
- `-b`, `--build`: build the real workflow model while creating a new app surface.
- `--harden`: add durability, recovery, validation, accessibility, and edge-state coverage.
- `-j`, `--judge`: score the app against the reality gates.
- `--verify`: prove the primary workflow by tests, build checks, and browser checks when possible.
- `-e`, `--economy`: skip live judge agents and use deterministic checks plus local review.

Default mode:

- Existing UI target: `--fix`.
- New app brief: `--build`.
- Review-only request: `--audit`.

## First Action

Load `steps/step-00-command-router.md`.

Step 00 parses the command, discovers project shape, loads only the needed references, and routes to audit, fix, build, harden, judge, or verify.

## Core References

Load only what the task needs:

- `references/command-interface.md`: grammar, mode precedence, output contracts.
- `references/reality-gates.md`: the twelve gates that define "not demoware."
- `references/app-archetypes.md`: workflow expectations for dashboards, CRUD, editors, checkout, AI tools, integrations, onboarding, settings, and auth-like surfaces.
- `references/implementation-playbook.md`: concrete patterns for data models, actions, state machines, validation, persistence, optimistic updates, undo, and honest mocks.
- `references/truth-boundaries.md`: how to represent sample data, unavailable services, auth, payments, exports, AI, analytics, and integrations without lying.
- `references/verification-playbook.md`: build, test, browser, persistence, accessibility, responsive, and smoke-test proof.
- `references/judge-system.md`: reality judge protocol and scoring gates.

## Non-Negotiables

- Do not stop at a static UI when the user asked for an app, dashboard, tool, form, editor, portal, or workflow.
- Do not ship dead buttons, `href="#"`, placeholder handlers, console-only submits, fake success toasts, decorative charts, fake metrics, fake users, fake payments, fake auth, fake AI, fake integrations, or fake exports.
- Do not claim production capability unless the code actually connects to the production capability with real credentials/configuration already present in the project.
- Prefer real project services, schemas, stores, routes, and design-system primitives over invented abstractions.
- When real backend/service access is absent, create an honest local boundary: local storage, in-memory state, fixture mode, disabled integration, explicit sample data, or documented adapter seam in code and UI.
- A primary workflow must include entry, intent, input, validation, submit/action, progress, success, failure, retry/recovery, persistence, and return/edit/delete paths where relevant.
- User-created or edited data must survive the immediate workflow. Use server/database/API first, existing store second, local storage/URL state third, and clearly scoped memory only for throwaway prototypes.
- Every primary action must either work, navigate to a real next step, or be disabled with a specific reason.
- Forms must preserve user input after errors and show actionable inline messages near the relevant fields.
- Data shown as real must be real or user-created. Sample data must be labeled as sample and must not pretend to be customers, revenue, uptime, compliance, security, or live analytics.
- Verification is part of the implementation, not an afterthought. For frontend work, run the app when feasible and inspect the workflow in a browser.
- Compose with `no-slop` and `perfect-design` when available: those skills improve design quality; Reality Skill makes the result operational and truthful.

## Required State

Maintain this state throughout the workflow:

```text
command:
target:
mode:
economy_mode:
project_type:
primary_user:
primary_job:
workflow_contract:
data_contract:
truth_boundaries:
reality_score_before:
blocking_gates:
files_changed:
implementation_strategy:
verification:
reality_score_after:
remaining_fake_boundaries:
ship_decision:
```

## Reality Contract

Before editing, write or infer a compact contract:

```text
User:
Job:
Starting point:
Completion condition:
Data needed:
Actions needed:
Persistence needed:
Unavailable real services:
Honest mock/local boundary:
States that must exist:
Verification path:
```

If the contract is unclear, inspect the app and infer the most likely primary job. Ask the user only when multiple high-impact jobs conflict and a wrong choice would waste the implementation.

## Local CLI Helper

For deterministic prechecks:

```bash
python skills/reality-skill/scripts/reality_cli.py --audit <target>
python skills/reality-skill/scripts/reality_cli.py --json --audit <target>
python skills/reality-skill/scripts/reality_cli.py --strict --audit <target>
```

The CLI catches common demoware signals. It is not a replacement for reading code, implementing the workflow, browser verification, or the reality judge.

## Done Means

- The primary job can be completed end-to-end.
- Primary actions are real or honestly unavailable.
- User input is validated and preserved.
- Relevant loading, empty, error, success, disabled, long-content, and small-screen states exist.
- User-created data persists through the expected scope.
- Navigation includes cancel, back, retry, return, edit, delete/recover paths where relevant.
- Fake capabilities are implemented, disabled, or clearly labeled as local/sample/mock boundaries.
- Verification ran, or the exact blocker is stated with the unverified risk.

