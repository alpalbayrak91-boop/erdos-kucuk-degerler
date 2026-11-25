# Erdős problemleri — küçük değerler (AlpLab)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24457110.svg)](https://doi.org/10.5281/zenodo.24457110)

Bu depo, [erdosproblems.com](https://www.erdosproblems.com) problemlerinin
[google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures)
deposundaki Lean tanımlarına göre hesapladığımız küçük değerleri, açık tanık grafları/kümeleri ve
doğrulama betiklerini yayımlar (`v1.1.0`). Betikler `betikler/`, `e600/`, `e642/`, `e983/`,
`e151_audit/` ve `formal/` altındadır.

*English summary below.*

## Sonuçlar (`v1.1.0`)

| Problem | Dizi | Değerler | Durum | Yöntem ve Dizin |
| --- | --- | --- | --- | --- |
| [#600](https://www.erdosproblems.com/600) | e(n,2), n = 3..14 | 4, 4, 7, 7, 10, 13, 19, 19, 22, 28, 31, 37 | Hesaplandı | CP-SAT + analitik üst sınır. `e600/cpsat_T.py`, `e600/THEORY.md`, `betikler/e600_ucgen_paketleme.py` |
| #600 | T(n), n = 3..14 | 1, 1, 2, 2, 3, 4, 6, 6, 7, 9, 10, 12 | Hesaplandı | `e600/results_cpsat.txt`, `e600/results_cpsat_11plus.txt` |
| [#642](https://www.erdosproblems.com/642) | f(n), n = 0..9 | 0, 0, 1, 3, 6, 9, 11, 14, 17, 20 | Hesaplandı | Kanonik graf sayımı (C) + Python dal-sınır + açık tanıklar; genel $f(n) \ge 3n - 7$ ($n \ge 3$) alt sınırı. `e642/e642_exact.c`, `e642/verify_e642.py`, `e642/THEORY.md`, `betikler/e642_kaba_kuvvet.py` |
| [#934](https://www.erdosproblems.com/934) | h₂(d) − 1, d = 1..12 | 1, 5, 10, 20, 29, 45, 58, 80, 97, 125, 146, 180 | Bilinen teorem | t = 2 hâli indüklenmiş 2K₂ içermeyen graflardır; kapalı form Chung–Gyárfás–Tuza–Trotter (1990). `betikler/e934_cgtt.py` |
| [#983](https://www.erdosproblems.com/983) | f(π(n)+1, n), n = 2..46 | 0, 0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4(×7), 5(×13), 6(×12) | Hesaplandı | Z3 CEGAR (`n = 2..46`, hem $\|S\| \le r$ hem $\|S\| = r$ tanımlarında özdeş) + kaba kuvvet çapraz kontrolü (`n = 2..16`). `e983/e983_exact_z3.py`, `e983/e983_exact_46.json`, `e983/THEORY.md`, `betikler/e983_kaba_kuvvet.py` |
| Denetim (OEIS `A032766` vs `A380408`; #151'den ayrım) | $\mathrm{ex}(n, \{C_{2k}\})$, n = 1..8 | 0, 1, 3, 4, 6, 7, 9, 10 (`⌊3(n−1)/2⌋`) | Bilinen teorem + Lean 4 kanıtı | Çift döngü içermeyen grafların ekstremal kenar sayısı = OEIS `A032766`; `A380408` dizisinden indis 24'te (`37 ≠ 36`) ayrılır ve Erdős–Gallai–Tuza klik kesen sanısından (#151) farklı bir problemdir. `formal/Erdos151EvenCycleA032766Audit.lean`, `e151_audit/THEORY.md` |

### Kısmi / açık

- **#709**: n = 2..6 için en küçük çarpanın k = 2 olduğu iddiasına karşı örnek bulunmadı
  (M ≤ 16, başlangıç < 400); k = 1 her n için bozuluyor (ör. A = {2, 3}, pencere {5, 6, 7}).
  Tarama periyodun tamamını kapsamadığı için bu bir ispat değil. `betikler/e709_karsi_ornek_arama.py`
- **#600**: n = 3..14 için tamam. Eski «n = 12 hesaplanıyor» notu kalktı; değerler ve kanıt aşağıdaki «Erdős #600 — e(n,2), n = 3..14» bölümünde.

### OEIS durumu

#600 için T(n), 3T(n) ve e(n,2) oeis.org üzerinde 22 Kasım 2026'da arandı, eşleşme yok
(aşağıdaki bölüm). Diğer diziler OEIS'in Ocak 2026 kesitinde (392.167 dizi) aranmış,
eşleşme bulunmamıştır. Çift döngüsüz grafların ekstremal kenar sayısı $\lfloor 3(n-1)/2 \rfloor$
ise OEIS'te zaten **`A032766`** olarak kayıtlıdır (`A380408` ile ilk 24 terimde çakışıp 25. terimde `37 ≠ 36` ile ayrılır; bkz. [`e151_audit/THEORY.md`](e151_audit/THEORY.md)).
Gönderim taslakları: [`OEIS_TASLAKLARI.md`](OEIS_TASLAKLARI.md).

### Sınırlar

- Bunlar küçük n değerleridir; problemlerin asimptotik sorularına cevap değildir.
- #934 dizisi ve çift döngüsüz graf sınırı ($\lfloor 3(n-1)/2 \rfloor$ = `A032766`) bilinen teoremlerin değerleridir; `e151_audit/` modülü Erdős #151 klik kesen sanısına çözüm iddiası taşımaz, yalnızca `A032766`/`A380408` önek çakışmasını ve problem ayrımını Lean 4 ile denetler.
- Hata görürseniz issue açın; düzeltilmiş değer ve gerekçe bu dosyaya işlenir.

## English summary (`v1.1.0`)

Exact small values, explicit combinatorial witnesses, and machine-checked audits for several Erdős problems, aligned with the Lean 4 definitions in `google-deepmind/formal-conjectures`:

- **#600** (`e600/`): $e(n,2) = 3T(n)+1$ for $n = 3 \dots 14$ (`4, 4, 7, 7, 10, 13, 19, 19, 22, 28, 31, 37`), certified by CP-SAT and an elementary upper bound at $n = 14$.
- **#642** (`e642/`): $f(n)$ for $n = 0 \dots 9$ (`0, 0, 1, 3, 6, 9, 11, 14, 17, 20`; for $n = 2 \dots 9$: `1, 3, 6, 9, 11, 14, 17, 20`), certified by canonical unlabeled graph enumeration in C (`e642/e642_exact.c`), an independent Python branch-and-bound solver up to $n = 8$ (`e642/verify_e642.py`), explicit optimal graph witnesses (`e642/witnesses_n0_to_9.json`), and a general construction $K_{3,n-3} \cup P_3$ proving $f(n) \ge 3n - 7$ for all $n \ge 3$ (`e642/THEORY.md`).
- **#983** (`e983/`): $f(\pi(n)+1, n)$ for $n = 2 \dots 46$ via Z3 CEGAR (`e983/e983_exact_z3.py`, `e983/e983_exact_46.json`), verifying exact agreement between $|S| \le r$ and $|S| = r$ across $2 \le n \le 46$ and cross-checked against brute force on $n = 2 \dots 16$.
- **#934** (`betikler/e934_cgtt.py`): $t = 2$ closed form of Chung–Gyárfás–Tuza–Trotter (1990), listed for completeness.
- **Even-Cycle-Free Audit (`e151_audit/`, `formal/Erdos151EvenCycleA032766Audit.lean`)**: Standalone Lean 4 (`lean --trust=0`, `0 sorry`) and Python audit of extremal edge counts of even-cycle-free graphs $\mathrm{ex}(n, \{C_4, C_6, \dots\}) = \lfloor 3(n-1)/2 \rfloor$ (`n = 1..8 -> 0, 1, 3, 4, 6, 7, 9, 10` = OEIS `A032766`), proving that the 24-term prefix match OEIS `A380408` diverges at index 24 (`37 != 36`) and explicitly distinguishing this classical extremal cycle sequence from the Erdős–Gallai–Tuza clique transversal conjecture (Erdős #151).

Run the full verification test suite with:
```bash
pytest -v tests/test_v110_verification.py
```

Hazırlayan: AlpLab (Alp Albayrak) — hesaplar Claude ve Gemini ajanlarıyla, bağımsız çözücü ve Lean 4 denetimi ile.

---

## Erdős #600 — e(n,2), n = 3..14

**Definition** ([erdosproblems.com/600](https://www.erdosproblems.com/600)). e(n,r) is the least m such that every graph on n vertices with at least m edges, each edge in at least one triangle, has an edge in at least r triangles. Isolated vertices are allowed. For r = 2 the extremal graphs are *locally linear* (every edge in exactly one triangle), so e(n,2) = 3·T(n) + 1, where T(n) is the maximum number of triangles in such a graph (equivalently: the largest linear, triangle-free triple system on n points — the Ruzsa–Szemerédi (6,3) setting).

| n | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T(n) | 1 | 1 | 2 | 2 | 3 | 4 | 6 | 6 | 7 | 9 | 10 | 12 |
| e(n,2) | 4 | 4 | 7 | 7 | 10 | 13 | 19 | 19 | 22 | 28 | 31 | 37 |

**How each value is certified**
- n ≤ 9: exhaustive search in pure Python (`betikler/e600_ucgen_paketleme.py`) and an independent CP-SAT model.
- n = 10..13: CP-SAT (OR-tools) proved optimality (`e600/cpsat_T.py`); every witness graph is re-checked (its triangles are exactly the chosen triples).
- n = 14: CP-SAT found a witness with 12 triangles; optimality follows from the elementary bound T(n) ≤ ⌊n·⌊(n+3)/2⌋/9⌋ (proof in `e600/THEORY.md`), which equals 12 at n = 14.
- n = 3..10 agree with the independent table in the [Erdős Problem a Day report #600](https://erdosproblemaday.com/report/600) (July 2026). n = 11..14 are new here.
- OEIS: draft [A400028](https://oeis.org/draft/A400028), status: submitted for editor review. No match for T(n), 3T(n) or e(n,2) on oeis.org when searched on 22 Nov 2026.

**Method and AI disclosure.** The computations, scripts and texts were produced with the help of AI agents (Claude, Gemini, Grok Bot); Alp Albayrak is responsible for the content.

---

## Erdős #600 — e(n,2), n = 3..14 (Türkçe)

**Tanım.** e(n,r): n köşeli, her kenarı en az bir üçgende olan ve en az m kenarı olan her grafta bir kenarın en az r üçgende bulunmasını zorunlu kılan en küçük m. Boşta köşeye izin var. r = 2 için en kalabalık graflarda her kenar tam bir üçgendedir; bu yüzden e(n,2) = 3·T(n) + 1, T(n) bu graflardaki en fazla üçgen sayısı.

(Tablo yukarıdakiyle aynı.)

**Nasıl doğrulandı:** n ≤ 9 kaba kuvvet ve ayrı bir CP-SAT modeli; n = 10–13 CP-SAT en iyilik kanıtı; n = 14 için 12 üçgenli örnek + basit üst sınır T(n) ≤ ⌊n·⌊(n+3)/2⌋/9⌋ = 12. n = 3–10 değerleri Temmuz 2026 tarihli bağımsız raporla aynı; n = 11–14 burada ilk kez veriliyor. OEIS taslağı [A400028](https://oeis.org/draft/A400028), durum: editör incelemesine gönderildi (submitted for editor review). 22 Kasım 2026 aramasında eşleşme yoktu.

---

## Erdős #642 — f(n), n = 0..9

Every simple cycle $C$ in an $n$-vertex simple graph must satisfy $\text{chords}(C) < |V(C)|$ (`Erdos642.maxEdges` in `formal-conjectures`). Full details, C canonical-enumeration solver, Python verifier, and proof of $f(n) \ge 3n - 7$ ($n \ge 3$) via $K_{3,n-3} \cup P_3$ are in [`e642/THEORY.md`](e642/THEORY.md).

| n | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| f(n) | 0 | 0 | 1 | 3 | 6 | 9 | 11 | 14 | 17 | 20 |

---

## Erdős #983 — f(π(n)+1, n), n = 2..46

Exact prime-covering thresholds $f(\pi(n)+1, n)$ (`Erdos983.f` in `formal-conjectures`) computed via Z3 CEGAR (`e983/e983_exact_z3.py`) with explicit lower-bound subsets $A \subseteq \{1, \dots, n\}$ in [`e983/e983_exact_46.json`](e983/e983_exact_46.json) and theory notes in [`e983/THEORY.md`](e983/THEORY.md):

- `n = 2..3`: `0, 0`
- `n = 4..5`: `1, 1`
- `n = 6..9`: `2, 2, 2, 2`
- `n = 10..14`: `3, 3, 3, 3, 3`
- `n = 15..21`: `4, 4, 4, 4, 4, 4, 4`
- `n = 22..34`: `5` (13 consecutive values; attains $2\pi(\sqrt{n}) + 1 = 5$ at $n = 22, 23, 24$)
- `n = 35..46`: `6` (12 consecutive values)

---

## Even-Cycle-Free Audit (`A032766` vs `A380408`) & Disambiguation from Erdős #151

[`formal/Erdos151EvenCycleA032766Audit.lean`](formal/Erdos151EvenCycleA032766Audit.lean) and [`e151_audit/THEORY.md`](e151_audit/THEORY.md) formally verify that even-cycle-free $n$-vertex simple graphs have maximum edge count $\lfloor 3(n-1)/2 \rfloor$ (`0, 1, 3, 4, 6, 7, 9, 10` for $n = 1 \dots 8$), prove exact bijection with OEIS `A032766`, prove that OEIS `A380408` diverges from `A032766` at 0-based index 24 (`37 != 36`), and explicitly separate this extremal cycle formula from the open Erdős–Gallai–Tuza clique transversal conjecture ([Erdős #151](https://www.erdosproblems.com/151)).

**Yapay zekâ beyanı.** Hesaplar, betikler ve metinler yapay zekâ ajanlarının yardımıyla üretildi; sorumluluğu Alp Albayrak'a aittir.
