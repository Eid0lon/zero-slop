# Command Interface

No Slop accepts command-like invocations. Treat user text after `no-slop` as arguments.

## Grammar

```text
no-slop [mode] [target] [options]

mode:
  -s | --scan
  -f | --fix
  -r | --redesign
  -j | --judge
       --prevent

options:
  -e | --economy
  --preset <name>
  --dial NAME=0..10
  --json
  --no-write
```

`target` defaults to the current workspace directory. If the target is a file, inspect the file and its nearest related styles/components. If the target is a directory, discover relevant frontend files with `rg --files`.

## Mode Precedence

When multiple modes appear, use this precedence:

1. `--prevent`
2. `--redesign`
3. `--fix`
4. `--judge`
5. `--scan`

Judge behavior is a gate, not just a command. In all non-economy modes, run the judge panel even when `--judge` is not explicitly present.

## Economy Mode

`-e` or `--economy` disables subagent judges. It does not lower standards. It replaces the multi-agent panel with the local rubric, deterministic scan, and a self-critique pass.

`--no-write` is accepted for compatibility with agent command contracts. The local helper is already read-only; actual edits are performed only by the skill workflow when the user requested fix/redesign work.

Use economy mode when:

- The user explicitly asks for speed or token savings.
- The target is tiny and visual risk is low.
- Tools cannot launch subagents.

Do not silently enable economy mode.

## Dials

Each dial is an integer from 0 to 10. Load `dials-and-presets.md` before applying them.

Examples:

```bash
no-slop --scan --preset dashboard
no-slop --fix --dial STRICTNESS=10 --dial MOTION_INTENSITY=1
no-slop --prevent --preset ecommerce --dial COPY_PRECISION=10
```

Invalid dial names or values are hard errors. Do not guess.

## Output Contracts

### Scan

```markdown
# no-slop Scan

Target:
Preset:
Dials:
Economy:
AI-slop score:
Slop signatures:
Judge gate:

## Findings
### Critical
### High
### Medium
### Low

## Category Breakdown
| Category | Count | Score |
```

### Fix or Redesign

```markdown
# no-slop Result

Target:
Mode:
Design direction:
Score before:
Score after:
Judge gate:

## Changed
- file - change

## Evidence
- command/check - result

## Blockers
- issue or "None"
```

### Judge

```markdown
# no-slop Judge Panel

Gate:
Panel average:
Lowest score:

## Judges
- Judge name: score/10, verdict, blockers

## Required Improvements
- ordered by severity
```

### Prevent

```markdown
# no-slop Prevention Contract

Status:
Preset:
Dials:
Forbidden defaults:
Required design direction:
Judge gate:

## Before Code
- decisions that must be satisfied
```
