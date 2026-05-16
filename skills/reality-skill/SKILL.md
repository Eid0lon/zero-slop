---
name: reality-skill
description: Turns AI-generated demo UIs into real usable product workflows. Use when building, reviewing, or finishing apps, dashboards, forms, CRUD flows, onboarding, checkout, settings, auth-like flows, or any interface that must work beyond a static mockup.
---

# Reality Skill

Reality Skill removes demoware.

A screen is not a product. A workflow is real only when a user can complete the primary job end-to-end with working actions, truthful data, state coverage, validation, persistence or an honest mock boundary, recovery paths, and no fake capability presented as real.

## Core Rule

Do not make the UI bigger. Make the user job finishable.

Prefer the smallest implementation that turns the current surface from a static or deceptive demo into an honest, usable workflow.

## Workflow

1. Identify the primary user job.
2. Trace the workflow from entry to completion.
3. List every fake, missing, decorative, dead, or dishonest element.
4. Fix the smallest set of files needed to make the workflow real.
5. Verify the workflow with tests, build checks, browser checks, or a clear manual path when tools are limited.

## The Seven Reality Gates

### 1. Action Gate

Every primary action must work, open a real path, or be visibly disabled with a reason.

Block:

- `href="#"`
- `console.log`-only submit handlers
- buttons with no handler
- fake "Save", "Deploy", "Pay", "Connect", "Generate", or "Invite" actions
- destructive actions without confirmation or undo where appropriate

### 2. Data Gate

Data must be truthful.

Real data is best. Local mock data is acceptable only when the boundary is honest and does not pretend to be production truth.

Block:

- fake metrics presented as real
- fake testimonials, logos, users, revenue, uptime, or AI results
- decorative charts with no labels, units, source, or decision path
- duplicated placeholder rows that imply real usage

### 3. State Gate

The relevant states must exist.

Check for:

- loading
- empty
- error
- disabled
- success
- partial data
- long content
- small screen

Do not add every state everywhere. Add the states needed for the workflow the user is actually trying to complete.

### 4. Persistence Gate

User-created or edited data must survive the immediate workflow.

Acceptable persistence, depending on the project:

- server/database/API
- existing app state store
- local storage
- URL state
- durable in-memory state for one-page prototypes, if clearly scoped

If persistence is intentionally mocked, make the boundary explicit in code and avoid UI language that implies production storage.

### 5. Navigation Gate

Users must not hit dead ends.

Check for:

- back paths
- cancel paths
- retry paths
- edit paths
- delete/recover paths
- return-to-list/detail paths
- active navigation state

### 6. Validation Gate

Forms and inputs must reject bad input with clear inline feedback.

Check for:

- required fields
- malformed email/URL/number/date values
- min/max length or quantity
- disabled submit while invalid or submitting
- useful error text near the field
- preservation of user input after an error

### 7. Truth Gate

The UI must not pretend a fake capability is real.

Block fake:

- authentication
- payments
- AI generation
- integrations
- analytics
- security claims
- compliance claims
- notifications
- exports
- team invites

If the real backend or service is unavailable, create an honest local/mock boundary and name it plainly. Do not invent production behavior.

## Common Fix Patterns

- Replace a dead button with a working local state transition.
- Replace decorative mock rows with add/edit/delete flows.
- Add localStorage when a prototype needs refresh-safe data.
- Add inline validation before submit.
- Add empty/error/loading states around existing data calls.
- Replace fake dashboard claims with clearly labeled sample data.
- Add cancel, back, retry, and success paths.
- Disable unavailable integrations instead of pretending they work.
- Preserve the existing visual design unless it blocks the workflow.

## Non-Negotiables

- Do not stop at static UI when the task asks for an app, tool, dashboard, form, or workflow.
- Do not leave TODOs, placeholder handlers, dead links, fake submit buttons, or fake success states.
- Do not invent production services, credentials, customers, payments, metrics, or claims.
- Do not rewrite the product broadly when a smaller reality fix will complete the job.
- Do not remove useful design polish unless it hides fake functionality or blocks usability.
- Preserve accessibility, semantics, keyboard paths, and responsive behavior.

## Output Contract

When using this skill, report:

```text
Primary job:
Reality gate:
Blockers found:
Files changed:
Verification:
Remaining fake boundaries:
```

Use `Remaining fake boundaries: None` only when every relevant fake boundary has been removed, implemented, disabled, or honestly labeled.

## Done Means

- The primary user job can be completed end-to-end.
- Primary actions are real or honestly unavailable.
- Data is real, user-created, or clearly marked as sample/mock.
- Relevant states and validation exist.
- Persistence is implemented or the mock boundary is explicit.
- The user has recovery/navigation paths.
- Verification was run or the exact limitation is stated.
