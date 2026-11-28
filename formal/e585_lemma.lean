import Mathlib.Combinatorics.SimpleGraph.Clique
import Mathlib.Data.Finset.Card
import Mathlib.Data.Finset.Sum
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset

/-!
# Erdős 585: the join `K₂ ∨ H` has no 4-regular subgraph

Lemma (repository README, `adaylar/s3_e585_ayni_koseli_iki_cevrim`): let `H` be a triangle-free
graph in which every set of `t ≥ 4` vertices spans at most `2t - 5` edges. Then `K₂ ∨ H` has no
subgraph that is 4-regular on a nonempty vertex set.

Vertex type of the join: `Fin k ⊕ Fin 2` (the two new vertices are `Sum.inr 0`, `Sum.inr 1`).
"Spans at most `2t - 5` edges" is stated with ordered pairs: the number of ordered pairs `(a, b)` in
`T × T` with `H.Adj a b` is at most `2 * (2 * |T| - 5)` (each edge is counted twice).
"4-regular on `S`" means: a subgraph `K ≤ G` such that every `v ∈ S` has exactly four `K`-neighbours
in `S`.

Checked with Lean `v4.37.0-rc1` and Mathlib `6ebcce37335b`:
`lake env lean formal/e585_lemma.lean`; `#print axioms E585.join_no_four_regular` gives
`[propext, Classical.choice, Quot.sound]` (no `sorry`, no `native_decide`, no new axioms).
-/

open Finset

namespace E585

/-- `K₂ ∨ H`: `H` on the left copy, an edge between the two new vertices, and every new vertex
adjacent to every old vertex. -/
def join {k : ℕ} (H : SimpleGraph (Fin k)) : SimpleGraph (Fin k ⊕ Fin 2) where
  Adj
    | .inl a, .inl b => H.Adj a b
    | .inr i, .inr j => i ≠ j
    | .inl _, .inr _ => True
    | .inr _, .inl _ => True
  symm := ⟨fun x y h => by
    cases x <;> cases y <;> simp_all [H.adj_comm, eq_comm]⟩
  loopless := ⟨fun x h => by
    cases x <;> simp_all⟩

theorem join_no_four_regular {k : ℕ} (H : SimpleGraph (Fin k)) [DecidableRel H.Adj]
    (htri : H.CliqueFree 3)
    (hsparse : ∀ T : Finset (Fin k), 4 ≤ T.card →
      ((T ×ˢ T).filter (fun p => H.Adj p.1 p.2)).card ≤ 2 * (2 * T.card - 5)) :
    ¬ ∃ (S : Finset (Fin k ⊕ Fin 2)) (K : SimpleGraph (Fin k ⊕ Fin 2)) (_ : DecidableRel K.Adj),
        S.Nonempty ∧ K ≤ join H ∧ ∀ v ∈ S, (S.filter (fun w => K.Adj v w)).card = 4 := by
  rintro ⟨S, K, _, hS, hK, hdeg⟩
  classical
  set T := S.toLeft with hT
  set J := S.toRight with hJ
  -- degree splits into left and right neighbours
  have split : ∀ v, (S.filter (fun w => K.Adj v w)).card =
      (T.filter (fun b => K.Adj v (.inl b))).card + (J.filter (fun i => K.Adj v (.inr i))).card := by
    intro v
    rw [← card_toLeft_add_card_toRight (u := S.filter (fun w => K.Adj v w))]
    congr 1 <;> (congr 1; ext x; simp [hT, hJ])
  have hj : J.card ≤ 2 := by
    simpa using card_le_univ J
  have hSc : S.card = T.card + J.card := (card_toLeft_add_card_toRight).symm
  -- right-neighbour count of left vertices, double counted
  have dc : ∑ a ∈ T, (J.filter (fun i => K.Adj (.inl a) (.inr i))).card
      = ∑ i ∈ J, (T.filter (fun a => K.Adj (.inr i) (.inl a))).card := by
    simp only [card_filter]
    rw [sum_comm]
    refine sum_congr rfl fun i _ => sum_congr rfl fun a _ => ?_
    simp [K.adj_comm]
  have dcle : ∑ i ∈ J, (T.filter (fun a => K.Adj (.inr i) (.inl a))).card ≤ 4 * J.card := by
    calc _ ≤ ∑ _i ∈ J, 4 := by
          refine sum_le_sum fun i hi => ?_
          have := split (.inr i)
          rw [hdeg _ (by simpa [hJ] using hi)] at this
          omega
      _ = 4 * J.card := by rw [sum_const, smul_eq_mul, mul_comm]
  have sum4 : ∑ a ∈ T, ((T.filter (fun b => K.Adj (.inl a) (.inl b))).card
      + (J.filter (fun i => K.Adj (.inl a) (.inr i))).card) = 4 * T.card := by
    rw [mul_comm, ← smul_eq_mul, ← sum_const]
    refine sum_congr rfl fun a ha => ?_
    rw [← split, hdeg _ (by simpa [hT] using ha)]
  rw [sum_add_distrib] at sum4
  -- left-left K-pairs are H-pairs
  have llle : ∑ a ∈ T, (T.filter (fun b => K.Adj (.inl a) (.inl b))).card
      ≤ ((T ×ˢ T).filter (fun p => H.Adj p.1 p.2)).card := by
    calc _ = ((T ×ˢ T).filter (fun p => K.Adj (.inl p.1) (.inl p.2))).card := by
          rw [card_filter, sum_product]; simp only [card_filter]
      _ ≤ _ := card_le_card fun p hp => by
          simp only [mem_filter] at hp ⊢
          exact ⟨hp.1, hK hp.2⟩
  by_cases ht : 4 ≤ T.card
  · have := hsparse T ht
    omega
  · -- small case: |S| = 5 and the three left vertices form a triangle
    obtain ⟨v, hv⟩ := hS
    have hv5 : 5 ≤ S.card := by
      have hsub : S.filter (fun w => K.Adj v w) ⊆ S.erase v := fun w hw => by
        simp only [mem_filter] at hw
        exact mem_erase.2 ⟨fun h => K.loopless.irrefl v (h ▸ hw.2), hw.1⟩
      have := card_le_card hsub
      rw [hdeg v hv, card_erase_of_mem hv] at this
      omega
    have hT3 : T.card = 3 := by omega
    have hS5 : S.card = 5 := by omega
    have full : ∀ x ∈ S, ∀ y ∈ S, x ≠ y → K.Adj x y := by
      intro x hx y hy hxy
      have hsub : S.filter (fun w => K.Adj x w) ⊆ S.erase x := fun w hw => by
        simp only [mem_filter] at hw
        exact mem_erase.2 ⟨fun h => K.loopless.irrefl x (h ▸ hw.2), hw.1⟩
      have heq := eq_of_subset_of_card_le hsub (by rw [hdeg x hx, card_erase_of_mem hx]; omega)
      have : y ∈ S.erase x := mem_erase.2 ⟨fun h => hxy h.symm, hy⟩
      rw [← heq] at this
      exact (mem_filter.1 this).2
    apply htri T
    refine ⟨fun a ha b hb hab => ?_, hT3⟩
    have := full (.inl a) (by simpa [hT] using ha) (.inl b) (by simpa [hT] using hb)
      (fun h => hab (Sum.inl_injective h))
    exact hK this

end E585
