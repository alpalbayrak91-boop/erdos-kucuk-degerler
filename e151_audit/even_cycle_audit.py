#!/usr/bin/env python3
"""Exact Python verifier for the Even-Cycle-Free Extremal Graph & OEIS A032766 Audit,
with explicit disambiguation from Erdos Problem #151 (Erdos-Gallai-Tuza clique transversals).

Verifies:
1. Even-cycle-free simple graph extremal edge counts ex(n, {C_4, C_6, ...}) = floor(3*(n-1)/2)
   exhaustively for n = 1..8 -> [0, 1, 3, 4, 6, 7, 9, 10] (OEIS A032766).
2. Prefix agreement for indices 0..23 and exact divergence at index 24 (n = 25) between
   OEIS A032766 (36) and OEIS A380408 (37).
3. Small-n sanity check on true Erdos Problem #151 (clique transversal number tau(G) <= n - H(n))
   for n = 1..5 over all labeled simple graphs, confirming the two problems are distinct.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
from typing import Dict, List, Optional, Sequence, Tuple


def has_even_cycle(n: int, edges: Sequence[Tuple[int, int]]) -> bool:
    adj = [0] * n
    for u, v in edges:
        stack = [(u, 1 << u, 0)]
        while stack:
            curr, vis, dist = stack.pop()
            nbrs = adj[curr] & ~vis
            while nbrs:
                bit = nbrs & -nbrs
                nbrs ^= bit
                nxt = bit.bit_length() - 1
                nd = dist + 1
                if nxt == v:
                    if nd >= 3 and (nd & 1) == 1:
                        return True
                else:
                    stack.append((nxt, vis | bit, nd))
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return False


def friendship_cactus_witness(n: int) -> List[Tuple[int, int]]:
    edges: List[Tuple[int, int]] = []
    for i in range((n - 1) // 2):
        a, b = 1 + 2 * i, 2 + 2 * i
        edges.extend([(0, a), (0, b), (a, b)])
    if (n - 1) % 2 == 1:
        edges.append((0, n - 1))
    return edges


def verify_no_even_cycle_free_above_bound(
    n: int, target: int, prev_max: Dict[int, int]
) -> Tuple[bool, Optional[List[Tuple[int, int]]], int]:
    assert target - 1 > prev_max[n - 1]
    min_d = (2 * target + n - 1) // n
    checked = 0
    for d in range(min_d, n):
        r_verts = list(range(d + 1, n))
        r_size = len(r_verts)
        r_pairs = list(itertools.combinations(r_verts, 2))
        max_r = prev_max[r_size] if r_size > 0 else 0
        for m_match in range(0, d // 2 + 1):
            base = [(0, i) for i in range(1, d + 1)]
            for j in range(m_match):
                base.append((1 + 2 * j, 2 + 2 * j))
            rem = target - len(base)
            if rem <= 0:
                if not has_even_cycle(n, base):
                    return False, base, checked
                continue
            if r_size + max_r < rem:
                continue
            choices = [None] + list(range(1, d + 1))
            for cross in itertools.product(choices, repeat=r_size):
                c_edges = [
                    (r_verts[i], cross[i])
                    for i in range(r_size)
                    if cross[i] is not None
                ]
                need_r = rem - len(c_edges)
                if need_r < 0 or need_r > min(len(r_pairs), max_r):
                    continue
                for r_ed in itertools.combinations(r_pairs, need_r):
                    checked += 1
                    cand = base + c_edges + list(r_ed)
                    if not has_even_cycle(n, cand):
                        return False, cand, checked
    return True, None, checked


def a380408_term(k: int) -> int:
    total = 0
    j = 0
    while True:
        denom = math.factorial(2 * j)
        if denom > max(1, k) and j > 0:
            break
        total += k // denom
        j += 1
    return total


def check_true_erdos151_small(max_n: int = 5) -> Dict[int, dict]:
    """Verify Erdos-Gallai-Tuza clique transversal bound tau(G) <= n - H(n) for n = 1..max_n."""
    summary: Dict[int, dict] = {}
    for n in range(1, max_n + 1):
        pairs = list(itertools.combinations(range(n), 2))
        min_indep_triangle_free = n
        max_tau = 0
        for m in range(len(pairs) + 1):
            for edges in itertools.combinations(pairs, m):
                adj = [0] * n
                for u, v in edges:
                    adj[u] |= 1 << v
                    adj[v] |= 1 << u
                # Check triangle-freeness
                tri_free = all((adj[u] & adj[v]) == 0 for u, v in edges)
                if tri_free:
                    alpha = 0
                    for r in range(n, -1, -1):
                        if any(
                            all(((adj[u] >> v) & 1) == 0 for u, v in itertools.combinations(sub, 2))
                            for sub in itertools.combinations(range(n), r)
                        ):
                            alpha = r
                            break
                    min_indep_triangle_free = min(min_indep_triangle_free, alpha)
                # Maximal cliques of size >= 2
                cliques_ge2 = []
                for r in range(2, n + 1):
                    for sub in itertools.combinations(range(n), r):
                        if all(((adj[u] >> v) & 1) == 1 for u, v in itertools.combinations(sub, 2)):
                            sub_set = set(sub)
                            if not any(
                                w not in sub_set and all(((adj[w] >> u) & 1) == 1 for u in sub)
                                for w in range(n)
                            ):
                                mask = 0
                                for u in sub:
                                    mask |= 1 << u
                                cliques_ge2.append(mask)
                if not cliques_ge2:
                    tau = 0
                else:
                    tau = n
                    for r in range(1, n + 1):
                        if any(
                            all((tmask & cmask) != 0 for cmask in cliques_ge2)
                            for tmask in (
                                sum(1 << u for u in sub)
                                for sub in itertools.combinations(range(n), r)
                            )
                        ):
                            tau = r
                            break
                max_tau = max(max_tau, tau)
        assert max_tau <= n - min_indep_triangle_free
        summary[n] = {"H_n": min_indep_triangle_free, "max_tau": max_tau, "bound_n_minus_H": n - min_indep_triangle_free}
    return summary


def run_audit() -> dict:
    prev_max = {0: 0, 1: 0, 2: 1}
    seq: List[int] = []
    for n in range(1, 9):
        wit = friendship_cactus_witness(n)
        assert len(wit) == (3 * (n - 1)) // 2
        assert not has_even_cycle(n, wit)
        if n >= 3:
            ok, cex, _ = verify_no_even_cycle_free_above_bound(n, len(wit) + 1, prev_max)
            assert ok, f"Counterexample at n={n}: {cex}"
        prev_max[n] = len(wit)
        seq.append(len(wit))

    a032766 = [x for x in range(200) if x % 3 in (0, 1)]
    assert seq == a032766[:8]
    for k in range(24):
        assert a380408_term(k) == a032766[k]
    a380408_24 = a380408_term(24)
    assert a380408_24 == 37 and a032766[24] == 36

    egt_small = check_true_erdos151_small(max_n=5)
    payload = {
        "even_cycle_free_n1_to_8": seq,
        "oeis_exact": "A032766",
        "prefix_match_0_to_23_with_A380408": True,
        "a380408_div_24": [a380408_24, a032766[24]],
        "erdos151_clique_transversal_small_n1_to_5": egt_small,
    }
    payload["sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")
    ).hexdigest()
    return payload


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2))
