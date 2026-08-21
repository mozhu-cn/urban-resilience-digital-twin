# Paper: submission manuscript

## Files

| File | Description |
|---|---|
| `manuscript.tex` | Full submission manuscript (Elsevier `elsarticle` format) |
| `references.bib` | References (all DOIs verified against Crossref, 2026-07) |
| `highlights.txt` | Elsevier Highlights (5 bullet points) |
| `figures/` | Figures for the manuscript (see below) |
| `docx_archive/` | Original draft .docx/.txt sources (archived) |

## Compilation

Requires a LaTeX distribution (TeX Live / MiKTeX) with the Elsevier class.

```bash
cd paper
pdflatex manuscript
bibtex manuscript
pdflatex manuscript
pdflatex manuscript
```

Or use an online service (Overleaf): upload `manuscript.tex`,
`references.bib` and `figures/`, select the `elsarticle` template.

### Before submission, complete

- [x] Author names (Zheyu Huang, Yujia Huang) and affiliation (Independent Researcher, China)
- [x] Target journal: International Journal of Disaster Risk Reduction (IJDRR)
- [x] Funding: none (no-grant statement in Acknowledgements)
- [x] Data availability statement (repository link included)
- [x] Highlights compliant with IJDRR (<= 85 characters each)
- [ ] Upload to Elsevier Editorial System (EES) / Editorial Manager
- [ ] Results tables/figures regenerated from `results/` (see below)

## Figures

The figures are produced by the experiment pipeline:

```bash
python run.py --experiments   # from the repository root
```

Outputs land in `results/`:

| Figure in manuscript | Source file | Content |
|---|---|---|
| Fig. 1 | `fig1_study_area.png` | Terrain, road network, infrastructure layout |
| Fig. 2 | `fig2_flood_evolution.png` | Flood evolution snapshots (3 stages) |
| Fig. 3 | `fig3_resilience_curves.png` | Resilience trajectories vs baselines |
| Fig. 4 | `fig4_sensitivity.png` | One-at-a-time sensitivity analysis |

Copy the generated PNGs into `paper/figures/` (or symlink) before compiling.

## Draft archive

`docx_archive/` contains the extracted plain-text versions of every
historical draft (Abstract, Highlights, Outlines, section-wise SCI versions,
previous full manuscripts). They are kept for provenance; the consolidated
manuscript supersedes them.

## Integration notes

The manuscript was assembled from the following sources:

- **Abstract**: latest `Abstract.docx` (reorganized, adds sensitivity
  analysis statement).
- **Introduction**: merged from `GPT.docx`/V2 introduction and the revised
  SCI introduction (`gpt2.docx`), with references.
- **Related Work**: new Section 2 from `gpt2.docx` (SCI submission version),
  with references.
- **Methodology**: complete equation set from V2 (`Urban_Digital_Twin_
  Resilience_Submission_V2.docx`), terminology aligned with
  `Revised_Digital_Twin_Paper_Modification_V1.docx`
  ("terrain-informed cellular flood propagation model").
- **Case study & experiments**: V2 + `Section4_..._SCI_Version.docx`
  (scenarios S1–S4, evaluation metrics).
- **Results**: V2 structure, numbers replaced by outputs of the actual
  simulation runs (`results/`).
- **Discussion/Conclusion**: V2 + `Discussion_Conclusion_section.docx` +
  `Section7_..._SCI_Version.docx`.
