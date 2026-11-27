# Erdős #642: a circumference refinement, $3n - c - 1$

*Status (27 Nov 2026).* This note records a conjecture, a proved lower bound that makes it sharp,
exhaustive data for $n \le 10$, and a reduction. The upper bound is **not** proved. We did not find
the statement in Draganić–Methuku–Munhá Correia–Sudakov or in Draganić–Girão; the
erdosproblems.com forum thread could not be re-read on the day of writing, so "not found" is the
honest status, not "new".

Notation as in [`THEORY.md`](THEORY.md) and [`CORE_REDUCTION.md`](CORE_REDUCTION.md): a graph is
**good** if every cycle has more vertices than chords, equivalently $e(G[S]) \le 2|S| - 1$ whenever
$G[S]$ is Hamiltonian. The **circumference** $c(G)$ is the length of a longest cycle.

## Conjecture C

> A good graph on $n$ vertices with circumference $c \ge 6$ has at most $3n - c - 1$ edges.

Reading: a longest cycle spans at most $2c - 1$ edges, and each of the $n - c$ vertices off it adds
at most $3$. For $c = n$ this is the trivial bound $2n-1$; for $c = 6$ it is $3n - 7$. Since
$3n - c - 1 \le 3n - 7$ for $c \ge 6$, and good graphs of circumference at most $5$ have fewer edges
(Kopylov's theorem for 2-connected graphs, block by block otherwise), Conjecture C implies
$f(n) \le 3n - 7$ for $n \ge 6$, hence a positive answer to Erdős Problem 642.

## Theorem 1 (the bound is attained)

For all integers $n \ge c \ge 6$ there is a good graph on $n$ vertices with circumference $c$ and
exactly $3n - c - 1$ edges.

**Construction.** Let $t = c - 5 \ge 1$ and $m = n - c + 2 \ge 2$. The graph $G(m,t)$ has

* three hubs $z, p, q$ with edges $zp$ and $zq$;
* an independent set $B$ of $m$ vertices, each joined to $z, p, q$;
* a path $u_1 u_2 \dots u_t$, every $u_i$ joined to $p$, and in addition $u_1 z$ and $u_t q$.

It has $m + t + 3 = n$ vertices and $2 + 3m + (t-1) + t + 2 = 3m + 2t + 3 = 3n - c - 1$ edges.
For $t = 1$ it is $K_{1,2,m+1}$.

**Proof.** Deleting the hubs leaves the isolated vertices of $B$ and the path $u_1 \dots u_t$. So a
cycle $Z$ with $h$ hubs splits, after removing them, into at most $h$ *segments*, each a single
vertex of $B$ or an interval of the path. Write $j$ for the number of $B$-vertices on $Z$, $s$ for
the number of path vertices, $\rho$ for the number of maximal intervals of the path they form, and
$S = V(Z)$.

*Circumference.* With three hubs there are at most three segments. If some segment is a path
interval, at most two are $B$-vertices, so $|Z| \le 3 + 2 + t$; with two or three path segments the
count is smaller, and with at most two hubs $|Z| \le 2 + t + 1$. The cycle
$z\,u_1 \dots u_t\,q\,b\,p\,b'\,z$ has length $t + 5$. Hence $c = t + 5$.

*Goodness.* We bound $e(G[S])$ against $2|S| - 1 = 2(h + j + s) - 1$. The path spans $s - \rho$
edges inside $S$.

* $h = 3$: $e(G[S]) = 2 + 3j + (s - \rho) + s + \varepsilon$, where $\varepsilon \le 2$ counts
  $u_1 z$ and $u_t q$. The claim is $j - \rho + \varepsilon \le 3$. If $s = 0$ then
  $\rho = \varepsilon = 0$ and $j \le 3$. If $s > 0$ then $\rho \ge 1$ and one segment is a path
  interval, so $j \le 2$.
* $h = 2$: $e(G[S]) \le 1 + 2j + (s - \rho) + s + 1 \le 3 + 2j + 2s$.
* $h = 1$: then $j = 0$ and $e(G[S]) \le (s - \rho) + s + 1 \le 2s + 1$.

$h = 0$ is impossible. $\blacksquare$

Machine check: `circumference/family.py` prints $G(m,t)$ for $2 \le m \le 7$, $2 \le t \le 11$,
$n \le 17$; all 50 are good with the stated circumference and edge count.

## Data: equality for every $c$, $n \le 10$

`geng n | circumference_check` over **all** graphs on $n$ vertices. Entry: maximum number of edges
of a good graph with circumference exactly $c$.

| $n$ | $c=6$ | $c=7$ | $c=8$ | $c=9$ | $c=10$ | good graphs / all graphs |
|---|---|---|---|---|---|---|
| 7 | 14 | 13 | | | | 871 / 1,044 |
| 8 | 17 | 16 | 15 | | | 8,014 / 12,346 |
| 9 | 20 | 19 | 18 | 17 | | 106,325 / 274,668 |
| 10 | 23 | 22 | 21 | 20 | 19 | 1,896,677 / 12,005,168 |

Every entry equals $3n - c - 1$ and no good graph exceeds it. For $n = 10$ the numbers of extremal
graphs are $1, 9, 239, 3983, 425039$ for $c = 6, \dots, 10$. For $c \le 5$ the maxima are smaller and
follow a different pattern ($c = 5$: $12, 15, 18, 19$). Raw output:
[`circumference/results_n7_to_10.txt`](circumference/results_n7_to_10.txt). A run for $n = 11$
(edge counts 21–26) was in progress at the time of writing: five of eight residue classes had
finished, with maxima $26, 25, 24, 23, 22, 21$ and no excess; it is not claimed as complete.

## Lemma 2 (shape of a minimal counterexample)

Let $G$ be a counterexample to Conjecture C with the fewest vertices, and then the fewest edges. Then

1. $G$ is not Hamiltonian, and $e(G) = 3n - c$;
2. for **every** longest cycle $C$, every vertex outside $C$ has degree at least $4$;
3. more generally, if $T \subseteq V(G)$ and $G - T$ has circumference $c'$, then at least
   $3|T| + 1 - (c - c')$ edges meet $T$. In particular, if $G - T$ is Hamiltonian, at least
   $n - c + 2|T| + 1$ edges meet $T$.

*Proof.* (1) A Hamiltonian good graph has at most $2n - 1$ edges. Deleting an edge off a longest
cycle keeps the graph good with the same circumference. (2) Deleting a vertex $x \notin C$ of degree
at most $3$ gives a good graph with circumference $c$ and at least $3(n-1) - c$ edges. (3) Apply
minimality to $G - T$, or the Hamiltonian bound $2(n - |T|) - 1$. $\blacksquare$

Condition (2) is weaker than "minimum degree at least $4$", so Conjecture C is stronger than the
core conjecture of [`CORE_REDUCTION.md`](CORE_REDUCTION.md).

## The first open case

$c = n - 1$: *if $G$ is good and not Hamiltonian, and $G - x$ has a Hamiltonian cycle $C$, then
$e(G) \le 2n$.* Equivalently $e(G[C]) \le 2c + 2 - d(x)$ when $d(x) \ge 4$. The inequalities coming
from the cycles through $x$ that skip one gap of $C$ between consecutive neighbours of $x$ are not
enough on their own: with $k$ chords of $C$ they give that a gap with $g$ inner vertices meets at
least $k + d(x) - 2 - c + g$ chords, and the arcs between two neighbours give matching upper
bounds, leaving slack exactly $1$. The fact that $C$ is a *longest* cycle has to be used.

## Also: $f(13) = 32$

The core check of `CORE_REDUCTION.md` for $n = 13$ finished: 27,472,319,548 graphs with minimum
degree at least $4$ and $32$ edges, none good
([`core/results_core_n13.txt`](core/results_core_n13.txt)). By Theorem 3 there, $f(13) = 32$ and
$K_{1,2,10}$ is the unique extremal graph.

## References

- N. Draganić, A. Methuku, D. Munhá Correia, B. Sudakov, *Cycles with many chords*,
  Random Structures Algorithms **64** (2024), 3–16; [arXiv:2306.09157](https://arxiv.org/abs/2306.09157).
- N. Draganić, A. Girão, *Cycles with almost linearly many chords*, arXiv:2601.08769.
- G. N. Kopylov, *Maximal paths and cycles in a graph*, Dokl. Akad. Nauk SSSR **234** (1977), 19–21.
