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
<course-slug>/                    index.html + lecture pages + lecture.css/js
standards/                        the documents above and the verifier
docs/                             validation records
```

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
  against new markup. Currently `v=12`.
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
