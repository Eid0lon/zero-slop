# Self-Coaching

Use this when stuck, when the UX feels "fine" but not excellent, or when deciding between several improvements.

## Reframe

Ask:

- What job is this screen actually helping complete?
- What does the user know at this moment?
- What are they afraid of breaking, losing, paying, sharing, or misunderstanding?
- What would they do next if they were interrupted?
- What would they do if the system failed?
- What would a keyboard-only user hit first?
- What would be confusing on a phone at 390px?
- What user support question does this UI create?

## Reduce Before Adding

Before adding a tooltip, instruction, modal, or new control, try:

- clearer label
- closer help text
- better grouping
- fewer same-weight actions
- visible state
- better default
- progressive disclosure
- inline validation
- preserving context

## Evidence Over Taste

When two directions compete:

- choose the one that makes the next action clearer
- choose the one that preserves user data
- choose the one that makes error recovery easier
- choose the one that is accessible with less custom code
- choose the one that can be verified

## Common False Passes

- It looks polished but the action outcome is unclear.
- It has a form but no validation/recovery.
- It has a dashboard but no decision path.
- It has AI output but no review/source/uncertainty boundary.
- It has a loading state but no failure state.
- It has a mobile layout but controls clip or reorder the journey badly.
- It has accessible-looking components but custom keyboard behavior is broken.
- It has analytics events but no task success metric.

## Final Challenge

Write this sentence:

```text
A user can now [job] from [start] to [completion], and if [failure] happens they can [recovery] without losing [context/data].
```

If the sentence is false or vague, keep working.

