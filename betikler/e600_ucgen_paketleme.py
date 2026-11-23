import itertools, sys
def max_tri_unique(n):
    """max number of triangles t such that union graph has every edge in exactly one triangle"""
    V=range(n); T=list(itertools.combinations(V,3)); best=[0]
    def edges(t): a,b,c=t; return {(a,b),(a,c),(b,c)}
    def ok(sel):
        E=set().union(*[edges(t) for t in sel]) if sel else set()
        adj={v:set() for v in V}
        for a,b in E: adj[a].add(b); adj[b].add(a)
        cnt=sum(1 for a,b,c in T if b in adj[a] and c in adj[a] and c in adj[b])
        return cnt==len(sel)
    def rec(i, sel, used):
        if len(sel)+ (len(T)-i) <= best[0]: return
        if len(sel)>best[0]: best[0]=len(sel)
        for j in range(i,len(T)):
            e=edges(T[j])
            if e & used: continue
            s2=sel+[T[j]]
            if ok(s2): rec(j+1, s2, used|e)
    rec(0,[],set()); return best[0]
for n in range(int(sys.argv[1]), int(sys.argv[2])):
    t=max_tri_unique(n); print(n, "ucgen", t, "e(n,2)=", 3*t+1, flush=True)
