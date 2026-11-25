# Erdős #642: Exact Small Values for n ≤ 9 and Linear Lower-Bound Construction

## Definition (`FormalConjectures/ErdosProblems/642.lean`)

Let $G = (V, E)$ be a finite simple graph on $n$ vertices. A *chord* of a simple cycle $C$ of length $L = |V(C)| \ge 3$ is an edge of $G$ joining two non-consecutive vertices of $C$. Thus if $G[V(C)]$ denotes the subgraph induced by the vertex set of $C$, the number of chords of $C$ equals $|E(G[V(C)])| - L$.

Hamburger and Szegedy ([erdosproblems.com/642](https://www.erdosproblems.com/642)) asked whether $f(n) = O(n)$, where $f(n)$ (`Erdos642.maxEdges n`) is the maximum number of edges in an $n$-vertex simple graph in which every simple cycle has strictly more vertices than chords:

$$\text{chords}(C) < |V(C)| \iff |E(G[V(C)])| \le 2|V(C)| - 1 \quad \text{for every simple cycle } C \subseteq G.$$

Notice that for $L = 3$ ($\binom{3}{2} = 3 \le 5$) and $L = 4$ ($\binom{4}{2} = 6 \le 7$), the inequality holds automatically in *every* simple graph. Consequently, a graph $G$ violates the condition if and only if some vertex subset $S \subseteq V(G)$ of size $L \ge 5$ induces at least $2L$ edges and admits a Hamiltonian cycle.

---

## Exact Values for $n = 0 \dots 9$

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| $f(n)$ | 0 | 0 | 1 | 3 | 6 | 9 | 11 | 14 | 17 | 20 |
| Non-isomorphic extremal graphs | 1 | 1 | 1 | 1 | 1 | 1 | 8 | 1 | 1 | 1 |
| Extremal structure | $K_0$ | $K_1$ | $K_2$ | $K_3$ | $K_4$ | $K_5 - e$ | 8 graphs (incl. $K_{3,3} \cup P_3$) | $K_{4,3} \cup P_3$ | $K_{5,3} \cup P_3$ | $K_{6,3} \cup P_3$ |

Explicit edge lists for optimal witnesses on $n = 0 \dots 9$ are stored in [`witnesses_n0_to_9.json`](witnesses_n0_to_9.json) and raw canonical-enumeration output in [`results_exact_n2_to_9.txt`](results_exact_n2_to_9.txt).

---

## Proposition 1 (General $3n - 7$ Lower Bound; Proved)

For every integer $n \ge 3$,

$$f(n) \ge 3n - 7.$$

**Proof.** Partition $V(G_n) = A \sqcup B$ with $|A| = 3$ and $|B| = n - 3$. Put an induced path $P_3$ of $2$ edges on $A$, make $B$ an independent set, and add all $3(n - 3)$ edges between $A$ and $B$. Then $|E(G_n)| = 3(n - 3) + 2 = 3n - 7$.

Let $C$ be any simple cycle in $G_n$, with $a = |V(C) \cap A| \le 3$ and $b = |V(C) \cap B|$. Because $B$ is independent, no two consecutive vertices along $C$ both lie in $B$; walking around $C$ maps each vertex of $V(C) \cap B$ to its successor in $V(C) \cap A$ injectively. Hence $b \le a \le 3$, and $b \ge 1$ because $G_n[A] \cong P_3$ is acyclic. Thus $|V(C)| = a + b \le 6$:
- If $|V(C)| \le 4$, every simple graph on $|V(C)|$ vertices has $\le \binom{|V(C)|}{2} \le 2|V(C)| - 1$ edges.
- If $|V(C)| = 5$, we must have $a = 3, b = 2$, so $|E(G_n[V(C)])| = 3 \cdot 2 + 2 = 8 \le 2(5) - 1 = 9$.
- If $|V(C)| = 6$, we must have $a = 3, b = 3$, so $|E(G_n[V(C)])| = 3 \cdot 3 + 2 = 11 \le 2(6) - 1 = 11$.

Hence every cycle in $G_n$ has strictly fewer chords than vertices. $\blacksquare$

*(Remark: Replacing $P_3$ on $A$ by $K_3$ fails for $n \ge 6$ because $K_{3,3} \cup K_3$ has $12 = 2 \cdot 6$ edges on $6$ vertices and is Hamiltonian; similarly $K_{4,4}$ alone has $16 = 2 \cdot 8$ edges on $8$ vertices and is Hamiltonian. By canonical enumeration, $G_n = K_{3, n-3} \cup P_3$ is the **unique** extremal graph up to isomorphism for $n = 7, 8, 9$.)*

---

## Certification & Reproducibility

1. **Exact canonical-enumeration solver in C (`e642_exact.c`)**:
   - Uses degree + neighbor-degree signature bucketing and branch-and-bound canonical labeling (`uint64_t` upper-triangle bitmask), cross-checked on all unlabeled graphs for $n = 2 \dots 6$ against OEIS `A000088` (`2, 4, 11, 34, 156`).
   - Exploits the lossless hereditary minimum-degree relation: if $G$ on $n$ vertices with $m$ edges satisfies the cycle property and $v$ is a vertex of minimum degree $\delta \le \lfloor 2m/n \rfloor$, then $G - v$ is a valid $(n-1)$-vertex graph with $m - \delta$ edges.
   - Run:
     ```bash
     gcc -O3 -Wall -Wextra e642/e642_exact.c -o /tmp/e642_exact
     /tmp/e642_exact --test-canon
     /tmp/e642_exact 9
     ```
2. **Independent pure-Python verifier & branch-and-bound solver (`verify_e642.py`)**:
   - Independently enumerates all simple cycles of every witness in `witnesses_n0_to_9.json` to check $\text{chords}(C) < |V(C)|$ directly, cross-checks Held-Karp bitmask equivalence, and proves $f(0 \dots 8) = 0, 0, 1, 3, 6, 9, 11, 14, 17$ in pure Python (~0.5 s).
   - Run:
     ```bash
     python3 e642/verify_e642.py
     ```

## References

- P. Erdős, *Some recent problems and results in graph theory*, Discrete Math. **164** (1997), 81–85.
- G. Chen, P. Erdős, and W. Staton, *Proof of a conjecture of Bollobás on nested cycles*, J. Combin. Theory Ser. B **66** (1996), 38–43 ($f(n) \ll n^{3/2}$).
- N. Draganić, A. Methuku, D. Munhá Correia, and B. Sudakov, *Cycles with many chords*, Random Structures Algorithms **64** (2024), 3–16 ($f(n) \ll n (\log n)^8$).
