#!/usr/bin/env python3
"""The cubic family G(GP(m,2), F_k) for Erdos problem 585 (graph6 output).

usage: kubik_aile.py M_MIN M_MAX [K]        (K defaults to 3)

B = generalized Petersen graph GP(m,2): outer vertices x_0..x_{m-1} with the cycle x_i x_{i+1},
inner vertices y_0..y_{m-1} with the edges y_i y_{i+2}, and the spokes x_i y_i (indices mod m).
F_k = { x_i y_{i+k}, x_i y_{i-k} : i mod m }, a 2-regular graph on V(B) with 2m edges.

G has the vertices u1, u2, w, one vertex a_e for each edge e of F_k, and V(B):
  u1 is adjacent to every other vertex; u2 to every other vertex except w;
  w is adjacent to u1 and to every a_e; a_e is adjacent to the two ends of e; B keeps its edges.
So n = 4m + 3 and the number of edges is 17m + 2.

For each m a comment line "# m=.. k=.. n=.. edges=.." and the graph6 string are printed.
Pipe the output (without the comment lines) to dort_duzenli.py to test for a 4-regular subgraph.
"""
import sys


def g6(n, edges):
    es = {(min(i, j), max(i, j)) for i, j in edges}
    bits = [1 if (i, j) in es else 0 for j in range(1, n) for i in range(j)]
    bits += [0] * (-len(bits) % 6)
    body = "".join(chr(63 + int("".join(map(str, bits[k:k + 6])), 2)) for k in range(0, len(bits), 6))
    if n < 63:
        return chr(63 + n) + body
    return "~" + chr(63 + (n >> 12)) + chr(63 + ((n >> 6) & 63)) + chr(63 + (n & 63)) + body


def gp(m, s=2):
    e = set()
    for i in range(m):
        e.add((min(i, (i + 1) % m), max(i, (i + 1) % m)))            # outer cycle
        e.add((i, m + i))                                             # spoke
        e.add((m + min(i, (i + s) % m), m + max(i, (i + s) % m)))     # inner edges
    return 2 * m, sorted(e)


def family(m, k):
    b, eb = gp(m)
    f = sorted({(i, m + (i + k) % m) for i in range(m)} | {(i, m + (i - k) % m) for i in range(m)})
    assert not set(f) & set(eb), "F shares an edge with B"
    a = len(f)
    n = a + b + 3
    u1, u2, w = 0, 1, 2
    av = list(range(3, 3 + a))
    bv = list(range(3 + a, n))
    edges = [(u1, v) for v in range(1, n)] + [(u2, v) for v in range(3, n)] + [(w, x) for x in av]
    edges += [(bv[x], bv[y]) for x, y in eb]
    for t, (x, y) in enumerate(f):
        edges += [(av[t], bv[x]), (av[t], bv[y])]
    assert len(set(edges)) == len(edges) == 5 * a + 2 * b + 2 + len(eb)
    return n, edges


if __name__ == "__main__":
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    k = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    for m in range(lo, hi + 1):
        n, edges = family(m, k)
        print(f"# m={m} k={k} n={n} edges={len(edges)}")
        print(g6(n, edges))
