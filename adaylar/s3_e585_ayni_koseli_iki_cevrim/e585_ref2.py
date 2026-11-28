#!/usr/bin/env python3
"""Second reference checker (pure Python, imports nothing from e585.c), fast enough for the
sparse extremal graphs at n = 12, 13.

For every vertex set S in which each vertex has >= 4 neighbours inside S (a necessary
condition for two edge-disjoint Hamiltonian cycles), list ALL Hamiltonian cycles of G[S] by
depth-first search as edge bitmasks, then test every pair for disjointness.
Usage: e585_ref2.py < graphs.g6  ->  "iyi=<0|1> kenar=<m>" per graph.
"""
import sys
from itertools import combinations


def parse(s):
    n = ord(s[0]) - 63
    bits = [(ord(c) - 63) >> (5 - k) & 1 for c in s[1:] for k in range(6)]
    adj = [set() for _ in range(n)]
    pairs = [(i, j) for j in range(1, n) for i in range(j)]
    for (i, j), b in zip(pairs, bits):
        if b:
            adj[i].add(j)
            adj[j].add(i)
    return n, adj


def cycles(S, adj, eid):
    s0, k, out = min(S), len(S), []

    def dfs(v, seen, path, mask):
        if len(path) == k:
            if s0 in adj[v] and path[1] < path[-1]:
                out.append(mask | eid[frozenset((v, s0))])
            return
        for w in adj[v]:
            if w in S and w not in seen:
                seen.add(w); path.append(w)
                dfs(w, seen, path, mask | eid[frozenset((v, w))])
                seen.discard(w); path.pop()

    dfs(s0, {s0}, [s0], 0)
    return out


def good(n, adj):
    eid = {}
    for v in range(n):
        for w in adj[v]:
            eid.setdefault(frozenset((v, w)), 1 << len(eid))
    for size in range(5, n + 1):
        for S in combinations(range(n), size):
            S = set(S)
            if any(len(adj[v] & S) < 4 for v in S):
                continue
            cs = cycles(S, adj, eid)
            if any(a & b == 0 for a, b in combinations(cs, 2)):
                return False
    return True


for line in sys.stdin:
    if line.strip():
        n, adj = parse(line.strip())
        print(f"iyi={int(good(n, adj))} kenar={sum(map(len, adj)) // 2}")
