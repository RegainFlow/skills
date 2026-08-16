# RegainFlow report design spec

Tokens and conventions sampled from the reference report ("Surviving the AI Hype Cycle", WeasyPrint 69, letter size). `assets/report.css` implements all of this; read this file when building figures or when you need to deviate from the template.

## Design tokens

| Token | Value | Used for |
|---|---|---|
| Ink | `#050912` | cover background, headings, synthesis box |
| Accent | `#2E4FE0` | rules, blue bars, links, dash bullets, card top borders |
| Accent soft | `#7999F4` | cover kicker, figure annotations |
| Muted | `#414958` | kickers, table headers |
| Faint | `#9EA1A8` | footers, source labels, TOC numbers |
| Panel | `#EFF2F7` | figure panels, stat cards |
| Panel fill | `#E3E8F5` | area fill under chart curves |
| Hairline | `#DCE1EC` | table and TOC row rules |

## Typography

- **Body:** Liberation Serif, ~10.5pt, line-height 1.55. Section titles are Liberation Serif *regular* (not bold) at 23–24pt — the lightness is part of the look.
- **Labels/kickers/footers:** DejaVu Sans Mono, bold, 6.5–7.5pt, UPPERCASE, letter-spacing 0.2–0.32em. Every structural label (SECTION 01, FIGURE 1 / ..., sources, running footer) uses this voice.
- **Tables and figure text:** DejaVu Sans, 8pt range.
- All three fonts ship with Ubuntu; no font installation needed.

## Page anatomy

- Letter, ~1in margins. Running footer via `@page`: brand name bottom-left, `REPORT TITLE  N` bottom-right, both mono/letterspaced/faint. The cover page suppresses the footer (`page: cover`).
- Every numbered section starts on a new page with: short blue rule (26×3.5pt) → mono kicker `SECTION NN` → serif title.
- Standard back matter order: ... → Sources & further reading (numbered as the last section) → About the authors (unnumbered kicker).

## Figures (matplotlib conventions)

Figures in the reference report are matplotlib renders placed inside the light panel. To match:

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK, ACCENT, SOFT = "#050912", "#2E4FE0", "#7999F4"
MUTED, FAINT, FILL, PANEL = "#414958", "#9EA1A8", "#E3E8F5", "#EFF2F7"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8,
    "figure.facecolor": PANEL,   # blends into the .figure panel
    "axes.facecolor": PANEL,
    "svg.fonttype": "none",      # keep text as text in SVG
})
fig, ax = plt.subplots(figsize=(7.2, 3.8))
# curves: ink line ~2pt; milestone markers: white-filled circles with ink edge
# area fill under the curve: FILL color
# stage/point labels: DejaVu Sans 6.5-7pt in INK or MUTED
# research annotations: 6pt italic in SOFT or MUTED, thin leader lines
# axis labels ("TIME / MATURITY", "EXCITEMENT / CONFIDENCE"):
#   monospace-feel = DejaVu Sans Mono 6pt, letterspaced via "T I M E"
for s in ax.spines.values(): s.set_visible(False)
ax.set_xticks([]); ax.set_yticks([])
fig.savefig("figures/figure-1.svg", bbox_inches="tight")
```

Figure grammar from the reference:

- **Sentiment-curve style:** one smooth curve, open-circle milestones, each milestone labeled with a bold-ish name plus an italic quote beneath; one or two research annotations in small italic connected by hairlines.
- **Trajectory-comparison style:** solid accent line for the recommended path, gray dashed for defaults, red dashed for the failure path; right-edge labels colored to match; a dotted horizontal threshold line labeled in tiny caps.
- Keep axes minimal: no ticks, no spines, only conceptual axis captions.
- Save as SVG (`svg.fonttype: none`) so text stays crisp in the PDF.

## Voice details worth copying

- Figure captions sit *below* the panel with a 3pt blue left bar and grayish-blue serif text, ~9.3pt.
- Stat cards: big serif number → small gray description → tiny mono source.
- The synthesis box is the ink color with an accent-soft kicker (`REGAINFLOW SYNTHESIS`) and light serif prose.
- Checklists use en-dash bullets (`–`) colored accent, with a bold serif lead-in phrase per item.
- Stage/step items in prose: `**Stage N: Name.**` then an italic blue characteristic quote, then the body.

## Bar/column chart convention

For quantitative comparisons (survey shares, before/after):

- Bars: `ACCENT` for the highlighted series, `FILL` (`#E3E8F5`) for context series; no borders.
- Value labels above/right of each bar in DejaVu Sans 7pt `INK`; no gridlines, no y-axis.
- Category labels in DejaVu Sans 7pt `MUTED`.
- Horizontal bars for ranked lists (longest on top); vertical columns for time series.
- Same panel-blending rcParams as the curve convention (facecolor `PANEL`, `svg.fonttype: none`).
