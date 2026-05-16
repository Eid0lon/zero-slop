# Step 04: Judge

## Objective

Use the strict multi-agent panel to decide whether the output is acceptable.

## Actions

1. Load `references/judge-system.md`.
2. If economy mode is true:
   - Do not launch subagents.
   - Produce the six-role self-judge table.
   - Mark gate as `ECONOMY_REVIEW`.
3. If economy mode is false:
   - Launch 4-6 judges in parallel.
   - Use all six judges for redesign and prevent.
   - Give each judge only the target, mode, dials, scan summary, relevant files, and screenshots if available.
   - If subagent tools are unavailable, mark gate as `JUDGE_PANEL_UNAVAILABLE`; do not mark `PASS`.
4. Aggregate:
   - panel average
   - lowest judge
   - hard blockers
   - required improvements
5. Apply gate formula from `dials-and-presets.md`.

## Gate Outcomes

- `PASS`: proceed to verification/final.
- `FAIL_FIXABLE`: return to `step-03-remediate.md` for another focused pass.
- `BLOCKED`: stop and state exact blockers.
- `ECONOMY_REVIEW`: continue only with explicit note that full subagent judging was disabled.
- `JUDGE_PANEL_UNAVAILABLE`: stop or rerun explicitly with `--economy`; never call it a full pass.

## Output

```markdown
# Judge Panel

Gate:
Panel average:
Lowest judge:
Allowed slop score:
Hard blockers:

## Judges
- name: score/10 - verdict - blockers

## Required Improvements
- ordered list
```

## Next Step

- If gate passes or economy review is acceptable, load `step-05-verify.md`.
- If gate fails and mode is `fix` or `redesign`, return to `step-03-remediate.md`.
- If gate fails in `scan`, report findings and stop.
- If gate fails in `prevent`, revise the prevention contract or block generation.
- If gate is `JUDGE_PANEL_UNAVAILABLE`, stop and name the missing capability.
