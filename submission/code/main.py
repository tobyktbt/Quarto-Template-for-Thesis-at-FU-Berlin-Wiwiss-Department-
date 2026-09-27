"""
Empirical pipeline and publication-ready figure generator for the Quarto Thesis Template.

Executes data generation / processing, statistical analysis, and exports vector graphics (PDF)
to plots/ with standardized academic typography.

Usage:
    python code/main.py
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")  # Headless rendering
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent if SCRIPT_DIR.name == "code" else SCRIPT_DIR
DATA_DIR = BASE_DIR / "data"
PLOTS_DIR = BASE_DIR / "plots"

DATA_DIR.mkdir(parents=True, exist_ok=True)
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# ── Academic Plot Theme ───────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#FFFFFF",
    "axes.facecolor": "#FFFFFF",
    "axes.edgecolor": "#888888",
    "axes.labelcolor": "#000000",
    "axes.titlecolor": "#000000",
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "text.color": "#000000",
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "font.family": "serif",
    "lines.linewidth": 1.5,
    "grid.color": "#E5E5E5",
    "grid.linestyle": "--",
    "grid.alpha": 0.7,
})


def run_pipeline():
    print("[1/3] Simulating Data Generating Process (DGP)...")
    np.random.seed(42)
    n = 120
    beta_0 = 2.0
    beta_1 = 1.5
    sigma = 1.0

    x = np.random.normal(0, 1, n)
    epsilon = np.random.normal(0, sigma, n)
    y = beta_0 + beta_1 * x + epsilon

    df = pd.DataFrame({"x": x, "y": y})
    data_csv_path = DATA_DIR / "simulated_dgp_data.csv"
    df.to_csv(data_csv_path, index=False)
    print(f"      Saved raw dataset to: {data_csv_path}")

    print("[2/3] Estimating OLS Regression...")
    X = np.column_stack([np.ones(n), x])
    k = X.shape[1]
    beta_hat = np.linalg.inv(X.T @ X) @ (X.T @ y)
    y_hat = X @ beta_hat
    residuals = y - y_hat
    sigma2_hat = (residuals @ residuals) / (n - k)
    vcov_hat = sigma2_hat * np.linalg.inv(X.T @ X)
    se_beta = np.sqrt(np.diag(vcov_hat))
    r2 = 1 - (residuals @ residuals) / np.sum((y - y.mean()) ** 2)

    print(f"      Intercept : {beta_hat[0]:.4f} (SE: {se_beta[0]:.4f})")
    print(f"      Slope (x) : {beta_hat[1]:.4f} (SE: {se_beta[1]:.4f})")
    print(f"      R-squared : {r2:.4f}")

    print("[3/3] Generating Vector PDF Plot...")
    fig, ax = plt.subplots(figsize=(6.5, 4.0), dpi=300)
    ax.scatter(x, y, alpha=0.65, color="#1f77b4", edgecolors="none", s=32, label="Simulated observations ($n=120$)")

    order = np.argsort(x)
    ax.plot(x[order], y_hat[order], color="#d62728", linewidth=2.0, label=f"Fitted OLS line ($\\hat{{\\beta}}_1 = {beta_hat[1]:.2f}$)")

    ax.set_xlabel("Independent Variable ($x$)")
    ax.set_ylabel("Dependent Variable ($y$)")
    ax.set_title("Linear Regression Fit on Simulated DGP Data")
    ax.grid(True)
    ax.legend(frameon=True, facecolor="#FAFAFA", edgecolor="#CCCCCC", fontsize=9)
    plt.tight_layout()

    out_pdf = PLOTS_DIR / "fig1_regression_fit.pdf"
    plt.savefig(out_pdf, format="pdf", bbox_inches="tight")
    plt.close()
    print(f"      Saved vector graphic to: {out_pdf}")
    print("\n[OK] Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
