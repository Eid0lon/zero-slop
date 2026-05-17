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
    match: str = ""
    confidence: str = "medium"
    effective_points: int | None = None
    action: str = "counted"
    context: str = ""
    counter_evidence: Sequence[str] = ()
    amplifiers: Sequence[str] = ()


PATTERNS: Sequence[Pattern] = (
    Pattern("Aesthetic Defaults", "High", 8, re.compile(r"from-blue|to-purple|from-indigo|to-pink|from-cyan|to-blue|bg-clip-text|text-transparent", re.I), "template gradient or gradient text"),
    Pattern("Aesthetic Defaults", "Medium", 4, re.compile(r"backdrop-blur|bg-white/10|border-white/20|shadow-2xl|shadow-xl|blur-3xl", re.I), "decorative glass/glow styling"),
    Pattern("Aesthetic Defaults", "Medium", 4, re.compile(r"#6366f1|#8b5cf6|indigo-500|violet-500|purple-600", re.I), "startup purple token"),
    Pattern("Layout Formulae", "High", 8, re.compile(r"Features|Testimonials|Pricing|Get Started|Start Free|Book a demo", re.I), "generic landing-page section or CTA"),
    Pattern("Layout Formulae", "Medium", 4, re.compile(r"grid-cols-3|grid-cols-4|md:grid-cols-3|lg:grid-cols-3|py-24|py-32|text-center", re.I), "formulaic grid/spacing/alignment"),
    Pattern("Component Soup", "Medium", 4, re.compile(r"rounded-2xl|rounded-3xl|hover:scale|hover:-translate-y|hover:shadow", re.I), "over-rounded or hover-lift component cliche"),
    Pattern("Component Soup", "Low", 2, re.compile(r"\b(?:Sparkles|Zap|Shield|Rocket|Star|Award|CheckCircle|TrendingUp)\b"), "generic decorative icon choice"),
    Pattern("Typography Sameness", "Medium", 4, re.compile(r"\b(?:Inter|Geist|Roboto|Plus Jakarta|Space Grotesk)\b|tracking-tight|tracking-\[-", re.I), "default generated typography signal"),
    Pattern("Typography Sameness", "Low", 2, re.compile(r"uppercase.*tracking-wider|text-xs.*uppercase|text-gray-400|text-slate-400", re.I), "weak label/body hierarchy"),
    Pattern("Motion Spam", "Medium", 4, re.compile(r"fadeIn|fade-in|opacity-0|whileInView|animate-.*fade|animate-.*bounce|animate-.*pulse|transition-all", re.I), "decorative or global motion"),
    Pattern("Copy Void", "Medium", 4, re.compile(r"unlock|empower|streamline|revolutionize|seamless|powerful|innovative|next-generation|all-in-one|supercharge", re.I), "generic marketing copy"),
    Pattern("Copy Void", "High", 8, re.compile(r"lorem|ipsum|\bplaceholder\b|\bdummy\b|trusted by|10k\+|99\.9%", re.I), "placeholder or fake proof risk"),
    Pattern("Accessibility Slop", "Critical", 15, re.compile(r"outline-none|focus:outline-none|focus:ring-0", re.I), "focus visibility risk"),
    Pattern("Responsive and Performance Slop", "Medium", 4, re.compile(r"min-h-screen|h-screen|w-screen|overflow-hidden|blur-|backdrop-blur|\bfilter\b|drop-shadow", re.I), "viewport trap or heavy visual effect risk"),
    Pattern("Code and Design-System Smells", "Medium", 4, re.compile(r"className=\"[^\"]*(\s+[^\s\"]+){15,}"), "long utility-class soup"),
    Pattern("Design Token Violation", "High", 8, re.compile(r"bg-\[#|text-\[#|border-\[#|shadow-\[|rounded-\[|#[0-9a-fA-F]{3,8}\b"), "raw visual values bypass tokens"),
    Pattern("Hierarchy Collapse", "High", 8, re.compile(r"text-lg font-semibold|font-semibold text-lg|grid-cols-3.*gap|grid.*gap-8", re.I), "repeated equal-weight hierarchy"),
    Pattern("Brand Incoherence", "Medium", 4, re.compile(r"modern|sleek|premium|beautiful|make it pop", re.I), "brand direction replaced by vague style words"),
)

CATEGORY_SCORE_CAPS: Dict[str, int] = {
    "Accessibility Slop": 30,
    "Aesthetic Defaults": 24,
    "Brand Incoherence": 18,
    "Code and Design-System Smells": 18,
    "Component Soup": 20,
    "Copy Void": 24,
    "Design Token Violation": 24,
    "Hierarchy Collapse": 22,
    "Layout Formulae": 24,
    "Motion Spam": 18,
    "Responsive and Performance Slop": 18,
    "Typography Sameness": 14,
}

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


def finding_points(finding: Finding) -> int:
    if finding.effective_points is None:
        return finding.points
    return finding.effective_points


def severity_for_points(points: int, fallback: str) -> str:
    if points >= 12:
        return "Critical"
    if points >= 7:
        return "High"
    if points >= 3:
        return "Medium"
    if points > 0:
        return "Low"
    return fallback


def nearby_text(lines: Sequence[str], zero_based_line: int, radius: int = 3) -> str:
    start = max(0, zero_based_line - radius)
    end = min(len(lines), zero_based_line + radius + 1)
    return "\n".join(lines[start:end])


def has_accessibility_evidence(text: str) -> bool:
    return bool(re.search(r"focus-visible|focus:ring(?!-0)|aria-|sr-only|role=|tabIndex|keyboard|<label\b|htmlFor=", text, re.I))


def has_focus_replacement(text: str) -> bool:
    return bool(re.search(r"focus-visible|focus:ring(?!-0)|focus-visible:ring|data-\[focus", text, re.I))


def has_design_token_evidence(text: str) -> bool:
    return bool(
        re.search(
            r"var\(--|theme\(|token|semantic|@theme|--(?:color-|surface|background|foreground|accent|primary|secondary|muted|border|ring|radius|shadow|space|text|card|panel)",
            text,
            re.I,
        )
    )


def has_product_specific_evidence(text: str) -> bool:
    return bool(
        re.search(
            r"\b(invoice|expense|transaction|ledger|patient|order|ticket|task|meeting|standup|report|transcript|routing|automation|integration|slack|github|jira|linear|notion|project|repository|deployment|customer|account|calendar|schedule|message|settings|workflow|chart|table|row|record|dataset|queue|incident|policy|claim|shipment|booking)\b",
            text,
            re.I,
        )
    )


def has_fake_proof(text: str) -> bool:
    return bool(re.search(r"lorem|ipsum|\bdummy\b|trusted by|10k\+|99\.9%|fake (?:metric|stat|data|claim)|placeholder (?:handler|data|copy|content)", text, re.I))


def is_heading_context(text: str) -> bool:
    return bool(re.search(r"<h[1-3]\b|\bh[1-3]\b|heading|headline|display title", text, re.I))


def is_interactive_context(text: str) -> bool:
    return bool(re.search(r"<(?:button|a|input|select|textarea)\b|href=|onClick=|role=[\"']button|primary button|cta|submit|action", text, re.I))


def is_placeholder_attribute(text: str) -> bool:
    return bool(re.search(r"\bplaceholder\s*=", text, re.I))


def class_attribute_contains_token(text: str, token: str) -> bool:
    for match in re.finditer(r"\bclass(?:Name)?\s*=\s*([\"'])(.*?)\1", text, re.I):
        classes = match.group(2)
        if re.search(rf"(^|\s){re.escape(token)}($|\s)", classes, re.I):
            return True
    return False


def is_css_filter_context(text: str) -> bool:
    return bool(
        re.search(
            r"(?<![\w.-])filter\s*:\s*(?:none|var\(|blur\(|brightness\(|contrast\(|grayscale\(|hue-rotate\(|invert\(|opacity\(|saturate\(|sepia\(|drop-shadow\()|backdrop-filter",
            text,
            re.I,
        )
        or class_attribute_contains_token(text, "filter")
    )


def is_code_structure_reference(line: str) -> bool:
    return bool(
        re.search(
            r"^\s*(import\b|\{?\s*/\*|//|(?:export\s+default\s+|export\s+)?function\s+[A-Z]|const\s+\w*(?:features|testimonials|pricing)\w*\s*=|(?:features|testimonials|pricing)\s*:|[A-Z][A-Za-z0-9_]*\s*:\s*\(|<\s*/?\s*(?:Features|Testimonials|Pricing|PricingCard)\b|.*[a-zA-Z0-9_]*(?:features|testimonials|pricing)[a-zA-Z0-9_]*\.map\b)",
            line,
            re.I,
        )
    )


def is_anchor_or_identifier_reference(line: str) -> bool:
    return bool(
        re.search(
            r"^\s*(?:\{?\s*)?(?:id|href|key)\s*=\s*['\"]#?(?:features|testimonials|pricing)['\"]\s*[},]?\s*$|^\s*href:\s*['\"]#(?:features|testimonials|pricing)['\"],?\s*$",
            line,
            re.I,
        )
    )


def has_landing_anchor_or_id(line: str) -> bool:
    return bool(re.search(r"\b(?:id|href)\s*=\s*['\"]#?(?:features|testimonials|pricing)['\"]", line, re.I))


def visible_text_contains_match(line: str, match: str) -> bool:
    needle = match.strip()
    if not needle:
        return False
    visible_chunks = re.findall(r">\s*([^<>{}][^<]*)\s*<", line)
    return any(re.search(rf"\b{re.escape(needle)}\b", chunk, re.I) for chunk in visible_chunks)


def visible_landing_label(line: str) -> bool:
    return any(
        visible_text_contains_match(line, label)
        for label in ("Features", "Testimonials", "Pricing", "Get Started", "Start Free", "Book a demo")
    )


def is_navigation_label(line: str) -> bool:
    return bool(re.search(r"\blabel:\s*['\"](?:Features|Testimonials|Pricing)['\"]|^\s*(?:Features|Testimonials|Pricing|See pricing)\s*$", line, re.I))


def is_generic_cta_label(line: str) -> bool:
    return bool(re.search(r"^\s*(?:Get Started|Start Free|Book a demo|Start 14-day trial|Talk to sales)\s*$|cta:\s*['\"](?:Get Started|Start Free|Book a demo|Start 14-day trial|Talk to sales)['\"]", line, re.I))


def has_visual_cliche_cluster(text: str) -> bool:
    hits = 0
    for pattern in (
        r"from-blue|to-purple|from-indigo|to-pink|bg-clip-text|text-transparent",
        r"backdrop-blur|bg-white/10|border-white/20|shadow-2xl|shadow-xl|blur-3xl",
        r"rounded-2xl|rounded-3xl",
        r"Features|Testimonials|Pricing",
        r"unlock|empower|seamless|powerful|innovative|next-generation",
    ):
        if re.search(pattern, text, re.I):
            hits += 1
    return hits >= 3


def calibrated_finding(
    finding: Finding,
    points: int,
    confidence: str,
    action: str,
    context: str,
    counter_evidence: Sequence[str],
    amplifiers: Sequence[str],
) -> Finding:
    return Finding(
        file=finding.file,
        line=finding.line,
        category=finding.category,
        severity=severity_for_points(points, finding.severity),
        points=finding.points,
        reason=finding.reason,
        excerpt=finding.excerpt,
        match=finding.match,
        confidence=confidence,
        effective_points=points,
        action=action,
        context=context,
        counter_evidence=tuple(counter_evidence),
        amplifiers=tuple(amplifiers),
    )


def calibrate_finding(
    finding: Finding,
    lines: Sequence[str],
    reason_counts: Dict[tuple[str, str], int],
    category_counts: Dict[str, int],
) -> Finding:
    line_index = max(0, finding.line - 1)
    line = lines[line_index].strip() if line_index < len(lines) else finding.excerpt
    context_text = nearby_text(lines, line_index)
    combined = f"{line}\n{context_text}"
    match = finding.match.lower()
    points = finding.points
    confidence = "medium"
    action = "counted"
    context = "raw deterministic signal"
    counters: List[str] = []
    amplifiers: List[str] = []
    reason_repeat = reason_counts.get((finding.category, finding.reason), 0)
    category_repeat = category_counts.get(finding.category, 0)

    if reason_repeat >= 4:
        amplifiers.append("repeated same-pattern cluster")
    if has_visual_cliche_cluster(combined):
        amplifiers.append("nearby cliche cluster")

    if finding.category == "Typography Sameness":
        if "tracking-tight" in match and is_heading_context(combined):
            counters.append("tracking-tight is attached to display/heading context")
            points = 0 if reason_repeat <= 2 else 1
            confidence = "low"
            context = "display typography, not automatically slop"
        elif match in {"inter", "geist", "roboto", "plus jakarta", "space grotesk"} and not re.search(r"font|next/font|font-family|class(?:Name)?=", combined, re.I):
            counters.append("font token appears as prose, not UI styling")
            points = 0
            confidence = "low"
            context = "prose mention"
        elif reason_repeat <= 1:
            counters.append("single typography default signal")
            points = min(points, 1)
            confidence = "low"
            context = "weak typography evidence"

    elif finding.category == "Component Soup":
        if re.search(r"hover:scale|hover:-translate-y|hover:shadow", line, re.I):
            if is_interactive_context(combined) and has_accessibility_evidence(combined):
                counters.append("hover affordance has interactive and focus/accessibility context")
                points = 0
                confidence = "low"
                context = "legitimate interactive affordance"
            elif is_interactive_context(combined) and reason_repeat <= 2:
                counters.append("single interactive hover affordance")
                points = 1
                confidence = "low"
                context = "weak component-cliche evidence"
        elif re.search(r"rounded-2xl|rounded-3xl", line, re.I) and reason_repeat <= 2 and not has_visual_cliche_cluster(combined):
            counters.append("large radius is isolated")
            points = 1
            confidence = "low"
            context = "isolated shape token"
        elif finding.severity == "Low" and reason_repeat <= 1:
            counters.append("single decorative icon signal")
            points = 0
            confidence = "low"
            context = "isolated icon choice"

    elif finding.category == "Responsive and Performance Slop":
        if match == "filter" and not is_css_filter_context(line):
            counters.append("filter appears to be product/control copy, not CSS filter")
            points = 0
            confidence = "low"
            context = "filter control wording"
        elif match == "min-h-screen" and not re.search(r"(?<!min-)h-screen|\bw-screen\b|overflow-hidden", combined, re.I):
            counters.append("min-h-screen without a viewport trap cluster")
            points = 1
            confidence = "low"
            context = "weak viewport-risk evidence"
        elif match == "overflow-hidden" and not re.search(r"(?<!min-)h-screen|\bw-screen\b|fixed\b|body\b", combined, re.I):
            counters.append("overflow-hidden is local clipping, not a viewport trap")
            points = 1
            confidence = "low"
            context = "weak overflow evidence"
        elif "backdrop-blur" in match and category_repeat <= 2 and not has_visual_cliche_cluster(combined):
            counters.append("single backdrop blur signal")
            points = 2
            confidence = "low"
            context = "isolated performance-risk evidence"

    elif finding.category == "Copy Void":
        if "placeholder" in match and is_placeholder_attribute(line) and not has_fake_proof(combined):
            counters.append("placeholder is an input affordance, not fake content")
            points = 0
            confidence = "low"
            context = "legitimate form placeholder"
        elif not has_fake_proof(combined) and has_product_specific_evidence(combined) and reason_repeat <= 1:
            counters.append("generic word is surrounded by product-specific nouns")
            points = 1
            confidence = "low"
            context = "weak copy residue"
        elif has_fake_proof(combined):
            confidence = "high"
            context = "unsupported proof/filler evidence"

    elif finding.category == "Layout Formulae":
        visible_label = visible_text_contains_match(line, finding.match)
        visible_generic_label = visible_label or visible_landing_label(line)
        if is_code_structure_reference(line) or is_anchor_or_identifier_reference(line) or (has_landing_anchor_or_id(line) and not visible_generic_label):
            counters.append("match is code structure, import, component name, id, or href; not visible layout proof")
            points = 0
            confidence = "low"
            context = "non-visible code reference"
        elif visible_generic_label and is_interactive_context(line):
            counters.append("visible generic label appears as navigation or action copy")
            points = 1 if not has_visual_cliche_cluster(combined) else min(points, 4)
            confidence = "low" if points <= 1 else "medium"
            context = "weak visible nav/action label evidence"
        elif visible_generic_label:
            counters.append("visible generic landing label is isolated from stronger template proof")
            points = 2 if not has_visual_cliche_cluster(combined) else min(points, 4)
            confidence = "low" if points <= 2 else "medium"
            context = "weak visible section-label evidence"
        elif is_navigation_label(line):
            counters.append("generic label appears as navigation copy only")
            points = 1
            confidence = "low"
            context = "weak nav-label evidence"
        elif is_generic_cta_label(line):
            counters.append("generic CTA label is weak evidence without surrounding template proof")
            points = 2
            confidence = "low"
            context = "weak CTA-label evidence"
        elif re.search(r"text-center|py-24|py-32|grid-cols-[34]|md:grid-cols-3|lg:grid-cols-3", match, re.I) and not has_visual_cliche_cluster(combined):
            counters.append("common layout utility alone is weak formula evidence")
            points = 1
            confidence = "low"
            context = "weak layout-formula evidence"
        elif re.search(r"Features|Testimonials|Pricing|Get Started|Start Free|Book a demo", match, re.I) and reason_repeat <= 1 and has_product_specific_evidence(combined):
            counters.append("generic section/CTA label has product-specific surrounding context")
            points = 2
            confidence = "low"
            context = "isolated landing-page formula"

    elif finding.category == "Aesthetic Defaults":
        if has_design_token_evidence(combined):
            counters.append("visual value is routed through semantic token context")
            points = 1
            confidence = "low"
            context = "token-backed visual styling"
        elif finding.reason == "decorative glass/glow styling" and reason_repeat <= 1 and not has_visual_cliche_cluster(combined):
            counters.append("single decorative effect signal")
            points = 2
            confidence = "low"
            context = "isolated aesthetic evidence"

    elif finding.category == "Design Token Violation":
        if re.search(r"^\s*--[\w-]+\s*:", line):
            counters.append("raw value defines a design token instead of bypassing one")
            points = 0
            confidence = "low"
            context = "token definition"
        elif has_design_token_evidence(combined):
            counters.append("arbitrary value references a semantic CSS variable or theme token")
            points = 0
            confidence = "low"
            context = "token-backed arbitrary value"
        elif reason_repeat <= 1:
            counters.append("single raw visual value")
            points = 4
            confidence = "medium"
            context = "raw token bypass"

    elif finding.category == "Hierarchy Collapse":
        if re.search(r"grid.*gap|grid-cols-3.*gap", line, re.I) and not has_visual_cliche_cluster(combined):
            counters.append("responsive grid alone is weak hierarchy-collapse evidence")
            points = 1
            confidence = "low"
            context = "weak grid hierarchy evidence"
        elif re.search(r"text-lg font-semibold|font-semibold text-lg", line, re.I) and not has_visual_cliche_cluster(combined):
            counters.append("single card-heading weight is not enough to prove hierarchy collapse")
            points = 1
            confidence = "low"
            context = "weak type hierarchy evidence"

    elif finding.category == "Code and Design-System Smells":
        if has_design_token_evidence(combined) or has_product_specific_evidence(combined):
            counters.append("long class string has design-system or product context")
            points = 2
            confidence = "low"
            context = "utility density, not automatic soup"

    elif finding.category == "Accessibility Slop":
        if has_focus_replacement(combined):
            counters.append("focus removal has a visible replacement nearby")
            points = 1
            confidence = "low"
            context = "focus reset with replacement"
        else:
            confidence = "high"
            context = "focus visibility blocker"

    if amplifiers and points > 0 and confidence == "medium":
        confidence = "high"
    if counters and not amplifiers and points > 0 and confidence != "low":
        confidence = "medium"
    if points <= 0:
        action = "ignored"
        points = 0

    return calibrated_finding(finding, points, confidence, action, context, counters, amplifiers)


def calibrate_findings(findings: Sequence[Finding], lines: Sequence[str]) -> List[Finding]:
    reason_counts: Dict[tuple[str, str], int] = {}
    category_counts: Dict[str, int] = {}
    for finding in findings:
        reason_key = (finding.category, finding.reason)
        reason_counts[reason_key] = reason_counts.get(reason_key, 0) + 1
        category_counts[finding.category] = category_counts.get(finding.category, 0) + 1

    calibrated = [calibrate_finding(finding, lines, reason_counts, category_counts) for finding in findings]
    return [finding for finding in calibrated if finding.action != "ignored" and finding_points(finding) > 0]


def aggregate_scan(findings: Sequence[Finding]) -> Dict[str, object]:
    category_scores_raw: Dict[str, Dict[str, int]] = {}
    category_counts: Dict[str, int] = {}
    severity_counts: Dict[str, int] = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}

    for finding in findings:
        points = finding_points(finding)
        bucket = category_scores_raw.setdefault(finding.category, {"high": 0, "medium": 0, "low": 0})
        bucket[finding.confidence if finding.confidence in bucket else "medium"] += points
        category_counts[finding.category] = category_counts.get(finding.category, 0) + 1
        severity_counts[finding.severity] = severity_counts.get(finding.severity, 0) + 1

    category_scores = {
        category: min(parts["high"] + parts["medium"] + min(parts["low"], 6), CATEGORY_SCORE_CAPS.get(category, 24))
        for category, parts in category_scores_raw.items()
        if parts["high"] + parts["medium"] + parts["low"] > 0
    }
    signature_findings = [
        finding
        for finding in findings
        if finding.confidence != "low" and finding_points(finding) >= 2
    ]
    signature_counts: Dict[str, int] = {}
    for finding in signature_findings:
        signature_counts[finding.category] = signature_counts.get(finding.category, 0) + 1

    signatures = detect_signatures(signature_counts, signature_findings)
    signature_score = sum(sig["points"] for sig in signatures)
    score = min(100, sum(category_scores.values()) + signature_score)

    return {
        "findings": list(findings),
        "score": score,
        "category_scores": category_scores,
        "category_counts": category_counts,
        "severity_counts": severity_counts,
        "signatures": signatures,
    }


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
            if path.suffix.lower() == ".md":
                continue
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

    lines = text.splitlines()
    seen_in_file = set()
    for line_no, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped:
            continue
        for pattern in PATTERNS:
            match = pattern.regex.search(stripped)
            if match:
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
                        match=match.group(0)[:80],
                    )
                )
    return calibrate_findings(findings, lines)


def scan_target(target: Path) -> Dict[str, object]:
    root = target if target.is_dir() else target.parent
    files = list(iter_scan_files(target))
    findings: List[Finding] = []
    for path in files:
        findings.extend(scan_file(path, root))

    aggregate = aggregate_scan(findings)

    return {
        "files_scanned": len(files),
        "findings": aggregate["findings"],
        "score": aggregate["score"],
        "category_scores": aggregate["category_scores"],
        "category_counts": aggregate["category_counts"],
        "severity_counts": aggregate["severity_counts"],
        "signatures": aggregate["signatures"],
    }


def scan_prompt(text: str) -> Dict[str, object]:
    findings: List[Finding] = []
    for pattern in PATTERNS:
        match = pattern.regex.search(text)
        if match:
            findings.append(
                Finding(
                    file="<brief>",
                    line=1,
                    category=pattern.category,
                    severity=pattern.severity,
                    points=pattern.points,
                    reason=pattern.reason,
                    excerpt=text[:180],
                    match=match.group(0)[:80],
                )
            )

    findings = calibrate_findings(findings, [text])
    aggregate = aggregate_scan(findings)
    score = min(100, int(aggregate["score"]) + prompt_risk_score(text))
    return {
        "files_scanned": 0,
        "findings": aggregate["findings"],
        "score": score,
        "category_scores": aggregate["category_scores"],
        "category_counts": aggregate["category_counts"],
        "severity_counts": aggregate["severity_counts"],
        "signatures": aggregate["signatures"],
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
    category_scores = scan["category_scores"]
    assert isinstance(counts, dict)
    assert isinstance(category_scores, dict)
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
        category_hit_count = sum(float(category_scores.get(category, 0)) / 4.0 for category in role_penalties[role])
        raw = 10.0 - (score / 18.0) - strict_penalty - (category_hit_count * 0.18) + tolerance_credit
        role_score = round(clamp(raw, 0.0, 10.0), 1)
        verdict = "PASS" if role_score >= thresholds["minimum_lowest_judge"] else "FAIL"
        judges.append(
            {
                "name": role,
                "score": role_score,
                "verdict": verdict,
                "blocker": blocker_for_role(role, category_scores, scan),
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


def strong_finding_count(scan: Dict[str, object], category: str) -> int:
    findings = scan.get("findings")
    if findings is None:
        findings = scan.get("top_findings", [])
    assert isinstance(findings, list)

    count = 0
    for finding in findings:
        if isinstance(finding, Finding):
            finding_category = finding.category
            confidence = finding.confidence
            points = finding_points(finding)
        elif isinstance(finding, dict):
            finding_category = str(finding.get("category", ""))
            confidence = str(finding.get("confidence", "medium"))
            points = int(finding.get("points", 0))
        else:
            continue
        if finding_category == category and confidence != "low" and points >= 3:
            count += 1
    return count


def blocker_for_role(role: str, scores: Dict[str, int], scan: Dict[str, object]) -> str:
    if role == "Visual Forensics Judge" and scores.get("Aesthetic Defaults", 0) >= 8:
        return "template aesthetic signals remain"
    if role == "Product UX Judge" and scores.get("Layout Formulae", 0) >= 12:
        return "formulaic layout obscures product-specific job"
    if role == "Design-System Judge" and scores.get("Design Token Violation", 0) >= 12:
        return "raw styling bypasses semantic tokens"
    if role == "Accessibility and Responsive Judge" and strong_finding_count(scan, "Accessibility Slop"):
        return "focus/accessibility risk detected"
    if role == "Copy and Brand Judge" and scores.get("Copy Void", 0) >= 8:
        return "copy is vague or unsupported"
    if role == "Motion and Interaction Judge" and scores.get("Motion Spam", 0) >= 8:
        return "motion signals lack purpose or reduced-motion proof"
    return "no primary blocker from deterministic scan"


def hard_blockers_for(scan: Dict[str, object]) -> List[str]:
    counts = scan["category_counts"]
    severities = scan["severity_counts"]
    signatures = scan["signatures"]
    findings = scan["findings"]
    assert isinstance(counts, dict)
    assert isinstance(severities, dict)
    assert isinstance(findings, list)

    blockers = []
    if severities.get("Critical", 0):
        blockers.append("critical issue detected")
    if strong_finding_count(scan, "Accessibility Slop"):
        blockers.append("accessibility risk detected")
    if strong_finding_count(scan, "Design Token Violation") >= 3:
        blockers.append("severe design token violation")
    if strong_finding_count(scan, "Hierarchy Collapse") >= 2:
        blockers.append("hierarchy collapse risk")
    for signature in signatures:
        if signature["name"] in {"Ecommerce Urgency Fog", "Token Collapse", "Startup Gradient Stack"}:
            blockers.append(f"slop signature: {signature['name']}")
    return sorted(set(blockers))


def summarize_findings(findings: Sequence[Finding], limit: int = 18) -> List[Dict[str, object]]:
    severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    ordered = sorted(findings, key=lambda f: (severity_order.get(f.severity, 9), -finding_points(f), f.file, f.line))
    return [
        {
            "file": f.file,
            "line": f.line,
            "severity": f.severity,
            "category": f.category,
            "reason": f.reason,
            "excerpt": f.excerpt,
            "match": f.match,
            "confidence": f.confidence,
            "points": finding_points(f),
            "raw_points": f.points,
            "context": f.context,
            "counter_evidence": list(f.counter_evidence),
            "amplifiers": list(f.amplifiers),
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
    weak = re.findall(r"\b(?:modern|sleek|premium|beautiful|clean|hero|features|testimonials|pricing)\b", text, flags=re.I)
    strong = re.findall(r"make it pop|blue-to-purple|indigo-to-pink|glassmorphism|glass cards|10k\+|99\.9%|ai saas", text, flags=re.I)
    if not weak and not strong:
        return 0
    if len(weak) <= 1 and not strong and has_product_specific_evidence(text):
        return 0
    return min(64, max(0, len(weak) - 1) * 4 + len(strong) * 8)


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


def category_score(scan: Dict[str, object], category: str) -> int:
    scores = scan["category_scores"]
    assert isinstance(scores, dict)
    return int(scores.get(category, 0))


def has_strong_finding(scan: Dict[str, object], category: str | None = None) -> bool:
    if category is not None:
        return strong_finding_count(scan, category) > 0

    findings = scan.get("findings")
    if findings is None:
        findings = scan.get("top_findings", [])
    assert isinstance(findings, list)
    for finding in findings:
        if isinstance(finding, Finding):
            finding_category = finding.category
            confidence = finding.confidence
            points = finding_points(finding)
        elif isinstance(finding, dict):
            finding_category = str(finding.get("category", ""))
            confidence = str(finding.get("confidence", "medium"))
            points = int(finding.get("points", 0))
        else:
            continue
        if (category is None or finding_category == category) and confidence != "low" and points >= 3:
            return True
    return False


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
    if score <= 30 and not names and not has_strong_finding(scan):
        return "Only low-confidence residue remains. Treat this as a review queue, not a structural AI-slop failure."
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
    layout = category_score(scan, "Layout Formulae")
    copy = category_score(scan, "Copy Void")
    aesthetic = category_score(scan, "Aesthetic Defaults")

    if has_generic_stack or (layout >= 8 and copy >= 8 and aesthetic >= 8):
        return {
            "risk": "HIGH",
            "finding": "This UI could become a CRM, AI SaaS, analytics tool, or productivity app by changing mostly the logo and nouns.",
        }
    if layout >= 8 or copy >= 8:
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
        score = sum(category_score(scan, category) for category in system["categories"])
        for signature in system.get("signatures", ()):
            if signature in names:
                score += 8
        if score >= int(system["fail_at"]) * 4:
            status = "FAIL"
            note = str(system["fail_note"])
        elif score >= int(system["warn_at"]):
            status = "WARN"
            note = f"{score} calibrated signal point(s) detected."
        else:
            status = "PASS"
            note = str(system["pass_note"])
        rows.append({"system": str(system["name"]), "status": status, "evidence": note})
    return rows


def autopsy_pretends_and_proves(scan: Dict[str, object]) -> Dict[str, str]:
    names = set(signature_names(scan))
    score = int(scan["score"])

    if "Dashboard Theater" in names:
        return {
            "pretends": "A data-backed product with operational credibility.",
            "proves": "The metrics and charts need sources, labels, or a decision path before they can carry trust.",
        }
    if category_score(scan, "Copy Void") >= 8 and category_score(scan, "Layout Formulae") >= 8:
        return {
            "pretends": "A polished product story with momentum and conversion intent.",
            "proves": "The story is still mostly abstract claims and familiar section choreography.",
        }
    if category_score(scan, "Aesthetic Defaults") >= 8 and category_score(scan, "Component Soup") >= 8:
        return {
            "pretends": "Premium visual craft.",
            "proves": "The craft is coming from trend styling rather than product-specific decisions.",
        }
    if category_score(scan, "Accessibility Slop") >= 4 and has_strong_finding(scan, "Accessibility Slop"):
        return {
            "pretends": "A ready-to-ship interface.",
            "proves": "Keyboard or focus risk still blocks a real release.",
        }
    if score <= 15:
        return {
            "pretends": "Nothing suspicious from deterministic patterns alone.",
            "proves": "A deeper review should focus on product truth, browser behavior, and real user workflows.",
        }
    if score <= 30 and not names and not has_strong_finding(scan):
        return {
            "pretends": "A mostly credible interface with a few familiar moves.",
            "proves": "The scanner found low-confidence residue only; human review should focus on product truth and browser behavior.",
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
    if category_score(scan, "Copy Void") >= 8:
        reasons.append("copy/proof may overclaim what the UI actually demonstrates")
    if category_score(scan, "Layout Formulae") >= 8:
        reasons.append("primary CTAs and page sections may still be static demo choreography")
    if category_score(scan, "Accessibility Slop") >= 4 and has_strong_finding(scan, "Accessibility Slop"):
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
    top_findings = scan.get("top_findings")
    if top_findings is None:
        findings = scan.get("findings", [])
        top_findings = summarize_findings(findings) if isinstance(findings, list) else []
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
            meta = f"{item.get('confidence', 'medium')}, {item.get('points', '?')}pt"
            print(f"- {item['severity']} / {item['category']} [{meta}]: `{item['file']}:{item['line']}` - {item['reason']} - {item['excerpt']}")
            if item.get("context"):
                print(f"  Context: {item['context']}")
            counters = item.get("counter_evidence") or []
            if counters:
                print(f"  Counter-evidence: {', '.join(str(counter) for counter in counters)}")
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
            meta = f"{item.get('confidence', 'medium')}, {item.get('points', '?')}pt"
            print(f"- {item['severity']} / {item['category']} [{meta}]: `{item['file']}:{item['line']}` - {item['reason']} - {item['excerpt']}")
            if item.get("context"):
                print(f"  Context: {item['context']}")
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
