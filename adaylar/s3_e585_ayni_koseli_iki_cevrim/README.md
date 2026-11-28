# S3. Erdős #585: no two edge-disjoint cycles on the same vertex set

**Status: candidate (ADAY_YENI).** Computed 2026-11-28. Reported in
[teorth/erdosproblems issue #563](https://github.com/teorth/erdosproblems/issues/563); not submitted to the OEIS.

**Credit.** The values a(1)..a(10) = 0, 1, 3, 6, 9, 12, 16, 19, 23, 27 were already published in
the working report "Erdős Problem #585: Same-vertex-set cycles — working report"
(https://erdosproblemaday.com/report/585, 2026-07-28; built by Patrick White with Claude). That
report also gives the lower bound a(11) >= 30. Here those ten values were recomputed with
independent code. **New in this work:**
- a(11) = 31, computed by two methods;
- a(12) = 36, from the certified ladder (method (c));
- a(13) = 39: the upper bound is method (d), the lower bound is the construction below;
- the number of extremal graphs (isomorphism classes) for n <= 12;
- the structure of the extremal graphs: for 2 <= n <= 13, a(n) = 2n - 3 + A006856(n - 2), and the
  join of K_2 with an extremal graph of girth >= 5 is extremal (section "Structure");
- lower bounds from that construction: a(14) >= 43, a(15) >= 48, a(16) >= 52, a(17) >= 56,
  a(18) >= 61, and a(n) >= 4n - 12 for every n >= 17;
- these graphs have no 4-regular subgraph at all, so the same values and bounds hold for the
  maximum number of edges of a graph with no 4-regular subgraph (equal to a(n) for n <= 13);
- a second construction, K_2 joined with the incidence graph of a linear triple system, gives
  a(n) >= 5n - O(sqrt(n)), for example a(41) >= 157 (useful for moderate n only: for large n the
  known bound c n log log n is larger).

## Definition

Problem [585](https://www.erdosproblems.com/585) (open) asks for the maximum number of edges in a
graph on n vertices that contains no two edge-disjoint cycles with the same vertex set. Call a
simple graph G *good* if no vertex set S (|S| >= 3) spans two edge-disjoint Hamiltonian cycles of
G[S]. Then a(n) is the maximum number of edges of a good graph on n vertices. Goodness is preserved
when edges or vertices are deleted.

Because of this closure, two facts determine a(n) = F: (i) some good graph has F edges, and
(ii) no good graph has exactly F + 1 edges.

Some easy facts:
- The union of the two cycles is 4-regular on S, so |S| >= 5.
- a(n) = C(n,2) for n <= 4.
- K5 has two edge-disjoint Hamiltonian cycles, so it is bad, and a(5) = 9.

## Terms

| n | a(n) | (a) geng scan: graphs with a(n) edges / good | (a) graphs with a(n)+1 edges / good | (b) extension ladder: max edges | extremal classes (a) = (b) |
|---|---|---|---|---|---|
| 1 | 0 | 1 / 1 | – | 0 | 1 |
| 2 | 1 | 1 / 1 | – | 1 | 1 |
| 3 | 3 | 1 / 1 | – | 3 | 1 |
| 4 | 6 | 1 / 1 | – | 6 | 1 |
| 5 | 9 | 1 / 1 | 1 / 0 | 9 | 1 |
| 6 | 12 | 5 / 3 | 2 / 0 | 12 | 3 |
| 7 | 16 | 21 / 1 | 10 / 0 | 16 | 1 |
| 8 | 19 | 402 / 12 | 221 / 0 | 19 | 12 |
| 9 | 23 | 10120 / 8 | 5995 / 0 | 23 | 8 |
| 10 | 27 | 596191 / 7 | 395166 / 0 | 27 | 7 |
| 11 | **31** | 27749332 (min degree >= 4) / 8 | 2173681 (min degree >= 5) / 0 | 31 | 8 |
| 12 | **36** | – | – | 36 (method (c)) | 1 (method (c)) |
| 13 | **39** | – | – | 39: reached by K_2 v H (section "Structure"); 40 edges excluded by method (d) | not classified; at least 126 |

The n = 12 row comes only from method (c). The n = 13 row comes from method (d) and the join
construction.

- Method (a) scans every graph with the given number of edges.
- Method (b) builds every good graph above a threshold, so it gives the maximum edge count directly.
- For every n <= 11, the two methods give the same graph6 list of extremal graphs after canonical
  labelling with `nauty-labelg`. The lists are in `tanik/uc_n<n>_m<a(n)>.g6`.
- For 4 <= n <= 10, a(n) - a(n-1) is 3 or 4.
- a(11) = 31 is one more than the bound a(11) >= 30 in the report.
- Good 11-vertex graphs with exactly 30 edges: 1780 classes, by both methods. Method (a) uses
  `geng -d3 11 30:30`, 68718688 graphs; minimum degree >= 30 - 27 = 3 by the argument below. The
  two lists are identical (`tanik/n11_m30_iyi.g6`).
- Running times on this machine (8 cores, shared, 3 parallel parts): n <= 10 takes seconds. At
  n = 11 the 32-edge scan takes 25 s, the 31-edge scan 4 min and the 30-edge scan 7 min. The
  ladder takes about 70 s.

## Structure: two universal vertices plus a graph of girth at least 5

Write K_2 v H for the join: two new adjacent vertices, each joined to every vertex of H. Write
A006856(k) for the maximum number of edges of a graph on k vertices with no 3-cycle and no 4-cycle
([OEIS A006856](https://oeis.org/A006856); set A006856(0) = 0).

**Observation.** For 2 <= n <= 13,

    a(n) = 2n - 3 + A006856(n - 2).

- For 2 <= n <= 12, `yapi.py` reads the extremal graphs in `tanik/` and finds graphs of the form
  K_2 v H, with H free of 3-cycles and 4-cycles, among them: 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1 classes
  for n = 2..12. These are the numbers of extremal graphs of girth >= 5 on 0..10 vertices
  ([OEIS A159847](https://oeis.org/A159847)). So for these n, K_2 v H is extremal for every
  extremal H.
- At n = 7 the extremal graph is K_2 v C_5. The report describes it as K_7 minus a 5-cycle, which
  is the same graph.
- At n = 12 the only extremal graph is K_2 v Petersen. The check is by canonical labelling:
  `nauty-geng -tf 10 15:15 | python3 yapi.py --join | nauty-labelg` gives `tanik/uc_n12_m36.g6`.
- For 6 <= n <= 11 there are also extremal graphs that are not of this form (1, 0, 10, 7, 6, 7
  classes).
- At n = 13 the value 39 = 23 + 16 is reached by K_2 v H for the 3 extremal graphs H on 11
  vertices (`tanik/birlesim_n13_m39.g6`).

**Lemma.** Let H be a triangle-free graph in which every set of t >= 4 vertices spans at most
2t - 5 edges. Then K_2 v H is good.

*Proof.* Let u, v be the two joined vertices. Suppose two edge-disjoint cycles have the same vertex
set S, and let U be their union. U is 4-regular on S, so it has 2|S| edges and |S| >= 5. Put
T = S \ {u, v}, t = |T| and j = |S ∩ {u, v}|. At most 4j edges of U meet {u, v}. So at least
2(t + j) - 4j = 2t - 2j >= 2t - 4 edges of U lie inside T, and these are edges of H. If t >= 4,
this contradicts the hypothesis. If t <= 3, then |S| = 5, so U = K_5 and T spans a triangle of H. ∎

**Consequences.**
- The case t = 4 of the hypothesis says that H has no 4-cycle. For 4 <= t <= 14 the values
  A006856(t) = 3, 5, 6, 8, 10, 12, 15, 16, 18, 21, 23 are all at most 2t - 5. So every graph of
  girth >= 5 on at most 14 vertices satisfies the hypothesis, and for 3 <= n <= 16

      a(n) >= 2n - 3 + A006856(n - 2).

  This gives a(13) >= 39, a(14) >= 43, a(15) >= 48 and a(16) >= 52.
- K_2 v K_3 = K_5 and K_2 v C_4 are bad. So on at most 16 vertices, the good graphs with two
  adjacent universal vertices are exactly the graphs K_2 v H with H of girth >= 5.
- **n >= 17.** For every k >= 15 there is a graph H_k on k vertices with 2k - 5 edges that satisfies
  the hypothesis. So a(n) >= 2n - 3 + 2(n - 2) - 5 = 4n - 12 for n >= 17.
  - H_15 is the extremal graph of girth >= 5 on 15 vertices (26 edges) minus one edge.
  - H_{k+1} is H_k plus a new vertex joined to two vertices at distance >= 3 (or in different
    components). By induction H_k has no 3-cycle and no 4-cycle. So such a pair exists unless H_k
    is connected with diameter <= 2, and a graph of diameter <= 2 with no 3-cycle and no 4-cycle
    is a star or a Moore graph (C_5, Petersen, Hoffman–Singleton, or a 57-regular graph on 3250
    vertices). A star has k - 1 edges, and the Moore graphs with 2k - 5 edges are C_5 and Petersen
    only, so none of these has k >= 15 vertices and 2k - 5 edges.
  - The new vertex creates no 3-cycle and no 4-cycle, and a set of t >= 5 vertices containing it
    spans at most 2(t - 1) - 5 + 2 = 2t - 5 edges. So H_{k+1} satisfies the hypothesis.
  - For comparison, adding vertices of degree 3 gives only 3n - 6 (the lower bound in the report).
- **The hypothesis cannot be weakened to 2t - 4 at t = 15.** A006856(15) = 26 = 2 * 15 - 4, and the join of K_2 with
  the unique extremal graph on 15 vertices is bad: all 17 vertices carry two edge-disjoint
  Hamiltonian cycles (`tanik/birlesim_n17_m57_kotu.txt`, checked by `sertifika_dogrula.py`). So
  this construction gives a(17) >= 56, not 57.
- **n = 18.** A006856(16) = 28 = 2 * 16 - 4, and there are 22 extremal graphs. Let H be one of them
  with minimum degree 3 and a vertex x of degree >= 5 (3 of the 22). Then K_2 v H has no 4-regular
  subgraph, so a(18) >= 33 + 28 = 61. Follow the proof of the Lemma:
  - a set T of at most 14 vertices spans at most 2t - 5 edges;
  - a set of 15 vertices spans at most 28 - 3 = 25 = 2t - 5 edges;
  - if T is all of H, at least 2t - 2j = 32 - 2j edges of U lie inside T, and H has only 28 edges.
    So j = 2 and U contains all 28 edges of H. Then x has degree >= 5 in U.
- The equality cannot continue for large n: A006856(k) grows like k^(3/2), while
  a(n) <= n (log n)^O(1) by Chakraborti, Janzer, Methuku and Montgomery. Whether equality holds
  for n = 14, 15, 16 is not known. At n = 17 the construction is one short of the formula.

**No 4-regular subgraph.** The proof of the Lemma uses only that U is 4-regular. So under the
hypothesis of the Lemma, K_2 v H has no 4-regular subgraph at all. Write r(n) for the maximum number
of edges of a graph on n vertices with no 4-regular subgraph. Then:
- r(n) <= a(n) for every n, because the union of two edge-disjoint cycles on the same vertex set
  is 4-regular;
- every lower bound in this section is a lower bound for r(n);
- r(n) = a(n) for n <= 13.

`dort_duzenli.py` looks for a 4-regular subgraph by integer programming. It shares nothing with
`e585.c`. Results (`out/dort_duzenli.log`):
- none in the 45 extremal graphs for n <= 12 (so for n <= 12 the two problems have the same
  extremal graphs);
- none in the joins behind the bounds for n = 13..18;
- one in the 57-edge join at n = 17 (all 17 vertices).

**Proposition (triple systems).** Let H be a bipartite graph with parts A and B and no 4-cycle, in
which every vertex of B has degree at most 3. The degrees in A are arbitrary. (H is the incidence
graph of a linear hypergraph with edges of size at most 3: A is the set of points, B the set of
edges.) Then K_2 v H has no 4-regular subgraph. In particular it is good.

*Proof.* Let U be a 4-regular subgraph with vertex set S. Put T = S \ {u, v}, a = |T ∩ A|,
b = |T ∩ B| and j = |S ∩ {u, v}|, and let m be the number of edges of U inside T. As in the Lemma,
m >= 2(a + b) - 2j >= 2a + 2b - 4. Every edge of U inside T joins A to B.
1. Every vertex of T ∩ A has degree 4 in U, so m <= 4a. Hence b <= a + 2.
2. For x in T ∩ B let d(x) <= 3 be the number of its U-neighbours in A. Let p be the number of x
   with d(x) = 3 and r the number of x with d(x) <= 1. Then m <= 3p + 2(b - p - r) + r, so
   p >= 2a - 4 + r.
3. m <= 3b gives b >= 2a - 4. With step 1, a <= 6.
4. The p vertices with d(x) = 3 give p triples of points of T ∩ A, and two of them share at most
   one point, because H has no 4-cycle. On a = 3, 4, 5, 6 points there are at most 1, 1, 2, 4 such
   triples, fewer than 2a - 4 = 2, 4, 6, 8. So a <= 2 and p = 0.
5. a = 2: by step 2, r = 0, so every x in T ∩ B is joined to both points of T ∩ A. There is at
   most one such x, as H has no 4-cycle. So |S| <= 5, U = K_5, and the two points of T ∩ A would be
   adjacent. a = 1: every x has d(x) <= 1, so b = r <= 2 by step 2; then |S| <= 5, U = K_5, and two
   vertices of B would be adjacent. a = 0: m = 0, so b <= j <= 2 and |S| <= 4. Each case is
   impossible. ∎

**Consequences.**
- If there is a linear triple system with a points and b triples, then for n = a + b + 2

      a(n) >= r(n) >= 2a + 5b + 1.

  The largest b is the packing number D(a) = 0, 0, 0, 1, 1, 2, 4, 7, 8, 12, 13, 17, 20, 26, ...
  for a = 0, 1, 2, ... ([OEIS A001839](https://oeis.org/A001839)); for a Steiner triple system
  b = a(a - 1)/6.
- For every n, taking the least a with a + D(a) >= n - 2 gives a(n) >= 5n - 9 - 3a, which is
  5n - O(sqrt(n)).
- This is a statement for small and moderate n. For large n the graphs of Pyber, Rödl and
  Szemerédi have no 4-regular subgraph and c n log log n edges, which is more.
- This is better than 4n - 12 for n = 34 and for every n >= 37 (equal for n = 30, 33, 36).
  Examples: a(41) >= 157 from STS(13) and a(78) >= 324 from STS(19).
- Checks: `e585` finds the joins good for the largest packings on 3..7 points (n <= 16) and for 75
  random linear systems with edges of size 2 and 3; `dort_duzenli.py` finds no 4-regular subgraph
  in the joins of the Fano plane, STS(9), STS(13) and STS(19) (`tanik/uclu_*.g6`).
- Leaves of degree 4 do not work in general: for the projective plane of order 3 minus two lines,
  the join has a 4-regular subgraph.

**Best lower bounds from these constructions.**

| n | 14 | 15 | 16 | 17 | 18 | 19 <= n <= 33 | 34 | 35 | 36 | 37 | 38 | 39 | 40 | 41 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a(n) >= | 43 | 48 | 52 | 56 | 61 | 4n - 12 | 125 | 128 | 132 | 137 | 142 | 147 | 152 | 157 |

None of these is known to be the exact value.

**Computer checks of the lemma (`birlesim.sh`, `out/birlesim.log`).**
- k = 3..11: K_2 v H is good for every graph H of girth >= 5 (3, 6, 11, 23, 48, 114, 293, 869 and
  2963 graphs).
- k = 12, 13, 14: K_2 v H is good for every extremal H (7, 1 and 4 graphs).
- k = 15: K_2 v H is bad for the extremal H (see above). K_2 v (H - e) is good for every edge e
  (9 classes, `tanik/birlesim_n17_m56.g6`).
- k = 16: the 3 joins with 61 edges are good (`tanik/birlesim_n18_m61.g6`, about 3 minutes per
  graph).

## Methods

**Checker `e585.c`.**
- For each graph it takes the 4-core of G and goes through every subset S of the core with
  |S| >= 5. In such an S every vertex has at least 4 neighbours in S and G[S] has at least 2|S|
  edges.
- It enumerates the Hamiltonian cycles C1 of G[S], each undirected cycle once. For each C1 it runs
  a depth-first search for a Hamiltonian cycle of G[S] - E(C1).
- For a bad graph it prints a witness (S, C1, C2).
- Leak tests:
  - n = 0, the 1-vertex graph, a single edge, the empty graph on 5 vertices, K4 and K5 - e are all
    good.
  - K5 is bad, with witness `C1=0-1-2-3-4-0 C2=0-2-4-1-3-0`.

**Reference checker `e585_ref.py` (pure Python).** It shares no code with `e585.c`. For every S it
lists all Hamiltonian cycles by permutations, stores them as edge sets, and looks for two disjoint
ones.
- It agrees with `e585.c` on every graph with n <= 8: 1 + 2 + 4 + 11 + 34 + 156 + 1044 + 12346
  graphs, of which 0, 0, 0, 0, 1, 8, 90 and 1834 are bad.
- At n = 11 it was compared on a **sample** of 20000 graphs drawn at random from `geng -d4 11 31:31`
  (seeded `shuf`), plus the 8 extremal graphs (`out/orneklem_n11.txt`). This is a sample, not an
  exhaustive second check.

**Method (a): exhaustive `nauty-geng` scan (`yontem_a.sh`, `f11_tarama.sh`).**
- For n <= 10, every graph with a(n) edges and every graph with a(n) + 1 edges is checked.
- For n = 11 the scan is restricted by minimum degree. Suppose G is good on 11 vertices with M edges
  and v has degree d. Then G - v is good on 10 vertices with M - d edges, so M - d <= a(10) = 27,
  which gives d >= M - 27.
  - M = 32: every good graph has minimum degree >= 5, so `geng -d5 11 32:32` is complete. It
    contains no good graph, so a(11) <= 31.
  - M = 31: `geng -d4 11 31:31` is complete and contains 8 good classes, so a(11) >= 31.
  - M = 30: `geng -d3 11 30:30` is complete and contains 1780 good classes.

**Method (b): vertex-extension ladder (`yontem_b.sh`, `e585 extend`).** This method does not use
geng.
- L_n is the set of all good graphs on n vertices with at least t_n edges, up to isomorphism
  (`nauty-labelg | sort -u`). The thresholds satisfy t_{n-1} = t_n - floor(2 t_n / n).
- Completeness: a good graph with m >= t_n edges has a vertex of minimum degree d <= floor(2m/n).
  Deleting it leaves a good graph with m - d >= t_{n-1} edges, because m - floor(2m/n) is
  nondecreasing in m. So every member of L_n is obtained from L_{n-1} by adding a vertex of minimum
  degree.
- When a vertex is added, only the sets S containing the new vertex are tested (`check -l`). This is
  sound because the parent graph is good.
- Run with t_11 = 30. The class counts are 1, 1, 2, 4, 13, 46, 287, 2115, 25398, 29979, 1788 for
  n = 1..11. The largest edge count in L_n is a(n) for every n.

**Certified upper bounds (`e585 check -c`, `sertifika_dogrula.py`).**
- For every bad graph, `check -c` prints one line `graph6 S C1 C2`, where C1 and C2 are vertex
  sequences.
- `sertifika_dogrula.py` is about 40 lines and imports nothing from `e585.c`. It checks three
  things:
  1. C1 and C2 are cycles whose edges are all in the graph.
  2. C1 and C2 have the same vertex set S.
  3. C1 and C2 have no common edge.
- With the graph6 file passed as an argument, it also checks that every generated graph has a
  certificate.
- Results (`out/sertifika.log`):
  - n = 10, 28 edges: 395166 graphs, 395166 valid certificates, 0 errors.
  - n = 11, `-d5 11 32:32`: 2173681 graphs, 2173681 valid certificates, 0 errors.
  - The two runs took 33 s and 154 s.
- So a(10) <= 27 and a(11) <= 31 depend only on three things: the completeness of nauty-geng, the
  minimum-degree argument, and this short verifier. The certificates are not stored, because they
  can be regenerated in a few minutes.
- The lower bounds rest on explicit good graphs in `tanik/`. Their goodness is confirmed by
  `e585_ref.py`.

**Method (c): certified ladder, n <= 13 (`yontem_c.sh`).** This is method (b) run in a form in
which no "bad" verdict is trusted.
- Every candidate is generated with `e585 extend -a`, which outputs all candidates and does no test.
- Every candidate is then classified with `check -C -l`.
  - A good candidate goes into L_n.
  - A bad candidate gets a certificate: two edge-disjoint cycles on one vertex set. Each certificate
    is checked by `sertifika_dogrula.py`.
  - So L_n is complete given L_{n-1}.
  - A wrong "good" verdict can only make L_n larger. It cannot break an upper bound.
- **n = 12.** The chain uses the thresholds t = 0, 1, 2, 4, 6, 9, 12, 16, 20, 25, 30, 35 for
  n = 1..12 (`out/yontem_c_n12_t35.log`).
  - Each step satisfies t_{n-1} <= t_n - floor(2 t_n / n); the script checks this.
  - All 445150 certificates are valid and there are 0 errors.
  - L_11(30) is reproduced (1780 + 8 classes). This classification is now certified as well, and no
    longer depends on the 68M-graph `-d3` scan.
  - L_12(35) has 28 classes with 35 edges and 1 class with 36 edges. So **a(12) = 36**, with one
    extremal graph, `tanik/uc_n12_m36.g6`.
- **n = 13.** Extending L_12(35) with t_13 = 41 (41 - floor(82/13) = 35) gives 792 candidates.
  All 792 are certified bad, so a(13) <= 40 (`out/yontem_c_n13_t41.log`).
  - Lower bound: extending L_12 to 39 edges gives 126 good classes,
    `tanik/n13_m39_iyi_altsinir.g6`. These are witnesses only, not a classification.
  - The ladder alone would need the full L_12(34) to decide 40. Method (d) below decides it in
    another way.
- **Independent check of the lower bounds.** `e585_ref2.py` is pure Python: it does a DFS
  enumeration of all Hamiltonian cycles per vertex set and tests every pair.
  - It agrees with `e585.c` on all graphs with n <= 8.
  - It confirms the 8 extremal graphs at n = 11, the extremal graph at n = 12 and all 126 39-edge
    witnesses at n = 13 (`out/ref2.txt`).

**Method (d): no good graph on 13 vertices has 40 edges (`yontem_d.sh`).** Let G be good on 13
vertices with 40 edges, and let v be a vertex of minimum degree d. Then d <= floor(80/13) = 6, and
G - v is good on 12 vertices with 40 - d <= a(12) = 36 edges. So d is 4, 5 or 6.
- **d = 4 or 5.** G - v has 36 or 35 edges, so it is one of the 29 graphs of L_12(35) from
  method (c). G is obtained from it by adding a vertex of minimum degree (`e585 extend 40 -a`).
  This gives 10093 candidates: 9301 with 40 edges and 792 with 41 edges. All 10093 have a valid
  certificate.
- **d = 6.** Every degree is at least 6 and the degree sum is 80, so every degree is at most 8.
  These graphs are generated by `nauty-geng -d6 -D8 13 40:40`, in 256 parts: 23489426 graphs.
  All have a valid certificate (0 errors, 0 missing).
- So a(13) <= 39 (`out/yontem_d.log`). With the lower bound from K_2 v H this gives **a(13) = 39**.
- The d = 6 part depends on the completeness of nauty-geng, as method (a) does. The d = 4, 5 part
  depends on L_12(35) from the certified ladder.
- Check of the generator: `nauty-geng -d6 -D6 13 39:39` gives 367860 graphs, the known number of
  6-regular graphs on 13 vertices ([OEIS A165627](https://oeis.org/A165627)).
- The extremal graphs at n = 13 are not classified here. 126 classes are known
  (`tanik/n13_m39_iyi_altsinir.g6`); 3 of them are the joins K_2 v H
  (`tanik/birlesim_n13_m39.g6`).

**Shared parts.** Methods (a) and (b) share the Hamiltonian-cycle routine of `e585.c`. For n <= 8,
that routine is checked against `e585_ref.py`.

## Collision check (K1, 2026-11-28)

| source | query | result |
|---|---|---|
| erdosproblems.com/585 + forum thread | page and comments | open; 0 comments; no small values; "OEIS: possible" |
| teorth/erdosproblems `data/problems.yaml` | entry 585 | open, `oeis: possible`, unformalized |
| google-deepmind/formal-conjectures | local clone, `gh search prs 585` | no 585.lean on main; open PR #6774 adds one (bounds only, no small values) |
| OpenAlex / arXiv 2404.07190 full text | "edge-disjoint cycles with the same vertex set" | Chakraborti–Janzer–Methuku–Montgomery bounds; no small-n table |
| OpenAlex | "dense graphs without 3-regular subgraphs" | Pyber–Rödl–Szemerédi (1995); no small-n table |
| local OEIS snapshot (2026-01, 392167 sequences) | 0,1,3,6,9,12,16,19,23,27 and sub-windows; 9,...,27,31; 1,3,1,12,8,7,8 | no match (A053096 and A072567 share only short windows) |
| live OEIS (browser, 2026-11-28) | 0,1,3,6,9,12,16,19,23,27 | no match; closest A220657 differs in one term |
| web (Exa) | "Erdős 585 small values" | **erdosproblemaday.com/report/585: a(1..10) published, a(11) >= 30** |
| erdosproblems.ai/problems/585 | page | no exact values |
| erdosproblemaday.com/report/585 | structure: "Petersen", "girth", "join", "universal", "A006856", general constructions | none of these; the only general bound is 3n - 6 (add vertices of degree 3); G_7 is described as K_7 minus a 5-cycle |
| arXiv 2404.07190, arXiv 2410.02437 (Janzer–Steiner–Sudakov) | small cases, join constructions | asymptotic results only |
| web (Exa) | "two universal vertices joined to a girth five graph", "K_2 join Petersen", same-vertex-set cycles | no match |
| local OEIS snapshot | 0,1,2,3,5,6,8,10,12,15,16,18,21,23 and 1,1,1,2,1,2,1,1,1,1,3,7,1,4,1,22 | A006856 and A159847 (used above) |

## Known bounds

- Lower bound: Pyber, Rödl and Szemerédi (J. Combin. Theory Ser. B 63 (1995) 41–54) give graphs
  with about c n log log n edges and no 4-regular subgraph.
- Upper bound: Chakraborti, Janzer, Methuku and Montgomery (Adv. Math. 469 (2025) 110228,
  arXiv:2404.07190) show that n (log n)^{O(1)} edges force such a pair of cycles.

## Reproduce

```
./run.sh        # compiles, runs every check; about 15 minutes on a shared 8-core machine
```

Single checks:

```
gcc -O3 -o e585 e585.c
nauty-geng -q 10 28:28 | ./e585 check -q            # graphs=395166 good=0 -> a(10) <= 27
nauty-geng -q -d5 11 32:32 | ./e585 check -q        # graphs=2173681 good=0 -> a(11) <= 31
./e585 check < tanik/uc_n11_m31.g6                  # 8 lines iyi=1 kenar=31
python3 e585_ref.py < tanik/uc_n11_m31.g6           # same, independent checker (about 1 min per graph)
nauty-geng -q -d5 11 32:32 > m32.g6 && ./e585 check -c < m32.g6 | python3 sertifika_dogrula.py m32.g6   # valid=2173681 errors=0 missing=0
./yontem_b.sh /tmp/ladder 11 30 && cat /tmp/ladder/yontem_b.log
./yontem_c.sh /tmp/c12 "1:0 2:1 3:2 4:4 5:6 6:9 7:12 8:16 9:20 10:25 11:30 12:35"   # a(12) = 36, about 3 min
./yontem_d.sh /tmp/d13 /tmp/c12/L12.g6        # a(13) <= 39, about 20 min with 3 jobs
python3 yapi.py tanik/uc_n*_m*.g6             # join form and 2n - 3 + A006856(n - 2)
./birlesim.sh /tmp/join                       # joins K_2 v H for k <= 14, about 2 min
python3 dort_duzenli.py < tanik/uclu_sts13_n41_m157.g6   # four_regular_subgraph=0 (needs scipy)
```

## Files

- `e585.c`: checker and extension (`check`, `extend`).
- `e585_ref.py`: independent reference checker.
- `sertifika_dogrula.py`: independent certificate verifier.
- `e585_ref2.py`: second independent checker (DFS enumeration of Hamiltonian cycles).
- `yontem_c.sh`: method (c), the certified ladder.
- `yontem_d.sh`: method (d), a(13) <= 39.
- `yapi.py`: join form of the extremal graphs; `--join` builds K_2 v H.
- `birlesim.sh`: computer checks of the lemma.
- `dort_duzenli.py`: looks for a 4-regular subgraph by integer programming (needs scipy).
- `yontem_a.sh`: method (a) for n <= 10.
- `f11_tarama.sh`: method (a) for n = 11.
- `yontem_b.sh`: method (b).
- `run.sh`: runs everything.
- `tanik/uc_n<n>_m<a(n)>.g6`: all extremal graphs (canonical graph6), n <= 12.
- `tanik/birlesim_n<n>_m<m>.g6`: the joins K_2 v H for the extremal H on n - 2 vertices, n = 13..16
  (and n = 18: the 3 joins with 61 edges).
- `tanik/birlesim_n17_m56.g6`: K_2 v (H - e) for the extremal H on 15 vertices, one graph per edge orbit.
- `tanik/birlesim_n17_m57_kotu.txt`: certificate that the 57-edge join at n = 17 is bad.
- `tanik/uclu_*.g6`: K_2 v (incidence graph) for the Fano plane, STS(9), STS(13) and STS(19).
- `out/`: logs.
- `oeis_draft.txt`: OEIS draft.
