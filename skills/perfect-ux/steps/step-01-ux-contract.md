# Step 01: UX Contract

## Objective

Define or infer the user, job, journey boundary, trust constraints, and verification standard before editing.

## Actions

1. Load `references/ux-contract.md`.
2. Inspect relevant code, routes, data models, forms, components, copy, and existing tests.
3. Write a compact UX Contract:

```text
User:
Context:
Primary job:
Starting point:
Completion condition:
Decision moments:
Inputs required:
Feedback required:
Failure/recovery paths:
Accessibility constraints:
Responsive constraints:
Performance constraints:
Trust/safety constraints:
Evidence to verify:
Forbidden friction:
```

4. Identify unknowns.
5. Infer conservative defaults unless multiple high-impact jobs conflict.
6. Reject abstract goals like "make it intuitive" unless translated into task outcomes.

## Output

```markdown
# UX Contract
Status:
Preset:
Dials:

## User And Job
## Journey Boundary
## States And Recovery
## Trust And Evidence
## Gates
```

## Next Step

Load `step-02-journey-audit.md`.

