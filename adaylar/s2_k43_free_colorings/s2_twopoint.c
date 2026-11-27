/* Method B2 (m = 7, 8): two-point extension over S6-orbits.
 * 1. All valid colourings U of the 20 triples of {0..5} (backtracking).
 * 2. Canonical form of U = min image over the 720 relabellings of {0..5};
 *    orbit sizes = multiplicities after sorting.
 * 3. For a representative U, ext(U) = edge 2-colourings e of K6 such that
 *    adding point 6 (triple {i,j,6} gets colour e(ij)) creates no
 *    monochromatic 4-set {a,b,c,6}: not (ab,ac,bc all red and abc red), same
 *    for blue. count(7) = sum orbit * |ext(U)|.
 * 4. Two new points 6 and 7: e6, e7 in ext(U) independently (4-sets
 *    {a,b,c,6} and {a,b,c,7}); triples {i,6,7} get colours s_i; 4-set
 *    {i,j,6,7} is monochromatic iff e6(ij) = e7(ij) = s_i = s_j. So the red
 *    s-set must be independent in Gr = {ij: e6, e7 red} and the blue s-set
 *    independent in Gb = {ij: e6, e7 blue}. count(8) = sum orbit *
 *    sum_{e6,e7} #s.                                                       */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int C2(int x) { return x * (x - 1) / 2; }
static int C3(int x) { return x * (x - 1) * (x - 2) / 6; }
static int tid(int a, int b, int c) {      /* sorts then colex index */
    int t; if (a > b) { t = a; a = b; b = t; } if (b > c) { t = b; b = c; c = t; } if (a > b) { t = a; a = b; b = t; }
    return C3(c) + C2(b) + a;
}
static uint32_t *all; static size_t nall, capall; static int col[20];
static int TA[20], TB[20], TC[20];
static void rec(int t) {
    if (t == 20) {
        uint32_t m = 0; for (int i = 0; i < 20; i++) if (col[i]) m |= 1u << i;
        if (nall == capall) { capall = capall ? 2 * capall : 1024; all = realloc(all, capall * 4); }
        all[nall++] = m; return;
    }
    int a = TA[t], b = TB[t], c = TC[t];       /* a<b<c; colex order => c max */
    for (int v = 0; v < 2; v++) {
        col[t] = v; int ok = 1;
        for (int x = 0; x < b && ok; x++) if (x != a) {
            /* 4-set {x,a,b,c} with x<b: all its other triples precede t in colex
               iff the largest-but-c elements are smaller; check only when complete */
            int t1 = tid(x, a, b), t2 = tid(x, a, c), t3 = tid(x, b, c);
            if (t1 < t && t2 < t && t3 < t && col[t1] == v && col[t2] == v && col[t3] == v) ok = 0;
        }
        if (ok) rec(t + 1);
    }
}
static int cmpu(const void *x, const void *y) { uint32_t a = *(const uint32_t *)x, b = *(const uint32_t *)y; return a < b ? -1 : a > b; }
int main(void) {
    for (int c = 0; c < 6; c++) for (int b = 0; b < c; b++) for (int a = 0; a < b; a++) {
        int t = tid(a, b, c); TA[t] = a; TB[t] = b; TC[t] = c;
    }
    rec(0);
    /* final validity check of every 4-set (guards the pruning logic) */
    size_t good = 0;
    for (size_t s = 0; s < nall; s++) {
        uint32_t m = all[s]; int ok = 1;
        for (int a = 0; a < 6; a++) for (int b = a + 1; b < 6; b++) for (int c = b + 1; c < 6; c++) for (int d = c + 1; d < 6; d++) {
            int x = (m >> tid(a,b,c) & 1) + (m >> tid(a,b,d) & 1) + (m >> tid(a,c,d) & 1) + (m >> tid(b,c,d) & 1);
            if (x == 0 || x == 4) ok = 0;
        }
        if (ok) all[good++] = m;
    }
    printf("m=6 colourings: %zu (generated %zu)\n", good, nall); nall = good;
    /* permutations of {0..5} */
    int perm[720][6], np = 0, p[6] = {0,1,2,3,4,5};
    for (;;) {
        for (int i = 0; i < 6; i++) perm[np][i] = p[i]; np++;
        int i = 4; while (i >= 0 && p[i] > p[i + 1]) i--; if (i < 0) break;
        int j = 5; while (p[j] < p[i]) j--; int t = p[i]; p[i] = p[j]; p[j] = t;
        for (int l = i + 1, r = 5; l < r; l++, r--) { t = p[l]; p[l] = p[r]; p[r] = t; }
    }
    uint32_t *canon = malloc(nall * 4);
    for (size_t s = 0; s < nall; s++) {
        uint32_t best = 0xffffffffu, m = all[s];
        for (int q = 0; q < np; q++) {
            uint32_t im = 0;
            for (int t = 0; t < 20; t++) if (m >> t & 1) im |= 1u << tid(perm[q][TA[t]], perm[q][TB[t]], perm[q][TC[t]]);
            if (im < best) best = im;
        }
        canon[s] = best;
    }
    qsort(canon, nall, 4, cmpu);
    /* edge masks for K6 and monochromatic-triangle masks */
    static uint32_t RED[1 << 15], BLUE[1 << 15];
    for (uint32_t e = 0; e < (1u << 15); e++) {
        uint32_t r = 0, b = 0;
        for (int t = 0; t < 20; t++) {
            int x = (e >> (C2(TB[t]) + TA[t]) & 1) + (e >> (C2(TC[t]) + TA[t]) & 1) + (e >> (C2(TC[t]) + TB[t]) & 1);
            if (x == 3) r |= 1u << t; if (x == 0) b |= 1u << t;
        }
        RED[e] = r; BLUE[e] = b;
    }
    /* independence masks over s in {0..63} */
    static uint64_t INDR[1 << 15], INDB[1 << 15];
    for (uint32_t g = 0; g < (1u << 15); g++) {
        uint64_t mr = 0, mb = 0;
        for (int s = 0; s < 64; s++) {
            int okr = 1, okb = 1;
            for (int j = 1; j < 6; j++) for (int i = 0; i < j; i++) if (g >> (C2(j) + i) & 1) {
                if ((s >> i & 1) && (s >> j & 1)) okr = 0;
                if (!(s >> i & 1) && !(s >> j & 1)) okb = 0;
            }
            if (okr) mr |= 1ull << s; if (okb) mb |= 1ull << s;
        }
        INDR[g] = mr; INDB[g] = mb;
    }
    uint32_t *ext = malloc((1u << 15) * 4);
    unsigned long long tot7 = 0, orbsum = 0; unsigned __int128 tot8 = 0; size_t nreps = 0;
    for (size_t s = 0; s < nall;) {
        size_t r = s; while (r < nall && canon[r] == canon[s]) r++;
        unsigned long long orb = r - s; uint32_t U = canon[s], Ub = ~U & 0xfffffu;
        int ne = 0;
        for (uint32_t e = 0; e < (1u << 15); e++) if (!((RED[e] & U) | (BLUE[e] & Ub))) ext[ne++] = e;
        tot7 += orb * (unsigned long long)ne;
        unsigned long long pairs = 0;
        for (int x = 0; x < ne; x++) for (int y = 0; y < ne; y++) {
            uint32_t gr = ext[x] & ext[y], gb = ~(ext[x] | ext[y]) & 0x7fffu;
            pairs += __builtin_popcountll(INDR[gr] & INDB[gb]);
        }
        tot8 += (unsigned __int128)orb * pairs;
        orbsum += orb; nreps++; s = r;
    }
    printf("S6-orbits: %zu, orbit-size sum %llu\n", nreps, orbsum);
    printf("7 %llu\n", tot7);
    char buf[64]; int k = 63; buf[k] = 0; unsigned __int128 v = tot8; if (!v) buf[--k] = '0';
    while (v) { buf[--k] = '0' + (int)(v % 10); v /= 10; }
    printf("8 %s\n", buf + k);
    return 0;
}
