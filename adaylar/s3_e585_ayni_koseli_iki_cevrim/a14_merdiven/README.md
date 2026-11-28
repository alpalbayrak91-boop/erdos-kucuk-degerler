# a(14): certified vertex-extension ladder

Run on 28 Nov 2026 (Colab CPU, 8 cores, 10,798 s). `calistir.py` drives `yontem_c_colab.sh`, which grows level `L_n`
(all good graphs on n vertices with at least t_n edges, up to isomorphism) from `L_{n-1}` by adding a vertex, and
writes a certificate (a pair of edge-disjoint cycles on the same vertex set) for every rejected candidate.
`sertifika_dogrula.py` re-checks every certificate independently of the search. Thresholds
`t = 0,1,2,4,6,9,12,15,19,23,28,33,38,44` for n = 1..14.

| n | t | candidates | certificates (all valid) | classes kept | edge counts |
|---|---|---|---|---|---|
| 11 | 28 | 22,009,718 | 16,459,377 | 2,531,034 | 28..31 |
| 12 | 33 | 21,404,966 | 19,958,694 | 476,615 | 33..36 |
| 13 | 38 | 5,557,097 | 5,443,659 | 36,943 | 38 (36,779), 39 (164) |
| 14 | 44 | 88,395 | 88,382 | 3 | 44 (3) |

Result: no good graph on 14 vertices has 45 or more edges, and exactly three isomorphism classes reach 44
(`L14.g6`). Each of the three was also checked with `../dort_duzenli.py` (integer programming, shares no code with
the search): `four_regular_subgraph=0`, m = 44. With the averaging upper bound a(14) <= 45 this gives
**a(14) = 44**, provided the ladder thresholds are valid lower bounds for the vertex-deletion step (see the
derivation in the parent README). Independent review of that step is pending.

Files: `L14.g6` (the three extremal graphs), `L13.g6.gz` (36,943 classes), `yontem_c.log`, source.
