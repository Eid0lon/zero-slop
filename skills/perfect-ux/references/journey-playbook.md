# Journey Playbook

Use this playbook to map, audit, and improve product journeys.

## 1. Map The Job

Write the job in this form:

```text
When [context], [user] needs to [action/change/decision] so they can [outcome].
```

Avoid feature statements. `Use filters` is not a job. `Find delayed invoices that need follow-up before payroll closes` is a job.

## 2. Trace The Primary Path

Map:

1. Entry point.
2. Orientation.
3. Required information.
4. Decision point.
5. Action.
6. Feedback.
7. Completion state.
8. Return/edit/retry path.

Each step should answer:

- What does the user need to know?
- What can they do?
- What can go wrong?
- How do they recover?
- What state proves progress?

## 3. Find Friction

Classify friction:

- `ambiguity`: user does not know what a label, state, or action means.
- `choice overload`: too many same-weight choices.
- `memory burden`: user must remember info from another place.
- `dead end`: no next, back, cancel, retry, or recovery.
- `data loss`: input or context disappears.
- `latency`: wait has no feedback or blocks unnecessary work.
- `trust gap`: claim/source/risk is unclear.
- `exclusion`: keyboard, screen reader, low vision, motor, motion, mobile, or slow-network users are blocked.
- `expert drag`: repeated use forces beginner-only paths.

Fix the highest user harm first, not the most visible blemish.

## 4. Information Architecture

Good IA is predictable object organization:

- Put primary objects before secondary reports.
- Group actions near the object they affect.
- Keep global navigation, local navigation, filters, and row/card actions visually distinct.
- Use active states, breadcrumbs, object titles, and empty states to maintain location.
- Use tabs for peer views, not required sequential steps.
- Use steppers for sequence only when order matters and progress must be visible.
- Use disclosure for advanced or optional detail after the main path is clear.

## 5. Domain Expectations

### Operational SaaS

- Primary object, status, owner, due date, and next action are visible.
- Tables/lists support search, filter, sort, selection, bulk action, and detail.
- Repeated work has saved defaults or keyboard support.
- Alerts are actionable, not decorative.

### Dashboard

- Start from the decision, not the chart.
- Every metric needs label, unit, period, source, trend context, and action path.
- Filters must be visible and reflected in state.
- Empty/partial/stale data states must be honest.

### Commerce

- Product evidence, price, availability, shipping, returns, comparison, variants, and cart impact must be clear.
- Validation should prevent checkout rework.
- Trust patterns should answer real risk, not use fake urgency.

### Onboarding

- Ask only for data needed now.
- Show why each step matters.
- Save progress.
- Provide skip/back/edit when safe.
- End with real first value, not a generic celebration.

### Editors And Creation Tools

- Preserve drafts.
- Expose undo/redo, selection, status, autosave, export/share, and failure recovery.
- Keep tools close to the object they modify.
- Do not hide destructive or irreversible actions.

### AI Tools

- Make input constraints visible.
- Show what the model used when possible.
- Distinguish generated suggestions from user-authored truth.
- Provide edit, regenerate, cite/source, copy/export, and report/error paths.
- Never imply certainty where the system cannot support it.

### Public Service

- Use plain language.
- Explain eligibility, evidence needed, time required, privacy, and final confirmation.
- Preserve progress and support interruption.
- Design for low confidence and high stress.

## 6. Beginner To Expert Bridge

First-time path:

- orient
- explain only immediate consequences
- reduce choices
- provide examples and defaults

Returning path:

- remember state
- surface recent items
- support keyboard/search
- reduce confirmation for low-risk tasks
- make bulk and repeated actions efficient

