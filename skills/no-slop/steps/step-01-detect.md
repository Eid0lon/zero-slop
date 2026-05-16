# Step 01: Detect

## Objective

Find AI-slop patterns in source code and, when possible, rendered UI.

## Actions

1. Discover relevant files:

```bash
rg --files {target} | rg "\\.(tsx|jsx|ts|js|vue|svelte|astro|css|scss|sass|less|html|mdx|md)$"
```

2. Run targeted searches from `references/ai-slop-patterns.md`.

3. Read suspicious files:
   - Main route/home/landing surfaces.
   - App shell and dashboard pages.
   - Shared Button/Card/Input/Nav/Dialog components.
   - Global styles, tokens, Tailwind config, CSS variables.
   - Files with the most pattern hits.

4. Inspect rendered UI when a local app/server can run:
   - Desktop viewport.
   - Mobile viewport.
   - First viewport framing.
   - Text overflow/overlap.
   - Keyboard focus.
   - Reduced motion when motion exists.

5. Score:
   - Use severity points from `ai-slop-patterns.md`.
   - Avoid double-counting one shared component.
   - Add slop signatures when clusters appear.
   - Report confidence.

6. If economy mode is false, prepare judge context:
   - scan summary
   - top suspicious files
   - screenshots if available
   - active preset and dials

## Output

```markdown
# Detection

Target:
Files scanned:
Project type:
AI-slop score:
Slop signatures:
Confidence:

## Findings by Severity
### Critical
### High
### Medium
### Low

## Category Breakdown
| Category | Count | Score |
```

## Next Step

- If mode is `scan`, load `step-04-judge.md` unless economy mode is true, then report.
- If mode is `judge`, load `step-04-judge.md`.
- If mode is `fix` or `redesign`, load `step-03-remediate.md`.
