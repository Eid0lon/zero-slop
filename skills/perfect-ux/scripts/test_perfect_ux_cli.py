#!/usr/bin/env python3
"""Regression tests for the deterministic perfect-ux CLI."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("perfect_ux_cli", SCRIPT_DIR / "perfect_ux_cli.py")
assert SPEC and SPEC.loader
cli = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = cli
SPEC.loader.exec_module(cli)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class PerfectUxCliRegressionTests(unittest.TestCase):
    def test_detects_dead_action_fake_proof_and_generic_cta(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(
                root / "src" / "Landing.jsx",
                """
export default function Landing() {
  return (
    <main>
      <p>Trusted by 10k+ teams with AI-powered guaranteed accurate decisions.</p>
      <a href="#">Get started</a>
      <button onClick={() => console.log("save")}>Submit</button>
    </main>
  )
}
""",
            )

            scan = cli.scan_target(root)
            gate = cli.judge(scan, cli.DEFAULT_DIALS, economy=False)

        self.assertEqual(scan["severity_counts"].get("Critical"), 2)
        self.assertIn("primary action may be dead or fake", gate["hard_blockers"])
        self.assertIn("trust or unsupported-claim risk", gate["hard_blockers"])
        self.assertEqual(gate["gate"], "FAIL")

    def test_clean_form_with_recovery_and_focus_passes_deterministic_precheck(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(
                root / "src" / "InvoiceForm.jsx",
                """
export function InvoiceForm() {
  const status = "success"
  return (
    <main>
      <form aria-busy={status === "saving"}>
        <label htmlFor="invoice-email">Billing email</label>
        <input id="invoice-email" required aria-invalid={false} />
        <p id="invoice-help">Use the address that receives invoice updates.</p>
        <button className="focus:outline-none focus-visible:ring-2">Save invoice</button>
        <button type="button">Cancel</button>
        <button type="button">Retry sync</button>
        <p role="status">Saved. You can undo the last change.</p>
      </form>
    </main>
  )
}
""",
            )

            scan = cli.scan_target(root)
            gate = cli.judge(scan, cli.DEFAULT_DIALS, economy=False)

        self.assertEqual(scan["severity_counts"].get("Critical"), 0)
        self.assertEqual(scan["hard_blockers"], [])
        self.assertGreaterEqual(scan["ux_score"], 88)
        self.assertEqual(gate["gate"], "PRECHECK_PASS_PANEL_REQUIRED")

    def test_contract_missing_recovery_and_evidence_fails(self) -> None:
        scan = cli.contract_scan("Dashboard for operators to review delayed shipments from the alerts page.")

        self.assertIn("missing_contract_terms", scan)
        self.assertIn("recovery", scan["missing_contract_terms"])
        self.assertIn("evidence", scan["missing_contract_terms"])
        self.assertTrue(scan["hard_blockers"])

    def test_focus_reset_with_visible_replacement_is_not_critical(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(
                root / "src" / "Button.jsx",
                """
export function Button() {
  return <button className="focus:outline-none focus-visible:ring-2">Save report</button>
}
""",
            )

            scan = cli.scan_target(root)

        self.assertEqual(scan["severity_counts"].get("Critical"), 0)
        self.assertNotIn("critical task completion or accessibility risk", scan["hard_blockers"])

    def test_placeholder_input_without_label_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(
                root / "src" / "Search.jsx",
                """
export function Search() {
  return <input placeholder="Search customers" />
}
""",
            )

            scan = cli.scan_target(root)

        self.assertGreater(scan["risk_category_counts"].get("Input", 0), 0)
        self.assertIn("form/input labeling or validation risk", scan["hard_blockers"])

    def test_placeholder_input_with_id_but_no_label_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(
                root / "src" / "Search.jsx",
                """
export function Search() {
  return <input id="customer-search" placeholder="Search customers" />
}
""",
            )

            scan = cli.scan_target(root)

        self.assertGreater(scan["risk_category_counts"].get("Input", 0), 0)
        self.assertIn("form/input labeling or validation risk", scan["hard_blockers"])

    def test_placeholder_input_with_matching_label_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(
                root / "src" / "Search.jsx",
                """
export function Search() {
  return (
    <form>
      <label htmlFor="customer-search">Search customers</label>
      <input id="customer-search" placeholder="Customer name or email" />
    </form>
  )
}
""",
            )

            scan = cli.scan_target(root)

        self.assertEqual(scan["risk_category_counts"].get("Input", 0), 0)
        self.assertNotIn("form/input labeling or validation risk", scan["hard_blockers"])

    def test_invalid_dial_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            cli.resolve_dials(None, ["NOPE=9"])


if __name__ == "__main__":
    unittest.main()
