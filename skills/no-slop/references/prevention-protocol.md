# Prevention Protocol

`--prevent` exists to stop bad UI before code is generated.

## Objective

Force the agent to define and judge a design contract before writing UI code.

## Sequence

1. Parse brief, target, preset, and dials.
2. Load `ai-slop-patterns.md`, `dials-and-presets.md`, and `judge-system.md`.
3. Detect risky prompt language:
   - "modern", "sleek", "premium", "beautiful", "clean", "make it pop".
   - No user, domain, task, object, or content constraints.
   - Requests for generic sections: hero, features, testimonials, pricing.
4. Inspect existing project tokens and components when target exists.
5. Draft a prevention contract.
6. Run judge panel against the contract.
7. Only generate code after the gate passes.

## Prevention Contract

```markdown
# Prevention Contract

User:
Primary job:
Domain expectation:
Surface type:
Preset:
Dials:

## Required Decisions
- Palette:
- Type:
- Density:
- Layout:
- Components:
- Motion:
- Copy:
- Assets/data:
- Accessibility:

## Forbidden Defaults
- specific slop moves forbidden for this task

## Acceptance Gates
- measurable constraints before output can be called done
```

## Automatic Rejections

Reject or revise the contract when it contains:

- A palette with no domain or brand rationale.
- More than one decorative gradient/glow/blur system.
- Feature cards as the primary structure without a product-specific reason.
- Motion used only to create excitement.
- Copy that could apply to any SaaS, portfolio, shop, or dashboard.
- No mobile strategy.
- No accessibility plan.
- No real product evidence when the surface needs proof.

## Generation Rules After Approval

- Generate the actual usable screen first, not a landing page, unless the user asked for marketing.
- Use the existing project stack and component conventions.
- Build stable dimensions for fixed-format UI.
- Include all obvious states for controls and workflows.
- Verify by scan, browser/screenshot when available, and judge panel before final.
