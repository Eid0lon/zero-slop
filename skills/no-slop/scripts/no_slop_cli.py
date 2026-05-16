#!/usr/bin/env python3
"""Deterministic helper CLI for the no-slop skill.

The skill workflow remains the authority for edits and live subagent judging.
This script gives a local scan, slop signatures, dials, presets, a strict
judge-gate approximation, and an autopsy report that can run from a shell.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


DIAL_NAMES = (
    "SLOP_TOLERANCE",
    "STRICTNESS",
    "VISUAL_DENSITY",
    "MOTION_INTENSITY",
    "BRAND_STRENGTH",
    "HIERARCHY_SHARPNESS",
    "COPY_PRECISION",
    "VARIANCE",
)

DEFAULT_DIALS: Dict[str, int] = {
    "SLOP_TOLERANCE": 1,
    "STRICTNESS": 9,
    "VISUAL_DENSITY": 5,
    "MOTION_INTENSITY": 2,
    "BRAND_STRENGTH": 7,
    "HIERARCHY_SHARPNESS": 8,
    "COPY_PRECISION": 8,
    "VARIANCE": 6,
}

PRESETS: Dict[str, Dict[str, int]] = {
    "saas": {
        "SLOP_TOLERANCE": 1,
        "STRICTNESS": 9,
        "VISUAL_DENSITY": 5,
        "MOTION_INTENSITY": 2,
        "BRAND_STRENGTH": 7,
        "HIERARCHY_SHARPNESS": 8,
        "COPY_PRECISION": 9,
        "VARIANCE": 6,
    },
    "dashboard": {
        "SLOP_TOLERANCE": 0,
        "STRICTNESS": 10,
        "VISUAL_DENSITY": 8,
        "MOTION_INTENSITY": 1,
        "BRAND_STRENGTH": 5,
        "HIERARCHY_SHARPNESS": 9,
        "COPY_PRECISION": 8,
        "VARIANCE": 4,
    },
    "portfolio": {
        "SLOP_TOLERANCE": 1,
        "STRICTNESS": 8,
        "VISUAL_DENSITY": 4,
        "MOTION_INTENSITY": 4,
        "BRAND_STRENGTH": 9,
        "HIERARCHY_SHARPNESS": 8,
        "COPY_PRECISION": 8,
        "VARIANCE": 8,
    },
    "ecommerce": {
        "SLOP_TOLERANCE": 0,
        "STRICTNESS": 10,
        "VISUAL_DENSITY": 7,
        "MOTION_INTENSITY": 2,
        "BRAND_STRENGTH": 7,
        "HIERARCHY_SHARPNESS": 9,
        "COPY_PRECISION": 10,
        "VARIANCE": 5,
    },
    "brutalist": {
        "SLOP_TOLERANCE": 1,
        "STRICTNESS": 8,
        "VISUAL_DENSITY": 7,
        "MOTION_INTENSITY": 1,
        "BRAND_STRENGTH": 10,
        "HIERARCHY_SHARPNESS": 9,
        "COPY_PRECISION": 8,
        "VARIANCE": 8,
    },
    "minimal": {
        "SLOP_TOLERANCE": 0,
        "STRICTNESS": 10,
        "VISUAL_DENSITY": 4,
        "MOTION_INTENSITY": 1,
        "BRAND_STRENGTH": 6,
        "HIERARCHY_SHARPNESS": 10,
        "COPY_PRECISION": 10,
        "VARIANCE": 3,
    },
    "editorial": {
        "SLOP_TOLERANCE": 1,
        "STRICTNESS": 8,
        "VISUAL_DENSITY": 5,
        "MOTION_INTENSITY": 3,
        "BRAND_STRENGTH": 9,
        "HIERARCHY_SHARPNESS": 9,
        "COPY_PRECISION": 9,
        "VARIANCE": 8,
    },
    "ai-tool": {
        "SLOP_TOLERANCE": 0,
        "STRICTNESS": 10,
        "VISUAL_DENSITY": 7,
        "MOTION_INTENSITY": 2,
        "BRAND_STRENGTH": 7,
        "HIERARCHY_SHARPNESS": 9,
        "COPY_PRECISION": 10,
        "VARIANCE": 5,
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
    ".md",
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
    "templates",
}


@dataclass(frozen=True)
class Pattern:
    category: str
    severity: str
    points: int
    regex: re.Pattern[str]
    reason: str


@dataclass
class Finding:
    file: str
    line: int
    category: str
    severity: str
    points: int
    reason: str
    excerpt: str


PATTERNS: Sequence[Pattern] = (
    Pattern("Aesthetic Defaults", "High", 8, re.compile(r"from-blue|to-purple|from-indigo|to-pink|from-cyan|to-blue|bg-clip-text|text-transparent", re.I), "template gradient or gradient text"),
    Pattern("Aesthetic Defaults", "Medium", 4, re.compile(r"backdrop-blur|bg-white/10|border-white/20|shadow-2xl|shadow-xl|blur-3xl", re.I), "decorative glass/glow styling"),
    Pattern("Aesthetic Defaults", "Medium", 4, re.compile(r"#6366f1|#8b5cf6|indigo-500|violet-500|purple-600", re.I), "startup purple token"),
    Pattern("Layout Formulae", "High", 8, re.compile(r"Features|Testimonials|Pricing|Get Started|Start Free|Book a demo", re.I), "generic landing-page section or CTA"),
    Pattern("Layout Formulae", "Medium", 4, re.compile(r"grid-cols-3|grid-cols-4|md:grid-cols-3|lg:grid-cols-3|py-24|py-32|text-center", re.I), "formulaic grid/spacing/alignment"),
    Pattern("Component Soup", "Medium", 4, re.compile(r"rounded-2xl|rounded-3xl|hover:scale|hover:-translate-y|hover:shadow", re.I), "over-rounded or hover-lift component cliche"),
    Pattern("Component Soup", "Low", 2, re.compile(r"Sparkles|Zap|Shield|Rocket|Star|Award|CheckCircle|TrendingUp"), "generic decorative icon choice"),
    Pattern("Typography Sameness", "Medium", 4, re.compile(r"Inter|Geist|Roboto|Plus Jakarta|Space Grotesk|tracking-tight|tracking-\[-", re.I), "default generated typography signal"),
    Pattern("Typography Sameness", "Low", 2, re.compile(r"uppercase.*tracking-wider|text-xs.*uppercase|text-gray-400|text-slate-400", re.I), "weak label/body hierarchy"),
    Pattern("Motion Spam", "Medium", 4, re.compile(r"fadeIn|fade-in|opacity-0|whileInView|animate-.*fade|animate-.*bounce|animate-.*pulse|transition-all", re.I), "decorative or global motion"),
    Pattern("Copy Void", "Medium", 4, re.compile(r"unlock|empower|streamline|revolutionize|seamless|powerful|innovative|next-generation|all-in-one|supercharge", re.I), "generic marketing copy"),
    Pattern("Copy Void", "High", 8, re.compile(r"lorem|ipsum|placeholder|dummy|trusted by|10k\+|99\.9%", re.I), "placeholder or fake proof risk"),
    Pattern("Accessibility Slop", "Critical", 15, re.compile(r"outline-none|focus:outline-none|focus:ring-0", re.I), "focus visibility risk"),
    Pattern("Responsive and Performance Slop", "Medium", 4, re.compile(r"min-h-screen|h-screen|w-screen|overflow-hidden|blur-|backdrop-blur|filter|drop-shadow", re.I), "viewport trap or heavy visual effect risk"),
    Pattern("Code and Design-System Smells", "Medium", 4, re.compile(r"className=\"[^\"]*(\s+[^\s\"]+){15,}"), "long utility-class soup"),
    Pattern("Design Token Violation", "High", 8, re.compile(r"bg-\[#|text-\[#|border-\[#|shadow-\[|rounded-\[|#[0-9a-fA-F]{3,8}"), "raw visual values bypass tokens"),
    Pattern("Hierarchy Collapse", "High", 8, re.compile(r"text-lg font-semibold|font-semibold text-lg|grid-cols-3.*gap|grid.*gap-8", re.I), "repeated equal-weight hierarchy"),
    Pattern("Brand Incoherence", "Medium", 4, re.compile(r"modern|sleek|premium|beautiful|make it pop", re.I), "brand direction replaced by vague style words"),
)

JUDGE_ROLES = (
    "Visual Forensics Judge",
    "Product UX Judge",
    "Design-System Judge",
    "Accessibility and Responsive Judge",
    "Copy and Brand Judge",
    "Motion and Interaction Judge",
)


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="no-slop", description="Strict anti-slop UI scanner and judge helper.")
    parser.add_argument("target", nargs="?", default=".", help="File, directory, or prevention brief.")
    parser.add_argument("-s", "--scan", action="store_true", help="Scan and score.")
    parser.add_argument("-f", "--fix", action="store_true", help="Plan surgical remediation.")
    parser.add_argument("-r", "--redesign", action="store_true", help="Plan full redesign.")
    parser.add_argument("-j", "--judge", action="store_true", help="Run strict judge gate.")
    parser.add_argument("--prevent", action="store_true", help="Run prevention contract mode.")
    parser.add_argument("--autopsy", action="store_true", help="Emit a forensic AI-slop autopsy report.")
    parser.add_argument("-e", "--economy", action="store_true", help="Disable subagent judge expectation.")
    parser.add_argument("--preset", choices=sorted(PRESETS), default=None, help="Apply a dial preset.")
    parser.add_argument("--dial", action="append", default=[], metavar="NAME=0..10", help="Override a control dial.")
    parser.add_argument("--no-write", action="store_true", help="Accepted for command compatibility; this helper never writes UI files.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    return parser.parse_args(argv)


def resolve_mode(args: argparse.Namespace) -> str:
    if args.prevent:
        return "prevent"
    if args.redesign:
        return "redesign"
    if args.fix:
        return "fix"
    if args.judge:
        return "judge"
    return "scan"


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
            if name == "SKILL.md":
                continue
            path = Path(root) / name
            if path.suffix.lower() in SCAN_SUFFIXES:
                yield path


def scan_file(path: Path, root: Path) -> List[Finding]:
    findings: List[Finding] = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return findings

    try:
        display = str(path.relative_to(root))
    except ValueError:
        display = str(path)

    seen_in_file = set()
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        for pattern in PATTERNS:
            if pattern.regex.search(stripped):
                key = (pattern.category, pattern.reason, line_no)
                if key in seen_in_file:
                    continue
                seen_in_file.add(key)
                findings.append(
                    Finding(
                        file=display,
                        line=line_no,
                        category=pattern.category,
                        severity=pattern.severity,
                        points=pattern.points,
                        reason=pattern.reason,
                        excerpt=stripped[:180],
                    )
                )
    return findings


def scan_target(target: Path) -> Dict[str, object]:
    root = target if target.is_dir() else target.parent
    files = list(iter_scan_files(target))
    findings: List[Finding] = []
    for path in files:
        findings.extend(scan_file(path, root))

    category_scores: Dict[str, int] = {}
    category_counts: Dict[str, int] = {}
    severity_counts: Dict[str, int] = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}

    for finding in findings:
        category_scores[finding.category] = category_scores.get(finding.category, 0) + finding.points
        category_counts[finding.category] = category_counts.get(finding.category, 0) + 1
        severity_counts[finding.severity] = severity_counts.get(finding.severity, 0) + 1

    signatures = detect_signatures(category_counts, findings)
    signature_score = sum(sig["points"] for sig in signatures)
    score = min(100, sum(f.points for f in findings) + signature_score)

    return {
        "files_scanned": len(files),
        "findings": findings,
        "score": score,
        "category_scores": category_scores,
        "category_counts": category_counts,
        "severity_counts": severity_counts,
        "signatures": signatures,
    }


def scan_prompt(text: str) -> Dict[str, object]:
    findings: List[Finding] = []
    for pattern in PATTERNS:
        if pattern.regex.search(text):
            findings.append(
                Finding(
                    file="<brief>",
                    line=1,
                    category=pattern.category,
                    severity=pattern.severity,
                    points=pattern.points,
                    reason=pattern.reason,
                    excerpt=text[:180],
                )
            )

    category_scores: Dict[str, int] = {}
    category_counts: Dict[str, int] = {}
    severity_counts: Dict[str, int] = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for finding in findings:
        category_scores[finding.category] = category_scores.get(finding.category, 0) + finding.points
        category_counts[finding.category] = category_counts.get(finding.category, 0) + 1
        severity_counts[finding.severity] = severity_counts.get(finding.severity, 0) + 1

    signatures = detect_signatures(category_counts, findings)
    score = min(100, sum(f.points for f in findings) + prompt_risk_score(text) + sum(sig["points"] for sig in signatures))
    return {
        "files_scanned": 0,
        "findings": findings,
        "score": score,
        "category_scores": category_scores,
        "category_counts": category_counts,
        "severity_counts": severity_counts,
        "signatures": signatures,
    }


def has_category(counts: Dict[str, int], name: str, minimum: int = 1) -> bool:
    return counts.get(name, 0) >= minimum


def detect_signatures(category_counts: Dict[str, int], findings: Sequence[Finding]) -> List[Dict[str, object]]:
    text = "\n".join(f.excerpt.lower() for f in findings[:300])
    signatures: List[Dict[str, object]] = []

    def add(name: str, severity: str, points: int, reason: str) -> None:
        signatures.append({"name": name, "severity": severity, "points": points, "reason": reason})

    if has_category(category_counts, "Aesthetic Defaults", 2) and has_category(category_counts, "Copy Void") and has_category(category_counts, "Layout Formulae"):
        add("Startup Gradient Stack", "High", 8, "gradient/default aesthetic combines with generic landing structure and copy")
    if has_category(category_counts, "Aesthetic Defaults", 2) and has_category(category_counts, "Component Soup", 2):
        add("Glass Feature Soup", "High", 8, "decorative surfaces and repeated component cliches cluster together")
    if "99.9" in text and (has_category(category_counts, "Layout Formulae") or has_category(category_counts, "Copy Void")):
        add("Dashboard Theater", "High", 8, "fake metric signal appears without evidence")
    if has_category(category_counts, "Copy Void", 2) and has_category(category_counts, "Layout Formulae"):
        add("Copy Fog Landing", "High", 8, "vague claims combine with formulaic sections")
    if has_category(category_counts, "Motion Spam", 2):
        add("Motion Confetti", "Medium", 4, "multiple motion signals without detected purpose")
    if has_category(category_counts, "Design Token Violation", 2):
        add("Token Collapse", "High", 8, "raw visual values repeatedly bypass token system")
    if has_category(category_counts, "Brand Incoherence") and has_category(category_counts, "Aesthetic Defaults"):
        add("Brand Costume", "High", 8, "vague style words combine with template aesthetics")

    return signatures


def gate_thresholds(dials: Dict[str, int]) -> Dict[str, float]:
    strictness = dials["STRICTNESS"]
    tolerance = dials["SLOP_TOLERANCE"]
    return {
        "allowed_slop_score": clamp(12 + (tolerance * 3) - (strictness * 2), 8, 35),
        "minimum_panel_average": clamp(7.0 + (strictness * 0.2) - (tolerance * 0.1), 7.0, 9.2),
        "minimum_lowest_judge": clamp(6.5 + (strictness * 0.15) - (tolerance * 0.1), 6.5, 8.6),
    }


def judge(scan: Dict[str, object], dials: Dict[str, int], economy: bool) -> Dict[str, object]:
    score = float(scan["score"])
    counts = scan["category_counts"]
    assert isinstance(counts, dict)
    thresholds = gate_thresholds(dials)
    strict_penalty = (dials["STRICTNESS"] - 5) * 0.15
    tolerance_credit = dials["SLOP_TOLERANCE"] * 0.08

    role_penalties = {
        "Visual Forensics Judge": ("Aesthetic Defaults", "Typography Sameness", "Hierarchy Collapse", "Brand Incoherence"),
        "Product UX Judge": ("Layout Formulae", "Hierarchy Collapse", "Copy Void"),
        "Design-System Judge": ("Design Token Violation", "Code and Design-System Smells", "Component Soup"),
        "Accessibility and Responsive Judge": ("Accessibility Slop", "Responsive and Performance Slop", "Motion Spam"),
        "Copy and Brand Judge": ("Copy Void", "Brand Incoherence", "Asset Fakery"),
        "Motion and Interaction Judge": ("Motion Spam", "Component Soup", "Responsive and Performance Slop"),
    }

    judges = []
    for role in JUDGE_ROLES:
        category_hit_count = sum(int(counts.get(category, 0)) for category in role_penalties[role])
        raw = 10.0 - (score / 18.0) - strict_penalty - (category_hit_count * 0.18) + tolerance_credit
        role_score = round(clamp(raw, 0.0, 10.0), 1)
        verdict = "PASS" if role_score >= thresholds["minimum_lowest_judge"] else "FAIL"
        judges.append(
            {
                "name": role,
                "score": role_score,
                "verdict": verdict,
                "blocker": blocker_for_role(role, counts),
            }
        )

    average = round(sum(j["score"] for j in judges) / len(judges), 1)
    lowest = min(j["score"] for j in judges)
    hard_blockers = hard_blockers_for(scan)
    passed = (
        score <= thresholds["allowed_slop_score"]
        and average >= thresholds["minimum_panel_average"]
        and lowest >= thresholds["minimum_lowest_judge"]
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
        "lowest_judge": lowest,
        "thresholds": thresholds,
        "hard_blockers": hard_blockers,
        "judges": judges,
        "subagent_panel_required": not economy,
        "note": "Local deterministic precheck only; non-economy PASS requires live subagent judges." if not economy else "Economy mode: subagent judges disabled by request.",
    }


def blocker_for_role(role: str, counts: Dict[str, int]) -> str:
    if role == "Visual Forensics Judge" and counts.get("Aesthetic Defaults", 0):
        return "template aesthetic signals remain"
    if role == "Product UX Judge" and counts.get("Layout Formulae", 0):
        return "formulaic layout obscures product-specific job"
    if role == "Design-System Judge" and counts.get("Design Token Violation", 0):
        return "raw styling bypasses semantic tokens"
    if role == "Accessibility and Responsive Judge" and counts.get("Accessibility Slop", 0):
        return "focus/accessibility risk detected"
    if role == "Copy and Brand Judge" and counts.get("Copy Void", 0):
        return "copy is vague or unsupported"
    if role == "Motion and Interaction Judge" and counts.get("Motion Spam", 0):
        return "motion signals lack purpose or reduced-motion proof"
    return "no primary blocker from deterministic scan"


def hard_blockers_for(scan: Dict[str, object]) -> List[str]:
    counts = scan["category_counts"]
    severities = scan["severity_counts"]
    signatures = scan["signatures"]
    assert isinstance(counts, dict)
    assert isinstance(severities, dict)
    blockers = []
    if severities.get("Critical", 0):
        blockers.append("critical issue detected")
    if counts.get("Accessibility Slop", 0):
        blockers.append("accessibility risk detected")
    if counts.get("Design Token Violation", 0) >= 3:
        blockers.append("severe design token violation")
    if counts.get("Hierarchy Collapse", 0) >= 2:
        blockers.append("hierarchy collapse risk")
    for signature in signatures:
        if signature["name"] in {"Ecommerce Urgency Fog", "Token Collapse", "Startup Gradient Stack"}:
            blockers.append(f"slop signature: {signature['name']}")
    return sorted(set(blockers))


def summarize_findings(findings: Sequence[Finding], limit: int = 18) -> List[Dict[str, object]]:
    severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    ordered = sorted(findings, key=lambda f: (severity_order.get(f.severity, 9), f.file, f.line))
    return [
        {
            "file": f.file,
            "line": f.line,
            "severity": f.severity,
            "category": f.category,
            "reason": f.reason,
            "excerpt": f.excerpt,
        }
        for f in ordered[:limit]
    ]


def build_result(args: argparse.Namespace) -> Dict[str, object]:
    mode = resolve_mode(args)
    dials = resolve_dials(args.preset, args.dial)
    target = Path(args.target)

    if mode != "prevent" and not target.exists():
        raise FileNotFoundError(f"Target does not exist: {target}")

    if mode == "prevent" and not target.exists():
        scan = scan_prompt(args.target)
    else:
        scan = scan_target(target)

    gate = judge(scan, dials, args.economy)
    if mode != "prevent" and scan["files_scanned"] == 0:
        gate["gate"] = "NO_SURFACE"
        gate["hard_blockers"] = sorted(set([*gate["hard_blockers"], "no scannable UI files found"]))
        for item in gate["judges"]:
            item["verdict"] = "FAIL"
            item["blocker"] = "no scannable UI surface was found"
    findings = scan["findings"]
    assert isinstance(findings, list)

    result = {
        "mode": mode,
        "target": str(target),
        "preset": args.preset or "default",
        "economy": bool(args.economy),
        "no_write": bool(args.no_write),
        "autopsy": bool(args.autopsy),
        "dials": dials,
        "scan": {
            "files_scanned": scan["files_scanned"],
            "score": scan["score"],
            "category_counts": scan["category_counts"],
            "category_scores": scan["category_scores"],
            "severity_counts": scan["severity_counts"],
            "signatures": scan["signatures"],
            "top_findings": summarize_findings(findings),
        },
        "judge": gate,
        "next_action": next_action(mode, gate),
    }
    if args.autopsy:
        result["autopsy_report"] = build_autopsy(result)
    return result


def prompt_risk_score(text: str) -> int:
    risky = re.findall(r"modern|sleek|premium|beautiful|clean|make it pop|hero|features|testimonials|pricing", text, flags=re.I)
    return min(100, len(risky) * 8)


def next_action(mode: str, gate: Dict[str, object]) -> str:
    if gate["gate"] == "PRECHECK_PASS_PANEL_REQUIRED":
        return "Run live subagent judge panel before claiming a full pass."
    if gate["gate"] == "NO_SURFACE":
        return "Point no-slop at a UI file or frontend source directory."
    if mode == "scan":
        return "Report findings. Do not edit."
    if mode == "judge":
        return "Block output until judge gate passes." if gate["gate"] == "FAIL" else "Gate passed."
    if mode == "prevent":
        return "Draft prevention contract before generating UI code."
    if gate["gate"] == "FAIL":
        return "Run remediation pass, re-scan, and re-judge."
    return "Proceed to verification."


AUTOPSY_SYSTEMS = (
    {
        "name": "Visual Identity",
        "categories": ("Aesthetic Defaults", "Typography Sameness", "Brand Incoherence"),
        "fail_at": 5,
        "warn_at": 1,
        "pass_note": "No deterministic template-aesthetic signal.",
        "fail_note": "Visual personality is carried by familiar generated defaults.",
    },
    {
        "name": "Product Proof",
        "categories": ("Copy Void",),
        "signatures": ("Dashboard Theater", "Copy Fog Landing"),
        "fail_at": 4,
        "warn_at": 1,
        "pass_note": "No vague proof or fake-proof signal detected.",
        "fail_note": "Claims are stronger than the evidence visible in the interface.",
    },
    {
        "name": "Information Architecture",
        "categories": ("Layout Formulae", "Hierarchy Collapse"),
        "fail_at": 5,
        "warn_at": 1,
        "pass_note": "No formulaic page skeleton detected.",
        "fail_note": "The structure reads like a reusable landing-page template.",
    },
    {
        "name": "Component Discipline",
        "categories": ("Component Soup", "Code and Design-System Smells", "Design Token Violation"),
        "fail_at": 5,
        "warn_at": 1,
        "pass_note": "No component-soup or token-collapse signal detected.",
        "fail_note": "Components look assembled from trend defaults rather than a system.",
    },
    {
        "name": "Interaction and Motion",
        "categories": ("Motion Spam", "Responsive and Performance Slop"),
        "fail_at": 4,
        "warn_at": 1,
        "pass_note": "No motion or viewport trap signal detected.",
        "fail_note": "Motion/performance choices may be decorative or fragile.",
    },
    {
        "name": "Accessibility",
        "categories": ("Accessibility Slop",),
        "fail_at": 1,
        "warn_at": 1,
        "pass_note": "No deterministic focus/accessibility blocker detected.",
        "fail_note": "Accessibility risk blocks a credible ship decision.",
    },
)

FIX_PLAYBOOK = {
    "Aesthetic Defaults": "Replace template gradients/glass with a product-specific palette, material model, and image or data proof.",
    "Layout Formulae": "Rebuild the first viewport around the user's job, not hero/features/pricing muscle memory.",
    "Component Soup": "Remove decorative card/icon repetition; use components only where they clarify hierarchy or action.",
    "Typography Sameness": "Create a deliberate type scale and reading rhythm instead of default generated font signals.",
    "Motion Spam": "Keep motion only for state, feedback, or spatial continuity; add reduced-motion proof when motion remains.",
    "Copy Void": "Replace broad promises with concrete product nouns, user jobs, constraints, and evidence.",
    "Accessibility Slop": "Restore visible focus, labels, keyboard paths, and non-hover access before visual polish.",
    "Responsive and Performance Slop": "Remove viewport traps and heavy effects that threaten mobile framing or performance.",
    "Code and Design-System Smells": "Extract repeated utility soup into coherent variants or semantic component styles.",
    "Design Token Violation": "Route raw colors, shadows, radii, and spacing through semantic tokens.",
    "Hierarchy Collapse": "Make the primary action, proof, metadata, and secondary content visibly different in weight.",
    "Brand Incoherence": "Translate vague style words into concrete product-specific palette, type, shape, voice, and proof.",
}

AUTOPSY_SIGNATURE_CAUSES = {
    "Startup Gradient Stack": "Generic AI SaaS composition: trend gradients, vague copy, and formulaic landing structure collapsed into one surface.",
    "Glass Feature Soup": "Decorative glass/card styling is doing the job that product evidence should do.",
    "Dashboard Theater": "Unsupported metrics or dashboard theater are being used as trust signals.",
    "Copy Fog Landing": "The page relies on abstract claims where concrete product proof should be.",
    "Motion Confetti": "Motion appears as decoration rather than state, continuity, or feedback.",
    "Token Collapse": "Raw visual values are bypassing the system often enough to erode design coherence.",
    "Brand Costume": "The interface is wearing a fashionable aesthetic without proving why it belongs to this product.",
}


def signature_names(scan: Dict[str, object]) -> List[str]:
    signatures = scan["signatures"]
    assert isinstance(signatures, list)
    return [str(sig["name"]) for sig in signatures]


def category_count(scan: Dict[str, object], category: str) -> int:
    counts = scan["category_counts"]
    assert isinstance(counts, dict)
    return int(counts.get(category, 0))


def top_categories(scan: Dict[str, object], limit: int = 6) -> List[Dict[str, object]]:
    counts = scan["category_counts"]
    scores = scan["category_scores"]
    assert isinstance(counts, dict)
    assert isinstance(scores, dict)
    rows = [
        {"category": category, "count": int(count), "score": int(scores.get(category, 0))}
        for category, count in counts.items()
    ]
    return sorted(rows, key=lambda row: (-row["score"], -row["count"], row["category"]))[:limit]


def autopsy_severity(score: int, gate: str) -> str:
    if gate == "NO_SURFACE":
        return "NO_SURFACE"
    if score <= 15:
        return "CLEAN"
    if score <= 30:
        return "RESIDUE"
    if score <= 55:
        return "CONTAMINATED"
    if score <= 75:
        return "SYSTEMIC"
    return "CRITICAL"


def autopsy_cause(scan: Dict[str, object], gate: Dict[str, object]) -> str:
    if gate["gate"] == "NO_SURFACE":
        return "No scannable UI surface was found, so there is nothing credible to judge."
    score = int(scan["score"])
    if score <= 15:
        return "No autopsy-level cause detected. Any remaining signals are minor deterministic hints, not a structural AI-slop failure."

    names = signature_names(scan)
    for name in (
        "Startup Gradient Stack",
        "Glass Feature Soup",
        "Dashboard Theater",
        "Copy Fog Landing",
        "Token Collapse",
        "Brand Costume",
        "Motion Confetti",
    ):
        if name in names:
            return AUTOPSY_SIGNATURE_CAUSES[name]

    categories = top_categories(scan, limit=1)
    if categories:
        category = str(categories[0]["category"])
        return f"Dominant failure mode: {category}. {FIX_PLAYBOOK.get(category, 'The interface carries repeated generic signals.')}"
    return "The surface has weak genericity signals, but no dominant deterministic cause."


def autopsy_verdict(scan: Dict[str, object], gate: Dict[str, object]) -> str:
    score = int(scan["score"])
    if gate["gate"] == "NO_SURFACE":
        return "No surface. No ship decision."
    if score <= 15 and not gate["hard_blockers"]:
        return "No obvious generated residue. Still verify in browser and with human context."
    if score <= 30:
        return "Usable shape, visible residue. Clean before a serious launch."
    if score <= 55:
        return "Looks designed at a glance, but the fingerprints are too loud."
    if score <= 75:
        return "The generic system is structural. Redesign is probably faster than patching."
    return "Looks shippable. Is not shippable."


def any_product_test(scan: Dict[str, object]) -> Dict[str, str]:
    names = set(signature_names(scan))
    has_generic_stack = bool(
        names.intersection({"Startup Gradient Stack", "Copy Fog Landing", "Glass Feature Soup", "Brand Costume"})
    )
    layout = category_count(scan, "Layout Formulae")
    copy = category_count(scan, "Copy Void")
    aesthetic = category_count(scan, "Aesthetic Defaults")

    if has_generic_stack or (layout and copy and aesthetic):
        return {
            "risk": "HIGH",
            "finding": "This UI could become a CRM, AI SaaS, analytics tool, or productivity app by changing mostly the logo and nouns.",
        }
    if layout or copy:
        return {
            "risk": "MEDIUM",
            "finding": "Some structure or language is reusable across too many products; product-specific proof should be strengthened.",
        }
    return {
        "risk": "LOW",
        "finding": "The deterministic scan did not find a strong could-be-any-product pattern.",
    }


def autopsy_systems(scan: Dict[str, object]) -> List[Dict[str, str]]:
    names = set(signature_names(scan))
    rows: List[Dict[str, str]] = []
    for system in AUTOPSY_SYSTEMS:
        count = sum(category_count(scan, category) for category in system["categories"])
        for signature in system.get("signatures", ()):
            if signature in names:
                count += 2
        if count >= int(system["fail_at"]):
            status = "FAIL"
            note = str(system["fail_note"])
        elif count >= int(system["warn_at"]):
            status = "WARN"
            note = f"{count} deterministic signal(s) detected."
        else:
            status = "PASS"
            note = str(system["pass_note"])
        rows.append({"system": str(system["name"]), "status": status, "evidence": note})
    return rows


def autopsy_pretends_and_proves(scan: Dict[str, object]) -> Dict[str, str]:
    names = set(signature_names(scan))
    counts = scan["category_counts"]
    assert isinstance(counts, dict)

    if "Dashboard Theater" in names:
        return {
            "pretends": "A data-backed product with operational credibility.",
            "proves": "The metrics and charts need sources, labels, or a decision path before they can carry trust.",
        }
    if counts.get("Copy Void", 0) and counts.get("Layout Formulae", 0):
        return {
            "pretends": "A polished product story with momentum and conversion intent.",
            "proves": "The story is still mostly abstract claims and familiar section choreography.",
        }
    if counts.get("Aesthetic Defaults", 0) and counts.get("Component Soup", 0):
        return {
            "pretends": "Premium visual craft.",
            "proves": "The craft is coming from trend styling rather than product-specific decisions.",
        }
    if counts.get("Accessibility Slop", 0):
        return {
            "pretends": "A ready-to-ship interface.",
            "proves": "Keyboard or focus risk still blocks a real release.",
        }
    if int(scan["score"]) <= 15:
        return {
            "pretends": "Nothing suspicious from deterministic patterns alone.",
            "proves": "A deeper review should focus on product truth, browser behavior, and real user workflows.",
        }
    return {
        "pretends": "A complete interface.",
        "proves": "The deterministic scan found repeated residue that still needs product-specific justification.",
    }


def autopsy_reality_handoff(scan: Dict[str, object]) -> Dict[str, object]:
    names = set(signature_names(scan))
    reasons: List[str] = []
    if "Dashboard Theater" in names:
        reasons.append("fake or unsupported metrics may be presented as product proof")
    if category_count(scan, "Copy Void"):
        reasons.append("copy/proof may overclaim what the UI actually demonstrates")
    if category_count(scan, "Layout Formulae"):
        reasons.append("primary CTAs and page sections may still be static demo choreography")
    if category_count(scan, "Accessibility Slop"):
        reasons.append("focus/accessibility risk affects real workflow completion")

    if reasons:
        return {
            "recommendation": "LOAD_REALITY_SKILL",
            "skill": "skills/reality-skill/SKILL.md",
            "reasons": reasons,
        }
    return {
        "recommendation": "OPTIONAL",
        "skill": "skills/reality-skill/SKILL.md",
        "reasons": ["no fake-proof/action signal detected by deterministic scan"],
    }


def autopsy_fix_order(scan: Dict[str, object], limit: int = 6) -> List[Dict[str, str]]:
    order = []
    for item in top_categories(scan, limit=limit):
        category = str(item["category"])
        order.append(
            {
                "category": category,
                "why": f"{item['count']} hit(s), {item['score']} point(s)",
                "move": FIX_PLAYBOOK.get(category, "Review this category and replace generic residue with product-specific decisions."),
            }
        )
    if not order:
        order.append(
            {
                "category": "Manual product review",
                "why": "No deterministic category hits.",
                "move": "Verify browser behavior, real content, mobile layout, and user workflow completion.",
            }
        )
    return order


def build_autopsy(result: Dict[str, object]) -> Dict[str, object]:
    scan = result["scan"]
    gate = result["judge"]
    assert isinstance(scan, dict)
    assert isinstance(gate, dict)
    score = int(scan["score"])
    severity = autopsy_severity(score, str(gate["gate"]))
    pretends = autopsy_pretends_and_proves(scan)
    any_product = any_product_test(scan)
    top_findings = scan["top_findings"]
    assert isinstance(top_findings, list)
    signatures = scan["signatures"]
    assert isinstance(signatures, list)

    share_line = autopsy_verdict(scan, gate)
    if score > 15:
        share_line = f"{share_line} {any_product['finding']}"

    return {
        "severity": severity,
        "cause_of_death": autopsy_cause(scan, gate),
        "verdict": autopsy_verdict(scan, gate),
        "any_product_test": any_product,
        "fingerprints": signatures,
        "systems": autopsy_systems(scan),
        "suspicious_lines": top_findings[:10],
        "pretends": pretends["pretends"],
        "proves": pretends["proves"],
        "reality_handoff": autopsy_reality_handoff(scan),
        "fix_order": autopsy_fix_order(scan),
        "share_line": share_line,
    }


def print_autopsy_markdown(result: Dict[str, object]) -> None:
    scan = result["scan"]
    gate = result["judge"]
    report = result["autopsy_report"]
    assert isinstance(scan, dict)
    assert isinstance(gate, dict)
    assert isinstance(report, dict)

    print("# AI UI Autopsy")
    print()
    print(f"Target: {result['target']}")
    print(f"Mode: {result['mode']}")
    print(f"AI-slop score: {scan['score']}/100")
    print(f"Severity: {report['severity']}")
    print(f"Judge gate: {gate['gate']}")
    print(f"Verdict: {report['verdict']}")
    print()
    print("## Cause Of Death")
    print(str(report["cause_of_death"]))
    print()
    print("## Any-Product Test")
    any_product = report["any_product_test"]
    assert isinstance(any_product, dict)
    print(f"Risk: {any_product['risk']}")
    print(str(any_product["finding"]))
    print()
    print("## Fingerprints")
    fingerprints = report["fingerprints"]
    assert isinstance(fingerprints, list)
    if fingerprints:
        for fingerprint in fingerprints:
            print(f"- {fingerprint['name']} ({fingerprint['severity']}): {fingerprint['reason']}")
    else:
        print("- None detected by deterministic scanner.")
    print()
    print("## Forensic Systems")
    print("| System | Status | Evidence |")
    print("| --- | --- | --- |")
    systems = report["systems"]
    assert isinstance(systems, list)
    for row in systems:
        print(f"| {row['system']} | {row['status']} | {row['evidence']} |")
    print()
    print("## Most Suspicious Lines")
    lines = report["suspicious_lines"]
    assert isinstance(lines, list)
    if lines:
        for item in lines:
            print(f"- {item['severity']} / {item['category']}: `{item['file']}:{item['line']}` - {item['reason']} - {item['excerpt']}")
    else:
        print("- No suspicious lines detected by deterministic scanner.")
    print()
    print("## What It Pretends")
    print(str(report["pretends"]))
    print()
    print("## What It Proves")
    print(str(report["proves"]))
    print()
    print("## Reality Handoff")
    handoff = report["reality_handoff"]
    assert isinstance(handoff, dict)
    print(f"Recommendation: {handoff['recommendation']}")
    print(f"Skill: {handoff['skill']}")
    reasons = handoff["reasons"]
    assert isinstance(reasons, list)
    for reason in reasons:
        print(f"- {reason}")
    print()
    print("## Fix Order")
    fixes = report["fix_order"]
    assert isinstance(fixes, list)
    for index, fix in enumerate(fixes, start=1):
        print(f"{index}. {fix['category']}: {fix['move']} ({fix['why']})")
    print()
    print("## Share Line")
    print(f"> {report['share_line']}")


def print_markdown(result: Dict[str, object]) -> None:
    scan = result["scan"]
    gate = result["judge"]
    print("# no-slop")
    print()
    print(f"Mode: {result['mode']}")
    print(f"Target: {result['target']}")
    print(f"Preset: {result['preset']}")
    print(f"Economy: {str(result['economy']).lower()}")
    print(f"AI-slop score: {scan['score']}/100")
    print(f"Judge gate: {gate['gate']}")
    print(f"Panel average: {gate['panel_average']}/10")
    print(f"Lowest judge: {gate['lowest_judge']}/10")
    if gate.get("note"):
        print(f"Note: {gate['note']}")
    print(f"Next action: {result['next_action']}")
    print()
    print("## Dials")
    for name, value in result["dials"].items():
        print(f"- {name}: {value}")
    print()
    print("## Slop Signatures")
    signatures = scan["signatures"]
    if signatures:
        for sig in signatures:
            print(f"- {sig['name']} ({sig['severity']}): {sig['reason']}")
    else:
        print("- None detected by deterministic scanner.")
    print()
    print("## Category Breakdown")
    category_counts = scan["category_counts"]
    category_scores = scan["category_scores"]
    if category_counts:
        print("| Category | Count | Score |")
        print("| --- | ---: | ---: |")
        for category in sorted(category_counts):
            print(f"| {category} | {category_counts[category]} | {category_scores.get(category, 0)} |")
    else:
        print("- No category hits.")
    print()
    print("## Top Findings")
    findings = scan["top_findings"]
    if findings:
        for item in findings:
            print(f"- {item['severity']} / {item['category']}: `{item['file']}:{item['line']}` - {item['reason']} - {item['excerpt']}")
    else:
        print("- No findings.")
    print()
    print("## Judges")
    for item in gate["judges"]:
        print(f"- {item['name']}: {item['score']}/10 {item['verdict']} - {item['blocker']}")
    print()
    print("## Hard Blockers")
    blockers = gate["hard_blockers"]
    if blockers:
        for blocker in blockers:
            print(f"- {blocker}")
    else:
        print("- None detected by deterministic scanner.")


def main(argv: Sequence[str]) -> int:
    try:
        args = parse_args(argv)
        result = build_result(args)
    except (ValueError, FileNotFoundError) as exc:
        print(f"no-slop: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, indent=2))
    elif args.autopsy:
        print_autopsy_markdown(result)
    else:
        print_markdown(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
