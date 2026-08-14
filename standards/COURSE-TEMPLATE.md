# Course template — standing up a new course

`LECTURE-TEMPLATE.md` says what one lecture page looks like. This says what a
whole *course* looks like: the folder, the course index, the navigation chain,
and the two separate places the site has to be told the course exists.

Written after Aerodynamics II reached sixteen lectures, so that the second
course does not have to rediscover any of it.

---

## 1. What a course is, on disk

```text
<course-slug>/
  index.html          course index: hero, cards, calculator bridge, study path
  lecture.css         copied, not shared
  lecture.js          copied, not shared
  <topic>.html        one file per lecture
```

`lecture.css` and `lecture.js` are **copied into each course folder**, not
linked from the repository root. They are ~19 kB and ~5 kB; duplicating them
is cheaper than coupling every course to a single file that no course owns.
Copy them from `aerodynamics-ii/`. **`lecture.css` is identical in every course**
— if it changes, it changes everywhere at once, in one commit, with `?v=N`
raised.

**`lecture.js` is not.** Its `ui` object is course-owned and *must* be edited on
copy: it carries `course: "Aerodynamics II"` and one label per calculator that
course uses. Copied unedited into `fluid-mechanics/`, the back button reads
"Aerodynamics II" and the calculator keys name apps the course does not use. On
copy, replace the `course` string in the three languages and replace the
calculator keys with the ones this course actually links to. Everything below the
`ui` object — the language switch, the storage, the MathJax rebuild — is shared
and is changed everywhere at once.

---

## 2. Naming

**Folder**: the English course name in kebab-case — `aerodynamics-ii`,
`fluid-mechanics`, `propulsion`, `flight-dynamics`.

**Lecture files**: named for the *topic*, never for the number.

```text
normal-shocks.html          not   lecture-03.html
shock-interactions.html     not   lecture-04b.html
```

This is not cosmetic. Aerodynamics II gained a lecture between 04 and 05 partway
through; it became "Lecture 4.5" in the index and every other file kept its name
and its inbound links. Numbered filenames would have forced a rename cascade
through sixteen files, thirty-two navigation links, and every anchor.

The number lives in exactly two places: the `course-card-number` on the index
card, and the `eyebrow` line in the lecture hero.

---

## 3. Two translation mechanisms — do not mix them

The site has **two independent translation systems**, and adding a course
touches both. Confusing them is the single most likely way to break a page.

| Where | Mechanism | Driver |
|---|---|---|
| Root `index.html` | `data-i18n="key"` attributes, one element, text swapped in place | `translations` object in `script.js` |
| Course `index.html` and every lecture | sibling `data-language="en\|es\|de"` blocks, two hidden | `lecture.js` |

So: the root page has **one** copy of each string plus a dictionary; the course
pages have **three** copies of everything and hide two. Never use `data-i18n`
inside a course folder, and never use `data-language` blocks on the root page.

---

## 4. The course index

Five sections, in this order. Copy `aerodynamics-ii/index.html` and replace
content; the skeleton is not worth rebuilding.

1. **Hero** — three `data-language` divs (eyebrow, `h1`, `hero-copy`), then a
   `hero-meta` with topic chips. Note this is the *one* place where the chips
   are free-form topic labels rather than the fixed three of a lecture hero.
2. **Module overview and cards** — a `section-label` / `section-title` /
   `section-intro` trio per language, a `module-overview` carrying the lecture
   count, then three `course-grid` blocks.
3. **Calculator bridge** — only if the course has calculators. Three
   `tool-choice-grid` blocks naming which lectures each tool serves.
4. **Study path** — four `path-step` items per language.
5. **References** — primary bibliography, closing with a `source-note`.

### The lecture count

`module-overview` carries a literal count in all three languages:

```html
<div class="module-overview"><span>16 lectures available</span><a href="#lecture-07-en">…</a></div>
```

It is a hand-maintained number and it *will* go stale. Update it in all three
language blocks whenever a card is added. Aerodynamics II shipped nine lectures'
worth of "9 lectures available" while carrying twelve.

---

## 5. Card anatomy

One line per card, identical structure in the three grids:

```html
<article class="course-card available">
  <span class="course-card-number">NN</span>
  <h3>Lecture title</h3>
  <p>One sentence naming the actual content, not the topic area.</p>
  <span class="status">Available</span>
  <a href="topic-file.html">Open lecture →</a>
</article>
```

### Status vocabulary

Fixed strings, like the `section-label` vocabulary of `LECTURE-TEMPLATE.md`:

| Meaning | English | Spanish | German |
|---|---|---|---|
| Published | `Available` | `Disponible` | `Verfügbar` |
| Published, supplementary | `Available · Supplementary` | `Disponible · Complementaria` | `Verfügbar · Ergänzend` |
| Not written yet | `Planned` | `Planeada` | `Geplant` |

"Supplementary" is for material the source script itself marks as an extension
rather than core content — Units VII and VIII of Aerodynamics II. It also goes
in the lecture's own hero eyebrow: `Aerodynamics II · Lecture 14 · Supplementary`.

A card whose status is `Planned` carries no `available` class and no link.

---

## 6. The navigation chain

Every lecture is linked from both sides, and each link exists in **four places
per file**:

- once in the hero `button-row` (shared by the three languages, so it uses
  `data-ui-key` for its label);
- once in the `next-nav` at the end of the English article;
- once in the Spanish article;
- once in the German article.

Change a link and you change four lines. Miss one and two languages navigate
somewhere different from the third.

```html
<!-- hero, language-neutral -->
<div class="button-row">
  <a class="button secondary" href="prev.html">← <span data-ui-key="previous">Previous lecture</span></a>
  <a class="button primary" href="next.html"><span data-ui-key="next">Next lecture</span> →</a>
</div>

<!-- end of each language article, translated in place -->
<nav class="next-nav">
  <a class="next-link" href="prev.html"><span>Previous lecture</span>← Short Title</a>
  <a class="next-link" href="next.html"><span>Next lecture</span>Short Title →</a>
</nav>
```

**First lecture**: no previous — use the back-to-course button instead.
**Last lecture**: no next — use back-to-course, and let the `next-nav` close
with the course index.

The `data-ui-key` values every course has are `previous`, `next`, `back`, `home`,
`course`, `tools`, `contents`, `repository`. On top of those, each course's
`lecture.js` defines one key per calculator it links to — Aerodynamics II has
`calculator`, `nozzleCalculator`, `turbofanCalculator`, `turbojetCalculator`,
`ramjetCalculator`; another course defines its own and does not inherit these.
Anything else must be written out three times inside the language articles.

---

## 7. Asset versioning

Every `<link>`, `<script>`, and inbound course-index link carries `?v=N`:

```html
<link rel="stylesheet" href="lecture.css?v=11" />
<script defer src="lecture.js?v=11"></script>
<a href="index.html?v=11" data-ui-key="course">…</a>
```

`N` is global to the site. Raising it means raising it in **every** page of
**every** course plus the root, in the same commit, or returning visitors keep a
cached stylesheet against new markup. Do not raise it for a content-only change;
raise it when `lecture.css` or `lecture.js` changes.

---

## 8. Wiring the course into the site root

The root page does not discover courses. Two edits, both required:

**a. The card in `#teaching` of `index.html`** — the six cards already exist.
An unwired course has a title and a description but no link. Add the anchor:

```html
<a href="fluid-mechanics/index.html?v=11" data-i18n="course_fluid_link">Open course resources →</a>
```

**b. The matching key in all three language blocks of `script.js`**, which is a
single `const translations = { "en": {…}, "es": {…}, "de": {…} }` object:

```js
"course_fluid_link": "Open course resources →",   // en
"course_fluid_link": "Abrir recursos del curso →", // es
"course_fluid_link": "Kursressourcen öffnen →",    // de
```

The existing slugs are `aero1`, `aero2`, `prop`, `fdc`, `fluid`, `num`. A card
with a `data-i18n` key that `script.js` does not define renders its hardcoded
English fallback in all three languages, silently.

---

## 9. Order of operations

1. Copy `aerodynamics-ii/lecture.css` and `lecture.js` into the new folder.
2. Copy `aerodynamics-ii/index.html`, strip it to the skeleton, translate the
   hero and study path, set the lecture count to `0`.
3. Read the source script and decide the lecture split **before** writing any
   page. Write the split down; it is the thing most expensive to change later.
4. Add every card up front with status `Planned` / `Planeada` / `Geplant`.
5. Write lectures one at a time per `LECTURE-TEMPLATE.md`, flipping each card to
   `Available` and raising the count as you go.
6. Chain prev/next as each lecture lands — do not leave it to the end.
7. Wire the root card and the `script.js` key.
8. Run the verifier before every commit.

---

## 10. Verification

```bash
python3 standards/verify_lectures.py fluid-mechanics
```

No arguments audits every course folder. The checks are the structural
invariants of `LECTURE-TEMPLATE.md` §8 plus the course-level ones here: matching
section-id lists across the three languages, `section-label` on every section,
TOC entries equal to sections in count *and order*, no duplicate ids, no broken
anchors, no dead file links, exactly three hero chips, and no TeX outside math
delimiters.

It does not check physics. Numbers are recomputed by hand, per
`LECTURE-TEMPLATE.md` §5, every time.
