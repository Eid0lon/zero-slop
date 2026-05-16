# Anti-Slop Remediation Playbook

Use this for `--fix` and `--redesign`.

## Prime Directive

Do not merely remove cliches. Replace them with decisions that match the product, user, domain, and task.

## Design Direction Block

Write this before editing:

```markdown
Design direction
- User:
- Primary job:
- Domain expectation:
- Density:
- Visual voice:
- Surface:
- Accent:
- Type:
- Shape/radius:
- Motion:
- Imagery/data:
- Copy voice:
- Accessibility constraints:
```

If coherent tokens exist, use them. If tokens are missing or harmful, define the smallest semantic set needed:

```css
:root {
  --surface: ;
  --surface-raised: ;
  --text: ;
  --text-muted: ;
  --border: ;
  --accent: ;
  --accent-contrast: ;
  --focus: ;
  --radius-control: ;
  --radius-surface: ;
  --shadow-raised: ;
  --motion-fast: ;
  --motion-standard: ;
}
```

## Fix vs Redesign

Use `--fix` when:

- The structure is basically right.
- Slop comes from shared components, copy, tokens, states, or local layout.
- A surgical patch can reduce the score below the gate.

Use `--redesign` when:

- The first viewport is formulaic.
- The page has no clear product/job.
- The UI is card soup across multiple sections.
- Tokens, hierarchy, copy, and layout all fail together.
- Slop score is above 55 or a major slop signature is present.

## Transformations

### Generic Hero

Before:

```text
Centered headline: "Unlock seamless productivity"
Subheadline: "A powerful platform for modern teams"
Buttons: "Get Started" / "Learn More"
Background: purple-blue gradient blob
```

After:

```text
Headline names the concrete offer.
First viewport shows the product, workflow, object, or useful data.
Primary CTA names the next action.
Secondary action answers a real objection.
Next section is visible on mobile and desktop.
```

### Feature Card Soup

Before:

```text
Six identical cards.
Generic icon tile.
Headings: Fast, Secure, Smart, Easy.
```

After:

```text
Workflow, comparison table, annotated screenshot, checklist, timeline, or grouped capability map.
Each item names a user outcome.
Icons appear only when they reduce reading effort.
```

### Purple/Blue Gradient Default

Before:

```text
from-blue-600 to-purple-600, gradient text, glow shadow.
```

After:

```text
Palette derived from brand, material, data, content, or domain.
One accent. Solid readable surfaces.
Gradient only when it communicates light, material, depth, data, or atmosphere.
```

### Glassmorphism Overload

Before:

```text
backdrop-blur cards over decorative orbs.
```

After:

```text
Solid surfaces for content.
Blur only for real layering such as overlays or translucent navigation.
Contrast verified against actual pixels.
```

### Rounded Everything

Before:

```text
rounded-2xl on cards, inputs, buttons, badges, modals.
```

After:

```text
Controls: 4-8px.
Panels/cards: 6-12px.
Pills only for chips, tags, and compact labels.
Sharper geometry for operational tools.
```

### Fade-In Parade

Before:

```text
Every section starts invisible and animates into view.
```

After:

```text
Motion explains state, continuity, drag/drop, route change, or feedback.
Reduced-motion support exists.
Reading content is not delayed.
```

### Weak Typography

Before:

```text
Huge hero, tiny gray body, all cards same heading size.
```

After:

```text
Type scale follows content importance.
Readable line height and measure.
Labels are clear, not over-styled.
Contrast supports scanning.
```

### Vague Copy

Before:

```text
"Streamline your workflow with powerful automation."
```

After:

```text
Name the object, user action, and outcome.
Example: "Route overdue invoices to the collector before the Friday cash review."
```

### Dashboard Slop

Before:

```text
Four large metric cards, unlabeled chart, activity feed.
```

After:

```text
Primary decision is visible.
Filters and comparison controls are close to data.
Tables/charts answer named questions.
Metrics include units, deltas, periods, and thresholds.
```

### E-commerce Slop

Before:

```text
Generic product grid, fake countdown, unclear checkout action.
```

After:

```text
Filters show counts and applied state.
Product cards expose comparison attributes.
Price, shipping, stock, returns, and total cost are clear.
No fake urgency.
```

### AI Tool Slop

Before:

```text
Chat box as entire product, vague examples, no recovery.
```

After:

```text
Task controls, examples, constraints, sources, history, confidence, and clear failure recovery.
Chat is one surface, not the whole UX, unless the product truly is conversation.
```

## Before/After Library

### Button Label

Before: `Get Started`

After options:

- `Create invoice run`
- `Compare plans`
- `Upload floor plan`
- `Schedule pickup`
- `Review flagged claims`

Rule: the label must describe the next action.

### Empty State

Before:

```text
No data yet. Get started by creating your first item.
```

After:

```text
No delayed shipments match these filters.
Widen the date range or clear Carrier: DHL.
```

Rule: name the object and recovery path.

### Card Grid

Before:

```text
[Fast] [Secure] [Powerful]
```

After:

```text
Step 1: Import claims
Step 2: Flag missing evidence
Step 3: Send reviewer packets
```

Rule: convert traits into workflow.

### Stat

Before:

```text
99.9% uptime
```

After:

```text
API availability: 99.94% over last 30 days
2 incidents, 14 min total degraded time
```

Rule: proof needs period, unit, and source.

### Motion

Before:

```text
Cards fade in on scroll.
```

After:

```text
Rows animate position after sorting so the user sees what changed.
Reduced-motion switches to instant update.
```

Rule: motion explains state change.

## Accessibility Fix Patterns

Focus:

```css
:focus-visible {
  outline: 2px solid var(--focus);
  outline-offset: 2px;
}
```

Reduced motion:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: 0.01ms !important;
  }
}
```

Stable media:

```tsx
<img src={src} width={1200} height={800} alt="Specific description" />
```

Adapt these to the existing stack. Do not paste blindly.
