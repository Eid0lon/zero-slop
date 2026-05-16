# AI-Slop Pattern Database

AI-slop is UI that collapses toward the statistical center of common generated web patterns instead of making product-specific decisions.

Use this file before every scan, prevention pass, fix, redesign, and judge cycle.

## Severity Model

Score from 0 to 100. Cap total at 100.

| Severity | Points | Use for |
| --- | ---: | --- |
| Critical | 15 | Accessibility blocker, broken mobile, unreadable text, fake proof in production, deceptive pattern, primary workflow blocked. |
| High | 8 | Above-the-fold genericity, brandless layout, hierarchy collapse, design token violation affecting many surfaces, heavy card soup. |
| Medium | 4 | Local cliche, vague copy, decorative motion/icon, weak responsive guard, repeated utility soup. |
| Low | 2 | Minor polish issue, small copy fog, isolated default style, weak but contained inconsistency. |

Interpretation:

- `0-15`: clean enough for strict production review.
- `16-30`: visible generated residue. Fix before high-stakes release.
- `31-55`: heavy slop. Remediation required.
- `56-75`: redesign likely faster than patching.
- `76-100`: reject. The design has no credible direction.

## Categories

### 1. Aesthetic Defaults

Flag:

- Blue-to-purple, indigo-to-pink, cyan-to-blue gradients.
- Gradient text used as personality.
- Glassmorphism as decoration: translucent cards, blur, glow borders.
- Dark neon backgrounds with cyan/violet orbs.
- White rounded card fields on white pages.
- Bokeh blobs, aurora meshes, particle decoration.
- One-hue palettes dominated by purple, blue, slate, beige, espresso, or orange.

Search:

```bash
rg -n "from-blue|to-purple|from-indigo|to-pink|from-cyan|to-blue|text-transparent|bg-clip-text" .
rg -n "backdrop-blur|bg-white/10|border-white/20|shadow-2xl|shadow-xl|blur-3xl|animate-pulse" .
rg -n "#6366[fF]1|#8[bB]5[cC][fF]6|indigo-500|violet-500|purple-600" .
```

### 2. Layout Formulae

Flag:

- Centered hero, vague subheadline, two CTAs, three feature cards.
- Six identical cards with icon, heading, paragraph.
- Same vertical padding on every section.
- Bento grid with arbitrary spans and no hierarchy.
- Default dashboard shell: sidebar, top bar, four stats, generic chart, activity feed.
- First viewport hides the product, object, place, tool, game, or primary task.

Search:

```bash
rg -n "grid-cols-3|grid-cols-4|md:grid-cols-3|lg:grid-cols-3|py-24|py-32|text-center" src app pages components
rg -n "Features|Testimonials|Pricing|Get Started|Start Free|Book a demo" src app pages components
```

### 3. Component Soup

Flag:

- Card around every object.
- Card inside card.
- Rounded icon tile above every feature heading.
- Generic icons that do not clarify meaning.
- Hover lift/scale/shadow on every card.
- Text buttons where a standard icon control is expected.

Search:

```bash
rg -n "rounded-2xl|rounded-3xl|hover:scale|hover:-translate-y|hover:shadow" src app pages components
rg -n "Sparkles|Zap|Shield|Rocket|Star|Award|CheckCircle|TrendingUp" src app pages components
```

### 4. Typography Sameness

Flag:

- Inter, Geist, Roboto, Plus Jakarta Sans, or Space Grotesk as the whole personality.
- `text-5xl font-bold tracking-tight` by reflex.
- Flat hierarchy.
- All labels as uppercase tiny tracked text.
- Tiny gray body copy.
- Negative letter spacing.

Search:

```bash
rg -n "Inter|Geist|Roboto|Plus Jakarta|Space Grotesk|tracking-tight|tracking-\\[-" .
rg -n "uppercase.*tracking-wider|text-xs.*uppercase|text-gray-400|text-slate-400" src app pages components
```

### 5. Motion Spam

Flag:

- Fade-in parade on every section.
- Bounce, wiggle, pulse, shimmer, or hover motion without state meaning.
- `transition-all` globally.
- Hover motion on non-interactive surfaces.
- No `prefers-reduced-motion`.

Search:

```bash
rg -n "fadeIn|fade-in|opacity-0|whileInView|animate-.*fade|animate-.*bounce|animate-.*pulse|transition-all" .
rg -n "prefers-reduced-motion" .
```

### 6. Copy Void

Flag:

- "Unlock", "empower", "streamline", "revolutionize", "seamless", "powerful", "innovative", "next-generation".
- "Built for teams", "all-in-one platform", "supercharge your workflow".
- Fake stats: "10K+ users", "99.9% uptime", "trusted by teams worldwide".
- Placeholder testimonials.
- CTAs that do not describe the next step.

Search:

```bash
rg -ni "unlock|empower|streamline|revolutionize|seamless|powerful|innovative|next-generation|all-in-one|supercharge" src app pages components
rg -ni "lorem|ipsum|placeholder|dummy|testimonial|trusted by|10k\\+|99\\.9%" src app pages components
```

### 7. Accessibility Slop

Flag:

- Low contrast gray text.
- `outline-none` without replacement.
- Icon-only buttons without accessible names.
- Hover-only content.
- Inputs without labels.
- Color-only status.
- Motion without reduced-motion.
- Tap targets too small.

Search:

```bash
rg -n "outline-none|focus:outline-none|focus:ring-0|aria-hidden|role=|aria-label|sr-only" src app pages components
rg -n "<input|<select|<textarea|button" src app pages components
```

### 8. Deceptive Patterns

Flag:

- Confirmshaming.
- Fake scarcity timers, fake stock pressure, fake activity.
- Hidden costs or commitments.
- Suppressed cancellation/delete/opt-out path.
- Primary button visually pushes expensive, irreversible, or unsafe action.

### 9. Asset Fakery

Flag:

- Abstract stock illustration for concrete product.
- AI image artifacts, impossible UI, fake charts, fake screenshots.
- Mixed icon/illustration styles.
- Decorative charts with no labels or scales.
- Generic ambiance where inspection matters.

### 10. Responsive and Performance Slop

Flag:

- Text overlaps or button labels overflow on mobile.
- Images/video without stable dimensions.
- Full viewport hero traps the page.
- Heavy filters, blurs, videos, and shadows with no purpose.
- Fonts causing layout shift.

Search:

```bash
rg -n "<img|next/image|Image\\s" src app pages components
rg -n "min-h-screen|h-screen|w-screen|overflow-hidden|blur-|backdrop-blur|filter|drop-shadow" src app pages components
```

### 11. Code and Design-System Smells

Flag:

- 15+ utility classes on many elements.
- Arbitrary values everywhere.
- Duplicate class strings instead of variants.
- One-off colors in components.
- No semantic tokens.
- Obvious comments narrating code.

Search:

```bash
rg -n "className=\"[^\"]*(\\s+[^\\s\"]+){15,}" src app pages components
rg -n "\\[[0-9#]|bg-\\[#|text-\\[#|p-\\[|m-\\[|w-\\[|h-\\[" src app pages components
```

### 12. Design Token Violation

Flag:

- Components bypass established tokens with raw hex, arbitrary Tailwind values, or local shadow/radius/color scales.
- Same semantic role has multiple colors, radii, spacing patterns, or focus treatments.
- Token names exist but do not map to actual UI meaning.
- Dark/light themes diverge without intent.

Search:

```bash
rg -n "bg-\\[#|text-\\[#|border-\\[#|shadow-\\[|rounded-\\[|#[0-9a-fA-F]{3,8}" src app pages components styles
rg -n "--color|--surface|--accent|theme\\(|tokens|semantic" src app pages components styles
```

### 13. Hierarchy Collapse

Flag:

- Everything has the same visual weight.
- Primary action, secondary action, metadata, and decoration compete.
- Cards repeat identical typography and spacing regardless of importance.
- First viewport lacks a clear reading path.
- Dashboard metrics are large but not decision-useful.

Signals:

- Repeated `font-semibold text-lg` headings in every card.
- Many equal-width columns with similar content length.
- CTA group where both buttons are styled as primary.

### 14. Brand Incoherence

Flag:

- Palette, type, shape, imagery, icon style, and copy voice do not belong to one product.
- Marketing surface and app surface feel unrelated.
- Brand signal is only a logo in the nav.
- Domain expectations are ignored: playful visuals for serious ops, stiff SaaS polish for expressive work, stock luxury for commodity goods.

### 15. Process Red Flags

Flag:

- The UI cannot explain why this color, layout, type, or image belongs to this product.
- Prompt only says "modern", "beautiful", "premium", or "sleek".
- No screenshot or browser verification after visual edits.
- No mobile pass.
- No content pass.

## Slop Signatures

A slop signature is a recognizable cluster. Detecting one increases severity because clusters are more damaging than isolated matches.

| Signature | Trigger Cluster | Default Severity |
| --- | --- | --- |
| `Startup Gradient Stack` | Gradient hero + vague SaaS copy + feature cards + two CTAs. | High |
| `Glass Feature Soup` | Glass cards + blur/glow + generic icons + hover lift. | High |
| `Dashboard Theater` | Four fake metrics + generic chart + activity feed + no decision path. | High |
| `Copy Fog Landing` | Buzzwords + fake proof + generic CTAs + no product evidence. | High |
| `Neon Orb Darkmode` | Dark slate + purple/cyan glow + gradient text + bokeh/orbs. | Medium/High |
| `Portfolio Template Drift` | Designer/developer portfolio using SaaS hero/cards instead of work evidence. | High |
| `Ecommerce Urgency Fog` | Fake scarcity + unclear price/charges + vague checkout action. | Critical |
| `Token Collapse` | Raw colors/radii/shadows across many components despite tokens. | High |
| `Motion Confetti` | Multiple animations without state meaning or reduced-motion support. | Medium/High |
| `Brand Costume` | Visual style copied from a trend with no relation to product/domain. | High |

## Scoring Rules

- Do not double-count repeated matches caused by one shared component. Score the component once and note fanout.
- Raise severity when the issue appears above the fold or in the primary workflow.
- Raise severity when the issue combines with a slop signature.
- Lower severity only when there is strong product-specific justification.
- Accessibility blockers, broken mobile, fake proof, and deception remain blockers regardless of score.
