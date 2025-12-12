import numpy as np
from evolib import Population, Individual, plot_approximation

# Fixed test sequence
SEQ_LEN = 100
WARMUP_STEPS = 0
CONFIG_FILE = "./configs/00_identity_test.yaml"
FRAME_FOLDER = "00_frames"

# Generate simple linear sequence
full_seq = np.linspace(-1.0, 1.0, SEQ_LEN)
input_seq = full_seq
target_seq = full_seq

# Fitness: MSE between predicted and actual (no shift)
def eval_identity_fitness(indiv: Individual) -> float:
    net = indiv.para["brain"].net
    net.reset(full=True)

    preds = []
    for i in range(WARMUP_STEPS, len(input_seq)):
        y_pred = net.calc([input_seq[i]])[0]
        preds.append(y_pred)

    y_true = target_seq[WARMUP_STEPS:]
    preds = np.array(preds)
    mse = np.mean((preds - y_true) ** 2)

    indiv.extra_metrics["mse"] = mse
    indiv.fitness = mse  # minimize error → maximize -mse
    return indiv.fitness

# Plot best prediction
def plot_prediction(pop: Population) -> None:
    best = pop.best()
    net = best.para["brain"].net
    net.reset(full=True)

    preds = []
    for i in range(WARMUP_STEPS, len(input_seq)):
        y_pred = net.calc([input_seq[i]])[0]
        preds.append(y_pred)

    plot_approximation(
        preds,
        target_seq[WARMUP_STEPS:],
        title=(
            f"Identity Test: x[t] → x[t]\n"
            f"gen={pop.generation_num}, MSE={best.extra_metrics['mse']:.6f}"
        ),
        pred_label="Prediction",
        true_label="Target",
        show=False,
        show_grid=False,
        save_path=f"{FRAME_FOLDER}/gen_{pop.generation_num:03d}.png",
    )

def main():
    pop = Population(CONFIG_FILE, fitness_function=eval_identity_fitness)
    pop.run(verbosity=1, on_generation_end=plot_prediction)

if __name__ == "__main__":
    main()
