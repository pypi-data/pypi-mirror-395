"""
Baseline experiment for the XOR task using a fixed EvoNet architecture.
Evaluates multiple random seeds for reproducibility.
Logs per-generation structure metrics and final network approximations.
"""

import numpy as np

from evolib import (
    Pop,
    Indiv,
    plot_approximation,
    save_combined_net_plot,
    mse_loss,
)
from evolib.utils.random import set_random_seed

from evolib.utils.heli_experiment_logger import HeliExperimentLogger

from typing import Callable
from pathlib import Path


Path("results/plots").mkdir(parents=True, exist_ok=True)
Path("results/fitness").mkdir(parents=True, exist_ok=True)
Path("results/structure").mkdir(parents=True, exist_ok=True)
Path("results/lineage").mkdir(parents=True, exist_ok=True)

# fmt: off
SEEDS = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
         59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
# fmt: on

CONFIG_FILE = "xor_structural_mutation.yaml"

# XOR dataset                                                                            
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])                                           
Y = np.array([0, 1, 1, 0])                                                               
                                                                                         
# Normalization                                                                          
X_NORM = X.astype(float)                                                                 
Y_TRUE = Y.astype(float)

def evonet_fitness(indiv: Indiv) -> None:
    """
    Fitness function for the XOR task.

    Computes the mean squared error (MSE) between network predictions
    and the true XOR outputs. Lower values indicate better performance.

    Args:
        indiv (Indiv): An individual containing a 'brain' EvoNet module.
    """
    net = indiv.para["brain"]
    predictions = [net.calc(x.tolist())[0] for x in X_NORM]
    indiv.fitness = mse_loss(Y_TRUE, np.array(predictions))

def make_on_end(pop: Pop, seed: int) -> Callable[[Pop], None]:

    def on_end(pop: Pop) -> None:
        # Visualize result

        best = pop.best()
        net = best.para["brain"].net
        y_pred = [net.calc(x.tolist())[0] for x in X]

        save_combined_net_plot(
            net,
            np.arange(len(X)),
            Y_TRUE,
            np.array(y_pred),
            f"results/plots/xor_structural_mutation_network_{seed}.png",
            title="Baseline XOR Approximation",
            xlabel="Input pattern index",
            ylabel="Output",
            true_label="Target: XOR",
            pred_label="Network Output",
        )

    return on_end


def make_on_generation_end(
    structure_logger: HeliExperimentLogger,
) -> Callable[[Pop], None]:
    """Return a generation-end callback bound to a given structure logger."""

    def on_generation_end(pop: Pop) -> None:
        structure_logger.log_generation(pop)

    return on_generation_end


for seed in SEEDS:
    with HeliExperimentLogger(
        f"results/structure/xor_structural_mutation_{seed}.csv"
    ) as structure_logger:
        set_random_seed(seed)
        pop = Pop(
            config_path=CONFIG_FILE,
            lineage_file=f"results/lineage/xor_structural_mutation_lineage_{seed}.csv",
            fitness_function=evonet_fitness,
        )
        pop.run(
            on_generation_end=make_on_generation_end(structure_logger),
            on_end=make_on_end(pop, seed),
        )
        pop.history_logger.save_csv(f"results/fitness/xor_structural_mutation_{seed}.csv")
