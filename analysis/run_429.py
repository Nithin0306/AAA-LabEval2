"""
run_429.py — Benchmark runner for UVa 429 (Word Transformation).

Sweeps:
  Graph 1 : V (dictionary size) vs Total Time
  Graph 2 : Q (queries) vs Total Time
  Graph 3 : V vs Total Time (preprocessing proxy — single query)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from benchmark import run_impl_repeated
from generate_inputs import gen_429, gen_429_multiquery
from plot import save_line_chart, save_csv

BASE = os.path.dirname(os.path.dirname(__file__))
WORD_DIR = os.path.join(BASE, "Word_Transformation")
RESULTS = os.path.join(BASE, "analysis", "results", "429")

BINARIES = {
    "Impl 1 (On-the-fly BFS)": os.path.join(WORD_DIR, "429_1"),
    "Impl 2 (Adjacency list)": os.path.join(WORD_DIR, "429_2"),
    "Impl 3 (Pattern map)":    os.path.join(WORD_DIR, "429_3"),
}

REPS = 5


def ensure_built():
    for label, binary in BINARIES.items():
        if not os.path.isfile(binary):
            src = binary + ".cpp"
            print(f"Building {src} ...")
            os.system(f"g++ -std=c++17 -O2 -o {binary} {src}")


def sweep_v_vs_time():
    """Graph 1: Dictionary size V vs total execution time."""
    V_values = [10, 20, 40, 60, 80, 100, 130, 160, 200]
    L, Q = 4, 10
    print("\n[Graph 1] V vs Total Time")

    y_series = {label: [] for label in BINARIES}
    csv_rows = []

    for V in V_values:
        inp = gen_429(V, L, Q, seed=7)
        row = [V]
        for label, binary in BINARIES.items():
            result = run_impl_repeated(binary, inp, reps=REPS)
            t = result["time_ms"]
            y_series[label].append(t)
            row.append(round(t, 4))
            print(f"  V={V:3d}  {label}: {t:.4f} ms")
        csv_rows.append(row)

    save_csv(
        csv_rows,
        ["V"] + list(BINARIES.keys()),
        os.path.join(RESULTS, "v_vs_time.csv"),
    )
    save_line_chart(
        V_values, y_series,
        x_label="Dictionary Size (V)",
        y_label="Time (ms)",
        title="UVa 429 — V vs Execution Time\n(L=4, Q=10)",
        output_path=os.path.join(RESULTS, "v_vs_time.png"),
    )


def sweep_q_vs_time():
    """Graph 2: Number of queries Q vs total execution time."""
    Q_values = [1, 5, 10, 20, 40, 80, 120, 160, 200]
    V, L = 100, 4
    print("\n[Graph 2] Q vs Total Time")

    inputs = gen_429_multiquery(V, L, Q_values, seed=13)
    y_series = {label: [] for label in BINARIES}
    csv_rows = []

    for Q, inp in zip(Q_values, inputs):
        row = [Q]
        for label, binary in BINARIES.items():
            result = run_impl_repeated(binary, inp, reps=REPS)
            t = result["time_ms"]
            y_series[label].append(t)
            row.append(round(t, 4))
            print(f"  Q={Q:3d}  {label}: {t:.4f} ms")
        csv_rows.append(row)

    save_csv(
        csv_rows,
        ["Q"] + list(BINARIES.keys()),
        os.path.join(RESULTS, "q_vs_time.csv"),
    )
    save_line_chart(
        Q_values, y_series,
        x_label="Number of Queries (Q)",
        y_label="Time (ms)",
        title="UVa 429 — Q vs Execution Time\n(V=100, L=4)",
        output_path=os.path.join(RESULTS, "q_vs_time.png"),
    )


def sweep_v_vs_preptime():
    """
    Graph 3: V vs preprocessing time proxy.
    Single query (Q=1) so search time is minimal.
    The delta between impls reflects their construction overhead.
    """
    V_values = [10, 20, 40, 60, 80, 100, 130, 160, 200]
    L, Q = 4, 1
    print("\n[Graph 3] V vs Preprocessing Time (Q=1 proxy)")

    y_series = {label: [] for label in BINARIES}
    csv_rows = []

    for V in V_values:
        inp = gen_429(V, L, Q, seed=99)
        row = [V]
        for label, binary in BINARIES.items():
            result = run_impl_repeated(binary, inp, reps=REPS)
            t = result["time_ms"]
            y_series[label].append(t)
            row.append(round(t, 4))
            print(f"  V={V:3d}  {label}: {t:.4f} ms")
        csv_rows.append(row)

    save_csv(
        csv_rows,
        ["V"] + list(BINARIES.keys()),
        os.path.join(RESULTS, "v_vs_preptime.csv"),
    )
    save_line_chart(
        V_values, y_series,
        x_label="Dictionary Size (V)",
        y_label="Time (ms)",
        title="UVa 429 — V vs Preprocessing Time Proxy\n(L=4, Q=1)",
        output_path=os.path.join(RESULTS, "v_vs_preptime.png"),
    )


if __name__ == "__main__":
    ensure_built()
    sweep_v_vs_time()
    sweep_q_vs_time()
    sweep_v_vs_preptime()
    print("\nDone. Results in analysis/results/429/")
