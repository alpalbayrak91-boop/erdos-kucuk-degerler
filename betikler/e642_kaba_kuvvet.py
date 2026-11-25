"""OEIS A400041 — Erdos Problem #642 (Hamburger and Szegedy).

a(n) = maximum number of edges in a simple graph on n vertices in which
every simple cycle has strictly more vertices than chords.
Exact values for n = 0..7: 0, 0, 1, 3, 6, 9, 11, 14 (extended to n = 8..9 -> 17, 20 in e642/).
Usage:
  python3 betikler/e642_kaba_kuvvet.py          # prints n=0..6 quickly
  python3 betikler/e642_kaba_kuvvet.py 0 8      # prints n=0..7
"""
import itertools, sys
def cycles(n, adj):
    # enumerate simple cycles (as vertex lists) with smallest vertex first, direction canonical
    out=[]
    for s in range(n):
        stack=[(s,[s])]
        while stack:
            v,path=stack.pop()
            for w in adj[v]:
                if w==s and len(path)>=3 and path[1]<path[-1]: out.append(path)
                elif w>s and w not in path: stack.append((w,path+[w]))
    return out
def ok(n, E):
    adj=[set() for _ in range(n)]
    for a,b in E: adj[a].add(b); adj[b].add(a)
    for c in cycles(n, adj):
        k=len(c); cyc={frozenset((c[i],c[(i+1)%k])) for i in range(k)}
        chords=sum(1 for a,b in itertools.combinations(c,2) if b in adj[a] and frozenset((a,b)) not in cyc)
        if chords>=k: return False
    return True
def f(n):
    allE=list(itertools.combinations(range(n),2))
    for m in range(len(allE),-1,-1):
        for E in itertools.combinations(allE,m):
            if ok(n,E): return m
    return 0
if __name__ == "__main__":
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    for n in range(lo, hi):
        print(n, f(n), flush=True)
