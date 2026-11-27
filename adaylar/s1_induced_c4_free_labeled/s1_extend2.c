/* Method D: labeled count at n from the UNLABELED (n-2)-vertex graphs by adding
 * two labeled vertices z1, z2 at once (independent check of method C).
 * For H (n-2 vertices): V(H) = admissible single neighbourhoods (no induced C4
 * through one new vertex: tested here by brute force over all 3-subsets).
 * Pair (N1, N2, z1~z2?) is admissible iff N1, N2 in V(H) and no induced C4
 * contains both z1 and z2:
 *   z1~z2 : C4 z1-z2-b-a with a in N1\N2, b in N2\N1, a~b      -> forbidden
 *   z1!~z2: C4 z1-a-z2-b with a,b in N1&N2, a!~b               -> forbidden
 * Labeled count(n) = sum_H (n-2)!/|Aut H| * w(H).
 * Output lines "aut sum_w count".                                         */
#include <stdio.h>
#include <stdint.h>
#include <string.h>
static int n; static uint32_t adj[16]; static int deg[16];
static int img[16]; static uint32_t used; static uint64_t naut;
static void autrec(int k) {
    if (k == n) { naut++; return; }
    for (int w = 0; w < n; w++) {
        if (used >> w & 1 || deg[w] != deg[k]) continue;
        int ok = 1;
        for (int i = 0; i < k && ok; i++)
            if (((adj[k] >> i) & 1) != ((adj[w] >> img[i]) & 1)) ok = 0;
        if (!ok) continue;
        img[k] = w; used |= 1u << w; autrec(k + 1); used &= ~(1u << w);
    }
}
static int single_ok(uint32_t N) {   /* new vertex z = bit n */
    uint32_t A[17]; for (int i = 0; i < n; i++) A[i] = adj[i] | ((N >> i & 1) << n); A[n] = N;
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) {
        uint32_t S = (1u << a) | (1u << b) | (1u << c) | (1u << n);
        if (__builtin_popcount(A[a] & S) == 2 && __builtin_popcount(A[b] & S) == 2 &&
            __builtin_popcount(A[c] & S) == 2 && __builtin_popcount(A[n] & S) == 2) return 0;
    }
    return 1;
}
#define MAXA 4096
static uint64_t avals[MAXA], wsum[MAXA], acnt[MAXA]; static int na;
static uint32_t Vs[1 << 12];
int main(void) {
    char line[256];
    while (fgets(line, sizeof line, stdin)) {
        if (line[0] == '>') continue;
        n = line[0] - 63; memset(adj, 0, sizeof adj);
        int bit = 0; const char *p = line + 1;
        for (int j = 1; j < n; j++) for (int i = 0; i < j; i++) {
            int v = (p[bit / 6] - 63) >> (5 - bit % 6) & 1; bit++;
            if (v) { adj[i] |= 1u << j; adj[j] |= 1u << i; }
        }
        for (int i = 0; i < n; i++) deg[i] = __builtin_popcount(adj[i]);
        naut = 0; used = 0; autrec(0);
        int nv = 0;
        for (uint32_t N = 0; N < (1u << n); N++) if (single_ok(N)) Vs[nv++] = N;
        uint64_t w = 0;
        for (int x = 0; x < nv; x++) for (int y = 0; y < nv; y++) {
            uint32_t N1 = Vs[x], N2 = Vs[y];
            uint32_t A = N1 & ~N2, B = N2 & ~N1, I = N1 & N2;
            int okadj = 1, oknon = 1;
            for (int a = 0; a < n && okadj; a++) if ((A >> a & 1) && (adj[a] & B)) okadj = 0;
            for (int a = 0; a < n && oknon; a++) if ((I >> a & 1) && (I & ~adj[a] & ~(1u << a))) oknon = 0;
            w += okadj + oknon;
        }
        int t; for (t = 0; t < na; t++) if (avals[t] == naut) break;
        if (t == na) { if (na == MAXA) return 2; avals[na] = naut; na++; }
        wsum[t] += w; acnt[t]++;
    }
    for (int t = 0; t < na; t++)
        printf("%llu %llu %llu\n", (unsigned long long)avals[t], (unsigned long long)wsum[t], (unsigned long long)acnt[t]);
    return 0;
}
