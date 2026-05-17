# Step 03: Real Implementation

Implement the smallest coherent product workflow.

1. Reuse existing project structure, routes, components, stores, API clients, schemas, and validation libraries.
2. Define or extend the data model.
3. Wire every primary action to a real state transition, route, API call, store update, or disabled truth boundary.
4. Add validation and preserve input on error.
5. Add persistence at the appropriate layer.
6. Add empty/loading/error/success/disabled states required by the workflow.
7. Add recovery paths: retry, cancel, back, edit, delete/undo where relevant.
8. Remove or relabel fake claims/data.
9. Keep visual design unless it blocks usability or honesty.

Prefer narrowly scoped edits. Do not redesign the product unless the current UI structure prevents the workflow from being real.

