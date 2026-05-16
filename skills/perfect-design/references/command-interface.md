# Command Interface

Perfect Design accepts command-like invocations. Treat user text after `perfect-design` as arguments.

## Grammar

```text
perfect-design [mode] [target-or-brief] [options]

mode:
  -c | --contract
       --create
  -r | --redesign
  -p | --polish
  -j | --judge
       --verify

options:
  -e | --economy
  --preset <name>
  --dial NAME=0..10
  --audit
  --json
  --no-write
```

## Mode Precedence

When multiple modes appear, use:

1. `--verify`
2. `--judge`
3. `--redesign`
4. `--create`
5. `--polish`
6. `--contract`

Default:

- Existing UI target: `--polish`.
- Brief only: `--contract`.

`--no-write` is accepted for compatibility with agent command contracts. The local helper is read-only; actual edits happen only through the skill workflow after the user requests create, redesign, or polish work.

`--audit` is the deterministic helper mode for source prechecks. It maps to the same workflow posture as `--polish`, but it does not imply file edits.

## Presets

See `dials-and-presets.md`.

Common:

```bash
perfect-design --create "AI research workspace for policy analysts" --preset operational-saas
perfect-design --redesign app/page.tsx --preset developer-tool
perfect-design --polish src --preset dashboard --dial DENSITY=8
perfect-design --audit src --json
```

## Economy Mode

`-e` or `--economy` disables live subagent judges. It does not lower standards. Mark results as `ECONOMY_REVIEW`.

Do not silently enable economy mode.

## Output Contracts

### Contract

```markdown
# Design Contract
Status:
Preset:
Dials:
No-slop precheck:

## Product
## Direction
## Gates
## Forbidden
```

### Create / Redesign / Polish

```markdown
# Perfect-Design Result
Target:
Mode:
Design thesis:
Premium score before:
Premium score after:
No-slop gate:
Judge gate:

## Changed
## Evidence
## Blockers
```

### Judge

```markdown
# Perfect-Design Judge Panel
Gate:
Panel average:
Lowest score:

## Judges
## Required Improvements
```

### Verify

```markdown
# Verification
Build:
Lint:
Typecheck:
Tests:
Browser:
Accessibility:
Remaining risk:
```
