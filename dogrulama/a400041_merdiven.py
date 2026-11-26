"""A400041 f(12) (Claude): kose buyutme merdiveni. V[n][m] = tum gecerli n-koseli m-kenarli graflar (izomorfizmden ari).
G in V[n][m] => min derece d <= floor(2m/n), d'li kose silinince V[n-1][m-d]. Bu yuzden V[n][m] = U_d ext(V[n-1][m-d], d)."""
import sys, itertools, subprocess, time, json
sys.path.insert(0,'/tmp/a400041')
from dogrula import g6_decode, ok
from buyut import ekle, g6, tekil
def V9(m):
    out=[]
    for s in subprocess.run(['nauty-geng','-q','9',f'{m}:{m}'],capture_output=True,text=True).stdout.split():
        n,adj=g6_decode(s)
        if ok(n,adj): out.append([set(a) for a in adj])
    return out
HEDEF_N=int(sys.argv[1]) if len(sys.argv)>1 else 12
# her seviyede gereken en kucuk m: hedef (HEDEF_N, 3*HEDEF_N-6) icin geriye dogru
gerek={HEDEF_N: 3*HEDEF_N-6}
for n in range(HEDEF_N,9,-1):
    m=gerek[n]; gerek[n-1]=m-(2*m)//n
V={9:{}}
for m in range(gerek[9], 21):
    V[9][m]=V9(m); print(f"V[9][{m}]={len(V[9][m])}", flush=True)
f={9:20}
for n in range(10, HEDEF_N+1):
    V[n]={}; t0=time.time()
    m=gerek[n]
    while True:
        dmax=(2*m)//n; aday=[]
        for d in range(0,dmax+1):
            for b in V[n-1].get(m-d,[]):
                for K in itertools.combinations(range(n-1),d):
                    g=ekle(b,K)
                    if ok(n,g): aday.append(g)
        V[n][m]=tekil(aday)
        print(f"V[{n}][{m}]={len(V[n][m])} ({time.time()-t0:.0f}s)", flush=True)
        if not V[n][m]:
            if m>gerek[n]:
                f[n]=m-1
            else:
                # baslangic seviyesinde bile gecerli graf yok: yalniz ust sinir; alt sinir taniktan gelir
                f[n]=f"<= {m-1} (tanik 3n-7 ile esitlik ayrica kontrol edilmeli)"
            break
        m+=1
    print(f"==> f({n}) = {f[n]}  (3n-7 = {3*n-7})", flush=True)
json.dump({str(k):v for k,v in f.items()}, open(f'/tmp/a400041/f_merdiven_{HEDEF_N}.json','w'))
