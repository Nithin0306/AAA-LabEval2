"""
plot.py — Reusable plotting functions for all three problems.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

COLORS = ["#4C9BE8", "#E8854C", "#4CE8A0"]
MARKERS = ["o", "s", "^"]
LINEWIDTH = 2.0
MARKERSIZE = 7
FONT_FAMILY = "DejaVu Sans"

plt.rcParams.update({
    "font.family": FONT_FAMILY,
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "legend.fontsize": 10,
    "figure.dpi": 120,
    "axes.grid": True,
    "grid.alpha": 0.35,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def save_line_chart(
    x_values: list,
    y_series: dict,
    x_label: str,
    y_label: str,
    title: str,
    output_path: str,
    x_log: bool = False,
    y_log: bool = False,
):
    """
    Plot multiple series on a single line chart.

    Args:
        x_values : shared x-axis values
        y_series : { label: [y0, y1, ...] }
        x_label  : x-axis label
        y_label  : y-axis label
        title    : chart title
        output_path : file path to save (.png)
        x_log / y_log : log scale toggles
    """
    fig, ax = plt.subplots(figsize=(7, 4.5))

    for idx, (label, y_vals) in enumerate(y_series.items()):
        color = COLORS[idx % len(COLORS)]
        marker = MARKERS[idx % len(MARKERS)]
        ax.plot(
            x_values, y_vals,
            label=label,
            color=color,
            marker=marker,
            linewidth=LINEWIDTH,
            markersize=MARKERSIZE,
        )

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()

    if x_log:
        ax.set_xscale("log")
    if y_log:
        ax.set_yscale("log")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"  Saved: {output_path}")


def save_bar_chart(
    categories: list,
    y_series: dict,
    x_label: str,
    y_label: str,
    title: str,
    output_path: str,
):
    """
    Grouped bar chart for categorical comparisons.
    """
    n_groups = len(categories)
    n_series = len(y_series)
    width = 0.8 / n_series
    x = np.arange(n_groups)

    fig, ax = plt.subplots(figsize=(7, 4.5))

    for idx, (label, y_vals) in enumerate(y_series.items()):
        offset = (idx - n_series / 2 + 0.5) * width
        ax.bar(
            x + offset, y_vals,
            width=width,
            label=label,
            color=COLORS[idx % len(COLORS)],
            alpha=0.85,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"  Saved: {output_path}")


def save_csv(rows: list, header: list, output_path: str):
    """Write benchmark results as a CSV file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(",".join(header) + "\n")
        for row in rows:
            f.write(",".join(str(v) for v in row) + "\n")
    print(f"  Saved: {output_path}")
