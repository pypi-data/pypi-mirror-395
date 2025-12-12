"""
Global aggregation and comparison of all sine experiments (baseline, structural, split, HELI).

Reads each experiment's aggregated results (mean/std per generation),
creates comparative plots for fitness and structure, and exports
a summary CSV with final metrics.

Run from the root directory:
    python aggregate_global.py
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
EXPERIMENTS = {
    "Baseline": "xor_baseline/results/aggregated/mean_std_per_generation.csv",
    "Structural": "xor_structural_mutation/results/aggregated/mean_std_per_generation.csv",
    "Split": "xor_structural_mutation_split/results/aggregated/mean_std_per_generation.csv",
    "HELI": "xor_structural_mutation_heli/results/aggregated/mean_std_per_generation.csv",
    "Split + HELI": "xor_structural_mutation_split_heli/results/aggregated/mean_std_per_generation.csv",
}

STRUCTURE = {
    "Baseline": "xor_baseline/results/aggregated/mean_structure_per_generation.csv",
    "Structural": "xor_structural_mutation/results/aggregated/mean_structure_per_generation.csv",
    "Split": "xor_structural_mutation_split/results/aggregated/mean_structure_per_generation.csv",
    "HELI": "xor_structural_mutation_heli/results/aggregated/mean_structure_per_generation.csv",
    "Split + HELI": "xor_structural_mutation_split_heli/results/aggregated/mean_structure_per_generation.csv",
}

OUT_DIR = Path("comparisons")
OUT_DIR.mkdir(exist_ok=True)

COLORS = {
    "Baseline": "#1f77b4",
    "Structural": "#2ca02c",
    "Split": "#ff7f0e",
    "HELI": "#d62728",
    "Split + HELI": "#9467bd",
}

# ---------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------
def load_csv_safe(path: str) -> pd.DataFrame | None:
    p = Path(path)
    if not p.exists():
        print(f"⚠️ Missing file: {p}")
        return None
    return pd.read_csv(p)

# ---------------------------------------------------------------------
# 1. Fitness comparison plot
# ---------------------------------------------------------------------
plt.figure(figsize=(7, 4))
summary_rows = []

for label, path in EXPERIMENTS.items():
    df = load_csv_safe(path)
    if df is None:
        continue
    plt.plot(df["generation"], df["mean_best_fitness"], color=COLORS[label],
             linewidth=2.0, label=label)
    plt.fill_between(df["generation"],
                     df["mean_best_fitness"] - df["std_best_fitness"],
                     df["mean_best_fitness"] + df["std_best_fitness"],
                     color=COLORS[label], alpha=0.15)

    # Summary metrics
    last = df.iloc[-1]
    summary_rows.append({
        "Variant": label,
        "Final_Fitness_Mean": last["mean_best_fitness"],
        "Final_Fitness_STD": last["std_best_fitness"],
    })

plt.xlabel("Generation")
plt.ylabel("Best Fitness (↓)")
plt.title("Sine Approximation – Fitness Comparison (Mean ± 1 STD, 30 Seeds)")
plt.grid(alpha=0.3)
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig(OUT_DIR / "fitness_comparison.png", dpi=300)
plt.close()

# ---------------------------------------------------------------------
# 2. Structure comparison plot (Neurons)
# ---------------------------------------------------------------------
plt.figure(figsize=(7, 4))

for label, path in STRUCTURE.items():
    df = load_csv_safe(path)
    if df is None:
        continue

    plt.plot(df["generation"], df["mean_num_neurons"], color=COLORS[label],
             linewidth=2.0, label=label)
    plt.fill_between(df["generation"],
                     df["mean_num_neurons"] - df["std_num_neurons"],
                     df["mean_num_neurons"] + df["std_num_neurons"],
                     color=COLORS[label], alpha=0.15)

    last = df.iloc[-1]

    # sichere Zuordnung anhand Variant-Namen statt Listenreihenfolge
    for row in summary_rows:
        if row["Variant"] == label:
            row.update({
                "Final_Neurons_Mean": last["mean_num_neurons"],
                "Final_Neurons_STD": last["std_num_neurons"],
                "Final_Weights_Mean": last["mean_num_weights"],
                "Final_Weights_STD": last["std_num_weights"],
            })
            break

plt.xlabel("Generation")
plt.ylabel("Neurons")
plt.title("Sine Approximation – Structural Growth (Mean ± 1 STD, 30 Seeds)")
plt.grid(alpha=0.3)
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig(OUT_DIR / "structure_comparison.png", dpi=300)
plt.close()

# ---------------------------------------------------------------------
# 3. Export summary table
# ---------------------------------------------------------------------
df_summary = pd.DataFrame(summary_rows)
df_summary = df_summary[
    ["Variant", "Final_Fitness_Mean", "Final_Fitness_STD",
     "Final_Neurons_Mean", "Final_Neurons_STD",
     "Final_Weights_Mean", "Final_Weights_STD"]
]
df_summary.to_csv(OUT_DIR / "summary_table.csv", index=False)

print(f"✅ Comparison complete. Results saved to: {OUT_DIR.resolve()}")
print(df_summary)
