/* Method A: direct count of 2-colourings of the 3-subsets of {0..m-1} with no
 * monochromatic 4-set (all four 3-subsets of the 4-set the same colour).
 * Triples are coloured in the order (i<j<k) by k, then (i,j) lexicographic.
 * When triple {i,j,k} is coloured, every 4-set {a,i,j,k} with a<i is complete
 * (its triples aij, aik, ajk were coloured earlier) and is checked: early cut.
 * For m >= 3 the colour of {0,1,2} is fixed and the count doubled
 * (colour swap is a bijection). Usage: s2_direct MMAX (MMAX <= 8)          */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int M; static int col[16][16][16]; static int ti[64], tj[64], tk[64], T;
static uint64_t leaves;
static void rec(int t) {
    if (t == T) { leaves++; return; }
    int i = ti[t], j = tj[t], k = tk[t];
    for (int c = 0; c < 2; c++) {
        if (t == 0 && c == 1) break;          /* symmetry: first triple red */
        col[i][j][k] = c;
        int ok = 1;
        for (int a = 0; a < i && ok; a++)
            if (col[a][i][j] == c && col[a][i][k] == c && col[a][j][k] == c) ok = 0;
        if (ok) rec(t + 1);
    }
}
int main(int argc, char **argv) {
    int MMAX = argc > 1 ? atoi(argv[1]) : 6;
    for (M = 1; M <= MMAX; M++) {
        T = 0;
        for (int k = 0; k < M; k++) for (int i = 0; i < k; i++) for (int j = i + 1; j < k; j++) {
            ti[T] = i; tj[T] = j; tk[T] = k; T++;
        }
        leaves = 0; rec(0);
        unsigned long long total = T ? 2 * leaves : 1;
        printf("%d %llu\n", M, total);
        fflush(stdout);
    }
    return 0;
}
