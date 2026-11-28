/-
Erdős problem 585, cubic family: arithmetic core of Lemma 1 of
adaylar/s3_e585_ayni_koseli_iki_cevrim/kubik_kaniti.md (core Lean 4, no Mathlib).

sayma1: Case 3b.  From (2) t1 + t2w + d(w) = 4, (1) d(w) + t1 + 2 t2w + 2 t2b + D_B = 8 - 2 e12,
        |S_B| <= 2 t1 + t2w + 2 t2b + D_B and |Q| <= |S_B| + t2w, conclude |Q| <= 12.
sayma2: Case 2.   From 4 |S_B| = 2 e(S_B) + 2 |S_A|, 2 e(S_B) <= 3 |S_B| and |S_A| <= 4, conclude |S_B| <= 8.
sayma3: Case 3a.  From e(S_B) = 2 |S_B| - 4 + e12 and 2 e(S_B) <= 3 |S_B|, conclude |S_B| <= 8.
Only the arithmetic is formalized here, not the graph-theoretic steps that produce these relations.
-/


theorem sayma1 (t1 t2w t2b dw e12 DB s Q : Nat)
    (h2 : t1 + t2w + dw = 4) (he : e12 ≤ 1)
    (h1 : dw + t1 + 2*t2w + 2*t2b + DB + 2*e12 = 8)
    (hs : s ≤ 2*t1 + t2w + 2*t2b + DB) (hq : Q ≤ s + t2w) : Q ≤ 12 := by omega

theorem sayma2 (s e t : Nat) (h1 : 2*e ≤ 3*s) (h2 : 4*s = 2*e + 2*t) (h3 : t ≤ 4) : s ≤ 8 := by omega

theorem sayma3 (s e e12 : Nat) (h1 : 2*e ≤ 3*s) (h2 : e12 ≤ 1) (h3 : e + 4 = 2*s + e12) : s ≤ 8 := by omega

#print axioms sayma1
#print axioms sayma2
#print axioms sayma3
