# Erdős problemleri — küçük değerler (AlpLab)

Bu depo, [erdosproblems.com](https://www.erdosproblems.com) problemlerinin
[google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures)
deposundaki Lean tanımlarına göre hesapladığımız küçük değerleri yayımlar. Her sayı kaba kuvvetle
(ya da belirtildiği yerde bilinen bir teoremle) üretildi; betikler `betikler/` altında ve tek başına
çalışır (yalnız Python standart kütüphanesi).

*English summary below.*

## Sonuçlar

| Problem | Dizi | Değerler | Durum | Yöntem |
| --- | --- | --- | --- | --- |
| [#600](https://www.erdosproblems.com/600) | e(n,2), n = 3..11 | 4, 4, 7, 7, 10, 13, 19, 19, 22 | Hesaplandı | Her kenarı tam bir üçgende olan graflar = kenar-ayrık üçgen paketleri (fazladan üçgen oluşturmayan); e(n,2) = 3·t_max(n) + 1. `e600_ucgen_paketleme.py` |
| #600 | t_max(n), n = 3..11 | 1, 1, 2, 2, 3, 4, 6, 6, 7 | Hesaplandı | Aynı betik |
| [#642](https://www.erdosproblems.com/642) | f(n), n = 0..7 | 0, 0, 1, 3, 6, 9, 11, 14 | Hesaplandı | Tüm graflar; her döngüde köşe sayısı > kiriş sayısı. `e642_kaba_kuvvet.py` |
| [#934](https://www.erdosproblems.com/934) | h₂(d) − 1, d = 1..12 | 1, 5, 10, 20, 29, 45, 58, 80, 97, 125, 146, 180 | Bilinen teorem | t = 2 hâli indüklenmiş 2K₂ içermeyen graflardır; kapalı form Chung–Gyárfás–Tuza–Trotter (1990). d ≤ 8 ayrıca ajan hesaplarıyla tutarlı. `e934_cgtt.py` |
| [#983](https://www.erdosproblems.com/983) | f(π(n)+1, n), n = 2..16 | 0, 0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4 | Hesaplandı | Tüm k-alt kümeler × tüm asal kümeleri. Lean tanımında 1 her S için sayılır, bu yüzden n = 2, 3 için değer 0. `e983_kaba_kuvvet.py` |

### Kısmi / açık

- **#709**: n = 2..6 için en küçük çarpanın k = 2 olduğu iddiasına karşı örnek bulunmadı
  (M ≤ 16, başlangıç < 400); k = 1 her n için bozuluyor (ör. A = {2, 3}, pencere {5, 6, 7}).
  Tarama periyodun tamamını kapsamadığı için bu bir ispat değil. `e709_karsi_ornek_arama.py`
- **#600, n = 12** hesaplanıyor.

### OEIS durumu

Diziler OEIS'in Ocak 2026 kesitinde (392.167 dizi) aranmış, eşleşme bulunmamıştır. Daha sonra
eklenen kayıtlar bu kesitte yok; OEIS'e gönderimden önce oeis.org'da son bir kontrol gerekir.
Gönderim taslakları: [`OEIS_TASLAKLARI.md`](OEIS_TASLAKLARI.md).

### Sınırlar

- Bunlar küçük n değerleridir; problemlerin asimptotik sorularına cevap değildir.
- #934 dizisi yeni bir matematik sonucu değil, bilinen bir teoremin değerleridir.
- Hata görürseniz issue açın; düzeltilmiş değer ve gerekçe bu dosyaya işlenir.

## English summary

Small values of several Erdős problems, computed by exhaustive search against the Lean definitions in
google-deepmind/formal-conjectures. #600: e(n,2) for n = 3..11. #642: f(n) for n = 0..7.
#983: f(π(n)+1, n) for n = 2..16 (note f = 0 for n = 2, 3 since 1 is S-smooth for every S).
#934 (t = 2) follows the Chung–Gyárfás–Tuza–Trotter closed form and is listed for completeness.
None of these sequences was found in the January 2026 OEIS snapshot. Scripts are self-contained.

Hazırlayan: AlpLab (Alp Albayrak) — hesaplar Claude ve Gemini ajanlarıyla, denetim Claude ile.
