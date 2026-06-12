# Academic Paper Writing — IEEE / SCI Format

Strict-format mode for academic paper writing. Use this when drafting or revising a paper targeting an IEEE conference/journal or an SCI-indexed journal. The format rules below are hard constraints, not suggestions.

> For a full paper-writing skill stack (research-paper-writing, proofread, bib-search, latex-paper, paper-audit + IEEEtran templates), see the companion repo [minimal-paper-skills](https://github.com/DNMCJH/minimal-paper-skills). This command is the lightweight in-kit entry point; install that stack for the complete workflow.

---

## Format Selection (choose first)

Ask the target venue before writing — format rules diverge:

| Target | Template | Columns | Reference style |
|--------|----------|---------|-----------------|
| IEEE conference | `IEEEtran` conference mode | Two-column | IEEE numbered `[1]` |
| IEEE journal (Trans/Access) | `IEEEtran` journal mode | Two-column (Access: one) | IEEE numbered |
| SCI journal (Elsevier) | `elsarticle` | Per journal | Numbered or author-year |
| SCI journal (Springer) | `sn-jnl` | Per journal | Per journal |

If unsure, default to **IEEEtran conference two-column** and confirm.

---

## IEEE Hard Rules

- **Document class**: `\documentclass[conference]{IEEEtran}` (or `[journal]`)
- **No custom margins/spacing** — IEEEtran sets them; never override `\geometry` or `\baselineskip`
- **Title**: title case, no trailing period
- **Authors**: `\author{\IEEEauthorblockN{...}\IEEEauthorblockA{...}}`
- **Abstract**: `\begin{abstract}...\end{abstract}`, single paragraph, 150–250 words, no citations, no math macros
- **Keywords**: `\begin{IEEEkeywords}...\end{IEEEkeywords}`
- **Sections**: `\section`, `\subsection` — IEEE auto-numbers (I, II, A, B); never hardcode numbers
- **Figures**: `\begin{figure}[!t]`, caption **below**, `Fig. 1.` style; reference as `Fig.~\ref{}`
- **Tables**: caption **above**, `TABLE I` (Roman numeral, all-caps label); use `booktabs` (`\toprule/\midrule/\bottomrule`), no vertical rules
- **Equations**: `equation` env, numbered; reference as `(\ref{})` not "equation X"
- **Citations**: `\cite{}`, numbered IEEE style (`IEEEtran.bst`); cite as `[1]`, `[2]–[5]`; never "author et al. [1] said"
- **Units**: SI units, `siunitx` recommended; space between number and unit (`5\,GHz`)

---

## SCI Journal Notes

- Always download the **target journal's own template** — generic SCI format does not exist; each publisher differs
- Structured abstract may be required (Background/Methods/Results/Conclusions) — check guide for authors
- Author-year (`natbib`, `\citep`/`\citet`) common in Elsevier; confirm per journal
- Highlights / graphical abstract often mandatory — ask if the journal requires them
- Declarations (funding, conflict of interest, data availability) usually required before submission

---

## Structure (IMRaD)

1. **Abstract** — problem, gap, approach, key quantitative result, significance (1 sentence each)
2. **Introduction** — broad context → specific gap → contributions (bulleted `\itemize` of 3–4 contributions)
3. **Related Work** — group by theme, end each with how your work differs
4. **Method** — reproducible: notation table, equations, algorithm pseudocode (`algorithm2e`)
5. **Experiments** — datasets, baselines, metrics, implementation details, ablations
6. **Results & Discussion** — tables/figures with significance, honest limitations
7. **Conclusion** — restate contribution + result, future work (no new claims)
8. **References** — `.bib` via BibTeX, consistent and complete

---

## Workflow (6 Steps)

1. **Venue + template** — Confirm target, fetch the correct template, set up the LaTeX skeleton
2. **Outline** — Section tree + contribution bullets + which experiments support which claim
3. **Draft method/experiments first** — the verifiable core; intro/abstract last
4. **Figures/tables** — vector (PDF/EPS) figures, `booktabs` tables, captions self-contained
5. **Proofread pass** — tense consistency, citation completeness, notation uniformity, no orphan refs
6. **Pre-submission audit** — page limit, anonymization (if double-blind), required declarations, `\ref` all resolve, BibTeX compiles clean

---

## Quick Reference: What NOT to Do

| Bad | Good |
|-----|------|
| Override IEEEtran margins/spacing | Leave class defaults untouched |
| Hardcoded section numbers ("3. Method") | `\section{Method}` (auto-numbered) |
| Vertical rules in tables | `booktabs`, horizontal rules only |
| Figure caption above figure | Caption below figure (IEEE) |
| Table caption below table | Caption above table (IEEE) |
| "Equation 3 shows..." | "(3) shows..." / `(\ref{eq:x})` |
| Citations in abstract | No citations in abstract |
| Manual `[1]` reference list | BibTeX + `IEEEtran.bst` |
| Generic "SCI format" assumed | Download the specific journal's template |
| Bitmap (PNG) figures of plots | Vector PDF/EPS |
