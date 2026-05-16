# Step 05: Verify

## Objective

Prove the UI is premium in code and in the browser when possible.

## Required Checks

Run only commands that exist:

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
- Capture screenshots.
- Check first viewport framing.
- Check visual hierarchy and product proof.
- Check text overflow, overlap, and clipping.
- Treat clipped status lines, command strips, tabs, filters, and action labels on mobile as blockers.
- Check hover, focus, active, disabled, loading, empty, error, and success states.
- Check keyboard navigation for the primary flow.
- Check reduced-motion behavior when motion exists.
- Check that media has stable dimensions.

## Re-Scan

Compare:

```markdown
Premium score before:
Premium score after:
No-slop before:
No-slop after:
Judge gate:
```

## Final Output

```markdown
# Perfect-Design Complete

Target:
Mode:
Preset:
Dials:

## Result
- Design thesis:
- Premium score:
- No-slop gate:
- Judge gate:

## Changed
- file - concise summary

## Verification
- Build:
- Lint:
- Typecheck:
- Tests:
- Browser:
- Accessibility:

## Remaining Risk
- item or "None known"
```
