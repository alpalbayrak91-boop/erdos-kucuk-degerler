#!/usr/bin/env python3
"""Read graph6 from stdin; print every way of adding one new vertex of degree d (graph6)."""
import sys, itertools
def decode(s):
    s = s.strip(); n = ord(s[0]) - 63; bits = []
    for ch in s[1:]:
        v = ord(ch) - 63; bits.extend((v >> k) & 1 for k in (5,4,3,2,1,0))
    adj = [[0]*n for _ in range(n)]; k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]: adj[i][j] = adj[j][i] = 1
            k += 1
    return n, adj
def encode(n, adj):
    bits = [adj[i][j] for j in range(1, n) for i in range(j)]
    while len(bits) % 6: bits.append(0)
    out = chr(n + 63)
    for k in range(0, len(bits), 6):
        v = 0
        for b in bits[k:k+6]: v = (v << 1) | b
        out += chr(v + 63)
    return out
d = int(sys.argv[1])
for line in sys.stdin:
    if not line.strip(): continue
    n, adj = decode(line)
    for nb in itertools.combinations(range(n), d):
        a = [row + [0] for row in adj] + [[0]*(n+1)]
        for u in nb: a[u][n] = a[n][u] = 1
        print(encode(n+1, a))
