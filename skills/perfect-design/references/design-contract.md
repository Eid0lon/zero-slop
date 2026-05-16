# Design Contract

Write this before code. A contract is a practical promise about what the interface must accomplish and how the visual system will carry it.

## Contract Template

```markdown
# Design Contract

User:
Context:
Primary job:
Secondary jobs:
Domain expectation:
Risk level:

First viewport obligation:
Product proof:
Data/media available:
Primary workflow:
Navigation model:

Design thesis:
Visual voice:
Density:
Layout model:
Typography:
Palette:
Shape/radius:
Elevation/material:
Icon/image style:
Motion:
Copy voice:

States required:
Accessibility constraints:
Responsive constraints:
Performance constraints:

Forbidden defaults:
Acceptance gates:
```

## Rejection Rules

Reject the contract when:

- It uses abstract style words without concrete decisions.
- The design thesis could apply to a random SaaS, portfolio, shop, or dashboard.
- The first viewport does not expose the product, object, workflow, or primary task.
- It relies on fake metrics, fake logos, fake testimonials, or placeholder screenshots.
- It lacks mobile, keyboard, focus, or reduced-motion strategy.
- It treats design system tokens as optional.
- It uses Awwwards-style expression for an operational task without a user benefit.

## Product Proof Prompts

Ask these internally:

- What can the user inspect in the first 5 seconds?
- What object is this product organized around?
- What information changes a user's decision?
- What state proves the product is real?
- What would a power user do with keyboard only?
- What would be embarrassing in a screenshot review?

## Minimal Accepted Contract

If the user gives little context, infer a conservative contract:

- For SaaS/tool: product screenshot/workflow first, restrained palette, compact hierarchy, exact CTAs.
- For dashboard: decision path first, filters near data, table/chart labels, units, deltas, periods.
- For commerce: product evidence, price clarity, filters, comparison attributes, honest checkout.
- For portfolio: real work evidence, case-study structure, distinct point of view, no generic trait cards.
- For editorial/brand: typography and imagery carry the story; usability and performance still gate the result.
