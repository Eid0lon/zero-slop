# Dials And Presets

All dials are `0..10`. Higher values mean stricter review.

## Dials

- `USER_NEED_FIT`: rejects flows that do not clearly serve a real user goal.
- `TASK_COMPLETION`: requires a finishable path, clear completion condition, and return path.
- `IA_CLARITY`: requires clear navigation, grouping, labels, and object model.
- `COGNITIVE_LOAD`: penalizes choice overload, equal-weight clutter, hidden dependencies, and unnecessary explanation.
- `FEEDBACK_QUALITY`: requires timely loading, progress, success, empty, disabled, and system status feedback.
- `ERROR_RECOVERY`: requires validation, preserved input, retry, undo, cancel, and useful errors.
- `A11Y_OPERABILITY`: requires keyboard access, focus, semantics, labels, contrast, target size, and reduced motion.
- `RESPONSIVE_RESILIENCE`: requires usable small screens, wrapping, stable controls, and no horizontal traps.
- `PERFORMANCE_FEEL`: requires quick response, stable layout, no sluggish animation, and clear waits.
- `TRUST_SAFETY`: requires honest claims, consent, risk disclosure, AI uncertainty, and source boundaries.
- `CONTENT_CLARITY`: requires labels, microcopy, errors, CTAs, and help text to name the user's object and next action.
- `EXPERT_EFFICIENCY`: requires shortcuts, bulk actions, saved filters, history, keyboard paths, or reduced repetition when the domain expects repeat use.

## Default Dials

```text
USER_NEED_FIT=9
TASK_COMPLETION=9
IA_CLARITY=8
COGNITIVE_LOAD=8
FEEDBACK_QUALITY=8
ERROR_RECOVERY=9
A11Y_OPERABILITY=10
RESPONSIVE_RESILIENCE=9
PERFORMANCE_FEEL=8
TRUST_SAFETY=9
CONTENT_CLARITY=9
EXPERT_EFFICIENCY=6
```

## Presets

### `operational-saas`

High density, repeated-use workflows, clear object model, fast recovery.

```text
USER_NEED_FIT=10
TASK_COMPLETION=10
IA_CLARITY=9
COGNITIVE_LOAD=8
FEEDBACK_QUALITY=9
ERROR_RECOVERY=10
A11Y_OPERABILITY=10
RESPONSIVE_RESILIENCE=9
PERFORMANCE_FEEL=9
TRUST_SAFETY=9
CONTENT_CLARITY=9
EXPERT_EFFICIENCY=9
```

### `dashboard`

Decision path, data credibility, filters, comparison, and scan efficiency.

```text
USER_NEED_FIT=10
TASK_COMPLETION=9
IA_CLARITY=10
COGNITIVE_LOAD=9
FEEDBACK_QUALITY=9
ERROR_RECOVERY=8
A11Y_OPERABILITY=10
RESPONSIVE_RESILIENCE=10
PERFORMANCE_FEEL=9
TRUST_SAFETY=10
CONTENT_CLARITY=9
EXPERT_EFFICIENCY=8
```

### `commerce`

Price clarity, search/filter, comparison, availability, validation, checkout recovery, and trust.

```text
USER_NEED_FIT=10
TASK_COMPLETION=10
IA_CLARITY=9
COGNITIVE_LOAD=8
FEEDBACK_QUALITY=9
ERROR_RECOVERY=10
A11Y_OPERABILITY=10
RESPONSIVE_RESILIENCE=10
PERFORMANCE_FEEL=9
TRUST_SAFETY=10
CONTENT_CLARITY=10
EXPERT_EFFICIENCY=6
```

### `onboarding`

Motivation, setup clarity, progressive disclosure, saved progress, and reversible choices.

```text
USER_NEED_FIT=10
TASK_COMPLETION=10
IA_CLARITY=9
COGNITIVE_LOAD=10
FEEDBACK_QUALITY=9
ERROR_RECOVERY=9
A11Y_OPERABILITY=10
RESPONSIVE_RESILIENCE=9
PERFORMANCE_FEEL=8
TRUST_SAFETY=9
CONTENT_CLARITY=10
EXPERT_EFFICIENCY=5
```

### `editor`

Creation flow, direct manipulation, undo, autosave, shortcuts, selection, and durable feedback.

```text
USER_NEED_FIT=10
TASK_COMPLETION=10
IA_CLARITY=8
COGNITIVE_LOAD=9
FEEDBACK_QUALITY=10
ERROR_RECOVERY=10
A11Y_OPERABILITY=10
RESPONSIVE_RESILIENCE=8
PERFORMANCE_FEEL=10
TRUST_SAFETY=8
CONTENT_CLARITY=8
EXPERT_EFFICIENCY=10
```

### `ai-tool`

Input constraints, transparent outputs, human review, uncertainty, source handling, and safe fallback.

```text
USER_NEED_FIT=10
TASK_COMPLETION=10
IA_CLARITY=9
COGNITIVE_LOAD=9
FEEDBACK_QUALITY=10
ERROR_RECOVERY=10
A11Y_OPERABILITY=10
RESPONSIVE_RESILIENCE=9
PERFORMANCE_FEEL=9
TRUST_SAFETY=10
CONTENT_CLARITY=10
EXPERT_EFFICIENCY=8
```

### `public-service`

Plain language, eligibility, error prevention, accessibility, trust, privacy, and non-expert completion.

```text
USER_NEED_FIT=10
TASK_COMPLETION=10
IA_CLARITY=10
COGNITIVE_LOAD=10
FEEDBACK_QUALITY=10
ERROR_RECOVERY=10
A11Y_OPERABILITY=10
RESPONSIVE_RESILIENCE=10
PERFORMANCE_FEEL=8
TRUST_SAFETY=10
CONTENT_CLARITY=10
EXPERT_EFFICIENCY=4
```

### `mobile`

Thumb-safe controls, short paths, stable viewports, forgiving inputs, and offline/slow-network tolerance.

```text
USER_NEED_FIT=10
TASK_COMPLETION=10
IA_CLARITY=9
COGNITIVE_LOAD=10
FEEDBACK_QUALITY=10
ERROR_RECOVERY=10
A11Y_OPERABILITY=10
RESPONSIVE_RESILIENCE=10
PERFORMANCE_FEEL=10
TRUST_SAFETY=9
CONTENT_CLARITY=10
EXPERT_EFFICIENCY=6
```

## Thresholds

Default full gate:

- minimum UX score: `88`
- minimum panel average: `8.8`
- minimum lowest judge: `8.2`
- no hard UX gate blocker
- accessibility and keyboard gates pass
- primary journey verified in browser when feasible

Raise thresholds when critical dials are `10`. Never lower accessibility below strict.

