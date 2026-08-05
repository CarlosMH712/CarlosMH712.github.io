# Academic Portal v10

Version 10 reconstructs the missing nozzle-content release from the public v7 portal,
the local `UnidadIV.tex` course chapter, and the published Nozzle Calculator.

## Reconstructed academic content

- Added Lecture 07: quasi-one-dimensional flow, conservation laws, area–velocity and
  area–Mach relations, critical properties, mass flow, choking, and a dimensional example.
- Added Lecture 08: convergent and convergent–divergent nozzle operation, mathematical
  branch selection, ideal design, exit-state calculation, and the two roots for
  `Ae/At = 2`.
- Added Lecture 09: the eight-regime back-pressure sequence, internal normal shocks,
  downstream critical area, shock-location procedure, external jet adjustment, thrust,
  characteristic velocity, viscous limitations, and regression cases.
- Kept diffusers and supersonic wind tunnels as explicitly identified future lectures so
  the nozzle sequence remains focused.

## Nozzle Calculator integration

- Added the live application link: https://nozzle-calculator.streamlit.app/
- Added `tools/nozzle-calculator.html` with purpose, operating cases, inputs, outputs,
  assumptions, limitations, regression values, references, and links to Lectures 07–09.
- Added direct launch and overview links on the portal home page, the Aerodynamics II
  index, and Lectures 07–09.
- Documented the six selectable application cases: Custom, Subsonic, Internal shock,
  Overexpanded, Correct expansion, and Underexpanded.
- Documented the axial plots, operating map, detailed shock location, result table, and
  downloadable CSV profile observed in the public application.

## Multilingual and navigation work

- Added matched English, Spanish, and German content for every new lecture section,
  equation, example, validation table, calculator description, and reference block.
- Rebuilt the Aerodynamics II index as three equivalent nine-card collections.
- Localized the study path and calculator-selection panels.
- Linked Lecture 06 → Lecture 07 → Lecture 08 → Lecture 09 → course index.
- Added localized labels for the nozzle calculator and previous/next lecture controls.

## Recovered technical corrections

- Reoriented Prandtl–Meyer characteristics so the fan propagates downstream from the
  convex corner and labeled its head and tail with `mu1` and `mu2`.
- Reoriented expansion characteristics in the sequential and diamond-airfoil diagrams
  and added the trailing-edge closing compression waves.
- Replaced the ambiguous panel-angle difference with `delta_i = phi_i - theta_i`.
- Replaced the state-vector angle with local flow direction:
  `S_i = (M_i, p_i, T_i, rho_i, p0_i, theta_i)`.
- Defined shock and expansion solvers in terms of the local turn magnitude `|delta_i|`.

## Visual and delivery updates

- Preserved the existing navy, aerodynamic-blue, orange, serif-heading, and card-based
  identity.
- Added responsive nozzle geometry, operating-regime, calculator, and validation layouts.
- Updated CSS and JavaScript cache-busting query strings to version 10.
- Added `docs/VALIDATION-v10.txt` with the final automated and numerical checks.

## Deployment

Upload the contents of this folder to the root of
`CarlosMH712/CarlosMH712.github.io`. The folder is a static GitHub Pages site; no build
step is required.

