import Mathlib.Order.LiminfLimsup
import Mathlib.Algebra.Order.Archimedean.Real.Basic
import Mathlib.Order.Lattice.Nat
import Mathlib.Data.Finset.Prod
import Mathlib.Order.Interval.Finset.Nat
import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith

open Filter

namespace Green24

/--
The maximum number of $\lbrace 0,1,3 \rbrace$ affine translates that a set of size $n$ can
contain.
-/
noncomputable def max013AffineTranslates (n : ℕ) : ℕ :=
  sSup { k |
    ∃ A : Finset ℤ,
      A.card = n ∧
      -- Iterate over (x,y) = (a, a + d) in A × A (x ≠ y), and check if a + 3d = x + 3(y - x) ∈ A
      k = ((A ×ˢ A).filter (fun (x, y) ↦ x ≠ y ∧ x + 3 * (y - x) ∈ A)).card
  }

namespace variants

/-- From [Aa19] p.577: the trivial upper bound is $n^2$ (non asymptotic). -/
theorem upper_trivial {n : ℕ} : max013AffineTranslates n ≤ n ^ 2 := by
  apply csSup_le
  · exact ⟨_, ⟨(Finset.range n).image Int.ofNat, by
      rw [Finset.card_image_of_injective _ Int.ofNat_injective, Finset.card_range], rfl⟩⟩
  · rintro k ⟨A, hA, rfl⟩
    apply le_trans (Finset.card_filter_le _ _)
    rw [Finset.card_product, hA, pow_two]

/-- The asymptotic constant $\gamma$ defined in [Aa19] p.579. -/
noncomputable def gamma : ℝ :=
  limsup (fun n : ℕ => (max013AffineTranslates n : ℝ) / ((n : ℝ)^2)) atTop

/-- For `A = {0, ..., 12m - 1}` the pairs `(x, x + d)` with `x < 6m`, `1 ≤ d ≤ 2m` all count. -/
theorem twelve_mul_sq_le (m : ℕ) : 12 * m ^ 2 ≤ max013AffineTranslates (12 * m) := by
  set A : Finset ℤ := (Finset.range (12 * m)).image Int.ofNat with hAdef
  have hA : A.card = 12 * m := by
    rw [hAdef, Finset.card_image_of_injective _ Int.ofNat_injective, Finset.card_range]
  have hmem : ∀ z : ℤ, 0 ≤ z → z < 12 * m → z ∈ A := by
    intro z h0 h1
    rw [hAdef, Finset.mem_image]
    exact ⟨z.toNat, Finset.mem_range.2 (by omega), by simp; omega⟩
  have hbdd : BddAbove {k | ∃ A : Finset ℤ, A.card = 12 * m ∧
      k = ((A ×ˢ A).filter (fun (x, y) ↦ x ≠ y ∧ x + 3 * (y - x) ∈ A)).card} := by
    refine ⟨(12 * m) ^ 2, ?_⟩
    rintro k ⟨B, hB, rfl⟩
    exact le_trans (Finset.card_filter_le _ _) (by rw [Finset.card_product, hB, pow_two])
  refine le_trans ?_ (le_csSup hbdd ⟨A, hA, rfl⟩)
  have hS : ((Finset.range (6 * m)) ×ˢ (Finset.Icc 1 (2 * m))).card = 12 * m ^ 2 := by
    rw [Finset.card_product, Finset.card_range, Nat.card_Icc, Nat.add_sub_cancel]; ring
  rw [← hS]
  apply Finset.card_le_card_of_injOn (fun p : ℕ × ℕ => ((p.1 : ℤ), (p.1 : ℤ) + p.2))
  · intro p hp
    have hp' := Finset.mem_coe.1 hp
    rw [Finset.mem_product, Finset.mem_range, Finset.mem_Icc] at hp'
    rw [Finset.mem_coe, Finset.mem_filter, Finset.mem_product]
    refine ⟨⟨hmem (p.1 : ℤ) (by positivity) (by omega), hmem ((p.1 : ℤ) + p.2) (by positivity) (by omega)⟩, ?_, ?_⟩
    · show (p.1 : ℤ) ≠ (p.1 : ℤ) + p.2
      omega
    · show (p.1 : ℤ) + 3 * (((p.1 : ℤ) + p.2) - p.1) ∈ A
      exact hmem _ (by omega) (by omega)
  · intro p _ q _ h
    simp only [Prod.mk.injEq] at h
    ext <;> omega

theorem lower_HL : gamma ≥ 1/12 := by
  unfold gamma
  have hb : IsBoundedUnder (· ≤ ·) atTop
      (fun n : ℕ => (max013AffineTranslates n : ℝ) / ((n : ℝ)^2)) := by
    refine ⟨1, Filter.eventually_map.2 (Filter.Eventually.of_forall fun n => ?_)⟩
    rcases Nat.eq_zero_or_pos n with rfl | hn
    · simp
    · rw [div_le_one (by positivity)]
      exact_mod_cast upper_trivial
  refine Filter.le_limsup_of_frequently_le ?_ hb
  rw [Filter.frequently_atTop]
  intro a
  refine ⟨12 * (a + 1), by omega, ?_⟩
  have h : ((12 * (a + 1) ^ 2 : ℕ) : ℝ) ≤ (max013AffineTranslates (12 * (a + 1)) : ℝ) := by
    exact_mod_cast twelve_mul_sq_le (a + 1)
  have hpos : (0 : ℝ) < ((12 * (a + 1) : ℕ) : ℝ) ^ 2 := by positivity
  show 1 / 12 ≤ (max013AffineTranslates (12 * (a + 1)) : ℝ) / ((12 * (a + 1) : ℕ) : ℝ) ^ 2
  rw [le_div_iff₀ hpos]
  push_cast at h ⊢
  nlinarith

end variants

end Green24
