# Research Synthesis

Use this as compressed research memory. It distills a broad sweep across usability research, accessibility standards, design systems, service design, commerce UX, performance guidance, and Human-AI interaction guidance.

## Core Thesis

Excellent UX is not the absence of friction. It is the intentional placement of friction where it protects the user, and the removal of friction where it only slows comprehension, action, recovery, or trust.

## Source-Derived Principles

1. Start with the user's job, not the screen.
   - ISO usability frames quality through effectiveness, efficiency, satisfaction, and context of use.
   - NN/g, GOV.UK, and service-design guidance converge on user needs, task success, and real context before visual preference.

2. The system model must be visible.
   - Users need to know where they are, what object they are affecting, what can happen next, and what changed.
   - Navigation, labels, status, breadcrumbs, selected states, and feedback do more UX work than decorative explanation.

3. Recognition beats recall.
   - Put needed options, constraints, examples, units, and consequences near the decision point.
   - Avoid hiding primary choices behind vague CTAs, unlabeled icons, or multi-step surprises.

4. Feedback must be immediate, specific, and recoverable.
   - Every action should produce an observable response.
   - Loading, progress, success, failure, retry, undo, cancel, and saved state are part of the product, not polish.

5. Error prevention is better than error messaging.
   - Use constraints, sensible defaults, previews, inline validation, masks only when they help, confirmation for high-risk actions, and undo where possible.
   - When errors happen, preserve user input and focus the recovery path.

6. Accessibility is core UX.
   - Keyboard access, focus visibility, semantic controls, labels, target size, contrast, reduced motion, text alternatives, and non-color-only status are gates.
   - A flow that excludes a user is not a good flow.

7. Mobile and responsive UX are interaction models, not breakpoints.
   - Controls must remain reachable, text must wrap, panels must not trap the viewport, and task order must remain coherent at narrow widths.
   - Stable dimensions and responsive media prevent layout shifts that feel like broken UX.

8. Performance is experienced as trust.
   - Long input latency, layout shift, late media, heavy blur/filter effects, and blocked transitions make users hesitate.
   - Perceived performance improves when the app acknowledges work, preserves context, and avoids surprise movement.

9. Content is interface.
   - Labels must name the object and action.
   - Error text should say what happened, why it matters, and what to do next.
   - Help text belongs next to the decision it clarifies.

10. Trust is earned through honest boundaries.
    - Do not present fake metrics, live data, AI certainty, security, compliance, payments, or integrations as real.
    - For AI, expose input limits, source boundaries, confidence or uncertainty where relevant, review controls, and escape hatches.

11. Expert efficiency matters after first success.
    - Repeated-use tools need keyboard paths, saved views, search, filter, bulk action, history, defaults, templates, and fewer repeated confirmations.
    - Beginner clarity and expert speed must coexist.

12. Measurement closes the loop.
    - Use task success rate, time on task, error rate, abandon points, rage/dead clicks, form completion, search refinement, support questions, accessibility defects, and user quotes.
    - Qualitative research finds why; quantitative evidence shows how often and where.

## Practical Translation Rules

When a user asks for "better UX":

- Convert style words into task outcomes.
- Write the UX Contract first.
- Map the primary journey from first entry to completion and recovery.
- Remove ambiguity before adding features.
- Fix inaccessible or unrecoverable actions before visual polish.
- Choose defaults that protect user time and data.
- Prefer concrete copy over explanatory paragraphs.
- Use progressive disclosure only after the main path is obvious.
- Verify with the rendered UI whenever possible.

When inspired by:

- NN/g: use heuristics, task analysis, mental models, error prevention, recognition over recall, and user testing.
- GOV.UK: use plain language, user needs, inclusive access, forms that preserve progress, and service completion.
- W3C/WAI/WCAG: treat accessibility as normative UX infrastructure.
- Baymard: remove checkout, form, filtering, product-list, and mobile commerce friction.
- Apple, Material, Fluent, Polaris, Carbon, Primer, Spectrum: use platform conventions, clear feedback, component consistency, and accessibility baked into primitives.
- web.dev: optimize perceived speed, responsiveness, and layout stability as UX.
- People + AI / Human-AI guidelines: keep humans in control, reveal uncertainty, support correction, and prevent automation surprises.

Never copy a design system's brand. Translate its operational principles into the user's product.

