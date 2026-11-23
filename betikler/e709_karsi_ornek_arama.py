import itertools, sys
def match(A, lo, hi):
    # distinct multiples in [lo,hi]
    adj={a:[x for x in range((lo+a-1)//a*a, hi+1, a)] for a in A}
    m={}
    def aug(a,seen):
        for x in adj[a]:
            if x in seen: continue
            seen.add(x)
            if x not in m or aug(m[x],seen):
                m[x]=a; return True
        return False
    return all(aug(a,set()) for a in sorted(A, key=lambda a:-a))
def works(n,k,Mmax,smax):
    for M in range(n+1, Mmax+1):
        for rest in itertools.combinations(range(2,M), n-1):
            A=rest+(M,)
            for s in range(smax):
                if not match(A, s+1, s+k*M): return (A,s)
    return None
for n in range(2,7):
    print(n, "k=1:", works(n,1,16,400), "k=2:", works(n,2,16,400), flush=True)
