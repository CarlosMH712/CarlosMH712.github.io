#!/usr/bin/env python3
"""Structural verifier for course lecture pages.

Checks the invariants of standards/LECTURE-TEMPLATE.md and
standards/COURSE-TEMPLATE.md that can be checked mechanically:

  - three sibling <article class="lecture" data-language="xx"> blocks
  - three matching <div class="toc-links" data-language="xx"> blocks
  - identical section-id lists across the three languages, modulo -es/-de
  - a section-label on every section, references included
  - TOC entries equal to the sections in count AND in order, per language
  - no duplicate ids on the page
  - no broken internal anchors
  - no links to files that do not exist
  - exactly three hero chips per language
  - no TeX macros sitting outside \\(...\\) or \\[...\\] delimiters

It does not check physics. Numbers are recomputed by hand, every time.

Usage:
    python3 standards/verify_lectures.py                 # every course folder
    python3 standards/verify_lectures.py fluid-mechanics # one course
    python3 standards/verify_lectures.py a/x.html        # one file

Exit status is 1 if any check fails, so it can gate a commit.
"""

import os
import re
import sys
from collections import Counter

LANGS = [("en", ""), ("es", "-es"), ("de", "-de")]
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def find_course_dirs():
    """A course folder is any directory holding both index.html and lecture.css."""
    out = []
    for name in sorted(os.listdir(REPO)):
        d = os.path.join(REPO, name)
        if os.path.isdir(d) and not name.startswith("."):
            if os.path.exists(os.path.join(d, "index.html")) and os.path.exists(
                os.path.join(d, "lecture.css")
            ):
                out.append(d)
    return out


def lecture_files(target):
    """Lecture pages of a course folder: every .html except the course index."""
    if os.path.isfile(target):
        return [target]
    return sorted(
        os.path.join(target, f)
        for f in os.listdir(target)
        if f.endswith(".html") and f != "index.html"
    )


def check_file(path):
    problems = []
    name = os.path.relpath(path, REPO)
    if name.startswith(".."):
        name = os.path.abspath(path)
    course_dir = os.path.dirname(path)
    src = open(path, encoding="utf-8").read()

    arts, tocs = {}, {}
    for lang, _ in LANGS:
        m = re.search(
            r'<article class="lecture" data-language="%s"[^>]*>(.*?)</article>' % lang,
            src, re.S,
        )
        if m:
            arts[lang] = m.group(1)
        else:
            problems.append("missing <article data-language=%s>" % lang)

        m = re.search(
            r'<div class="toc-links" data-language="%s"[^>]*>(.*?)</div>' % lang,
            src, re.S,
        )
        if m:
            tocs[lang] = re.findall(r'href="#([^"]+)"', m.group(1))
        else:
            problems.append("missing <div class=toc-links data-language=%s>" % lang)

    if len(arts) == 3 and len(tocs) == 3:
        ids, base = {}, {}
        for lang, suf in LANGS:
            secs = re.findall(r'<section id="([^"]+)"[^>]*>(.*?)</section>', arts[lang], re.S)
            ids[lang] = [i for i, _ in secs]
            for i, body in secs:
                if 'class="section-label"' not in body:
                    problems.append("[%s] section #%s has no section-label" % (lang, i))
            b = []
            for i in ids[lang]:
                if suf and i.endswith(suf):
                    b.append(i[: -len(suf)])
                elif not suf:
                    b.append(i)
                else:
                    problems.append("[%s] id '%s' is missing the '%s' suffix" % (lang, i, suf))
                    b.append(i)
            base[lang] = b

        if not (base["en"] == base["es"] == base["de"]):
            problems.append(
                "section id lists differ across languages\n"
                "      en=%s\n      es=%s\n      de=%s" % (base["en"], base["es"], base["de"])
            )

        for lang, _ in LANGS:
            if tocs[lang] != ids[lang]:
                problems.append(
                    "[%s] TOC does not match sections in order\n"
                    "      toc=%s\n      sec=%s" % (lang, tocs[lang], ids[lang])
                )
        section_count = len(ids["en"])
    else:
        section_count = 0

    all_ids = re.findall(r'\sid="([^"]+)"', src)
    dups = sorted(k for k, v in Counter(all_ids).items() if v > 1)
    if dups:
        problems.append("duplicate ids: %s" % dups)

    idset = set(all_ids)
    broken = sorted(a for a in set(re.findall(r'href="#([^"]+)"', src)) if a and a not in idset)
    if broken:
        problems.append("broken anchors: %s" % broken)

    for href in sorted(set(re.findall(r'href="(?!https?:|#|mailto:)([^"#?]+)', src))):
        if not os.path.exists(os.path.normpath(os.path.join(course_dir, href))):
            problems.append("link target does not exist: %s" % href)

    m = re.search(r'<div class="hero-meta">(.*?)</div>', src, re.S)
    if not m:
        problems.append("no hero-meta block")
    else:
        chips = {l: len(re.findall(r'<span data-language="%s"' % l, m.group(1))) for l, _ in LANGS}
        if set(chips.values()) != {3}:
            problems.append("hero chips per language = %s (expected 3/3/3)" % chips)

    stripped = re.sub(r"\\\(.*?\\\)", "", src, flags=re.S)
    stripped = re.sub(r"\\\[.*?\\\]", "", stripped, flags=re.S)
    stripped = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", stripped, flags=re.S)
    stray = sorted(set(re.findall(r"\\[a-zA-Z]{2,}", stripped)))
    if stray:
        problems.append("TeX macros outside math delimiters: %s" % stray[:8])

    return name, section_count, problems


def main():
    targets = sys.argv[1:]
    if targets:
        paths = []
        for t in targets:
            t = t if os.path.isabs(t) else os.path.join(REPO, t)
            if not os.path.exists(t):
                print("no such path: %s" % t)
                return 1
            paths.extend(lecture_files(t))
    else:
        paths = [p for d in find_course_dirs() for p in lecture_files(d)]

    if not paths:
        print("no lecture files found")
        return 1

    rows, failures = [], 0
    for p in paths:
        name, count, problems = check_file(p)
        rows.append((name, count, len(problems)))
        if problems:
            failures += 1
            print("\n%s" % name)
            for pr in problems:
                print("  - %s" % pr)

    print("\n%-52s %9s %9s" % ("file", "sections", "problems"))
    print("-" * 72)
    for name, count, nprob in rows:
        print("%-52s %9d %9d" % (name, count, nprob))

    print()
    if failures:
        print("FAILED: %d of %d files have problems." % (failures, len(rows)))
        return 1
    print("ALL CHECKS PASSED across %d lecture files." % len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
