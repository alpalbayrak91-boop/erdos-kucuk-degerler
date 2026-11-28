#!/usr/bin/env python3
"""Structure of the extremal graphs: two adjacent universal vertices plus a graph of girth >= 5.

usage: yapi.py tanik/uc_n*_m*.g6
For every graph6 file (all graphs in a file have the same n) it reports
  n, the number of edges m, the number of graphs, how many of them are of the form K_2 v H
  (two adjacent vertices joined to everything) with H free of 3-cycles and 4-cycles, and |E(H)|.
It then compares m with 2n - 3 + A006856(n - 2)  (A006856 = ex(k; {C3, C4})).

`yapi.py --join < H.g6` prints the graph6 of K_2 v H for every input graph H.
Pure Python, no dependencies; shares no code with e585.c.
"""
import sys
from itertools import combinations

A006856 = [0, 0, 1, 2, 3, 5, 6, 8, 10, 12, 15, 16, 18, 21, 23, 26, 28, 31, 34, 38, 41]  # index k = 0..20


def dec(s):
    n = ord(s[0]) - 63
    bits = [(ord(c) - 63) >> (5 - k) & 1 for c in s[1:] for k in range(6)]
    pairs = [(i, j) for j in range(1, n) for i in range(j)]
    return n, {p for p, b in zip(pairs, bits) if b}


def enc(n, E):
    bits = [1 if (i, j) in E else 0 for j in range(1, n) for i in range(j)]
    while len(bits) % 6:
        bits.append(0)
    return chr(n + 63) + "".join(chr(63 + int("".join(map(str, bits[k:k + 6])), 2)) for k in range(0, len(bits), 6))


def join_k2(n, E):
    u, v = n, n + 1
    return n + 2, set(E) | {(i, u) for i in range(n)} | {(i, v) for i in range(n)} | {(u, v)}


def girth5(vs, adj):
    """True if the graph induced on vs has no 3-cycle and no 4-cycle."""
    for a, b in combinations(vs, 2):
        common = len(adj[a] & adj[b] & vs)
        if common >= 2 or (common >= 1 and b in adj[a]):
            return False
    return True


def join_form(n, E):
    """Return |E(H)| if the graph is K_2 v H with H of girth >= 5, else None."""
    adj = {i: set() for i in range(n)}
    for i, j in E:
        adj[i].add(j)
        adj[j].add(i)
    uni = [x for x in range(n) if len(adj[x]) == n - 1]
    for u, v in combinations(uni, 2):
        rest = set(range(n)) - {u, v}
        if girth5(rest, adj):
            return sum(1 for i, j in E if i in rest and j in rest)
    return None


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--join":
        for line in sys.stdin:
            if line.strip():
                print(enc(*join_k2(*dec(line.strip()))))
        return
    print("n m graphs join_form |E(H)| 2n-3+A006856(n-2) equal")
    for path in sys.argv[1:]:
        gs = [dec(l.strip()) for l in open(path) if l.strip()]
        n, m = gs[0][0], len(gs[0][1])
        forms = [join_form(n, E) for n, E in gs]
        hit = [f for f in forms if f is not None]
        pred = 2 * n - 3 + A006856[n - 2] if n >= 2 else None
        eh = ",".join(map(str, sorted(set(hit)))) if hit else "-"
        print(n, m, len(gs), len(hit), eh, pred, "yes" if pred == m else "no")


if __name__ == "__main__":
    main()
