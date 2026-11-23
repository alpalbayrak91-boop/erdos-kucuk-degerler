"""Bounds vs data for T(n) (max triangles, locally linear graph on n vertices).
Proved upper bound U(n)=floor(n*floor((n+3)/2)/9); proved constructions L(n)."""
import ast, re, itertools, networkx as nx
T={}; W={}
for f in ["results_cpsat.txt","results_cpsat_11plus.txt"]:
    for line in open(f):
        m=re.match(r"n=(\d+) status=(\w+) T=(\d+) bound=(\d+).*sol=(\[.*\])",line)
        if m:
            n=int(m[1]); T[n]=(m[2],int(m[3]),int(m[4])); W[n]=ast.literal_eval(m[5])
def U(n): return n*((n+3)//2)//9
L={1:0,2:0}
for n in range(3,16):
    c=[(n-1)//2, n//3]            # windmill, disjoint triangles
    c+= [L[n-1]]                  # add isolated vertex
    c+= [L[a]+L[n-a] for a in range(1,n)]          # disjoint union
    c+= [L[a]+L[n+1-a] for a in range(2,n)]        # glue at one vertex
    if n>=9: c.append(6 + (L[n-8] if n-8>=1 else 0))  # K3xK3 glued at a vertex
    L[n]=max(c)
print(" n  T(n)  status   solverUB  U(n)  simpleL(n)  degree multiset of witness")
for n in sorted(T):
    st,v,b=T[n]; deg={}
    for t in W[n]:
        for x in t: deg[x]=deg.get(x,0)+1
    ds=sorted(deg.values(),reverse=True)+[0]*(n-len(deg))
    print(f"{n:2d} {v:4d}  {st:9s} {b:4d}  {U(n):4d}  {L[n]:6d}      {ds}")
# check per-triple inequality on witnesses
for n in W:
    deg={}
    for t in W[n]:
        for x in t: deg[x]=deg.get(x,0)+1
    assert all(sum(deg[x] for x in t)<=(n+3)//2 for t in W[n])
print("per-triple degree inequality holds on all witnesses")
