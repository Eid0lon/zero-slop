# Reality Gates

Use these gates to audit, implement, and judge. A gate fails when a normal user could reasonably believe a workflow is available but cannot actually complete it, recover from failure, or trust its data.

## Gate 1: Job Gate

The surface must have a clear primary job and completion condition.

Fail signs:

- It is mostly a gallery of cards, metrics, or CTAs with no finishable task.
- The page has many impressive controls but no coherent path.
- The success state does not correspond to a user-visible outcome.

Pass signs:

- A user can say what they are doing, start it, complete it, and see the result.
- Secondary features do not obscure the main job.

## Gate 2: Action Gate

Every primary action must work, navigate to a real path, or be disabled with a reason.

Block:

- `href="#"`
- buttons with no handler
- handlers that only call `console.log`, `alert`, or a fake timeout
- fake Save, Publish, Deploy, Pay, Connect, Generate, Invite, Export, Sync, Analyze, or Upload
- destructive actions without confirmation, undo, or obvious recovery where appropriate

## Gate 3: Data Gate

Data must be real, user-created, or honestly sample.

Block:

- fake metrics presented as live
- fake revenue, uptime, compliance, security, customer counts, testimonials, logos, reviews, team members, or AI output
- decorative charts with no labels, units, source, time range, or decision path
- repeated placeholder rows implying real usage

## Gate 4: Input Gate

Inputs must have a data model, constraints, validation, and preserved values.

Check:

- required fields
- malformed email, URL, number, date, time, file, or currency values
- min/max and length constraints
- disabled submit while invalid/submitting
- inline messages near the fields
- successful clear/reset behavior only after data is committed

## Gate 5: State Gate

Relevant states must exist and must be reachable.

Minimum state set for primary workflows:

- initial
- loading/submitting
- empty
- validation error
- system error
- success
- disabled/unavailable
- partial data
- long content
- small screen

Do not add theatrical states. Add states the workflow actually needs.

## Gate 6: Persistence Gate

User-created or edited data must survive the expected scope.

Preference order:

1. Existing server/database/API.
2. Existing app store/cache.
3. Local storage or IndexedDB.
4. URL state for filters and shareable views.
5. In-memory state only for explicitly scoped throwaway prototypes.

Fail signs:

- Save appears to work but refresh loses the item.
- Edit/delete changes only the DOM, not the source of truth.
- The app says "synced" without sync.

## Gate 7: Navigation Gate

Users must not hit dead ends.

Check:

- back/cancel paths
- retry paths
- return-to-list/detail paths
- edit paths
- delete/recover paths
- active navigation state
- deep link or URL coherence when the stack supports it

## Gate 8: Feedback Gate

The app must explain what just happened.

Check:

- progress while async work runs
- success feedback tied to the actual committed result
- error feedback with a useful next step
- disabled controls with reasons
- no fake celebratory toast for failed or unimplemented work

## Gate 9: Truth Gate

The UI must not pretend a fake capability is real.

Special scrutiny:

- authentication
- payments
- AI generation
- analytics
- integrations
- notifications
- exports/imports
- permissions
- security/compliance
- team invites

If a real service is unavailable, create an honest local or disabled boundary.

## Gate 10: Robustness Gate

The workflow must tolerate normal messy use.

Check:

- duplicate submits
- slow/failing requests
- long names/text
- empty data sets
- partial objects/missing optional fields
- reloads during or after work
- keyboard-only use
- small viewport use

## Gate 11: Accessibility Gate

Reality includes operability.

Check:

- semantic buttons/links/forms
- labels for inputs
- focus visibility
- keyboard reachable dialogs/menus/tabs
- disabled states announced or explained
- color not the only error/success signal

## Gate 12: Verification Gate

Claims must be proven.

Pass proof can include:

- unit/integration tests
- typecheck/lint/build
- deterministic CLI audit
- browser walkthrough with primary path
- persistence refresh check
- responsive screenshot/inspection
- manual verification steps when tools are blocked

No verification means no full pass.

