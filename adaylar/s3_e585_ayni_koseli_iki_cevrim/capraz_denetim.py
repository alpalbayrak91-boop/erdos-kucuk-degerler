"""Independent cross-check of dort_duzenli.py: does a graph have a 4-regular subgraph?

Same 0/1 model, two other solvers: CP-SAT (ortools) and CBC (pulp), one thread each.
usage: capraz_denetim.py [SECONDS] < graphs.g6      (lines starting with '#' are skipped)
Output per graph: YOK = no 4-regular subgraph (infeasible), VAR = one exists,
BILINMIYOR = time limit reached.  Needs: pip install ortools pulp.
"""
import sys, time
from ortools.sat.python import cp_model
import pulp
def dec(s):
    if ord(s[0])==126:
        n=((ord(s[1])-63)<<12)|((ord(s[2])-63)<<6)|(ord(s[3])-63); s=s[3:]
    else: n=ord(s[0])-63
    bits=[(ord(c)-63)>>(5-k)&1 for c in s[1:] for k in range(6)]
    pairs=[(i,j) for j in range(1,n) for i in range(j)]
    return n,[p for p,b in zip(pairs,bits) if b]
def cpsat(n,E,sn):
    m=cp_model.CpModel()
    x=[m.NewBoolVar(f"x{k}") for k in range(len(E))]; y=[m.NewBoolVar(f"y{v}") for v in range(n)]
    inc=[[] for _ in range(n)]
    for k,(i,j) in enumerate(E): inc[i].append(x[k]); inc[j].append(x[k])
    for v in range(n): m.Add(sum(inc[v])==4*y[v])
    m.Add(sum(y)>=1)
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=sn; s.parameters.num_search_workers=1
    r=s.Solve(m)
    return {cp_model.INFEASIBLE:'YOK', cp_model.OPTIMAL:'VAR', cp_model.FEASIBLE:'VAR'}.get(r,'BILINMIYOR')
def cbc(n,E,sn):
    p=pulp.LpProblem("d",pulp.LpMinimize)
    x=[pulp.LpVariable(f"x{k}",cat="Binary") for k in range(len(E))]; y=[pulp.LpVariable(f"y{v}",cat="Binary") for v in range(n)]
    p+=pulp.lpSum([])
    inc=[[] for _ in range(n)]
    for k,(i,j) in enumerate(E): inc[i].append(x[k]); inc[j].append(x[k])
    for v in range(n): p+=pulp.lpSum(inc[v])==4*y[v]
    p+=pulp.lpSum(y)>=1
    p.solve(pulp.PULP_CBC_CMD(msg=0,timeLimit=sn,threads=1))
    st=pulp.LpStatus[p.status]
    return {'Infeasible':'YOK','Optimal':'VAR'}.get(st,'BILINMIYOR('+st+')')
sn=float(sys.argv[1]) if len(sys.argv)>1 else 120
for line in sys.stdin:
    g=line.strip()
    if not g or g.startswith('#'): continue
    n,E=dec(g)
    t=time.time(); a=cpsat(n,E,sn); ta=time.time()-t
    t=time.time(); b=cbc(n,E,sn); tb=time.time()-t
    print(f"n={n} m={len(E)} cpsat={a} ({ta:.1f} s) cbc={b} ({tb:.1f} s)", flush=True)
