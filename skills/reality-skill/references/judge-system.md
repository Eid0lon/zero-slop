# Judge System

Use judge mode to decide whether an app is still demoware.

## Scoring

Score each gate from 0 to 5:

- 0: absent or deceptive
- 1: mostly fake
- 2: partially wired with serious gaps
- 3: usable but brittle or under-verified
- 4: solid with minor gaps
- 5: real, truthful, resilient, verified

Gates:

1. Job
2. Actions
3. Data
4. Inputs
5. States
6. Persistence
7. Navigation
8. Feedback
9. Truth
10. Robustness
11. Accessibility
12. Verification

Reality score:

```text
sum(gate_scores) / 60 * 100
```

## Hard Fail Conditions

Block shipping if any of these are true:

- Primary workflow cannot complete.
- A primary action is dead or fake.
- Save/edit/delete loses data unexpectedly.
- Fake auth/payment/security/compliance/integration/AI is presented as real.
- Form submission can silently discard user input.
- No verification was performed and tools were available.

## Judge Roles

When live subagents are allowed and useful, ask for independent reviews:

- Product Operator: can the user complete the job?
- Skeptical Backend: are data and persistence real?
- QA Breaker: what normal use breaks it?
- Trust Auditor: what claims are dishonest?
- Accessibility Operator: can it be operated without ideal conditions?

If live agents are unavailable, perform the roles locally and mark `JUDGE_PANEL_UNAVAILABLE`.

## Output

```text
Reality score:
Gate scores:
Hard fails:
Workflow proof:
Truth boundary proof:
Persistence proof:
Verification proof:
Required changes:
Ship decision:
```

