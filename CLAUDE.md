# CarlosMH712.github.io

Personal academic site of Carlos Alberto Molina Holguín (Universidad Autónoma de
Chihuahua). Static HTML, no build step. Deployed by GitHub Pages from `main`,
repository root, at <https://carlosmh712.github.io/>.

**A push to `main` publishes.** There is no staging environment.

## Read before writing

| Task | Document |
|---|---|
| Any lecture page | `standards/LECTURE-TEMPLATE.md` |
| A new course, or adding a lecture to one | `standards/COURSE-TEMPLATE.md` |
| Any page at all — colours, type, components | `standards/SITE-DESIGN.md` |
| A Streamlit calculator | `standards/DESIGN-SYSTEM.md` |
| Handing a job to an assistant | `standards/PROMPTS.md` |

## Layout

```text
index.html script.js styles.css   portal; data-i18n + translations object
tools/                            landing page per calculator, trilingual
tutorials/                        software tutorials; hub + one folder per program
tutorials/<program>/              index.html + tutorial pages + lecture.css/js
<course-slug>/                    index.html + lecture pages + lecture.css/js
standards/                        the documents above and the verifier
docs/                             validation records
```

**The verifier only walks top-level directories.** `tutorials/xflr5/` is nested,
so `verify_lectures.py` with no argument does not reach it. Verify it by path:
`python3 standards/verify_lectures.py tutorials/xflr5/perfil-y-polares.html`.

## Preview

```bash
python3 -m http.server 8516 --directory .
```

## Verify before every commit that touches a lecture

```bash
python3 standards/verify_lectures.py
```

Exits non-zero on failure. Structure only — it does not check physics.

## The conventions that actually break things

- **Two translation mechanisms, never mixed.** The root page uses `data-i18n`
  attributes resolved by `script.js`. Course pages and lectures use three sibling
  `data-language="en|es|de"` blocks with two hidden, driven by `lecture.js`.
  Adding a course touches both.
- **Never interleave languages in one element.** Three blocks, two hidden.
  `<strong>Subsonic · Subsónico · Unterschall</strong>` defeats the mechanism.
- **One TOC per language**, pointing at that language's own `-es`/`-de` anchors.
  A shared English TOC sends other readers to hidden elements.
- **All inline maths escaped `\(…\)`.** Writing `(M<1)` with bare parentheses
  renders as literal text and is invisible in review, because display equations
  on the same page still work.
- **German takes the decimal comma** — `0{,}528282`, `\gamma=1{,}4` — in prose,
  tables, and display maths alike. Spanish and English take the point.
- **Recompute every number** before it goes on a page. Nothing is transcribed
  from a book, a table, or an earlier version of the page.
- **`?v=N` is global.** Raising it means raising it in every page of every course
  plus the root, in one commit, or returning visitors keep a cached stylesheet
  against new markup. Currently `v=13`.
- **Lecture files are named for the topic, never the number.** A lecture was once
  inserted between 04 and 05 and became "4.5"; no file had to be renamed.
- **Push when work is done.** Two commits' worth of lectures once existed only on
  one machine and were lost when the folder was deleted. An unpushed commit is
  not a backup.

## Courses

| # | Course | Folder | State |
|---|---|---|---|
| 01 | Aerodynamics I (AE504) | — | script ready, not converted |
| 02 | Aerodynamics II (AE604) | `aerodynamics-ii/` | 16 lectures, complete |
| 03 | Propulsion | — | three calculators live, no lectures |
| 04 | Flight Dynamics and Control | — | script ready, not converted |
| 05 | Fluid Mechanics (MC611) | — | **next up**; script ready |
| 06 | Numerical Methods | — | not started |
| 07 | Aerospace Systems Engineering (AE506) | `aerospace-systems-engineering/` | 24 lectures, complete |

Cards 01–06 already existed in `#teaching` on the root page; card 07 was added
with the course. Aerodynamics II, Fluid Mechanics and Aerospace Systems
Engineering carry links; the rest need a `course_<slug>_link` key added to the
three language blocks of `script.js` plus the anchor on the card. Slugs are
`aero1`, `aero2`, `prop`, `fdc`, `fluid`, `num`, `syseng`.

Source scripts are LaTeX, under `~/Documents/<course>/…/Capitulos/`. Aerospace
Systems Engineering is the exception: its script lives under
`~/Documents/Materias/Aerospace Systems Engineering/` and compiles in two
editions from one `\lightversion` switch. The lectures are cut from the light
edition, whose section order already matches the eleven-slot template.

**Aerospace Systems Engineering is a process course, not a physics course**, and
uses the substitute slot vocabulary of `LECTURE-TEMPLATE.md` §3: `physics` reads
*Engineering situation*, `model` reads *Scope and limits*, `summary` reads
*Operative rules*. The ids are unchanged. A course picks one vocabulary and every
one of its lectures uses it.

Two of its 24 lectures have no chapter behind them in the script. Lecture 20,
the Vee and the SE engine, exists because the script mentions the Vee once and
only to deny its symmetry, while students meet it everywhere else. Lecture 24,
ethics and professional responsibility, covers Unit VI of the `AE506.pdf`
*programa analítico* — *"Ética en la ingeniería"* — which the script does not
reach at all: a grep for `ethic`, `moral` and `responsabilidad profesional`
across the eight units returns nothing. Competency B3 and the manufacturing side
of E2 are still thin, and `AE506.pdf` also lists `E2.D4 Análisis Estructural`
under this subject, which does not belong to it and is a question for whoever
owns the plan of study rather than something to fix in content.

## Software tutorials

`tutorials/` holds guides to the programs used in the courses, one folder per
program, and follows the same trilingual rules as a course. The first series is
`tutorials/xflr5/`; OpenFOAM and Gmsh are the planned next two.

The series runs to **eleven tutorials in three blocks**, from a single airfoil to
a complete aircraft and its static longitudinal, lateral and directional
stability; `tutorials/xflr5/index.html` carries the syllabus and is the record of
what has been promised. Five are published: 1.1, 1.2, 1.3, 2.1 and 3.3. Static
longitudinal stability (3.3) went out ahead of 2.2, 3.1 and 3.2 at the author's request,
so it carries the minimum of 3.1 itself and its previous-tutorial link points to 2.1. Filenames are
topic-based, so inserting an intermediate tutorial renames nothing.

XFLR5 itself was closed on 2026-06-30 and 6.62 is its final release; its successor
is flow5. The series stays on 6.62 by the author's decision of 2026-09-15, and the
series index and every guide carry a visible notice saying so.

The XFLR5 tutorials ship with **Spanish complete and English and German carrying
a per-section summary plus a visible "translation in preparation" notice**. That
is a deliberate, temporary state agreed with the author: the structure is
trilingual and passes the verifier, but the full EN and DE prose is still owed.
Do not treat the summaries as finished translations. The author confirmed on
2026-09-13 that the series is for Spanish-language classes and the other languages
are low priority for now: new tutorials may ship in this same state, and effort
belongs in the Spanish text.

`tutorials/openfoam-compresible/` is the series «OpenFOAM · Compressible flow» (added
2026-09-24), separate from the planned OpenFOAM aircraft series (card 02 of the portal). It runs
on blueCFD-Core 2024 (OpenFOAM 12) on Windows, in the bash terminal that blueCFD installs. Its
first tutorial, the compression–expansion ramp, ships the case as `archivos/rampa.zip`, the first
downloadable file of the tutorials. Pages, index and zip are generated from
`~/Documents/tutoriales/openfoam-compresible/generadores/` (`t11_build.py`, `indice_build.py`).

## Calculators

Separate repositories, deployed on Streamlit Cloud, each with a landing page
under `tools/` and a link from the root page:

`compressible-flow-calculator` · `nozzle-calculator` · `propulsion-calculator`
(turbofan) · `turbojet-calculator` · `ramjet-calculator`

All five serve Aerodynamics II and Propulsion only. Their local working copies
were deleted from `~/Downloads`; re-clone from GitHub before working on one.

**An app belongs to the courses it serves, not to the site.** Most lectures have
no calculator and are complete without one; never bridge a course to an app
because the app exists. Where an app *does* cover a lecture, the two point at
each other and that lecture's worked example is a regression case in the app's
test suite. See `DESIGN-SYSTEM.md` §13 and `LECTURE-TEMPLATE.md` §7.

## Git

Commits go directly to `main`; the whole history is linear and Pages builds from
it. Commit messages are in Spanish. Do not commit or push unless asked.

`.DS_Store` is ignored. The `README-v*.md` files at the root are historical
release records, not current documentation.
