"""
Comprehensive threshold analysis for XOR experiments.

Generates:
1. Threshold summary CSV
2. Clustered barplot (thresholds per variant)
3. Heatmap of success rates
4. Horizontal barplot per variant

Required CSV format inside each folder:
- generation
- best_fitness

Author: <you>
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

EXPERIMENT_ROOT = Path(".")

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
    """Extract final best_fitness from each run."""
    return np.array([df["best_fitness"].iloc[-1] for df in runs], dtype=float)


# ---------------------------------------------------------
# MAIN ANALYSIS
# ---------------------------------------------------------

records = []

for label, folder in VARIANTS.items():
    path = EXPERIMENT_ROOT / folder
    runs = load_seed_files(path)
    finals = extract_final_fitness(runs)

    entry = {
        "variant": label,
        "seeds": len(finals),
        "median": np.median(finals),
        "q1": np.percentile(finals, 25),
        "q3": np.percentile(finals, 75),
    }

    for thr in THRESHOLDS:
        entry[f"pct_<_ {thr}"] = np.mean(finals < thr) * 100.0

    records.append(entry)

summary_df = pd.DataFrame(records)
summary_df.to_csv("threshold_summary.csv", index=False)
print(summary_df)


# ---------------------------------------------------------
# PLOT 1: CLUSTERED BARPLOT
# ---------------------------------------------------------

threshold_colors = {
    0.10: "#a6cee3",
    0.05: "#1f78b4",
    0.02: "#b2df8a",
    0.01: "#33a02c",
}

x = np.arange(len(VARIANTS))
width = 0.18

fig, ax = plt.subplots(figsize=(10, 5))

for i, thr in enumerate(THRESHOLDS):
    values = [summary_df.loc[j, f"pct_<_ {thr}"] for j in range(len(summary_df))]
    ax.bar(
        x + i * width,
        values,
        width,
        label=f"< {thr}",
        color=threshold_colors[thr],
        edgecolor="black",
        linewidth=0.7,
    )

ax.set_xticks(x + width * 1.5)
ax.set_xticklabels(summary_df["variant"], rotation=25, ha="right")
ax.set_ylabel("Success Rate (%)")
ax.set_title("Threshold Success Rates per Variant")
ax.legend(title="Threshold", frameon=False)
ax.grid(axis="y", alpha=0.3)

fig.tight_layout()
fig.savefig("plot_threshold_clustered.png", dpi=300)
plt.close(fig)


# ---------------------------------------------------------
# PLOT 2: HEATMAP
# ---------------------------------------------------------

heatmap_data = summary_df.set_index("variant")[
    [f"pct_<_ {thr}" for thr in THRESHOLDS]
].copy()

heatmap_data.columns = [f"< {thr}" for thr in THRESHOLDS]

fig, ax = plt.subplots(figsize=(8, 4))
sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".1f",
    cmap="viridis",
    linewidths=0.5,
    cbar_kws={"label": "Success Rate (%)"},
    ax=ax,
)

ax.set_title("Heatmap of Threshold Success Rates")
fig.tight_layout()
fig.savefig("plot_threshold_heatmap.png", dpi=300)
plt.close(fig)


# ---------------------------------------------------------
# PLOT 3: HORIZONTAL BARPLOT
# ---------------------------------------------------------

# Choose the threshold < 0.02 as the primary performance indicator
primary_thr = 0.02
values = summary_df[f"pct_<_ {primary_thr}"].values
labels = summary_df["variant"].tolist()
colors_bar = [COLORS[v] for v in labels]

fig, ax = plt.subplots(figsize=(8, 4))

ax.barh(
    labels,
    values,
    color=colors_bar,
    edgecolor="black",
    linewidth=0.8,
)

ax.set_xlabel("Success Rate (%)")
ax.set_title(f"Success Rate per Variant (Threshold < {primary_thr})")
ax.grid(axis="x", alpha=0.3)

fig.tight_layout()
fig.savefig("plot_threshold_horizontal.png", dpi=300)
plt.close(fig)

print("Plots saved:")
print(" - plot_threshold_clustered.png")
print(" - plot_threshold_heatmap.png")
print(" - plot_threshold_horizontal.png")
print(" - threshold_summary.csv")
