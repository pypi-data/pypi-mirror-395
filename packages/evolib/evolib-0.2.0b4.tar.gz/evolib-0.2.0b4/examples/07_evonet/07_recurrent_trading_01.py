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
from matplotlib.ticker import FormatStrFormatter

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

FRAME_FOLDER = "07_frames"
CONFIG_FILE = "./configs/07_recurrent_trading.yaml"

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


    """Evaluate an individual using trading-like stepwise profit and accuracy."""
    net = indiv.para["brain"].net

    total_profit = 0.0
    total_correct = 0
    total_samples = 0

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

        position = 0.0

        for t in range(WARMUP_STEPS + 1, len(input_seq)):
            price_prev = input_seq[t - 1]
            price_now = input_seq[t]

            # Prediction auf Basis des vorherigen Preises
            output = net.calc([price_prev])
            pred_class = int(np.argmax(output))
            signal = class_pos[pred_class]

            # Accuracy (nur Zusatzmetrik)
            if t < len(labels) and pred_class == labels[t]:
                total_correct += 1

            # Trading-Logik
            if position == 0.0 and signal != 0.0:
                position = signal
            elif position != 0.0:
                if np.sign(signal) != np.sign(position) and signal != 0.0:
                    position = signal  # direktes Umschalten
                elif signal == 0.0:
                    position = 0.0  # Position schließen

            # Schrittweises Profit-Update
            pnl = position * (price_now - price_prev)
            total_profit += pnl
            total_samples += 1

    accuracy = total_correct / max(1, total_samples)
    avg_profit = total_profit / max(1, EVAL_RUNS)

    indiv.fitness = -avg_profit  # Minimierung
    indiv.extra_metrics["accuracy"] = accuracy
    indiv.extra_metrics["profit"] = avg_profit

    return indiv.fitness


# --- Visualization -----------------------------------------------------------


def save_plot(pop: Population) -> None:
    """Plot series with trades and continuous equity curve (single test run)."""
    best = pop.best()
    net = best.para["brain"].net

    # --- Neuer Run (einzelner Seed, gleiche Datenquelle wie evaluate) ---
    seed = 42 #np.random.randint(0, 2**32 - 1)
    full_seq = generate_timeseries(SEQ_LEN + PRED_LEN, pattern=PATTERN, seed=seed)
    input_seq = full_seq[:-PRED_LEN]
    labels = make_labels(input_seq, PRED_LEN)

    net.reset(full=True)
    class_pos = [-1.0, -0.5, 0.0, 0.5, 1.0]

    equity = [0.0]
    trades = []
    position = 0.0
    total_profit = 0.0
    total_correct = 0
    total_samples = 0

    # Warmup
    for val in input_seq[:WARMUP_STEPS]:
        net.calc([val])

    # Schrittweise Berechnung
    for t in range(WARMUP_STEPS + 1, len(input_seq)):
        price_prev = input_seq[t - 1]
        price_now = input_seq[t]

        # Prediction (auf Basis des vorherigen Preises)
        output = net.calc([price_prev])
        pred_class = int(np.argmax(output))
        signal = class_pos[pred_class]

        # Accuracy
        if t < len(labels) and pred_class == labels[t]:
            total_correct += 1
        total_samples += 1

        # Trading-Logik
        if position == 0.0 and signal != 0.0:
            position = signal
            trades.append((t, price_now, "open", signal))
        elif position != 0.0:
            if np.sign(signal) != np.sign(position) and signal != 0.0:
                trades.append((t, price_now, "close+open", signal))
                position = signal
            elif signal == 0.0:
                trades.append((t, price_now, "close", 0.0))
                position = 0.0

        # Equity-Update = Positionsgröße × Preisänderung
        pnl = position * (price_now - price_prev)
        total_profit += pnl
        equity.append(equity[-1] + pnl)

    # Kennzahlen für diesen Plot
    acc = total_correct / max(1, total_samples)
    prof = total_profit

    # --- Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True,
                                   gridspec_kw={"height_ratios": [2, 1]})

    # Zeitreihe
    ax1.plot(input_seq, color="black", linewidth=1.5)
    for t, price, action, signal in trades:
        if "open" in action:
            ax1.scatter(t, price,
                        color="green" if signal > 0 else "red",
                        s=80, marker="^",
                        label="Long open" if signal > 0 else "Short open")
        elif "close" in action:
            ax1.scatter(t, price, color="blue", s=80, marker="v", label="Close")

    ax1.set_title(f"Trading Strategy (Acc={acc:.2f}, Profit={prof:.3f})")

    # Legende einmalig
    handles, labels = ax1.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax1.legend(by_label.values(), by_label.keys(), loc="upper right")

    # Equity-Kurve
    ax2.plot(equity, color="blue", linewidth=1.5, label="Equity")
    ax2.set_ylabel("Equity")
    ax2.set_xlabel("Time")
    ax2.legend(loc="upper left")
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%1.2f'))
    # add threshold line at 0.5
    ax2.axhline(0.0, color="gray", linestyle="--", linewidth=1, alpha=0.6)

    plt.tight_layout()
    plt.savefig(f"{FRAME_FOLDER}/gen_{pop.generation_num:03d}.png", dpi=300)
    plt.close()


# --- Main loop ---------------------------------------------------------------

if __name__ == "__main__":
    pop = resume_or_create(CONFIG_FILE, fitness_fn=evaluate)
    pop.run(verbosity=1, on_generation_end=save_plot)
