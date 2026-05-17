# App Archetypes

Use this file to decide what "real" means for common app types. Pick the closest archetype and add only the expectations relevant to the user's brief.

## CRUD / Admin

Expected workflow:

- list records
- create record
- validate fields
- view details
- edit record
- delete with confirmation or undo
- search/filter/sort when shown
- empty state with create path
- persistence after refresh

Reality blockers:

- table rows cannot be edited
- Add button opens nothing
- filters do not change results
- delete removes only visually
- details page has no return path

## Dashboard / Analytics

Expected workflow:

- choose time range/scope
- inspect labeled metrics
- drill into the underlying items or explanation
- distinguish live, cached, sample, and unavailable data
- handle empty/error/loading states

Reality blockers:

- decorative charts
- random metrics
- fake growth percentages
- no units/time range/source
- no path from metric to action

## Form / Application / Intake

Expected workflow:

- enter data
- validate inline
- save draft when appropriate
- submit
- see confirmation and submitted summary
- recover from failure without losing input

Reality blockers:

- required fields ignored
- submit clears data before commit
- fake success toast
- no error path

## Editor / Builder / Canvas

Expected workflow:

- create or load a document/object
- edit visible content
- undo/recover where appropriate
- save/export/share honestly
- persist work
- handle long content and empty canvas

Reality blockers:

- toolbar controls are decorative
- preview does not reflect edits
- export/download does not produce a file
- save does not persist

## Checkout / Billing

Expected workflow:

- item/cart review
- quantity and price updates
- validation
- explicit payment boundary
- success/failure/cancel states
- no fake charge claims

Reality blockers:

- fake Pay button
- fake card validation
- fake order confirmation
- invented prices/taxes as real

## Auth-Like / Account

Expected workflow:

- explain whether auth is real, demo, or local
- validate credentials fields
- maintain session scope honestly
- support logout/reset path if shown
- do not imply security that does not exist

Reality blockers:

- fake OAuth buttons
- login accepts anything while claiming security
- avatar/team/permissions fabricated as real

## Integration / Connect Flow

Expected workflow:

- show required provider/config
- connect only if real credentials/provider code exists
- otherwise show disabled or local sandbox mode
- handle connected, disconnected, error, retry, revoke

Reality blockers:

- fake Connect button
- fake sync timestamp
- fake imported records
- no revoke/disconnect path

## AI Tool

Expected workflow:

- accept prompt/input
- call a real model/service if configured, or clearly label local mock/sample mode
- show progress
- show output tied to input
- allow retry/edit/copy/save
- handle failure/rate limits/missing key

Reality blockers:

- canned output pretending to be generated
- spinner followed by unrelated fake result
- no missing-key state
- copy/save buttons do nothing

## Onboarding

Expected workflow:

- collect needed setup data
- validate step inputs
- allow back/skip when appropriate
- persist progress
- finish into the configured product state

Reality blockers:

- progress dots do not reflect steps
- Finish goes to a generic dashboard unrelated to choices
- setup choices are not used later

## Settings

Expected workflow:

- load current values
- edit values
- validate
- save/cancel/reset
- show success/error
- persist changes

Reality blockers:

- toggles do not persist
- Save always succeeds
- dangerous changes lack confirmation

