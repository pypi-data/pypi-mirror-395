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
    """Evaluate an individual based on trading-like profit and accuracy."""
    net = indiv.para["brain"].net

    total_profit = 0.0
    total_correct = 0
    total_samples = 0

    # Mapping: class → position size
    class_pos = [-1.0, -0.5, 0.0, 0.5, 1.0]

    for i in range(EVAL_RUNS):
        seed = np.random.randint(0, 2**32 - 1)
        full_seq = generate_timeseries(SEQ_LEN + PRED_LEN, pattern=PATTERN, seed=seed)
        input_seq = full_seq[:-PRED_LEN]
        labels = make_labels(input_seq, PRED_LEN)

        net.reset(full=True)

        # Warmup
        for val in input_seq[:WARMUP_STEPS]:
            net.calc([val])

        # Trading phase
        for t in range(WARMUP_STEPS, len(labels)):
            x_t = input_seq[t]
            output = net.calc([x_t])
            pred_class = int(np.argmax(output))

            # Accuracy (just as extra info)
            if pred_class == labels[t]:
                total_correct += 1

            # True movement
            future_mean = np.mean(input_seq[t+1 : t+1+PRED_LEN])
            true_diff = future_mean - input_seq[t]

            # Profit = position × price change
            pos = class_pos[pred_class]
            profit = pos * true_diff

            total_profit += profit
            total_samples += 1

    # Metrics
    accuracy = total_correct / max(1, total_samples)
    avg_profit = total_profit / max(1, total_samples)

    # EvoLib expects minimization → negative profit
    indiv.fitness = -avg_profit
    indiv.extra_metrics["accuracy"] = accuracy
    indiv.extra_metrics["profit"] = avg_profit

    return indiv.fitness



# --- Visualization -----------------------------------------------------------

def save_plot(pop: Population) -> None:
    """Plot series with predictions and equity curve of the best individual."""
    best = pop.best()
    net = best.para["brain"].net
    net.reset(full=True)

    class_pos = [-1.0, -0.5, 0.0, 0.5, 1.0]
    equity = [0.0]  # start balance
    preds = []

    # Warmup
    for val in INPUT_SEQ[:WARMUP_STEPS]:
        net.calc([val])

    # Trading & profit accumulation
    for t in range(WARMUP_STEPS, len(LABELS)):
        x_t = INPUT_SEQ[t]
        output = net.calc([x_t])
        pred_class = int(np.argmax(output))
        preds.append(pred_class)

        future_mean = np.mean(INPUT_SEQ[t+1 : t+1+PRED_LEN])
        true_diff = future_mean - INPUT_SEQ[t]
        pos = class_pos[pred_class]
        profit = pos * true_diff
        equity.append(equity[-1] + profit)

    # Colors & labels
    colors = {0: "red", 1: "orange", 2: "gray", 3: "lightgreen", 4: "green"}
    names = [
        "strongly decreasing",
        "slightly decreasing",
        "stable",
        "slightly increasing",
        "strongly increasing",
    ]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True,
                                   gridspec_kw={"height_ratios": [2, 1]})

    # --- Top: Series with prediction markers
    ax1.plot(INPUT_SEQ, color="black", linewidth=1.5)
    last_pred = None
    for i, p in enumerate(preds):
        t = i + WARMUP_STEPS
        if p != last_pred:
            ax1.scatter(t, INPUT_SEQ[t], color=colors[p], s=80, marker="o")
        last_pred = p
    
    # Legend                                                                             
    handles = [                                                                          
        plt.Line2D([0], [0], marker="o", color="w",                                      
                   label=names[i],                                                       
                   markerfacecolor=colors[i], markersize=8)                              
        for i in range(5)                                                                
    ]                                                                                    
    ax1.legend(handles=handles, loc="upper right") 

    acc = best.extra_metrics.get("accuracy", 0.0)
    prof = best.extra_metrics.get("profit", 0.0)
    ax1.set_title(f"Trading-like Prediction (Acc={acc:.2f}, Profit={prof:.3f})")

    # --- Bottom: Equity curve
    ax2.plot(equity, color="blue", linewidth=1.5)
    ax2.set_ylabel("Equity (Profit)")
    ax2.set_xlabel("Time")

    plt.tight_layout()
    plt.savefig(f"{FRAME_FOLDER}/gen_{pop.generation_num:03d}.png", dpi=300)
    plt.close()

# --- Main loop ---------------------------------------------------------------

if __name__ == "__main__":
    pop = resume_or_create(CONFIG_FILE, fitness_fn=evaluate)
    pop.run(verbosity=1, on_generation_end=save_plot)
