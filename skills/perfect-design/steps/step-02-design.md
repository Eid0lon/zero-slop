# Step 02: Design and Edit

## Objective

Turn the contract into a real interface using the existing codebase style where it is coherent, and improving the system only where it blocks premium output.

## Actions

1. Load `references/composition-playbook.md`, `references/product-archetypes.md`, and `references/interaction-accessibility.md`.
2. Map the surface:
   - primary workflow
   - navigation and IA
   - reusable components
   - states and edge cases
   - visual tokens
   - data/media dependencies
3. Choose scope:
   - `create`: build the actual usable experience first.
   - `redesign`: rebuild structure, tokens, content hierarchy, and interaction.
   - `polish`: refine hierarchy, tokens, copy, states, and responsive behavior without product churn.
4. Edit files in the smallest coherent set.
5. Keep code and style consistent with the local stack.
6. Avoid fake proof, filler data, and ornamental complexity.
7. Run deterministic prechecks when available:

```bash
python perfect-design/scripts/perfect_design_cli.py --audit <target>
python no-slop/scripts/no_slop_cli.py --scan <target>
```

## Edit Priorities

1. Product clarity and first viewport.
2. IA and workflow completion.
3. Typography, spacing, density, and hierarchy.
4. Token coherence and component states.
5. Accessibility, keyboard, focus, responsive stability.
6. Motion and feedback.
7. Visual distinction without trend costume.

## Output

```markdown
# Design Pass

Design thesis:

## Changed
- file - change

## Decisions
- concrete choice and why it fits the product

## Prechecks
- command - result
```

## Next Step

Load `step-03-no-slop.md`.
