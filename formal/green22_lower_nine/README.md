# Green's Open Problem 22: `lower_nine` (formal proof of a known result)

Label: **formal proof of a known result** (formalization). This is not a new mathematical result; the
argument is the one stated in the upstream docstring.

## Statement

Upstream: [google-deepmind/formal-conjectures, `FormalConjectures/GreensOpenProblems/22.lean`](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/GreensOpenProblems/22.lean),
theorem `Green22.green_22.variants.lower_nine` (`@[category research solved]`, body `sorry` on upstream `main`
at commit f606af1, 27 Nov 2026).

```lean
theorem green_22.variants.lower_nine : ∀ r : ℕ, r ≠ 0 →
    ∀ N : ℕ, (∀ c : Icc 1 N → Fin r, HasMonochromaticSumProduct N r c) → 9 ≤ N
```

`HasMonochromaticSumProduct N r c` says there are `x, y ≥ 3` with `x + y, x * y ∈ {1, ..., N}` of the same
colour. The statement and the definition are copied verbatim from upstream.

## Proof idea

Apply the hypothesis to the constant colouring (everything gets colour `0`, which exists since `r ≠ 0`).
It yields `x, y ≥ 3` with `x * y ≤ N`, hence `9 ≤ 3 * 3 ≤ x * y ≤ N`.

## Build

Lean `v4.37.0-rc1`, Mathlib rev `6ebcce37335bcb6bca64596e5d57bb3035648030`. Inside any Lake project with that
Mathlib:

```
lake env lean --trust=0 formal/green22_lower_nine/Green22LowerNine.lean
```

Imports are targeted (`Mathlib.Order.Interval.Finset.Nat`, `Mathlib.Order.Filter.Defs`, `Mathlib.Data.Fin.Basic`).

## Gate verdict

Checked by an independent gate (statement compared with upstream, `--trust=0`, `#print axioms`): verdict `GECTI`
(pass), axioms `propext`, `Classical.choice`, `Quot.sound` only; no `sorry`, `native_decide` or extra axioms.
Full verdict: `gate_verdict.json`.
