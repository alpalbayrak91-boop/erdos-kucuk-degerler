#!/usr/bin/env python3
"""G(m,t): gobekler z,p,q (z~p, z~q); B: m kose, hepsi z,p,q'ya bagli; yol u_1..u_t, her u_i~p, u_1~z, u_t~q.
n = m+3+t, kenar = 3m+2t+3, iddia: iyi ve cevre = t+5 (m>=2, t>=2). stdout: graph6."""
import sys
def g6(n, E):
    adj=[[0]*n for _ in range(n)]
    for a,b in E: adj[a][b]=adj[b][a]=1
    bits=[adj[i][j] for j in range(1,n) for i in range(j)]
    while len(bits)%6: bits.append(0)
    return chr(n+63)+''.join(chr(63+int(''.join(map(str,bits[k:k+6])),2)) for k in range(0,len(bits),6))
def G(m,t):
    z,p,q=0,1,2; B=list(range(3,3+m)); U=list(range(3+m,3+m+t)); E=[(z,p),(z,q)]
    for b in B: E+=[(b,z),(b,p),(b,q)]
    for i in range(t-1): E.append((U[i],U[i+1]))
    for u in U: E.append((u,p))
    E+=[(U[0],z),(U[-1],q)]
    return 3+m+t, E
for m in range(2,8):
    for t in range(2,12):
        n,E=G(m,t)
        if n<=17: print(g6(n,E))
