#!/usr/bin/env python3
"""The cycle family G(C_b, F) (section "Theorem (cycle family)" of README.md).

usage: aile.py B_MIN B_MAX
For every b in B_MIN..B_MAX prints two graph6 lines:
  G(C_b, F) with F = C_b(3), and with F = C_b(3) minus the edge {b_0, b_3}.
A line "# b=<b> F=<C3|C3-e> n=<n> m=<m> |E(F)|=<f>" precedes each graph (dort_duzenli.py skips
nothing, so filter with `grep -v '^#'` before piping).

Vertices: u1 = 0, u2 = 1, w = 2, b_i = 3 + i (0 <= i < b), then one vertex a_e per edge e of F.
Edges: u1 to everything; u2 to everything except w; w to every a_e; the cycle b_i b_{i+1};
a_e to both ends of e.  C_b(3) is the set of pairs {b_i, b_{i+3 mod b}} (for b = 6 it has only
3 edges).  Pure Python, no dependencies.
"""
import sys


def enc(n, E):
    assert n <= 62
    bits = [1 if (i, j) in E else 0 for j in range(1, n) for i in range(j)]
    while len(bits) % 6:
        bits.append(0)
    return chr(n + 63) + "".join(chr(63 + int("".join(map(str, bits[k:k + 6])), 2)) for k in range(0, len(bits), 6))


def family(b, F):
    u1, u2, w = 0, 1, 2
    B = [3 + i for i in range(b)]
    F = sorted(F)
    A = [3 + b + k for k in range(len(F))]
    n = 3 + b + len(F)
    E = set()

    def add(x, y):
        assert x != y
        E.add((min(x, y), max(x, y)))

    for v in range(n):
        if v != u1:
            add(u1, v)
        if v not in (u1, u2, w):
            add(u2, v)
    for i in range(b):
        add(B[i], B[(i + 1) % b])
    for a, (x, y) in zip(A, F):
        add(a, w)
        add(a, B[x])
        add(a, B[y])
    return n, E


def c3(b):
    return {(min(i, (i + 3) % b), max(i, (i + 3) % b)) for i in range(b)}


def main():
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    for b in range(lo, hi + 1):
        full = c3(b)
        for name, F in (("C3", full), ("C3-e", full - {(0, 3)})):
            n, E = family(b, F)
            assert len(E) == 5 * len(F) + 3 * b + 2
            print(f"# b={b} F={name} n={n} m={len(E)} |E(F)|={len(F)}")
            print(enc(n, E))


if __name__ == "__main__":
    main()
