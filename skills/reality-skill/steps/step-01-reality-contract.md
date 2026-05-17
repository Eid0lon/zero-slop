# Step 01: Reality Contract

Write or infer a compact contract before edits.

```text
User:
Job:
Starting point:
Completion condition:
Data needed:
Actions needed:
Persistence needed:
Unavailable real services:
Honest mock/local boundary:
States that must exist:
Verification path:
```

Rules:

- Prefer one primary job. Add secondary jobs only if they are necessary for the primary job.
- If a brief says "dashboard", identify what decision/action the dashboard enables.
- If a brief says "AI", identify input, generation boundary, output, save/copy/retry path, and missing-key behavior.
- If a brief says "CRUD", identify entity, fields, validation, list/detail/edit/delete paths, and persistence.
- If a brief says "checkout/auth/integration", treat truth boundaries as high-risk.
- Ask the user only when the primary job cannot be inferred safely.

