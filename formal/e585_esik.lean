/-
Erdős Problem 585 — threshold step of the a(14) vertex-addition ladder (adaylar/s3_e585_ayni_koseli_iki_cevrim/a14_merdiven).

The ladder only extends graphs on n - 1 vertices with at least t_{n-1} edges; this is sound because a good graph on
n vertices with e edges has a vertex of degree at most floor(2e/n), whose deletion leaves at least e - floor(2e/n)
edges. `thr_mono` and `step` show that e - floor(2e/n) is monotone in e, and `table_check` checks the thirteen
threshold inequalities t_{n-1} <= t_n - floor(2 t_n / n) for n = 2..14 used by the ladder.

Provenance: proof written by Kimi K3.1 Pro through Open Math OS (AlpLab Formal Math team, 28 Nov 2026); the only
edit is the removal of the obsolete line `import Mathlib.Tactic.Omega` (omega is a core tactic).
Checked: `lake env lean --trust=0 formal/e585_esik.lean`, Lean 4.37.0-rc1, Mathlib 6ebcce37, exit code 0;
axioms: thr_mono [propext, Classical.choice, Quot.sound], table_check [propext, Classical.choice],
step [propext, Classical.choice, Quot.sound].
-/
import Mathlib.Data.Nat.Basic
import Mathlib.Tactic.IntervalCases

theorem thr_mono (n e : Nat) (hn : 2 <= n) : e - 2 * e / n <= (e + 1) - 2 * (e + 1) / n := by
  have hn0 : 0 < n := by omega
  have hdiv : 2 * (e + 1) / n <= 2 * e / n + 1 := by
    calc
      2 * (e + 1) / n = (2 * e + 2) / n := by
        have he : 2 * (e + 1) = 2 * e + 2 := by omega
        rw [he]
      _ <= (2 * e + n) / n := by
        apply Nat.div_le_div_right
        omega
      _ = 2 * e / n + 1 := Nat.add_div_right _ hn0
  have hle : 2 * e / n <= 2 * (e + 1) / n := by
    apply Nat.div_le_div_right
    omega
  omega

def t : List Nat := [0, 1, 2, 4, 6, 9, 12, 15, 19, 23, 28, 33, 38, 44]

theorem table_check (n : Nat) (hn : 2 <= n) (hn14 : n <= 14) :
    t.getD (n - 2) 0 <= t.getD (n - 1) 0 - 2 * t.getD (n - 1) 0 / n := by
  interval_cases n <;> decide

theorem step (n e t : Nat) (hn : 2 <= n) (h : t <= e) : t - 2 * t / n <= e - 2 * e / n := by
  induction e, h using Nat.le_induction with
  | base => exact Nat.le_refl _
  | succ e h ih =>
      exact ih.trans (thr_mono n e hn)

-- VERIFIED_SUMMARY:
-- Proved thr_mono and step, and checked all thirteen table inequalities for n = 2 through 14 by decide.

#print axioms thr_mono
#print axioms table_check
#print axioms step
