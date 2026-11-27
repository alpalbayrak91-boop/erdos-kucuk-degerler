# Draft comment for erdosproblems.com/642 (not posted)

Before posting: re-read the thread and search it for "circumference" and "longest cycle".

---

Two computational remarks and a question, extending Boris Alexeev's values.

1. $f(13) = 32$, with $K_{1,2,10}$ the unique extremal graph. This uses a reduction: given the result
   for $n-1$, it suffices to check that no graph on $n$ vertices with minimum degree at least $4$ and
   exactly $3n-7$ edges has the property (for $n = 13$: about $2.7 \times 10^{10}$ graphs, none).

2. A refinement by circumference. For all graphs with $n \le 10$ vertices, the maximum number of edges
   of a graph with the property whose longest cycle has exactly $c \ge 6$ vertices is exactly
   $3n - c - 1$. The bound is attained for all $n \ge c \ge 6$ by an explicit family: hubs $z,p,q$ with
   $zp, zq$; $n-c+2$ vertices joined to all three hubs; a path $u_1 \dots u_{c-5}$ with every $u_i$
   joined to $p$, plus $u_1 z$ and $u_{c-5} q$.

Question: is it true that a graph in which every cycle has more vertices than chords, with
circumference $c \ge 6$, has at most $3n - c - 1$ edges? This would give $f(n) = 3n - 7$ for $n \ge 6$.
The first case I cannot do is $c = n-1$.

Details and code: https://github.com/alpalbayrak91-boop/erdos-kucuk-degerler/blob/main/e642/CIRCUMFERENCE.md
