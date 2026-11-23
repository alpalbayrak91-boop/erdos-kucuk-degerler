"""T(n) = max number of triangles in an n-vertex graph where every edge lies in EXACTLY one triangle.
Equivalently: max family of triples (linear: two triples share <=1 vertex) such that the union graph
has no triangle other than the chosen triples. Exact via OR-tools CP-SAT (proves optimality).
e(n,2) of Erdos #600 = 3*T(n) + 1 (isolated vertices allowed)."""
import sys, itertools, time
from ortools.sat.python import cp_model

def solve(n, workers=8, tlimit=36000):
    V = range(n)
    triples = list(itertools.combinations(V, 3))
    m = cp_model.CpModel()
    x = {t: m.NewBoolVar(str(t)) for t in triples}
    pairs = list(itertools.combinations(V, 2))
    cont = {p: [t for t in triples if p[0] in t and p[1] in t] for p in pairs}
    # linearity: each pair in at most one triple
    for p in pairs:
        m.Add(sum(x[t] for t in cont[p]) <= 1)
    # no extra triangle: for non-chosen abc, cannot have ab,bc,ca each covered by a (different) triple
    for (a, b, c) in triples:
        for t1 in cont[(a, b)]:
            if t1 == (a, b, c): continue
            for t2 in cont[(b, c)]:
                if t2 == (a, b, c): continue
                for t3 in cont[(a, c)]:
                    if t3 == (a, b, c): continue
                    m.AddBoolOr([x[t1].Not(), x[t2].Not(), x[t3].Not()])
    # symmetry breaking: WLOG triple (0,1,2) chosen if n>=3
    if n >= 3: m.Add(x[(0, 1, 2)] == 1)
    m.Maximize(sum(x.values()))
    s = cp_model.CpSolver()
    s.parameters.num_workers = workers
    s.parameters.max_time_in_seconds = tlimit
    t0 = time.time()
    st = s.Solve(m)
    sol = [t for t in triples if s.Value(x[t])]
    return s.StatusName(st), int(s.ObjectiveValue()), int(s.BestObjectiveBound()), sol, time.time() - t0

def check(n, sol):
    import networkx as nx
    G = nx.Graph(); G.add_nodes_from(range(n))
    for a, b, c in sol: G.add_edges_from([(a, b), (b, c), (a, c)])
    tri = [tuple(sorted(c)) for c in nx.enumerate_all_cliques(G) if len(c) == 3]
    ok = sorted(tri) == sorted(sol) and G.number_of_edges() == 3 * len(sol)
    return ok, G.number_of_edges()

if __name__ == "__main__":
    for n in map(int, sys.argv[1:]):
        st, val, bd, sol, dt = solve(n)
        ok, E = check(n, sol)
        print(f"n={n} status={st} T={val} bound={bd} edges={E} e(n,2)={3*val+1} verified={ok} time={dt:.1f}s sol={sol}", flush=True)
