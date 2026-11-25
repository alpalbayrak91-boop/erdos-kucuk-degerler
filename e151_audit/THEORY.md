# Even-Cycle-Free Extremal Graphs (`A032766`), False Prefix Match (`A380408`), and Disambiguation from Erdős #151

## 1. Honest Scope & Problem Disambiguation

This module documents a formal and computational audit resolving two distinct questions that must **not** be conflated:

1. **Erdős Problem #151 (Erdős–Gallai–Tuza Clique Transversal Conjecture, `FormalConjectures/ErdosProblems/151.lean`)**:
   - Let $\tau(G)$ be the minimum number of vertices meeting every maximal clique of $G$ of size $\ge 2$, and let $H(n)$ be the largest integer such that every triangle-free $n$-vertex graph contains an independent set of size $H(n)$ (related to off-diagonal Ramsey numbers $R(3, k)$).
   - Erdős #151 asks whether $\tau(G) \le n - H(n)$ for every $n$-vertex graph $G$.
   - **Important:** This module does *not* claim progress on Erdős #151; `even_cycle_audit.py` only performs a small-$n$ sanity check ($n = 1 \dots 5$) of $\tau(G) \le n - H(n)$ to illustrate the exact definition alongside the extremal cycle audit below.

2. **Even-Cycle-Free Extremal Graph Function $\mathrm{ex}(n, \{C_4, C_6, \dots\})$ and OEIS `A032766` vs. `A380408`**:
   - A classical extremal graph result (folklore / block-cactus decomposition; often discussed alongside Erdős–Gallai cycle extremal problems) states that the maximum number of edges in an $n$-vertex simple graph containing no cycle of even length is:
     $$\mathrm{ex}(n, \{C_4, C_6, \dots\}) = \left\lfloor \frac{3(n - 1)}{2} \right\rfloor \quad (n \ge 1).$$
   - For $n = 1 \dots 8$, the values are:
     $$0, 1, 3, 4, 6, 7, 9, 10.$$
   - Because $0, 1, 3, 4, 6, 7, 9, 10, \dots$ agrees for the first **24 terms** ($0 \le k \le 23$, $n = 1 \dots 24$) with OEIS `A380408` ($a(k) = \sum_{j \ge 0} \lfloor k / (2j)! \rfloor$), automated prefix lookups of small-$n$ tables easily misidentify the sequence as `A380408`.

---

## 2. Formal Lean 4 Results (`../formal/Erdos151EvenCycleA032766Audit.lean`)

All statements below are machine-checked in standalone Lean 4 (`lean --trust=0`, `0 sorry`, zero custom axioms):

1. **2-Connected Block Upper Bound (`even_cycle_free_upper_bound`)**:
   In any simple graph without even cycles, no 2-connected block can contain two cycles sharing an edge or >=2 vertices (theta graph $\implies$ even cycle), so every nontrivial block on $b$ vertices is either $K_2$ ($b = 2$, $1$ edge) or an odd cycle $C_b$ ($b \ge 3$ odd, $b$ edges). Each block satisfies $2 e(B) \le 3(b - 1)$ (`single_block_bound`). Summing over the block-cut forest ($\sum (b_i - 1) \le n - 1$) yields:
   $$\sum_i e(B_i) \le \left\lfloor \frac{3(n - 1)}{2} \right\rfloor.$$
2. **Friendship-Cactus Tightness (`friendship_cactus_matches_formula`)**:
   Attaching $\lfloor (n-1)/2 \rfloor$ edge-disjoint triangles at a central vertex $0$ (plus one pendant edge when $n$ is even) gives an even-cycle-free graph with $3\lfloor (n-1)/2 \rfloor + ((n-1) \bmod 2) = \lfloor 3(n-1)/2 \rfloor$ edges for every $n \ge 1$.
3. **Exact Bijection with OEIS `A032766` (`evenCycleFree_in_A032766`, `evenCycleFree_strict_mono`, `evenCycleFree_surjective_A032766`)**:
   As $n$ ranges over $\{1, 2, 3, \dots\}$, $\lfloor 3(n-1)/2 \rfloor$ is strictly increasing and hits *precisely* the nonnegative integers congruent to $0$ or $1 \pmod{3}$ — i.e., **OEIS `A032766`**.
4. **Refutation of `A380408` at Index 24 (`a380408_diverges_from_A032766_at_24`)**:
   At $k = 24$ ($n = 25$), $4! = 24$ contributes an extra $+1$ to `A380408`:
   $$\mathrm{A380408}(24) = 24 + \lfloor 24/2 \rfloor + \lfloor 24/24 \rfloor = 37 \neq 36 = \left\lfloor \frac{3(25 - 1)}{2} \right\rfloor = \mathrm{A032766}(24).$$

---

## 3. Reproducibility

```bash
lean --trust=0 formal/Erdos151EvenCycleA032766Audit.lean
python3 e151_audit/even_cycle_audit.py
```
