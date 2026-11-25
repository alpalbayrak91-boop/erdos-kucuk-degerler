"""OEIS A400042 — Erdos Problem #983 (Erdos and Straus).

a(n) = f(pi(n)+1, n), where f(k,n) is the least r such that every k-subset A of {1..n}
contains more than r elements whose prime factors all lie in some set of r primes.
Exact values for n = 2..16: 0, 0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4 (extended to n = 46 in e983/).
Usage:
  python3 betikler/e983_kaba_kuvvet.py          # prints [a(2)..a(16)]
  python3 betikler/e983_kaba_kuvvet.py 16       # prints [a(2)..a(N)]
"""
import sys, itertools
def primerange(a,b): return [p for p in range(a,b) if p>1 and all(p%q for q in range(2,int(p**.5)+1))]
def primefactors(a):
    r=[];d=2
    while d*d<=a:
        if a%d==0:
            r.append(d)
            while a%d==0: a//=d
        d+=1
    if a>1: r.append(a)
    return r
def f983(n):
    P=list(primerange(2,n+1)); k=len(P)+1
    pf={a:frozenset(primefactors(a)) for a in range(1,n+1)}
    Ssets=[]
    for r in range(len(P)+1):
        for S in itertools.combinations(P,r): Ssets.append((r,frozenset(S)))
    worst=0
    for A in itertools.combinations(range(1,n+1),k):
        g=None
        for r,S in Ssets:
            cnt=sum(1 for a in A if pf[a]<=S)
            if cnt>r: g=r; break
        worst=max(worst,g)
    return worst
if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    print([f983(n) for n in range(2,N+1)])
