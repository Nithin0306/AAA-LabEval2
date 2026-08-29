"""
run_10171.py — Benchmark runner for UVa 10171 (Meeting Prof. Miguel).

Sweeps:
  Graph 1 : E (streets) vs Total Time
  Graph 2 : V (locations) vs Total Time
  Graph 3 : E vs Memory Usage
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from benchmark import run_impl_repeated
from generate_inputs import gen_10171
from plot import save_line_chart, save_csv

BASE = os.path.dirname(os.path.dirname(__file__))
MPM_DIR = os.path.join(BASE, "Meeting_Prof_Miguel")
RESULTS = os.path.join(BASE, "analysis", "results", "10171")

BINARIES = {
    "Impl 1 (Floyd-Warshall)": os.path.join(MPM_DIR, "10171_1"),
    "Impl 2 (Dijkstra)":       os.path.join(MPM_DIR, "10171_2"),
    "Impl 3 (Bellman-Ford)":   os.path.join(MPM_DIR, "10171_3"),
}

REPS = 5


def ensure_built():
    for label, binary in BINARIES.items():
        if not os.path.isfile(binary):
            src = binary + ".cpp"
            print(f"Building {src} ...")
            os.system(f"g++ -std=c++17 -O2 -o {binary} {src}")


def _batch_input(instances: list) -> str:
    """Combine multiple instances into one stdin stream (terminate with '0')."""
    parts = []
    for inp in instances:
        lines = inp.strip().splitlines()
        # Remove trailing "0" terminator from each and re-add at end
        non_zero = [l for l in lines if l.strip() != "0"]
        parts.extend(non_zero)
    parts.append("0")
    return "\n".join(parts)


def sweep_e_vs_time():
    """Graph 1: Number of edges E vs execution time (V fixed at 20)."""
    E_values = [5, 10, 20, 40, 60, 80, 100, 150, 200]
    V = 20
    BATCH = 50
    print("\n[Graph 1] E vs Total Time")

    y_series = {label: [] for label in BINARIES}
    csv_rows = []

    for E in E_values:
        instances = [gen_10171(V, E, seed=i) for i in range(BATCH)]
        inp = _batch_input(instances)
        row = [E]
        for label, binary in BINARIES.items():
            result = run_impl_repeated(binary, inp, reps=REPS)
            t = result["time_ms"]
            y_series[label].append(t)
            row.append(round(t, 4))
            print(f"  E={E:3d}  {label}: {t:.4f} ms")
        csv_rows.append(row)

    save_csv(
        csv_rows,
        ["E"] + list(BINARIES.keys()),
        os.path.join(RESULTS, "e_vs_time.csv"),
    )
    save_line_chart(
        E_values, y_series,
        x_label="Number of Streets (E)",
        y_label="Time (ms)",
        title="UVa 10171 — E vs Execution Time\n(V=20, 50 batched instances)",
        output_path=os.path.join(RESULTS, "e_vs_time.png"),
    )


def sweep_v_vs_time():
    """Graph 2: Number of locations V vs execution time (E proportional to V)."""
    V_values = [4, 6, 8, 10, 14, 18, 22, 26]
    BATCH = 50
    print("\n[Graph 2] V vs Total Time")

    y_series = {label: [] for label in BINARIES}
    csv_rows = []

    for V in V_values:
        E = V * 3
        instances = [gen_10171(V, E, seed=i + 100) for i in range(BATCH)]
        inp = _batch_input(instances)
        row = [V]
        for label, binary in BINARIES.items():
            result = run_impl_repeated(binary, inp, reps=REPS)
            t = result["time_ms"]
            y_series[label].append(t)
            row.append(round(t, 4))
            print(f"  V={V:2d}  {label}: {t:.4f} ms")
        csv_rows.append(row)

    save_csv(
        csv_rows,
        ["V"] + list(BINARIES.keys()),
        os.path.join(RESULTS, "v_vs_time.csv"),
    )
    save_line_chart(
        V_values, y_series,
        x_label="Number of Locations (V)",
        y_label="Time (ms)",
        title="UVa 10171 — V vs Execution Time\n(E = 3V, 50 batched instances)",
        output_path=os.path.join(RESULTS, "v_vs_time.png"),
    )


def sweep_e_vs_memory():
    """Graph 3: E vs peak memory usage."""
    E_values = [5, 20, 50, 100, 200]
    V = 20
    BATCH = 20
    print("\n[Graph 3] E vs Memory")

    y_series = {label: [] for label in BINARIES}
    csv_rows = []

    for E in E_values:
        instances = [gen_10171(V, E, seed=i + 200) for i in range(BATCH)]
        inp = _batch_input(instances)
        row = [E]
        for label, binary in BINARIES.items():
            result = run_impl_repeated(binary, inp, reps=3)
            m = result["memory_kb"]
            y_series[label].append(m)
            row.append(m)
            print(f"  E={E:3d}  {label}: {m} KB")
        csv_rows.append(row)

    save_csv(
        csv_rows,
        ["E"] + list(BINARIES.keys()),
        os.path.join(RESULTS, "e_vs_memory.csv"),
    )
    save_line_chart(
        E_values, y_series,
        x_label="Number of Streets (E)",
        y_label="Peak Memory (KB)",
        title="UVa 10171 — E vs Peak Memory\n(V=20, 20 batched instances)",
        output_path=os.path.join(RESULTS, "e_vs_memory.png"),
    )


if __name__ == "__main__":
    ensure_built()
    sweep_e_vs_time()
    sweep_v_vs_time()
    sweep_e_vs_memory()
    print("\nDone. Results in analysis/results/10171/")
