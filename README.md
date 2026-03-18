# Quarto Thesis Template

## Structure

```
thesis_quarto/
├── _quarto.yml
├── main.qmd
├── requirements.txt
├── references.bib
├── _output/
└── Chapters/
    ├── abstract.qmd
    ├── 1_introduction.qmd
    ├── 2_literature_review.qmd
    ├── 3_methodology.qmd
    ├── 4_results.qmd
    ├── 5_discussion.qmd
    ├── 6_conclusion.qmd
    └── appendix.qmd
```

## Build

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\Activate.ps1
quarto render main.qmd
```

The generated PDF is written to `_output/main.pdf`.

## Customize front matter

Edit `main.qmd` to set:
- title and subtitle
- author and date
- title page fields (supervisor, semester, student details, deadline)
- declaration text

## Citations

Use citation keys from `references.bib`:
- parenthetical: `[@key]`
- narrative: `@key`

The references section is rendered automatically.

## Hyperlink colors for submission

In `main.qmd`, find these lines in the header block:

```tex
\newif\ifsubmission
\submissionfalse
```

Switch to:

```tex
\submissiontrue
```

When `\submissiontrue` is set, all link colors are black in the PDF.
