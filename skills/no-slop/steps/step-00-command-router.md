# Step 00: Command Router

## Objective

Parse the command, resolve strictness controls, load only required references, and route the workflow.

## Actions

1. Parse mode flags:
   - `-s`, `--scan`
   - `-f`, `--fix`
   - `-r`, `--redesign`
   - `-j`, `--judge`
   - `--prevent`
   - `-e`, `--economy`

2. Apply mode precedence from `references/command-interface.md`.

3. Parse target:
   - Use current directory when omitted.
   - Validate existence when target is a path.
   - For a brief in `--prevent`, treat target as generation context rather than a required file.

4. Parse `--preset` and `--dial NAME=VALUE`.
   - Load `references/dials-and-presets.md`.
   - Reject invalid dial names or values.
   - Apply preset first, explicit dials second.

5. Initialize state:

```text
command:
target:
mode:
economy_mode:
preset:
dials:
judge_enabled:
project_type:
scan_surface:
```

6. Discover project shape:

```bash
rg --files {target}
```

Prioritize `app`, `src`, `pages`, `components`, `styles`, `public`, `theme`, `tokens`, and route files.

7. Load references:
   - Always: `ai-slop-patterns.md`, `design-quality-rubric.md`.
   - Dials/presets: `dials-and-presets.md`.
   - Non-economy: `judge-system.md`.
   - Fix/redesign: `remediation-playbook.md`.
   - Prevent: `prevention-protocol.md`.
   - Command ambiguity or handoff: `ecosystem-contract.md`.

## Next Step

- If mode is `prevent`, load `step-02-prevent.md`.
- Otherwise load `step-01-detect.md`.
