# `e642/` — Erdős Problem #642 Exact Small Values (`n = 0..9`)

This directory contains the exact canonical-enumeration solver, independent pure-Python verifier, and optimal graph witnesses for [Erdős Problem #642](https://www.erdosproblems.com/642) (`Erdos642.maxEdges` in `google-deepmind/formal-conjectures`).

- [`THEORY.md`](THEORY.md): Mathematical formulation, Proposition 1 ($f(n) \ge 3n - 7$ for $n \ge 3$), exact values for $n = 0 \dots 9$, and uniqueness results.
- [`e642_exact.c`](e642_exact.c): Exact C canonical-enumeration solver up to $n = 9$ (with `--test-canon` sanity check against OEIS `A000088`).
- [`verify_e642.py`](verify_e642.py): Self-contained pure-Python cycle-chord witness checker (`n = 0..9`) and branch-and-bound solver (`n = 0..8`).
- [`witnesses_n0_to_9.json`](witnesses_n0_to_9.json): Machine-readable optimal witnesses for $n = 0 \dots 9$.
- [`results_exact_n2_to_9.txt`](results_exact_n2_to_9.txt): Exact solver log for $n = 2 \dots 9$.
- [`CORE_REDUCTION.md`](CORE_REDUCTION.md): reduction of "$f(n) = 3n-7$ with unique extremal graph $K_{1,2,n-3}$" to graphs of minimum degree $\ge 4$ (Lemmas 1–2, Theorem 3, Corollary 4), with the core check for $n \le 12$.
- [`core/`](core): `good_check.c` (direct test of the cycle–chord property), `extend.py`, `run_core_check.sh`, and the raw results `results_core_n7_to_12.txt`.
- [`CIRCUMFERENCE.md`](CIRCUMFERENCE.md): Conjecture C (a good graph with circumference $c \ge 6$ has at most $3n-c-1$ edges; **refuted** at $n = 13$, see the file), a proof that the value is attained for all $n \ge c \ge 6$, exhaustive data for $n \le 10$, and $f(13) = 32$.
- [`circumference/`](circumference): `circumference_check.c`, `family.py`, raw results.

## Replay the n = 13 result and circumference witnesses

From the repository root, run `python3 e642/reproduce.py` (Python 3.10+).
It directly checks every simple cycle of the four published circumference
counterexamples and of the 32-edge witness \(K_{1,2,10}\). It also checks the
recorded shard coverage and counts against `core/results_core_n13.txt`.
That log contains 27,472,319,548 candidate graphs and zero good graphs.

For a fresh upper-bound replay, use 64-bit Linux with a C compiler and nauty's
`geng` (also found as `nauty-geng` on some distributions):

```sh
python3 e642/reproduce.py --shard 0
python3 e642/reproduce.py --all-shards
```

Shards 0 through 15 can also be replayed separately. Use `--all-shards` or run
all 16 shard commands for full coverage. The enumeration takes hours of CPU
time. The n = 13 upper bound uses the induction in [CORE_REDUCTION.md](CORE_REDUCTION.md)
and its n = 12 premise. The n = 14 circumference witness has 30 edges and
addresses the refuted circumference conjecture. The package leaves the exact
value of \(f(14)\) outside the replay scope.
