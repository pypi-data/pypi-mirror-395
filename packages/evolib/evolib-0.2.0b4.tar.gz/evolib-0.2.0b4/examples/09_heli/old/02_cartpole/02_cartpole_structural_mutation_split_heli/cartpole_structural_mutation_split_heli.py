"""
This script evaluates multiple random seeds for reproducibility.
Each run logs structure evolution and final approximation results.
"""

import numpy as np

from evolib import (
    Pop,
    Individual,
    plot_approximation,
    save_combined_net_plot,
    GymEnv,
)
from evolib.utils.random import set_random_seed

from evolib.utils.heli_experiment_logger import HeliExperimentLogger

from typing import Callable

# fmt: off
SEEDS = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
         59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
# fmt: on

CONFIG_FILE = "cartpole_structural_mutation_split_heli.yaml"
MAX_STEPS = 500

# init environment once (can be reused for all individuals)
cartpole_env = GymEnv("CartPole-v1", max_steps=MAX_STEPS, deterministic_init=False)

def evonet_fitness(indiv: Individual) -> None:
    """Evaluate one individual by running CartPole and assign fitness."""
    fitness = cartpole_env.evaluate(indiv, module="brain")
    indiv.fitness = -fitness


def make_on_end(pop: Pop, seed: int) -> Callable[[Pop], None]:

    def on_end(pop: Pop) -> None:
        # Visualize result

        best = pop.best()
        net = best.para["brain"].net

        gif = cartpole_env.visualize(
            best,
            pop.generation_num,              
            filename=f"results/plots/cartpole_structural_mutation_split_heli_{seed}.gif", 
        )

        net.plot(f"results/plots/cartpole_structural_mutation_split_heli_network_{seed}.png",
                 fillcolors_on=True, thickness_on=True)

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
        f"results/structure/cartpole_structural_mutation_split_heli_structure_{seed}.csv"
    ) as structure_logger:
        set_random_seed(seed)
        pop = Pop(
            config_path=CONFIG_FILE,
            lineage_file=f"results/lineage/cartpole_structural_mutation_split_heli_lineage_{seed}.csv",
            fitness_function=evonet_fitness,
        )
        pop.run(
            on_generation_end=make_on_generation_end(structure_logger),
            on_end=make_on_end(pop, seed),
        )
        pop.history_logger.save_csv(f"results/fitness/cartpole_structural_mutation_split_heli_{seed}.csv")
