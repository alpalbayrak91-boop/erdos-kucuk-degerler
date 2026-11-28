#!/usr/bin/env python3
"""Does a graph contain a 4-regular subgraph?  Independent of e585.c (integer programming).

usage: dort_duzenli.py < graphs.g6
For each graph6 line prints  "n=<n> m=<m> four_regular_subgraph=<0|1> [S=<vertices>]".

Model: x_e in {0,1} for every edge, y_v in {0,1} for every vertex,
       sum of x_e over the edges at v = 4 y_v,   sum of y_v >= 1.
A solution is a nonempty subgraph in which every vertex has degree 4.
A graph with no 4-regular subgraph has no two edge-disjoint cycles on the same vertex set
(the union of two such cycles is 4-regular).  The converse is false in general.
Needs scipy >= 1.9 (scipy.optimize.milp, HiGHS).
"""
import sys

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix


def dec(s):
    if ord(s[0]) == 126:      # graph6 with 63 <= n <= 258047: '~' and three more bytes
        n = ((ord(s[1]) - 63) << 12) | ((ord(s[2]) - 63) << 6) | (ord(s[3]) - 63)
        s = s[3:]
    else:
        n = ord(s[0]) - 63
    bits = [(ord(c) - 63) >> (5 - k) & 1 for c in s[1:] for k in range(6)]
    pairs = [(i, j) for j in range(1, n) for i in range(j)]
    return n, [p for p, b in zip(pairs, bits) if b]


def four_regular_subgraph(n, edges):
    m = len(edges)
    if m == 0:
        return None
    a = lil_matrix((n + 1, m + n))
    for k, (i, j) in enumerate(edges):
        a[i, k] = 1
        a[j, k] = 1
    for v in range(n):
        a[v, m + v] = -4
        a[n, m + v] = 1
    lo = np.zeros(n + 1)
    hi = np.zeros(n + 1)
    lo[n], hi[n] = 1, n
    res = milp(c=np.zeros(m + n), constraints=LinearConstraint(a.tocsr(), lo, hi),
               integrality=np.ones(m + n), bounds=Bounds(0, 1))
    if res.status == 2:      # infeasible
        return None
    if res.status != 0 or res.x is None:
        raise RuntimeError(f"solver status {res.status}: {res.message}")
    x = np.rint(res.x).astype(int)
    used = [e for k, e in enumerate(edges) if x[k]]
    deg = [0] * n
    for i, j in used:
        deg[i] += 1
        deg[j] += 1
    s = [v for v in range(n) if x[m + v]]
    assert s and all(deg[v] == (4 if v in s else 0) for v in range(n)), "solution check failed"
    return s


for line in sys.stdin:
    g = line.strip()
    if not g:
        continue
    n, edges = dec(g)
    s = four_regular_subgraph(n, edges)
    print(f"n={n} m={len(edges)} four_regular_subgraph={0 if s is None else 1}" + ("" if s is None else " S=" + ",".join(map(str, s))))
