#!/usr/bin/env python3
"""Independent reference checker for Erdos 585 (pure Python, different algorithm).

For every vertex set S with |S| >= 5, list ALL Hamiltonian cycles of G[S]
by brute force over permutations (start fixed at min(S)), store each as a
frozenset of edges, and look for two disjoint ones.  No 4-core pruning,
no cycle-removal search: shares no logic with e585.c.

Usage: e585_ref.py < graphs.g6   ->  one line "iyi=<0|1> kenar=<m>" per graph.
"""
from __future__ import annotations

import sys
from itertools import combinations, permutations


def parse_g6(s: str) -> tuple[int, set[tuple[int, int]]]:
    s = s.strip()
    if s.startswith(">>graph6<<"):
        s = s[10:]
    n = ord(s[0]) - 63
    bits = []
    for ch in s[1:]:
        v = ord(ch) - 63
        bits.extend((v >> (5 - k)) & 1 for k in range(6))
    edges = set()
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                edges.add((i, j))
            k += 1
    return n, edges


def ham_cycles(S: tuple[int, ...], E: set[tuple[int, int]]) -> list[frozenset]:
    first, rest = S[0], S[1:]
    out = []
    for perm in permutations(rest):
        if perm[0] > perm[-1]:
            continue
        cyc = (first,) + perm
        es = []
        for a, b in zip(cyc, cyc[1:] + (first,)):
            e = (a, b) if a < b else (b, a)
            if e not in E:
                break
            es.append(e)
        else:
            out.append(frozenset(es))
    return out


def is_good(n: int, E: set[tuple[int, int]]) -> bool:
    for size in range(5, n + 1):
        for S in combinations(range(n), size):
            sub = {e for e in E if e[0] in S and e[1] in S}
            if len(sub) < 2 * size:
                continue
            cycles = ham_cycles(S, sub)
            for c1, c2 in combinations(cycles, 2):
                if not (c1 & c2):
                    return False
    return True


def main() -> None:
    for line in sys.stdin:
        if not line.strip():
            continue
        n, E = parse_g6(line)
        print(f"iyi={int(is_good(n, E))} kenar={len(E)}")


if __name__ == "__main__":
    main()
