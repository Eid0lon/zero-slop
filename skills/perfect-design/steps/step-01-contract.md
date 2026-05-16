# Step 01: Design Contract

## Objective

Create a product-specific contract before changing UI. This prevents decorative guessing and gives judges something concrete to enforce.

## Actions

1. Load `references/design-contract.md`.
2. Inspect any existing UI, tokens, components, routes, assets, and copy.
3. If `no-slop` is available and the target exists, run its scan or equivalent workflow before editing.
4. Identify:
   - user and context
   - primary job
   - first viewport obligation
   - domain expectations
   - data/content/proof that must be real
   - design thesis
   - layout model
   - palette/type/radius/elevation/token strategy
   - interaction model
   - accessibility and responsive constraints
   - forbidden defaults
5. Reject the contract if it could fit any unrelated product.

## Output

```markdown
# Design Contract

Status:
Preset:
Dials:
No-slop precheck:

## Product
User:
Primary job:
Domain:
First viewport obligation:

## Direction
Design thesis:
Layout:
Typography:
Palette:
Shape/elevation:
Motion:
Assets/data:
Copy voice:

## Gates
- measurable acceptance gates

## Forbidden
- exact defaults this task must not use
```

## Next Step

- If contract passes, load `step-02-design.md`.
- If contract fails twice, load `references/self-coaching.md`, revise once more, then block or ask for missing product facts.
