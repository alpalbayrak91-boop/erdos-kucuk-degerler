# OEIS gönderim taslakları

> Superseded for #600 by [`e600/THEORY.md`](e600/THEORY.md) (values up to n=14) and OEIS draft [A400028](https://oeis.org/draft/A400028).

OEIS'e gönderim, kayıtlı bir OEIS hesabıyla (oeis.org/Submit.html) elle yapılır. Aşağıdaki metinler
oraya yapıştırılmak için hazır. Göndermeden önce her diziyi oeis.org'da son kez arayın: buradaki kontrol
Ocak 2026 kesitine karşı yapıldı.

---

## 1. Erdős #642

```
%N Maximum number of edges in a simple graph on n vertices in which every cycle has more vertices than chords.
%S 0,0,1,3,6,9,11,14
%C Erdős Problem #642 (Hamburger and Szegedy) asks whether a(n) = O(n). Chen, Erdős and Staton proved a(n) = O(n^(3/2)); Draganić, Methuku, Munhá Correia and Sudakov improved this to O(n (log n)^8).
%C A chord of a cycle is an edge between two vertices of the cycle that is not an edge of the cycle.
%e a(4) = 6: in K_4 every triangle has 0 chords and every 4-cycle has 2 chords < 4 vertices, so K_4 qualifies.
%o (Python) # exhaustive search, see https://github.com/alpalbayrak91-boop/erdos-kucuk-degerler/blob/main/betikler/e642_kaba_kuvvet.py
%K nonn,more
%O 0,4
```

## 2. Erdős #600, r = 2

```
%N e(n,2): least e such that every graph on n vertices with at least e edges, each edge in at least one triangle, has an edge in at least 2 triangles.
%S 4,4,7,7,10,13,19,19,22
%C Erdős Problem #600. A graph in which every edge lies in exactly one triangle has 3t edges, where t is its number of triangles, so e(n,2) = 3*t(n) + 1 with t(n) the maximum number of edge-disjoint triangles on n vertices whose union contains no further triangle (Ruzsa–Szemerédi (6,3)-type configurations).
%C Ruzsa and Szemerédi proved e(n,r) = o(n^2) for fixed r.
%o (Python) # see betikler/e600_ucgen_paketleme.py in https://github.com/alpalbayrak91-boop/erdos-kucuk-degerler
%K nonn,more
%O 3,1
```

İsteğe bağlı eş dizi: t(n), n = 3..11 → 1,1,2,2,3,4,6,6,7.

## 3. Erdős #983

```
%N a(n) = f(pi(n)+1, n), where f(k,n) is the least r such that every k-subset A of {1..n} contains more than r elements whose prime factors all lie in some set of r primes.
%S 0,0,1,1,2,2,2,2,3,3,3,3,3,4,4
%C Erdős Problem #983 (Erdős and Straus) asks whether 2*pi(sqrt(n)) - a(n) -> infinity; Liam Price and GPT-5.5 Pro showed on the erdosproblems.com forum that a(n) = 2*pi(sqrt(n)) + 1 for infinitely many n, so the answer is no.
%C The number 1 has no prime factors and is counted for every set of primes, so a(2) = a(3) = 0.
%o (Python) # see betikler/e983_kaba_kuvvet.py in https://github.com/alpalbayrak91-boop/erdos-kucuk-degerler
%K nonn,more
%O 2,5
```

## 4. Erdős #934, t = 2 (isteğe bağlı)

```
%N Maximum number of edges in a graph with maximum degree at most n containing no induced 2K_2.
%S 1,5,10,20,29,45,58,80,97,125,146,180
%F a(n) = 5n^2/4 for even n, (5n^2 - 2n + 1)/4 for odd n (Chung, Gyárfás, Tuza, Trotter, 1990).
%C Equals h_2(n) - 1 in Erdős Problem #934.
%K nonn,easy
%O 1,2
```

Not: #934 bilinen bir kapalı formdur; gönderim değeri yalnız OEIS'te eksik olmasıdır.
