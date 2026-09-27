# Quarto Thesis Template for FU Berlin (Wiwiss Department)

A robust, publication-ready [Quarto](https://quarto.org/) template designed for academic theses (Bachelor's, Master's, Seminar Papers, or Dissertations) adhering to the formal standards of Freie Universität Berlin and common economics/social sciences guidelines.

---

## Project Structure

```text
thesis_quarto/
├── _quarto.yml             # Quarto configuration (default PDF build, bibliography)
├── main.qmd                # Master document (geometry, packages, title page, TOC, declaration)
├── environment.yml         # Conda / Mamba environment definition
├── requirements.txt        # Pip dependencies (version-pinned)
├── references.bib          # BibTeX bibliography
├── _output/                # Build output (compiled main.pdf)
├── Chapters/               # Modular manuscript chapters
│   ├── abstract.qmd
│   ├── 1_introduction.qmd
│   ├── 2_literature_review.qmd
│   ├── 3_methodology.qmd
│   ├── 4_results.qmd
│   ├── 5_discussion.qmd
│   ├── 6_conclusion.qmd
│   └── appendix.qmd
├── code/                   # Decoupled empirical pipeline scripts
│   └── main.py             # Data processing, estimation, and vector figure generator
├── data/                   # Raw or processed empirical datasets
│   └── simulated_dgp_data.csv
├── plots/                  # Generated publication-ready vector figures (*.pdf)
│   └── fig1_regression_fit.pdf
├── word_counter/           # Academic word counter tool
│   └── count_words.py
└── submission/             # Standalone replication package template
    └── README.md
```

---

## Quickstart & Build Instructions

### 1. Environment Setup

#### Option A: Conda / Mamba (Recommended)
```bash
conda env create -f environment.yml
conda activate thesis_env
```

#### Option B: Standard Python (venv / pip)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Run the Empirical Pipeline (Optional)
Generate all datasets and vector figures prior to rendering:
```powershell
python code/main.py
```

### 3. Render the Thesis PDF
```powershell
quarto render main.qmd
```
The output PDF is saved to `_output/main.pdf`.

---

## Core Features & Best Practices

### 1. Decoupled Empirical Workflow (Pipeline & Manuscript)
Rather than executing resource-intensive computations and plotting inside `.qmd` code chunks during the build, this template recommends a decoupled architecture:
- **`code/main.py`** processes data and exports figures as vector graphics (`.pdf`) using a standardized academic theme.
- **`Chapters/*.qmd`** embeds the vector figures directly:
  ```markdown
  ![Linear regression fit on simulated DGP data](plots/fig1_regression_fit.pdf){#fig-regression-fit width=85%}

  \figurenote{Fitted OLS line on simulated data. Generated via \texttt{code/main.py}.}
  ```
- **Benefits:** Instant Quarto compilation (`< 5s`), no kernel/memory crashes with large datasets, and crisp, infinitely scalable vector figures in print quality.

### 2. Strict Float & Table Placement
Figures and tables are configured with `fig-pos: "H"` and `tbl-pos: "H"`. Combined with `\usepackage[section]{placeins}` and `\restylefloat{figure}`, floats remain strictly within their respective sections and will not wander arbitrarily across subsequent pages.

### 3. Unified Figure & Table Notes
Use the robust `\figurenote` and `\tablenote` macros directly beneath tables and figures without causing float warnings or spacing glitches:
```latex
\figurenote{Source: Federal Statistical Office (2024). Standard errors in parentheses.}
\tablenote{Significance levels: * p < 0.10, ** p < 0.05, *** p < 0.01.}
```

### 4. Wide Tables & Landscape Support
For wide regression tables, use the included helper command:
```latex
\scaleTable{0.85}{%
  \begin{tabular}{lcccc}
    \toprule
    Variable & Model (1) & Model (2) & Model (3) & Model (4) \\
    \midrule
    ...
    \bottomrule
  \end{tabular}
}
```

### 5. 3-Phase Page Numbering & Clean Appendix in TOC
- **Front Matter (Title, TOC, Lists, Abstract):** Suppressed or Roman lowercase (`roman`).
- **Main Body (Chapters 1–6):** Arabic numerals (`arabic`) starting at 1 with `fancyhdr` footers.
- **References:** Numbered in uppercase Roman (`Roman`) and listed in the TOC via `\addcontentsline{toc}{section}{References}` with its Roman page number visible and clickable.
- **Appendix:** Page numbering and footers suppressed (`\pagenumbering{gobble}` and `\pagestyle{empty}`). A single, clean "Appendix" entry is added to the Table of Contents via `\addcontentsline{toc}{section}{Appendix}` which jumps directly to the appendix section without displaying a page number. Sub-appendices (`## Appendix A {.unnumbered .unlisted}`) do not clutter the TOC.

### 6. Dynamic Date for Declaration of Independent Work
The declaration (*Eigenständigkeitserklärung*) automatically inserts the current German date format (`DD.MM.YYYY`) upon compilation:
```latex
Berlin, \ifnum\day<10 0\fi\number\day.\ifnum\month<10 0\fi\number\month.\number\year
```

### 7. Submission Link Coloring
In `main.qmd`, switch from blue hyperlinks (for screen reading) to monochrome black for physical printing / final submission:
```latex
\newif\ifsubmission
\submissiontrue   % true = all links black; false = colored links
```

---

## Academic Word Counter (`word_counter/`)

University examination offices enforce exact word limits for prose text (excluding LaTeX markup, math, formulas, code, and comments).

Run the custom word counter:
```bash
python word_counter/count_words.py
# Or specify a custom target word limit:
python word_counter/count_words.py 6000
```

The script reports both `RAW` tokens and filtered `Fließtext` (prose) words per chapter and checks against the configured target limit.

---

## Standalone Replication Package (`submission/`)

Many university chairs and journals require a self-contained replication archive alongside the PDF. The template provides a ready-to-use replication template under `submission/` containing instructions for setting up environments and reproducing empirical results.
