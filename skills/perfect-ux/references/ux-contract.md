# UX Contract

Write this before code. A UX Contract is a practical promise about who the experience serves, what job they must complete, how the system will guide them, and how success will be proven.

## Contract Template

```markdown
# UX Contract

User:
Context:
Frequency:
Skill level:
Primary job:
Secondary jobs:
Starting point:
Completion condition:

Object model:
Navigation model:
Primary path:
Decision moments:
Inputs required:
Outputs/results:

Feedback required:
Failure modes:
Recovery paths:
Persistence expectations:
Trust/safety constraints:
Privacy/consent constraints:
AI/model boundaries:

Accessibility constraints:
Responsive constraints:
Performance constraints:
Expert-efficiency constraints:

Research/evidence available:
Metrics to watch:
Forbidden friction:
Acceptance gates:
```

## Rejection Rules

Reject or revise the contract when:

- It names a screen but not a user job.
- The completion condition is vague.
- The starting point is missing.
- It lacks failure and recovery paths.
- It relies on copy explanations instead of simplifying the flow.
- It treats accessibility as post-processing.
- It hides trust-sensitive claims, AI uncertainty, payments, auth, privacy, or security behind vague wording.
- It has no verification evidence.
- It optimizes for first impression while making repeated use slower.

## Contract Prompts

Ask internally:

- What does the user know before arriving?
- What are they trying to change, decide, create, compare, or recover?
- What information do they need at the moment of decision?
- What is the smallest path that honestly completes the job?
- What happens if the user is wrong, late, impatient, keyboard-only, on mobile, offline, distracted, or using assistive tech?
- What state proves the system did the work?
- What would users contact support about?
- What metric or usability signal would reveal failure?

## Minimal Accepted Contract

When the user gives little context, infer conservatively:

- For SaaS/tools: name the work object, make the primary action visible, include status, validation, error recovery, persistence, and keyboard path.
- For dashboards: define the decision, data source, time range, comparison, filters, empty state, and action after insight.
- For commerce: clarify product evidence, price, availability, shipping/returns, comparison, validation, checkout path, and trust.
- For onboarding: preserve progress, explain why each step matters, reduce up-front choices, and show a meaningful first success.
- For AI tools: name input limits, output review path, uncertainty, sources if available, retry/edit path, and human control.
- For public services: use plain language, eligibility, save/return, error prevention, accessibility, privacy, and final confirmation.

