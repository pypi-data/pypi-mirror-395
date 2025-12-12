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
    """Load all CSVs inside a variant subfolder."""
    files = sorted(directory.glob("*.csv"))
    return [pd.read_csv(f) for f in files]


def extract_final_fitness(runs: list[pd.DataFrame]) -> np.ndarray:
    """Extract final best_fitness value from each run."""
    return np.array([df["best_fitness"].iloc[-1] for df in runs], dtype=float)


# ---------------------------------------------------------
# MAIN ANALYSIS
# ---------------------------------------------------------

records = []

for label, folder in VARIANTS.items():
    runs = load_seed_files(EXPERIMENT_ROOT / folder)
    finals = extract_final_fitness(runs)

    entry = {
        "variant": label,
        "seeds": len(finals),
        "median": np.median(finals),
        "q1": np.percentile(finals, 25),
        "q3": np.percentile(finals, 75),
    }

    for thr in THRESHOLDS:
        entry[f"pct_<_{thr}"] = np.mean(finals < thr) * 100.0

    records.append(entry)

summary_df = pd.DataFrame(records)
summary_df.to_csv("threshold_summary.csv", index=False)
print(summary_df)


# ---------------------------------------------------------
# VISUALIZATION: BAR CHART (SUCCESS RATES)
# ---------------------------------------------------------

fig, ax = plt.subplots(figsize=(9, 5))

x = np.arange(len(VARIANTS))
width = 0.18

for i, thr in enumerate(THRESHOLDS):
    values = [summary_df.loc[j, f"pct_<_{thr}"] for j in range(len(summary_df))]
    # use colors in the same order as variants
    color_list = [COLORS[label] for label in summary_df["variant"]]
    ax.bar(
        x + i * width,
        values,
        width,
        label=f"< {thr}",
        color=color_list,
        edgecolor="black",
        linewidth=0.7,
    )

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
colors_box = []

for label, folder in VARIANTS.items():
    runs = load_seed_files(EXPERIMENT_ROOT / folder)
    values = extract_final_fitness(runs)
    data.append(values)
    labels.append(label)
    colors_box.append(COLORS[label])

# Custom colored boxplot
bp = ax.boxplot(
    data,
    labels=labels,
    patch_artist=True,
)

for patch, color in zip(bp["boxes"], colors_box):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)
    patch.set_edgecolor("black")
    patch.set_linewidth(0.8)

ax.set_ylabel("Final Fitness (↓)")
ax.set_title("Distribution of Final Fitness per Variant")
ax.grid(alpha=0.3)

fig.tight_layout()
fig.savefig("final_fitness_boxplot.png", dpi=300)
plt.close(fig)
