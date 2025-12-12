"""
Aggregate per-seed results for fitness and structure metrics.

This script computes mean ± std per generation across all seed runs
and stores both the numeric aggregates and corresponding plots.

Usage: run inside an experiment folder
"""

import pandas as pd
import matplotlib.pyplot as plt
import glob
from pathlib import Path

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
RESULTS_DIR = Path("results")
FITNESS_DIR = RESULTS_DIR / "fitness"
STRUCTURE_DIR = RESULTS_DIR / "structure"
AGGREGATED_DIR = RESULTS_DIR / "aggregated"
AGGREGATED_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------
# 1. Aggregate fitness metrics
# ---------------------------------------------------------------------
fitness_files = sorted(FITNESS_DIR.glob("*.csv"))
if not fitness_files:
    raise FileNotFoundError(f"No fitness CSVs found in {FITNESS_DIR}")

dfs_fitness = [pd.read_csv(f) for f in fitness_files]
df_fitness_all = pd.concat(dfs_fitness, ignore_index=True)

grouped = df_fitness_all.groupby("generation")["best_fitness"]
mean_fitness = grouped.mean()
std_fitness = grouped.std()

df_fitness_result = pd.DataFrame({
    "generation": mean_fitness.index,
    "mean_best_fitness": mean_fitness.values,
    "std_best_fitness": std_fitness.values,
})
df_fitness_result.to_csv(AGGREGATED_DIR / "mean_std_per_generation.csv", index=False)

# ---------------------------------------------------------------------
# 2. Aggregate structure metrics
# ---------------------------------------------------------------------
structure_files = sorted(STRUCTURE_DIR.glob("*.csv"))
if not structure_files:
    raise FileNotFoundError(f"No structure CSVs found in {STRUCTURE_DIR}")

dfs_structure = [pd.read_csv(f) for f in structure_files]
df_structure_all = pd.concat(dfs_structure, ignore_index=True)

group_weights = df_structure_all.groupby("generation")["mean_num_weights"]
group_neurons = df_structure_all.groupby("generation")["mean_num_neurons"]

df_structure_result = pd.DataFrame({
    "generation": group_weights.mean().index,
    "mean_num_weights": group_weights.mean().values,
    "std_num_weights": group_weights.std().values,
    "mean_num_neurons": group_neurons.mean().values,
    "std_num_neurons": group_neurons.std().values,
})
df_structure_result.to_csv(AGGREGATED_DIR / "mean_structure_per_generation.csv", index=False)

# ---------------------------------------------------------------------
# 3. Plot generation
# ---------------------------------------------------------------------
def plot_with_std(x, y, std, title, ylabel, filename, yscale="linear", color="blue"):
    plt.figure(figsize=(7, 4))
    plt.plot(x, y, color=color)
    plt.fill_between(x, y - std, y + std, color=color, alpha=0.15)
    plt.xlabel("Generation")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.grid(alpha=0.3, which="both")
    plt.yscale(yscale)
    plt.savefig(AGGREGATED_DIR / filename, dpi=300)
    plt.close()

# Fitness plot
plot_with_std(
    mean_fitness.index,
    mean_fitness.values,
    std_fitness.values,
    title="Structural Mutation with Split (HELI)– Mean Best Fitness ± 1 STD (30 Seeds)",
    ylabel="Best Fitness (↓)",
    color="#9467bd",
    filename="fitness_mean_over_seeds.png",
)

# Weights Plot
plot_with_std(
    group_weights.mean().index,
    group_weights.mean().values,
    group_weights.std().values,
    title="Structural Mutation with Split (HELI) – Mean Weight Count ± 1 STD (30 Seeds)",
    ylabel="Connections",
    color="#9467bd",
    filename="structure_mean_weights.png",
)

# Neurons plot
plot_with_std(
    group_neurons.mean().index,
    group_neurons.mean().values,
    group_neurons.std().values,
    title="Structural Mutation with Split (HELI) – Mean Neuron Count ± 1 STD (30 Seeds)",
    ylabel="Neurons",
    color="#9467bd",
    filename="structure_mean_neurons.png",
)

print(f"Aggregates and plots written to {AGGREGATED_DIR.resolve()}")
