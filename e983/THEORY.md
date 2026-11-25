# Erdős #983: Exact Prime-Covering Values $f(\pi(n)+1, n)$ for $n = 2 \dots 46$ via Z3 CEGAR

## Definition (`FormalConjectures/ErdosProblems/983.lean`)

For $n \ge 2$ and $\pi(n) < k \le n$, `Erdos983.f k n` is the smallest integer $r \ge 0$ such that for every $k$-element subset $A \subseteq \{1, \dots, n\}$, there exists a set $S$ of $r$ primes such that strictly more than $r$ elements of $A$ are $S$-smooth (divisible only by primes in $S$):

$$\text{numSmooth}(A, S) := |\{a \in A : \forall p \mid a,\; p \text{ prime} \implies p \in S\}| > r.$$

Note on $a = 1$: since $1$ has no prime factors, $1$ is $S$-smooth for *every* set of primes $S$ (including $S = \emptyset$, $r = 0$). For $n \in \{2, 3\}$, $k = \pi(n) + 1 = n$, so $A = \{1, \dots, n\}$ necessarily contains $1$, giving $\text{numSmooth}(A, \emptyset) = 1 > 0$ and therefore $f(\pi(n)+1, n) = 0$.

### Equivalence of $|S| = r$ (`f_eq`) and $|S| \le r$ (`f_le`) on $n = 2 \dots 46$

In literature prose, the condition is sometimes read with $|S| \le r$ (`f_le`) and in `FormalConjectures/ErdosProblems/983.lean` with $|S| = r$ (`f_eq`). Clearly $f_{\le}(n) \le f_{=}(n)$ whenever $r \le \pi(n)$, and in fact any witness $S_0 \subseteq P(n)$ with $|S_0| = s \le r$ and $\text{numSmooth}(A, S_0) > s$ only fails to pad to size $r$ if fewer than $r - s$ new $S$-smooth elements appear upon adding $r - s$ primes; hence $f_{\le}(n)$ and $f_{=}(n)$ could in principle differ if a small smooth cluster cannot be padded. Our Z3 solver checks **both** definitions independently and verifies that **$f_{\le}(n) = f_{=}(n)$ for every $2 \le n \le 46$** (`divergences = []`).

---

## Exact Values for $n = 2 \dots 46$

Sequence $f(\pi(n)+1, n)$ for $n = 2 \dots 46$:

```text
0, 0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6
```

Step jumps occur at:
- $n = 4$: $0 \to 1$ ($A = \{2, 3, 4\}$ avoids $1$)
- $n = 6$: $1 \to 2$ ($A = \{2, 3, 5, 6\}$)
- $n = 10$: $2 \to 3$ ($A = \{2, 5, 6, 7, 10\}$)
- $n = 15$: $3 \to 4$
- $n = 22$: $4 \to 5$ (attains the Erdős–Straus upper bound $2\pi(\sqrt{22}) + 1 = 5$, and likewise at $n = 23, 24$)
- $n = 35$: $5 \to 6$

Notice that at $n = 22, 23, 24$, $\pi(\sqrt{n}) = 2$, so $2\pi(\sqrt{n}) + 1 = 5 = f(\pi(n)+1, n)$, illustrating in finite range why $2\pi(\sqrt{n}) - f(\pi(n)+1, n)$ drops to $-1$ (matching the asymptotic negative answer to Erdős–Straus part (i) via Pomerance's prime-number-graph corollary).

---

## Z3 CEGAR Formulation & Large-Prime Decomposition

Let $P = \{p \le n : p \text{ prime}\}$, partitioned into:
- $P_{\text{small}} = \{p \in P : 2p \le n\}$ (at most $\pi(23) = 9$ primes for $n \le 46$), and
- $P_{\text{big}} = \{p \in P : 2p > n\}$.

Every prime $p \in P_{\text{big}}$ divides *only itself* in $\{1, \dots, n\}$. Consequently:
1. All primes in $P_{\text{big}}$ are completely symmetric in $\{1, \dots, n\}$, allowing lossless symmetry-breaking constraints $x_{p_{i+1}} \implies x_{p_i}$ across $P_{\text{big}}$.
2. For any subset $A \subseteq \{1, \dots, n\}$ and $S = S_{\text{small}} \sqcup S_{\text{big}}$, $\text{numSmooth}(A, S) = \text{numSmooth}(A, S_{\text{small}}) + |A \cap S_{\text{big}}|$, so maximizing over $S_{\text{big}}$ of size $r - |S_{\text{small}}|$ simply adds $\min(r - |S_{\text{small}}|, |A \cap P_{\text{big}}|)$.

In Counterexample-Guided Abstraction Refinement (CEGAR), Z3 searches for a boolean indicator vector $x \in \{0,1\}^n$ with $\sum_{a=1}^n x_a = \pi(n) + 1$ avoiding all smooth-cluster inequalities added so far:
- If a candidate $A$ admits a violating $S_{\text{small}}$, the exact pseudo-Boolean cut blocking $S_{\text{small}}$ is added and Z3 resolves.
- If no violating $S_{\text{small}}$ exists, $A$ is verified by an independent pure-Python checker (`verify_adversarial_witness`) and recorded in `e983_exact_46.json` (`lower_bound_witness_A`), certifying $f(\pi(n)+1, n) \ge r + 1$.
- When Z3 proves `unsat` at threshold $r$, no counterexample $A$ exists, certifying $f(\pi(n)+1, n) \le r$.

## Reproducibility

```bash
python3 e983/e983_exact_z3.py 46 > e983/e983_exact_46.json
```

## References

- P. Erdős, *Some applications of graph theory to number theory*, Proc. Second Chapel Hill Conf. Combinatorial Math. Appl. (1970), 136–145.
- C. Pomerance, *The prime number graph*, Math. Comp. **33** (1979), 399–408.
- [erdosproblems.com/983](https://www.erdosproblems.com/983) and `FormalConjectures/ErdosProblems/983.lean`.
