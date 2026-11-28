# Proof of the Theorem (cycle family)

This file gives the full proof of the Theorem stated in `README.md`, section "Theorem (cycle
family)". The family and a proof sketch were found by an automated LLM agent search (Gemini). The
proof below follows that sketch; it was checked line by line by Claude, and the statement was
confirmed for b = 7..20 by integer programming (`aile.py`, `out/aile.log`).

## The graphs

Let b >= 3 and let B = {b_0, ..., b_{b-1}}, indices mod b. Write C_b for the cycle
b_0 b_1 ... b_{b-1} b_0 and C_b(3) for the graph on B with edges {b_i, b_{i+3}}, 0 <= i < b
("3-step chords"). Let F be a subgraph of C_b(3).

G = G(C_b, F) has vertex set {u1, u2, w} ∪ A ∪ B, where A = {a_e : e ∈ E(F)}, and edges

- u1 is adjacent to every other vertex;
- u2 is adjacent to every other vertex except w;
- w is adjacent to every vertex of A (and to u1), to nothing else;
- B carries the cycle C_b;
- A is independent, and a_e is adjacent to the two ends of e (and to u1, u2, w).

So n = |E(F)| + b + 3, and the number of edges is

    (n - 1) + (n - 3) + |E(F)| + b + 2|E(F)| = 5|E(F)| + 3b + 2.

Degrees used below: in R = G - {u1, u2}, every a ∈ A has degree 3 (w and two vertices of B), w has
degree |A| and N_R(w) = A, and a vertex x ∈ B has 2 neighbours in B and deg_F(x) neighbours in A.

For b >= 7 the steps 3 and b - 3 are different and both differ from 1, so C_b(3) is 2-regular, has
b edges, and shares no edge with C_b. Its components are cycles of length L = b / gcd(b, 3).

## Theorem

**Theorem.** If b >= 7 and F ⊆ C_b(3), then G(C_b, F) has no nonempty 4-regular subgraph.

With F = C_b(3) (b edges) this gives n = 2b + 3 and 8b + 2 edges; with F = C_b(3) minus one edge,
n = 2b + 2 and 8b - 3 edges. Since the union of two edge-disjoint cycles on the same vertex set is
4-regular,

    a(2b + 3) >= r(2b + 3) >= 8b + 2   (4n - 10 for odd n >= 17),
    a(2b + 2) >= r(2b + 2) >= 8b - 3   (4n - 11 for even n >= 16).

## Proof

Suppose H ⊆ G is 4-regular on a nonempty vertex set S. Write

- S_R = S \ {u1, u2}, S_A = S ∩ A, S_B = S ∩ B, H_R = H[S_R];
- e(X) for the number of edges of H with both ends in X, and e_H(X, Y) for the number of edges of
  H between X and Y;
- e_F(X) for the number of edges of F with both ends in X.

Every vertex of S has degree exactly 4 in H.

Two facts are used repeatedly.

- (P) If ∅ ≠ X ⊊ B, the edges of H inside X are edges of C_b[X], which is a disjoint union of paths.
  So H[X] is a forest; if it has c components (isolated vertices count), then e(X) = |X| - c. If
  c = 1, X is a set of consecutive vertices of C_b.
- (Q) Distinct vertices of A correspond to distinct edges of F. So the number of a ∈ S_A whose two
  B-neighbours both lie in X (and are joined to a in H) is at most e_F(X).

### Case 1: S ∩ {u1, u2} = ∅

Then H ⊆ R. Every a ∈ A has degree 3 < 4 in R, so S_A = ∅. Then w has no neighbour in S (its
neighbours in R are in A), so w ∉ S. What is left is S ⊆ B, where every vertex has degree 2 < 4 in
C_b. So S = ∅, a contradiction.

### Case 2: S ∩ {u1, u2} = {u}

Let e_uw ∈ {0, 1} indicate whether the edge u w is in H (if u = u2 then e_uw = 0, since u2 w is not
an edge of G).

*S_A is not empty.* Suppose S_A = ∅. The only possible neighbour of w in S is u, so w has degree
at most 1 in H and w ∉ S. A vertex of B has at most 2 + 1 = 3 neighbours in B ∪ {u}, so S_B = ∅.
Then S = {u}, and u has degree 0 in H, a contradiction.

*Every a ∈ S_A uses all its edges.* In G - (the other vertex of {u1, u2}), a has exactly 4
neighbours: u, w and its two neighbours in B. So all four edges are in H. In particular w ∈ S,
every a ∈ S_A is joined to u and to w in H, and N_B(a) ⊆ S_B; so S_B ≠ ∅.

*Counting at w.* The neighbours of w in S are S_A and possibly u. So deg_H(w) = |S_A| + e_uw = 4,
that is |S_A| = 4 - e_uw <= 4.

*Counting at u.* u is joined in H to all of S_A and, if e_uw = 1, to w: that is |S_A| + e_uw = 4
edges, all of deg_H(u). So u has no H-neighbour in S_B (for u = u1 and for u = u2).

*Counting at S_B.* A vertex of S_B has H-neighbours only in S_B and S_A, and e_H(S_A, S_B) = 2|S_A|.
Summing degrees over S_B,

    4|S_B| = 2 e(S_B) + 2|S_A|,   so   2|S_B| - e(S_B) = |S_A| <= 4.

- If S_B = B, then e(S_B) <= b, so b <= 2b - e(S_B) = |S_A| <= 4. This contradicts b >= 5.
- If ∅ ≠ S_B ⊊ B, then by (P) e(S_B) <= |S_B| - 1, so |S_B| + 1 <= |S_A| <= 4 and |S_B| ∈ {1, 2, 3}.
  By (Q), |S_A| <= e_F(S_B) <= C(|S_B|, 2). For |S_B| = 1, 2, 3 this is 0, 1, 3, smaller than
  |S_B| + 1 = 2, 3, 4. A contradiction.

Cases 1 and 2 use neither F ⊆ C_b(3) nor max degree 2: they hold for every simple graph F on B
and every b >= 5.

### Case 3: u1, u2 ∈ S

Let e12 ∈ {0, 1} indicate whether u1 u2 is in H. The number of H-edges between {u1, u2} and S_R is

    E_top = 4 + 4 - 2 e12 = 8 - 2 e12 ∈ {6, 8}.

For v ∈ S_R let d_top(v) = |N_H(v) ∩ {u1, u2}| ∈ {0, 1, 2}, and D_B = Σ_{x ∈ S_B} d_top(x), so
that E_top = Σ_{v ∈ S_R} d_top(v).

Each a ∈ S_A has degree 3 in R, so d_top(a) >= 1; hence d_top(a) ∈ {1, 2}. Let A_1 and A_2 be the
sets of a ∈ S_A with d_top(a) = 1 and 2, and t_1 = |A_1|, t_2 = |A_2|. For a ∈ A_1, a has degree
3 in H_R, so all three of its R-edges (to w and to its two B-neighbours) are in H.

*Identity (E0).* Summing H-degrees over S_R gives 2 e(S_R) + E_top = 4|S_R|, so

    e(S_R) = 2|S_R| - 4 + e12.

The edges of H_R either meet S_A or lie inside S_B (A is independent and w has no neighbour in B).
An a ∈ A_1 meets 3 of them and an a ∈ A_2 meets 2 (no edge joins two vertices of A). So

    3 t_1 + 2 t_2 + e(S_B) = 2|S_R| - 4 + e12.     (E0)

#### Case 3a: w ∉ S

No a ∈ S_A can use its edge to w, so t_1 = 0, and every a ∈ S_A = A_2 is joined in H to both of its
B-neighbours, which lie in S_B. By (Q), t_2 <= e_F(S_B). Now |S_R| = t_2 + |S_B|, and (E0) becomes

    2|S_B| - e(S_B) = 4 - e12 ∈ {3, 4}.

Counting E_top: 2 t_2 + D_B = 8 - 2 e12.

- S_B = ∅ is impossible (0 ≠ 4 - e12).
- S_B = B is impossible: 2b - e(B) >= b >= 5 > 4.
- So ∅ ≠ S_B ⊊ B, and by (P) e(S_B) = |S_B| - c with c >= 1 components. Then
  |S_B| + c = 4 - e12, with 1 <= c <= |S_B|. The only triples (|S_B|, c, e12) are:
  - (2, 1, 1): S_B = {b_i, b_{i+1}}. This pair is not a 3-step chord (1 ≢ ±3 mod b, as b >= 7), so
    e_F(S_B) = 0 and t_2 = 0. But then D_B = 8 - 2 = 6 > 2|S_B| = 4, impossible since d_top <= 2.
  - (2, 2, 0): t_2 <= e_F(S_B) <= 1 and D_B <= 2|S_B| = 4, so 2 t_2 + D_B <= 6 < 8. Impossible.
  - (3, 1, 0): S_B = {b_i, b_{i+1}, b_{i+2}}. The pairwise distances on C_b are 1, 1, 2, and neither
    1 nor 2 is ≡ ±3 mod b; this needs b ≠ 4 and b ≠ 5, and holds as b >= 7. So e_F(S_B) = 0,
    t_2 = 0 and D_B = 8 > 2|S_B| = 6. Impossible.

#### Case 3b: w ∈ S

Now |S_R| = t_1 + t_2 + |S_B| + 1, and d_top(w) ∈ {0, 1} because u2 w is not an edge. Substituting in
(E0), the terms 2 t_2 cancel and

    2|S_B| - e(S_B) = t_1 + 2 - e12.     (E1)

Split A_2 into A_2w (those joined to w in H; each then has exactly one H-neighbour in S_B) and A_2b
(those not joined to w; each is joined in H to both B-neighbours), t_2 = t_2w + t_2b.

- Every a ∈ A_1 ∪ A_2b is joined in H to both of its B-neighbours, so by (Q)

      t_1 + t_2b <= e_F(S_B).     (E2)

- The H-neighbours of w are A_1, A_2w and possibly u1, so deg_H(w) = 4 gives

      t_1 + t_2w + d_top(w) = 4,   in particular t_1 <= 4.     (E3)

- Counting E_top: 8 - 2 e12 = t_1 + 2 t_2w + 2 t_2b + d_top(w) + D_B. Substituting
  t_2w = 4 - t_1 - d_top(w) from (E3),

      2 t_2b + D_B = t_1 + d_top(w) - 2 e12 = 4 - t_2w - 2 e12.     (E4)

*S_B is a proper nonempty subset of B.* S_B = ∅ is impossible, because the right side of (E1) is
t_1 + 2 - e12 >= 1. If S_B = B, then e(B) <= b, and (E1), (E3) give
b <= 2b - e(B) = t_1 + 2 - e12 <= 6. This contradicts b >= 7. **This is the step where b >= 7 is
used.**

So ∅ ≠ S_B ⊊ B, and by (P) e(S_B) = |S_B| - c with c >= 1. (E1) becomes

    |S_B| + c = t_1 + 2 - e12.     (E5)

*The inequality (E6).* Here F ⊆ C_b(3) is used through deg_F(x) <= 2. For x ∈ S_B, the H-neighbours
of x are in S_B, in S_A and in {u1, u2}, and x has deg_F(x) <= 2 neighbours in A. So
d_top(x) = 4 - deg_{H[S_B]}(x) - e_H(x, S_A) >= 2 - deg_{H[S_B]}(x). Summing over S_B,

    D_B >= 2|S_B| - 2 e(S_B) = 2c.     (E6)

This is the only place where the maximum degree of F is used.

*The bound (E7).* From (E4) and (E6),

    2c <= D_B = 4 - t_2w - 2 e12 - 2 t_2b <= 4 - 2 e12 - 2 t_2b.     (E7)

So c = 1 or c = 2.

**c = 1.** Write s = |S_B|. By (P), S_B = {b_0, ..., b_{s-1}} after a rotation. (E5) gives
t_1 = s + e12 - 1, and (E3) gives s = t_1 + 1 - e12 <= 5. An edge of F inside S_B joins b_i, b_j
with 0 <= i < j <= s - 1 and j - i ≡ ±3 (mod b).

- s = 1: e_F(S_B) = 0, so by (E2) t_1 = 0, and then t_1 = s + e12 - 1 gives e12 = 0. By (E4) and
  (E6), 2 = 2c <= D_B <= t_1 + d_top(w) = d_top(w) <= 1. A contradiction.
- s = 2: the distance is 1, so e_F(S_B) = 0; but t_1 = 1 + e12 >= 1, against (E2).
- s = 3: the distances are 1, 1, 2, none ≡ ±3 (mod b) for b >= 7, so e_F(S_B) = 0; but
  t_1 = 2 + e12 >= 2, against (E2).
- s = 4: the distances are at most 3, and b - 3 >= 4, so the only possible chord is {b_0, b_3} and
  e_F(S_B) <= 1; but t_1 = 3 + e12 >= 3, against (E2).
- s = 5: the distances are at most 4. Distance 3 gives {b_0, b_3} and {b_1, b_4}; distance
  b - 3 <= 4 happens only for b = 7 and gives {b_0, b_4}. So e_F(S_B) <= 3; but t_1 = 4 + e12 >= 4,
  against (E2).

**c = 2.** In (E7), 4 = 2c <= D_B = 4 - t_2w - 2 e12 - 2 t_2b <= 4, so every inequality is an
equality: t_2w = 0, t_2b = 0, e12 = 0 and D_B = 4. Then (E3) gives t_1 = 4 - d_top(w) ∈ {3, 4}, and
(E5) gives |S_B| = t_1 ∈ {3, 4}.

(E6) was obtained by summing, over x ∈ S_B, the inequalities
d_top(x) >= 2 - deg_{H[S_B]}(x), each of which comes from e_H(x, S_A) <= 2. The differences
2 - e_H(x, S_A) are nonnegative and now add up to 0, so each of them is 0: e_H(x, S_A) = 2 for
every x ∈ S_B. Since t_2 = 0, S_A = A_1, and every edge of H between S_A and
S_B comes from some a ∈ A_1, which is joined to both ends of its edge of F. So the edges
F_1 = {N_B(a) : a ∈ A_1} form a subgraph of F[S_B] ⊆ C_b(3) in which every vertex of S_B has
degree 2: a 2-regular simple graph on 3 or 4 vertices, that is a 3-cycle or a 4-cycle.

C_b(3) is 2-regular. In F_1 every vertex of S_B has degree 2, so F_1 contains both edges of
C_b(3) at each of its vertices; hence F_1 is a union of whole components of C_b(3), which are
cycles of length L = b / gcd(b, 3). A union of such cycles on 3 or 4 vertices is a single 3-cycle (L = 3) or a
single 4-cycle (L = 4).

- If 3 ∤ b, then L = b >= 7 > 4: no such cycle.
- If b = 9, the 3-cycles of C_9(3) are {b_0, b_3, b_6}, {b_1, b_4, b_7}, {b_2, b_5, b_8}. Each of them
  is an independent set of C_9, so e(S_B) = 0 and c = |S_B| = 3 ≠ 2. A contradiction.
- If b = 12, the 4-cycles of C_12(3) are {b_i, b_{i+3}, b_{i+6}, b_{i+9}}. Each is an independent set
  of C_12, so e(S_B) = 0 and c = 4 ≠ 2. A contradiction.
- If 3 | b and b >= 15, then L = b / 3 >= 5 > 4: no such cycle.

All cases lead to a contradiction, so H does not exist. ∎

## Remarks

- Cases 1 and 2 hold for every simple graph F on B and every b >= 5. Case 3a uses only that F
  shares no edge with C_b and has no edge between vertices at distance 2 on C_b; for the triple
  (3, 1, 0) this is the condition 2 ≢ ±3 (mod b), i.e. b ≠ 5. The hypothesis b >= 7 is used where
  S_B = B in Case 3b. The maximum degree 2 of F is used only in (E6). In the subcase c = 2 the values
  b = 9 and b = 12 need a separate argument, because then C_b(3) has components that are 3-cycles
  and 4-cycles; these are independent sets in C_b.
- Computation (`out/aile.log`): for b = 7..20 both graphs (F = C_b(3), and F = C_b(3) minus the
  edge {b_0, b_3}) have no 4-regular subgraph. For b = 5 both graphs have one (n = 13 with 42 edges
  and n = 12 with 37 edges), so the theorem fails at b = 5. For b = 6, C_6(3) is a perfect matching
  with 3 edges and the two graphs (n = 12 with 35 edges, n = 11 with 30 edges) have no 4-regular
  subgraph; they are not in the 4n - 10 / 4n - 11 pattern.
