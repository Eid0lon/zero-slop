# Step 03: Improve

## Objective

Make the smallest coherent changes that improve the user's chance of completing the job with clarity, accessibility, recovery, and trust.

## Actions

1. Choose scope:
   - `fix`: remove blockers and high-friction defects.
   - `harden`: add resilience, edge states, keyboard paths, measurement hooks, and recovery.
2. Use existing project primitives first.
3. Edit in this order:
   1. Completion blockers and dead ends.
   2. Data loss and error recovery.
   3. Accessibility, keyboard, focus, labels, and semantics.
   4. Decision clarity, IA, labels, and microcopy.
   5. Feedback states and performance feel.
   6. Trust boundaries and unsupported claims.
   7. Expert efficiency and repeated-use speed.
4. Compose with sibling skills:
   - `reality-skill` for real actions/data/persistence.
   - `perfect-design` for broad layout/visual changes.
   - `no-slop` before and after material UI changes.
5. Preserve behavior unless the behavior is the UX defect.
6. Add tests when changing validation, state transitions, persistence, routing, or destructive actions.
7. Re-run deterministic precheck after edits:

```bash
python skills/perfect-ux/scripts/perfect_ux_cli.py --audit <target>
```

## Output

```markdown
# UX Improvement Pass
Primary job:

## Changed
- file - change

## Friction Removed
- user harm - fix

## Prechecks
- command - result
```

## Next Step

Load `step-04-judge.md`.

