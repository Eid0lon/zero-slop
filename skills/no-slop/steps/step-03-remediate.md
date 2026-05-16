# Step 03: Remediate

## Objective

Apply surgical fixes or a coherent redesign that reduces slop without breaking behavior.

## Actions

1. Load `references/remediation-playbook.md`.
2. Write the design direction block before editing.
3. Choose scope:
   - `fix`: patch the smallest set of files that removes blockers and shared slop sources.
   - `redesign`: rebuild layout, tokens, hierarchy, copy, and motion where the structure itself is slop.
4. Edit according to existing stack conventions.
5. Preserve behavior, semantics, focus, keyboard access, and responsive stability.
6. Avoid unrelated refactors.
7. Re-run detection on changed files.

## Fix Priorities

1. Accessibility blockers, broken mobile, deceptive patterns, fake content.
2. Above-the-fold genericity and unclear product promise.
3. Design token violations.
4. Hierarchy collapse.
5. Brand incoherence.
6. Card/icon/motion/copy cliches.
7. Utility-class and implementation cleanup that prevents recurrence.

## Output

```markdown
# Remediation Log

Design direction:

## Files changed
- path - change

## Issues fixed
- severity/category - before -> after

## Tradeoffs
- remaining issue and reason
```

## Next Step

Load `step-04-judge.md`.
