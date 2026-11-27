"""Method C: exact model count with a compiled SDD (PySDD).

One Boolean variable per 3-subset of {0..m-1} (True = red). For each 4-set
{a,b,c,d} two clauses forbid "all four triples red" and "all four blue".
The CNF is compiled to an SDD and its models are counted; the count is
global over all C(m,3) variables. Usage: python s2_sdd.py MMAX
"""
import sys
from itertools import combinations

from pysdd.sdd import SddManager, Vtree


def count(m):
    triples = list(combinations(range(m), 3))
    if not triples:
        return 1
    var = {t: i + 1 for i, t in enumerate(triples)}
    nv = len(triples)
    vtree = Vtree(var_count=nv, var_order=list(range(1, nv + 1)), vtree_type="balanced")
    mgr = SddManager.from_vtree(vtree)
    mgr.auto_gc_and_minimize_on()
    f = mgr.true()
    for q in combinations(range(m), 4):
        lits = [mgr.literal(var[t]) for t in combinations(q, 3)]
        not_all_red = ~lits[0] | ~lits[1] | ~lits[2] | ~lits[3]
        not_all_blue = lits[0] | lits[1] | lits[2] | lits[3]
        f = f & not_all_red & not_all_blue
    wmc = f.wmc(log_mode=False)
    return int(wmc.propagate())


if __name__ == "__main__":
    for m in range(1, int(sys.argv[1]) + 1):
        print(m, count(m), flush=True)
