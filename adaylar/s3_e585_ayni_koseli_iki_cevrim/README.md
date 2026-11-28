# S3. Erdős #585: no two edge-disjoint cycles on the same vertex set

**Status: candidate (ADAY_YENI); not submitted anywhere.** Computed 2026-11-28.

**Credit.** The values a(1)..a(10) = 0, 1, 3, 6, 9, 12, 16, 19, 23, 27 were already published in
the working report "Erdős Problem #585: Same-vertex-set cycles — working report"
(https://erdosproblemaday.com/report/585, 2026-07-28; built by Patrick White with Claude). That
report also gives the lower bound a(11) >= 30. Here those ten values were recomputed with
independent code. **New in this work:** a(11) = 31, computed by two methods; a(12) = 36 and 39 <= a(13) <= 40, both
from the certified ladder (method (c)); and the number of extremal graphs (isomorphism classes) for
n <= 12.

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
| 13 | **39 or 40** | – | – | 40 is an upper bound only; 39 is reached | ? |

The n = 12 and n = 13 rows come only from method (c).

- Method (a) scans every graph with the given number of edges.
- Method (b) builds every good graph above a threshold, so it gives the maximum edge count directly.
- For every n, the two methods give the same graph6 list of extremal graphs after canonical
  labelling with `nauty-labelg`. The lists are in `tanik/uc_n<n>_m<a(n)>.g6`.
- For n <= 10, a(n) - a(n-1) is 3 or 4.
- a(11) = 31 is one more than the bound a(11) >= 30 in the report.
- Good 11-vertex graphs with exactly 30 edges: 1780 classes, by both methods. Method (a) uses
  `geng -d3 11 30:30`, 68718688 graphs; minimum degree >= 30 - 27 = 3 by the argument below. The
  two lists are identical (`tanik/n11_m30_iyi.g6`).
- Running times on this machine (8 cores, shared, 3 parallel parts): n <= 10 takes seconds. At
  n = 11 the 32-edge scan takes 25 s, the 31-edge scan 4 min and the 30-edge scan 7 min. The
  ladder takes about 70 s.

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
  - Deciding 40 needs the full L_12(34) and so the chain t_13 = 39 (or 40). That chain needs
    L_10(23) (1083603 classes) and L_11(28) (22009718 candidates). It was stopped to stay within
    the time budget. a(13) is open between 39 and 40.
- **Independent check of the lower bounds.** `e585_ref2.py` is pure Python: it does a DFS
  enumeration of all Hamiltonian cycles per vertex set and tests every pair.
  - It agrees with `e585.c` on all graphs with n <= 8.
  - It confirms the 8 extremal graphs at n = 11, the extremal graph at n = 12 and all 126 39-edge
    witnesses at n = 13 (`out/ref2.txt`).

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
```

## Files

- `e585.c`: checker and extension (`check`, `extend`).
- `e585_ref.py`: independent reference checker.
- `sertifika_dogrula.py`: independent certificate verifier.
- `e585_ref2.py`: second independent checker (DFS enumeration of Hamiltonian cycles).
- `yontem_c.sh`: method (c), the certified ladder.
- `yontem_a.sh`: method (a) for n <= 10.
- `f11_tarama.sh`: method (a) for n = 11.
- `yontem_b.sh`: method (b).
- `run.sh`: runs everything.
- `tanik/uc_n<n>_m<a(n)>.g6`: all extremal graphs (canonical graph6).
- `out/`: logs.
- `oeis_draft.txt`: OEIS draft.
