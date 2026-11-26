# Independent verification (26 Nov 2026)

## A400041 (Erdős #642): a(8) = 17, a(9) = 20
`a400041_nauty_dogrula.py n m` enumerates all non-isomorphic graphs with n vertices and m edges
(`nauty-geng`) and checks the defining property (every cycle has more vertices than chords) by DFS,
independently of `e642/e642_exact.c`. The property is closed under edge deletion, so
"no valid graph with m+1 edges" proves a(n) <= m.

| n | m | graphs | valid |
|---|---|---|---|
| 7 | 14 | 65 | 1 |
| 7 | 15 | 41 | 0 |
| 8 | 17 | 980 | 1 |
| 8 | 18 | 663 | 0 |
| 9 | 20 | 27987 | 1 |
| 9 | 21 | 21933 | 0 |

### a(10) = 23, a(11) = 26 (vertex extension, `a400041_kose_buyutme.py`)
The property is also closed under vertex deletion. A valid graph with n vertices and m edges has a vertex of
degree d <= floor(2m/n); deleting it leaves a valid (n-1)-vertex graph with m-d edges. Starting from all valid
9-vertex graphs (m=19: 12 graphs, m=20: 1 graph, from `nauty-geng`):
- no valid 10-vertex graph with 24 edges; valid 10-vertex graphs with 23 edges: exactly 1 up to isomorphism (`nauty-labelg`);
- no valid 11-vertex graph with 27 edges;
- witnesses K_{3,n-3} plus a path P_3 on the 3-side: 23 edges (n=10) and 26 edges (n=11), both valid.
Independently confirmed by a separate exhaustive search (min-degree vertex deletion). Run time ~13 s.

## A400042 (Erdős #983): terms for n = 2..28
`betikler/e983_kaba_kuvvet.py 28` (exhaustive search) agrees term by term with the Z3 computation in
`e983/e983_exact_46.json` for n = 2..28:
0,0,1,1,2,2,2,2,3,3,3,3,3,4,4,4,4,4,4,4,5,5,5,5,5,5,5
