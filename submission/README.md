# Standalone Replication Package

This folder demonstrates the structure of a self-contained replication archive as required by many academic journals and university departments.

---

## Directory Structure

- **`code/`**: Python pipeline scripts executing data cleaning, statistical estimation, and plot generation.
- **`data/`**: Raw or processed empirical datasets (`.csv`, `.parquet`, etc.).
- **`plots/`**: Generated publication-ready vector figures (`.pdf`).
- **`requirements.txt`**: Pip dependency specifications.
- **`environment.yml`**: Conda / Mamba environment definition.

---

## Quickstart

### Option A: Conda / Mamba (Recommended)

```bash
# 1. Create and activate environment
conda env create -f environment.yml
conda activate thesis_env

# 2. Execute empirical pipeline
python code/main.py
```

### Option B: Python Virtual Environment (venv)

```bash
# 1. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Execute empirical pipeline
python code/main.py
```
