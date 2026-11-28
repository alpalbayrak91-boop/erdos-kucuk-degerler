#!/usr/bin/env python3
"""Randomized test of the map in Lemma 2 of kubik_kaniti.md (the mechanical part of the lemma).

For random index sets Q (|Q| <= 12, built from a few clusters) in G_m, take the vertices u1, u2, w,
all x_q, y_q with q in Q and all a_e whose two ends have indices in Q.  Apply the map of Lemma 2
(gaps of size <= 3 kept, larger gaps shrunk to 1) into G_M and check that the map is injective and
that EVERY edge of G_m among these vertices is sent to an edge of G_M.
Output per (m, k, M): number of trials, edges tested, shrunk gaps, errors (must be 0).
usage: python3 kubik_tasima_sina.py
"""
import random, sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from kubik_aile import gp


def kur(m,k):
    b,eb=gp(m)
    f=sorted({(i,m+(i+k)%m) for i in range(m)}|{(i,m+(i-k)%m) for i in range(m)})
    a=len(f); n=a+b+3
    av=list(range(3,3+a)); bv=list(range(3+a,n))
    E=[(0,v) for v in range(1,n)]+[(1,v) for v in range(3,n)]+[(2,x) for x in av]+[(bv[x],bv[y]) for x,y in eb]
    for t,(x,y) in enumerate(f): E+=[(av[t],bv[x]),(av[t],bv[y])]
    ad={0:('u1',),1:('u2',),2:('w',)}
    for t,(x,y) in enumerate(f): ad[av[t]]=('a',x,(y-m-x)%m)       # dis uc indisi, fark (k ya da m-k)
    for i in range(m): ad[bv[i]]=('x',i); ad[bv[m+i]]=('y',i)
    return n,[(min(i,j),max(i,j)) for i,j in E],ad,av,bv,f


def sina(m,k,Mh,deneme,seed):
    rnd=random.Random(seed)
    n,E,ad,av,bv,f=kur(m,k); n2,E2,ad2,av2,bv2,f2=kur(Mh,k); ters={v:kk for kk,v in ad2.items()}; E2s=set(E2)
    kenarlar=0; sikistirilan=0; hata=0; atlanan=0
    for _ in range(deneme):
        r=rnd.randint(2,12)
        # kumeler halinde indis sec: birkac yakin grup
        Q=set()
        while len(Q)<r:
            c=rnd.randrange(m)
            for _ in range(rnd.randint(1,4)):
                if len(Q)<r: Q.add((c+rnd.randint(-3,3))%m)
        q=sorted(Q); r=len(q)
        gaps=[(q[(j+1)%r]-q[j])%m or m for j in range(r)]
        jb=max(range(r),key=lambda j:gaps[j])
        if gaps[jb]<4: atlanan+=1; continue
        bas=q[(jb+1)%r]; don=lambda i:(i-bas)%m
        qq=sorted(don(v) for v in q); p=[0]
        for j in range(r-1):
            g=qq[j+1]-qq[j]; p.append(p[-1]+(g if g<=3 else 1)); sikistirilan+=(g>=4)
        assert p[-1]<=33<Mh
        phi=dict(zip(qq,p))
        V=[0,1,2]+[v for v in range(3,n) if (ad[v][0] in('x','y') and ad[v][1] in Q) or (ad[v][0]=='a' and ad[v][1] in Q and (ad[v][1]+ad[v][2])%m in Q)]
        def gor(v):
            t=ad[v]
            if t[0] in('u1','u2','w'): return ters[t]
            if t[0] in('x','y'): return ters[(t[0],phi[don(t[1])])]
            c=t[2] if t[2]<=3 else t[2]-m
            return ters[('a',phi[don(t[1])],c%Mh)]
        img={v:gor(v) for v in V}
        if len(set(img.values()))!=len(V): hata+=1; continue
        Vs=set(V)
        for i,j in E:
            if i in Vs and j in Vs:
                kenarlar+=1
                e=(min(img[i],img[j]),max(img[i],img[j]))
                if e not in E2s: hata+=1
    return dict(m=m,k=k,M=Mh,deneme=deneme,atlanan=atlanan,sinanan_kenar=kenarlar,sikistirilan_bosluk=sikistirilan,hata=hata)
for (m,k,Mh) in [(37,3,34),(40,3,34),(53,3,35),(70,3,34),(100,3,34),(40,2,34),(45,1,36)]:
    print(sina(m,k,Mh,3000,m*1000+Mh))
