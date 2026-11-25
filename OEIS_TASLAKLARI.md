# OEIS Gönderim Durumu ve Düzeltilmiş Taslaklar (25 Kasım 2026)

OEIS Style Sheet kuralı uyarınca `LINKS` satırları **yazar soyadına göre alfabetik** (`Albayrak` -> `Bloom` -> `Wikipedia`) sıralanmıştır. Canlı durumlar `alplab_dis_basvuru_ve_oeis_bekcisi.py` tarafından otomatik izlenir.

---

## Canlı OEIS Taslak Durumu (25 Kasım 2026)

| Dizi | Erdős Problemi | Durum | Editör Yorumu & Yapılacak İşlem |
|---|---|---|---|
| **[A400028](https://oeis.org/draft/A400028)** | **#600** ($r=2$, $T(n)$, $n=0..14$) | **`proposed`** (İncelemede) | Jason Yuen (24 Kas) `Szemerédi` aksanlarını düzeltti ve `proposed` kuyruğuna aldı. **Dokunma — yayına hazır.** |
| **[A400041](https://oeis.org/draft/A400041)** | **#642** (Hamburger–Szegedy) | **`editing`** (45 sn Düzeltme) | Sean A. Irvine (24 Kas): `"Links needs to be alphabetical"`. Aşağıdaki `LINKS` bloğunu yapıştırıp `Submit changes for review` tıkla. |
| **[A400042](https://oeis.org/draft/A400042)** | **#983** (Erdős–Straus) | **`editing`** (45 sn Düzeltme) | Sean A. Irvine (24 Kas): `"Links needs to be alphabetical"`. Aşağıdaki `LINKS` bloğunu yapıştırıp `Submit changes for review` tıkla. |

---

## 1. [A400041](https://oeis.org/draft/A400041) — Erdős #642 (Kopyala-Yapıştır Düzeltmesi)

**`LINKS` kutusundaki mevcut 3 satırı silip tam olarak şunu yapıştır (`Albayrak` -> `Bloom` soyadı alfabetik):**

```html
Alp Albayrak, <a href="https://doi.org/10.5281/zenodo.24457110">Data and scripts (Zenodo)</a>.
Alp Albayrak, <a href="https://github.com/alpalbayrak91-boop/erdos-kucuk-degerler/blob/main/betikler/e642_kaba_kuvvet.py">Python program for Problem 642</a>.
Thomas Bloom, <a href="https://www.erdosproblems.com/642">Problem 642</a>, Erdős Problems.
```

*(İsteğe bağlı: `v1.1.0` C kanonik arama ile kanıtlanan `a(8)=17, a(9)=20` terimlerini şimdi değil `A400041` yayına alındıktan hemen sonra revizyonla veya istersen `DATA` satırını `0, 0, 1, 3, 6, 9, 11, 14, 17, 20` yaparak ekleyebilirsin; en hızlı onay için yalnız `LINKS` düzeltip `Submit` önerilir.)*

---

## 2. [A400042](https://oeis.org/draft/A400042) — Erdős #983 (Kopyala-Yapıştır Düzeltmesi)

**`LINKS` kutusundaki mevcut 3 satırı silip tam olarak şunu yapıştır (`Albayrak` -> `Bloom` soyadı alfabetik):**

```html
Alp Albayrak, <a href="https://doi.org/10.5281/zenodo.24457110">Data and scripts (Zenodo)</a>.
Alp Albayrak, <a href="https://github.com/alpalbayrak91-boop/erdos-kucuk-degerler/blob/main/betikler/e983_kaba_kuvvet.py">Python program for Problem 983</a>.
Thomas Bloom, <a href="https://www.erdosproblems.com/983">Problem 983</a>, Erdős Problems.
```

*(Not: `e983/e983_exact_46.json` içindeki `n=2..46` Z3 CEGAR değerleri `A400042` onaylanır onaylanmaz `b400042.txt` b-file veya `DATA` genişletmesi olarak hazır bekliyor.)*

---

## 3. [A400028](https://oeis.org/draft/A400028) — Erdős #600 ($r = 2$, Onay Kuyruğunda)

- `DATA` ($n = 0..14$): `0, 0, 0, 1, 1, 2, 2, 3, 4, 6, 6, 7, 9, 10, 12` (`OFFSET 0,6`)
- `LINKS` zaten `Alp Albayrak` -> `Thomas Bloom` -> `Wikipedia` alfabetik sırasında; editör Jason Yuen inceleyip `proposed` statüsüne taşıdı.

---

## 4. Yeni Aday Diziler (Sonraki OEIS Gönderim Dalgası — `erdos-kucuk-degerler v1.2.0`)

### 4A. Erdős #23 — Üçgensiz Çizgelerde İki-Parçalı Yapma Engellenmişliği $b_\Delta(N)$
```
%N Maximum over all triangle-free graphs G on n vertices of |E(G)| - MaxCut(G) (minimum number of edges whose deletion makes G bipartite).
%S 0,0,0,0,1,1,1,2,2,4
%C Erdős Problem #23 asks whether a(n) <= n^2/25 for all n, where equality holds at multiples of 5 via balanced blowups of C_5.
%C Note the jump from a(9) = 2 to a(10) = 4 achieved by the balanced blowup C_5[I_2, I_2, I_2, I_2, I_2] (20 edges, MaxCut = 16).
%H Alp Albayrak, <a href="https://github.com/alpalbayrak91-boop/erdos-kucuk-degerler">Code, witness graphs and Lean 4 proofs</a>.
%H Thomas Bloom, <a href="https://www.erdosproblems.com/23">Problem 23</a>, Erdős Problems.
%K nonn,more,hard
%O 1,8
```

### 4B. Erdős #934 ($t = 2$, İsteğe Bağlı Kapalı Form)
```
%N Maximum number of edges in a graph with maximum degree at most n containing no induced 2K_2.
%S 1,5,10,20,29,45,58,80,97,125,146,180
%F a(n) = 5*n^2/4 for even n, (5*n^2 - 2*n + 1)/4 for odd n (Chung, Gyárfás, Tuza, Trotter, 1990).
%C Equals h_2(n) - 1 in Erdős Problem #934.
%H Thomas Bloom, <a href="https://www.erdosproblems.com/934">Problem 934</a>, Erdős Problems.
%K nonn,easy
%O 1,2
```
