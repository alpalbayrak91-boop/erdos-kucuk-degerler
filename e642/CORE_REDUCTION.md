# Erdős #642: reduction of the exact value $f(n) = 3n-7$ to graphs of minimum degree $\ge 4$

*Status of this note (26 Nov 2026).* The values $f(n) = 3n-7$ for $6 \le n \le 12$ and the uniqueness of
the extremal graph $K_{1,2,n-3}$ for $7 \le n \le 12$ were reported by Boris Alexeev in the
[erdosproblems.com forum thread](https://www.erdosproblems.com/forum/thread/642) (28 Jan 2026,
computer search). What this note adds is an elementary **reduction**: the exact formula together with
uniqueness is *equivalent* to a statement about graphs of minimum degree at least $4$ only, and that
statement can be checked far more cheaply than a full search. We did not find this reduction in the
forum thread, in Chen–Erdős–Staton or in Draganić–Methuku–Munhá Correia–Sudakov; it is elementary and
may well be folklore. Nothing here bounds $f(n)$ for general $n$: the problem stays open.

## Setting

A graph is **good** if every cycle has strictly more vertices than chords, and $f(n)$ is the maximum
number of edges of a good graph on $n$ vertices. As in [`THEORY.md`](THEORY.md):

* **(F1)** Subgraphs of good graphs are good; adding edges to a bad graph keeps it bad.
* **(F2)** $G$ is bad iff some $S \subseteq V(G)$ with $|S| \ge 5$ has $G[S]$ Hamiltonian and
  $e(G[S]) \ge 2|S|$.

Write $T_m = K_{1,2,m}$: a centre $c$, a non-adjacent pair $p, q$, and an independent set $B$ of size
$m$, with every vertex of $B$ joined to $c, p, q$ and $c$ joined to $p, q$. It has $m+3$ vertices and
$3m+2$ edges. With $n = m+3$ this is the graph $K_{3,n-3} \cup P_3$ of `THEORY.md`, Proposition 1, so
$T_{n-3}$ is good and $f(n) \ge 3n-7$.

## Lemma 1 (peeling)

Let $n \ge 7$ and assume $f(n-1) \le 3(n-1)-7$.

1. A good graph on $n$ vertices with exactly $3n-6$ edges has minimum degree at least $4$.
2. If $G$ is good on $n$ vertices with exactly $3n-7$ edges and $\deg v \le 3$, then $\deg v = 3$ and
   $G - v$ has exactly $3(n-1)-7$ edges.

*Proof.* $G - v$ is good on $n-1$ vertices. In (1), $\deg v \le 3$ would give
$e(G-v) \ge 3n-9 > 3(n-1)-7$. In (2), $e(G-v) = 3n-7-\deg v \le 3n-10$ forces $\deg v \ge 3$. $\blacksquare$

## Lemma 2 (one-vertex extensions of $T_m$)

Let $m \ge 3$ and let $G$ be obtained from $T_m$ by adding a new vertex $v$ whose neighbourhood $N$
has $|N| \ge 3$. Then $G$ is good if and only if $N = \{c, p, q\}$, in which case $G = T_{m+1}$.

*Proof.* If $N = \{c,p,q\}$ then $G = T_{m+1}$, which is good. Otherwise $N$ meets $B$ (it has at least
three elements and is not $\{c,p,q\}$). By (F1) it suffices to treat $|N| = 3$: choose three
neighbours of $v$, at least one of them in $B$, and delete the other edges at $v$. Let
$j = |N \cap B| \in \{1,2,3\}$ and pick $T \subseteq B$ with $|T| = 3$ and $N \cap B \subseteq T$.
Put $S = \{c,p,q,v\} \cup T$. Then $|S| = 7$ and

$$e(G[S]) = \underbrace{2}_{cp,\,cq} + \underbrace{9}_{T \times \{c,p,q\}} + \underbrace{3}_{\text{edges at } v} = 14 = 2|S| .$$

It remains to exhibit a Hamiltonian cycle of $G[S]$.

* $j = 1$, $N = \{b, h_1, h_2\}$ with $h_1, h_2 \in \{c,p,q\}$, $T = \{b, b_1, b_2\}$:
  $\;v\,b\,x\,b_1\,y\,b_2\,z\,v$ with $\{x,y,z\} = \{c,p,q\}$ and $z = h_1$.
* $j = 2$, $N = \{b, b', h\}$, $T = \{b, b', b_1\}$: $\;v\,b\,q\,b_1\,p\,c\,b'\,v$.
* $j = 3$, $N = T = \{b, b', b''\}$: $\;v\,b\,q\,b''\,p\,c\,b'\,v$.

Each listed consecutive pair is an edge ($B$–hub edges, the edge $pc$, and the edges at $v$). So $G$
is bad by (F2). $\blacksquare$

## Theorem 3 (inductive step)

Let $n \ge 8$. Assume

* **(i)** $f(n-1) = 3(n-1)-7$ and $T_{n-4}$ is the unique extremal graph on $n-1$ vertices;
* **(ii) Core($n$):** no good graph on $n$ vertices has minimum degree $\ge 4$ and exactly $3n-7$
  edges.

Then $f(n) = 3n-7$ and $T_{n-3}$ is the unique extremal graph on $n$ vertices.

*Proof.* Suppose a good graph on $n$ vertices has at least $3n-6$ edges; delete edges to get a good
$G'$ with exactly $3n-6$ edges. By Lemma 1(1), $\delta(G') \ge 4$. The degree sum is $6n-12 < 6n$, so
a vertex $v$ of minimum degree has degree $4$ or $5$. If it is $4$, then $G' - v$ is good with
$3(n-1)-7$ edges, hence $G' - v \cong T_{n-4}$ by (i), and $G'$ is an extension of $T_{n-4}$ by a vertex
of degree $4$, contradicting Lemma 2 ($n-4 \ge 4$). So $\delta(G') \ge 5$; deleting any edge leaves a
good graph with $3n-7$ edges and minimum degree $\ge 4$, contradicting (ii). Hence $f(n) \le 3n-7$,
with equality by $T_{n-3}$.

Now let $G$ be good with exactly $3n-7$ edges. By (ii), $\delta(G) \le 3$. By Lemma 1(2) a vertex $v$
of degree $\le 3$ has degree exactly $3$ and $G - v$ is extremal, so $G - v \cong T_{n-4}$ by (i), and
Lemma 2 gives $G \cong T_{n-3}$. $\blacksquare$

## Corollary 4 (equivalence)

Let $N \ge 8$. Given the base case $n = 7$ ($f(7) = 14$, unique extremal graph $T_4$), the following
are equivalent:

* $f(n) = 3n-7$ and $T_{n-3}$ is the unique extremal graph, for all $7 \le n \le N$;
* Core($n$) holds for all $8 \le n \le N$.

*Proof.* ($\Leftarrow$) Induction with Theorem 3. ($\Rightarrow$) A good graph with $3n-7$ edges and
minimum degree $\ge 4$ would be extremal and not isomorphic to $T_{n-3}$, whose minimum degree is $3$.
$\blacksquare$

So the sharp form of the Hamburger–Szegedy question, "$f(n) = 3n-7$ for all $n \ge 6$", is equivalent
(together with uniqueness for $n \ge 7$) to:

> **Core conjecture.** For $n \ge 8$, every graph on $n$ vertices with minimum degree at least $4$
> and exactly $3n-7$ edges contains a cycle with at least as many chords as vertices.

Two remarks on what the hypothesis cannot be weakened to. Minimum degree $3$ is not enough: $T_{n-3}$.
The edge count cannot drop to $2n$: a connected $4$-regular graph is good iff it is non-Hamiltonian
(a proper induced subgraph on $s$ vertices has fewer than $2s$ edges), and such graphs exist (below,
$n = 11$).

Also, by the usual peeling of vertices of degree $\le 3$, Erdős's question $f(n) = O(n)$ is
equivalent to a linear bound for good graphs of minimum degree $\ge 4$; and if such graphs always had
at most $cn$ edges for some $c < 3$, then Core($n$) would hold for all $n > 7/(3-c)$ and the exact
formula would follow from a finite check.

## Proposition 5 (no computation needed for $n = 8$)

Core(8) holds: a graph on $8$ vertices with minimum degree $\ge 4$ is Hamiltonian by Dirac's theorem,
and with $17 \ge 16$ edges $S = V$ is a witness in (F2). More generally a counterexample to Core($n$)
must be non-Hamiltonian, since $3n-7 \ge 2n$ for $n \ge 7$.

## Verification of Core($n$) for $9 \le n \le 12$

`geng -d4 n (3n-7):(3n-7)` (nauty) piped into [`core/good_check.c`](core/good_check.c), which tests
(F2) directly: all vertex subsets, Hamiltonicity by depth-first search.

| $n$ | edges $3n-7$ | graphs with $\delta \ge 4$ | good |
|---|---|---|---|
| 8 | 17 | 24 | 0 |
| 9 | 20 | 714 | 0 |
| 10 | 23 | 35,225 | 0 |
| 11 | 26 | 2,505,044 | 0 |
| 12 | 29 | 233,751,478 | 0 |

With the base case (all 65 graphs on 7 vertices with 14 edges: exactly one good; all 41 with 15
edges: none good) this re-derives $f(n) = 3n-7$ and uniqueness for $7 \le n \le 12$, independently of
the earlier full searches. Lemma 2 was also checked by machine for $n = 8, \dots, 11$: exactly one good
degree-3 extension up to isomorphism, no good degree-4 extension. Raw output:
[`core/results_core_n7_to_12.txt`](core/results_core_n7_to_12.txt). Reproduce with
`core/run_core_check.sh 11` (about ten seconds) or `core/run_core_check.sh 12` (about ten CPU-minutes).

Core(13) has since been checked: 27,472,319,548 graphs with minimum degree at least $4$ and $32$ edges, none
good ([`core/results_core_n13.txt`](core/results_core_n13.txt)). Hence $f(13) = 32$ with unique extremal graph
$K_{1,2,10}$; see [`CIRCUMFERENCE.md`](CIRCUMFERENCE.md).

## How sparse are good graphs of minimum degree $\ge 4$?

Searching all edge counts from $2n$ upwards:

| $n$ | good graphs with $\delta \ge 4$ |
|---|---|
| $\le 8$ | none (Dirac) |
| 9 | none (edge counts 18–20 checked) |
| 10 | none (20–23 checked) |
| 11 | exactly one: $4$-regular, 22 edges, graph6 `J?ouPjI{@i?` (two copies of $K_5 - e$ joined through a cut vertex); none with 23–26 edges |
| 12 | exactly two, both $4$-regular (24 edges): `K?b@`cr]EWX_`, `KCOcbQUdbWLG`; none with 25–30 edges |

So for $n \le 12$ every good graph of minimum degree $\ge 4$ is $4$-regular and has $2n$ edges, well
below $3n-7$. This is a small-$n$ phenomenon and not the general picture:

**Remark (density $7/3$ is attainable).** A graph is good iff each of its blocks is good, because a
cycle and all its chords lie in one block. Take $T_m$ ($m \ge 3$) and, for every $b \in B$, a new copy
of $K_5 - e$ whose two vertices of degree $3$ are joined to $b$. The blocks are $T_m$ and $m$ copies of
"$K_5 - e$ plus a vertex joined to its two non-adjacent vertices" ($6$ vertices, $11$ edges, good by
the $n=6$ data). The result is good, has minimum degree $4$, $n = 6m+3$ vertices and $14m+2$ edges, so
$e/n \to 7/3$.

**Question.** Let $c^\ast$ be the supremum of $e(G)/|G|$ over good graphs of minimum degree $\ge 4$.
The remark gives $c^\ast \ge 7/3$. Is $c^\ast < 3$? By the remark after Corollary 4 that would settle
the exact value of $f(n)$ up to a finite check, and $c^\ast < \infty$ is exactly Erdős's question.

## References

- B. Alexeev, comment of 28 Jan 2026 in the [erdosproblems.com thread for #642](https://www.erdosproblems.com/forum/thread/642).
- G. Chen, P. Erdős, W. Staton, *Proof of a conjecture of Bollobás on nested cycles*, J. Combin. Theory Ser. B **66** (1996), 38–43.
- N. Draganić, A. Methuku, D. Munhá Correia, B. Sudakov, *Cycles with many chords*, Random Structures Algorithms **64** (2024), 3–16; [arXiv:2306.09157](https://arxiv.org/abs/2306.09157).
- B. D. McKay, A. Piperno, *Practical graph isomorphism, II*, J. Symbolic Comput. **60** (2014), 94–112 (nauty, `geng`).
