# Verification Playbook

## Code Verification

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

If a command is missing, record `not available`.

## Browser Verification

When a dev server can run:

- Desktop: inspect the primary viewport.
- Mobile: inspect narrow viewport around 375px.
- Check text fit in buttons, tabs, cards, badges, toolbars, and fixed-format elements.
- Check hover/focus/active/disabled/loading/empty/error/success states.
- Check keyboard flow.
- Check reduced motion if animations exist.
- Check images/media render, maintain aspect ratio, and do not shift layout.
- Check that no decorative layer obscures text.

If the in-app browser blocks local `file://` or `localhost` URLs, do not silently downgrade the review. Use the safest available rendered fallback, such as approved headless Chrome screenshots, and record the limitation. A deterministic scanner pass is not visual proof.

## Mobile Screenshot Gate

Block completion when a mobile screenshot around `390px` wide shows:

- clipped status lines, alert text, command hints, tabs, buttons, or filters
- horizontal page overflow
- controls wider than the viewport
- action labels truncated inside buttons
- a selected row/card that hides its metadata or status
- any evidence pane, log line, or incident action that cannot be reached by vertical scroll

Fix with wrapping, responsive grid changes, shorter copy, `min-width: 0`, `overflow-wrap`, and stable control dimensions. Do not hide overflow to fake a pass.

## Visual Evidence

Capture screenshots when tooling exists and store them near task artifacts only when useful.

## Accessibility Evidence

Minimum manual checks:

- Keyboard reaches every interactive control.
- Visible focus on all interactive controls.
- Icon buttons have accessible names.
- Inputs have labels.
- Status is not color-only.
- Contrast is plausible and must be measured when uncertain.

## Final Risk Statement

Always name:

- tests run
- tests unavailable
- browser checks run
- remaining limitations
