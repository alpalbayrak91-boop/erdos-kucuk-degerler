# The cubic family: proof for all m >= 9 (computer-assisted)

This file proves the statement of `README.md`, section "Cubic family", for every m >= 9. The proof
has two hand-checked lemmas and one finite computation (`out/kubik_tam.log`). It was written by
Claude; an independent review is recorded at the end.

## The graphs

Let m >= 7. B = GP(m, 2) has outer vertices x_i and inner vertices y_i (i in Z_m), with the edges
x_i x_{i+1} (outer cycle), x_i y_i (spokes) and y_i y_{i+2} (inner edges). The *index* of x_i and of
y_i is i. F is the graph on V(B) with the 2m edges x_i y_{i+3}, x_i y_{i-3}.

G_m has the vertices u1, u2, w, one vertex a_e for each edge e of F, and V(B). Its edges: u1 is
adjacent to every other vertex; u2 to every other vertex except w; w to u1 and to every a_e; a_e to
the two ends of e (and to w, u1, u2); B keeps its edges. Write A for the set of the a_e and
R = G_m - {u1, u2}.

Facts used below (all immediate from the definition, for m >= 7):

- (F1) every a in A has exactly three neighbours in R: w and the two ends of its edge of F;
- (F2) the neighbours of w in R are exactly the vertices of A;
- (F3) every b in V(B) has exactly three neighbours in B and exactly two in A, and no others in R
  (F is 2-regular and shares no edge with B, because 3, -3, 0 are distinct mod m);
- (F4) B is connected;
- (F5) the two ends of an edge of B or of F have indices that differ by 0, 1, 2 or 3 (mod m, up
  to sign), and whether two vertices are joined in B or in F depends only on their types (outer or
  inner) and on the difference of their indices.

**Theorem.** For m = 7 and for every m >= 9, G_m has no nonempty 4-regular subgraph.

## Lemma 1 (a 4-regular subgraph is small)

Let H be a nonempty 4-regular subgraph of G_m, S = V(H), S_A = S ∩ A, S_B = S ∩ V(B). Let Q be the
set of indices of the vertices of S_B, together with the indices of both ends of e for every
a_e in S_A. Then |Q| <= 12.

*Proof.* Every vertex of S has degree 4 in H. Write e(X) for the number of edges of H inside X.

**Case 1: u1, u2 not in S.** Then H is a subgraph of R. By (F1) no vertex of A is in S; then by
(F2) w has no neighbour in S, so w is not in S; then S is a subset of V(B), where degrees are at
most 3 by (F3). So S is empty, a contradiction. This case does not occur.

**Case 2: exactly one of u1, u2 is in S;** call it u.

*If S_A is empty:* w has at most one neighbour in S (namely u), so w is not in S. A vertex b of
S_B has at most 3 + 1 neighbours in S (three in B, and u), so all three B-neighbours of b are in S
and b is joined to u in H. Hence S_B is closed under taking neighbours in B, so S_B = V(B) by
(F4), and u has 2m > 4 neighbours in H. A contradiction.

*If S_A is not empty:* by (F1) a vertex a of S_A has exactly four neighbours in G_m minus the
other vertex of {u1, u2}, so H uses all four: a is joined to u, to w and to both ends of its edge,
which are therefore in S_B. So the indices coming from S_A are already indices of S_B, and
|Q| <= |S_B|. Also w is in S. Let e_uw in {0, 1} say whether u w is an edge of H. By (F2) the
neighbours of w in H are all of S_A and, if e_uw = 1, the vertex u; so

    |S_A| + e_uw = deg_H(w) = 4,   in particular |S_A| <= 4.

The vertex u is joined in H to every vertex of S_A and, if e_uw = 1, to w. These are
|S_A| + e_uw = 4 edges of H at u, and deg_H(u) = 4, so u has no H-neighbour in S_B. A vertex of
S_B therefore has all its H-neighbours in S_B and S_A (w has no neighbour in B, and the other
vertex of {u1, u2} is not in S). Summing the degrees over S_B and using (F3):

    4 |S_B| = 2 e(S_B) + 2 |S_A| <= 3 |S_B| + 8,

because H[S_B] is a subgraph of the cubic graph B. So |S_B| <= 8.

**Case 3: u1, u2 in S.** Let e12 in {0, 1} say whether u1 u2 is an edge of H. For a vertex v of
S other than u1, u2 let d(v) in {0, 1, 2} be the number of its H-neighbours in {u1, u2}. Counting
the edges of H at u1 and u2:

    sum of d(v) over v in S \ {u1, u2}  =  8 - 2 e12.        (1)

Let D_B be the sum of d(b) over b in S_B. For a in S_A, (F1) gives d(a) >= 1.

*Case 3a: w not in S.* A vertex a of S_A has at most two neighbours in S inside R (the ends of its
edge), so d(a) = 2 and both ends are in S_B. So |Q| <= |S_B|. With t = |S_A|, (1) reads
2t + D_B = 8 - 2 e12, and summing degrees over S_B gives

    4 |S_B| = 2 e(S_B) + 2t + D_B = 2 e(S_B) + 8 - 2 e12 <= 3 |S_B| + 8.

So |S_B| <= 8.

*Case 3b: w in S.* Since u2 w is not an edge, d(w) <= 1. Split S_A into three sets:
- A1: d(a) = 1. Then a has three H-neighbours in R, so it is joined to w and to both ends of its
  edge.
- A2w: d(a) = 2 and a is joined to w in H. Then a is joined in H to exactly one end of its edge.
- A2b: d(a) = 2 and a is not joined to w in H. Then a is joined in H to both ends of its edge.

Let t1, t2w, t2b be their sizes. By (F2) the H-neighbours of w are A1, A2w and possibly u1:

    t1 + t2w + d(w) = 4.        (2)

Equation (1) reads d(w) + t1 + 2 t2w + 2 t2b + D_B = 8 - 2 e12. Subtracting (2):

    D_B + 2 t2b = 4 - 2 e12 - t2w.        (3)

For b in S_B let alpha(b) be the number of H-neighbours of b in S_A. By (F3),
4 = deg_{H[S_B]}(b) + alpha(b) + d(b) with deg_{H[S_B]}(b) <= 3, so alpha(b) + d(b) >= 1. The sum
of alpha(b) over S_B is the number of H-edges between S_A and S_B, which is 2 t1 + t2w + 2 t2b.
Summing alpha(b) + d(b) >= 1 over S_B and using (3):

    |S_B| <= 2 t1 + t2w + 2 t2b + D_B = 2 t1 + 4 - 2 e12.

The indices in Q that are not indices of S_B come from vertices of A2w (the end of the edge that
is not used), at most one index each. So, using (2),

    |Q| <= |S_B| + t2w <= 2 t1 + 4 + (4 - t1) = t1 + 8 <= 12.

This finishes the proof of Lemma 1. ∎

## Lemma 2 (moving a 4-regular subgraph to another member of the family)

Let m >= 37 and M >= 34. If G_m has a nonempty 4-regular subgraph, then so does G_M.

*Proof.* Let H and Q be as in Lemma 1, and r = |Q| <= 12. The r cyclic gaps between consecutive
elements of Q add up to m >= 37 > 3r, so one gap is at least 4. Rotate the indices of G_m (a
rotation is an automorphism of G_m) so that Q = {q_1 < q_2 < ... < q_r} inside {0, ..., m - 1},
with q_1 = 0 and the gap from q_r back to q_1 around the cycle at least 4; that is, q_r <= m - 4.
Put p_1 = 0 and, for 1 <= j < r,

    p_{j+1} = p_j + (q_{j+1} - q_j)   if q_{j+1} - q_j <= 3,
    p_{j+1} = p_j + 1                 if q_{j+1} - q_j >= 4.

So 0 = p_1 < p_2 < ... < p_r <= 3 (r - 1) <= 33: gaps of size at most 3 are kept, larger gaps are
shrunk to 1. Let phi(q_j) = p_j, read as an element of Z_M. Since M >= 34, the p_j are distinct
mod M.

*Claim.* If q, q' in Q satisfy q' = q + c (mod m) with -3 <= c <= 3, then
phi(q') = phi(q) + c (mod M). Indeed, consider the arc of the cycle Z_m from q to q' of length
|c| <= 3. It cannot contain the gap from q_r back to q_1, which has length at least 4. So the arc
does not pass through the point where the indices wrap around, and q' = q + c holds as an equation
between integers in {0, ..., m - 1}. The elements of Q on the arc cut it into gaps whose sizes add
up to |c| <= 3, so each of these gaps has size at most 3 and is kept by the construction. Hence
p' - p = q' - q = c.

Define a map on S: u1, u2, w are fixed; x_q goes to x_{phi(q)} and y_q to y_{phi(q)}; and a_e,
where e = {x_i, y_{i+c}} with c = 3 or -3, goes to a_{e'} with e' = {x_{phi(i)}, y_{phi(i)+c}}. Here
i and i + c are in Q by the definition of Q, so by the Claim phi(i + c) = phi(i) + c and e' is an
edge of F in G_M. The map is injective: phi is injective, the types (outer, inner) are kept, and
a_e is determined by the index of its outer end and the sign of c.

It sends every edge of H to an edge of G_M:
- edges at u1 and at u2 (including u1 u2 and u1 w), and the edges a w: the same adjacencies hold
  in G_M (u2 w is not an edge of H);
- an edge between two vertices of S_B: by (F5) its ends have indices in Q that differ by at most 2,
  the Claim keeps this difference, and adjacency in B depends only on the types and the difference;
- an edge from a_e to an end of e: by the definition of e'.

Two vertices whose indices were separated by a shrunk gap may become adjacent in G_M; this does
not matter, because H is only required to be a subgraph. Since the map is injective and sends
edges of H to edges of G_M, the image of H is a nonempty 4-regular subgraph of G_M. ∎

## Proof of the Theorem

By computation (see "Computation" below), G_m has no nonempty 4-regular subgraph for m = 7 and for
9 <= m <= 36. Let m >= 37 and suppose G_m has one. By Lemma 2 (with M = 34) so does G_34, which
contradicts the computation. ∎

**Corollary.** For every m >= 9, a(4m + 3) >= r(4m + 3) >= 17m + 2. Deleting j of the vertices
a_e gives a(4m + 3 - j) >= 17m + 2 - 5j, so a(n) >= 4.25 n - 13 for every n >= 36.

## Remarks

- Lemma 1 uses only (F1)-(F4): B connected and cubic, F 2-regular and edge-disjoint from B. Lemma 2
  uses (F5) in addition. Neither uses the girth of B, and both hold for a step k in place of 3
  with |k| <= 3 whenever F is 2-regular and edge-disjoint from B. For k = 2 the members
  m = 9, ..., 12 contain a 4-regular subgraph on six vertices (u1, u2, one a_e, and x_i, y_i,
  y_{i+2}); its set Q = {i, i + 2} has a gap of size at least 4, so the construction in the proof
  of Lemma 2 applies to it directly and every member with k = 2 contains such a subgraph.
- For m = 8 (k = 3) there is a 4-regular subgraph: u1, u2 and the inner 4-cycle y_0 y_2 y_4 y_6.
  Its set Q = {0, 2, 4, 6} has no gap of size 4, in agreement with the hypothesis m >= 37 of
  Lemma 2 (which is only used to obtain such a gap).

- **The template cannot be made denser by adding chords.** Take any graph B, any graph F on V(B),
  and build G as above. If some vertex b of B lies on three edges e1, e2, e3 of F, then G has a
  4-regular subgraph on the seven vertices u1, u2, w, b, a_{e1}, a_{e2}, a_{e3}: take the edges
  w a_{ei}, u1 a_{ei}, u2 a_{ei}, b a_{ei} (i = 1, 2, 3) and the two edges u1 w and u2 b. So F must
  have maximum degree at most 2, hence |E(F)| <= |V(B)|, and with a cubic B the family above has
  the largest number of edges this template allows, 8.5 |V(B)| + 2. The search graphs with more
  than 4.25 n edges (n = 26, 30, 32) are therefore not of this form.

## Computation

The Theorem needs "no nonempty 4-regular subgraph" for m = 7 and 9 <= m <= 36. Logs:
- `out/kubik_tam.log`: `kubik_aile.py | dort_duzenli.py` (0/1 program, HiGHS) for m = 7 and
  9 <= m <= 70. No 4-regular subgraph for m = 7 and 9 <= m <= 58 and 60 <= m <= 70; for m = 59
  the run reached its time limit (1500 s) without an answer. The values m = 37..70 are not needed
  for the proof;
- `out/kubik_cpsat.log`: the same model with CP-SAT for the m listed there.

The solvers report infeasibility without a machine-checkable certificate; the statement rests on
the agreement of two independent solvers on the range that the proof uses.

## Review

- An independent reviewer (Claude Sonnet, instructed to look for errors) re-derived Lemma 1 and
  Lemma 2, found no mathematical error, and tested them numerically where 4-regular subgraphs
  exist: the family with k = 1, 2 (about 40 subgraphs, transplant map applied and checked edge by
  edge) and random connected cubic B with random 2-regular F (142 subgraphs, 76 of them in Case 3b;
  the bound |Q| <= 12 is attained). Two corrections from that review are included above.
- A council of open-weight models (Open Math OS; six answered) was asked to find errors. One
  objected to the count at u in Case 2; the step is correct and is now written out in full.
