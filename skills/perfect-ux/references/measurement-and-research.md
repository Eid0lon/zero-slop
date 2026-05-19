# Measurement And Research

Use this when the task asks for evidence, analytics, usability testing, or when the UX risk is too high to rely on expert review alone.

## Evidence Ladder

Use the best available evidence:

1. Real user task observation.
2. Usability test on the actual or clickable flow.
3. Analytics tied to task events.
4. Support tickets, sales calls, interviews, user quotes.
5. Accessibility audit and assistive-tech checks.
6. Browser walkthrough by the agent.
7. Deterministic code scan.
8. Heuristic review.

Heuristic review is useful, but it is not proof of user success.

## Task Metrics

Track:

- task success rate
- time on task
- error rate
- abandon/drop-off point
- form completion rate
- validation error frequency
- retry rate
- undo/delete recovery usage
- dead clicks and rage clicks
- search refinements and zero-result searches
- first meaningful success
- repeat-task speed
- accessibility defects
- support contacts per task

## Usability Test Script

Keep it small and concrete:

```text
Scenario:
User:
Starting URL/state:
Task:
Success condition:
What not to help with:
Observe:
Questions after:
```

Prefer 3-5 formative participants per iteration when resources are limited. Iterate on clear problems instead of waiting for a perfect study.

## Analytics Event Plan

For important flows, define:

```text
journey_started
primary_action_clicked
validation_error_shown
system_error_shown
retry_clicked
success_reached
abandoned
undo_clicked
help_opened
search_zero_results
```

Events should include object type, safe status metadata, and step name. Do not log sensitive user input.

## Research Method Choice

- Unknown user need: interviews, field study, support/sales review.
- Confusing flow: moderated usability test.
- Many users drop off: analytics funnel plus session review.
- Bad forms: validation analytics plus usability test.
- Accessibility risk: WCAG audit plus keyboard/screen reader checks.
- IA uncertainty: tree test, card sort, search logs.
- Copy uncertainty: comprehension test or preference only after task clarity.

## Shipping With Limited Evidence

If research cannot run now:

- state the assumption
- make the smallest reversible improvement
- add instrumentation or manual verification steps
- avoid irreversible changes
- define what would prove the change wrong

