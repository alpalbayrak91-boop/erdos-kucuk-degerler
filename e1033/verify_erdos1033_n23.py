#!/usr/bin/env python3
"""Standalone exhaustive verifier for Erdos Problem #1033 (three_halves variant, n = 23).

Constructs the explicit 23-vertex Erdos-Laskar counterexample graph G23:
  A = {0..8} (independent set of size 9)
  B = {9..22} (14 vertices inducing a 7-edge perfect matching)
  plus all 9 * 14 = 126 edges between A and B.

Checks:
  1. Simple graph axioms (irreflexive, symmetric) and exact degrees (14 in A, 10 in B).
  2. Edge count |E(G23)| = 133, so 4 * |E(G23)| = 532 > 529 = 23^2.
  3. Exhaustively over all C(23, 3) = 1771 triples (and all 196 triangles):
     max triangle degree sum is 34 (one vertex in A of deg 14 + two matched vertices in B of deg 10),
     so 2 * sum_deg <= 68 < 69 = 3 * 23.
"""
from __future__ import annotations

from itertools import combinations
import json
import sys


def adj_nat23(u: int, v: int) -> bool:
    if u < 9 and v >= 9:
        return True
    if u >= 9 and v < 9:
        return True
    if u >= 9 and v >= 9 and (u - 9) // 2 == (v - 9) // 2 and u != v:
        return True
    return False


def main() -> int:
    n = 23
    for v in range(n):
        assert not adj_nat23(v, v), f"loop at {v}"
    for u in range(n):
        for v in range(n):
            assert adj_nat23(u, v) == adj_nat23(v, u), f"asymmetry at ({u}, {v})"

    degrees = [sum(1 for j in range(n) if adj_nat23(i, j)) for i in range(n)]
    for i in range(n):
        expected = 14 if i < 9 else 10
        assert degrees[i] == expected, f"deg({i})={degrees[i]} != {expected}"

    two_e = sum(degrees)
    assert two_e == 266
    edges = two_e // 2
    assert edges == 133
    assert 4 * edges == 532 > 529 == n * n

    triples_checked = 0
    triangle_count = 0
    max_tri_deg_sum = -1
    for a, b, c in combinations(range(n), 3):
        triples_checked += 1
        if adj_nat23(a, b) and adj_nat23(a, c) and adj_nat23(b, c):
            triangle_count += 1
            s = degrees[a] + degrees[b] + degrees[c]
            if s > max_tri_deg_sum:
                max_tri_deg_sum = s
            assert 2 * s < 3 * n, f"triangle {(a, b, c)} violates counterexample bound"

    assert triples_checked == 1771
    assert triangle_count == 9 * 7 == 63
    assert max_tri_deg_sum == 34
    assert 2 * max_tri_deg_sum == 68 < 69 == 3 * n

    report = {
        "problem": "Erdos #1033 (variants.three_halves)",
        "n": n,
        "edges": edges,
        "four_e": 4 * edges,
        "n_sq": n * n,
        "triples_checked": triples_checked,
        "triangles": triangle_count,
        "max_triangle_degree_sum": max_tri_deg_sum,
        "two_max_triangle_degree_sum": 2 * max_tri_deg_sum,
        "three_n": 3 * n,
        "verified": True,
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
