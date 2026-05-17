#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reality_cli import RULES, scan_file, summarize


class RealityCliTests(unittest.TestCase):
    def test_detects_dead_href_and_console_handler(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "App.tsx"
            source.write_text(
                '<a href="#">Open</a>\n<button onClick={() => console.log("save")}>Save</button>\n',
                encoding="utf-8",
            )

            findings = scan_file(source, RULES, root)
            codes = {finding.code for finding in findings}

            self.assertIn("DEAD_HREF", codes)
            self.assertIn("CONSOLE_HANDLER", codes)
            self.assertTrue(summarize(findings)["hard_fail"])

    def test_clean_file_has_no_findings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "App.tsx"
            source.write_text(
                '<button type="submit">Save</button>\n<p>Saved in this browser</p>\n',
                encoding="utf-8",
            )

            findings = scan_file(source, RULES, root)

            self.assertEqual([], findings)
            self.assertEqual("NO_DEMOWARE_SIGNALS_FOUND", summarize(findings)["decision"])


if __name__ == "__main__":
    unittest.main()
