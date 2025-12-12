"""
Example: BipedalWalker with EvoLib

This script demonstrates how to evolve a neural network controller
for the continuous-control **BipedalWalker-v3** Gymnasium environment.  
The walker must learn to coordinate its legs and joints to move
forward without falling.  

Key aspects:
* Continuous state (24-dimensional observation vector).
* Continuous action space (4 torques for hip and knee joints).
* Fitness: negative cumulative reward (minimization).
* Visualization: renders the best walker every 10 generations.
"""

from evolib import Population, Individual, resume_or_create, GymEnv, save_checkpoint

CONFIG_FILE = "./configs/05_bipedal_walker.yaml"
FRAME_FOLDER = "05_frames"
RUN_NAME = "05_BipedalWalker"
MAX_STEPS = 1600  # typical for BipedalWalker is 1600


# init environment once (can be reused for all individuals)
gym_env = GymEnv("BipedalWalker-v3", max_steps=MAX_STEPS)


def eval_walker_fitness(indiv: Individual) -> None:
    """Run a single episode in a fresh environment to avoid Box2D race conditions."""
    #local_env = GymEnv("BipedalWalker-v3", max_steps=MAX_STEPS)
    reward = gym_env.evaluate(indiv, module="brain", episodes=3)
    #print(f"Reward: {reward}")
    indiv.fitness = -reward

def checkpoint(pop: Population) -> None:                                                 
    save_checkpoint(pop, run_name=RUN_NAME)
    print("Checkpoint saved.")

def on_improvement(pop: Population) -> None:
    """Visualize the best individual every 10 generations (and at the end)."""

    best = pop.best() 
    best.para["brain"].net.plot(name="test")

def on_generation_end(pop: Population) -> None:
    """Visualize the best individual every 10 generations (and at the end)."""

    checkpoint(pop)

    return

    best = pop.best()
    print(best.para["brain"].evo_params.mutation_strength)

#    if pop.generation_num % 10 == 0 or pop.generation_num == pop.max_generations:
    best = pop.best()
    gif = gym_env.visualize(
        best,
        pop.generation_num,
        filename=f"{FRAME_FOLDER}/gen_{pop.generation_num:03d}.gif",
    )
    print(f"Saved: {gif}")


if __name__ == "__main__":
    pop = resume_or_create(
        CONFIG_FILE,
        fitness_function=eval_walker_fitness,
        run_name=RUN_NAME,
    )
    
    if pop.generation_num >= 50:
        print("*** Generation >= 50 --> setting mutation_probability to 0.4 ***")
        for indiv in pop.indivs:
            indiv.para["brain"].evo_params.mutation_probability = 0.4

    pop.run(verbosity=1, 
            on_generation_end=on_generation_end,
            on_improvement=on_improvement)
