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
for n in range(int(sys.argv[1]), int(sys.argv[2])):
    print(n, f(n), flush=True)
