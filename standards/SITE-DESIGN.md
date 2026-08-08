# Site design — the portal, the course pages, the tool landings

What the *website* looks like. `LECTURE-TEMPLATE.md` covers the anatomy of a
lecture and `COURSE-TEMPLATE.md` the anatomy of a course; this covers the visual
layer all of them share, and the parts of the site that are neither — the portal
and the calculator landing pages.

Everything here was read out of `styles.css`, `aerodynamics-ii/lecture.css` and
`tools/tool.css`. Those files are the source of truth; this document exists so a
new page can be built without reverse-engineering three stylesheets.

---

## 1. Three stylesheets, one system

| File | Serves | Loaded by |
|---|---|---|
| `styles.css` | the portal only | `index.html` |
| `<course>/lecture.css` | course index and every lecture | course pages, copied per course |
| `tools/tool.css` | calculator landing pages | `tools/*.html` |

They share the palette and the typography exactly. They do **not** share
components: a `.card` on the portal and a `.course-card` in a course folder are
different components with different rules, and a `.hero` is not a
`.lecture-hero` is not a `.tool-hero`. Do not try to unify them; the duplication
is deliberate and each file is small.

---

## 2. Tokens

Declared as custom properties on `:root` in `styles.css` and `lecture.css`:

```css
--navy:#071d33;  --navy-2:#0b3558;  --blue:#0d568d;  --sky:#eaf4fb;
--ink:#172333;   --muted:#607181;   --line:#d8e2ea;  --paper:#ffffff;
--soft:#f5f8fa;  --accent:#d67b28;  --accent-dark:#b96216;
--success:#176b47;  --warning:#8a5a12;
--shadow:0 18px 50px rgba(18,50,77,.09);
```

`--navy-2`, `--success` and `--warning` exist only in `lecture.css`, because only
lectures have callouts. Widths: `--max:1180px` on the portal;
`--content-width:1160px` and `--reading-width:820px` in lectures — the second is
what keeps a paragraph of physics readable next to a sticky table of contents.

**Never write a hex value into a page.** If a colour is needed that is not in the
list, the answer is almost always one of the thirteen with an opacity.

---

## 3. Typography

Two families, loaded together from Google Fonts on every page:

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:wght@600;700&display=swap" rel="stylesheet" />
```

- **Source Serif 4**, 600/700 — the brand mark, `h1`, and `h2`. Always with
  `letter-spacing:-.03em` and a tight `line-height` near 1.0–1.1.
- **Inter**, 400–700 — everything else. Body copy runs at `line-height:1.65`.

Headings scale fluidly: `clamp(3rem,6.7vw,5.8rem)` for a portal hero `h1`,
`clamp(2.25rem,4.7vw,3.65rem)` for a section `h2`.

### The eyebrow

`.eyebrow`, `.section-label` and `.profile-degree` share one rule: uppercase,
`letter-spacing:.13em`, `font-size:.73rem`, `font-weight:700`. Colour is
`--blue` on light backgrounds and `#9fd6fa` on the navy hero. This small
uppercase line above a heading is the single most repeated element on the site —
it is the `section-label` that `LECTURE-TEMPLATE.md` makes mandatory.

---

## 4. The hero

Every top-of-page hero on the site is the same gradient:

```css
radial-gradient(circle at 75% 18%, rgba(73,171,235,.34), transparent 25rem),
linear-gradient(135deg, #061729, #0a3558 62%, #0c4f83)
```

with white text, `#d7e9f5` body copy and `#9fd6fa` eyebrows. The portal hero
adds a decorative outlined circle bleeding off the bottom-right corner. The
Streamlit apps reproduce the same gradient in `.portal-hero`, which is why a
screenshot of an app and a screenshot of the site read as one product.

---

## 5. Buttons

```css
.button           min-height:47px; padding:.72rem 1.12rem; radius:8px;
                  font-size:.9rem; font-weight:700; transition:.18s
.button:hover     transform:translateY(-1px)
.button.primary   white on --accent, hover --accent-dark
.button.secondary white, 1px rgba(255,255,255,.5) border — for use on the hero
.button.outline   --navy on white, --line border — for use on light surfaces
.button.disabled  opacity .65, pointer-events none
```

A `.button-row` is a flex row with `gap:.8rem` that becomes a full-width column
below 640px. On a lecture hero the order is fixed: previous, next or
back-to-course, then the calculator button if the lecture has one.

---

## 6. Portal components

- **`.card`** — the six teaching cards. `min-height:285px`, `13px` radius,
  `--line` border, a `--accent` number, and the link absolutely positioned at
  the bottom-left so all six line up regardless of copy length.
- **`.tool-card`** — a two-column feature block for a calculator, on a
  `linear-gradient(135deg,#fff,var(--sky))` with a `#bddbef` border.
- **`.status`** — a pill: `--blue` on white, `#b9d8ec` border, fully rounded.
- **`.info-panel`** — a `--soft` block with a `4px solid var(--accent)` left
  border. Inverts to white inside `.section-alt`.
- **`.mini-card`** — the compact three-up grid.

Sections alternate `.section` and `.section-alt` (`--soft` background) down the
page. Vertical rhythm is `6.2rem` per section.

---

## 7. Lecture components

Documented in full by `LECTURE-TEMPLATE.md`; the visual contract is:

- **`.lecture-shell`** — the two-column grid of sticky `.toc` plus article.
- **`.equation-card`** — a bordered white block holding one display equation;
  `.equation-grid` puts two side by side; `.equation-label` titles one.
- **`.callout`** — neutral; `.callout.success` uses `--success`;
  `.callout.warning` uses `--warning`. A callout carries the point a paragraph
  would bury, and there is never more than one warning in a row.
- **`.process-flow`** — numbered steps for the `algorithm` slot.
- **`.check-list`** — the `mistakes` slot, bold claim then correction.
- **`.example`**, **`.solution-step`** (with `.solution-step-number`),
  **`.result-box`** — the worked example.
- **`.validation-case`** — ties the example to a calculator regression test.
- **`.details`** — a `<details>` wrapper for any derivation longer than a few
  lines, so the page stays scannable.
- **`.table-wrap`** — every table is wrapped so it scrolls horizontally on
  mobile instead of widening the page.
- **`.source-note`** — the closing line of the `references` slot.

---

## 8. Tool landing pages

`tools/tool.css` adds one idea the rest of the site does not have: a **mock of
the application** rather than a screenshot, built from divs so it never goes
stale and costs nothing to load.

```text
.app-preview        white card, rotate(1deg), heavy shadow
  .preview-bar      three grey dots and a title, like a window chrome
  .preview-body     115px sidebar + main, grid
    .preview-sidebar   --sky background, small labels
    .preview-main      eyebrow, h2, .preview-metrics (3-up), .preview-chart
```

Around it: `.tool-hero-grid`, `.module-grid` for what the app computes,
`.validation-panel` with `.validation-row` entries naming regression cases,
`.lecture-link-grid` pointing back at the lectures, and `.launch-panel` with the
Streamlit URL. All of it trilingual with `data-language` blocks, like the course
pages and unlike the portal.

---

## 9. Responsive behaviour

Two breakpoints, and only two:

**`max-width:980px`** — the hamburger `.menu-button` appears and `.site-nav`
becomes an absolutely positioned panel; every two-column grid collapses to one;
`.card-grid` and `.mini-grid` go to two columns.

**`max-width:640px`** — single column everywhere; `.button` becomes full width;
hero `h1` drops to `clamp(2.7rem,14vw,4.1rem)`; the footer centres and stacks.

A table never reflows — it scrolls inside `.table-wrap`. A page must never
scroll horizontally at any width.

---

## 10. Translation, again

The portal and the course pages use different mechanisms, and this is the single
easiest thing to get wrong. `COURSE-TEMPLATE.md` §3 has the full table; the short
form:

- **portal** — `data-i18n="key"`, one element, `script.js` swaps the text;
- **course pages, lectures, tool landings** — three sibling
  `data-language="en|es|de"` blocks, two carrying `hidden`, `lecture.js` shows
  one.

Never mix them on one page, and never put two languages in one element.

---

## 11. Asset versioning

Every `<link>` and `<script>` carries `?v=N`, currently `v=11`, and `N` is global
to the site. Raise it in **every** page of **every** course plus the root in one
commit, or returning visitors get a cached stylesheet against new markup. Raise
it when a stylesheet or a script changes — not for a content edit.

---

## 12. Checklist for a new page

- [ ] Palette taken from §2; no raw hex in the markup
- [ ] Inter and Source Serif 4 loaded; no heading in Inter
- [ ] Eyebrow above every section heading
- [ ] The correct hero variant for the page type
- [ ] Buttons from §5, in the fixed order
- [ ] Tables wrapped in `.table-wrap`
- [ ] The right translation mechanism for the page type, not the other one
- [ ] `?v=N` matching the rest of the site
- [ ] Checked at 640px and 980px; no horizontal scroll
