"""
Example: Evolve a controller for the MountainCarContinuous-v0 environment.

This example demonstrates how an evolutionary algorithm can evolve
a neural controller that drives the car up the hill.
Each individual is evaluated in the MountainCarContinuous-v0 environment and
the best individual of each generation is visualized as a GIF.
"""

from evolib import GymEnv, Individual, Population, resume_or_create

CONFIG_FILE = "./configs/mountaincar_continuous.yaml"
FRAME_FOLDER = "mountain_car_frames"
MAX_STEPS = 999

# init environment once (can be reused for all individuals)
mountaincar_env = GymEnv("MountainCarContinuous-v0", max_steps=MAX_STEPS)


def eval_fitness(indiv):
    """Evaluate MountainCarContinuous by tracking max_position."""
    env = mountaincar_env.env  # unwrap actual gymnasium environment

    obs, _ = env.reset()
    max_pos = obs[0]  # position is the first state component

    for _ in range(MAX_STEPS):
        # EvoNet forward pass
        net = indiv.para["brain"].net
        action = net.calc(obs)[0]  # output is 1-dimensional

        obs, reward, terminated, truncated, info = env.step([action])
        pos = obs[0]

        if pos > max_pos:
            max_pos = pos

        if terminated or truncated:
            break

    indiv.fitness = max_pos


def on_generation_end(pop: Population) -> None:
    """Save an animated GIF of the current best individual each generation."""
    best = pop.best()
    gif = mountaincar_env.visualize(
        best,
        pop.generation_num,
        filename=f"{FRAME_FOLDER}/gen_{pop.generation_num:03d}.gif",
    )
    print(f"Saved: {gif}")


    net = best.para["brain"].net
    net.calc([-1.0, 0.03])[0]
    net.plot(f"{FRAME_FOLDER}/net_gen_{pop.generation_num:03d}", fillcolors_on=True, thickness_on=True)


if __name__ == "__main__":
    pop = resume_or_create(
        CONFIG_FILE,
        fitness_function=eval_fitness,
        run_name="03_mountaincar_continuous",
    )

    pop.run(verbosity=1, on_generation_end=on_generation_end)
