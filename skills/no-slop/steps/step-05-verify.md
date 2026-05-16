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

## Reality Skill Handoff

Before final output, decide whether the result needs a reality pass.

Load the sibling skill at `skills/reality-skill/SKILL.md` when any of these are true:

- The target is an app, dashboard, form, CRUD flow, onboarding flow, checkout, settings page, or auth-like flow.
- The remediation touched primary actions, data display, fake proof, fake metrics, forms, navigation, loading/empty/error states, persistence, or user-created content.
- The UI could still be a static demo that only looks complete.

After loading Reality Skill:

1. Identify the primary user job.
2. Run the seven reality gates: Action, Data, State, Persistence, Navigation, Validation, Truth.
3. Modify only what is needed to make the workflow honest and finishable.
4. Keep No Slop's design improvements intact unless they hide fake functionality or block the workflow.
5. Re-run relevant verification after any Reality Skill changes.

Examples of valid Reality Skill edits:

- Wire dead buttons to real local state transitions.
- Replace `href="#"` with real routes, disabled states, or honest unavailable states.
- Add inline validation and submit feedback to forms.
- Add loading, empty, error, disabled, and success states where the workflow needs them.
- Add localStorage or existing-store persistence for user-created prototype data.
- Label sample data honestly or replace fake proof with truthful product evidence.

If the target is a static marketing/content surface with no workflow and no fake proof/data/actions, mark `Reality handoff: Not applicable` and state why.

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
- Reality handoff:

## Remaining Risk
- item or "None known"
```
