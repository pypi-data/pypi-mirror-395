import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# --- Beispielhafte Eingabedatenstruktur (anpassen an reale CSVs) ---
# Jede CSV enthält: generation, mean_best, std_best
data_files = {
    "Baseline": "xor_baseline/results/aggregated/mean_std_per_generation.csv",
    "Structural Mutation": "xor_structural_mutation/results/aggregated/mean_std_per_generation.csv",
    "Structural Mutation (HELI)": "xor_structural_mutation_heli/results/aggregated/mean_std_per_generation.csv",
    "Structural Mutation + Split": "xor_structural_mutation_split/results/aggregated/mean_std_per_generation.csv",
    "Structural Mutation + Split (HELI)": "xor_structural_mutation_split_heli/results/aggregated/mean_std_per_generation.csv",
}

colors = {
    "Baseline": "#1f77b4",
    "Structural Mutation": "#2ca02c",
    "Structural Mutation (HELI)": "#d62728",
    "Structural Mutation + Split": "#ff7f0e",
    "Structural Mutation + Split (HELI)": "#9467bd",
}

# --- Daten einlesen ---
dfs = {}
for name, path in data_files.items():
    df = pd.read_csv(path)
    dfs[name] = df

# --- Composite: alle fünf Varianten separat ---
fig, axes = plt.subplots(2, 3, figsize=(14, 8))
axes = axes.flatten()

for i, (name, df) in enumerate(dfs.items()):
    ax = axes[i]
    mean, std = df["mean_best_fitness"], df["std_best_fitness"]
    gens = df["generation"]
    ax.plot(gens, mean, color=colors[name], lw=2)
    ax.fill_between(gens, mean - std, mean + std, color=colors[name], alpha=0.3)
    ax.set_title(name, fontsize=11)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Best Fitness (↓)")
    ax.grid(alpha=0.3)

# letztes Panel leer lassen
for j in range(len(dfs), len(axes)):
    axes[j].axis("off")

fig.suptitle("Comparison of Evolution Variants – Mean ± 1 STD (30 Seeds)", fontsize=14)
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig("comparison_all_variants.png", dpi=300)
plt.close(fig)


# --- Dreier-Variante (für Paper): Baseline vs Structural vs HELI+Split ---
fig, ax = plt.subplots(figsize=(6, 4))

selected = [
    ("Baseline", colors["Baseline"]),
    ("Structural Mutation + Split", colors["Structural Mutation + Split"]),
    ("Structural Mutation + Split (HELI)", colors["Structural Mutation + Split (HELI)"]),
]

for name, color in selected:
    df = dfs[name]
    mean, std = df["mean_best_fitness"], df["std_best_fitness"]
    gens = df["generation"]
    ax.plot(gens, mean, color=color, lw=2, label=name)
    ax.fill_between(gens, mean - std, mean + std, color=color, alpha=0.25)

ax.set_xlabel("Generation")
ax.set_ylabel("Best Fitness (↓)")
ax.legend(frameon=False, fontsize=9)
ax.grid(alpha=0.3)
ax.set_title("Baseline vs Structural vs Structural + HELI")

fig.tight_layout()
fig.savefig("comparison_core_variants.png", dpi=300)
plt.close(fig)
