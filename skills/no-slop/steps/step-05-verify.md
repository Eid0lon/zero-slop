# Step 05: Verify

## Objective

Prove that the UI improved and still works.

## Required Checks

Run only commands that exist in the project:

```bash
npm run lint
npm run typecheck
npm run build
npm test
pnpm lint
pnpm typecheck
pnpm build
pnpm test
```

Do not invent missing scripts.

## Visual Checks

When a local app/server can run:

- Open desktop viewport.
- Open mobile viewport.
- Capture screenshots if tooling is available.
- Check first viewport framing.
- Check text overflow and overlap.
- Check hover, focus, active, disabled, loading, empty, error, and success states.
- Check keyboard navigation for the primary flow.
- Check reduced-motion behavior when motion exists.

If browser tooling is unavailable, inspect code and state the limitation.

## Re-Scan

Re-run relevant scan commands on changed files.

Compare:

```markdown
AI-slop score before:
AI-slop score after:
Score reduction:
Critical before/after:
High before/after:
Medium before/after:
Low before/after:
```

## Final Output

```markdown
# no-slop Complete

Target:
Mode:
Preset:
Dials:

## Result
- Before:
- After:
- Judge gate:

## Changed
- file - concise summary

## Verification
- Build:
- Lint:
- Typecheck:
- Tests:
- Visual:
- Accessibility:

## Remaining Risk
- item or "None known"
```
