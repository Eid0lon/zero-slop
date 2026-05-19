# Step 00: Command Router

## Objective

Parse the request, discover the product surface, resolve UX controls, and route the workflow without loading unnecessary references.

## Actions

1. Parse mode flags:
   - `-c`, `--contract`
   - `-m`, `--map`
   - `-a`, `--audit`
   - `-f`, `--fix`
   - `--harden`
   - `-j`, `--judge`
   - `--verify`
   - `-e`, `--economy`

2. Apply precedence from `references/command-interface.md`.

3. Resolve target:
   - If the target exists, treat it as a UI/code surface.
   - If the target does not exist, treat it as a brief.
   - If omitted, inspect the current workspace.

4. Parse `--preset` and `--dial NAME=VALUE`.
   - Load `references/dials-and-presets.md`.
   - Apply preset first, explicit dials second.
   - Reject unknown dials or values outside `0..10`.

5. Initialize state:

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
scan_surface:
ux_contract:
journey_map:
```

6. Discover project shape:

```bash
rg --files {target}
```

Prioritize `app`, `src`, `pages`, `routes`, `components`, `forms`, `stores`, `services`, `schemas`, `actions`, `api`, `styles`, `theme`, `tokens`, `tests`, and route files.

7. Load references:
   - Always: `research-synthesis.md`, `ux-contract.md`, `ux-gates.md`, `ecosystem-contract.md`.
   - Map/audit/fix/harden: `journey-playbook.md`, `interaction-playbook.md`, `content-and-trust.md`.
   - Research/evidence tasks: `measurement-and-research.md`, `research-source-ledger.md`.
   - Judge: `judge-system.md`.
   - Verification: `verification-playbook.md`.
   - Stuck or ambiguous: `self-coaching.md`.

8. Check sibling skill relevance:
   - Use `perfect-design` when visual direction or layout craft changes.
   - Use `no-slop` before/after material UI work.
   - Use `reality-skill` when actions/data/persistence/integrations must become real.

## Next Step

- Brief or `--contract`: load `step-01-ux-contract.md`.
- `--map`: load `step-01-ux-contract.md`, then `step-02-journey-audit.md`.
- `--audit`: run deterministic precheck if useful, then load `step-02-journey-audit.md`.
- `--fix` or `--harden`: load `step-01-ux-contract.md`, `step-02-journey-audit.md`, then `step-03-improve.md`.
- `--judge`: load `step-04-judge.md`.
- `--verify`: load `step-05-verify.md`.

