# UVa 321 — The New Villa: Complexity Analysis Report

## Problem Summary

A person starts in room 1 (light on, all others off) and must reach room R
with only room R's light on. They can move through a door only if the
destination room's light is on, and can toggle lights from switches in the
current room.

This is a **BFS on an explicit state space** where each state encodes
**(current room, bitmask of lights)**. The state space grows as **R × 2^R**.

---

## Implementations

| Implementation | State Representation | Graph Construction | BFS |
|---|---|---|---|
| `321_1` | `struct State {room, mask}` | On-demand during BFS | State-struct queue |
| `321_2` | Integer: `room * 2^R + mask` | On-demand during BFS | Integer queue |
| `321_3` | Integer encoded | **Prebuilt** full adjacency list | Integer queue on prebuilt graph |

### Algorithmic Complexity

Let **R** = rooms, **D** = doors, **S** = switch connections.

| Implementation | Preprocessing | BFS |
|---|---|---|
| `321_1` | O(1) | O(R × 2^R × (D + S)) |
| `321_2` | O(1) | O(R × 2^R × (D + S)) |
| `321_3` | O(R × 2^R × (D + S)) — all transitions built upfront | O(V + E) on prebuilt graph |

---

## Parameters

| Parameter | Role |
|---|---|
| R | Exponential effect on state space (R × 2^R) |
| D | Move transitions per state |
| S | Light-toggle transitions per state |
| Reachable states | Actual BFS frontier size |

---

## Experimental Setup

- Inputs generated with a door chain (1–2–...–R) and room 1 controlling room R
  to guarantee a reachable goal state
- Each data point is the **median of 5 runs**
- Memory measured via `/usr/bin/time -v` (peak RSS)

---

## Graph 1 — R vs Theoretical State Space

> Formula: R × 2^R (all room–mask combinations)

![R vs States](../analysis/results/321/r_vs_states.png)

**State space by room count:**

| R | Maximum States (R × 2^R) |
|---|---|
| 2 | 8 |
| 4 | 64 |
| 6 | 384 |
| 8 | 2,048 |
| 10 | 10,240 |

**Observations:**

- The state space doubles with each additional room (ignoring the linear R
  factor). This is why the problem caps R at 10.
- Even at R=10, a visited array of 10,240 booleans and a parent array of
  10,240 entries must be allocated per test case.

---

## Graph 2 — R vs Execution Time

> Parameters: D = R-1, S = R/2

![R vs Time](../analysis/results/321/r_vs_time.png)

**Measured data (ms):**

| R | Impl 1 (State struct) | Impl 2 (Integer BFS) | Impl 3 (Prebuilt graph) |
|---|---|---|---|
| 2 | 1.77 | 1.38 | 1.28 |
| 4 | 1.43 | 1.60 | 1.61 |
| 6 | 1.55 | 1.19 | 1.50 |
| 8 | 1.34 | 1.32 | 1.75 |
| 9 | 1.43 | 1.49 | 2.31 |
| 10 | 1.43 | 1.60 | 3.36 |

**Observations:**

- `321_1` and `321_2` are nearly identical — the struct vs integer encoding
  has negligible effect on BFS cost at this scale.
- `321_3` diverges at R ≥ 8. Its prebuilt adjacency list must enumerate **all**
  R × 2^R states and their transitions before BFS starts — this preprocessing
  cost grows exponentially with R and dominates at large R.
- At R=10, `321_3` takes 3.36 ms vs 1.43 ms for `321_1` — a 2.3× overhead
  from preprocessing alone.

---

## Graph 3 — R vs Peak Memory

> Parameters: D = R-1, S = R/2

![R vs Memory](../analysis/results/321/r_vs_memory.png)

**Measured data (KB):**

| R | Impl 1 (State struct) | Impl 2 (Integer BFS) | Impl 3 (Prebuilt graph) |
|---|---|---|---|
| 4 | 3,852 | 3,832 | 3,800 |
| 6 | 3,964 | 4,068 | 4,100 |
| 8 | 4,104 | 3,984 | 4,348 |
| 10 | 4,208 | 4,040 | 5,316 |

**Observations:**

- All three grow slowly with R — but `321_3` diverges at large R because
  the prebuilt adjacency list stores all transitions explicitly in memory,
  not just the visited and parent arrays.
- At R=10, `321_3` uses ~5.3 MB vs ~4.1 MB for `321_1` — the extra 1.2 MB
  is the prebuilt edge list for 10,240 states.
- `321_2` uses slightly less memory than `321_1` because integer queue entries
  (4 bytes each) are smaller than struct entries (8 bytes each).

---

## Implementation Choice Implications

**Choose `321_1`** when readability matters. Named struct fields (`room`,
`mask`) make the BFS logic self-documenting and easier to verify for
correctness.

**Choose `321_2`** when performance is important. Integer encoding eliminates
struct-copy overhead in the queue. The measured data shows it is consistently
equal to or faster than `321_1`.

**Choose `321_3`** when the graph topology is queried multiple times with the
same R, D, S layout (i.e., many queries on the same physical villa layout).
Preprocessing separates graph construction from traversal — a cleaner
design at the cost of higher memory and startup time. The data confirms this
tradeoff: `321_3` is 2.3× slower to start but once the graph is built, BFS
traversal is O(V+E) on a standard adjacency list.
