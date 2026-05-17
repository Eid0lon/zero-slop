# zero-slop

<p align="center">
  <img src="https://img.shields.io/badge/license-Apache%202.0-blue?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/status-early%20public-important?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/skills-3-success?style=flat-square" alt="Skills">
</p>

Three agent skills to help your AI-generated interfaces feel like *your* product — not like every other AI output on the web.

> **Repo:** [github.com/Eid0lon/zero-slop](https://github.com/Eid0lon/zero-slop)

- [What it does](#what-it-does)
- [What this is not](#what-this-is-not)
- [The three skills](#the-three-skills)
- [Install](#install)
- [Commands](#commands)
- [Scan vs Autopsy](#scan-vs-autopsy)
- [How they work together](#how-they-work-together)
- [What it looks for](#what-it-looks-for)
- [Example](#example)
- [Dials and presets](#dials-and-presets)
- [FAQ](#faq)
- [License](#license)

---

## What it does

AI coding agents tend to reach for the same visual habits — purple gradients, glass cards, "empower your workflow" headlines, three centered feature cards above the fold. These are pulled from training data, not shaped by *your* product.

`no-slop` reviews your frontend code for these patterns and gives you a friendly report with a score and actionable suggestions. `perfect-design` helps you define the right direction before any code is written. `reality-skill` makes sure the result is a working product, not just a pretty screenshot.

Together they form a gentle pipeline: `no-slop` spots the generic bits, `perfect-design` builds a product-specific replacement, and `reality-skill` completes the workflow so it actually works end-to-end.

---

## What this is not

- Not a replacement for a human designer — think of it as a co-pilot, not an autopilot.
- Not a visual AI model — it works with code, not pixels.
- Not a one-size-fits-all design system — it adapts to your product archetype.
- Not a guarantee of perfection — but it raises the floor considerably.
- Not a taste enforcer — it focuses on practical QA, review, and anti-cliché checks.

---

## The three skills

### `no-slop` — spot and improve generic UI

- Reviews `.tsx`, `.jsx`, `.vue`, `.svelte`, `.css`, `.html` files with a context-aware engine (not just regex counting)
- Gives a 0–100 score and names the patterns it found
- Produces an AI UI Autopsy: a human-readable summary of what feels off, which lines are involved, confidence level, counter-evidence, and suggested fix order
- Runs a 6-role review protocol to decide if the UI passes muster
- Can apply targeted improvements (`--fix`) or rethink the whole surface (`--redesign`)
- Also works on briefs before any code is generated (`--prevent`)

### `perfect-design` — build product-specific UI

- Writes a Design Contract (who it's for, what job it does, the domain, and key visual choices) before touching code
- Has 6 product archetypes (operational SaaS, dashboard, commerce, portfolio, editorial, dev tool) to set the right expectations
- Scores UI against a 14-dimension rubric
- Works hand-in-hand with `no-slop` — runs it before and after every design pass

### `reality-skill` — turn demos into real workflows

- Traces the primary user journey from entry to completion
- Catches dead buttons, placeholder data, fake claims, decorative-only dashboards, and stub handlers
- Asks for proper loading, empty, error, disabled, success, validation, persistence, and navigation states
- Respects honest local/mock boundaries when production services aren't available yet
- Keeps changes focused: finish the workflow without redesigning everything

---

## Install

```bash
npx skills add Eid0lon/zero-slop
```

Then activate the skills you need in your agent.

## Commands

### `no-slop`

| Command | What it does |
|---|---|
| `--autopsy` | A friendly forensic report: overall verdict, what's causing the issue, which lines are involved, and what to address first |
| `--scan` | Quick deterministic scan: 0–100 score, categories, signatures, and findings — great for debugging or CI |
| `--fix` | Targeted improvements on specific issues |
| `--redesign` | A fresh pass when the score calls for more than small tweaks |
| `--judge` | Runs the 6-role review protocol |
| `--prevent` | Reviews a brief before any code is generated |
| `-e` | Economy mode — deterministic checks only, no live judges needed |

### `perfect-design`

| Command | What it does |
|---|---|
| `--contract` | Writes a Design Contract from a brief |
| `--create` | Builds a new UI from a contract |
| `--redesign` | Rebuilds direction, layout, tokens, and copy |
| `--polish` | Refines an existing UI while keeping the product model intact |
| `--judge` | Runs the premium review protocol |
| `--verify` | Build, lint, browser, and accessibility checks |
| `-e` | Economy mode — deterministic checks only, no live judges needed |

### `reality-skill`

Reality Skill is a workflow skill rather than a CLI command. Invoke it whenever an app, dashboard, form, checkout, onboarding flow, settings page, or CRUD surface needs to go beyond a static mockup.

---

## Scan vs Autopsy

`scan` and `autopsy` use the same engine under the hood, but they're made for different moments.

Use `--autopsy` when you want to understand what's going on:

```bash
no-slop --autopsy path/to/ui
```

Autopsy tells you whether the surface is `CLEAN`, `RESIDUE`, `CONTAMINATED`, or `CRITICAL`, explains why it landed there, what patterns were spotted, and what to tackle first. This is the go-to for reviews, before/after comparisons, sharing with teammates, and deciding if a UI actually needs attention.

Use `--scan` when you want the raw numbers:

```bash
no-slop --scan path/to/ui
no-slop --scan --json path/to/ui
```

Scan gives you the calibrated score, category breakdowns, matching signatures, and exact findings. Handy for debugging a specific line, writing tests, gating CI, or piping into another tool. In short: autopsy is the human-friendly report; scan is the machine-readable data underneath.

---

## How they work together

```
1. perfect-design --contract     —  decide what your product is before writing code
2. no-slop --autopsy             —  understand where the current UI stands
3. perfect-design --create/polish —  build or refine the interface
4. no-slop --scan --json         —  debug specific findings or add CI checks
5. no-slop --judge               —  verify nothing generic slipped through
6. perfect-design --judge        —  verify the result feels product-specific
7. reality-skill                 —  verify the primary workflow actually works
8. perfect-design --verify       —  build, lint, browser, a11y checks
```

If `no-slop` isn't available, `perfect-design` notes it and applies a local checklist. It never claims a pass it can't back up.

---

## What it looks for

Here are a few things the scanner keeps an eye out for:

- Hero sections with blue-to-purple or indigo-to-pink gradients
- Glassmorphism cards with backdrop blur
- Feature grids with Sparkles / Shield / Rocket icons
- Copy like "Unlock seamless productivity" or "Empower your workflow"
- Made-up stats ("10K+ users", "99.9% uptime")
- `focus:outline-none` with no visible focus replacement
- Hover scale or lift applied indiscriminately to every card
- Animations that don't respect `prefers-reduced-motion`
- Hardcoded hex colors bypassing design tokens

The full pattern catalog and scoring rules live in `skills/no-slop/references/ai-slop-patterns.md`.

---

## Example

Prompt:

> Build a modern, premium landing page for an AI SaaS that helps teams automate their productivity.
>
> Make it ultra professional, futuristic, with a clean and premium design. Include:
>
> - Hero section with big headline, powerful subheadline, and two CTA buttons
> - Features section with 6 cards
> - Testimonials section
> - Pricing tiers (3 plans)
> - FAQ
> - Footer
>
> Use React + Tailwind CSS. Modern style with gradients, glassmorphism, smooth animations, elegant dark mode. Make it visually stunning and convincing.
>
> Full code, responsive, ready to ship.

| Before | After |
|---|---|
| ![](examples/before.png) | ![](examples/after.png) |

---

## Dials and presets

`no-slop` and `perfect-design` use dials (0–10 sliders) to adjust how strict the checks are. A preset is just a handy bundle of dial values for common product types. `reality-skill` uses fixed workflow gates instead of dials.

| Preset | What it expects |
|---|---|
| `saas` | Product proof over marketing fluff, no fake dashboards |
| `dashboard` | Dense tables, clear filters, labeled charts, keyboard paths |
| `ecommerce` | Price/shipping clarity, honest comparison, no fake scarcity |
| `portfolio` | Work evidence over trait cards, real case studies |
| `brutalist` | Deliberate rawness, not carelessness |
| `minimal` | Fewer elements, sharper choices, high contrast |
| `editorial` | Typography, imagery, voice, pacing |
| `ai-tool` | Task controls, sources, constraints, error recovery |

---

## FAQ

<details>
<summary>Does this replace a human designer?</summary>
Not at all. It helps spot generic patterns and keeps decisions product-focused, but it doesn't replace taste, strategy, or visual craft. Think of it as a thoughtful reviewer, not a replacement for your designer.
</details>

<details>
<summary>Do I need to use every skill?</summary>
Nope. `no-slop` works great on its own for reviewing generic patterns. `perfect-design` adds direction and a deeper rubric when you want it. `reality-skill` is for apps and workflows that need to go beyond a static mockup. Pick what fits your needs.
</details>

<details>
<summary>Does it work with any framework?</summary>
Reviews `.tsx`, `.jsx`, `.vue`, `.svelte`, `.astro`, `.css`, `.scss`, `.html`, and `.mdx`. The ideas apply to any stack — you can point the CLI at any directory.
</details>

<details>
<summary>What's economy mode?</summary>
`-e` skips the live subagent judges and runs deterministic local checks only. Same standards, lighter on resources. Great for quick scans or when subagents aren't available.
</details>

<details>
<summary>Can I contribute or share feedback?</summary>
Absolutely. This is an early public release. Open an issue, send a PR, or share a before/after example — all welcome.
</details>

---

## License

[Apache 2.0](https://github.com/Eid0lon/zero-slop/blob/main/LICENSE)

Copyright (c) 2026
