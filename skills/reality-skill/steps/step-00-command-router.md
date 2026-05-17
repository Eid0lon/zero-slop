# Step 00: Command Router

1. Parse explicit `reality` command flags using `references/command-interface.md`.
2. If no command is present, infer mode:
   - existing UI + "fix", "make real", "functional", or app completion language: `--fix`
   - review language: `--audit`
   - new app/tool/dashboard request: `--build`
   - launch/QA/solid/harden language: `--harden`
3. Discover target:
   - inspect user-provided path first
   - otherwise inspect project files with `rg --files`
   - find package/config/routes/components/stores/API modules
4. Load only the needed references:
   - always load `references/reality-gates.md`
   - load `references/app-archetypes.md` after identifying the app type
   - load `references/implementation-playbook.md` for editing modes
   - load `references/truth-boundaries.md` when fake services/data are involved
   - load `references/verification-playbook.md` before verifying
   - load `references/judge-system.md` for judge/harden/final score
5. Continue to:
   - Step 01 for contract
   - Step 02 for forensic audit
   - Step 03 for implementation
   - Step 04 for verification and judge

Maintain the required state block from `SKILL.md` throughout.

