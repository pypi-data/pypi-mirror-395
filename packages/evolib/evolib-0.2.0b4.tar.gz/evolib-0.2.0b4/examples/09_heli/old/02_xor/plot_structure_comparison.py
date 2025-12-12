"""
Final publication-quality plot: Structural growth (neurons) for sine approximation experiments.

Reduced to Baseline, Split, and Split + HELI.
"""

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
OUT_DIR = Path("comparisons")
OUT_DIR.mkdir(exist_ok=True)

CSV_PATHS = {
    "Baseline": "01_sine_baseline/results/aggregated/mean_structure_per_generation.csv",
    "Split": "01_sine_structural_mutation_split/results/aggregated/mean_structure_per_generation.csv",
    "Split + HELI": "01_sine_structural_mutation_split_heli/results/aggregated/mean_structure_per_generation.csv",
}

COLORS = {
    "Baseline": "#1f77b4",
    "Split": "#ff7f0e",
    "Split + HELI": "#9467bd",
}

# ---------------------------------------------------------------------
# Plot setup
# ---------------------------------------------------------------------
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "font.size": 10,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.dpi": 600,
    "lines.linewidth": 2.0,
    "axes.linewidth": 0.8,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
})

fig, ax = plt.subplots(figsize=(5.5, 3.5))

for label, path in CSV_PATHS.items():
    df = pd.read_csv(path)
    ax.plot(df["generation"], df["mean_num_neurons"],
            color=COLORS[label], label=label)
    ax.fill_between(df["generation"],
                    df["mean_num_neurons"] - df["std_num_neurons"],
                    df["mean_num_neurons"] + df["std_num_neurons"],
                    color=COLORS[label], alpha=0.15)

# ---------------------------------------------------------------------
# Labels and limits
# ---------------------------------------------------------------------
ax.set_xlabel("Generation")
ax.set_ylabel("Neurons")
ax.set_ylim(0, 14)
ax.set_xlim(0, 200)
ax.set_title("Sine Approximation – Structural Growth (Mean ± 1 STD, 30 Seeds)")
ax.legend(frameon=False, loc="upper left")
ax.grid(alpha=0.3)

# ---------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------
outfile = OUT_DIR / "structure_comparison_final.png"
fig.tight_layout()
fig.savefig(outfile, dpi=600)
plt.close(fig)

print(f"✅ Saved high-quality plot to {outfile.resolve()}")
