# Prompts

Copy-paste briefs for the recurring jobs on this site. Each one is written to be
pasted verbatim after filling the bracketed slots, and each ends by naming the
verification that closes it.

The worked example throughout is **Fluid Mechanics (MC611)**, the next course to
be filled, whose source script is at
`~/Documents/Mecanica de Fluidos v2/Script_Mecánica_de_Fluidos_2026/Capitulos/`.

Two rules apply to every prompt here and are repeated inside each one because
they are the two that have actually been broken:

- **Recompute every number.** Nothing is transcribed from a book, a table, or an
  earlier version of the page.
- **Never interleave languages in one element.** Three sibling blocks, two hidden.

---

## P1 · Stand up a new course

> Set up the course **\<Course name\> (\<code\>)** on `CarlosMH712.github.io`,
> following `standards/COURSE-TEMPLATE.md`.
>
> Source script: **\<path to the LaTeX chapters\>**.
> Folder: **\<course-slug\>**.
>
> Read `standards/COURSE-TEMPLATE.md` first, then:
>
> 1. Read the source script and propose the lecture split — how many lectures,
>    which units map to which, which are core and which the script itself marks
>    as supplementary. **Show me the split and wait for my approval before
>    writing any page.**
> 2. Copy `lecture.css` and `lecture.js` from `aerodynamics-ii/`.
> 3. Build the course `index.html` with all cards present at status
>    `Planned`/`Planeada`/`Geplant`, count set to zero, trilingual hero and
>    study path.
> 4. Wire the root: the `#teaching` card anchor in `index.html` plus the
>    `course_<slug>_link` key in the three language blocks of `script.js`.
>
> Do not write any lecture yet. Finish by running
> `python3 standards/verify_lectures.py <course-slug>` and showing me the output.

Filled in for MC611:

> Set up the course **Fluid Mechanics (MC611)** on `CarlosMH712.github.io`,
> following `standards/COURSE-TEMPLATE.md`. Source script:
> `~/Documents/Mecanica de Fluidos v2/Script_Mecánica_de_Fluidos_2026/Capitulos/`.
> Folder: `fluid-mechanics`. The root card slug is `fluid` and its card already
> exists without a link. …

---

## P2 · Write one lecture

> Write Lecture **\<NN\>** of **\<Course name\>** for `CarlosMH712.github.io`,
> following `standards/LECTURE-TEMPLATE.md`.
>
> Source material: **\<unit or sections of the script\>**.
> File: **\<course-slug\>/\<topic\>.html**.
> \<If applicable:\> Mark it supplementary in the eyebrow and on the index card.
>
> Eleven slots in the fixed order, three language articles, three TOCs, the fixed
> `section-label` vocabulary, ids suffixed `-es`/`-de`. Theory body sized to the
> topic. Omit the `calculator` slot unless a calculator on this site actually
> covers the topic — and if you omit it, omit the hero calculator button too.
>
> **Recompute every number independently before it goes on the page and tell me
> where each one came from.** Where the \<name\> calculator covers the topic, use
> values that are regression targets of its test suite. State plainly in the
> `model` section what the model does *not* claim.
>
> German uses the decimal comma throughout. All inline maths escaped `\(…\)` —
> bare parentheses render as literal text. Never put two languages in one element.
>
> Then: add the card to the course index in all three languages, flip the count,
> chain prev/next in all three languages of this lecture and of its neighbour,
> and run `python3 standards/verify_lectures.py <course-slug>`.
>
> Do not commit until I ask and you have shown me the verification.

Filled in for the first MC611 lecture:

> Write Lecture 01 of **Fluid Mechanics** for `CarlosMH712.github.io`, following
> `standards/LECTURE-TEMPLATE.md`. Source material: **Unidad I of the MC611
> script**. File: `fluid-mechanics/fluid-properties.html`. …

---

## P3 · Complete a lecture into the missing languages

For the case where an English draft exists and Spanish and German do not.

> `\<course-slug\>/\<file\>.html` currently has only the \<language\> article.
> Write the missing \<languages\> articles with **exact structural parity**:
> the same section count, the same section ids modulo the `-es`/`-de` suffix,
> the same equations, the same tables, the same reference list, the same number
> of callouts. Insert them as siblings before `</div></main>`, each with its own
> `next-nav`.
>
> Add the matching `toc-links` block per language, pointing at that language's
> own suffixed anchors — a shared English TOC sends other readers to hidden
> elements.
>
> The physics is not translated: equations, symbols, and station numbering stay
> identical. Only prose, labels, and figure text change. German takes the decimal
> comma — `0{,}528282`, `\gamma=1{,}4` — in tables and display maths alike.
>
> The numbers are already verified; do not recompute them, transcribe them
> exactly. Finish with `python3 standards/verify_lectures.py <course-slug>`.

---

## P4 · Add or refresh a calculator

> Build the **\<name\>** calculator following `standards/DESIGN-SYSTEM.md`.
> When in doubt, copy from `compressible-flow-calculator`, the reference
> implementation.
>
> It accompanies Lectures **\<NN–MM\>** of **\<course\>**, so the two must point
> at each other: the app carries `SITE_URL` back to the portal, the lecture's
> `calculator` slot and hero button link to the deployed app, and the worked
> example of Lecture \<NN\> becomes a regression case in the test suite with the
> exact values already on the page.
>
> Also required by `DESIGN-SYSTEM.md` §13: a landing page under `tools/` and a
> link from the root `index.html`, both trilingual.
>
> The README must carry a "what the model does not claim" section in the same
> words the lecture's `model` section uses.

---

## P5 · Audit pass

> Run `python3 standards/verify_lectures.py` over every course and report.
>
> Then, for **\<course-slug\>**, independently recompute every number that
> appears on the pages — every table cell, every solution step, every value in a
> callout — from the exact relations, and report any that do not reproduce. Do
> not fix anything yet; show me the list first.

This is the pass that has historically found real defects: a corrupted `\rho`,
unescaped inline maths, a shared English TOC serving three languages, and two
values that were right only by luck of rounding.

---

## P0 · Session opener

Useful when starting cold in this repository. Usually unnecessary — `CLAUDE.md`
is loaded automatically — but handy when pasting into a bare assistant.

> This is `CarlosMH712.github.io`, a trilingual academic site deployed by GitHub
> Pages from `main`. Read `CLAUDE.md`, then `standards/LECTURE-TEMPLATE.md` and
> `standards/COURSE-TEMPLATE.md` before touching any course page. Do not commit
> or push until I ask.

---

## Writing register

The prose target across every lecture, in all three languages: explain the
mechanism, not the vocabulary. Name what the model refuses to claim as readily as
what it predicts. Prefer the sentence that tells a student why a result is
surprising over the one that restates the equation in words. Avoid filler
openings, avoid summarising what was just said, and let a callout carry the point
that a paragraph would bury.

The lectures already written are the register. When in doubt, read
`aerodynamics-ii/shock-expansion.html` for a core lecture and
`aerodynamics-ii/hypersonic-flow-introduction.html` for one that spends most of
its length explaining where a theory stops working.
