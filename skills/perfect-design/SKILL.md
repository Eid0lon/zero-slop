---
name: perfect-design
description: Premium UI design engineering skill for creating, redesigning, polishing, and judging product-specific interfaces with senior-level craft. Use when Codex works on frontend design, UX/UI, design systems, dashboards, SaaS apps, landing pages, commerce, portfolios, visual polish, interaction quality, or wants output in the spirit of Vercel, Linear, Raycast, Awwwards, and high-end product teams. Composes with no-slop as the anti-generic gate.
---

# Perfect Design

Perfect Design is the premium design layer. `no-slop` removes generic AI residue; Perfect Design creates a coherent, product-specific interface that feels designed by a senior design engineer.

## Command Interface

Use `references/command-interface.md`.

Primary commands:

```bash
perfect-design --contract [brief-or-target]
perfect-design --create [brief-or-target]
perfect-design --redesign [target]
perfect-design --polish [target]
perfect-design --judge [target]
perfect-design --verify [target]
perfect-design -e --polish [target]
```

Short flags:

- `-c`, `--contract`: write the design contract before code.
- `--create`: build a new UI surface from a brief.
- `-r`, `--redesign`: rebuild direction, layout, tokens, copy, and interaction.
- `-p`, `--polish`: refine an existing surface without changing the product model.
- `-j`, `--judge`: run the brutal premium judge panel.
- `--verify`: prove the result in code and browser when possible.
- `-e`, `--economy`: disable live subagent judges only when the user explicitly accepts a lower-cost review.

Default mode:

- Existing UI target: `--polish`.
- Brief without target: `--contract`.

## First Action

Load `steps/step-00-command-router.md`.

Step 00 parses command flags, discovers project shape, loads the right references, and routes to contract, create, redesign, polish, judge, or verify.

## Core References

Load only what the task needs:

- `references/command-interface.md`: grammar, precedence, output contracts.
- `references/dials-and-presets.md`: premium craft dials and archetype presets.
- `references/research-synthesis.md`: distilled research from Vercel, Linear, Raycast, Awwwards, WCAG, Baymard, Polaris, Radix, web.dev, Resend, Supabase, and related sources.
- `references/design-contract.md`: pre-code contract structure and rejection rules.
- `references/product-archetypes.md`: domain-specific design expectations.
- `references/composition-playbook.md`: layout, hierarchy, typography, color, tokens, imagery, and visual rhythm.
- `references/interaction-accessibility.md`: keyboard, focus, states, motion, performance, and responsive stability.
- `references/no-slop-integration.md`: how to combine Perfect Design with `no-slop`.
- `references/legacy-boundary.md`: proof that `old-perfect-design` is intentionally outside the editable scope.
- `references/judge-system.md`: mandatory brutal judge protocol and gate formula.
- `references/premium-quality-rubric.md`: scoring rubric and ship gates.
- `references/self-coaching.md`: the internal checklist to use when stuck.
- `references/verification-playbook.md`: build/browser/accessibility/visual proof.

## Non-Negotiables

- Always write or infer a Design Contract before generating or rewriting UI.
- Always identify the user, job, domain expectation, design thesis, proof/data/media, and primary workflow.
- Always inspect existing tokens, components, layouts, content, and states before editing.
- Compose with `no-slop` whenever available. Run it before and after material UI work, or mark `NO_SLOP_UNAVAILABLE`.
- Do not stop at removing cliches. Replace them with clear product decisions.
- Do not use "premium", "clean", "modern", "beautiful", or "sleek" as design direction. Translate style words into concrete type, spacing, density, palette, material, copy, motion, and state decisions.
- Do not make a landing page unless the user asked for marketing. Build the actual usable surface first.
- Do not hide the product, object, place, app, game, state, or primary task in the first viewport.
- Do not ship card soup, decorative gradients, stock-like blobs, fake proof, vague CTAs, or motion without purpose.
- For operational tools, prefer dense, scan-friendly, restrained interfaces. For expressive/editorial work, create a deliberate art direction with strong content rhythm.
- Preserve behavior, accessibility, semantics, keyboard access, focus visibility, responsive stability, and performance.
- Use proven primitives for difficult interaction patterns when the stack provides them.
- Judge with subagents by default. If live judges are unavailable and economy mode is false, mark `JUDGE_PANEL_UNAVAILABLE`; never claim a full pass.
- Iterate until the premium gate passes. If blocked, state exact blockers.

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
user:
primary_job:
design_thesis:
design_contract:
no_slop_before:
premium_score_before:
files_changed:
judge_panel:
judge_gate:
verification:
no_slop_after:
premium_score_after:
remaining_risk:
```

## Local CLI Helper

For deterministic prechecks:

```bash
python perfect-design/scripts/perfect_design_cli.py --contract "brief text"
python perfect-design/scripts/perfect_design_cli.py --audit <target>
python perfect-design/scripts/perfect_design_cli.py --preset dashboard --dial CRAFT_STRICTNESS=10 --audit <target>
```

Wrappers are provided in `bin/perfect-design` and `bin/perfect-design.ps1`. The CLI is a precheck, not a replacement for the Codex workflow, live browser review, or subagent judging.
