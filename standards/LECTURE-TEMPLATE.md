# Lecture template — course pages and their calculators

The structural standard for a lecture page on `CarlosMH712.github.io`, and for
the computational tool that accompanies it. Companion to `DESIGN-SYSTEM.md`,
which covers the Streamlit applications themselves: that document says what a
calculator looks like, this one says what a *lecture* looks like and how the two
are wired together.

Written so that a new course — Aerodynamics I, Propulsion, Flight Dynamics —
lands with the same shape as Aerodynamics II without anyone having to
reverse-engineer it from nine existing files.

---

## 1. Why the structure is fixed

Students navigate a course by pattern, not by reading every page. If the
objectives are the first thing on Lecture 02 and the fourth thing on Lecture 05,
the pattern is broken and every page has to be read from the top to find
anything. The order below is fixed for exactly that reason.

One block is deliberately *not* fixed — the theory body. Forcing the derivation
of the area–Mach relation and the derivation of the Prandtl–Meyer function into
the same subsection count would damage both. What gets standardised is
everything that surrounds the physics, not the physics.

---

## 2. The ten slots

| # | Slot | `id` | Required |
|---|------|------|----------|
| 1 | Learning objectives | `objectives` | always |
| 2 | Physical picture | `physics` | always |
| 3 | Model and assumptions | `model` | always |
| 4 | **Theory body** | topic-specific, 1–6 sections | always |
| 5 | Calculation algorithm | `algorithm` | when a procedure exists |
| 6 | Worked example | `example` | always |
| 7 | Key equations | `summary` | always |
| 8 | Common mistakes | `mistakes` | always |
| 9 | Further topics | `advanced` | when material is deferred |
| 10 | Computational tool | `calculator` | when a calculator covers it |
| 11 | Sources | `references` | always, and always last |

Slots 5, 9, and 10 are the only optional ones. Everything else appears on every
lecture, in this order, with these ids.

### What belongs in each

**1 · Learning objectives.** Four to six bullets, each starting with a verb the
student can be examined on: *calculate*, *distinguish*, *explain why*,
*recognise when*. Not a topic list — "shock waves" is not an objective,
"calculate the downstream Mach number from \(M_1\)" is.

**2 · Physical picture.** The qualitative setup before any algebra: what
phenomenon, why it matters, what it looks like. This is where the main diagram
goes, and it carries the `lead` paragraph.

**3 · Model and assumptions.** What is assumed, and — equally important — what
is excluded. Ends with a `callout warning` naming what the model does not claim.
This mirrors the "what the model does not claim" section that `DESIGN-SYSTEM.md`
requires of every calculator README; a lecture and its tool should draw the same
boundary in the same words.

**4 · Theory body.** The substance. One to six sections, ids and labels chosen
for the topic. The only rule is that derivations longer than a few lines go
inside a `<details class="details">` so the page stays scannable.

**5 · Calculation algorithm.** A `process-flow` of numbered steps, when the
lecture produces a procedure the student will actually execute. Omit it when the
lecture is conceptual — Lectures 01 and 02 of Aerodynamics II legitimately have
none.

**6 · Worked example.** One complete problem, `solution-step` by `solution-step`,
ending in a `result-box`. Every number must be independently recomputed before
it goes on the page — see §5. When a calculator exists, follow the example with
a `validation-case` block naming the inputs, so the example doubles as a
regression target.

**7 · Key equations.** A compact table recapitulating the operative equations of
the lecture and when each applies. This is the section students use before an
exam. It carries the convention already used in the Aerodynamics II script,
where Units III and IV close with a *tabla operativa de ecuaciones*.

**8 · Common mistakes.** A `check-list` of errors seen in actual student work,
each as **bold claim** followed by the correction. Draw from the script's own
*errores comunes* tables where they exist; they are better than invented ones
because they come from grading.

**9 · Further topics.** Only when the script develops material the lecture
defers. Name the topics explicitly so the omission is visible rather than
silent.

**10 · Computational tool.** What the calculator does for this lecture, which
inputs correspond to it, and a button. Not a duplicate of the tool's own landing
page under `tools/` — one paragraph and a link.

**11 · Sources.** See §4.

---

## 3. Trilingual conventions

Every lecture ships in English, Spanish, and German, and the three must be
**structurally identical**: same sections, same ids modulo suffix, same
equations, same figures, same reference count.

### Architecture

Three sibling `<article class="lecture" data-language="xx">` blocks, plus three
`<div class="toc-links" data-language="xx">` blocks in the sidebar. `lecture.js`
shows one and hides the others.

```html
<aside class="toc">
  <h2 data-ui-key="contents">On this page</h2>
  <div class="toc-links" data-language="en">…</div>
  <div class="toc-links" data-language="es" hidden>…</div>
  <div class="toc-links" data-language="de" hidden>…</div>
</aside>

<article class="lecture" data-language="en">…</article>
<article class="lecture" data-language="es" hidden>…</article>
<article class="lecture" data-language="de" hidden>…</article>
```

> **Do not use a single TOC.** A shared index in English with anchors pointing
> only at the English sections sends Spanish and German readers to hidden
> elements. Each language needs its own TOC pointing at its own suffixed ids.
> This bug shipped once and survived nine lectures before it was caught.

> **Do not interleave languages inside one element.** `<strong>Subsonic ·
> Subsónico · Unterschall</strong>` looks compact and defeats the whole
> mechanism: nothing can hide it, and every reader sees all three. This also
> shipped once, across the three nozzle lectures.

### Id suffixes

English sections carry the bare id; Spanish and German append `-es` and `-de`.

```
#objectives   #objectives-es   #objectives-de
```

### Fixed label vocabulary

`<p class="section-label">` is mandatory on all eleven slots, **including
`references`**, which was the only section historically missing one. The strings
are fixed:

| Slot | English | Spanish | German |
|---|---|---|---|
| `objectives` | Learning objectives | Objetivos de aprendizaje | Lernziele |
| `physics` | Physical picture | Panorama físico | Physikalisches Bild |
| `model` | Model and assumptions | Modelo e hipótesis | Modell und Annahmen |
| `algorithm` | Calculation algorithm | Algoritmo de cálculo | Rechenalgorithmus |
| `example` | Worked example | Ejemplo resuelto | Rechenbeispiel |
| `summary` | Key equations | Ecuaciones clave | Kerngleichungen |
| `mistakes` | Common mistakes | Errores comunes | Häufige Fehler |
| `advanced` | Further topics | Temas complementarios | Weiterführende Themen |
| `calculator` | Computational tool | Herramienta computacional | Rechenwerkzeug |
| `references` | Sources | Fuentes | Quellen |

Theory-body labels are free, but should describe the *role* of the section
("Central relation", "Integrated form") rather than restate its heading.

### Process-course variant

Three of the slot labels assume the lecture derives physics. They do not fit a
course whose subject is engineering *method* rather than a governed phenomenon —
Aerospace Systems Engineering is the first such course on the site, and
Numerical Methods will be the second. For those courses, and only for those,
three labels take a substitute string. **The `id` does not change**, so the
verifier, the TOC ordering, and the eleven-slot order are untouched.

| Slot | English | Spanish | German |
|---|---|---|---|
| `physics` | Engineering situation | Situación de ingeniería | Ingenieurtechnischer Kontext |
| `model` | Scope and limits | Alcance y límites | Geltungsbereich und Grenzen |
| `summary` | Operative rules | Reglas operativas | Arbeitsregeln |

The substitution is per course, not per lecture: a course picks one vocabulary
and every one of its lectures uses it. Mixing the two inside a course breaks the
navigational pattern the fixed vocabulary exists to protect.

What each substituted slot must still deliver:

- **Engineering situation** — the decision or failure the lecture addresses,
  before any procedure. Carries the `lead` paragraph and the main diagram, exactly
  as `physics` does.
- **Scope and limits** — what the method assumes, what it does not decide, and
  what it must not be used for. Still ends in a `callout warning`. For a method
  the warning is usually about over-reading its output: a risk matrix ranks, it
  does not analyse.
- **Operative rules** — the compact recapitulation students use before an exam.
  Where a physics lecture tabulates equations, a method lecture tabulates the
  rule, its trigger, and its consequence. A method lecture that *does* have
  equations — RPN, fault-tree gates, a weighted sum — tabulates them here
  alongside the rules.

### Physics is not translated

Equations, symbols, and station numbering stay identical in all three languages.
Only prose, labels, and figure text are translated. German uses the decimal
comma throughout — `0{,}528282`, `\gamma=1{,}4` — and Spanish and English use
the decimal point.

---

## 4. References

Fixed order, full bibliographic form, **identical entries in all three
languages** — only the section heading and the publisher city format change.

1. The course's primary textbook, with chapter or section.
2. The specialised reference for the topic.
3. The standard tables, linked to a permanent archive.
4. Any topic-specific source.
5. The `programa analítico` of the course.

```html
<li>Anderson, J. D., Jr. <em>Fundamentals of Aerodynamics</em>, 6th ed.
    New York: McGraw-Hill Education, 2017, Chapter 8.</li>
<li>Ames Research Staff.
    <a href="https://ntrs.nasa.gov/citations/19930091059" target="_blank"
       rel="noopener noreferrer"><em>Equations, Tables, and Charts for
    Compressible Flow</em>, NACA Report 1135</a>. Washington, DC: NACA, 1953.</li>
```

Close with a `source-note` naming the unit of the script the lecture came from,
and stating whether the numbers were recomputed.

---

## 5. Numbers

**Recompute every number before it goes on the page.** Not one value in a worked
example, table, or callout should be transcribed from a book, a table, or an
earlier version of the page without being independently evaluated first.

This is not pedantry. Two of the values that shipped in Aerodynamics II were
correct only by luck of rounding, and the exercise of recomputing them is what
surfaced the corrupted `\rho` and the unescaped inline math.

Where a calculator exists, prefer example values that are already regression
targets of that calculator. The Aerodynamics II nozzle lectures use
\(p_e/p_0 = 0.937162\), \(0.513401\), \(0.093933\), and \(0.704452\), all of
which appear in the nozzle calculator's test suite. An example that doubles as a
regression case cannot silently drift away from the tool.

Where no calculator covers the topic — the ordinary case, see §7 — choose values
that exercise the physics rather than values that round well, and say in the
`source-note` how they were verified. The obligation to recompute does not weaken
when there is no app to check against; it is the only check there is.

---

## 6. Page furniture

### Hero

Exactly three chips, in this order, all trilingual:

```html
<div class="hero-meta">
  <span data-language="en">Estimated reading: 40 min</span>
  <span data-language="es" hidden>Lectura estimada: 40 min</span>
  <span data-language="de" hidden>Lesedauer: ca. 40 min</span>
  <span data-language="en">Level: undergraduate</span>
  <span data-language="es" hidden>Nivel: licenciatura</span>
  <span data-language="de" hidden>Niveau: Bachelor</span>
  <span data-language="en">Model: inviscid perfect gas</span>
  <span data-language="es" hidden>Modelo: gas perfecto inviscido</span>
  <span data-language="de" hidden>Modell: reibungsfreies ideales Gas</span>
</div>
```

Reading time, then level, then the model's scope. Not the entry condition, not a
result — those belong in the body. Four chips of mixed category is what the
pages drifted into before this rule.

### Maths

MathJax with `\(…\)` inline and `\[…\]` display. **Inline maths must be
escaped.** Writing `(M<1)` with bare parentheses renders as literal text; it is
invisible in review because display equations on the same page still work. Check
a new page by counting: a lecture should have a hundred or more `\(` in source.

### Asset versioning

Every `<link>` and `<script>` carries `?v=N`. Raising N requires raising it in
**every** page at once, or returning visitors keep the cached stylesheet.

---

## 7. Wiring a lecture to its calculator

### Most lectures have no calculator, and that is the normal state

A calculator is built when a topic has a procedure worth automating, not so that
every lecture has a button. Aerodynamics II has five apps across sixteen
lectures; the other eleven omit slot 10 and are complete. **A lecture without a
calculator is not missing anything** — do not invent a bridge to an app from
another course because one happens to exist. Fluid Mechanics does not use the
compressible-flow or nozzle calculators, and its pages must not link to them.

The test for whether a lecture links to an app is narrow: *does this app compute
the quantity this lecture teaches, in the notation this lecture uses?* Anything
looser produces a link the student follows once and never again.

### When one does exist, all four legs are wired

- The lecture's `calculator` section and hero button link to the deployed app.
- The app's sidebar carries `SITE_URL` back to the portal.
- The tool's landing page under `tools/` links to the lectures that cover it.
- Worked-example values are regression targets in the app's test suite.

`DESIGN-SYSTEM.md` §13 requires "a landing page under `tools/` and a link from
`index.html`" for every calculator. The lecture side of that contract is this
section.

---

## 8. Checklist for a new lecture

- [ ] Eleven slots present in order; optional ones justified by content
- [ ] Three `article` blocks and three `toc-links` blocks
- [ ] Ids suffixed `-es` / `-de`; no duplicate ids on the page
- [ ] Every TOC anchor resolves in all three languages
- [ ] `section-label` on every section, references included, from the fixed vocabulary
- [ ] Same section count and same reference count in the three languages
- [ ] All inline maths escaped; no bare-parenthesis maths, no interleaved languages
- [ ] Every number independently recomputed — unconditional, calculator or not
- [ ] *If* a calculator covers the topic: example doubles as a regression case
- [ ] Three hero chips in the fixed order
- [ ] References in the fixed order with full bibliographic data and a `source-note`
- [ ] `?v=N` consistent with the rest of the site
- [ ] Previous/next navigation correct in all three languages

---

## 9. Prompt

> Write Lecture NN of **\<course\>** for `CarlosMH712.github.io`, following
> `LECTURE-TEMPLATE.md`. Source material: **\<unit of the script\>**.
>
> Eleven slots in order, three language articles, three TOCs, fixed label
> vocabulary. Theory body sized to the topic. Recompute every number
> independently and tell me where each came from; where the \<name\> calculator
> covers the topic, use values that are regression targets of its test suite.
>
> State plainly in the `model` section what the model does not claim, in the same
> terms the calculator's README uses.
