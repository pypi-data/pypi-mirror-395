"""
Example: Recurrent Time Series Classification (5 classes)

This example demonstrates how an EvoNet with recurrent connections
can be evolved to classify the *future trend* of a time series.
Instead of predicting the exact numeric value, the task is to decide
whether the series will strongly decrease, decrease, stay neutral,
increase, or strongly increase within the next PRED_LEN steps.

Visualization: the input series is shown as a black line, with
colored points marking the predicted and true trend classes.
"""

import numpy as np
import matplotlib.pyplot as plt

from evolib import (
    Population,
    Individual,
    generate_timeseries,
    plot_approximation,
    resume_or_create,
    save_checkpoint,
    resume_from_checkpoint,
)

# Parameters ------------------------------------------------------------------
PATTERN = "trend_switch"  # pattern for synthetic time series
SEQ_LEN = 300             # number of training steps
PRED_LEN = 20              # horizon for classification
WARMUP_STEPS = max(0, PRED_LEN)
EVAL_RUNS = 10

FRAME_FOLDER = "06_frames"
CONFIG_FILE = "./configs/06_recurrent_indicator.yaml"

# --- Data generation ---------------------------------------------------------
FULL_SEQ = generate_timeseries(SEQ_LEN + PRED_LEN, pattern=PATTERN)
INPUT_SEQ = FULL_SEQ[:-PRED_LEN]

def make_labels(series: np.ndarray, horizon: int) -> np.ndarray:
    """Generate 5-class labels for future trend prediction."""
    labels = []
    for t in range(len(series) - horizon):
        future_mean = np.mean(series[t+1 : t+1+horizon])
        diff = (future_mean - series[t]) / max(1e-6, abs(series[t]))
        # thresholds in %
        if diff < -0.02:
            labels.append(0)  # strongly decreasing
        elif diff < -0.005:
            labels.append(1)  # slightly decreasing
        elif diff <= 0.005:
            labels.append(2)  # stable
        elif diff <= 0.02:
            labels.append(3)  # slightly increasing
        else:
            labels.append(4)  # strongly increasing
    return np.array(labels)

LABELS = make_labels(INPUT_SEQ, PRED_LEN)

# --- Fitness function --------------------------------------------------------
def evaluate(indiv: Individual) -> float:
    """Evaluate an individual using directional score (fitness) and accuracy (extra metric)."""
    net = indiv.para["brain"].net

    total_correct = 0
    total_samples = 0
    total_score = 0.0

    for i in range(EVAL_RUNS): 
        seed = np.random.randint(0, 2**32 - 1)
        full_seq = generate_timeseries(SEQ_LEN + PRED_LEN, pattern=PATTERN, seed=seed)
        input_seq = full_seq[:-PRED_LEN] 
        labels = make_labels(input_seq, PRED_LEN)

        net.reset(full=True)

        # Warmup phase
        for val in input_seq[:WARMUP_STEPS]:
            net.calc([val])

        # Classification phase
        for t in range(WARMUP_STEPS, len(labels)):
            x_t = input_seq[t]
            output = net.calc([x_t])
            pred_class = int(np.argmax(output))

            # Accuracy
            if pred_class == labels[t]:
                total_correct += 1

            # Directional score
            future_mean = np.mean(input_seq[t+1 : t+1+PRED_LEN])
            true_diff = future_mean - input_seq[t]

            class_mid = [-0.03, -0.01, 0.0, 0.01, 0.03]  # representative trend values
            pred_value = class_mid[pred_class]

            total_score += np.sign(true_diff) * pred_value
            total_samples += 1

    # Metrics
    accuracy = total_correct / max(1, total_samples)
    avg_score = total_score / max(1, total_samples)

    # Fitness = negative directional score (because EvoLib minimizes)
    indiv.fitness = -avg_score
    indiv.extra_metrics["accuracy"] = accuracy
    indiv.extra_metrics["directional_score"] = avg_score

    return indiv.fitness
# --- Visualization -----------------------------------------------------------
def save_plot(pop: Population) -> None:
    """Plot time series with true class labels of the best individual."""
    best = pop.best()
    net = best.para["brain"].net
    net.reset(full=True)

    # Warmup
    for val in INPUT_SEQ[:WARMUP_STEPS]:
        net.calc([val])

    # Predictions
    preds = []
    for t in range(WARMUP_STEPS, len(LABELS)):
        x_t = INPUT_SEQ[t]
        output = net.calc([x_t])
        preds.append(int(np.argmax(output)))


    # Colors and names
    colors = {0: "red", 1: "orange", 2: "gray", 3: "lightgreen", 4: "green"}
    names = [
        "strongly decreasing",
        "slightly decreasing",
        "stable",
        "slightly increasing",
        "strongly increasing",
    ]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(INPUT_SEQ, color="black", linewidth=1.5)

    # Plot true labels
    #for t, lab in enumerate(LABELS):
    #    ax.scatter(t, INPUT_SEQ[t], color=colors[lab], s=30, alpha=0.5)

    # Plot predictions of best individual
    last_pred = None
    for i, p in enumerate(preds):
        t = i + WARMUP_STEPS
        if p != last_pred:
            ax.scatter(t, INPUT_SEQ[t], color=colors[p], s=80, marker="o", linewidths=2)
        last_pred = p

    # Legend
    handles = [
        plt.Line2D([0], [0], marker="o", color="w",
                   label=names[i],
                   markerfacecolor=colors[i], markersize=8)
        for i in range(5)
    ]
    ax.legend(handles=handles, loc="upper right")

    acc = best.extra_metrics.get("accuracy", 0.0)
    score = best.extra_metrics["directional_score"]
    ax.set_title(f"5-Class Time Series Prediction (Accuracy={acc:.2f}, Score: {score:.2f})")
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    plt.tight_layout()
    plt.savefig(f"{FRAME_FOLDER}/gen_{pop.generation_num:03d}.png", dpi=300)
    #plt.show()
    plt.close()


# --- Main loop ---------------------------------------------------------------

if __name__ == "__main__":
    pop = resume_or_create(CONFIG_FILE, fitness_fn=evaluate)
    pop.run(verbosity=1, on_generation_end=save_plot)
