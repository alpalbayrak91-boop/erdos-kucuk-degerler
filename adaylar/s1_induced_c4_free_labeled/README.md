# S1. Labeled graphs with no induced 4-cycle

**Status: candidate; novelty not claimed; not yet submitted.** Computed 2026-11-27.

## Definition

a(n) = number of simple graphs on the labeled vertex set {1..n} that contain no induced
subgraph isomorphic to C4. Taking complements, a(n) is also the number of labeled
2K2-free graphs on n vertices. The unlabeled version is OEIS A352068.

## Terms

| n | a(n) | A: direct (no nauty) | B: classes, n!/\|Aut\| via countg | C: +1 vertex on classes of n-1 | D: +2 vertices on classes of n-2 | classes (A352068) |
|---|---|---|---|---|---|---|
| 1 | 1 | 1 | 1 | – | – | 1 |
| 2 | 2 | 2 | 2 | 2 | – | 2 |
| 3 | 8 | 8 | 8 | 8 | 8 | 4 |
| 4 | 61 | 61 | 61 | 61 | 61 | 10 |
| 5 | 834 | 834 | 834 | 834 | 834 | 28 |
| 6 | 19258 | 19258 | 19258 | 19258 | 19258 | 100 |
| 7 | 711359 | 711359 | 711359 | 711359 | 711359 | 441 |
| 8 | 40091516 | 40091516 | 40091516 | 40091516 | 40091516 | 2574 |
| 9 | 3310769148 | – | 3310769148 | 3310769148 | 3310769148 | 19849 |
| 10 | 387102675123 | – | 387102675123 | 387102675123 | 387102675123 | 201682 |
| 11 | 62257972139056 | – | – | 62257972139056 | 62257972139056 | 2647682 (not recomputed) |

Every term for n <= 10 is produced by at least three of the four methods; n = 11 by C and D.
The plain bitmask enumeration `s1_bruteforce_small.c` (all 2^C(n,2) edge sets, all 4-subsets)
gives the same values for n <= 7.

## Methods

- **A** `s1_direct.c`: depth-first enumeration of labeled graphs; vertex k picks its
  neighbourhood in {0..k-1}; all 4-subsets through k are tested (a 4-vertex induced subgraph
  is C4 iff every vertex has degree 2 inside it). Independent of nauty.
- **B** `nauty-geng n | s1_filter | nauty-countg --a`: one graph per isomorphism class, filtered
  by an all-4-subsets test; `countg --a` gives the histogram of automorphism group orders;
  a(n) = sum n!/|Aut G| (`s1_sum.py B`). The class counts equal A352068 for n = 1..10,
  which checks the filter.
- **C** `s1_extend.c`: a(n) = sum over classes H on n-1 vertices of (n-1)!/|Aut H| * v(H),
  where v(H) counts neighbourhoods N of a new vertex z creating no induced C4
  (z-a-x-b with a,b in N non-adjacent, x outside N adjacent to both). |Aut H| by an own
  backtracking search (no nauty).
- **D** `s1_extend2.c`: two new labeled vertices z1, z2 on classes H with n-2 vertices; single
  neighbourhoods tested by brute force; pairs rejected if z1~z2 and some a in N1\N2 is adjacent
  to some b in N2\N1, or z1 !~ z2 and N1 ∩ N2 is not a clique.

Reproduce: `./run.sh` (about 1 CPU minute; raw outputs in `out/`).

## Novelty check (K1), 2026-11-27

| source | query | result |
|---|---|---|
| oeis.org | `1,2,8,61,834,19258,711359` | no match |
| oeis.org | `19258,711359,40091516` | no match |
| oeis.org | `40091516` | no match |
| oeis.org | `3310769148` | no match |
| oeis.org | words: `labeled "induced cycle of length four"`; `labeled 2K2-free` | no match |
| oeis.org | A352068, A079566 (unlabeled, unlabeled connected) | no labeled version cross-referenced |
| web search | "enumeration of labeled 2K2-free graphs / no induced C4" | structural papers (Blázsik–Hujter–Pluhár–Tuza 1993; Prömel–Steger 1991, asymptotic); graphclasses.org "speed" only; no exact values |
| erdosproblems.com | problems 558, 1111 | no OEIS link, no such sequence |

Related but different: A345249 (labeled graphs with no 4-cycle as a subgraph:
1, 2, 8, 54, 548, ...), A006125 (all labeled graphs).

## Note

The sequence came from submissions attached to Erdős problems 558 and 1111; it is not implied
by either problem statement.
