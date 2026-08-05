#!/usr/bin/env python3
"""Static and numerical validation for Academic Portal v10."""

from __future__ import annotations

import math
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from lxml import etree, html


ROOT = Path(__file__).resolve().parents[1]
NOZZLE_URL = "https://nozzle-calculator.streamlit.app/"
REQUIRED_NOZZLE_FILES = [
    ROOT / "index.html",
    ROOT / "aerodynamics-ii" / "index.html",
    ROOT / "aerodynamics-ii" / "nozzle-flow-fundamentals.html",
    ROOT / "aerodynamics-ii" / "convergent-divergent-nozzles.html",
    ROOT / "aerodynamics-ii" / "nozzle-back-pressure-thrust.html",
    ROOT / "tools" / "nozzle-calculator.html",
]

checks: list[tuple[str, bool, str]] = []


def record(name: str, condition: bool, detail: str = "") -> None:
    checks.append((name, bool(condition), detail))


def area_ratio(mach: float, gamma: float = 1.4) -> float:
    return (1.0 / mach) * (
        (2.0 / (gamma + 1.0)) * (1.0 + 0.5 * (gamma - 1.0) * mach**2)
    ) ** ((gamma + 1.0) / (2.0 * (gamma - 1.0)))


def bisect_root(function, low: float, high: float, iterations: int = 100) -> float:
    f_low = function(low)
    for _ in range(iterations):
        middle = 0.5 * (low + high)
        f_middle = function(middle)
        if f_low * f_middle <= 0.0:
            high = middle
        else:
            low = middle
            f_low = f_middle
    return 0.5 * (low + high)


def mach_from_area(ratio: float, branch: str, gamma: float = 1.4) -> float:
    function = lambda mach: area_ratio(mach, gamma) - ratio
    if branch == "sub":
        return bisect_root(function, 1.0e-8, 1.0 - 1.0e-10)
    return bisect_root(function, 1.0 + 1.0e-10, 20.0)


def pressure_ratio_isentropic(mach: float, gamma: float = 1.4) -> float:
    return (1.0 + 0.5 * (gamma - 1.0) * mach**2) ** (-gamma / (gamma - 1.0))


def normal_shock(mach_1: float, gamma: float = 1.4) -> tuple[float, float, float]:
    mach_2 = math.sqrt(
        (1.0 + 0.5 * (gamma - 1.0) * mach_1**2)
        / (gamma * mach_1**2 - 0.5 * (gamma - 1.0))
    )
    p2_p1 = 1.0 + (2.0 * gamma / (gamma + 1.0)) * (mach_1**2 - 1.0)
    p02_p01 = (
        (((gamma + 1.0) * mach_1**2) / ((gamma - 1.0) * mach_1**2 + 2.0))
        ** (gamma / (gamma - 1.0))
        * ((gamma + 1.0) / (2.0 * gamma * mach_1**2 - (gamma - 1.0)))
        ** (1.0 / (gamma - 1.0))
    )
    return mach_2, p2_p1, p02_p01


def exit_pressure_with_shock(shock_area_ratio: float, exit_area_ratio: float = 2.0) -> tuple[float, float]:
    mach_1 = mach_from_area(shock_area_ratio, "sup")
    _, _, p02_p01 = normal_shock(mach_1)
    a2star_at = 1.0 / p02_p01
    exit_a2star = exit_area_ratio / a2star_at
    mach_exit = mach_from_area(exit_a2star, "sub")
    return pressure_ratio_isentropic(mach_exit) * p02_p01, mach_exit


# Static files, links, fragments, IDs, cache versions, and language parity.
html_files = sorted(ROOT.rglob("*.html"))
record("HTML files discovered", len(html_files) >= 11, f"{len(html_files)} files")

all_ids: dict[Path, set[str]] = {}
documents: dict[Path, etree._Element] = {}
parse_errors: list[str] = []

for path in html_files:
    parser = html.HTMLParser(encoding="utf-8")
    document = html.fromstring(path.read_bytes(), parser=parser)
    documents[path] = document
    errors = [entry for entry in parser.error_log if entry.level_name in {"ERROR", "FATAL"}]
    if errors:
        parse_errors.extend(f"{path.relative_to(ROOT)}:{entry.line}: {entry.message}" for entry in errors)
    ids = [value for value in document.xpath("//*[@id]/@id") if value]
    all_ids[path] = set(ids)
    record(f"Unique IDs: {path.relative_to(ROOT)}", len(ids) == len(set(ids)), f"{len(ids)} ids")

record("HTML parser errors", not parse_errors, "; ".join(parse_errors[:5]))

broken_links: list[str] = []
unsafe_blank_links: list[str] = []
bad_cache_links: list[str] = []

for source, document in documents.items():
    attributes = document.xpath("//*[@href]/@href | //*[@src]/@src")
    for raw in attributes:
        value = raw.strip()
        if not value or value.startswith(("mailto:", "tel:", "data:", "javascript:")):
            continue
        parsed = urlsplit(value)
        if parsed.scheme in {"http", "https"} or value.startswith("//"):
            continue
        target_path = source if not parsed.path else (source.parent / unquote(parsed.path)).resolve()
        try:
            target_path.relative_to(ROOT.resolve())
        except ValueError:
            broken_links.append(f"{source.relative_to(ROOT)} -> {value} (outside root)")
            continue
        if not target_path.exists():
            broken_links.append(f"{source.relative_to(ROOT)} -> {value} (missing)")
            continue
        if parsed.fragment and target_path.suffix.lower() == ".html":
            if target_path not in all_ids:
                fragment_doc = html.fromstring(target_path.read_bytes())
                all_ids[target_path] = set(fragment_doc.xpath("//*[@id]/@id"))
            if parsed.fragment not in all_ids[target_path]:
                broken_links.append(f"{source.relative_to(ROOT)} -> {value} (missing fragment)")
        if target_path.suffix.lower() in {".css", ".js"} and not parsed.query.startswith("v=10"):
            bad_cache_links.append(f"{source.relative_to(ROOT)} -> {value}")

    for element in document.xpath('//*[@target="_blank"]'):
        rel_tokens = set((element.get("rel") or "").split())
        if not {"noopener", "noreferrer"}.issubset(rel_tokens):
            unsafe_blank_links.append(f"{source.relative_to(ROOT)} -> {element.get('href', '')}")

record("Local paths and fragments", not broken_links, "; ".join(broken_links[:8]))
record("Safe external-tab links", not unsafe_blank_links, "; ".join(unsafe_blank_links[:8]))
record("Cache busting v10", not bad_cache_links, "; ".join(bad_cache_links[:8]))

for path in REQUIRED_NOZZLE_FILES:
    record(
        f"Nozzle calculator link: {path.relative_to(ROOT)}",
        path.exists() and NOZZLE_URL in path.read_text(encoding="utf-8"),
    )

for relative in [
    "aerodynamics-ii/index.html",
    "aerodynamics-ii/nozzle-flow-fundamentals.html",
    "aerodynamics-ii/convergent-divergent-nozzles.html",
    "aerodynamics-ii/nozzle-back-pressure-thrust.html",
    "tools/nozzle-calculator.html",
]:
    path = ROOT / relative
    doc = documents[path]
    counts = {language: len(doc.xpath(f'//*[@data-language="{language}"]')) for language in ("en", "es", "de")}
    record(f"Language blocks: {relative}", len(set(counts.values())) == 1, str(counts))

course_index = documents[ROOT / "aerodynamics-ii" / "index.html"]
for language in ("en", "es", "de"):
    cards = course_index.xpath(
        f'//*[@data-language="{language}" and contains(concat(" ", normalize-space(@class), " "), " course-grid ")]'
        '/*[contains(concat(" ", normalize-space(@class), " "), " course-card ")]'
    )
    record(f"Nine course cards ({language})", len(cards) == 9, f"{len(cards)} cards")

record("No obsolete cache versions", not any(token in path.read_text(encoding="utf-8") for path in ROOT.rglob("*.html") for token in ("?v=7", "?v=8", "?v=9")))


# Numerical regression.
gamma = 1.4
m_sub = mach_from_area(2.0, "sub", gamma)
m_sup = mach_from_area(2.0, "sup", gamma)
p_star_p0 = (2.0 / (gamma + 1.0)) ** (gamma / (gamma - 1.0))
p_first = pressure_ratio_isentropic(m_sub, gamma)
_, p2_p1_exit, _ = normal_shock(m_sup, gamma)
p_design = pressure_ratio_isentropic(m_sup, gamma)
p_shock_exit = p_design * p2_p1_exit
p_internal, m_internal_exit = exit_pressure_with_shock(1.5, 2.0)
m_internal_1 = mach_from_area(1.5, "sup", gamma)
m_internal_2, _, _ = normal_shock(m_internal_1, gamma)
inverse_area = bisect_root(lambda ratio: exit_pressure_with_shock(ratio, 2.0)[0] - 0.7, 1.000001, 1.999999)
inverse_pressure, inverse_mach_exit = exit_pressure_with_shock(inverse_area, 2.0)

p0 = 800_000.0
t0 = 400.0
at = 2.0e-3
gas_constant = 287.0
mass_flow = (
    p0 * at / math.sqrt(t0)
    * math.sqrt(gamma / gas_constant)
    * (2.0 / (gamma + 1.0)) ** ((gamma + 1.0) / (2.0 * (gamma - 1.0)))
)

numeric_targets = [
    ("Critical pressure ratio", p_star_p0, 0.5282817877, 1.0e-9),
    ("Area–Mach subsonic root", m_sub, 0.3059038342, 1.0e-9),
    ("Area–Mach supersonic root", m_sup, 2.1971981217, 1.0e-9),
    ("First choking pressure", p_first, 0.9371625024, 1.0e-9),
    ("Design pressure", p_design, 0.0939326457, 1.0e-9),
    ("Shock-at-exit pressure", p_shock_exit, 0.5134007279, 1.0e-9),
    ("Known internal-shock M1", m_internal_1, 1.8541235267, 1.0e-9),
    ("Known internal-shock M2", m_internal_2, 0.6048432152, 5.0e-7),
    ("Known internal-shock exit Mach", m_internal_exit, 0.4041970508, 5.0e-7),
    ("Known internal-shock exit pressure", p_internal, 0.7044524318, 5.0e-7),
    ("Inverse shock area", inverse_area, 1.51009, 2.0e-5),
    ("Inverse shock exit Mach", inverse_mach_exit, 0.40669, 2.0e-5),
    ("Inverse shock pressure closure", inverse_pressure, 0.7, 1.0e-10),
    ("Critical mass flow", mass_flow, 3.233474, 1.0e-6),
]

for name, actual, expected, tolerance in numeric_targets:
    record(name, abs(actual - expected) <= tolerance, f"actual={actual:.10f}, expected={expected:.10f}")


passed = sum(condition for _, condition, _ in checks)
failed = len(checks) - passed
print(f"Portal v10 validation: {passed}/{len(checks)} checks passed")
for name, condition, detail in checks:
    marker = "PASS" if condition else "FAIL"
    print(f"[{marker}] {name}" + (f" — {detail}" if detail else ""))

if failed:
    sys.exit(1)
