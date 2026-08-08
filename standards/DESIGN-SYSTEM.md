# Design system — the calculators

The reference for building a Streamlit calculator so that it belongs to the same
family as `compressible-flow-calculator`, `nozzle-calculator`,
`propulsion-calculator`, `turbojet-calculator` and `ramjet-calculator`.

Companion to `LECTURE-TEMPLATE.md`, which says what a *lecture* looks like and
how a lecture and its calculator are wired together. This one says what the
*application* looks like.

When in doubt, copy from `compressible-flow-calculator`. It is the reference
implementation, and everything below was read out of it rather than invented.

> **This document was rebuilt from the shipped code**, after the original was
> lost with an unpushed commit. The five repositories are the real source of
> truth; where this file and a repository disagree, the repository wins and this
> file should be corrected.

---

## 1. What a calculator is for

An academic tool that accompanies a lecture. Three consequences that settle most
design questions before they are asked:

- **The textbook formulation is a feature, not a limitation.** A student must be
  able to reproduce the app's numbers by hand from the lecture. Modern
  refinements go in as a *selectable mode*, never as a silent replacement.
- **The worked example of the lecture is a test case of the app.** Not an
  illustration — an actual assertion in `tests/`, so the two cannot drift apart.
- **What the model refuses to claim is part of the interface.** The README and
  the lecture's `model` section state the same exclusions in the same words.

---

## 2. Repository layout

One repository per calculator, deployed on Streamlit Cloud, separate from the
site repository:

```text
app.py                  the whole interface; one file
core/                   the physics, one module per topic, no Streamlit imports
geometry/               optional: shape handling for the topic
visualization/plots.py  every figure, one module
tests/                  pytest, one file per core module
examples/               reproducible input sets
.streamlit/config.toml  theme
requirements.txt
README.md
DEPLOYMENT.md
```

**`core/` never imports Streamlit.** That is what makes the physics testable
without a browser and reusable from a notebook. `app.py` imports `core`; the
dependency never runs the other way.

Modules are named for the physics, not the screen: `isentropic.py`,
`normal_shock.py`, `oblique_shock.py`, `prandtl_meyer.py`, `pitot.py`,
`atmosphere.py`, `units.py`.

---

## 3. Colour and type

The palette is the site's palette. It is not re-chosen per app; the same nine
values appear in `styles.css`, in `lecture.css`, in `.streamlit/config.toml`,
and as constants at the top of `visualization/plots.py`.

| Token | Hex | Where it is used |
|---|---|---|
| navy | `#071d33` | headings, hero background, plot lines and markers |
| navy-2 | `#0b3558` | secondary hero stop, annotation text |
| blue | `#0d568d` | links, section labels, metric top border |
| sky | `#eaf4fb` | sidebar background, secondary surfaces |
| ink | `#172333` | body text |
| muted | `#607181` | captions, axis labels, secondary text |
| line | `#d8e2ea` | borders, grid lines |
| paper | `#ffffff` | cards, plot area |
| soft | `#f5f8fa` | page background |
| accent | `#d67b28` | primary action, emphasis curve |
| accent-dark | `#b96216` | primary action hover |
| success | `#176b47` | validated / design-point marker |
| warning | `#8a5a12` | caution callouts |

Type is two families, loaded from Google Fonts in both the site and the app:

- **Inter** — 400/500/600/700 — all body text, controls, tables, plot fonts.
- **Source Serif 4** — 600/700 — `h1`/`h2` and the hero only.

Never introduce a third family, and never set a heading in Inter.

### `.streamlit/config.toml`

```toml
[theme]
base = "light"
primaryColor = "#d67b28"
backgroundColor = "#f5f8fa"
secondaryBackgroundColor = "#eaf4fb"
textColor = "#172333"
font = "sans serif"

[server]
headless = true

[browser]
gatherUsageStats = false
```

---

## 4. Page structure

Top to bottom, the same order in every app:

1. **`st.set_page_config`** — wide layout, the app's own title and icon.
2. **`inject_css()`** — fonts and the light-theme override (§5).
3. **Portal hero** — a `.portal-hero` block reproducing the site hero: eyebrow,
   `h1` in Source Serif 4, byline, one-paragraph copy, and a row of
   `.hero-chip` pills naming the model's scope.
4. **Sidebar** — language selector, gas constants, units, display decimals, and
   the `SITE_URL` link back to the portal.
5. **Module tabs or radio** — one entry per `core` module.
6. **Per module**: a `section_banner(title, copy)`, the inputs, a
   `metric_grid(...)` of results, the tables, the figure, and the equations in
   an expander.
7. **Validation and sources** at the bottom.

Two helpers carry the visual identity and should be copied verbatim rather than
re-derived: `section_banner` and `metric_grid`. A metric tile is a white card
with a `1px #d8e2ea` border, a `4px #0d568d` top border, `12px` radius and a
`112px` minimum height — that top border is what makes a screenshot of any of
the five apps recognisable as the same family.

`SITE_URL = "https://carlosmh712.github.io/"` is a module-level constant in
`app.py`. Every app links back to the portal; the portal links out to every app.

---

## 5. The light theme, and why `config.toml` is not enough

`base = "light"` in `config.toml` sets the *default*. It does not win against a
visitor whose browser requests a dark colour scheme: Streamlit then recolours
labels, tables and input fields on its own, and the app arrives with white text
on white cards.

The fix is a `st.markdown` block, injected once, that pins the surfaces
explicitly — `stAppViewContainer`, `stHeader`, `stSidebar`, `.block-container`,
`stMetric`, and the table and input classes.

Two traps in that block, both of which have cost a debugging session:

- **No CSS comments inside the injected string.** Streamlit passes it through
  its markdown processor, which eats the opening `/*` and then dumps the rest of
  the stylesheet onto the page as visible text.
- **`unsafe_allow_html=True` is required**, and the `<style>` must be in the
  same `st.markdown` call as the content it styles is not — inject once, early,
  before anything renders.

---

## 6. Figures

Plotly, one module, `visualization/plots.py`, with the palette imported as
module constants (`NAVY`, `BLUE`, `SKY`, `ORANGE`, `GREEN`, `MUTED`, `LINE`,
`SOFT`, `WHITE`).

Every figure passes through a single styling function that sets:

```python
paper_bgcolor="rgba(0,0,0,0)"     # the page gradient shows through
plot_bgcolor=WHITE
font=dict(family="Inter, Arial, sans-serif", color=NAVY)
hoverlabel=dict(bgcolor=WHITE, font_color=NAVY)
```

and then `update_xaxes` / `update_yaxes` with `gridcolor=LINE`,
`zerolinecolor=LINE`, `automargin=True`.

Conventions inside a figure:

- the **selected** curve is `BLUE`; unselected curves are `#9eb4c5`;
- the **operating point** is a `NAVY` marker with a white outline;
- the **design point** is a `GREEN` diamond, larger, white outline;
- a **limit or asymptote** is an `ORANGE` dashed line;
- annotations sit on `rgba(255,255,255,0.62–0.84)` with a `LINE` border, never
  on a bare background.

A figure that needs a legend to be readable usually needs fewer curves instead.

---

## 7. Equations

Every module carries an `equations_<topic>()` function that renders the
governing relations with `st.latex`, inside an expander so the page stays
scannable. The equations are the same ones, in the same notation and the same
station numbering, as the lecture that the module accompanies. A symbol that
means one thing on the page and another in the app is a defect.

---

## 8. Diagnostics

The app says what it is doing and refuses to guess:

- when a root or an integration does not converge, it says so and returns
  nothing — it never falls back to a plausible number;
- when a shock detaches, it reports detachment rather than the strong-branch
  root;
- when an input leaves the model's range (`M < 1` in a supersonic routine,
  negative pressure, a wedge past the maximum deflection) it names the
  violated condition;
- `ρ > 0`, `p > 0`, `T > 0` are asserted, not assumed.

---

## 9. Language

The apps are trilingual like the site: English, Spanish, German, selected in the
sidebar. Labels, table headers and prose are translated; **equations, symbols and
station numbering are not.** The same rule as `LECTURE-TEMPLATE.md` §3.

Table columns are relabelled per language by a helper
(`localized_region_table`), so the underlying dataframe keeps one canonical set
of column names and only the display layer translates.

---

## 10. Units

`core/units.py` owns every conversion. The rest of the code works in SI
internally and converts only at the boundary — inputs on the way in, display on
the way out. Pressure, temperature, density and speed each have a selector in
the sidebar, and the chosen unit is carried into the metric labels and the table
headers so a number is never shown without its unit.

The gas constant is adjustable, not hardcoded, because the courses use air,
combustion products and occasionally other gases.

---

## 11. Tests

`pytest`, one file per `core` module, plus a `test_consistency.py` that checks
relations across modules — that the isentropic and shock routines agree where
they overlap, that a round trip through a conversion returns the input.

Two rules:

- **Every lecture worked example is a test case**, with the exact values printed
  on the lecture page as the expected values.
- **A test asserts a number, not that the code ran.** `assert result is not None`
  is not a test.

The reference implementation carries about 450 lines of tests across eleven
files for roughly 800 lines of `app.py` and its `core`.

---

## 12. README

Fixed sections, in this order:

1. Title and one-paragraph description.
2. **Main modules** — what the app computes.
3. **Two things that are easy to get wrong** — the topic's real traps, in the
   same words the lecture's `mistakes` section uses.
4. Configuration notes (adjustable gas constant, units).
5. **Quick start** and **Manual start**.
6. **Tests** — how to run them and what they cover.
7. **Technical assumptions** — the "what the model does not claim" section.
   This must match the lecture's `model` section. The reference implementation
   reads: calorically perfect gas; two-dimensional, inviscid, piecewise-linear
   surface; attached oblique-shock model unless the solver reports detachment;
   no boundary-layer interaction or wave–wave interaction.
8. Credits and sources.

---

## 13. Landing page and links

Every calculator has a trilingual landing page under `tools/` on the site, and a
link from the root `index.html`. The landing page uses `tools/tool.css` and is
built from: `.tool-hero` with an `.app-preview` mock, a `.module-grid`, a
`.validation-panel` naming the regression cases, a `.lecture-link-grid` pointing
at the lectures the tool serves, and a `.launch-panel` with the Streamlit URL.

The wiring is a loop and all four legs are required:

```text
lecture  →  app        calculator slot + hero button
app      →  portal     SITE_URL in the sidebar
tools/   →  lectures   lecture-link-grid
root     →  tools/     card in #tools
```

---

## 14. Checklist for a new calculator

- [ ] `core/` has no Streamlit import
- [ ] Palette and fonts taken from §3, not re-chosen
- [ ] `config.toml` present **and** `inject_css()` overriding dark mode
- [ ] Portal hero, sidebar with `SITE_URL`, `section_banner` + `metric_grid`
- [ ] Figures routed through the single styling function
- [ ] Equations match the lecture's notation and station numbering
- [ ] Non-convergence and out-of-range inputs reported, never guessed
- [ ] Trilingual labels; equations untranslated
- [ ] All conversions in `units.py`; SI internally
- [ ] Lecture worked examples present as tests with the published values
- [ ] README carries "Technical assumptions" matching the lecture's `model`
- [ ] Landing page under `tools/` and a link from the root page
- [ ] All four legs of the link loop closed

---

## 15. Prompt

> Build the **\<name\>** calculator following `standards/DESIGN-SYSTEM.md`,
> copying `compressible-flow-calculator` where the document says to.
>
> It accompanies Lectures **\<NN–MM\>** of **\<course\>**. Close all four legs of
> the link loop, and make the worked example of Lecture \<NN\> a regression test
> with the exact values already published on the page.
>
> The README's "Technical assumptions" section must state the exclusions in the
> same words as the lecture's `model` section.
