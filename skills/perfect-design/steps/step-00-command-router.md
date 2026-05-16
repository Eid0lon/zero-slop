# Step 00: Command Router

## Objective

Parse the request, discover the product surface, resolve craft controls, and route the workflow without loading unnecessary references.

## Actions

1. Parse mode flags:
   - `-c`, `--contract`
   - `--create`
   - `-r`, `--redesign`
   - `-p`, `--polish`
   - `--audit`
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
scan_surface:
design_contract:
no_slop_available:
```

6. Discover project shape:

```bash
rg --files {target}
```

Prioritize `app`, `src`, `pages`, `components`, `styles`, `theme`, `tokens`, `public`, route files, global styles, component libraries, and existing screenshots/assets.

7. Load references:
   - Always: `research-synthesis.md`, `design-contract.md`, `premium-quality-rubric.md`, `no-slop-integration.md`.
   - Create/redesign/polish: `composition-playbook.md`, `product-archetypes.md`, `interaction-accessibility.md`.
   - Judge: `judge-system.md`.
   - Verification: `verification-playbook.md`.
   - Stuck or ambiguous: `self-coaching.md`.

## Next Step

- Brief or `--contract`: load `step-01-contract.md`.
- `--audit`: run deterministic helper prechecks, then load `step-03-no-slop.md` and `step-04-judge.md` if the user asked for a full review.
- Create/redesign/polish: load `step-01-contract.md`, then `step-02-design.md`.
- Judge: load `step-04-judge.md`.
- Verify: load `step-05-verify.md`.
