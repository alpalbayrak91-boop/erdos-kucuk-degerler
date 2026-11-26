"""A400041 bagimsiz dogrulama: nauty-geng ile tum n-kose graflar (m kenar), 'her cevrimde chord < kose' kontrolu."""
import sys, subprocess, itertools
def g6_decode(s):
    s=s.strip(); n=ord(s[0])-63; bits=[]
    for ch in s[1:]:
        v=ord(ch)-63; bits.extend((v>>(5-i))&1 for i in range(6))
    adj=[set() for _ in range(n)]; k=0
    for j in range(1,n):
        for i in range(j):
            if bits[k]: adj[i].add(j); adj[j].add(i)
            k+=1
    return n,adj
def ok(n,adj):
    # DFS cevrim sayimi, ilk ihlalde dur
    for s in range(n):
        stack=[(s,[s],{s})]
        while stack:
            v,path,seen=stack.pop()
            for w in adj[v]:
                if w==s and len(path)>=3 and path[1]<path[-1]:
                    k=len(path); pos={x:i for i,x in enumerate(path)}
                    ch=0
                    for a,b in itertools.combinations(path,2):
                        if b in adj[a]:
                            d=abs(pos[a]-pos[b])
                            if d!=1 and d!=k-1: ch+=1
                    if ch>=k: return False
                elif w>s and w not in seen:
                    stack.append((w,path+[w],seen|{w}))
    return True
if __name__ == "__main__":
    n=int(sys.argv[1]); m=int(sys.argv[2])
    p=subprocess.Popen(['nauty-geng','-q',str(n),f'{m}:{m}'],stdout=subprocess.PIPE,text=True)
    toplam=gecen=0
    for line in p.stdout:
        toplam+=1
        nn,adj=g6_decode(line)
        if ok(nn,adj): gecen+=1
    print(f"n={n} m={m} graf={toplam} gecen={gecen}", flush=True)
