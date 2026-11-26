"""A400041 f(10), f(11) bagimsiz dogrulama (Claude): ozellik kose silmeye kapali.
G gecerli, n kose, m kenar ise min derece d<=floor(2m/n); o koseyi silince n-1 koseli gecerli graf, m-d kenar."""
import subprocess, itertools, sys
sys.path.insert(0,'/tmp/a400041')
from dogrula import g6_decode, ok
def gecerli_9(m):
    p=subprocess.run(['nauty-geng','-q','9',f'{m}:{m}'],capture_output=True,text=True).stdout.split()
    out=[]
    for s in p:
        n,adj=g6_decode(s)
        if ok(n,adj): out.append([set(a) for a in adj])
    return out
def ekle(adj, komsular):
    n=len(adj); yeni=[set(a) for a in adj]+[set(komsular)]
    for k in komsular: yeni[k].add(n)
    return yeni
def kanon(adj):  # izomorfizm tekillestirme icin basit: sirali derece dizisi + kenar kumesi min permutasyon yerine nauty
    n=len(adj); E=sorted((i,j) for i in range(n) for j in adj[i] if i<j)
    return n,E
def g6(adj):
    n=len(adj); bits=[]
    for j in range(1,n):
        for i in range(j): bits.append(1 if j in adj[i] else 0)
    while len(bits)%6: bits.append(0)
    return chr(n+63)+''.join(chr(63+int(''.join(map(str,bits[k:k+6])),2)) for k in range(0,len(bits),6))
def tekil(graflar):
    if not graflar: return []
    girdi='\n'.join(g6(a) for a in graflar)+'\n'
    out=subprocess.run(['nauty-labelg','-q'],input=girdi,capture_output=True,text=True).stdout.split()
    gor={}; 
    for s,a in zip(out,graflar): gor.setdefault(s,a)
    return list(gor.values())
def m_kenar(adj): return sum(len(a) for a in adj)//2
# 9 koseli gecerli graflar: 19 ve 20 kenar
g19=gecerli_9(19); g20=gecerli_9(20)
print("9-kose gecerli: m=19 ->",len(g19)," m=20 ->",len(g20), flush=True)
# f(10)<=23: 24 kenarli 10-kose gecerli graf -> d<=4, kalan >=20 kenar -> yalniz g20 + derece-4 kose
v24=[g for b in g20 for K in itertools.combinations(range(9),4) if ok(10,(g:=ekle(b,K)))]
print("10-kose 24 kenar gecerli:",len(v24))
# 10-kose 23 kenar gecerli: g19 + d4 veya g20 + d3
v23=[g for b in g19 for K in itertools.combinations(range(9),4) if ok(10,(g:=ekle(b,K)))] + \
    [g for b in g20 for K in itertools.combinations(range(9),3) if ok(10,(g:=ekle(b,K)))]
v23=tekil(v23); print("10-kose 23 kenar gecerli (izomorfizmden ari):",len(v23), flush=True)
# f(11)<=26: 27 kenarli 11-kose -> d<=4, kalan >=23 -> v23 + derece-4
v27=sum(1 for b in v23 for K in itertools.combinations(range(10),4) if ok(11,ekle(b,K)))
print("11-kose 27 kenar gecerli:",v27)
# alt sinir tanigi: K_{3,n-3} + P3 (3'lu tarafta 2 kenar)
for n in (10,11):
    adj=[set() for _ in range(n)]
    for a in range(3):
        for b in range(3,n): adj[a].add(b); adj[b].add(a)
    for a,b in ((0,1),(1,2)): adj[a].add(b); adj[b].add(a)
    print(f"tanik n={n}: kenar={m_kenar(adj)} gecerli={ok(n,adj)}")
