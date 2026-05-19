#!/usr/bin/env python3
"""Deterministic helper CLI for the perfect-ux skill.

The skill workflow remains the authority for edits, browser checks, sibling
skill composition, research evidence, and live subagent judging. This script
provides a local precheck for UX contracts and UI source files.
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
    "USER_NEED_FIT",
    "TASK_COMPLETION",
    "IA_CLARITY",
    "COGNITIVE_LOAD",
    "FEEDBACK_QUALITY",
    "ERROR_RECOVERY",
    "A11Y_OPERABILITY",
    "RESPONSIVE_RESILIENCE",
    "PERFORMANCE_FEEL",
    "TRUST_SAFETY",
    "CONTENT_CLARITY",
    "EXPERT_EFFICIENCY",
)

DEFAULT_DIALS: Dict[str, int] = {
    "USER_NEED_FIT": 9,
    "TASK_COMPLETION": 9,
    "IA_CLARITY": 8,
    "COGNITIVE_LOAD": 8,
    "FEEDBACK_QUALITY": 8,
    "ERROR_RECOVERY": 9,
    "A11Y_OPERABILITY": 10,
    "RESPONSIVE_RESILIENCE": 9,
    "PERFORMANCE_FEEL": 8,
    "TRUST_SAFETY": 9,
    "CONTENT_CLARITY": 9,
    "EXPERT_EFFICIENCY": 6,
}

PRESETS: Dict[str, Dict[str, int]] = {
    "operational-saas": {
        "USER_NEED_FIT": 10,
        "TASK_COMPLETION": 10,
        "IA_CLARITY": 9,
        "COGNITIVE_LOAD": 8,
        "FEEDBACK_QUALITY": 9,
        "ERROR_RECOVERY": 10,
        "A11Y_OPERABILITY": 10,
        "RESPONSIVE_RESILIENCE": 9,
        "PERFORMANCE_FEEL": 9,
        "TRUST_SAFETY": 9,
        "CONTENT_CLARITY": 9,
        "EXPERT_EFFICIENCY": 9,
    },
    "dashboard": {
        "USER_NEED_FIT": 10,
        "TASK_COMPLETION": 9,
        "IA_CLARITY": 10,
        "COGNITIVE_LOAD": 9,
        "FEEDBACK_QUALITY": 9,
        "ERROR_RECOVERY": 8,
        "A11Y_OPERABILITY": 10,
        "RESPONSIVE_RESILIENCE": 10,
        "PERFORMANCE_FEEL": 9,
        "TRUST_SAFETY": 10,
        "CONTENT_CLARITY": 9,
        "EXPERT_EFFICIENCY": 8,
    },
    "commerce": {
        "USER_NEED_FIT": 10,
        "TASK_COMPLETION": 10,
        "IA_CLARITY": 9,
        "COGNITIVE_LOAD": 8,
        "FEEDBACK_QUALITY": 9,
        "ERROR_RECOVERY": 10,
        "A11Y_OPERABILITY": 10,
        "RESPONSIVE_RESILIENCE": 10,
        "PERFORMANCE_FEEL": 9,
        "TRUST_SAFETY": 10,
        "CONTENT_CLARITY": 10,
        "EXPERT_EFFICIENCY": 6,
    },
    "onboarding": {
        "USER_NEED_FIT": 10,
        "TASK_COMPLETION": 10,
        "IA_CLARITY": 9,
        "COGNITIVE_LOAD": 10,
        "FEEDBACK_QUALITY": 9,
        "ERROR_RECOVERY": 9,
        "A11Y_OPERABILITY": 10,
        "RESPONSIVE_RESILIENCE": 9,
        "PERFORMANCE_FEEL": 8,
        "TRUST_SAFETY": 9,
        "CONTENT_CLARITY": 10,
        "EXPERT_EFFICIENCY": 5,
    },
    "editor": {
        "USER_NEED_FIT": 10,
        "TASK_COMPLETION": 10,
        "IA_CLARITY": 8,
        "COGNITIVE_LOAD": 9,
        "FEEDBACK_QUALITY": 10,
        "ERROR_RECOVERY": 10,
        "A11Y_OPERABILITY": 10,
        "RESPONSIVE_RESILIENCE": 8,
        "PERFORMANCE_FEEL": 10,
        "TRUST_SAFETY": 8,
        "CONTENT_CLARITY": 8,
        "EXPERT_EFFICIENCY": 10,
    },
    "ai-tool": {
        "USER_NEED_FIT": 10,
        "TASK_COMPLETION": 10,
        "IA_CLARITY": 9,
        "COGNITIVE_LOAD": 9,
        "FEEDBACK_QUALITY": 10,
        "ERROR_RECOVERY": 10,
        "A11Y_OPERABILITY": 10,
        "RESPONSIVE_RESILIENCE": 9,
        "PERFORMANCE_FEEL": 9,
        "TRUST_SAFETY": 10,
        "CONTENT_CLARITY": 10,
        "EXPERT_EFFICIENCY": 8,
    },
    "public-service": {
        "USER_NEED_FIT": 10,
        "TASK_COMPLETION": 10,
        "IA_CLARITY": 10,
        "COGNITIVE_LOAD": 10,
        "FEEDBACK_QUALITY": 10,
        "ERROR_RECOVERY": 10,
        "A11Y_OPERABILITY": 10,
        "RESPONSIVE_RESILIENCE": 10,
        "PERFORMANCE_FEEL": 8,
        "TRUST_SAFETY": 10,
        "CONTENT_CLARITY": 10,
        "EXPERT_EFFICIENCY": 4,
    },
    "mobile": {
        "USER_NEED_FIT": 10,
        "TASK_COMPLETION": 10,
        "IA_CLARITY": 9,
        "COGNITIVE_LOAD": 10,
        "FEEDBACK_QUALITY": 10,
        "ERROR_RECOVERY": 10,
        "A11Y_OPERABILITY": 10,
        "RESPONSIVE_RESILIENCE": 10,
        "PERFORMANCE_FEEL": 10,
        "TRUST_SAFETY": 9,
        "CONTENT_CLARITY": 10,
        "EXPERT_EFFICIENCY": 6,
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
    code: str
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
    code: str
    category: str
    severity: str
    points: int
    reason: str
    excerpt: str
    kind: str


RISK_RULES: Sequence[Rule] = (
    Rule("DEAD_HREF", "Task Completion", "Critical", 18, re.compile(r'href=["\']#["\']', re.I), "dead link blocks completion"),
    Rule("CONSOLE_ACTION", "Task Completion", "Critical", 18, re.compile(r"onClick=.*console\.log|console\.log\(.*(save|submit|send|delete|publish|connect|export)", re.I), "primary-looking action only logs"),
    Rule("ALERT_ACTION", "Feedback", "High", 9, re.compile(r"onClick=.*alert\(|alert\((['\"])(success|saved|submitted|done|error|failed)", re.I), "browser alert is weak workflow feedback"),
    Rule("TODO_PRIMARY", "Task Completion", "High", 10, re.compile(r"todo|coming soon|not implemented|placeholder|dummy", re.I), "placeholder implementation or content"),
    Rule("VAGUE_CTA", "Content Clarity", "Medium", 4, re.compile(r">\s*(Get started|Learn more|Submit|Continue|Next|Click here)\s*<|aria-label=['\"](Get started|Learn more|Submit|Continue|Next)['\"]", re.I), "generic action label hides the user's object or outcome"),
    Rule("GENERIC_PROMISE", "Trust", "Medium", 5, re.compile(r"unlock|empower|seamless|revolutionize|supercharge|effortless|magic|all-in-one|next-generation", re.I), "generic promise does not explain the user's next action"),
    Rule("FAKE_PROOF", "Trust", "High", 12, re.compile(r"trusted by|10k\+|99\.9%|five-star|fortune 500|world-class|bank-grade|SOC ?2|HIPAA|GDPR", re.I), "trust-sensitive claim needs evidence or scope"),
    Rule("AI_CERTAINTY", "Trust", "High", 10, re.compile(r"AI-powered|AI generated|automatically (detects|fixes|decides|approves)|guaranteed accurate|hallucination-free", re.I), "AI capability needs boundaries, review, or uncertainty handling"),
    Rule("PLACEHOLDER_LABEL", "Input", "High", 10, re.compile(r"<input(?![^>]*(aria-label|aria-labelledby))(?=[^>]*placeholder=)", re.I), "input appears to rely on placeholder without a label hook"),
    Rule("DISABLED_NO_REASON", "Feedback", "Medium", 5, re.compile(r"<button[^>]*disabled(?![^>]*(aria-describedby|title=))", re.I), "disabled control may lack a visible reason"),
    Rule("CLICKABLE_DIV", "Accessibility", "Critical", 18, re.compile(r"<(div|span)[^>]*onClick=", re.I), "non-semantic clickable element risks keyboard and assistive-tech failure"),
    Rule("FOCUS_RESET", "Accessibility", "Critical", 18, re.compile(r"focus:outline-none|outline:\s*none|outline-none", re.I), "focus reset without replacement risks keyboard exclusion"),
    Rule("ARIA_HIDDEN_FOCUS", "Accessibility", "Critical", 18, re.compile(r"aria-hidden=['\"]true['\"][^>]*(button|href|tabIndex|tabindex)|<(button|a)[^>]*aria-hidden=['\"]true", re.I), "focusable or interactive content hidden from assistive tech"),
    Rule("COLOR_ONLY", "Accessibility", "High", 8, re.compile(r"text-(red|green|emerald|rose|yellow)-|bg-(red|green|emerald|rose|yellow)-", re.I), "status may be color-only unless paired with text/icon semantics"),
    Rule("VIEWPORT_TRAP", "Responsive", "High", 9, re.compile(r"h-screen|w-screen|100vh|overflow-hidden", re.I), "viewport or overflow trap can break mobile task flow"),
    Rule("MOTION_RISK", "Performance Feel", "Medium", 5, re.compile(r"transition-all|animate-(spin|pulse|bounce)|whileInView|backdrop-blur|blur-3xl", re.I), "motion or visual effect may slow or distract from the task"),
    Rule("LAYOUT_SHIFT_RISK", "Performance Feel", "Medium", 5, re.compile(r"<img(?![^>]*(width=|height=|sizes=|style=|className=.*aspect|class=.*aspect))", re.I), "media may cause layout shift without stable dimensions"),
    Rule("NO_RECOVERY_ERROR", "Error Recovery", "High", 10, re.compile(r"Something went wrong|Oops|Invalid input|Error occurred|try again later", re.I), "error message is not actionable enough"),
    Rule("DESTRUCTIVE_AMBIGUITY", "Error Recovery", "High", 10, re.compile(r">\s*(Delete|Remove|Destroy|Reset)\s*<", re.I), "destructive action needs object name, confirmation, undo, or recovery evidence"),
)

POSITIVE_RULES: Sequence[Rule] = (
    Rule("LABEL_HOOK", "Input", "Positive", 5, re.compile(r"<label|htmlFor=|aria-label=|aria-labelledby=", re.I), "label or accessible-name signal", "positive"),
    Rule("STATE_COVERAGE", "Feedback", "Positive", 6, re.compile(r"loading|submitting|saving|empty|error|success|disabled|pending|stale", re.I), "state coverage signal", "positive"),
    Rule("RECOVERY_CONTROL", "Error Recovery", "Positive", 7, re.compile(r"retry|undo|cancel|restore|back|edit|reconnect|try again", re.I), "recovery path signal", "positive"),
    Rule("FOCUS_VISIBLE", "Accessibility", "Positive", 7, re.compile(r"focus-visible|:focus-visible|focus:ring|data-focus", re.I), "visible focus replacement signal", "positive"),
    Rule("SEMANTIC_STRUCTURE", "Accessibility", "Positive", 5, re.compile(r"<main|<nav|<form|<fieldset|<legend|role=", re.I), "semantic structure signal", "positive"),
    Rule("REDUCED_MOTION", "Accessibility", "Positive", 5, re.compile(r"prefers-reduced-motion|reducedMotion|useReducedMotion", re.I), "reduced-motion support", "positive"),
    Rule("RESPONSIVE_STABILITY", "Responsive", "Positive", 5, re.compile(r"minmax\(|min-w-0|overflow-wrap|break-words|aspect-ratio|aspect-\[|@container|container-type", re.I), "responsive stability signal", "positive"),
    Rule("PERFORMANCE_FEEDBACK", "Performance Feel", "Positive", 5, re.compile(r"skeleton|progress|aria-busy|Suspense|defer|optimistic", re.I), "wait or performance feedback signal", "positive"),
    Rule("TASK_TOOLS", "Expert Efficiency", "Positive", 5, re.compile(r"search|filter|sort|shortcut|kbd|bulk|select all|saved view|recent", re.I), "repeat-use efficiency signal", "positive"),
    Rule("TRUST_BOUNDARY", "Trust", "Positive", 6, re.compile(r"sample data|sandbox|local draft|source|confidence|review|consent|privacy|permission|audit log", re.I), "trust boundary signal", "positive"),
    Rule("VALIDATION", "Input", "Positive", 6, re.compile(r"required|minLength|maxLength|pattern=|schema|zod|yup|validate|aria-invalid", re.I), "validation signal", "positive"),
    Rule("PERSISTENCE", "Task Completion", "Positive", 5, re.compile(r"localStorage|indexedDB|saveDraft|autosave|persist|cache", re.I), "persistence or draft preservation signal", "positive"),
)

DIMENSIONS = (
    "user_need",
    "task_completion",
    "information_architecture",
    "decision_clarity",
    "cognitive_load",
    "input_quality",
    "feedback",
    "error_recovery",
    "accessibility",
    "responsive",
    "performance_feel",
    "trust",
    "content",
    "expert_efficiency",
    "measurement",
)


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="perfect-ux", description="UX quality precheck helper.")
    parser.add_argument("target", nargs="?", default=".", help="File, directory, or brief text.")
    parser.add_argument("-c", "--contract", action="store_true", help="Evaluate a UX contract or brief.")
    parser.add_argument("-m", "--map", action="store_true", help="Map a journey from brief or source.")
    parser.add_argument("-a", "--audit", action="store_true", help="Audit UI source files.")
    parser.add_argument("-f", "--fix", action="store_true", help="Treat target as a UX fix target.")
    parser.add_argument("--harden", action="store_true", help="Audit for hardening readiness.")
    parser.add_argument("-j", "--judge", action="store_true", help="Emit judge-style precheck.")
    parser.add_argument("--verify", action="store_true", help="Emit verification precheck.")
    parser.add_argument("-e", "--economy", action="store_true", help="Mark live judges disabled.")
    parser.add_argument("--preset", choices=sorted(PRESETS), default=None, help="Apply a preset.")
    parser.add_argument("--dial", action="append", default=[], metavar="NAME=0..10", help="Override a dial.")
    parser.add_argument("--no-write", action="store_true", help="Accepted for compatibility; this helper never writes UI files.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    return parser.parse_args(argv)


def resolve_mode(args: argparse.Namespace, target_exists: bool) -> str:
    if args.verify:
        return "verify"
    if args.judge:
        return "judge"
    if args.harden:
        return "harden"
    if args.fix:
        return "fix"
    if args.audit:
        return "audit"
    if args.map:
        return "map"
    if args.contract:
        return "contract"
    return "audit" if target_exists else "contract"


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


def has_focus_replacement(line: str) -> bool:
    return bool(re.search(r"focus-visible|:focus-visible|focus:ring|data-focus", line, re.I))


def color_status_has_text(line: str) -> bool:
    return bool(re.search(r"error|success|warning|failed|saved|active|inactive|status|aria-label|sr-only", line, re.I))


def has_label_for_input(line: str, text: str) -> bool:
    match = re.search(r"id=(['\"])([^'\"]+)\1", line, re.I)
    if not match:
        return False
    input_id = re.escape(match.group(2))
    return bool(re.search(rf"<label[^>]*(htmlFor|for)=(['\"]){input_id}\2", text, re.I))


def should_skip_risk(rule: Rule, line: str, text: str) -> bool:
    if rule.code == "FOCUS_RESET" and has_focus_replacement(line):
        return True
    if rule.code == "PLACEHOLDER_LABEL" and has_label_for_input(line, text):
        return True
    if rule.code == "COLOR_ONLY" and color_status_has_text(line):
        return True
    if rule.code == "DESTRUCTIVE_AMBIGUITY" and re.search(r"undo|confirm|dialog|modal|aria-describedby|delete .*['\"]?\w", line, re.I):
        return True
    return False


def scan_text(text: str, file_name: str = "<brief>") -> List[Finding]:
    findings: List[Finding] = []
    lines = text.splitlines() or [text]
    for line_no, line in enumerate(lines, start=1):
        excerpt = line.strip()
        if not excerpt:
            continue
        for rule in (*RISK_RULES, *POSITIVE_RULES):
            if rule.regex.search(excerpt):
                if rule.kind == "risk" and should_skip_risk(rule, excerpt, text):
                    continue
                findings.append(
                    Finding(
                        file=file_name,
                        line=line_no,
                        code=rule.code,
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
    risk_points = min(120, sum(f.points for f in risks))
    positive_points = min(45, sum(f.points for f in positives))
    category_counts: Dict[str, int] = {}
    risk_category_counts: Dict[str, int] = {}
    positive_category_counts: Dict[str, int] = {}
    severity_counts: Dict[str, int] = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Positive": 0}
    codes: Dict[str, int] = {}

    for finding in findings:
        category_counts[finding.category] = category_counts.get(finding.category, 0) + 1
        codes[finding.code] = codes.get(finding.code, 0) + 1
        if finding.kind == "risk":
            risk_category_counts[finding.category] = risk_category_counts.get(finding.category, 0) + 1
        else:
            positive_category_counts[finding.category] = positive_category_counts.get(finding.category, 0) + 1
        severity_counts[finding.severity] = severity_counts.get(finding.severity, 0) + 1

    base_score = 70 + positive_points - risk_points
    if file_count == 0:
        base_score -= 12
    ux_score = int(clamp(base_score, 0, 100))
    friction_score = int(clamp(risk_points - positive_points * 0.35, 0, 100))
    dimensions = dimension_scores(risk_category_counts, positive_category_counts, severity_counts, ux_score)
    hard_blockers = hard_blockers_for(risk_category_counts, severity_counts, codes, file_count)
    return {
        "files_scanned": file_count,
        "ux_score": ux_score,
        "friction_score": friction_score,
        "risk_points": risk_points,
        "positive_points": positive_points,
        "category_counts": category_counts,
        "risk_category_counts": risk_category_counts,
        "positive_category_counts": positive_category_counts,
        "severity_counts": severity_counts,
        "codes": codes,
        "dimensions": dimensions,
        "findings": list(findings),
        "top_findings": top_findings(risks),
        "positive_signals": top_findings(positives, limit=14),
        "hard_blockers": hard_blockers,
    }


def contract_scan(brief: str) -> Dict[str, object]:
    findings = scan_text(brief)
    lowered = brief.lower()
    contract_terms = {
        "user": bool(re.search(r"user|persona|customer|merchant|analyst|developer|operator|admin|buyer|patient|citizen", lowered)),
        "job": bool(re.search(r"job|task|workflow|journey|create|review|approve|compare|monitor|buy|filter|debug|complete", lowered)),
        "start": bool(re.search(r"start|entry|from|landing|first|route|page|screen", lowered)),
        "completion": bool(re.search(r"complete|success|done|saved|published|purchased|resolved|submitted|finish", lowered)),
        "feedback": bool(re.search(r"loading|feedback|status|progress|success|empty|disabled|pending", lowered)),
        "recovery": bool(re.search(r"error|retry|undo|cancel|recover|validation|failure|back", lowered)),
        "accessibility": bool(re.search(r"accessib|keyboard|focus|contrast|mobile|responsive|reduced motion|screen reader", lowered)),
        "trust": bool(re.search(r"trust|privacy|source|consent|secure|AI|confidence|sample|truth|risk", lowered)),
        "evidence": bool(re.search(r"test|metric|measure|analytics|verify|browser|usability|evidence", lowered)),
    }
    missing = [name for name, ok in contract_terms.items() if not ok]
    scan = summarize_scan(findings, 0)
    scan["hard_blockers"] = [item for item in scan["hard_blockers"] if item != "no scannable UI files found"]
    penalty = len(missing) * 6
    scan["ux_score"] = int(clamp(scan["ux_score"] - penalty + 18, 0, 100))
    scan["missing_contract_terms"] = missing
    if missing:
        scan["hard_blockers"] = sorted(set([*scan["hard_blockers"], "contract missing: " + ", ".join(missing)]))
    return scan


def dimension_scores(
    risk_category_counts: Dict[str, int],
    positive_category_counts: Dict[str, int],
    severity_counts: Dict[str, int],
    ux_score: int,
) -> Dict[str, int]:
    baseline = int(clamp(round(ux_score / 20), 0, 5))
    scores = {dimension: baseline for dimension in DIMENSIONS}

    def lower(dimension: str, amount: int = 1) -> None:
        scores[dimension] = max(0, scores[dimension] - amount)

    def raise_(dimension: str, amount: int = 1) -> None:
        scores[dimension] = min(5, scores[dimension] + amount)

    category_to_dimensions = {
        "Task Completion": ("task_completion", "user_need"),
        "Content Clarity": ("content", "decision_clarity"),
        "Trust": ("trust", "content"),
        "Input": ("input_quality", "error_recovery"),
        "Feedback": ("feedback", "task_completion"),
        "Accessibility": ("accessibility",),
        "Responsive": ("responsive",),
        "Performance Feel": ("performance_feel",),
        "Error Recovery": ("error_recovery", "task_completion"),
        "Expert Efficiency": ("expert_efficiency",),
    }
    for category, count in risk_category_counts.items():
        for dimension in category_to_dimensions.get(category, ()):
            lower(dimension, 2 if severity_counts.get("Critical", 0) and category == "Accessibility" else 1)
    for category in positive_category_counts:
        for dimension in category_to_dimensions.get(category, ()):
            raise_(dimension)
    if positive_category_counts.get("Input", 0) and positive_category_counts.get("Error Recovery", 0):
        raise_("measurement")
    return scores


def top_findings(findings: Sequence[Finding], limit: int = 16) -> List[Dict[str, object]]:
    order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Positive": 4}
    items = sorted(findings, key=lambda f: (order.get(f.severity, 9), f.file, f.line))
    return [
        {
            "file": f.file,
            "line": f.line,
            "code": f.code,
            "severity": f.severity,
            "category": f.category,
            "reason": f.reason,
            "excerpt": f.excerpt,
        }
        for f in items[:limit]
    ]


def hard_blockers_for(
    category_counts: Dict[str, int],
    severity_counts: Dict[str, int],
    codes: Dict[str, int],
    file_count: int,
) -> List[str]:
    blockers: List[str] = []
    if severity_counts.get("Critical", 0):
        blockers.append("critical task completion or accessibility risk")
    if codes.get("DEAD_HREF", 0) or codes.get("CONSOLE_ACTION", 0):
        blockers.append("primary action may be dead or fake")
    if category_counts.get("Input", 0) >= 1:
        blockers.append("form/input labeling or validation risk")
    if category_counts.get("Error Recovery", 0):
        blockers.append("error recovery risk")
    if category_counts.get("Trust", 0) >= 2:
        blockers.append("trust or unsupported-claim risk")
    if category_counts.get("Responsive", 0) >= 2:
        blockers.append("responsive journey risk")
    if file_count == 0:
        blockers.append("no scannable UI files found")
    return sorted(set(blockers))


def thresholds(dials: Dict[str, int]) -> Dict[str, float]:
    strictness = max(
        dials["USER_NEED_FIT"],
        dials["TASK_COMPLETION"],
        dials["A11Y_OPERABILITY"],
        dials["TRUST_SAFETY"],
    )
    return {
        "minimum_panel_average": round(clamp(7.8 + strictness * 0.12, 8.2, 9.2), 1),
        "minimum_lowest_score": round(clamp(7.4 + strictness * 0.10, 7.8, 8.8), 1),
        "minimum_ux_score": round(clamp(80 + strictness * 1.0, 84, 92), 1),
    }


def judge(scan: Dict[str, object], dials: Dict[str, int], economy: bool) -> Dict[str, object]:
    threshold = thresholds(dials)
    ux_score = float(scan["ux_score"])
    hard_blockers = list(scan["hard_blockers"])
    dimensions = scan["dimensions"]
    assert isinstance(dimensions, dict)

    role_dimensions = {
        "User Need Judge": ("user_need", "task_completion", "decision_clarity"),
        "Journey and IA Judge": ("information_architecture", "task_completion", "cognitive_load"),
        "Interaction and Recovery Judge": ("input_quality", "feedback", "error_recovery"),
        "Accessibility and Mobile Judge": ("accessibility", "responsive", "performance_feel"),
        "Content and Trust Judge": ("content", "trust", "decision_clarity"),
        "Measurement and Evidence Judge": ("measurement", "feedback", "task_completion"),
    }
    judges = []
    for role, dims in role_dimensions.items():
        dimension_average = sum(float(dimensions[d]) for d in dims) / len(dims)
        score = round(clamp((ux_score / 10.0) * 0.58 + dimension_average * 0.84, 0, 10), 1)
        verdict = "PASS" if score >= threshold["minimum_lowest_score"] and not hard_blockers else "FAIL"
        judges.append({"name": role, "score": score, "verdict": verdict, "blocker": blocker_for(role, scan)})

    average = round(sum(j["score"] for j in judges) / len(judges), 1)
    lowest = min(j["score"] for j in judges)
    passed = (
        ux_score >= threshold["minimum_ux_score"]
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
    if role == "User Need Judge" and category_counts.get("Task Completion", 0):
        return "primary job or action path may not be finishable"
    if role == "Journey and IA Judge" and category_counts.get("Content Clarity", 0):
        return "labels or CTAs do not reveal the next step"
    if role == "Interaction and Recovery Judge" and (category_counts.get("Input", 0) or category_counts.get("Error Recovery", 0) or category_counts.get("Feedback", 0)):
        return "forms, feedback, or recovery need stronger state coverage"
    if role == "Accessibility and Mobile Judge" and (category_counts.get("Accessibility", 0) or category_counts.get("Responsive", 0)):
        return "accessibility or mobile operability risk detected"
    if role == "Content and Trust Judge" and category_counts.get("Trust", 0):
        return "claims or AI/trust boundaries need evidence"
    if role == "Measurement and Evidence Judge" and scan["hard_blockers"]:
        return "hard blocker remains before evidence can prove success"
    if scan["hard_blockers"]:
        return "hard blocker remains"
    return "no deterministic blocker; live judge still required"


def build_result(args: argparse.Namespace) -> Dict[str, object]:
    target = Path(args.target)
    target_exists = target.exists()
    mode = resolve_mode(args, target_exists)
    dials = resolve_dials(args.preset, args.dial)

    if mode == "contract" or (not target_exists and mode in {"map", "audit", "fix", "harden"}):
        scan = contract_scan(args.target)
    elif target_exists:
        scan = scan_target(target)
    else:
        raise FileNotFoundError(f"Target does not exist: {target}")

    gate = judge(scan, dials, args.economy)
    return {
        "mode": mode,
        "target": str(target),
        "preset": args.preset or "default",
        "economy": bool(args.economy),
        "no_write": bool(args.no_write),
        "dials": dials,
        "scan": {
            "files_scanned": scan["files_scanned"],
            "ux_score": scan["ux_score"],
            "friction_score": scan["friction_score"],
            "risk_points": scan["risk_points"],
            "positive_points": scan["positive_points"],
            "category_counts": scan["category_counts"],
            "risk_category_counts": scan["risk_category_counts"],
            "positive_category_counts": scan["positive_category_counts"],
            "severity_counts": scan["severity_counts"],
            "codes": scan["codes"],
            "dimensions": scan["dimensions"],
            "top_findings": scan["top_findings"],
            "positive_signals": scan["positive_signals"],
            "missing_contract_terms": scan.get("missing_contract_terms", []),
            "hard_blockers": scan["hard_blockers"],
        },
        "judge": gate,
        "next_action": next_action(mode, gate),
    }


def next_action(mode: str, gate: Dict[str, object]) -> str:
    if gate["gate"] == "PRECHECK_PASS_PANEL_REQUIRED":
        return "Run live UX judges and browser journey verification before claiming a full pass."
    if mode == "contract":
        return "Complete or revise the UX Contract before code."
    if gate["gate"] == "FAIL":
        return "Fix hard UX blockers, re-run precheck, then rejudge."
    return "Proceed to journey verification."


def print_markdown(result: Dict[str, object]) -> None:
    scan = result["scan"]
    gate = result["judge"]
    print("# Perfect-UX Precheck")
    print()
    print(f"Mode: {result['mode']}")
    print(f"Target: {result['target']}")
    print(f"Preset: {result['preset']}")
    print(f"UX score: {scan['ux_score']}/100")
    print(f"Friction score: {scan['friction_score']}/100")
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
            print(f"- {item['severity']} / {item['category']} / {item['code']}: `{item['file']}:{item['line']}` - {item['reason']} - {item['excerpt']}")
    else:
        print("- No deterministic risk findings.")
    print()
    print("## Positive Signals")
    if scan["positive_signals"]:
        for item in scan["positive_signals"]:
            print(f"- {item['category']} / {item['code']}: `{item['file']}:{item['line']}` - {item['reason']}")
    else:
        print("- No positive UX implementation signals detected.")
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
        print(f"perfect-ux: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_markdown(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
