# Erdős problemleri — küçük değerler (AlpLab)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24457110.svg)](https://doi.org/10.5281/zenodo.24457110)

Bu depo, [erdosproblems.com](https://www.erdosproblems.com) problemlerinin
[google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures)
deposundaki Lean tanımlarına göre hesapladığımız küçük değerleri yayımlar. Her sayı kaba kuvvetle
(ya da belirtildiği yerde bilinen bir teoremle) üretildi; betikler `betikler/` altında ve tek başına
çalışır (yalnız Python standart kütüphanesi).

*English summary below.*

## Sonuçlar

| Problem | Dizi | Değerler | Durum | Yöntem |
| --- | --- | --- | --- | --- |
| [#600](https://www.erdosproblems.com/600) | e(n,2), n = 3..14 | 4, 4, 7, 7, 10, 13, 19, 19, 22, 28, 31, 37 | Hesaplandı | Ayrıntı, kanıt ve betikler: aşağıdaki «Erdős #600» bölümü. `e600/cpsat_T.py`, `e600/THEORY.md`, `betikler/e600_ucgen_paketleme.py` |
| #600 | T(n), n = 3..14 | 1, 1, 2, 2, 3, 4, 6, 6, 7, 9, 10, 12 | Hesaplandı | Aynı bölüm (`e600/results_cpsat.txt`, `e600/results_cpsat_11plus.txt`) |
| [#642](https://www.erdosproblems.com/642) | f(n), n = 0..7 | 0, 0, 1, 3, 6, 9, 11, 14 | Hesaplandı | Tüm graflar; her döngüde köşe sayısı > kiriş sayısı. `e642_kaba_kuvvet.py` |
| [#934](https://www.erdosproblems.com/934) | h₂(d) − 1, d = 1..12 | 1, 5, 10, 20, 29, 45, 58, 80, 97, 125, 146, 180 | Bilinen teorem | t = 2 hâli indüklenmiş 2K₂ içermeyen graflardır; kapalı form Chung–Gyárfás–Tuza–Trotter (1990). d ≤ 8 ayrıca ajan hesaplarıyla tutarlı. `e934_cgtt.py` |
| [#983](https://www.erdosproblems.com/983) | f(π(n)+1, n), n = 2..16 | 0, 0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4 | Hesaplandı | Tüm k-alt kümeler × tüm asal kümeleri. Lean tanımında 1 her S için sayılır, bu yüzden n = 2, 3 için değer 0. `e983_kaba_kuvvet.py` |

### Kısmi / açık

- **#709**: n = 2..6 için en küçük çarpanın k = 2 olduğu iddiasına karşı örnek bulunmadı
  (M ≤ 16, başlangıç < 400); k = 1 her n için bozuluyor (ör. A = {2, 3}, pencere {5, 6, 7}).
  Tarama periyodun tamamını kapsamadığı için bu bir ispat değil. `e709_karsi_ornek_arama.py`
- **#600**: n = 3..14 için tamam. Eski «n = 12 hesaplanıyor» notu kalktı; değerler ve kanıt aşağıdaki «Erdős #600 — e(n,2), n = 3..14» bölümünde.

### OEIS durumu

#600 için T(n), 3T(n) ve e(n,2) oeis.org üzerinde 22 Kasım 2026'da arandı, eşleşme yok
(aşağıdaki bölüm). Diğer diziler OEIS'in Ocak 2026 kesitinde (392.167 dizi) aranmış,
eşleşme bulunmamıştır. Daha sonra
eklenen kayıtlar bu kesitte yok; OEIS'e gönderimden önce oeis.org'da son bir kontrol gerekir.
Gönderim taslakları: [`OEIS_TASLAKLARI.md`](OEIS_TASLAKLARI.md).

### Sınırlar

- Bunlar küçük n değerleridir; problemlerin asimptotik sorularına cevap değildir.
- #934 dizisi yeni bir matematik sonucu değil, bilinen bir teoremin değerleridir.
- Hata görürseniz issue açın; düzeltilmiş değer ve gerekçe bu dosyaya işlenir.

## English summary

Small values of several Erdős problems, computed by exhaustive search against the Lean definitions in
google-deepmind/formal-conjectures. #600: e(n,2) for n = 3..14 (section below; scripts in `e600/`). #642: f(n) for n = 0..7.
#983: f(π(n)+1, n) for n = 2..16 (note f = 0 for n = 2, 3 since 1 is S-smooth for every S).
#934 (t = 2) follows the Chung–Gyárfás–Tuza–Trotter closed form and is listed for completeness.
#600 (T(n), 3T(n), e(n,2)) had no match on oeis.org (searched 22 Nov 2026). The other sequences were not found in the January 2026 OEIS snapshot. Scripts are self-contained.

Hazırlayan: AlpLab (Alp Albayrak) — hesaplar Claude ve Gemini ajanlarıyla, denetim Claude ile.

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

**Yapay zekâ beyanı.** Hesaplar, betikler ve metinler yapay zekâ ajanlarının yardımıyla üretildi; sorumluluğu Alp Albayrak'a aittir.
