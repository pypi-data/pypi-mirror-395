"""
Composite figure (2 subplots): Fitness and Structural Growth comparison
with shared external legend and correctly positioned (a)/(b) labels.
"""

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
OUT_DIR = Path("comparisons")
OUT_DIR.mkdir(exist_ok=True)

FITNESS = {
    "Baseline": "xor_baseline/results/aggregated/mean_std_per_generation.csv",
    "Split": "xor_structural_mutation_split/results/aggregated/mean_std_per_generation.csv",
    "Split + HELI": "xor_structural_mutation_split_heli/results/aggregated/mean_std_per_generation.csv",
}

STRUCTURE = {
    "Baseline": "xor_baseline/results/aggregated/mean_structure_per_generation.csv",
    "Split": "xor_structural_mutation_split/results/aggregated/mean_structure_per_generation.csv",
    "Split + HELI": "xor_structural_mutation_split_heli/results/aggregated/mean_structure_per_generation.csv",
}

COLORS = {
    "Baseline": "#1f77b4",
    "Split": "#ff7f0e",
    "Split + HELI": "#9467bd",
}

# ---------------------------------------------------------------------
# Style setup
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
    "lines.linewidth": 1.8,
    "axes.linewidth": 0.8,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
})

# ---------------------------------------------------------------------
# Create figure
# ---------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.8), sharex=False)

# (a) Fitness
ax = axes[0]
for label, path in FITNESS.items():
    df = pd.read_csv(path)
    ax.plot(df["generation"], df["mean_best_fitness"], color=COLORS[label], label=label)
    ax.fill_between(df["generation"],
                    df["mean_best_fitness"] - df["std_best_fitness"],
                    df["mean_best_fitness"] + df["std_best_fitness"],
                    color=COLORS[label], alpha=0.15)
ax.set_xlabel("Generation")
ax.set_ylabel("Best Fitness (↓)")
ax.set_ylim(0, 0.1)
ax.set_xlim(0, 200)
ax.text(0.02, 1.05, "(a)", transform=ax.transAxes,
        fontsize=12, fontweight="bold", va="bottom", ha="left")
ax.grid(alpha=0.3)

# (b) Structure
ax = axes[1]
for label, path in STRUCTURE.items():
    df = pd.read_csv(path)
    ax.plot(df["generation"], df["mean_num_neurons"], color=COLORS[label])
    ax.fill_between(df["generation"],
                    df["mean_num_neurons"] - df["std_num_neurons"],
                    df["mean_num_neurons"] + df["std_num_neurons"],
                    color=COLORS[label], alpha=0.15)
ax.set_xlabel("Generation")
ax.set_ylabel("Neurons")
ax.set_ylim(0, 14)
ax.set_xlim(0, 200)
ax.text(0.02, 1.05, "(b)", transform=ax.transAxes,
        fontsize=12, fontweight="bold", va="bottom", ha="left")
ax.grid(alpha=0.3)

# Gemeinsame Legende unterhalb
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", ncol=3,
           frameon=False, bbox_to_anchor=(0.5, -0.05))

# ---------------------------------------------------------------------
# Layout & Save
# ---------------------------------------------------------------------
fig.suptitle("Sine Approximation – Comparison of Fitness and Structural Growth",
             fontsize=13, y=1.02)
fig.tight_layout(rect=[0, 0.07, 1, 1])
outfile = OUT_DIR / "figure_composite.png"
fig.savefig(outfile, dpi=600)
plt.close(fig)

print(f"✅ Clean composite figure saved to: {outfile.resolve()}")
