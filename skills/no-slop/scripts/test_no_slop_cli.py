#!/usr/bin/env python3
"""Regression tests for the deterministic no-slop CLI."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("no_slop_cli", SCRIPT_DIR / "no_slop_cli.py")
assert SPEC and SPEC.loader
cli = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = cli
SPEC.loader.exec_module(cli)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class NoSlopCliRegressionTests(unittest.TestCase):
    def test_code_structure_anchors_and_theme_tokens_are_not_slop(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(
                root / "src" / "App.jsx",
                """
import Features from './components/Features'
import Pricing from './components/Pricing'

export default function App() {
  return (
    <main className="min-h-screen bg-surface-950 text-surface-50">
      <a href="#features">See pricing</a>
      <Features />
      <Pricing />
    </main>
  )
}
""",
            )
            write(
                root / "src" / "components" / "Features.jsx",
                """
const featuresRow = [
  { title: 'Routes tasks from meetings', description: 'Assigns action items to owners.' },
]

export default function Features() {
  return (
    <section id="features">
      {/* Testimonials header */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {featuresRow.map(feature => <article key={feature.title}>{feature.title}</article>)}
      </div>
    </section>
  )
}
""",
            )
            write(
                root / "src" / "index.css",
                """
@import "tailwindcss";
@theme {
  --color-surface-950: #0C0A09;
  --color-surface-50: #FAFAF9;
}
""",
            )

            scan = cli.scan_target(root)

        self.assertEqual(scan["category_scores"].get("Design Token Violation", 0), 0)
        self.assertEqual(scan["severity_counts"].get("High", 0), 0)
        self.assertLessEqual(scan["score"], 20)

    def test_legitimate_tailwind_and_form_context_stays_clean(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(
                root / "src" / "Dashboard.jsx",
                """
export function Dashboard() {
  return (
    <main className="min-h-screen bg-[var(--surface)] text-[var(--foreground)]">
      <h1 className="text-2xl font-semibold tracking-tight">Invoice review</h1>
      <button
        aria-label="Create invoice"
        className="rounded-2xl hover:scale-[1.01] focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--ring)]"
      >
        Create invoice
      </button>
      <label htmlFor="invoice-filter">Filter invoices</label>
      <input id="invoice-filter" placeholder="Search invoices" />
    </main>
  )
}
""",
            )

            scan = cli.scan_target(root)
            gate = cli.judge(scan, cli.DEFAULT_DIALS, economy=False)

        self.assertLessEqual(scan["score"], 8)
        self.assertNotIn("accessibility risk detected", gate["hard_blockers"])

    def test_clean_product_brief_has_no_hidden_prompt_tax(self) -> None:
        scan = cli.scan_prompt("clean invoice dashboard with semantic tokens and keyboard accessible filters")

        self.assertEqual(scan["score"], 0)
        self.assertEqual(scan["category_counts"], {})

    def test_obvious_ai_saas_prompt_still_fails_hard(self) -> None:
        scan = cli.scan_prompt(
            "Build a modern premium AI SaaS landing page with a blue-to-purple gradient hero, "
            "glass cards, Features, Testimonials, Pricing, 10k+ users, 99.9% uptime, "
            "unlock seamless productivity, hover scale cards, smooth animations"
        )
        names = {signature["name"] for signature in scan["signatures"]}

        self.assertEqual(scan["score"], 100)
        self.assertIn("Dashboard Theater", names)
        self.assertIn("Copy Fog Landing", names)

    def test_low_confidence_focus_reset_does_not_create_accessibility_blocker(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(
                root / "src" / "Button.jsx",
                """
export function Button() {
  return (
    <button className="focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--ring)]">
      Save invoice
    </button>
  )
}
""",
            )

            scan = cli.scan_target(root)
            gate = cli.judge(scan, cli.DEFAULT_DIALS, economy=False)
            report = cli.build_autopsy({"scan": scan, "judge": gate})

        self.assertEqual(scan["category_scores"].get("Accessibility Slop", 0), 1)
        self.assertNotIn("accessibility risk detected", gate["hard_blockers"])
        self.assertTrue(
            all(judge["blocker"] != "focus/accessibility risk detected" for judge in gate["judges"])
        )
        self.assertEqual(report["reality_handoff"]["recommendation"], "OPTIONAL")

    def test_low_score_strong_aesthetic_is_not_called_low_confidence_residue(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(
                root / "src" / "Hero.jsx",
                """
export function Hero() {
  return (
    <h1 className="bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent">
      Ship faster
    </h1>
  )
}
""",
            )

            scan = cli.scan_target(root)
            gate = cli.judge(scan, cli.DEFAULT_DIALS, economy=False)
            report = cli.build_autopsy({"scan": scan, "judge": gate})

        self.assertGreater(scan["score"], 0)
        self.assertTrue(cli.has_strong_finding(scan, "Aesthetic Defaults"))
        self.assertNotIn("low-confidence residue", report["cause_of_death"])

    def test_visible_pricing_text_is_not_erased_by_href_or_id_context(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(
                root / "src" / "Pricing.jsx",
                """
export function Pricing() {
  return (
    <section id="pricing">
      <h2>Pricing</h2>
      <a href="#pricing">Pricing</a>
      <a href="#features">See pricing</a>
    </section>
  )
}
""",
            )

            scan = cli.scan_target(root)

        self.assertGreater(scan["category_scores"].get("Layout Formulae", 0), 0)
        self.assertEqual(scan["severity_counts"].get("High", 0), 0)

    def test_repeated_focus_resets_with_replacements_do_not_create_role_blocker(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            buttons = "\n".join(
                f"""
      <button className="focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--ring)]">
        Save invoice {index}
      </button>
"""
                for index in range(6)
            )
            write(
                root / "src" / "Toolbar.jsx",
                f"""
export function Toolbar() {{
  return (
    <div>
{buttons}
    </div>
  )
}}
""",
            )

            scan = cli.scan_target(root)
            gate = cli.judge(scan, cli.DEFAULT_DIALS, economy=False)

        self.assertGreaterEqual(scan["category_scores"].get("Accessibility Slop", 0), 4)
        self.assertFalse(cli.has_strong_finding(scan, "Accessibility Slop"))
        self.assertTrue(
            all(judge["blocker"] != "focus/accessibility risk detected" for judge in gate["judges"])
        )

    def test_filter_copy_and_array_methods_are_not_css_filter_effects(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write(
                root / "src" / "Queue.jsx",
                """
export function Queue({ orders }) {
  const state = { filter: 'open' }
  const filter = 'open'
  const visible = orders.filter(order => order.status === filter)
  return (
    <section>
      <div className="segmented" aria-label="Queue filter">
        <button>Open</button>
      </div>
      {visible.map(order => <article key={order.id}>{order.title}</article>)}
    </section>
  )
}
""",
            )

            scan = cli.scan_target(root)

        self.assertEqual(scan["category_scores"].get("Responsive and Performance Slop", 0), 0)


if __name__ == "__main__":
    unittest.main()
