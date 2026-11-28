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
(`L14.g6`). So **a(14) = 44**. (The ladder adds every neighbourhood that reaches the threshold, with no upper limit
on the number of edges, so the averaging bound a(14) <= 45 is not needed.) Each of the three graphs was also checked
with `../dort_duzenli.py` (integer programming, shares no code with the search): `four_regular_subgraph=0`, m = 44.

The thresholds are valid: if G is good on n vertices with e >= t_n edges and v has minimum degree, then G - v is good
with at least e - floor(2e/n) >= t_n - floor(2 t_n / n) >= t_{n-1} edges (the last inequality holds, with equality,
for every n = 2..14). Details and the review of the run are in the parent README, section "a(14) = 44".

Review (`hakem.log`, 28 Nov 2026, on another machine, from the level files): the candidate counts of
`e585 extend t_n -a` were recomputed for every n = 2..14 and equal the log; level 14 was run again in one process with
exit statuses checked and gave the same 3 classes; every vertex-deleted subgraph with at least t_{n-1} edges of a
graph in L_14, L_13, L_12 is in the level below (36, 333,258 and 3,932,147 graphs, none missing). The run script
itself does not check the exit status of its parallel parts; these checks were made because of that.

Files: `L14.g6` (the three extremal graphs), `L13.g6.gz` (36,943 classes), `yontem_c.log`, `hakem.log`, source.
