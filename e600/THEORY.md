# Erdős #600, r = 2: what is proved

Notation: G locally linear (every edge in exactly one triangle) on n vertices; its triangles form a linear, triangle-free triple system H with T triples. d_v = number of triples at v, so deg_G(v) = 2 d_v.

## Proposition 1 (upper bound, elementary; proved)
T(n) ≤ ⌊ n·⌊(n+3)/2⌋ / 9 ⌋.

Proof. Let xyz be a triangle. The sets N(x)\{y,z}, N(y)\{x,z}, N(z)\{x,y} avoid x,y,z and are pairwise disjoint: a common neighbour w of x and y (w ≠ z) would put edge xy in two triangles. Hence (2d_x−2)+(2d_y−2)+(2d_z−2) ≤ n−3, i.e. d_x+d_y+d_z ≤ ⌊(n+3)/2⌋. Summing over the T triples, Σ_v d_v² ≤ T·⌊(n+3)/2⌋. By Cauchy–Schwarz, Σ_v d_v² ≥ (Σ d_v)²/n = 9T²/n. So T ≤ n⌊(n+3)/2⌋/9. ∎
(Without the integer rounding this is the classical m ≤ n(n+3)/6 edge bound for locally linear graphs, Math. Slovaca 39 (1989); the rounding step is what gives T(14) ≤ 12.)

Data: the bound is attained for every n ≤ 14 except n = 11 (bound 8, true 7) and n = 13 (bound 11, true 10). It explains the plateaus T(3)=T(4), T(5)=T(6), T(9)=T(10): there the bound itself does not increase. It cannot stay tight: it is ~n²/18, while T(n) = o(n²) (Ruzsa–Szemerédi).

## Proposition 2 (constructions; proved)
(a) T is nondecreasing (add an isolated vertex).
(b) T(a+b) ≥ T(a)+T(b) (disjoint union) and T(a+b−1) ≥ T(a)+T(b) (identify one vertex: no new triangle, since a triangle through the glued vertex would need an edge between the two parts).
(c) Windmill: T(n) ≥ ⌊(n−1)/2⌋. Loose cycle of k ≥ 4 triangles: T(2k) ≥ k.
(d) K3×K3 (rook graph, 9 vertices, 6 triangles, extremal at n = 9); gluing k copies in a chain gives T(8k+1) ≥ 6k.
(e) Ruzsa–Szemerédi/Behrend: for odd m and A ⊆ Z_m with no non-trivial solution of a+b = 2c, triples {(x,0),(x+a,1),(x+2a,2)} give T(3m) ≥ m|A| (A = {0,1}, m = 3 gives the 9-vertex extremal example). With Behrend sets this yields T(n) ≥ n²/exp(O(√log n)).

Combining (a),(b),(d) gives only 8 at n = 13, 14, while the truth is 10, 12, so the optimal graphs for n ≥ 11 are NOT these simple gluings (witness degree sequences have several degree-3 vertices).

## Observations (conjectural)
- C1 (confidence high for small n, false for large n): T(n) = U(n) holds "most of the time" for small n. It must fail infinitely often because U(n) ≍ n² and T(n) = o(n²).
- C2 (moderate): T(15) = 15 = U(15)? Untested; CP-SAT for n = 15 was still running at the time of writing.
- e(n,2) = n + T(n) is FALSE (n = 9: 19 vs 15).

## Known asymptotics (references)
- Ruzsa & Szemerédi (1978): e(n,r) = o(n²) for fixed r; Behrend-type lower bound n^{2−o(1)}.
- Fox (removal lemma): ≤ n²/exp(Ω(log* n)) (see Wikipedia "Ruzsa–Szemerédi problem").
- Mathlib: `ruzsaSzemerediNumberNat` (formal definition and the Behrend lower bound).
