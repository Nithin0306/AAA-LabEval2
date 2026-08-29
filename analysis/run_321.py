"""
run_321.py — Benchmark runner for UVa 321 (The New Villa).

Sweeps:
  Graph 1 : R (rooms) vs Number of Reachable States  [theoretical + measured]
  Graph 2 : R vs Total Execution Time
  Graph 3 : R vs Peak Memory
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from benchmark import run_impl_repeated
from generate_inputs import gen_321
from plot import save_line_chart, save_csv

BASE = os.path.dirname(os.path.dirname(__file__))
VILLA_DIR = os.path.join(BASE, "The_New_Villa")
RESULTS = os.path.join(BASE, "analysis", "results", "321")

BINARIES = {
    "Impl 1 (State struct BFS)":      os.path.join(VILLA_DIR, "321_1"),
    "Impl 2 (Integer-encoded BFS)":   os.path.join(VILLA_DIR, "321_2"),
    "Impl 3 (Prebuilt state graph)":  os.path.join(VILLA_DIR, "321_3"),
}

REPS = 5

R_VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10]


def ensure_built():
    for label, binary in BINARIES.items():
        if not os.path.isfile(binary):
            src = binary + ".cpp"
            print(f"Building {src} ...")
            os.system(f"g++ -std=c++17 -O2 -o {binary} {src}")


def theoretical_states(R: int) -> int:
    """Upper bound on BFS state space: R rooms × 2^R light configurations."""
    return R * (2 ** R)


def sweep_r_vs_states():
    """
    Graph 1: R vs number of reachable states (theoretical upper bound).
    This is deterministic — no need to run binaries.
    """
    print("\n[Graph 1] R vs Theoretical State Space")

    states = [theoretical_states(R) for R in R_VALUES]

    for R, s in zip(R_VALUES, states):
        print(f"  R={R:2d}  States = {s}")

    save_csv(
        [[R, theoretical_states(R)] for R in R_VALUES],
        ["R", "max_states"],
        os.path.join(RESULTS, "r_vs_states.csv"),
    )
    save_line_chart(
        R_VALUES,
        {"R × 2^R": states},
        x_label="Number of Rooms (R)",
        y_label="Maximum States (R × 2^R)",
        title="UVa 321 — R vs State Space Size\n(Theoretical Upper Bound)",
        output_path=os.path.join(RESULTS, "r_vs_states.png"),
        y_log=True,
    )


def sweep_r_vs_time():
    """Graph 2: R vs execution time."""
    print("\n[Graph 2] R vs Execution Time")

    y_series = {label: [] for label in BINARIES}
    csv_rows = []

    for R in R_VALUES:
        D = R - 1
        S = max(1, R // 2)
        inp = gen_321(R, D, S, seed=42)
        row = [R]
        for label, binary in BINARIES.items():
            result = run_impl_repeated(binary, inp, reps=REPS)
            t = result["time_ms"]
            y_series[label].append(t)
            row.append(round(t, 4))
            print(f"  R={R:2d}  {label}: {t:.4f} ms")
        csv_rows.append(row)

    save_csv(
        csv_rows,
        ["R"] + list(BINARIES.keys()),
        os.path.join(RESULTS, "r_vs_time.csv"),
    )
    save_line_chart(
        R_VALUES, y_series,
        x_label="Number of Rooms (R)",
        y_label="Time (ms)",
        title="UVa 321 — R vs Execution Time\n(D = R-1, S = R/2)",
        output_path=os.path.join(RESULTS, "r_vs_time.png"),
    )


def sweep_r_vs_memory():
    """Graph 3: R vs peak memory."""
    print("\n[Graph 3] R vs Peak Memory")

    y_series = {label: [] for label in BINARIES}
    csv_rows = []

    for R in R_VALUES:
        D = R - 1
        S = max(1, R // 2)
        inp = gen_321(R, D, S, seed=42)
        row = [R]
        for label, binary in BINARIES.items():
            result = run_impl_repeated(binary, inp, reps=3)
            m = result["memory_kb"]
            y_series[label].append(m)
            row.append(m)
            print(f"  R={R:2d}  {label}: {m} KB")
        csv_rows.append(row)

    save_csv(
        csv_rows,
        ["R"] + list(BINARIES.keys()),
        os.path.join(RESULTS, "r_vs_memory.csv"),
    )
    save_line_chart(
        R_VALUES, y_series,
        x_label="Number of Rooms (R)",
        y_label="Peak Memory (KB)",
        title="UVa 321 — R vs Peak Memory\n(D = R-1, S = R/2)",
        output_path=os.path.join(RESULTS, "r_vs_memory.png"),
    )


if __name__ == "__main__":
    ensure_built()
    sweep_r_vs_states()
    sweep_r_vs_time()
    sweep_r_vs_memory()
    print("\nDone. Results in analysis/results/321/")
