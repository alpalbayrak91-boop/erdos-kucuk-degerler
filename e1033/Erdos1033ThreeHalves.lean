/-
AlpLab (Gemini 4 Carbon, 2026-11-26): Erdos Problem #1033, variant `three_halves`.
Explicit Erdos-Laskar finite counterexample on n = 23 vertices:
  A = {0..8} independent (|A| = 9), B = {9..22} inducing a 7-edge perfect matching (|B| = 14),
  plus the complete bipartite graph between A and B.
  Total edges = 9 * 14 + 7 = 133, so 4 * |E| = 532 > 529 = 23^2.
  Vertex degrees: deg(v) = 14 for v in A, deg(v) = 10 for v in B.
  Since A is independent, every triangle hits at most 1 vertex in A and at least 2 in B,
  so its degree sum is <= 14 + 10 + 10 = 34 and 2 * sum_deg <= 68 < 69 = 3 * 23.
ZERO sorry, ZERO native_decide, ZERO custom axioms, ZERO chr(36).
-/
import Mathlib.Combinatorics.SimpleGraph.Clique
import Mathlib.Combinatorics.SimpleGraph.DegreeSum
import Mathlib.Combinatorics.SimpleGraph.Finite

open Finset

namespace AlpLab.Erdos1033

/-- Pure Nat adjacency predicate for the n = 23 Erdos-Laskar counterexample graph. -/
def adjNat23 (u v : ℕ) : Bool :=
  (u < 9 && 9 ≤ v) ||
  (9 ≤ u && v < 9) ||
  (9 ≤ u && 9 ≤ v && (u - 9) / 2 == (v - 9) / 2 && u != v)

theorem adjNat23_symm (u v : ℕ) : adjNat23 u v = adjNat23 v u := by
  dsimp only [adjNat23]
  by_cases hu : u < 9
  · have h9u : ¬ (9 ≤ u) := by omega
    by_cases hv : v < 9
    · have h9v : ¬ (9 ≤ v) := by omega
      simp [hu, hv, h9u, h9v]
    · have h9v : 9 ≤ v := by omega
      simp [hu, hv, h9v]
  · have h9u : 9 ≤ u := by omega
    by_cases hv : v < 9
    · have h9v : ¬ (9 ≤ v) := by omega
      simp [hu, hv, h9u, h9v]
    · have h9v : 9 ≤ v := by omega
      by_cases hdiv : (u - 9) / 2 = (v - 9) / 2
      · simp [hu, hv, h9u, h9v, hdiv, bne_comm]
      · have hdiv2 : (v - 9) / 2 ≠ (u - 9) / 2 := fun h => hdiv h.symm
        have hb1 : ((u - 9) / 2 == (v - 9) / 2) = false := beq_false_of_ne hdiv
        have hb2 : ((v - 9) / 2 == (u - 9) / 2) = false := beq_false_of_ne hdiv2
        simp [hu, hv, h9u, h9v, hb1, hb2]

theorem adjNat23_irrefl (v : ℕ) : adjNat23 v v = false := by
  dsimp only [adjNat23]
  by_cases hv : v < 9
  · have h9v : ¬ (9 ≤ v) := by omega
    simp [hv, h9v]
  · have h9v : 9 ≤ v := by omega
    simp [hv, h9v]

/-- The explicit 23-vertex Erdos-Laskar simple graph. -/
def G23 : SimpleGraph (Fin 23) where
  Adj u v := adjNat23 u.val v.val = true
  symm := ⟨fun u v h => by rwa [adjNat23_symm] at h⟩
  loopless := ⟨fun v h => by rw [adjNat23_irrefl] at h; cases h⟩

instance : DecidableRel G23.Adj := fun u v =>
  inferInstanceAs (Decidable (adjNat23 u.val v.val = true))

def degList23 (i : ℕ) : ℕ :=
  (List.range 23).countP (fun j => adjNat23 i j)

theorem sum_range_countP (n : ℕ) (p : ℕ → Bool) :
    (∑ j ∈ Finset.range n, if p j = true then 1 else 0) = (List.range n).countP p := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Finset.sum_range_succ, ih, List.range_succ, List.countP_append, List.countP_cons,
      List.countP_nil, Nat.zero_add]

theorem degList23_all_cert :
    (List.range 23).all (fun i => degList23 i == (if i < 9 then 14 else 10)) = true := by
  decide +kernel

theorem degList23_formula (i : ℕ) (hi : i < 23) :
    degList23 i = if i < 9 then 14 else 10 := by
  have h := degList23_all_cert
  rw [List.all_eq_true] at h
  exact beq_iff_eq.mp (h i (List.mem_range.mpr hi))

theorem G23_degree_eq (v : Fin 23) :
    G23.degree v = if v.val < 9 then 14 else 10 := by
  have hmem : G23.neighborFinset v = Finset.univ.filter (fun w : Fin 23 => adjNat23 v.val w.val = true) := by
    ext w
    simp only [SimpleGraph.mem_neighborFinset, Finset.mem_filter, Finset.mem_univ, true_and]
    rfl
  rw [← SimpleGraph.card_neighborFinset_eq_degree, hmem, Finset.card_filter]
  rw [Fin.sum_univ_eq_sum_range (fun j => if adjNat23 v.val j = true then 1 else 0) 23]
  rw [sum_range_countP]
  exact degList23_formula v.val v.isLt

theorem sum_deg23_range_cert :
    ((List.range 23).map (fun i => if i < 9 then (14 : ℕ) else 10)).sum = 266 := by
  decide +kernel

theorem sum_range_eq_list_map_sum (n : ℕ) (f : ℕ → ℕ) :
    (∑ i ∈ Finset.range n, f i) = ((List.range n).map f).sum := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Finset.sum_range_succ, ih, List.range_succ, List.map_append, List.sum_append,
      List.map_cons, List.map_nil, List.sum_cons, List.sum_nil, Nat.add_zero]

theorem G23_edge_count_gt : 23 ^ 2 < 4 * #G23.edgeFinset := by
  have htwice := G23.sum_degrees_eq_twice_card_edges
  have hsum : (∑ v : Fin 23, G23.degree v) = 266 := by
    simp_rw [G23_degree_eq]
    rw [Fin.sum_univ_eq_sum_range (fun i => if i < 9 then (14 : ℕ) else 10) 23]
    rw [sum_range_eq_list_map_sum]
    exact sum_deg23_range_cert
  omega

theorem G23_no_edge_within_A {u v : Fin 23} (hadj : G23.Adj u v)
    (hu : u.val < 9) : ¬ (v.val < 9) := by
  intro hv
  change adjNat23 u.val v.val = true at hadj
  dsimp only [adjNat23] at hadj
  have h1 : ¬ (9 ≤ v.val) := by omega
  have h2 : ¬ (9 ≤ u.val) := by omega
  simp [hu, hv, h1, h2] at hadj

/-- Same statement as `Erdos1033.erdos_1033.variants.three_halves` in google-deepmind/formal-conjectures. -/
theorem erdos_1033_variants_three_halves :
    ¬ ∀ n : ℕ, ∀ (G : SimpleGraph (Fin n)) [DecidableRel G.Adj], n ^ 2 < 4 * #G.edgeFinset →
      ∃ t, G.IsNClique 3 t ∧ 3 * n ≤ 2 * ∑ v ∈ t, G.degree v := by
  intro hall
  obtain ⟨t, ht_clique, ht_deg⟩ := hall 23 G23 G23_edge_count_gt
  obtain ⟨a, b, c, hab, hac, hbc, rfl⟩ := Finset.card_eq_three.mp ht_clique.card_eq
  have hab_adj : G23.Adj a b := ht_clique.isClique (by simp) (by simp) hab
  have hac_adj : G23.Adj a c := ht_clique.isClique (by simp) (by simp) hac
  have hbc_adj : G23.Adj b c := ht_clique.isClique (by simp) (by simp) hbc
  have hsum_split :
      (∑ v ∈ ({a, b, c} : Finset (Fin 23)), G23.degree v) =
        G23.degree a + G23.degree b + G23.degree c := by
    rw [Finset.sum_insert (by simp [hab, hac]), Finset.sum_insert (by simp [hbc]),
      Finset.sum_singleton]
    omega
  rw [hsum_split, G23_degree_eq a, G23_degree_eq b, G23_degree_eq c] at ht_deg
  by_cases ha : a.val < 9
  · have hb : ¬ (b.val < 9) := G23_no_edge_within_A hab_adj ha
    have hc : ¬ (c.val < 9) := G23_no_edge_within_A hac_adj ha
    simp only [ha, hb, hc, ↓reduceIte] at ht_deg
    omega
  · by_cases hb : b.val < 9
    · have hc : ¬ (c.val < 9) := G23_no_edge_within_A hbc_adj hb
      simp only [ha, hb, hc, ↓reduceIte] at ht_deg
      omega
    · by_cases hc : c.val < 9 <;> simp only [ha, hb, hc, ↓reduceIte] at ht_deg <;> omega

end AlpLab.Erdos1033
