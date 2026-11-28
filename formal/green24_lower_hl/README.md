# Green's Open Problem 24: `lower_HL` (formal proof of a known result)

Label: **formal proof of a known result** (formalization). Not a new mathematical result. Work done by a
local AI agent; Lean source checked by the compiler and an independent gate.

## Statement

Upstream: [google-deepmind/formal-conjectures, `FormalConjectures/GreensOpenProblems/24.lean`](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/GreensOpenProblems/24.lean),
theorem `Green24.variants.lower_HL` (`@[category research solved]`, body `sorry` on upstream `main` at f606af1).

```lean
noncomputable def gamma : ℝ :=
  limsup (fun n : ℕ => (max013AffineTranslates n : ℝ) / ((n : ℝ)^2)) atTop

theorem lower_HL : gamma ≥ 1/12
```

`max013AffineTranslates n` is the maximum, over `A ⊆ ℤ` with `|A| = n`, of the number of pairs `(x, y)`,
`x ≠ y`, with `x + 3(y - x) ∈ A`. Source of the bound: [Aa19] J. Aaronson, "Maximising the number of
solutions to a linear equation in a set of integers", Bull. LMS 51 (2019), 577-594, equation (1.2).
Definitions and statement are verbatim from upstream (`upper_trivial` and its upstream proof are included).

## Proof idea

For `n = 12m` take `A = {0, ..., 12m - 1}`. The pairs `(x, x + d)` with `x < 6m`, `1 ≤ d ≤ 2m` are distinct
and satisfy `x + 3d < 12m`, so `max013AffineTranslates (12m) ≥ 12m² = n²/12`. The ratio is bounded by 1
(`upper_trivial`), so the limsup is at least `1/12` (`Filter.le_limsup_of_frequently_le`).

## Build

Lean `v4.37.0-rc1`, Mathlib rev `6ebcce37335bcb6bca64596e5d57bb3035648030`, targeted imports:

```
lake env lean --trust=0 formal/green24_lower_hl/Green24LowerHL.lean
```

## Gate verdict

Independent gate (statement and definitions compared with upstream, `--trust=0`, `#print axioms`): `GECTI`
(pass), axioms `propext`, `Classical.choice`, `Quot.sound` only. Full verdict: `gate_verdict.json`.
A Palomar-layout project is at https://github.com/alpalbayrak91-boop/green24-lower-hl-palomar.
