# No-Slop Integration

Perfect Design and `no-slop` are separate gates.

- `no-slop`: detects and removes generic AI UI residue.
- `perfect-design`: creates and verifies a premium product-specific direction.

Use both whenever possible.

## Sequence

1. Perfect Design contract.
2. `no-slop` pre-scan when target exists.
3. Design/edit pass.
4. `no-slop` post-scan.
5. Premium judge panel.
6. Browser/build/accessibility verification.

## Local Detection

If the sibling skill exists in this repo:

```bash
python no-slop/scripts/no_slop_cli.py --scan <target>
```

If installed elsewhere, invoke the available `no-slop` skill or command.

## Hard Failures

Do not mark Perfect Design complete when `no-slop` still finds:

- critical accessibility issue
- fake proof or placeholder production content
- primary workflow unclear
- heavy card soup
- generic hero stack
- vague CTAs/copy
- token collapse
- mobile overlap

## When `no-slop` Is Unavailable

Record:

```text
NO_SLOP_UNAVAILABLE
```

Then run the local checklist:

- Is the first viewport product-specific?
- Is copy specific enough that competitors could not use it unchanged?
- Are tokens semantic and coherent?
- Are cards/components necessary?
- Is motion purposeful?
- Are screenshots/data/assets real or explicitly demo?
- Does mobile fit?
- Is keyboard/focus intact?

This is not a full `no-slop` pass.
