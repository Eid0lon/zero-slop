# Interaction and Accessibility

## Interaction Quality

Senior interfaces feel good because state changes are legible.

Required states:

- default
- hover
- focus-visible
- active/pressed
- disabled with explanation when relevant
- loading
- empty
- error
- success
- selected/current
- expanded/collapsed

## Keyboard

- Preserve native controls whenever possible.
- Use proven primitives for dialogs, menus, comboboxes, tabs, sliders, popovers, and command palettes.
- Match WAI-ARIA Authoring Practices for custom widgets.
- Keep tab order aligned with visual and task order.
- Put focus inside dialogs and return it after close.
- For command palettes, support search, arrow navigation, Enter, Escape, and clear action grouping.

## Focus

- Never remove focus without a replacement.
- Focus must be visible on all surfaces.
- Prefer two-color focus indicators when backgrounds vary.
- Focus style is part of the design system, not a browser accident.

## Motion

- Motion must explain:
  - state change
  - continuity
  - spatial relationship
  - feedback
  - progress
  - reordering
- Do not delay reading content for animation.
- Honor `prefers-reduced-motion`.
- Animate transform and opacity when possible.
- Avoid blur/filter-heavy motion unless the domain justifies the cost.

## Responsive Stability

- Test at mobile and desktop.
- Avoid fixed viewport traps.
- Prevent text overflow in buttons, cards, tabs, badges, and toolbars.
- Prevent status/alert lines and command strips from clipping at `375px-430px`; wrap or stack them deliberately.
- Use `aspect-ratio`, explicit media dimensions, grid constraints, and min/max widths.
- Do not scale fonts with viewport width.

## Accessibility Gate

Block shipping for:

- inaccessible custom controls
- missing labels on icon buttons or inputs
- color-only status
- low contrast text or focus
- keyboard traps
- hidden primary workflows
- reduced-motion violations
- mobile screenshot clipping of primary status, filters, commands, or actions
- touch targets that are too small for the context

## Performance as Craft

- Reserve image/video space to prevent layout shift.
- Avoid heavy global filters and excessive shadows.
- Avoid late-loading fonts that reflow layout.
- Keep interactions responsive.
- Treat CLS, LCP, and INP as design concerns when a browser/performance pass is available.
