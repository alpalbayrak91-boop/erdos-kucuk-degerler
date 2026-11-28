import Mathlib.Order.Interval.Finset.Nat
import Mathlib.Order.Filter.Defs
import Mathlib.Data.Fin.Basic

open Finset Filter

namespace Green22

/--
A colouring `c : {1, ..., N} → Fin r` has the monochromatic sum-product property if there exist
`x, y ≥ 3` such that `x + y` and `xy` are both in `{1, ..., N}` and receive the same colour.
-/
def HasMonochromaticSumProduct (N : ℕ) (r : ℕ) (coloring : Icc 1 N → Fin r) : Prop :=
  ∃ x y : ℕ, 3 ≤ x ∧ 3 ≤ y ∧
    ∃ h_sum : x + y ∈ Icc 1 N, ∃ h_prod : x * y ∈ Icc 1 N,
      coloring ⟨x + y, h_sum⟩ = coloring ⟨x * y, h_prod⟩

theorem green_22.variants.lower_nine : ∀ r : ℕ, r ≠ 0 →
    ∀ N : ℕ, (∀ c : Icc 1 N → Fin r, HasMonochromaticSumProduct N r c) → 9 ≤ N := by
  intro r hr N h
  obtain ⟨x, y, hx, hy, _, hp, _⟩ := h (fun _ => ⟨0, Nat.pos_of_ne_zero hr⟩)
  exact le_trans (Nat.mul_le_mul hx hy) (Finset.mem_Icc.mp hp).2

end Green22
