"""Approximating sin(x) using a feedforward network defined via EvoNet.

This script evaluates multiple random seeds for reproducibility.
Each run logs structure evolution and final approximation results.
"""

import numpy as np
import os

from evolib import Indiv, Pop, mse_loss, plot_approximation, save_combined_net_plot
from evolib.utils.random import set_random_seed

from evolib.utils.heli_experiment_logger import HeliExperimentLogger

from typing import Callable

# fmt: off
SEEDS = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
         59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
# fmt: on

CONFIG_FILE = "01_sine_structural_mutation.yaml"

# Define target function
X_RAW = np.linspace(0, 2 * np.pi, 100)
X_NORM = (X_RAW - np.pi) / np.pi
Y_TRUE = np.sin(X_RAW)


# Fitness function
def evonet_fitness(indiv: Indiv) -> None:
    predictions = []
    net = indiv.para["brain"]

    for x_norm in X_NORM:
        output = net.calc([x_norm])
        predictions.append(output[0])

    indiv.fitness = mse_loss(Y_TRUE, np.array(predictions))


def make_on_end(pop: Pop, seed: int) -> Callable[[Pop], None]:

    def on_end(pop: Pop) -> None:
        # Visualize result

        best = pop.best()
        net = best.para["brain"].net

        y_pred = [net.calc([x])[0] for x in X_NORM]
        plot_approximation(
            y_pred,
            Y_TRUE,
            title="Best Approximation",
            pred_marker=None,
            true_marker=None,
            show=False,
            save_path=f"results/plots/01_sine_structural_mutation_best_approximation_{seed}.png",
        )

        save_combined_net_plot(
            net, X_RAW, Y_TRUE, y_pred, 
            f"results/plots/01_sine_structural_mutation_network_{seed}.png"
        )

    return on_end

def make_on_generation_end(structure_logger: HeliExperimentLogger) -> Callable[[Pop],
                                                                               None]:
    """Return a generation-end callback bound to a given structure logger."""
    def on_generation_end(pop: Pop) -> None:
        structure_logger.log_generation(pop.generation_num, pop.indivs)
    return on_generation_end


for seed in SEEDS:
    with HeliExperimentLogger(
        f"results/structure/01_sine_structural_mutation_structure_{seed}.csv"
    ) as structure_logger:
        set_random_seed(seed)
        pop = Pop(config_path=CONFIG_FILE,
            lineage_file=f"results/lineage/01_sine_structural_mutation_lineage_{seed}.csv",
            fitness_function=evonet_fitness)
        pop.run(on_generation_end=make_on_generation_end(structure_logger),
                on_end=make_on_end(pop, seed)
        )
        pop.history_logger.save_csv(f"results/fitness/01_sine_structural_mutation_{seed}.csv")
