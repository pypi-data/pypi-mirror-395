"""
Threshold-Based Analysis for Evolution Experiments

This script loads per-seed CSV logs for multiple variants,
computes threshold success rates, summary statistics, and
generates publication-quality plots.

Expected CSV format:
- generation
- best_fitness

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

EXPERIMENT_ROOT = Path(".")  # adjust path

VARIANTS = {
    "Baseline": "xor_baseline/results/fitness",
    "Structural": "xor_structural_mutation/results/fitness",
    "Structural + Split": "xor_structural_mutation_split/results/fitness",
    "Structural + HELI": "xor_structural_mutation_heli/results/fitness",
    "Structural + Split + HELI": "xor_structural_mutation_split_heli/results/fitness",
}

THRESHOLDS = [0.10, 0.05, 0.02, 0.01]

COLORS = {
    "Baseline": "#1f77b4",
    "Structural": "#2ca02c",
    "Structural + Split": "#ff7f0e",
    "Structural + HELI": "#d62728",
    "Structural + Split + HELI": "#9467bd",
}

# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def load_seed_files(directory: Path) -> list[pd.DataFrame]:
    """
    Load all CSVs inside a variant subfolder.
    Each CSV represents one seed.
    """
    files = sorted(directory.glob("*.csv"))
    runs = []
    for f in files:
        df = pd.read_csv(f)
        runs.append(df)
    return runs


def extract_final_fitness(runs: list[pd.DataFrame]) -> np.ndarray:
    """
    Extract final best_fitness from each run.
    """
    finals = []
    for df in runs:
        finals.append(df["best_fitness"].iloc[-1])
    return np.array(finals, dtype=float)


# ---------------------------------------------------------
# MAIN ANALYSIS
# ---------------------------------------------------------

results = []

for label, folder in VARIANTS.items():
    variant_path = EXPERIMENT_ROOT / folder
    runs = load_seed_files(variant_path)
    final_values = extract_final_fitness(runs)

    entry = {
        "variant": label,
        "seeds": len(final_values),
        "median": np.median(final_values),
        "q1": np.percentile(final_values, 25),
        "q3": np.percentile(final_values, 75),
    }

    for thr in THRESHOLDS:
        entry[f"pct_<_{thr}"] = np.mean(final_values < thr) * 100.0

    results.append(entry)

summary_df = pd.DataFrame(results)
summary_df.to_csv("threshold_summary.csv", index=False)

print(summary_df)


# ---------------------------------------------------------
# VISUALIZATION: BAR CHART (SUCCESS RATES)
# ---------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 5))

x = np.arange(len(VARIANTS))
width = 0.18

for i, thr in enumerate(THRESHOLDS):
    values = [summary_df.loc[j, f"pct_<_{thr}"] for j in range(len(summary_df))]
    ax.bar(x + i * width, values, width, label=f"< {thr}")

ax.set_xticks(x + width * (len(THRESHOLDS) - 1) / 2)
ax.set_xticklabels(summary_df["variant"], rotation=30, ha="right")
ax.set_ylabel("Success Rate (%)")
ax.set_title("Threshold Success Rates per Variant")
ax.legend(frameon=False)
ax.grid(axis="y", alpha=0.3)

fig.tight_layout()
fig.savefig("threshold_success_rates.png", dpi=300)
plt.close(fig)


# ---------------------------------------------------------
# VISUALIZATION: BOXPLOT OF FINAL FITNESS
# ---------------------------------------------------------

fig, ax = plt.subplots(figsize=(7, 5))

data = []
labels = []

for label, folder in VARIANTS.items():
    runs = load_seed_files(EXPERIMENT_ROOT / folder)
    vals = extract_final_fitness(runs)
    data.append(vals)
    labels.append(label)

ax.boxplot(data, labels=labels)
ax.set_ylabel("Final Fitness (↓)")
ax.set_title("Distribution of Final Fitness per Variant")
ax.grid(alpha=0.3)

fig.tight_layout()
fig.savefig("final_fitness_boxplot.png", dpi=300)
plt.close(fig)
