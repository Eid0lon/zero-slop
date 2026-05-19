# Verification Playbook

Verification proves the user can complete the job. It is not just a build check.

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
python skills/perfect-ux/scripts/perfect_ux_cli.py --audit <target>
python skills/no-slop/scripts/no_slop_cli.py --scan <target>
python skills/reality-skill/scripts/reality_cli.py --audit <target>
```

If a command is missing, record `not available`.

## Browser Journey Verification

When a dev server can run:

1. Start at the real entry point.
2. Complete the primary job with valid data.
3. Trigger invalid input and confirm inline recovery.
4. Trigger or inspect loading/empty/error/success/disabled states where feasible.
5. Confirm input survives errors.
6. Confirm keyboard-only path.
7. Inspect focus order and focus visibility.
8. Inspect mobile width around `375px` to `390px`.
9. Confirm no text, controls, menus, alerts, or panels overlap or clip.
10. Check that slow work has feedback and no surprise layout shift.

## Accessibility Evidence

Minimum checks:

- Keyboard reaches every interactive control.
- Visible focus on all interactive controls.
- Inputs have labels.
- Icon buttons have accessible names.
- Dialog/menu/tab/listbox patterns are operable by keyboard.
- Status is not color-only.
- Motion respects reduced-motion when animation exists.
- Touch targets are plausible on mobile.
- Contrast is measured when uncertain.

## Task Evidence

Record:

- scenario tested
- start point
- data entered
- success condition reached
- recovery path tested
- browser/viewport used
- failures found and fixed

## Performance Feel

Inspect:

- input latency
- layout shift around primary controls
- skeleton/media dimensions
- long waits without feedback
- heavy animation or blur near task-critical content

## Final Risk Statement

Always name:

- checks run
- checks unavailable
- browser journey result
- remaining user harm risk

