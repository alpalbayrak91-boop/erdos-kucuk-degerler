#!/usr/bin/env python3
"""Check badness certificates "graph6 S=.. C1=a-b-..-a C2=..." (independent of e585.c).

Each line must give two cycles that use only edges of the graph, have the
same vertex set S (each vertex once, |S| >= 3), and share no edge.
Optional argument: a file of graph6 strings; every one must have a valid line.
Prints "certificates=<N> valid=<N> errors=<N> missing=<N>".
"""
import sys


def edges_g6(s):
    n = ord(s[0]) - 63
    bits = [(ord(c) - 63) >> (5 - k) & 1 for c in s[1:] for k in range(6)]
    pairs = [(i, j) for j in range(1, n) for i in range(j)]
    return {frozenset(p) for p, b in zip(pairs, bits) if b}


def cycle(spec, E):
    vs = [int(x) for x in spec.split("-")]
    if len(vs) < 4 or vs[0] != vs[-1] or len(set(vs[:-1])) != len(vs) - 1:
        return None
    es = {frozenset(p) for p in zip(vs, vs[1:])}
    return (set(vs[:-1]), es) if len(es) == len(vs) - 1 and es <= E else None


ok = bad = 0
seen = set()
for line in sys.stdin:
    g, S, c1, c2 = line.split()
    E = edges_g6(g)
    a, b = cycle(c1[3:], E), cycle(c2[3:], E)
    S = {int(x) for x in S[2:].split(",")}
    if a and b and a[0] == b[0] == S and not (a[1] & b[1]):
        ok += 1
        seen.add(g)
    else:
        bad += 1
missing = 0
if len(sys.argv) > 1:
    missing = sum(1 for l in open(sys.argv[1]) if l.strip() and l.strip() not in seen)
print(f"certificates={ok + bad} valid={ok} errors={bad} missing={missing}")
