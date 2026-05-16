# Step 04: Judge

## Objective

Run a brutal premium judge panel that decides whether the result feels senior, product-specific, and shippable.

## Actions

1. Load `references/judge-system.md`.
2. If economy mode is true:
   - Do not launch subagents.
   - Produce the local six-role judge table.
   - Mark gate as `ECONOMY_REVIEW`.
3. If economy mode is false:
   - Launch 4-6 independent judges in parallel.
   - Use all six judges for create/redesign or high-risk surfaces.
   - Give judges only the target, contract, changed files, screenshots if available, mode, preset, dials, and no-slop summary.
   - Ask for harsh blockers, not encouragement.
4. Aggregate:
   - panel average
   - lowest score
   - hard blockers
   - required improvements
5. If the gate fails and the task is editable, return to `step-02-design.md` for a focused pass.

## Gate Outcomes

- `PASS`: proceed to verification.
- `FAIL_FIXABLE`: improve and rejudge.
- `BLOCKED`: stop and state exact blockers.
- `ECONOMY_REVIEW`: state that live judges were disabled.
- `JUDGE_PANEL_UNAVAILABLE`: never claim full pass.

## Output

```markdown
# Perfect-Design Judge Panel

Gate:
Panel average:
Lowest score:
Hard blockers:

## Judges
- name: score/10 - verdict - blockers

## Required Improvements
- ordered list
```

## Next Step

If gate passes or economy review is acceptable, load `step-05-verify.md`.
