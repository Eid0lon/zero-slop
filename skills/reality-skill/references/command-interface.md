# Command Interface

Use this file to parse explicit `reality` commands and choose the safest workflow.

## Grammar

```text
reality [mode] [target-or-brief] [flags]
```

Modes:

- `--audit`, `-a`: inspect and report reality blockers without editing unless the user also asks to fix.
- `--fix`, `-f`: implement the smallest changes that make the primary workflow finishable.
- `--build`, `-b`: create or extend an app by designing the real workflow model before UI/code.
- `--harden`: improve reliability, state coverage, validation, persistence, recovery, and edge cases.
- `--judge`, `-j`: score the app against the gates and block shipping if core workflow gates fail.
- `--verify`: run proof only: tests, build, browser path, persistence, responsive checks.

Flags:

- `--strict`: treat sample data, unverified actions, fake charts, and disabled missing integrations as blockers unless explicitly scoped.
- `--prototype`: allow local storage or fixture mode, but require honest UI labels and no production claims.
- `--no-browser`: skip browser checks only when the user requested it or the app cannot run.
- `--scope <job>`: focus on a specific workflow/job.
- `--economy`, `-e`: skip live judge agents if available; still use deterministic checks.

## Precedence

1. Explicit user instruction wins.
2. Existing UI plus action/fix language routes to `--fix`.
3. Existing UI plus review/audit language routes to `--audit`.
4. New app/tool/dashboard language routes to `--build`.
5. Regression, QA, production, launch, or "make it solid" routes to `--harden`.
6. "Is this real?", "judge", or "review reality" routes to `--judge`.

## Output Contracts

Audit:

```text
Primary job:
Reality score:
Blocking gates:
Dead/fake elements:
Missing states:
Persistence gap:
Truth boundary issues:
Recommended fix path:
```

Fix/build/harden:

```text
Primary job:
Implemented workflow:
Files changed:
Reality gates closed:
Verification:
Remaining fake boundaries:
Ship decision:
```

Judge:

```text
Reality score:
Gate failures:
Workflow proof:
Data/truth proof:
State/persistence proof:
Required changes:
Ship decision:
```

## Reporting Rule

Never use `Remaining fake boundaries: None` unless every relevant fake boundary is implemented, disabled, or honestly labeled in both code and UI.

