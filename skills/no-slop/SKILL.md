---
name: no-slop
description: Strict anti-slop UI design system for scanning, fixing, redesigning, judging, and preventing generic AI-generated frontend work. Use when Codex works on UI/UX, React/Vue/Svelte/HTML/CSS/Tailwind, landing pages, dashboards, apps, design systems, visual polish, copy, accessibility, motion, or frontend generation that must be judged with severe anti-slop standards. Supports commands such as no-slop --scan, --fix, --redesign, --judge, --prevent, and --economy.
---

# No Slop

No Slop is a cold, precise anti-slop workflow. Its job is to detect generic AI UI, remove it, and block weak output before it ships.

After anti-slop remediation, hand app-like surfaces to `reality-skill` so the result is not only less generic, but also usable beyond a static mockup.

## Command Interface

Use the command grammar in `references/command-interface.md`.

Primary commands:

```bash
no-slop --scan [target]
no-slop --fix [target]
no-slop --redesign [target]
no-slop --judge [target]
no-slop --prevent [target-or-brief]
no-slop --autopsy [target-or-brief]
no-slop -e --scan [target]
```

Short flags:

- `-s`, `--scan`: scan and score.
- `-f`, `--fix`: surgical remediation.
- `-r`, `--redesign`: full redesign.
- `-j`, `--judge`: run the strict judge panel.
- `--prevent`: prevention mode before UI generation.
- `--autopsy`: emit the forensic AI UI Autopsy report.
- `-e`, `--economy`: disable judge subagents and use local deterministic checks only.

Default mode is `--scan`. Judge mode is active by default unless `--economy` is set.

## First Action

Load `steps/step-00-command-router.md`.

Step 00 parses command flags, resolves dials and presets, loads the right references, and routes to scan, fix, redesign, judge, or prevent.

## Core References

Load only what the task needs:

- `references/command-interface.md`: CLI grammar, flag precedence, output contracts.
- `references/dials-and-presets.md`: the eight 0-10 control dials and fast presets.
- `references/ai-slop-patterns.md`: detection taxonomy, severity scoring, slop signatures.
- `references/judge-system.md`: mandatory multi-agent judge protocol and fail gates.
- `references/prevention-protocol.md`: pre-generation detector and judge workflow.
- `references/remediation-playbook.md`: fix/redesign tactics and before/after examples.
- `references/design-quality-rubric.md`: scoring rubric and quality gates.
- `references/ecosystem-contract.md`: ownership, composition, and handoff rules.

## Non-Negotiables

- Run 4-6 independent judge subagents by default for every non-economy command.
- If subagent tools are unavailable in non-economy mode, mark `JUDGE_PANEL_UNAVAILABLE`; never claim a full pass.
- Do not soften judge feedback with praise padding.
- Do not replace one generic aesthetic with another.
- Do not ship purple-blue gradients, glass cards, card soup, vague copy, fake proof, motion spam, token chaos, or brandless layouts unless the product context specifically justifies them.
- Do not generate UI in `--prevent` until the detector and judge panel have approved a design contract.
- Do not finish `--fix` or `--redesign` with failed judge gates. Iterate. If the gate still fails, block the result and state why.
- At the end of `--fix` or `--redesign`, load the sibling skill `skills/reality-skill/SKILL.md` when the target includes an app, dashboard, form, CRUD flow, onboarding, checkout, settings, auth-like flow, fake proof, fake data, or primary actions. Use it to remove demoware without broad redesign.
- Preserve behavior, accessibility, semantic structure, focus states, keyboard access, and responsive stability.
- Use existing design tokens and component conventions when they are coherent. Replace them only when they are the problem.
- For operational tools, prefer dense, scan-friendly, restrained interfaces. For expressive products, create a deliberate art direction, not decoration.

## Required State

Maintain this state throughout the workflow:

```text
command:
target:
mode:
economy_mode:
preset:
dials:
slop_score_before:
slop_score_after:
slop_signatures:
autopsy_report:
issues_by_severity:
design_direction:
judge_panel:
judge_gate:
files_changed:
verification:
reality_handoff:
reality_changes:
```

## Local CLI Helper

For a deterministic local scan, run:

```bash
python no-slop/scripts/no_slop_cli.py --scan <target>
python no-slop/scripts/no_slop_cli.py --autopsy <target>
python no-slop/scripts/no_slop_cli.py --prevent "brief text" --autopsy
python no-slop/scripts/no_slop_cli.py --preset dashboard --dial STRICTNESS=10 --scan <target>
```

The CLI supports scoring, dials, presets, signatures, economy mode, autopsy reporting, and a deterministic judge-gate summary. The Codex skill workflow remains the authority for actual code edits and live subagent judging.
