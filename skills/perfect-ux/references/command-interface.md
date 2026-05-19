# Command Interface

Perfect UX accepts command-like invocations. Treat user text after `perfect-ux` as arguments.

## Grammar

```text
perfect-ux [mode] [target-or-brief] [options]

mode:
  -c | --contract
  -m | --map
  -a | --audit
  -f | --fix
       --harden
  -j | --judge
       --verify

options:
  -e | --economy
  --preset <name>
  --dial NAME=0..10
  --json
  --no-write
```

## Mode Precedence

When multiple modes appear, use:

1. `--verify`
2. `--judge`
3. `--harden`
4. `--fix`
5. `--audit`
6. `--map`
7. `--contract`

Default:

- Existing UI target: `--audit`.
- Editable user request on an existing target: `--fix`.
- Brief only: `--contract`.

`--no-write` is accepted for compatibility with agent command contracts. The local helper is read-only; actual edits happen only through the skill workflow after the user asks for fix, harden, or build work.

## Presets

See `dials-and-presets.md`.

Common:

```bash
perfect-ux --contract "incident response dashboard for SREs" --preset dashboard
perfect-ux --audit src/app --preset operational-saas
perfect-ux --fix app/settings --dial ERROR_RECOVERY=10
perfect-ux --harden src/ai-workbench --preset ai-tool
perfect-ux --audit src --json
```

## Economy Mode

`-e` or `--economy` disables live subagent judges. It does not lower standards. Mark results as `ECONOMY_REVIEW`.

Do not silently enable economy mode.

## Output Contracts

### Contract

```markdown
# UX Contract
Status:
Preset:
Dials:

## User And Job
## Journey
## States And Recovery
## Trust And Evidence
## Gates
```

### Map

```markdown
# Journey Map
Target:
Primary job:

## Entry Points
## Decisions
## Actions
## Feedback
## Failure And Recovery
## Evidence Gaps
```

### Audit / Fix / Harden

```markdown
# Perfect-UX Result
Target:
Mode:
UX score before:
UX score after:
Judge gate:

## Changed
## Friction Removed
## Evidence
## Blockers
```

### Judge

```markdown
# Perfect-UX Judge Panel
Gate:
Panel average:
Lowest score:

## Judges
## Required Improvements
```

### Verify

```markdown
# UX Verification
Build:
Lint:
Typecheck:
Tests:
Browser journey:
Keyboard:
Accessibility:
Responsive:
Performance feel:
Remaining risk:
```

