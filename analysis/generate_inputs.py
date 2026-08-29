"""
generate_inputs.py — Controlled input generators for all three problems.

UVa 429  — Word Transformation
UVa 10171 — Meeting Prof. Miguel
UVa 321  — The New Villa
"""

import random
import string
from itertools import combinations


def gen_429(V: int, L: int = 4, Q: int = 5, seed: int = 42) -> str:
    """
    Generate a UVa 429 input with V words of length L and Q queries.
    Guarantees at least a path by constructing a chain then adding random words.
    """
    rng = random.Random(seed)
    alphabet = string.ascii_lowercase

    def random_word():
        return "".join(rng.choice(alphabet) for _ in range(L))

    words = set()

    # Seed a chain: each word differs from previous by one letter
    chain = [random_word()]
    while len(chain) < max(V // 2, 2):
        prev = list(chain[-1])
        pos = rng.randrange(L)
        candidates = [c for c in alphabet if c != prev[pos]]
        prev[pos] = rng.choice(candidates)
        word = "".join(prev)
        chain.append(word)
        words.add(word)

    for w in chain:
        words.add(w)

    # Fill remaining slots with random words
    attempts = 0
    while len(words) < V and attempts < V * 20:
        words.add(random_word())
        attempts += 1

    words = list(words)[:V]

    # Build queries from chain pairs that are guaranteed reachable
    queries = []
    for _ in range(Q):
        i, j = rng.sample(range(min(len(chain), len(words))), 2)
        queries.append(f"{chain[i]} {chain[j]}")

    lines = ["1", ""]
    lines += words
    lines.append("*")
    lines += queries
    lines.append("")
    return "\n".join(lines)


def gen_429_multiquery(V: int, L: int, Q_list: list, seed: int = 42) -> list:
    """Return list of input strings, one per Q value, same dictionary."""
    base = gen_429(V, L, Q_list[-1], seed)
    # Extract dictionary lines
    parts = base.split("\n")
    dict_end = parts.index("*")
    dict_lines = parts[2:dict_end]

    rng = random.Random(seed)
    results = []
    for Q in Q_list:
        chain_words = dict_lines[:max(2, len(dict_lines) // 2)]
        queries = []
        for _ in range(Q):
            if len(chain_words) >= 2:
                i, j = rng.sample(range(len(chain_words)), 2)
                queries.append(f"{chain_words[i]} {chain_words[j]}")
            else:
                queries.append(f"{dict_lines[0]} {dict_lines[0]}")
        lines = ["1", ""] + dict_lines + ["*"] + queries + [""]
        results.append("\n".join(lines))
    return results


def gen_10171(V: int, E: int, seed: int = 42) -> str:
    """
    Generate a UVa 10171 input with V locations (A..Z, V<=26) and E streets.
    Streets are split roughly equally between 'Y' (young) and 'M' (miguel).
    Direction is randomly U or B.
    """
    rng = random.Random(seed)
    V = min(V, 26)
    nodes = [chr(ord("A") + i) for i in range(V)]

    edges = []
    for _ in range(E):
        age = rng.choice(["Y", "M"])
        direction = rng.choice(["U", "B"])
        u, v = rng.sample(nodes, 2)
        cost = rng.randint(1, 100)
        edges.append(f"{age} {direction} {u} {v} {cost}")

    src_young = nodes[0]
    src_old = nodes[min(1, V - 1)]

    lines = [str(E)] + edges + [f"{src_young} {src_old}", "0"]
    return "\n".join(lines)


def gen_321(R: int, D: int, S: int, seed: int = 42) -> str:
    """
    Generate a UVa 321 input with R rooms, D doors, S switches.
    Guarantees room 1 and room R are connected via a chain of doors,
    and room 1 has a switch to room R (so a solution exists).
    R must be <= 10.
    """
    R = min(R, 10)
    rng = random.Random(seed)

    door_set = set()
    # Chain: 1-2, 2-3, ..., (R-1)-R
    for i in range(1, R):
        door_set.add((i, i + 1))

    extra_doors = 0
    attempts = 0
    while extra_doors < D - (R - 1) and attempts < 200:
        u = rng.randint(1, R)
        v = rng.randint(1, R)
        if u != v:
            key = (min(u, v), max(u, v))
            if key not in door_set:
                door_set.add(key)
                extra_doors += 1
        attempts += 1

    switch_list = []
    # Room 1 controls room R (ensures goal is reachable)
    switch_list.append((1, R))

    attempts = 0
    while len(switch_list) < S and attempts < 200:
        u = rng.randint(1, R)
        v = rng.randint(1, R)
        if u != v:
            switch_list.append((u, v))
        attempts += 1

    lines = [f"{R} {len(door_set)} {len(switch_list)}"]
    for u, v in door_set:
        lines.append(f"{u} {v}")
    for u, v in switch_list:
        lines.append(f"{u} {v}")
    lines.append("0 0 0")
    return "\n".join(lines)
