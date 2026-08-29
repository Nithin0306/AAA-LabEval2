# UVa 10171 — Meeting Prof. Miguel: Complexity Analysis Report

## Problem Summary

Two people start at different locations in a directed weighted city graph.
The young person can only use streets marked Y or YB; Prof. Miguel can only
use streets marked M or MB. Find the meeting point that minimises the sum
of their individual travel costs.

This is a **weighted shortest-path problem** on two independent directed
graphs (one per person), solved independently and then combined.

---

## Implementations

| Implementation | Algorithm | Data Structure | Complexity |
|---|---|---|---|
| `10171_1` | Floyd-Warshall | 26×26 adjacency matrix | O(V³) |
| `10171_2` | Dijkstra (min-heap) | Adjacency list | O((V+E) log V) |
| `10171_3` | Bellman-Ford | Edge list | O(V·E) |

### Algorithmic Complexity

| Implementation | Preprocessing | After solve |
|---|---|---|
| `10171_1` | O(V³) — fixed at 26³ = 17,576 ops | O(1) — matrix lookup |
| `10171_2` | O(E log V) — proportional to edges | O(1) after Dijkstra |
| `10171_3` | O(V·E) — slowest on dense graphs | O(1) after Bellman-Ford |

---

## Parameters

| Parameter | Role |
|---|---|
| V | Dominates Floyd-Warshall (cubic); low effect on Dijkstra and Bellman-Ford here |
| E | Dominates Dijkstra (E log V) and Bellman-Ford (V·E) |
| Graph type | Directed vs bidirectional affects total edge count |

---

## Experimental Setup

- 50 instances batched per measurement to amplify timing differences
  (individual instance timings are sub-millisecond at this scale)
- Each data point is the **median of 5 runs**
- V and E swept independently to isolate their individual effects

---

## Graph 1 — Number of Streets E vs Execution Time

> Parameters: V = 20, 50 batched instances

![E vs Time](../analysis/results/10171/e_vs_time.png)

**Measured data (ms, 50 instances):**

| E | Impl 1 (Floyd-Warshall) | Impl 2 (Dijkstra) | Impl 3 (Bellman-Ford) |
|---|---|---|---|
| 5 | 2.39 | 1.59 | 1.28 |
| 40 | 2.59 | 1.70 | 1.41 |
| 100 | 3.06 | 2.31 | 1.95 |
| 200 | 3.37 | 2.58 | 2.31 |

**Observations:**

- `10171_1` (Floyd-Warshall) rises slowly — it always performs V³ = 17,576
  operations regardless of E. Its overhead comes from the dense matrix
  initialisation and three nested loops.
- `10171_2` (Dijkstra) grows with E because the priority queue processes more
  edges. Efficient on sparse graphs, less so as E approaches V².
- `10171_3` (Bellman-Ford) is the most E-sensitive — its O(V·E) inner loop
  iterates over all edges V−1 times. The early-termination optimisation
  limits this in practice.

---

## Graph 2 — Number of Locations V vs Execution Time

> Parameters: E = 3V, 50 batched instances

![V vs Time](../analysis/results/10171/v_vs_time.png)

**Measured data (ms, 50 instances):**

| V | Impl 1 (Floyd-Warshall) | Impl 2 (Dijkstra) | Impl 3 (Bellman-Ford) |
|---|---|---|---|
| 4 | 2.40 | 1.43 | 1.50 |
| 10 | 2.91 | 1.45 | 1.55 |
| 18 | 2.87 | 1.48 | 1.70 |
| 26 | 2.86 | 1.84 | 1.75 |

**Observations:**

- Floyd-Warshall grows with V but its cubic cost is bounded — at V=26 the
  cost is 17,576 operations, which is small in absolute terms.
- Dijkstra and Bellman-Ford grow more slowly with V here because E = 3V
  keeps the graph sparse. Their advantage is most visible on sparse graphs.

---

## Graph 3 — Number of Streets E vs Peak Memory

> Parameters: V = 20, 20 batched instances

![E vs Memory](../analysis/results/10171/e_vs_memory.png)

**Measured data (KB):**

| E | Impl 1 (Floyd-Warshall) | Impl 2 (Dijkstra) | Impl 3 (Bellman-Ford) |
|---|---|---|---|
| 5 | 3,780 | 3,868 | 3,776 |
| 50 | 3,868 | 3,896 | 3,780 |
| 200 | 3,820 | 3,784 | 3,980 |

**Observations:**

- All three implementations show nearly flat memory usage because V is
  capped at 26. The process baseline (~3.8 MB) dominates.
- `10171_1` uses a fixed 26×26 matrix — memory is **constant** regardless
  of E.
- `10171_2` stores adjacency lists and `10171_3` stores an edge list — both
  grow linearly with E, but the growth is negligible relative to process
  overhead at this problem scale.

---

## Implementation Choice Implications

**Choose `10171_1` (Floyd-Warshall)** when V is small and fixed and you want
all-pairs shortest paths. The O(V³) is negligible at V ≤ 26; the matrix
representation makes lookups O(1).

**Choose `10171_2` (Dijkstra)** when the graph is sparse (E ≪ V²). Requires
non-negative edge weights. Most efficient as E grows on sparse graphs.

**Choose `10171_3` (Bellman-Ford)** when negative edge weights are possible
(the problem uses non-negative costs but Bellman-Ford handles the general
case). The early-termination optimisation makes it competitive with Dijkstra
when graphs are sparse and many edges relax quickly.
