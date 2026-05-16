# Step 03: No-Slop Gate

## Objective

Use `no-slop` as the anti-generic gate after the premium design pass.

## Actions

1. Load `references/no-slop-integration.md`.
2. If `no-slop` exists locally, run or emulate its scan on changed UI files.
3. If it finds blockers, fix them before judging premium quality.
4. If `no-slop` is unavailable, record `NO_SLOP_UNAVAILABLE` and perform the local anti-generic checklist from `no-slop-integration.md`.

## Failure Handling

Fix immediately when any of these remain:

- generic hero/layout formula
- vague CTA/copy
- decorative gradient/glass/card soup
- fake proof or placeholder content
- token chaos
- accessibility blocker
- mobile overflow or text overlap

## Output

```markdown
# No-Slop Gate

Before:
After:
Gate:
Blockers:
```

## Next Step

Load `step-04-judge.md`.
