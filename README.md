# Graph Algorithms & Problem Solving — Academic Assignment

This repository contains implementations, test suites, and empirical complexity analysis for three graph algorithm problems selected across different graph paradigms:

1. **Unweighted Graph Problem:** UVa 429 — Word Transformation
2. **Weighted Graph Problem:** UVa 10171 — Meeting Prof. Miguel
3. **Implicit Graph / State Mapping Problem:** UVa 321 — The New Villa

Each problem includes **three distinct C++ implementation strategies**, automated evaluation against test cases via `Makefile`, and a detailed performance & complexity analysis report supported by benchmark experiments.

---

## 📁 Repository Structure

```text
├── docs/                      # Original PDF problem statements
│   ├── p429.pdf
│   ├── p10171.pdf
│   └── p321.pdf
├── Word_Transformation/       # Problem 1: Unweighted Graphs
│   ├── 429_1.cpp              # Impl 1: On-the-fly pairwise scan + BFS
│   ├── 429_2.cpp              # Impl 2: Prebuilt adjacency list + BFS
│   ├── 429_3.cpp              # Impl 3: Wildcard pattern map + BFS
│   ├── Makefile               # Automated build & test execution
│   ├── test_case_1..3.txt     # Input test cases
│   ├── expected_output_1..3.txt
│   └── report.md              # Empirical & theoretical complexity report
├── Meeting_Prof_Miguel/       # Problem 2: Weighted Graphs
│   ├── 10171_1.cpp            # Impl 1: Floyd-Warshall (All-Pairs Shortest Path)
│   ├── 10171_2.cpp            # Impl 2: Dijkstra's Algorithm (Min-Heap)
│   ├── 10171_3.cpp            # Impl 3: Bellman-Ford Algorithm
│   ├── Makefile
│   ├── test_case_1..3.txt
│   ├── expected_output_1..3.txt
│   └── report.md
├── The_New_Villa/             # Problem 3: Mapping to Graphs (Implicit State-Space)
│   ├── 321_1.cpp              # Impl 1: On-demand BFS with State Struct
│   ├── 321_2.cpp              # Impl 2: On-demand BFS with Bitmask Integer Encoding
│   ├── 321_3.cpp              # Impl 3: Prebuilt Full State Graph + BFS
│   ├── Makefile
│   ├── test_case_1..3.txt
│   ├── expected_output_1..3.txt
│   └── report.md
└── analysis/                  # Modular Python benchmarking & plotting suite
    ├── benchmark.py           # Timing & RSS memory measurement module
    ├── generate_inputs.py     # Controlled test input generators
    ├── plot.py                # Graph plotting utilities
    ├── run_429.py             # Sweep runner for UVa 429
    ├── run_10171.py           # Sweep runner for UVa 10171
    ├── run_321.py             # Sweep runner for UVa 321
    └── run_all.py             # Master script to execute all benchmarks
```

---

## 📌 Problems & Reports

### 1. UVa 429 — Word Transformation (Unweighted Graph)
- **Problem Statement:** [`docs/p429.pdf`](docs/p429.pdf)
- **Detailed Analysis & Graphs:** [`Word_Transformation/report.md`](Word_Transformation/report.md)
- **Overview:** Find the shortest sequence of single-character word modifications to reach a target word using BFS.
- **Implementations:**
  - `429_1.cpp`: On-the-fly $O(V \cdot L)$ pairwise scan per step. Total: $O(Q \cdot V^2 \cdot L)$.
  - `429_2.cpp`: $O(V^2 \cdot L)$ prebuilt adjacency list representation. Total: $O(V^2 \cdot L + Q \cdot (V + E))$.
  - `429_3.cpp`: Wildcard pattern map lookup (`h*t -> hot`). Total: $O(V \cdot L + Q \cdot (V \cdot L + E))$.
- **Empirical Results:**
  - As query volume $Q$ increases to 200, `429_1` scales linearly up to **47.07 ms**, whereas `429_2` amortises graph construction to stay virtually flat (**3.90 ms**), and `429_3` grows moderately to **9.05 ms**.
  - `429_3` is the preferred choice for large dictionaries ($V$) because wildcard map construction ($O(V \cdot L)$) avoids the expensive $O(V^2)$ all-pairs pairwise comparison step required by `429_2`.

### 2. UVa 10171 — Meeting Prof. Miguel (Weighted Graph)
- **Problem Statement:** [`docs/p10171.pdf`](docs/p10171.pdf)
- **Detailed Analysis & Graphs:** [`Meeting_Prof_Miguel/report.md`](Meeting_Prof_Miguel/report.md)
- **Overview:** Compute optimal meeting points minimizing combined travel costs on two independent weighted graphs (Young vs. Mature).
- **Implementations:**
  - `10171_1.cpp`: Floyd-Warshall algorithm ($O(V^3)$).
  - `10171_2.cpp`: Dijkstra's algorithm with priority queue ($O((V + E) \log V)$).
  - `10171_3.cpp`: Bellman-Ford algorithm with early termination ($O(V \cdot E)$).
- **Empirical Results:**
  - On sparse graphs ($E=5$), Dijkstra (**3.77 ms**) and Bellman-Ford with early termination (**3.84 ms**) outperform Floyd-Warshall (**5.74 ms** across 50 instances) because Floyd-Warshall always runs $V^3 = 17,576$ inner loop iterations regardless of edge density.

### 3. UVa 321 — The New Villa (Implicit Graph Mapping)
- **Problem Statement:** [`docs/p321.pdf`](docs/p321.pdf)
- **Detailed Analysis & Graphs:** [`The_New_Villa/report.md`](The_New_Villa/report.md)
- **Overview:** Navigate a house of rooms and light switches, mapping the state space $(room, light\_mask)$ of size $R \times 2^R$ to a shortest-path graph problem.
- **Implementations:**
  - `321_1.cpp`: On-demand BFS using explicit `State` structs.
  - `321_2.cpp`: On-demand BFS using compact integer state encoding (`room * 2^R + mask`).
  - `321_3.cpp`: Prebuilt full explicit state-space adjacency graph prior to BFS traversal.
- **Empirical Results:**
  - At $R=10$ (10,240 potential states), `321_3` takes **7.90 ms** and **5.31 MB** RSS memory due to constructing edges for all states upfront, compared to `321_1` (**3.62 ms**, **4.09 MB**) which explores only reachable states on-demand.

---

## 🛠️ How to Build and Run Implementations

Each problem folder contains a `Makefile` that compiles all three C++ implementations and evaluates them against the test suite (`test_case_1..3.txt` vs `expected_output_1..3.txt`).

### Running Problem 1 (Word Transformation)
```bash
cd Word_Transformation

# Run all 3 implementations against test cases
make run

# Compile specific implementation
make 429_1
make 429_2
make 429_3

# Clean binary executables
make clean
```

### Running Problem 2 (Meeting Prof. Miguel)
```bash
cd Meeting_Prof_Miguel

# Run all 3 implementations against test cases
make run

# Compile specific implementation
make 10171_1
make 10171_2
make 10171_3

# Clean binary executables
make clean
```

### Running Problem 3 (The New Villa)
```bash
cd The_New_Villa

# Run all 3 implementations against test cases
make run

# Compile specific implementation
make 321_1
make 321_2
make 321_3

# Clean binary executables
make clean
```

---

## 📊 Running Empirical Benchmarks & Generating Plots

The `analysis/` directory contains an automated benchmarking framework written in Python that measures wall-clock time and peak resident set size (RSS memory) across controlled parameter sweeps.

To execute all benchmarks and regenerate plots & CSV dataset tables:

```bash
python3 analysis/run_all.py
```

Or run benchmarks for an individual problem:
```bash
python3 analysis/run_429.py
python3 analysis/run_10171.py
python3 analysis/run_321.py
```
