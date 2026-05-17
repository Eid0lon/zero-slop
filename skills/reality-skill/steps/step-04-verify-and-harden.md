# Step 04: Verify And Harden

Load `references/verification-playbook.md` and run the strongest feasible proof.

Minimum final checks:

- Build/type/lint/test command when present.
- Browser workflow check for frontend apps when feasible.
- Invalid input check for forms.
- Persistence check for user-created data.
- Truth-boundary check for unavailable services.
- Responsive/keyboard smoke check when UI changed.

Then score with `references/judge-system.md`.

Do not claim full success if:

- the app could not be run and no tests cover the workflow
- the primary workflow was not manually or automatically exercised
- persistence was not checked
- fake service boundaries remain unlabeled

