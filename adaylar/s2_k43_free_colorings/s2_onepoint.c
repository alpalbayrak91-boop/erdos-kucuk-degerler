/* Method B1 (m = 7, 8): one-point extension over S7-orbits of the valid
 * colourings of {0..6}.
 * 1. Valid colourings of {0..5} by plain enumeration of all 2^20 masks with a
 *    full 4-set check; representatives = masks equal to their own minimum
 *    image over the 720 relabellings.
 * 2. Every valid colouring of {0..6} is isomorphic to one whose restriction
 *    to {0..5} is such a representative. Extend each representative by all
 *    2^15 colourings of triples {i,j,6}, keep valid ones (full check of the
 *    4-sets through 6), canonicalise under S7 (5040 relabellings, byte
 *    tables), store canonical form and stabiliser size in a hash set.
 *    Check: sum of 5040/|stab| over classes must equal count(7).
 * 3. count(8) = sum over classes (5040/|stab|) * f(T), where f(T) = number
 *    of 2-colourings c of the 21 edges of K7 (colour of triple {i,j,7}) with
 *    no triangle abc monochromatic in c in the colour of T(abc).            */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static int C2(int x) { return x * (x - 1) / 2; }
static int C3(int x) { return x * (x - 1) * (x - 2) / 6; }
static int tidx(int a, int b, int c) {
    int t; if (a > b) { t = a; a = b; b = t; } if (b > c) { t = b; b = c; c = t; } if (a > b) { t = a; a = b; b = t; }
    return C3(c) + C2(b) + a;
}
static int TA[35], TB[35], TC[35];
static int perms(int n, int (*out)[7]) {
    int p[7], np = 0; for (int i = 0; i < n; i++) p[i] = i;
    for (;;) {
        memcpy(out[np++], p, sizeof(int) * n);
        int i = n - 2; while (i >= 0 && p[i] > p[i + 1]) i--; if (i < 0) break;
        int j = n - 1; while (p[j] < p[i]) j--; int t = p[i]; p[i] = p[j]; p[j] = t;
        for (int l = i + 1, r = n - 1; l < r; l++, r--) { t = p[l]; p[l] = p[r]; p[r] = t; }
    }
    return np;
}
static int valid_upto(uint64_t m, int n) {           /* all 4-sets in {0..n-1} */
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) for (int d = c + 1; d < n; d++) {
        int x = (int)(m >> tidx(a,b,c) & 1) + (int)(m >> tidx(a,b,d) & 1) + (int)(m >> tidx(a,c,d) & 1) + (int)(m >> tidx(b,c,d) & 1);
        if (x == 0 || x == 4) return 0;
    }
    return 1;
}
static int P6[720][7], P7[5040][7];
static uint64_t BT[5040][5][256];                    /* byte tables for S7 */
#define HS (1u << 21)
static uint64_t hkey[HS]; static uint32_t hstab[HS]; static uint8_t hused[HS];
int main(void) {
    for (int c = 0; c < 8; c++) for (int b = 0; b < c; b++) for (int a = 0; a < b; a++) {
        int t = tidx(a, b, c); if (t < 35) { TA[t] = a; TB[t] = b; TC[t] = c; }
    }
    int n6 = perms(6, P6), n7 = perms(7, P7);
    for (int q = 0; q < n7; q++) for (int B = 0; B < 5; B++) for (int v = 0; v < 256; v++) {
        uint64_t im = 0;
        for (int k = 0; k < 8; k++) if (v >> k & 1) {
            int t = 8 * B + k; if (t >= 35) continue;
            im |= 1ull << tidx(P7[q][TA[t]], P7[q][TB[t]], P7[q][TC[t]]);
        }
        BT[q][B][v] = im;
    }
    /* step 1 */
    uint32_t *reps = malloc(4096 * 4); int nreps = 0; unsigned long long n6valid = 0;
    for (uint32_t m = 0; m < (1u << 20); m++) {
        if (!valid_upto(m, 6)) continue;
        n6valid++;
        int isrep = 1;
        for (int q = 0; q < n6 && isrep; q++) {
            uint32_t im = 0;
            for (int t = 0; t < 20; t++) if (m >> t & 1) im |= 1u << tidx(P6[q][TA[t]], P6[q][TB[t]], P6[q][TC[t]]);
            if (im < m) isrep = 0;
        }
        if (isrep) reps[nreps++] = m;
    }
    printf("m=6 valid %llu, S6-representatives %d\n", n6valid, nreps);
    /* step 2 */
    size_t ncls = 0, ncand = 0;
    for (int r = 0; r < nreps; r++) for (uint32_t e = 0; e < (1u << 15); e++) {
        uint64_t T = reps[r] | ((uint64_t)e << 20);
        int ok = 1;                                   /* 4-sets {a,b,c,6} */
        for (int a = 0; a < 6 && ok; a++) for (int b = a + 1; b < 6 && ok; b++) for (int c = b + 1; c < 6 && ok; c++) {
            int x = (int)(T >> tidx(a,b,c) & 1) + (int)(T >> tidx(a,b,6) & 1) + (int)(T >> tidx(a,c,6) & 1) + (int)(T >> tidx(b,c,6) & 1);
            if (x == 0 || x == 4) ok = 0;
        }
        if (!ok) continue;
        ncand++;
        uint64_t best = ~0ull; uint32_t stab = 0;
        for (int q = 0; q < n7; q++) {
            uint64_t im = BT[q][0][T & 255] | BT[q][1][T >> 8 & 255] | BT[q][2][T >> 16 & 255] | BT[q][3][T >> 24 & 255] | BT[q][4][T >> 32 & 255];
            if (im < best) best = im;
            if (im == T) stab++;
        }
        uint32_t h = (uint32_t)((best * 0x9E3779B97F4A7C15ull) >> 43) & (HS - 1);
        while (hused[h] && hkey[h] != best) h = (h + 1) & (HS - 1);
        if (!hused[h]) { hused[h] = 1; hkey[h] = best; hstab[h] = stab; ncls++; }
    }
    unsigned long long tot7 = 0;
    for (uint32_t h = 0; h < HS; h++) if (hused[h]) tot7 += 5040 / hstab[h];
    printf("candidates %zu, S7-classes %zu\n7 %llu\n", ncand, ncls, tot7); fflush(stdout);
    /* step 3 */
    uint64_t *RED = malloc((1u << 21) * 8), *BLUE = malloc((1u << 21) * 8);
    for (uint32_t e = 0; e < (1u << 21); e++) {
        uint64_t r = 0, b = 0;
        for (int t = 0; t < 35; t++) {
            int x = (e >> (C2(TB[t]) + TA[t]) & 1) + (e >> (C2(TC[t]) + TA[t]) & 1) + (e >> (C2(TC[t]) + TB[t]) & 1);
            if (x == 3) r |= 1ull << t; if (x == 0) b |= 1ull << t;
        }
        RED[e] = r; BLUE[e] = b;
    }
    unsigned __int128 tot8 = 0; const uint64_t full = (1ull << 35) - 1;
    for (uint32_t h = 0; h < HS; h++) if (hused[h]) {
        uint64_t T = hkey[h], Tb = ~T & full; unsigned long long f = 0;
        if (!valid_upto(T, 7)) { printf("internal error\n"); return 3; }
        for (uint32_t e = 0; e < (1u << 21); e++) f += !((RED[e] & T) | (BLUE[e] & Tb));
        tot8 += (unsigned __int128)(5040 / hstab[h]) * f;
    }
    char buf[64]; int k = 63; buf[k] = 0; unsigned __int128 v = tot8; if (!v) buf[--k] = '0';
    while (v) { buf[--k] = '0' + (int)(v % 10); v /= 10; }
    printf("8 %s\n", buf + k);
    return 0;
}
