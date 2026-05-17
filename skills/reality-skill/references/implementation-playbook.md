# Implementation Playbook

Use existing project patterns first. This playbook is for choosing the smallest implementation that makes the workflow real.

## 1. Build The Product Model

Before UI edits, define:

- entity names and fields
- allowed statuses
- primary actions
- validation constraints
- persistence target
- error types
- success result

If the project has schemas, API types, database models, forms, routes, or stores, extend those rather than duplicating data structures in the component.

## 2. Prefer A Workflow State Machine

For complex flows, represent states explicitly:

```text
idle -> editing -> validating -> submitting -> succeeded
                         |          |
                         v          v
                     invalid     failed -> retrying
```

Use simple component state for small flows and reducers/state machines for multi-step flows. Avoid invisible boolean soup when states are mutually exclusive.

## 3. Make Actions Commit Real Changes

Action implementation checklist:

- read user input from controlled form/state
- validate before commit
- prevent duplicate submit
- call existing API/store or local adapter
- update the source of truth
- show progress
- show success tied to committed result
- preserve user input on failure
- expose retry/cancel/back path

## 4. Add Persistence At The Right Layer

Server app:

- use existing route handlers, loaders, actions, database clients, query clients, or service modules
- preserve cache invalidation conventions
- surface API failures in UI

Client prototype:

- use local storage/IndexedDB through a small adapter
- version stored objects
- guard JSON parse failures
- seed sample data only when no user data exists
- label sample mode when it affects user trust

Do not scatter raw storage calls through many components if a store/service layer already exists.

## 5. Use Honest Mock Boundaries

Acceptable local boundaries:

- `Sample data` for illustrative records.
- `Local draft` for browser-only saved data.
- `Sandbox mode` for simulated integrations.
- `Mock response` for non-production API stand-ins used in dev.
- Disabled controls with a reason, such as `Connect requires API credentials`.

Unacceptable boundaries:

- fake production success
- fake payments
- fake auth/security/compliance
- fake analytics
- fake customer proof

## 6. Make Data Operational

For every visible dataset, provide at least one meaningful operation:

- create/edit/delete records
- filter/sort/search
- drill into detail
- select and bulk act
- export real current data or disable export
- explain metric source and time range

Decorative data without operations is usually a template smell.

## 7. Validation Pattern

Good validation:

- runs before submit
- appears near the field
- uses plain language
- keeps focus and input
- blocks impossible values
- allows optional empty values intentionally
- mirrors server errors when applicable

Do not rely only on browser alerts, color, or disabled submit with no explanation.

## 8. Recovery Pattern

Every workflow failure should answer:

- what failed?
- did user data survive?
- what can the user do next?

Common recovery controls:

- Retry
- Edit input
- Cancel
- Back to list
- Restore/Undo
- Reconnect
- Download local copy

## 9. Destructive Actions

Use confirmation, undo, soft-delete, or clear preview depending on impact.

Minimum behavior:

- name the item being deleted/changed
- prevent accidental double-submit
- update source of truth
- provide success/error feedback
- preserve a recovery route where reasonable

## 10. Exports And Imports

Export is real only if it produces a file/string with current data. Import is real only if it parses, validates, previews errors, and commits accepted data.

If not implemented, disable and label it.

## 11. Browser Verification Path

For frontend changes, manually walk the app like a user:

1. Start from first visible entry point.
2. Complete the primary action with valid data.
3. Try invalid data and confirm inline errors.
4. Refresh and confirm persistence.
5. Trigger or simulate empty/error state when feasible.
6. Use keyboard for the main path.
7. Inspect mobile width for overlap or unusable controls.

