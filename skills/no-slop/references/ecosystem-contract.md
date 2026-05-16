# Ecosystem Contract: no-slop

## Role

No Slop owns anti-slop UI detection, remediation, prevention, and strict anti-generic judging. It removes generic AI residue; it does not replace the premium design-direction work owned by `perfect-design`.

## Composes With

- `review`: when UI changes touch logic, data flow, auth, billing, persistence, or security-sensitive behavior.
- `debug`: when visual defects come from runtime behavior, hydration, async state, or measurements.
- `perfect-design`: when the user asks for broad creative UI generation, premium product-specific design, or senior design-engineering output, and No Slop is used as the anti-generic quality gate.
- `reality-skill`: after No Slop remediation when the target is an app, dashboard, form, CRUD flow, onboarding, checkout, settings, auth-like flow, or contains fake proof/data/actions that must become honest and usable.
- `perfect-shot`: when the design work is one part of a larger first-pass implementation.
- `create-deep-search`: when the user explicitly needs current design research, domain UX research, or external references.

## Ownership Boundary

No Slop can:

- Scan UI code and rendered screens.
- Define design direction.
- Patch styling, layout, copy, components, tokens, accessibility, and motion.
- Judge output with subagents.
- Block weak results.

No Slop should not:

- Rewrite business logic without cause.
- Change data contracts unless required for UI truthfulness.
- Invent fake metrics, testimonials, screenshots, or brand assets.
- Add dependencies unless the existing stack or domain justifies them.

## Quality Gate

Done means:

- AI-slop score reported.
- Slop signatures named or ruled out.
- Active dials and preset reported.
- Judge gate passed or explicitly blocked.
- Accessibility and responsive checks completed or limitation stated.
- Reality Skill handoff completed or marked not applicable with reason.
- Build/lint/type/test checks run when available.
- Remaining risk named.
