# Interaction Playbook

Use this playbook when editing controls, forms, states, mobile behavior, keyboard paths, motion, and perceived performance.

## Controls

- Use native controls where possible.
- Use proven accessible primitives for dialogs, menus, comboboxes, listboxes, tabs, popovers, toasts, and tooltips.
- Icon-only controls need accessible names and visible hover/focus affordance.
- Destructive actions must name the affected object and provide confirmation, undo, or recovery proportional to impact.
- Disabled controls need a visible reason when users are likely to try them.

## Forms

Minimum form quality:

- visible label for every input
- hint text only for constraints, examples, or consequences
- placeholder never as the only label
- required/optional clarity where useful
- local validation when constraints are known
- server errors mapped back to the relevant fields
- preserved input after failure
- focus placed on the first meaningful error or summary
- submit disabled only when the reason is obvious or explained
- success state tied to committed data

Validation message shape:

```text
[Field/action] needs [specific fix] because [constraint/consequence].
```

Keep messages human and specific. Avoid blaming the user.

## Feedback And State

Every primary action needs one of:

- instant state change
- pending/submitting state
- progress for long work
- optimistic state with rollback path
- success confirmation tied to object/result
- error with retry/recovery

State inventory:

- initial
- loading
- empty
- partial/stale
- validation error
- system error
- disabled/unavailable
- success
- long content
- small screen
- keyboard focus

## Keyboard And Focus

- Tab order follows visual/task order.
- Focus is visible and not color-only.
- Modal/dialog focus is trapped only while open and restored after close.
- Menus, listboxes, tabs, comboboxes, and grids follow expected keyboard patterns.
- Escape closes temporary surfaces when safe.
- Enter/Space activate controls according to native behavior.
- Do not create clickable `div`/`span` without role, tab index, keyboard events, and accessible name. Prefer `button` or `a`.

## Mobile

- Avoid hover-only discovery.
- Keep primary actions reachable and not hidden behind decorative content.
- Ensure text and controls wrap instead of clipping.
- Use stable dimensions for fixed toolbars, tabs, grids, and media.
- Inputs should use appropriate keyboard types where the stack supports them.
- Avoid `100vh` traps and horizontal overflow.

## Motion

Motion must clarify:

- causality
- transition
- loading/progress
- spatial relationship
- attention to a changed state

Block:

- animation that delays task completion
- endless decorative motion near controls
- large layout movement during reading or input
- no reduced-motion fallback

## Performance Feel

- Reserve space for media, tables, skeletons, and async content.
- Keep input response fast.
- Use skeletons only when they resemble final structure.
- Prefer progressive rendering when data can arrive in parts.
- Avoid heavy blur/filter/backdrop effects in dense workflows.
- Tell users what is happening when work takes more than a moment.

## Recovery

Every failure should answer:

- What happened?
- Did my data survive?
- What can I do next?

Useful controls:

- Retry
- Edit
- Cancel
- Back
- Undo
- Restore
- Reconnect
- Download/copy local fallback
- Contact/support path when genuinely needed

