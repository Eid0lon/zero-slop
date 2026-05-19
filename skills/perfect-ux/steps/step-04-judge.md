# Step 04: Judge

## Objective

Evaluate whether the changed or audited experience passes the Perfect UX gate.

## Actions

1. Load `references/judge-system.md` and `references/dials-and-presets.md`.
2. Gather evidence:
   - UX Contract
   - journey audit
   - deterministic precheck
   - changed files
   - sibling skill results
   - screenshots or browser walkthrough when available
3. Run 4-6 independent judge subagents unless economy mode is active.
4. Use all six judges for high-risk surfaces:
   - forms
   - checkout
   - onboarding
   - dashboards
   - AI tools
   - settings/auth/billing
   - public services
5. Apply gate:
   - panel average threshold passes
   - lowest judge threshold passes
   - UX score threshold passes
   - no hard blocker exists
   - accessibility and keyboard gates pass
   - verification evidence exists or limitation is recorded

## Output

```markdown
# Perfect-UX Judge Panel
Gate:
Panel average:
Lowest score:

## Judges
## Required Improvements
## Ship Decision
```

## Failure Protocol

For editable modes:

1. Fix hard blockers.
2. Re-run precheck.
3. Re-run judges.
4. Continue until pass or exact blocker.

If subagents are unavailable in non-economy mode, record:

```text
JUDGE_PANEL_UNAVAILABLE
```

Do not claim a full pass.

## Next Step

Load `step-05-verify.md`.

