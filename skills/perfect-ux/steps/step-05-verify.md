# Step 05: Verify

## Objective

Prove the primary journey works for a real user under normal, failure, keyboard, mobile, and slow/uncertain conditions.

## Actions

1. Load `references/verification-playbook.md`.
2. Run available code checks:

```bash
npm run lint
npm run typecheck
npm run build
npm test
python skills/perfect-ux/scripts/perfect_ux_cli.py --audit <target>
```

3. When a dev server can run, verify in browser:
   - primary path with valid data
   - invalid data and recovery
   - loading/error/empty/success/disabled states
   - keyboard path
   - focus visibility
   - mobile viewport around 375px to 390px
   - no clipping, overlap, or horizontal overflow
   - performance feel and layout stability
4. Record unavailable checks explicitly.
5. State remaining user harm risk.

## Output

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

## Done Gate

Do not say the UX fully passes unless:

- primary journey completed
- recovery path checked
- accessibility/keyboard checked
- mobile checked
- code checks run when available
- judge gate passed or limitation recorded

