---
name: regainflow-report
description: Turn drafted content into a styled RegainFlow insight-report PDF with the house design — dark cover page, table of contents, numbered sections, figure panels, stat cards, sources page, and authors page. Use whenever the user asks for a report, insight report, whitepaper, or branded PDF from drafted or researched content, or says "make it look like our report" / "the hype cycle report style". Always run the de-ai-ify skill on the content first.
---

# RegainFlow insight report

Produce a letter-size PDF in the RegainFlow house style: near-black cover with blue accents, Liberation Serif body, monospace uppercase labels, light-gray figure panels, and a fixed front/back-matter structure. The reference implementation is "Surviving the AI Hype Cycle"; this skill makes that design replicable.

## Non-negotiable brand assets

These ship with the skill and must be reproduced exactly in every report — never regenerate, redraw, substitute, or paraphrase them:

- **Logo:** `assets/logo.png` is the canonical RF mark (white letterform, blue offset). Use it on the cover via `<img>`; never render a text-based "RF" substitute.
- **Cofounder photos:** `assets/author-ramirez.png` (Leonardo J. Ramirez, Co-founder & CEO) and `assets/author-baltus.png` (William J. Baltus, Co-founder & CTO). Never swap, crop out, or replace with placeholders.
- **Authors page:** names, roles, credential lines, and both bio paragraphs per author are fixed brand copy, baked verbatim into `assets/template.html`. Copy that block unchanged. The de-ai-ify pass never touches this copy.

If a report adds a guest author, append them after the two founders using the same component; the founders' entries stay verbatim.

## Pipeline (in order)

### 1. De-AI-ify first

Before any layout work, run the **de-ai-ify** skill on the draft content (skip only if it was already cleaned in this conversation). Show the user the cleaned markdown preview and the What changed notes, and get a go-ahead before building the PDF. Clean prose in, then styling — never the reverse.

### 2. Agree on the outline

Propose and confirm with the user before building:

- **Section plan** — numbered sections with working titles. The fixed skeleton is: Cover → Contents ("In this report") → Executive brief → numbered sections 01..N → Sources & further reading (last numbered section) → About the authors. Don't drop the contents, sources, or authors pages unless the user says so.
- **Figures** — which sections get one, what each shows, and what style (see figure grammar in `references/design-spec.md`). Describe each proposed figure in a sentence and confirm.
- **Stat cards** — the executive brief carries 3–4 headline numbers with sources when the content has them.
- **Authors** — the authors page is canonical (see Non-negotiable brand assets below); confirm only whether both founders appear or a guest author is added.
- **Cover copy** — kicker line, title (breaks well over two lines), 2–3 sentence standfirst, tagline.

Keep this step brief: one message with the proposed outline, then adjust.

### 3. Build

1. Create a working dir (e.g. `/home/claude/report/`), copy in everything from `assets/` (report.css, template.html, logo.png, and both author photos — the HTML references them by relative path).
2. Generate figures as SVG into `figures/` using the matplotlib conventions in `references/design-spec.md`. Figures must visually blend with the `#EFF2F7` panel.
3. Write the report HTML by filling the template. `template.html` contains every component once (cover, TOC, stat cards, figure panel + caption, data table, dashed checklist, synthesis box, sources, authors); duplicate what you need, delete what you don't. Keep these invariants:
   - Set the two hidden strings at the top (`brand-string`, `title-string`) — they drive the running footer.
   - Section pages use: blue rule → `SECTION NN` kicker → serif title.
   - Fill TOC page numbers **after** a first render (see step 4), since content length determines them.
4. Render: `python <skill>/scripts/build_pdf.py report.html report.pdf` (install WeasyPrint with `pip install weasyprint --break-system-packages` if missing). Render once, note the actual page number of each section from the output, update the TOC rows, render again.
5. **Visually check** the PDF before presenting: rasterize a few pages (`pdftoppm -png -r 60`) and view them. Look for: overflowing stat cards, orphaned section headings, figures spilling past the panel, TOC numbers that don't match. Fix and re-render.

### 4. Deliver

Copy the final PDF to `/mnt/user-data/outputs/` and present it with `present_files`. Offer the intermediate markdown or HTML only if the user asks.

## Component library

`assets/template.html` is a gallery — each component appears once. Pick per content, don't use everything in every report:

| Component | Class | Use when |
|---|---|---|
| Stat cards | `.stat-grid` | Executive brief has 3–4 headline numbers with sources |
| Figure panel + caption | `.figure` / `.figure-caption` | Any chart or diagram; caption credits the data |
| Data table | `table.data` | Structured comparisons (frameworks, mappings) |
| Dashed checklist | `ul.dash` | Actionable recommendations with bold lead-ins |
| Synthesis box | `.synthesis` | Closing a major argument; max 1–2 per report |
| Pull quote | `.pullquote` | One striking line worth isolating, with attribution |
| Key takeaways | `.takeaways` | 3–5 numbered takeaways at brief or section end |
| Process strip | `.process-strip` | A named path/framework as a horizontal chain; `dim` de-emphasizes |
| Side note | `.note` | Methodology, definitions, scope caveats (use `.note.accent` for emphasis) |
| Do / don't | `.duo` | Practices vs anti-patterns, two columns |
| Numbered recs | `.numlist` | 3–6 major recommendations with big mono numbers |

Restraint reads as expertise: at most 1–2 special components per page, plenty of body prose between them. Never stack two panels back-to-back without prose.

## Style rules the CSS doesn't enforce

- Section titles are short (2–5 words) and sentence case ("The sentiment curve", not "THE SENTIMENT CURVE" — the mono kicker carries the caps).
- Executive brief opens with the thesis in two sentences, then the stat cards, then a bold one-line takeaway.
- Body prose, not bullet spam: the house style uses paragraphs with bold lead-ins (`**Stage 1: Confusion.**`) and reserves the dashed checklist (`ul.dash`) for genuinely actionable recommendation lists.
- Every figure gets a caption below the panel crediting the data or noting the figure is generated.
- Sources page: one line per source with what it supports in parentheses, ending with `· domain.com` in the mono link style.
- The synthesis box appears at most once or twice per report, at the end of a major argument.
- Quotes inside stage items are italic + accent blue (`.quote-lead`).

## Reference files

- `assets/report.css` — full stylesheet, design tokens in `:root`.
- `assets/logo.png`, `assets/author-ramirez.png`, `assets/author-baltus.png` — canonical brand images (see Non-negotiable brand assets).
- `assets/template.html` — component gallery; copy and fill.
- `references/design-spec.md` — read before making figures or deviating from the template; contains color tokens, typography table, and matplotlib figure conventions.
- `scripts/build_pdf.py` — HTML → PDF via WeasyPrint.
