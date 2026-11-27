/* Method B: extension count. A colouring of the triples of {0..m-1} is stored
 * as a bitmask over triples in colex order (idx(i<j<k) = C(k,3)+C(j,2)+i), bit
 * set = red. Adding point p = m-1 to a valid colouring T of {0..p-1} means
 * colouring every edge ij of K_p (colour of triple {i,j,p}). The new 4-sets
 * are {a,b,c,p}: monochromatic iff abc, abp, acp, bcp share a colour, i.e. iff
 * edges ab, ac, bc are all red and abc is red, or all blue and abc is blue.
 * For each edge colouring e we precompute RED(e), BLUE(e) = masks of
 * triangles of K_p that are monochromatic red / blue in e; e is admissible
 * for T iff (RED(e) & T) == 0 and (BLUE(e) & ~T) == 0.
 * Builds all valid colourings level by level from m = 1 (independent of
 * method A). Usage: s2_extend MMAX (MMAX <= 7). Prints "m count".          */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int C2(int x) { return x * (x - 1) / 2; }
static int C3(int x) { return x * (x - 1) * (x - 2) / 6; }
int main(int argc, char **argv) {
    int MMAX = argc > 1 ? atoi(argv[1]) : 6;
    uint64_t *cur = malloc(sizeof(uint64_t)); size_t ncur = 1; cur[0] = 0; /* m = 0 */
    for (int m = 1; m <= MMAX; m++) {
        int p = m - 1, E = C2(p), NT = C3(p);
        uint64_t full = NT ? ((NT == 64) ? ~0ull : ((1ull << NT) - 1)) : 0;
        size_t ne = (size_t)1 << E;
        uint64_t *RED = malloc(ne * 8), *BLUE = malloc(ne * 8);
        for (size_t e = 0; e < ne; e++) {
            uint64_t r = 0, b = 0;
            for (int k = 0; k < p; k++) for (int j = 0; j < k; j++) for (int i = 0; i < j; i++) {
                int eij = (e >> (C2(j) + i)) & 1, eik = (e >> (C2(k) + i)) & 1, ejk = (e >> (C2(k) + j)) & 1;
                int t = C3(k) + C2(j) + i;
                if (eij && eik && ejk) r |= 1ull << t;
                if (!eij && !eik && !ejk) b |= 1ull << t;
            }
            RED[e] = r; BLUE[e] = b;
        }
        int store = (m < MMAX);
        size_t cap = store ? 1024 : 0, nnext = 0; uint64_t *next = store ? malloc(cap * 8) : NULL;
        unsigned long long count = 0;
        for (size_t s = 0; s < ncur; s++) {
            uint64_t T = cur[s], Tb = ~T & full;
            for (size_t e = 0; e < ne; e++) {
                if ((RED[e] & T) | (BLUE[e] & Tb)) continue;
                count++;
                if (store) {
                    if (nnext == cap) { cap *= 2; next = realloc(next, cap * 8); }
                    next[nnext++] = T | ((uint64_t)e << NT);
                }
            }
        }
        printf("%d %llu\n", m, count); fflush(stdout);
        free(RED); free(BLUE); free(cur); cur = next; ncur = nnext;
    }
    return 0;
}
