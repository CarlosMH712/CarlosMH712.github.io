# Standards

Everything that has to stay consistent across courses, calculators, and the
portal. Read the relevant document *before* writing, not after — most of what is
here was learned by having to undo something.

| File | What it governs | Read it when |
|---|---|---|
| [`LECTURE-TEMPLATE.md`](LECTURE-TEMPLATE.md) | One lecture page: the eleven slots, the fixed label vocabulary, trilingual architecture, references, numbers | Writing or reviewing any lecture |
| [`COURSE-TEMPLATE.md`](COURSE-TEMPLATE.md) | A whole course: folder layout, the course index, cards, the prev/next chain, wiring into the site root | Starting a new course, or adding a lecture to one |
| [`SITE-DESIGN.md`](SITE-DESIGN.md) | The visual layer: tokens, typography, hero, buttons, the components of all three stylesheets, responsive rules | Building or changing any page |
| [`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md) | The Streamlit calculators: repository layout, colour and type, figures, diagnostics, units, tests, README | Building or changing a calculator |
| [`PROMPTS.md`](PROMPTS.md) | Copy-paste briefs for each of the recurring jobs | Handing any of the above to an assistant |
| [`verify_lectures.py`](verify_lectures.py) | The structural checks, mechanised | Before every commit that touches a lecture |

> **`DESIGN-SYSTEM.md` was rebuilt from the shipped code**, after the original
> was lost with an unpushed commit. It was reconstructed by reading
> `compressible-flow-calculator` — its `config.toml`, `app.py`, `plots.py`,
> `tests/` and README — rather than from memory. The five repositories remain the
> real source of truth; where a repository and this document disagree, correct
> the document.

## The verifier

```bash
python3 standards/verify_lectures.py                  # every course
python3 standards/verify_lectures.py fluid-mechanics  # one course
```

Exits non-zero on any failure, so it can gate a commit. It checks structure
only — matching section ids across the three languages, `section-label`
coverage, TOC order, duplicate ids, broken anchors, dead file links, hero chips,
and TeX left outside math delimiters.

**It does not check physics.** Every number on every page is recomputed
independently before it ships, per `LECTURE-TEMPLATE.md` §5. Two values once
shipped correct only by luck of rounding, and the exercise of recomputing them
is what surfaced a corrupted `\rho` and a page of unescaped inline maths.

## The three failures worth memorising

These shipped, survived review, and had to be repaired across many files at once:

1. **One shared English TOC** serving all three languages, whose anchors pointed
   at sections hidden for Spanish and German readers. Survived nine lectures.
2. **Interleaved languages in a single element** — `<strong>Subsonic ·
   Subsónico · Unterschall</strong>` — which nothing can hide, so every reader
   saw all three. Shipped across the three nozzle lectures.
3. **Unescaped inline maths** — `(M<1)` with bare parentheses renders as literal
   text, and it is invisible in review because display equations on the same page
   still render correctly.

The verifier now catches all three.

## Push early

A fourth failure, from outside the code: two commits' worth of work existed only
on this machine when the working folder was deleted. Lectures 12–15 and this
folder were reconstructed from a session transcript; `DESIGN-SYSTEM.md` was not,
because nobody had read it. **A commit that is not pushed is not a backup.**
