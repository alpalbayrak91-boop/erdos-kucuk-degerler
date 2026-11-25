#!/usr/bin/env python3
"""Independent Python verifier and exact branch-and-bound solver for Erdos Problem #642.

Verifies:
1. All optimal graph witnesses for n = 0..9 in witnesses_n0_to_9.json satisfy
   CyclesHaveMoreVerticesThanChords under BOTH:
   - Explicit simple-cycle chord counting (chords(C) < |V(C)| for every simple cycle C), and
   - Held-Karp subset density criterion (no L-subset with L >= 5 has >= 2L edges and a Hamiltonian cycle).
2. Independent pure-Python branch-and-bound optimality proof for n = 0..8:
   f(0..8) = [0, 0, 1, 3, 6, 9, 11, 14, 17].
3. Validity of the general split-bipartite construction K_{3, n-3} + P_3 (3n - 7 edges) for n = 3..11.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import List, Sequence, Tuple


def enumerate_simple_cycles(n: int, edges: Sequence[Sequence[int]]) -> List[List[int]]:
    """Enumerate all undirected simple cycles as canonical vertex lists."""
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    cycles: List[List[int]] = []
    for start in range(n):
        stack: List[Tuple[int, List[int]]] = [(start, [start])]
        while stack:
            curr, path = stack.pop()
            for nxt in adj[curr]:
                if nxt == start and len(path) >= 3 and path[1] < path[-1]:
                    cycles.append(path)
                elif nxt > start and nxt not in path:
                    stack.append((nxt, path + [nxt]))
    return cycles


def is_valid_by_cycle_enumeration(n: int, edges: Sequence[Sequence[int]]) -> bool:
    """Direct definition check: every simple cycle C has strictly fewer chords than vertices."""
    edge_set = {frozenset((u, v)) for u, v in edges}
    if len(edge_set) != len(edges):
        return False
    for u, v in edges:
        if not (0 <= u < n and 0 <= v < n and u != v):
            return False
    for cyc in enumerate_simple_cycles(n, edges):
        k = len(cyc)
        cyc_edges = {frozenset((cyc[i], cyc[(i + 1) % k])) for i in range(k)}
        chords = sum(
            1
            for a, b in itertools.combinations(cyc, 2)
            if frozenset((a, b)) in edge_set and frozenset((a, b)) not in cyc_edges
        )
        if chords >= k:
            return False
    return True


def _has_hamiltonian_cycle_bitmask(adj_sub: List[int], k: int) -> bool:
    """Exact Held-Karp bitmask check: does k-vertex graph have a Hamiltonian cycle (k >= 3)?"""
    if k < 3:
        return False
    full = (1 << k) - 1
    dp = [0] * (1 << k)
    dp[1] = 1
    for mask in range(1, 1 << k):
        if not (mask & 1):
            continue
        reach = dp[mask]
        if not reach:
            continue
        u_bits = reach
        while u_bits:
            lsb = u_bits & -u_bits
            u = lsb.bit_length() - 1
            u_bits ^= lsb
            nbrs = adj_sub[u] & (~mask) & full
            v_bits = nbrs
            while v_bits:
                v_lsb = v_bits & -v_bits
                dp[mask | v_lsb] |= v_lsb
                v_bits ^= v_lsb
    return bool(dp[full] & adj_sub[0])


def is_erdos642_valid_bitmask(n: int, adj: List[int]) -> bool:
    """Held-Karp check: no subset S of size L >= 5 with |E(G[S])| >= 2L is Hamiltonian."""
    if n < 5:
        return True
    verts = list(range(n))
    for length in range(5, n + 1):
        thresh = 2 * length
        for sub in itertools.combinations(verts, length):
            sub_mask = 0
            for v in sub:
                sub_mask |= 1 << v
            e_cnt = 0
            for v in sub:
                e_cnt += (adj[v] & sub_mask).bit_count()
            e_cnt //= 2
            if e_cnt < thresh:
                continue
            local_adj = [0] * length
            for i, u in enumerate(sub):
                m_u = adj[u]
                row = 0
                for j, w in enumerate(sub):
                    if (m_u >> w) & 1:
                        row |= 1 << j
                local_adj[i] = row
            if _has_hamiltonian_cycle_bitmask(local_adj, length):
                return False
    return True


def solve_erdos642_max_edges(n: int) -> Tuple[int, List[Tuple[int, int]]]:
    """Exact pure-Python branch-and-bound solver with max-degree symmetry breaking on vertex 0."""
    if n <= 1:
        return 0, []
    if n <= 4:
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        return len(edges), edges

    all_pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    adj_seed = [0] * n
    seed_edges: List[Tuple[int, int]] = []
    for u, v in all_pairs:
        adj_seed[u] |= 1 << v
        adj_seed[v] |= 1 << u
        if is_erdos642_valid_bitmask(n, adj_seed):
            seed_edges.append((u, v))
        else:
            adj_seed[u] ^= 1 << v
            adj_seed[v] ^= 1 << u
    best_m = len(seed_edges)
    best_edges = list(seed_edges)

    for d0 in range(n - 1, -1, -1):
        if (n * d0) // 2 <= best_m:
            break
        adj = [0] * n
        cur_edges: List[Tuple[int, int]] = []
        for v in range(1, d0 + 1):
            adj[0] |= 1 << v
            adj[v] |= 1 << 0
            cur_edges.append((0, v))

        # Order remaining pairs by largest endpoint j first so every vertex w > j
        # has degree <= 1 (at most edge (0, w)) and cannot participate in any cycle.
        rem_pairs = [(i, j) for j in range(2, n) for i in range(1, j)]
        rem_len = len(rem_pairs)

        def dfs(idx: int, e_so_far: int) -> None:
            nonlocal best_m, best_edges
            if e_so_far + (rem_len - idx) <= best_m:
                return
            if idx == rem_len:
                if e_so_far > best_m:
                    best_m = e_so_far
                    best_edges = list(cur_edges)
                return

            u, v = rem_pairs[idx]
            if adj[u].bit_count() < d0 and adj[v].bit_count() < d0:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
                ok = True
                active_n = v + 1
                if active_n >= 5:
                    others = [w for w in range(active_n) if w != u and w != v]
                    for length in range(5, active_n + 1):
                        thresh = 2 * length
                        for extra in itertools.combinations(others, length - 2):
                            sub = (u, v) + extra
                            sub_mask = 0
                            for w in sub:
                                sub_mask |= 1 << w
                            e_cnt = 0
                            for w in sub:
                                e_cnt += (adj[w] & sub_mask).bit_count()
                            e_cnt //= 2
                            if e_cnt >= thresh:
                                local_adj = [0] * length
                                for ii, wu in enumerate(sub):
                                    mu = adj[wu]
                                    row = 0
                                    for jj, wv in enumerate(sub):
                                        if (mu >> wv) & 1:
                                            row |= 1 << jj
                                    local_adj[ii] = row
                                if _has_hamiltonian_cycle_bitmask(local_adj, length):
                                    ok = False
                                    break
                        if not ok:
                            break
                if ok:
                    cur_edges.append((u, v))
                    dfs(idx + 1, e_so_far + 1)
                    cur_edges.pop()
                adj[u] ^= 1 << v
                adj[v] ^= 1 << u

            dfs(idx + 1, e_so_far)

        dfs(0, d0)

    return best_m, best_edges


def construct_k3_bipartite_plus_p3(n: int) -> List[Tuple[int, int]]:
    """Construct G_n = K_{3, n-3} + P_3 with 3n - 7 edges for n >= 3."""
    if n < 3:
        raise ValueError("n must be >= 3")
    a0, a1, a2 = n - 3, n - 2, n - 1
    edges = [(b, a) for b in range(n - 3) for a in (a0, a1, a2)]
    edges.extend([(a0, a2), (a1, a2)])
    return edges


def verify_all(max_bnb_n: int = 8) -> dict:
    here = Path(__file__).resolve().parent
    data = json.loads((here / "witnesses_n0_to_9.json").read_text(encoding="utf-8"))
    expected = [0, 0, 1, 3, 6, 9, 11, 14, 17, 20]
    assert data["f_seq_0_to_9"] == expected

    for row in data["witnesses"]:
        n = row["n"]
        f_n = row["f_n"]
        edges = row["edges"]
        assert f_n == expected[n]
        assert len(edges) == f_n
        assert is_valid_by_cycle_enumeration(n, edges), f"Cycle check failed at n={n}"
        adj = [0] * n
        for u, v in edges:
            adj[u] |= 1 << v
            adj[v] |= 1 << u
        assert is_erdos642_valid_bitmask(n, adj), f"Bitmask check failed at n={n}"

    bnb_seq = []
    for n in range(max_bnb_n + 1):
        val, wit = solve_erdos642_max_edges(n)
        assert val == expected[n], f"BnB mismatch at n={n}: {val} != {expected[n]}"
        assert is_valid_by_cycle_enumeration(n, wit)
        bnb_seq.append(val)

    for n in range(3, 12):
        gn = construct_k3_bipartite_plus_p3(n)
        assert len(gn) == 3 * n - 7
        adj = [0] * n
        for u, v in gn:
            adj[u] |= 1 << v
            adj[v] |= 1 << u
        assert is_erdos642_valid_bitmask(n, adj)

    return {
        "verified_witnesses_n0_to_9": expected,
        "python_bnb_exact_seq": bnb_seq,
        "k3_p3_lower_bound_verified_up_to": 11,
    }


if __name__ == "__main__":
    print(json.dumps(verify_all(max_bnb_n=8), indent=2))
