# Verification Playbook

Reality Skill must prove the workflow, not just compile.

## Baseline Commands

Discover the project first, then choose the local commands that exist:

- package scripts: `npm run`, `pnpm run`, `yarn run`, `bun run`
- typecheck
- lint
- unit tests
- integration/e2e tests
- build
- app-specific smoke commands

Do not invent commands. Read package/config files and use what the repo provides.

## Deterministic Reality Scan

Run when useful:

```bash
python skills/reality-skill/scripts/reality_cli.py --audit <target>
python skills/reality-skill/scripts/reality_cli.py --strict --audit <target>
```

Treat results as leads. Confirm in code before editing or reporting severe failures.

## Browser Proof

For local frontend apps, start the dev server when feasible and verify:

- first viewport shows the real product/task
- primary action path completes
- invalid input shows inline errors
- refresh preserves expected data
- empty/error states are reachable or simulated
- disabled unavailable capabilities explain why
- mobile viewport remains usable
- no text overlap, dead controls, or blank main surfaces

Capture screenshots or describe exact manual proof when screenshot tooling is unavailable.

## Persistence Proof

For user-created data:

1. Create or edit data.
2. Navigate away and back.
3. Refresh the page if browser storage/server persistence is expected.
4. Confirm the data is still present.
5. Confirm sample seed data does not overwrite user data.

## Error Proof

At least one failure path should be checked for the primary workflow:

- invalid form data
- simulated API failure
- missing credential/config
- empty dataset
- duplicate submit prevention

## Accessibility Proof

Minimum checks:

- interactive elements are keyboard reachable
- focus is visible
- form controls have labels
- dialogs/menus do not trap or lose focus incorrectly
- errors are text, not color-only

## Ship Decisions

Use one of:

- `SHIP`: core workflow is real and verified.
- `SHIP_WITH_BOUNDARY`: workflow is usable, with explicitly labeled local/sample/mock boundaries.
- `BLOCKED`: a primary action, truth boundary, persistence path, or verification step still fails.
- `NEEDS_USER_DECISION`: multiple plausible primary jobs or real service credentials are needed.

