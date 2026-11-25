#!/usr/bin/env python3
"""Exact Z3 CEGAR solver and witness verifier for Erdos Problem #983: f(pi(n)+1, n).

Checks BOTH prime-set cardinality conventions:
  - f_le(n): least r such that every (pi(n)+1)-subset A of {1..n} has a prime set S
    with |S| <= r and numSmooth(A, S) > |S|.
  - f_eq(n): least r such that every (pi(n)+1)-subset A of {1..n} has a prime set S
    with |S| == r and numSmooth(A, S) > r (matching Erdos983.f in formal-conjectures).

Cross-checks:
  1. Verifies BOTH f_le and f_eq against independent direct brute-force on n = 2..16.
  2. Computes certified f_le(n) and f_eq(n) for n = 2..max_n with explicit adversarial
     witnesses A (of size pi(n)+1) proving f(n) > r - 1 and Z3 UNSAT certificates
     proving f(n) <= r.
"""
from __future__ import annotations

import itertools
import json
import sys
import time
from typing import List, Optional, Tuple


def primes_up_to(n: int) -> List[int]:
    out = []
    for p in range(2, n + 1):
        if all(p % d != 0 for d in range(2, int(p ** 0.5) + 1)):
            out.append(p)
    return out


def prime_factor_set(a: int) -> frozenset[int]:
    r = set()
    d = 2
    while d * d <= a:
        if a % d == 0:
            r.add(d)
            while a % d == 0:
                a //= d
        d += 1
    if a > 1:
        r.add(a)
    return frozenset(r)


def brute_e983_both(n: int) -> Tuple[int, int]:
    """Direct brute-force (for small n <= 16) matching f_le (|S| <= r) and f_eq (|S| == r)."""
    P = primes_up_to(n)
    k = len(P) + 1
    pf = {a: prime_factor_set(a) for a in range(1, n + 1)}
    sets_by_r = {r: [frozenset(S) for S in itertools.combinations(P, r)] for r in range(len(P) + 1)}
    worst_le = 0
    worst_eq = 0
    for A in itertools.combinations(range(1, n + 1), k):
        g_le = None
        g_eq = None
        for r in range(len(P) + 1):
            for S in sets_by_r[r]:
                cnt = sum(1 for a in A if pf[a] <= S)
                if cnt > r:
                    if g_eq is None:
                        g_eq = r
                    if g_le is None:
                        g_le = r
                    break
            if g_le is not None and g_eq is not None:
                break
        assert g_le is not None and g_eq is not None
        worst_le = max(worst_le, g_le)
        worst_eq = max(worst_eq, g_eq)
    return worst_le, worst_eq


def verify_adversarial_witness(n: int, A: List[int], r: int, exact_eq: bool) -> bool:
    """Pure-Python check that |A| = pi(n)+1 and NO prime set S of size <= r (or == r)
    has numSmooth(A, S) > |S|. Uses exact decomposition P = P_small u P_big where
    primes p > n/2 can only divide themselves inside {1..n}."""
    P = primes_up_to(n)
    k = len(P) + 1
    if len(A) != k or len(set(A)) != k or any(a < 1 or a > n for a in A):
        return False
    pf = {a: prime_factor_set(a) for a in A}
    P_small = [p for p in P if 2 * p <= n]
    P_big = [p for p in P if 2 * p > n]
    A_set = set(A)
    big_in_A = sum(1 for p in P_big if p in A_set)
    for s_len in range(min(r, len(P_small)) + 1):
        if exact_eq and (r - s_len) > len(P_big):
            continue
        for S_sm in itertools.combinations(P_small, s_len):
            S_set = frozenset(S_sm)
            sm_cnt = sum(1 for a in A if pf[a] <= S_set)
            if not exact_eq:
                if sm_cnt > s_len:
                    return False
            else:
                pad_gain = min(r - s_len, big_in_A)
                if sm_cnt + pad_gain > r:
                    return False
    return True


def cegar_can_exceed(n: int, r: int, exact_eq: bool) -> Tuple[bool, Optional[List[int]], int]:
    """Return (True, A, iters) if f(n) > r (counterexample A found), else (False, None, iters)."""
    from z3 import Bool, Implies, Or, PbEq, PbLe, Solver, sat, unsat

    P = primes_up_to(n)
    k = len(P) + 1
    P_small = [p for p in P if 2 * p <= n]
    P_big = [p for p in P if 2 * p > n]
    pf = {a: prime_factor_set(a) for a in range(1, n + 1)}

    s = Solver()
    x = {a: Bool(f"x_{a}") for a in range(1, n + 1)}
    s.add(PbEq([(x[a], 1) for a in range(1, n + 1)], k))

    for i in range(len(P_big) - 1):
        s.add(Implies(x[P_big[i + 1]], x[P_big[i]]))

    for slen in (0, 1):
        if slen > r or slen > len(P_small):
            continue
        if exact_eq and (r - slen) > len(P_big):
            continue
        for S_sm in itertools.combinations(P_small, slen):
            S_set = frozenset(S_sm)
            sm_elts = [a for a in range(1, n + 1) if pf[a] <= S_set]
            if not exact_eq:
                s.add(PbLe([(x[a], 1) for a in sm_elts], slen))
            else:
                if slen == r:
                    s.add(PbLe([(x[a], 1) for a in sm_elts], r))
                else:
                    c1 = PbLe([(x[a], 1) for a in sm_elts], slen)
                    c2 = PbLe([(x[a], 1) for a in (sm_elts + P_big)], r)
                    s.add(Or(c1, c2))

    iters = 0
    while True:
        iters += 1
        res = s.check()
        if res == unsat:
            return False, None, iters
        assert res == sat
        m = s.model()
        A = [a for a in range(1, n + 1) if bool(m.eval(x[a], model_completion=True))]
        A_set = set(A)
        big_in_A = sum(1 for p in P_big if p in A_set)

        viol = None
        for slen in range(min(r, len(P_small)) + 1):
            if exact_eq and (r - slen) > len(P_big):
                continue
            for S_sm in itertools.combinations(P_small, slen):
                S_set = frozenset(S_sm)
                sm_cnt = sum(1 for a in A if pf[a] <= S_set)
                if not exact_eq:
                    if sm_cnt > slen:
                        viol = (slen, S_set)
                        break
                else:
                    if sm_cnt + min(r - slen, big_in_A) > r:
                        viol = (slen, S_set)
                        break
            if viol is not None:
                break

        if viol is None:
            assert verify_adversarial_witness(n, A, r, exact_eq)
            return True, A, iters

        slen, S_set = viol
        sm_elts = [a for a in range(1, n + 1) if pf[a] <= S_set]
        if not exact_eq:
            s.add(PbLe([(x[a], 1) for a in sm_elts], slen))
        else:
            if slen == r:
                s.add(PbLe([(x[a], 1) for a in sm_elts], r))
            else:
                c1 = PbLe([(x[a], 1) for a in sm_elts], slen)
                c2 = PbLe([(x[a], 1) for a in (sm_elts + P_big)], r)
                s.add(Or(c1, c2))


def solve_n(n: int, exact_eq: bool, start_r: int = 0) -> Tuple[int, Optional[List[int]]]:
    r = max(0, start_r)
    best_witness = None
    while True:
        exceeds, witness, _ = cegar_can_exceed(n, r, exact_eq)
        if not exceeds:
            return r, best_witness
        best_witness = witness
        r += 1


def main() -> None:
    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 46
    t0 = time.time()

    for n in range(2, min(max_n, 16) + 1):
        bf_le, bf_eq = brute_e983_both(n)
        z_le, _ = solve_n(n, exact_eq=False)
        z_eq, _ = solve_n(n, exact_eq=True)
        assert bf_le == z_le and bf_eq == z_eq, (
            f"Mismatch at n={n}: bf=({bf_le},{bf_eq}) z3=({z_le},{z_eq})"
        )

    rows = []
    f_le_list = []
    f_eq_list = []
    diffs = []
    prev_le = 0
    for n in range(2, max_n + 1):
        r_start = max(0, prev_le - 1)
        val_le, wit_le = solve_n(n, exact_eq=False, start_r=r_start)
        if wit_le is None and val_le > 0:
            val_le, wit_le = solve_n(n, exact_eq=False, start_r=0)
        val_eq, wit_eq = solve_n(n, exact_eq=True, start_r=max(0, val_le - 1))
        if wit_eq is None and val_eq > 0:
            val_eq, wit_eq = solve_n(n, exact_eq=True, start_r=0)
        prev_le = val_le
        f_le_list.append(val_le)
        f_eq_list.append(val_eq)
        P = primes_up_to(n)
        es_ub = 2 * len(primes_up_to(int(n ** 0.5))) + 1
        row = {
            "n": n,
            "pi_n": len(P),
            "k": len(P) + 1,
            "f_le": val_le,
            "f_eq": val_eq,
            "erdos_straus_ub": es_ub,
            "lower_bound_witness_A": wit_eq,
        }
        if val_le != val_eq:
            diffs.append({**row, "witness_for_f_eq_gt_f_le": wit_eq})
        rows.append(row)

    out = {
        "n_range": [2, max_n],
        "brute_cross_check_2_to_16": "PASS",
        "f_le_seq": f_le_list,
        "f_eq_seq": f_eq_list,
        "divergences": diffs,
        "elapsed_s": round(time.time() - t0, 3),
        "rows": rows,
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
