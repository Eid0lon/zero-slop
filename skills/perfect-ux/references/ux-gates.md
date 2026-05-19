# UX Gates

Use these gates to audit, implement, and judge. A gate fails when a normal user could reasonably be confused, blocked, misled, excluded, or forced to redo work.

## Gate 1: User Need Gate

The surface must serve a specific user in a specific context.

Fail signs:

- The UI is organized around features, sections, or marketing claims rather than a user job.
- Primary copy could apply to any product.
- The user's object, risk, or decision is not visible.

Pass signs:

- The user, job, object, and success condition are clear within the first meaningful interaction.

## Gate 2: Entry And Orientation Gate

The user must know where they are and what they can do next.

Check:

- page title or active location
- selected navigation state
- object/context label
- first useful action
- return/back path

## Gate 3: Task Completion Gate

The primary job must have a start, action path, completion condition, and result.

Block:

- vague CTAs with unclear destination
- modal dead ends
- actions that do not reveal progress or outcome
- success states that do not correspond to a user-visible change

## Gate 4: Information Architecture Gate

Navigation, grouping, labels, and hierarchy must match the user's mental model.

Fail signs:

- equal-weight controls compete for attention
- settings/actions/data are mixed without grouping
- tabs hide required sequential work
- breadcrumbs, filters, or active states are missing where users need orientation

## Gate 5: Decision Clarity Gate

The UI must put the right information near the decision.

Check:

- constraints, units, examples, price, status, time range, ownership, source, side effects, and consequences appear before action
- comparison data uses consistent labels and units
- help text sits next to the field or choice it clarifies

## Gate 6: Cognitive Load Gate

The interface must reduce unnecessary memory, reading, and decision effort.

Fail signs:

- too many same-weight choices
- long generic explanations
- repeated data entry
- hidden prerequisites
- frequent mode switches
- visual density without hierarchy

## Gate 7: Input And Form Gate

Inputs must be labeled, constrained, validated, preserved, and recoverable.

Block:

- placeholder-only labels
- lost input after error
- disabled submit with no reason
- validation only after expensive submission when local validation is possible
- messages far from the field they refer to

## Gate 8: Feedback Gate

The system must acknowledge user actions and status changes quickly and specifically.

Check:

- loading/submitting
- progress for long work
- optimistic/pending state where appropriate
- success tied to committed result
- empty, partial, stale, offline, and unavailable states
- no fake spinner that hides a dead action

## Gate 9: Error Recovery Gate

Failures must preserve context and tell the user how to continue.

Check:

- what failed
- whether user data survived
- retry/edit/cancel/back path
- field-level errors where applicable
- focus management after error
- undo or confirmation for risky actions

## Gate 10: Accessibility And Operability Gate

The flow must be usable by keyboard, assistive tech, low vision, motor-impaired users, and reduced-motion users.

Block:

- invisible focus
- non-semantic clickable elements with no keyboard handling
- unlabeled icon buttons or inputs
- color-only status
- keyboard traps
- inaccessible custom dialogs/menus/tabs/comboboxes
- target sizes too small for touch-critical actions

## Gate 11: Responsive And Mobile Gate

The journey must remain coherent and usable on small screens.

Block:

- clipped controls or text
- horizontal page overflow
- fixed panels that trap content
- controls wider than the viewport
- primary actions pushed below unrelated content
- inaccessible hover-only interactions

## Gate 12: Performance Feel Gate

The experience must feel responsive and stable.

Check:

- no unexpected layout shift around primary actions
- stable media dimensions
- low input latency
- no heavy animation/filter on critical interactions
- clear feedback for slow work

## Gate 13: Trust And Truth Gate

The interface must not overclaim or obscure risk.

Block:

- fake live metrics, fake customers, fake security, fake compliance, fake AI confidence, fake payments, fake integrations
- unclear data source or time range for important decisions
- hidden destructive consequences
- ambiguous consent or privacy-sensitive data use

## Gate 14: Content Clarity Gate

Copy must name the user's object, action, consequence, and recovery path.

Fail signs:

- `Get started`, `Learn more`, `Submit`, `Continue`, `Unlock`, `Empower`, or `AI powered` where a specific action or object should be named
- errors that blame the user
- instructions that compensate for a confusing design

## Gate 15: Expert Efficiency Gate

Repeated-use products must not force slow novice paths forever.

Check:

- keyboard shortcuts or command surfaces
- saved filters/views/defaults
- bulk actions
- search
- history/recent items
- templates
- fewer repeated confirmations for low-risk repeat actions

## Gate 16: Measurement Gate

Claims of UX improvement must have evidence.

Pass proof can include:

- browser walkthrough of primary task
- usability test notes or task scenario
- analytics event plan
- task success/time/error metrics
- form completion data
- accessibility test results
- support-ticket or user-quote evidence
- deterministic CLI precheck
- code tests for validation/state behavior

No evidence means no full pass.

