# Step 02: Forensic Audit

Audit before editing unless the user explicitly asks for a greenfield build.

## Code Search

Use `rg` for:

```text
href="#"
console.log
alert(
TODO
FIXME
Coming soon
mock
sample
dummy
placeholder
Math.random
setTimeout
localStorage
onClick
disabled
toast
export
connect
pay
invite
generate
save
delete
```

Run `scripts/reality_cli.py` when useful.

## Manual Inspection

Identify:

- the primary job
- every primary action
- data source and write path
- validation path
- persistence path
- empty/loading/error/success states
- navigation/recovery paths
- claims that imply production reality

## Severity

- P0: fake or broken primary workflow, deceptive high-trust claim.
- P1: missing persistence, validation, recovery, or critical state.
- P2: brittle edge case, weak feedback, partial truth label.
- P3: polish-level reality improvement.

Do not bury P0/P1 issues behind cosmetic notes.

