# Step 02: Journey Audit

## Objective

Map the primary journey and locate the UX friction that blocks comprehension, completion, recovery, accessibility, trust, or repeat efficiency.

## Actions

1. Load `references/journey-playbook.md`, `references/interaction-playbook.md`, `references/content-and-trust.md`, and `references/ux-gates.md`.
2. Trace the primary path:
   - entry
   - orientation
   - information needed
   - decision
   - action
   - feedback
   - completion
   - recovery/return
3. Run deterministic precheck when useful:

```bash
python skills/perfect-ux/scripts/perfect_ux_cli.py --audit <target>
```

4. Inspect for:
   - ambiguous labels and CTAs
   - missing state coverage
   - form and validation defects
   - keyboard/focus risks
   - mobile clipping or order problems
   - trust gaps and unsupported claims
   - dead ends and missing recovery
   - expert-efficiency drag
5. Prioritize by user harm:
   - cannot complete
   - loses data
   - cannot recover
   - excluded by accessibility
   - misled or unsafe
   - slow/repetitive
   - merely unclear

## Output

```markdown
# Journey Audit
Primary job:

## Path
## Blocking Friction
## Missing States
## Trust Gaps
## Evidence Needed
```

## Next Step

- Audit-only: report findings and stop.
- Editable mode: load `step-03-improve.md`.

