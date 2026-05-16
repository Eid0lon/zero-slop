#!/usr/bin/env python3
"""Deterministic helper CLI for the perfect-design skill.

The skill workflow remains the authority for edits, browser checks, no-slop
composition, and live subagent judging. This script provides a local precheck
for contracts and UI source files.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


DIAL_NAMES = (
    "CRAFT_STRICTNESS",
    "DENSITY",
    "BRAND_SPECIFICITY",
    "HIERARCHY_CONTRAST",
    "INTERACTION_DEPTH",
    "MOTION_DISCIPLINE",
    "CONTENT_PRECISION",
    "SYSTEM_COHERENCE",
    "A11Y_RIGOR",
    "DISTINCTIVENESS",
)

DEFAULT_DIALS: Dict[str, int] = {
    "CRAFT_STRICTNESS": 9,
    "DENSITY": 6,
    "BRAND_SPECIFICITY": 8,
    "HIERARCHY_CONTRAST": 9,
    "INTERACTION_DEPTH": 6,
    "MOTION_DISCIPLINE": 8,
    "CONTENT_PRECISION": 9,
    "SYSTEM_COHERENCE": 9,
    "A11Y_RIGOR": 10,
    "DISTINCTIVENESS": 7,
}

PRESETS: Dict[str, Dict[str, int]] = {
    "operational-saas": {
        "CRAFT_STRICTNESS": 10,
        "DENSITY": 8,
        "BRAND_SPECIFICITY": 6,
        "HIERARCHY_CONTRAST": 9,
        "INTERACTION_DEPTH": 8,
        "MOTION_DISCIPLINE": 9,
        "CONTENT_PRECISION": 9,
        "SYSTEM_COHERENCE": 10,
        "A11Y_RIGOR": 10,
        "DISTINCTIVENESS": 5,
    },
    "developer-tool": {
        "CRAFT_STRICTNESS": 10,
        "DENSITY": 7,
        "BRAND_SPECIFICITY": 8,
        "HIERARCHY_CONTRAST": 9,
        "INTERACTION_DEPTH": 8,
        "MOTION_DISCIPLINE": 9,
        "CONTENT_PRECISION": 10,
        "SYSTEM_COHERENCE": 10,
        "A11Y_RIGOR": 10,
        "DISTINCTIVENESS": 6,
    },
    "dashboard": {
        "CRAFT_STRICTNESS": 10,
        "DENSITY": 9,
        "BRAND_SPECIFICITY": 5,
        "HIERARCHY_CONTRAST": 10,
        "INTERACTION_DEPTH": 8,
        "MOTION_DISCIPLINE": 10,
        "CONTENT_PRECISION": 9,
        "SYSTEM_COHERENCE": 10,
        "A11Y_RIGOR": 10,
        "DISTINCTIVENESS": 4,
    },
    "editorial": {
        "CRAFT_STRICTNESS": 9,
        "DENSITY": 5,
        "BRAND_SPECIFICITY": 10,
        "HIERARCHY_CONTRAST": 10,
        "INTERACTION_DEPTH": 6,
        "MOTION_DISCIPLINE": 7,
        "CONTENT_PRECISION": 9,
        "SYSTEM_COHERENCE": 9,
        "A11Y_RIGOR": 10,
        "DISTINCTIVENESS": 9,
    },
    "commerce": {
        "CRAFT_STRICTNESS": 10,
        "DENSITY": 8,
        "BRAND_SPECIFICITY": 8,
        "HIERARCHY_CONTRAST": 9,
        "INTERACTION_DEPTH": 8,
        "MOTION_DISCIPLINE": 9,
        "CONTENT_PRECISION": 10,
        "SYSTEM_COHERENCE": 10,
        "A11Y_RIGOR": 10,
        "DISTINCTIVENESS": 6,
    },
    "portfolio": {
        "CRAFT_STRICTNESS": 9,
        "DENSITY": 5,
        "BRAND_SPECIFICITY": 10,
        "HIERARCHY_CONTRAST": 9,
        "INTERACTION_DEPTH": 6,
        "MOTION_DISCIPLINE": 7,
        "CONTENT_PRECISION": 9,
        "SYSTEM_COHERENCE": 9,
        "A11Y_RIGOR": 10,
        "DISTINCTIVENESS": 10,
    },
}

SCAN_SUFFIXES = {
    ".tsx",
    ".jsx",
    ".ts",
    ".js",
    ".vue",
    ".svelte",
    ".astro",
    ".css",
    ".scss",
    ".sass",
    ".less",
    ".html",
    ".mdx",
}

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".next",
    ".nuxt",
    ".svelte-kit",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".turbo",
    ".cache",
    "__pycache__",
    "agents",
    "references",
    "scripts",
    "steps",
}


@dataclass(frozen=True)
class Rule:
    category: str
    severity: str
    points: int
    regex: re.Pattern[str]
    reason: str
    kind: str = "risk"


@dataclass
class Finding:
    file: str
    line: int
    category: str
    severity: str
    points: int
    reason: str
    excerpt: str
    kind: str


RISK_RULES: Sequence[Rule] = (
    Rule("Contract", "High", 8, re.compile(r"\bmodern\b|\bclean\b|\bpremium\b|\bsleek\b|\bbeautiful\b|make it pop", re.I), "abstract style word without concrete design decision"),
    Rule("Product Proof", "High", 8, re.compile(r"lorem|ipsum|placeholder|dummy|trusted by|10k\+|99\.9%", re.I), "placeholder or unsupported proof"),
    Rule("Copy", "Medium", 4, re.compile(r"unlock|empower|streamline|revolutionize|seamless|powerful|innovative|next-generation|all-in-one|supercharge", re.I), "generic copy weakens product specificity"),
    Rule("Aesthetic", "Medium", 4, re.compile(r"from-blue|to-purple|from-indigo|to-pink|text-transparent|bg-clip-text|backdrop-blur|blur-3xl", re.I), "template aesthetic signal"),
    Rule("Layout", "Medium", 4, re.compile(r"Features|Testimonials|Pricing|Get Started|Learn More|Book a demo", re.I), "formulaic section or CTA"),
    Rule("Component", "Medium", 4, re.compile(r"rounded-2xl|rounded-3xl|hover:scale|hover:-translate-y|hover:shadow", re.I), "overused component styling"),
    Rule("Accessibility", "Critical", 15, re.compile(r"outline-none|focus:outline-none|focus:ring-0", re.I), "focus visibility risk"),
    Rule("Responsive", "High", 8, re.compile(r"h-screen|w-screen|overflow-hidden", re.I), "viewport trap or overflow risk"),
    Rule("Motion", "Medium", 4, re.compile(r"transition-all|animate-.*pulse|animate-.*bounce|whileInView|fadeIn|fade-in", re.I), "motion may lack purpose or reduced-motion proof"),
    Rule("Tokens", "High", 8, re.compile(r"bg-\[#|text-\[#|border-\[#|shadow-\[|rounded-\[|#[0-9a-fA-F]{3,8}"), "raw values may bypass semantic tokens"),
    Rule("Implementation", "Medium", 4, re.compile(r"className=\"[^\"]*(\s+[^\s\"]+){18,}"), "long utility class string may hide system decisions"),
)

POSITIVE_RULES: Sequence[Rule] = (
    Rule("Product Proof", "Positive", 5, re.compile(r"table|chart|code|pre>|kbd|metric|status|filter|sort|timeline|diff|log|trace|invoice|deployment|issue", re.I), "concrete product artifact or workflow signal", "positive"),
    Rule("Accessibility", "Positive", 6, re.compile(r"focus-visible|aria-label|aria-labelledby|aria-describedby|sr-only|role=", re.I), "accessibility implementation signal", "positive"),
    Rule("Motion", "Positive", 5, re.compile(r"prefers-reduced-motion|reducedMotion|useReducedMotion", re.I), "reduced motion support", "positive"),
    Rule("Responsive", "Positive", 5, re.compile(r"aspect-ratio|aspect-\[|minmax\(|container|@container|max-width|min-width", re.I), "responsive stability signal", "positive"),
    Rule("Tokens", "Positive", 5, re.compile(r"--surface|--text|--border|--accent|--focus|tokens|theme\(|var\(--", re.I), "semantic token signal", "positive"),
    Rule("Interaction", "Positive", 5, re.compile(r"loading|empty|error|success|disabled|selected|expanded|collapsed", re.I), "state coverage signal", "positive"),
)

DIMENSIONS = (
    "product_model",
    "first_viewport",
    "information_architecture",
    "visual_hierarchy",
    "typography",
    "tokens",
    "interaction",
    "content_proof",
    "accessibility",
    "responsive",
    "motion",
    "implementation",
    "performance",
    "distinctiveness",
)


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="perfect-design", description="Premium UI design precheck helper.")
    parser.add_argument("target", nargs="?", default=".", help="File, directory, or brief text.")
    parser.add_argument("-c", "--contract", action="store_true", help="Evaluate a design contract or brief.")
    parser.add_argument("--audit", action="store_true", help="Audit UI source files.")
    parser.add_argument("--create", action="store_true", help="Treat target as new UI brief.")
    parser.add_argument("-r", "--redesign", action="store_true", help="Audit for redesign readiness.")
    parser.add_argument("-p", "--polish", action="store_true", help="Audit for polish readiness.")
    parser.add_argument("-j", "--judge", action="store_true", help="Emit judge-style precheck.")
    parser.add_argument("--verify", action="store_true", help="Emit verification precheck.")
    parser.add_argument("-e", "--economy", action="store_true", help="Mark live judges disabled.")
    parser.add_argument("--preset", choices=sorted(PRESETS), default=None, help="Apply a preset.")
    parser.add_argument("--dial", action="append", default=[], metavar="NAME=0..10", help="Override a dial.")
    parser.add_argument("--no-write", action="store_true", help="Accepted for command compatibility; this helper never writes UI files.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    return parser.parse_args(argv)


def resolve_mode(args: argparse.Namespace, target_exists: bool) -> str:
    if args.verify:
        return "verify"
    if args.judge:
        return "judge"
    if args.redesign:
        return "redesign"
    if args.create:
        return "create"
    if args.polish or args.audit:
        return "polish"
    if args.contract:
        return "contract"
    return "polish" if target_exists else "contract"


def resolve_dials(preset: str | None, overrides: Sequence[str]) -> Dict[str, int]:
    dials = dict(DEFAULT_DIALS)
    if preset:
        dials.update(PRESETS[preset])
    for item in overrides:
        if "=" not in item:
            raise ValueError(f"Invalid dial override '{item}'. Expected NAME=0..10.")
        name, raw_value = item.split("=", 1)
        name = name.strip().upper()
        if name not in DIAL_NAMES:
            raise ValueError(f"Unknown dial '{name}'. Valid dials: {', '.join(DIAL_NAMES)}.")
        try:
            value = int(raw_value)
        except ValueError as exc:
            raise ValueError(f"Invalid value for {name}: {raw_value!r}. Expected integer 0..10.") from exc
        if not 0 <= value <= 10:
            raise ValueError(f"Invalid value for {name}: {value}. Expected 0..10.")
        dials[name] = value
    return dials


def iter_scan_files(target: Path) -> Iterable[Path]:
    if target.is_file():
        if target.suffix.lower() in SCAN_SUFFIXES:
            yield target
        return
    for root, dirs, files in os.walk(target):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            path = Path(root) / name
            if path.suffix.lower() in SCAN_SUFFIXES:
                yield path


def scan_text(text: str, file_name: str = "<brief>") -> List[Finding]:
    findings: List[Finding] = []
    lines = text.splitlines() or [text]
    for line_no, line in enumerate(lines, start=1):
        excerpt = line.strip()
        if not excerpt:
            continue
        for rule in (*RISK_RULES, *POSITIVE_RULES):
            if rule.regex.search(excerpt):
                findings.append(
                    Finding(
                        file=file_name,
                        line=line_no,
                        category=rule.category,
                        severity=rule.severity,
                        points=rule.points,
                        reason=rule.reason,
                        excerpt=excerpt[:180],
                        kind=rule.kind,
                    )
                )
    return findings


def scan_file(path: Path, root: Path) -> List[Finding]:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    try:
        display = str(path.relative_to(root))
    except ValueError:
        display = str(path)
    return scan_text(text, display)


def scan_target(target: Path) -> Dict[str, object]:
    root = target if target.is_dir() else target.parent
    files = list(iter_scan_files(target))
    findings: List[Finding] = []
    for path in files:
        findings.extend(scan_file(path, root))
    return summarize_scan(findings, len(files))


def summarize_scan(findings: Sequence[Finding], file_count: int) -> Dict[str, object]:
    risks = [f for f in findings if f.kind == "risk"]
    positives = [f for f in findings if f.kind == "positive"]
    risk_points = min(100, sum(f.points for f in risks))
    positive_points = min(35, sum(f.points for f in positives))
    category_counts: Dict[str, int] = {}
    risk_category_counts: Dict[str, int] = {}
    positive_category_counts: Dict[str, int] = {}
    severity_counts: Dict[str, int] = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Positive": 0}
    for finding in findings:
        category_counts[finding.category] = category_counts.get(finding.category, 0) + 1
        if finding.kind == "risk":
            risk_category_counts[finding.category] = risk_category_counts.get(finding.category, 0) + 1
        else:
            positive_category_counts[finding.category] = positive_category_counts.get(finding.category, 0) + 1
        severity_counts[finding.severity] = severity_counts.get(finding.severity, 0) + 1

    base_score = 72 + positive_points - risk_points
    if file_count == 0:
        base_score -= 12
    premium_score = int(clamp(base_score, 0, 100))
    dimensions = dimension_scores(risk_category_counts, positive_category_counts, severity_counts, premium_score)
    hard_blockers = hard_blockers_for(risk_category_counts, severity_counts, file_count)
    return {
        "files_scanned": file_count,
        "premium_score": premium_score,
        "risk_points": risk_points,
        "positive_points": positive_points,
        "category_counts": category_counts,
        "risk_category_counts": risk_category_counts,
        "positive_category_counts": positive_category_counts,
        "severity_counts": severity_counts,
        "dimensions": dimensions,
        "findings": list(findings),
        "top_findings": top_findings(risks),
        "positive_signals": top_findings(positives, limit=12),
        "hard_blockers": hard_blockers,
    }


def contract_scan(brief: str) -> Dict[str, object]:
    findings = scan_text(brief)
    lowered = brief.lower()
    contract_terms = {
        "user": bool(re.search(r"user|persona|customer|merchant|analyst|developer|operator|designer|buyer", lowered)),
        "job": bool(re.search(r"job|task|workflow|create|review|approve|compare|monitor|ship|buy|filter|debug", lowered)),
        "domain": bool(re.search(r"saas|dashboard|commerce|developer|portfolio|editorial|finance|health|education|logistics|ai", lowered)),
        "proof": bool(re.search(r"data|screenshot|table|chart|metric|code|product|inventory|invoice|issue|deployment|report", lowered)),
        "accessibility": bool(re.search(r"accessib|keyboard|focus|contrast|mobile|responsive|reduced motion", lowered)),
    }
    missing = [name for name, ok in contract_terms.items() if not ok]
    scan = summarize_scan(findings, 0)
    scan["hard_blockers"] = [item for item in scan["hard_blockers"] if item != "no scannable UI files found"]
    penalty = len(missing) * 7
    scan["premium_score"] = int(clamp(scan["premium_score"] - penalty + 10, 0, 100))
    scan["missing_contract_terms"] = missing
    if missing:
        scan["hard_blockers"] = sorted(set([*scan["hard_blockers"], "contract missing: " + ", ".join(missing)]))
    return scan


def dimension_scores(
    risk_category_counts: Dict[str, int],
    positive_category_counts: Dict[str, int],
    severity_counts: Dict[str, int],
    premium_score: int,
) -> Dict[str, int]:
    baseline = int(clamp(round(premium_score / 20), 0, 5))
    scores = {dimension: baseline for dimension in DIMENSIONS}

    def lower(dimension: str, amount: int = 1) -> None:
        scores[dimension] = max(0, scores[dimension] - amount)

    def raise_(dimension: str, amount: int = 1) -> None:
        scores[dimension] = min(5, scores[dimension] + amount)

    if risk_category_counts.get("Product Proof", 0):
        lower("content_proof")
        lower("product_model")
    if risk_category_counts.get("Contract", 0):
        lower("distinctiveness")
        lower("visual_hierarchy")
    if risk_category_counts.get("Accessibility", 0) and severity_counts.get("Critical", 0):
        lower("accessibility", 2)
    if risk_category_counts.get("Responsive", 0):
        lower("responsive")
        lower("performance")
    if risk_category_counts.get("Motion", 0):
        lower("motion")
    if risk_category_counts.get("Tokens", 0):
        lower("tokens")
        lower("implementation")
    if risk_category_counts.get("Implementation", 0):
        lower("implementation")
    if risk_category_counts.get("Layout", 0):
        lower("first_viewport")
        lower("information_architecture")
    if risk_category_counts.get("Copy", 0):
        lower("content_proof")
    if positive_category_counts.get("Product Proof", 0):
        raise_("product_model")
        raise_("content_proof")
    if positive_category_counts.get("Interaction", 0):
        raise_("interaction")
    if positive_category_counts.get("Accessibility", 0):
        raise_("accessibility")
    if positive_category_counts.get("Responsive", 0):
        raise_("responsive")
        raise_("performance")
    if positive_category_counts.get("Tokens", 0):
        raise_("tokens")
        raise_("implementation")
    if positive_category_counts.get("Motion", 0):
        raise_("motion")
    return scores


def top_findings(findings: Sequence[Finding], limit: int = 16) -> List[Dict[str, object]]:
    order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Positive": 4}
    items = sorted(findings, key=lambda f: (order.get(f.severity, 9), f.file, f.line))
    return [
        {
            "file": f.file,
            "line": f.line,
            "severity": f.severity,
            "category": f.category,
            "reason": f.reason,
            "excerpt": f.excerpt,
        }
        for f in items[:limit]
    ]


def hard_blockers_for(category_counts: Dict[str, int], severity_counts: Dict[str, int], file_count: int) -> List[str]:
    blockers: List[str] = []
    if severity_counts.get("Critical", 0):
        blockers.append("critical accessibility or interaction risk")
    if category_counts.get("Product Proof", 0):
        blockers.append("placeholder or unsupported proof")
    if category_counts.get("Responsive", 0):
        blockers.append("responsive stability risk")
    if category_counts.get("Tokens", 0) >= 4:
        blockers.append("token coherence risk")
    if file_count == 0:
        blockers.append("no scannable UI files found")
    return sorted(set(blockers))


def thresholds(dials: Dict[str, int]) -> Dict[str, float]:
    strictness = dials["CRAFT_STRICTNESS"]
    return {
        "minimum_panel_average": round(clamp(7.6 + strictness * 0.16, 8.0, 9.4), 1),
        "minimum_lowest_score": round(clamp(7.2 + strictness * 0.13, 7.5, 9.0), 1),
        "minimum_premium_score": round(clamp(78 + strictness * 1.5, 82, 94), 1),
    }


def judge(scan: Dict[str, object], dials: Dict[str, int], economy: bool) -> Dict[str, object]:
    threshold = thresholds(dials)
    premium_score = float(scan["premium_score"])
    hard_blockers = list(scan["hard_blockers"])
    dimensions = scan["dimensions"]
    assert isinstance(dimensions, dict)

    role_dimensions = {
        "Art Direction Judge": ("visual_hierarchy", "typography", "tokens", "distinctiveness"),
        "Product UX Judge": ("product_model", "first_viewport", "information_architecture", "content_proof"),
        "Interaction Judge": ("interaction", "motion", "responsive"),
        "Design System Judge": ("tokens", "implementation", "performance"),
        "Accessibility and Responsive Judge": ("accessibility", "responsive", "motion"),
        "Content and Proof Judge": ("content_proof", "product_model", "first_viewport"),
    }
    judges = []
    for role, dims in role_dimensions.items():
        dimension_average = sum(float(dimensions[d]) for d in dims) / len(dims)
        score = round(clamp((premium_score / 10.0) * 0.55 + dimension_average * 0.9, 0, 10), 1)
        verdict = "PASS" if score >= threshold["minimum_lowest_score"] and not hard_blockers else "FAIL"
        judges.append({"name": role, "score": score, "verdict": verdict, "blocker": blocker_for(role, scan)})

    average = round(sum(j["score"] for j in judges) / len(judges), 1)
    lowest = min(j["score"] for j in judges)
    passed = (
        premium_score >= threshold["minimum_premium_score"]
        and average >= threshold["minimum_panel_average"]
        and lowest >= threshold["minimum_lowest_score"]
        and not hard_blockers
    )
    if economy:
        gate = "ECONOMY_REVIEW"
    elif passed:
        gate = "PRECHECK_PASS_PANEL_REQUIRED"
    else:
        gate = "FAIL"

    return {
        "gate": gate,
        "panel_average": average,
        "lowest_score": lowest,
        "thresholds": threshold,
        "judges": judges,
        "hard_blockers": hard_blockers,
        "note": "Local deterministic precheck only; non-economy PASS requires live subagent judges." if not economy else "Economy mode: live judges disabled.",
    }


def blocker_for(role: str, scan: Dict[str, object]) -> str:
    category_counts = scan.get("risk_category_counts", scan["category_counts"])
    assert isinstance(category_counts, dict)
    if role == "Art Direction Judge" and (category_counts.get("Aesthetic", 0) or category_counts.get("Contract", 0)):
        return "visual direction is not yet specific enough"
    if role == "Product UX Judge" and (category_counts.get("Layout", 0) or category_counts.get("Product Proof", 0)):
        return "product/job proof is weak or formulaic"
    if role == "Interaction Judge" and category_counts.get("Motion", 0):
        return "motion/state behavior needs purpose and reduced-motion proof"
    if role == "Design System Judge" and category_counts.get("Tokens", 0):
        return "raw values threaten token coherence"
    if role == "Accessibility and Responsive Judge" and (category_counts.get("Accessibility", 0) or category_counts.get("Responsive", 0)):
        return "accessibility or responsive risk detected"
    if role == "Content and Proof Judge" and (category_counts.get("Copy", 0) or category_counts.get("Product Proof", 0)):
        return "copy/proof is not concrete enough"
    if scan["hard_blockers"]:
        return "hard blocker remains"
    return "no deterministic blocker; live judge still required"


def build_result(args: argparse.Namespace) -> Dict[str, object]:
    target = Path(args.target)
    target_exists = target.exists()
    mode = resolve_mode(args, target_exists)
    dials = resolve_dials(args.preset, args.dial)

    if mode == "contract" or (not target_exists and mode in {"create", "polish", "redesign"}):
        scan = contract_scan(args.target)
    elif target_exists:
        scan = scan_target(target)
    else:
        raise FileNotFoundError(f"Target does not exist: {target}")

    no_slop = run_no_slop(target) if target_exists and mode != "contract" else {"status": "not_run", "reason": "brief_or_contract_mode"}
    gate = judge(scan, dials, args.economy)
    return {
        "mode": mode,
        "target": str(target),
        "preset": args.preset or "default",
        "economy": bool(args.economy),
        "no_write": bool(args.no_write),
        "dials": dials,
        "no_slop": no_slop,
        "scan": {
            "files_scanned": scan["files_scanned"],
            "premium_score": scan["premium_score"],
            "risk_points": scan["risk_points"],
            "positive_points": scan["positive_points"],
            "category_counts": scan["category_counts"],
            "risk_category_counts": scan["risk_category_counts"],
            "positive_category_counts": scan["positive_category_counts"],
            "severity_counts": scan["severity_counts"],
            "dimensions": scan["dimensions"],
            "top_findings": scan["top_findings"],
            "positive_signals": scan["positive_signals"],
            "missing_contract_terms": scan.get("missing_contract_terms", []),
            "hard_blockers": scan["hard_blockers"],
        },
        "judge": gate,
        "next_action": next_action(mode, gate),
    }


def run_no_slop(target: Path) -> Dict[str, object]:
    repo_root = Path(__file__).resolve().parents[3]
    script = repo_root / "skills" / "no-slop" / "scripts" / "no_slop_cli.py"
    if not script.exists():
        return {"status": "NO_SLOP_UNAVAILABLE", "reason": str(script)}
    try:
        completed = subprocess.run(
            [sys.executable, str(script), "--scan", str(target.resolve()), "--no-write", "--json"],
            cwd=str(repo_root),
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"status": "error", "reason": str(exc)}
    if completed.returncode != 0:
        return {"status": "error", "returncode": completed.returncode, "stderr": completed.stderr.strip()}
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {"status": "error", "reason": "invalid no-slop JSON", "stdout": completed.stdout[:500]}
    return {
        "status": "ok",
        "score": payload.get("scan", {}).get("score"),
        "gate": payload.get("judge", {}).get("gate"),
        "hard_blockers": payload.get("judge", {}).get("hard_blockers", []),
        "signatures": payload.get("scan", {}).get("signatures", []),
        "files_scanned": payload.get("scan", {}).get("files_scanned"),
    }


def next_action(mode: str, gate: Dict[str, object]) -> str:
    if gate["gate"] == "PRECHECK_PASS_PANEL_REQUIRED":
        return "Run no-slop, live judge panel, and browser verification before claiming a full pass."
    if mode == "contract":
        return "Complete or revise the Design Contract before code."
    if gate["gate"] == "FAIL":
        return "Fix hard blockers, re-run no-slop, then rejudge."
    return "Proceed to verification."


def print_markdown(result: Dict[str, object]) -> None:
    scan = result["scan"]
    gate = result["judge"]
    print("# Perfect-Design Precheck")
    print()
    print(f"Mode: {result['mode']}")
    print(f"Target: {result['target']}")
    print(f"Preset: {result['preset']}")
    print(f"Premium score: {scan['premium_score']}/100")
    no_slop = result.get("no_slop", {})
    if no_slop:
        print(f"No-slop: {no_slop.get('status')} score={no_slop.get('score')} gate={no_slop.get('gate')}")
    print(f"Judge gate: {gate['gate']}")
    print(f"Panel average: {gate['panel_average']}/10")
    print(f"Lowest score: {gate['lowest_score']}/10")
    print(f"Next action: {result['next_action']}")
    print()
    if scan.get("missing_contract_terms"):
        print("## Missing Contract Terms")
        for item in scan["missing_contract_terms"]:
            print(f"- {item}")
        print()
    print("## Dials")
    for name, value in result["dials"].items():
        print(f"- {name}: {value}")
    print()
    print("## Top Findings")
    if scan["top_findings"]:
        for item in scan["top_findings"]:
            print(f"- {item['severity']} / {item['category']}: `{item['file']}:{item['line']}` - {item['reason']} - {item['excerpt']}")
    else:
        print("- No deterministic risk findings.")
    print()
    print("## Positive Signals")
    if scan["positive_signals"]:
        for item in scan["positive_signals"]:
            print(f"- {item['category']}: `{item['file']}:{item['line']}` - {item['reason']}")
    else:
        print("- No positive implementation signals detected.")
    print()
    print("## Hard Blockers")
    if scan["hard_blockers"]:
        for blocker in scan["hard_blockers"]:
            print(f"- {blocker}")
    else:
        print("- None detected by deterministic precheck.")
    print()
    print("## Judges")
    for item in gate["judges"]:
        print(f"- {item['name']}: {item['score']}/10 {item['verdict']} - {item['blocker']}")


def main(argv: Sequence[str]) -> int:
    try:
        args = parse_args(argv)
        result = build_result(args)
    except (ValueError, FileNotFoundError) as exc:
        print(f"perfect-design: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_markdown(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
