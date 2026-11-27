# S2. 2-colourings of triples with no monochromatic 4-set

**Status: candidate; novelty not claimed; not yet submitted.** Computed 2026-11-27.

## Definition

a(m) = number of colourings of all 3-subsets of {1..m} with two colours such that no 4-subset
has all four of its 3-subsets in the same colour (labeled R(4,4;3)-good colourings; colours
are distinguished). a(m) = 0 for m >= 13 because R(4,4;3) = 13 (McKay and Radziszowski 1991),
so the sequence is finite; a(9)..a(12) are positive and not computed here.

## Terms

| m | a(m) | A: direct backtracking | B: one-point extension (all colourings) | C: SDD model count | B1: S7-classes + 1 point | B2: S6-classes + 2 points |
|---|---|---|---|---|---|---|
| 1 | 1 | 1 | 1 | 1 | – | – |
| 2 | 1 | 1 | 1 | 1 | – | – |
| 3 | 2 | 2 | 2 | 2 | – | – |
| 4 | 14 | 14 | 14 | 14 | – | – |
| 5 | 512 | 512 | 512 | 512 | – | – |
| 6 | 118784 | 118784 | 118784 | 118784 | – | – |
| 7 | 153010788 | 153010788 | 153010788 | 153010788 | 153010788 | 153010788 |
| 8 | 638804584320 | – | – | – | 638804584320 | 638804584320 |

Isomorphism-class counts found along the way: 226 classes for m = 6 and 31060 for m = 7
(relabelling only, complements counted separately). These agree with Table 1 of
B. D. McKay, "A class of Ramsey-extremal hypergraphs", arXiv:1608.07762 (2016), which lists
unlabeled counts (226, 31060, 15854385 for 6, 7, 8 points) but not labeled ones.

## Methods

- **A** `s2_direct.c`: triples coloured in colex order; every 4-set is tested when its last
  triple is coloured; first triple fixed red and the count doubled.
- **B** `s2_extend.c`: builds all valid colourings point by point; adding point p colours the
  edges of K_p; a 4-set {a,b,c,p} is monochromatic iff triangle abc is monochromatic in the edge
  colouring in the colour of triple abc (precomputed triangle masks).
- **C** `s2_sdd.py`: CNF with one variable per triple and two clauses per 4-set, compiled to a
  sentential decision diagram (PySDD) and model-counted.
- **B1** `s2_onepoint.c`: representatives of the S6-classes at m = 6 (all 2^20 masks, minimum
  image), extended by point 7 and canonicalised under S7 with stabiliser sizes; the class sizes
  5040/|Stab| sum to a(7); a(8) = sum over classes of 5040/|Stab| * f(T), f(T) = admissible
  colourings of the 21 edges of K7.
- **B2** `s2_twopoint.c`: S6-classes at m = 6 (sorting canonical forms); two new points 7 and 8
  colour K6 independently (e7, e8), and the six triples {i,7,8} must avoid a monochromatic
  {i,j,7,8}; this is counted with independent-set bitmasks.

Reproduce: `./run.sh` (A, B, B1, B2 about 2 CPU minutes; C about 5 CPU minutes, skip with `NO_SDD=1`).

## Novelty check (K1), 2026-11-27

| source | query | result |
|---|---|---|
| oeis.org | `1,1,2,14,512,118784` | no match |
| oeis.org | `118784,153010788`; `153010788`; `638804584320` | no match |
| oeis.org | `3,12,226,31060`; `226,31060,15854385` (unlabeled, McKay 2016) | no match |
| oeis.org | words: `monochromatic K_4^(3)`; `2-colorings triples monochromatic hypergraph` | no match |
| literature | McKay–Radziszowski 1991 (R(4,4;3) = 13); McKay 2016 arXiv:1608.07762 | unlabeled class counts only (see above); no labeled counts |
| web / arXiv search | labeled counts of R(4,4;3)-good colourings | not found |
| erdosproblems.com | problems 562, 564 | no OEIS link, no such sequence |

## Note

The sequence came from submissions attached to Erdős problems 562 and 564 (hypergraph Ramsey
numbers); it is the labeled counting version of the R(4,4;3) problem.
