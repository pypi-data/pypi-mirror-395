# Example 05-06 — Evolving mutation strength as a module (global sigma)
from __future__ import annotations

import numpy as np

from evolib import Indiv, Pop, mse_loss

TARGET = np.ones(16, dtype=float)  # einfacher Zielvektor
LAMBDA = 40  # offspring
MU = 20  # parents
SIGMA_MIN, SIGMA_MAX = 1e-4, 1.0


def softplus(x: float) -> float:
    return np.log1p(np.exp(x))


def clamp_sigma(s: float) -> float:
    return float(np.clip(s, SIGMA_MIN, SIGMA_MAX))


def decode_sigma(indiv: Indiv) -> float:
    # meta_sigma: stores log-ish parameter, convert to positive sigma
    # log_s = float(indiv.para["meta_sigma"].vector[0])
    # return clamp_sigma(softplus(log_s))
    sigma = clamp_sigma(abs(indiv.para["meta_sigma"].vector[0]))
    return sigma


def eval_fitness(indiv: Indiv) -> None:
    vec = np.array(indiv.para["controller"].vector, dtype=float)
    indiv.fitness = mse_loss(TARGET, vec)


def mutate_with_sigma(parent: Indiv) -> Indiv:
    # shallow clone via EvoLib-API: falls es kein clone gibt, erzeuge neues Indiv aus config
    child = parent.copy() if hasattr(parent, "copy") else parent.spawn_clone()
    sigma = decode_sigma(parent)

    # mutate controller manually using sigma
    x = np.array(child.para["controller"].vector, dtype=float)
    x += sigma * np.random.randn(x.size)
    # respect bounds [-1,1] if gesetzt
    x = np.clip(x, -1.0, 1.0)
    child.para["controller"].vector = x

    # mutate meta_sigma via its standard mutation (kleiner Schritt)
    child.para["meta_sigma"].mutate()
    return child


def mu_plus_lambda_step(pop: Pop) -> None:
    # evaluate parents if needed
    for ind in pop.indivs:
        if ind.fitness is None:
            eval_fitness(ind)

    # produce offspring
    offspring = []
    for _ in range(LAMBDA):
        p = np.random.choice(pop.indivs[:MU])  # simple truncation parents
        c = mutate_with_sigma(p)
        eval_fitness(c)
        offspring.append(c)

    # replacement: (μ+λ), keep best MU
    combined = pop.indivs + offspring
    combined.sort(key=lambda i: i.fitness)
    pop.indivs = combined[:MU]


def run() -> None:
    np.random.seed(42)
    pop = Pop("new.yaml", fitness_function=eval_fitness)
    # initial eval
    for ind in pop.indivs:
        eval_fitness(ind)

    max_gens = 300
    for _ in range(max_gens):
        mu_plus_lambda_step(pop)
        if pop.generation_num % 10 == 0:
            best = pop.best()
            print(
                f"gen={pop.generation_num:4d}  fit={best.fitness:.6f}  sigma={decode_sigma(best):.4f}"
            )
            print(pop.best().para["meta_sigma"].vector[0])
        pop.generation_num += 1


if __name__ == "__main__":
    run()
