/* Method C: labeled count at n from the UNLABELED (n-1)-vertex graphs.
 * Input: graph6 lines (all induced-C4-free graphs on n-1 vertices, one per
 * isomorphism class). For each H compute |Aut H| by own backtracking (no nauty)
 * and v(H) = number of subsets N of V(H) such that adding a new vertex with
 * neighbourhood N creates no induced C4. A new induced C4 through the new
 * vertex z is z-a-x-b-z with a,b in N non-adjacent and x outside N adjacent to
 * both a and b. Labeled count = sum_H (n-1)!/|Aut H| * v(H).
 * Output: lines "aut sum_v count" aggregated by aut value.                 */
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
#define MAXA 4096
static uint64_t avals[MAXA], vsum[MAXA], acnt[MAXA]; static int na;
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
        uint64_t v = 0;
        for (uint32_t N = 0; N < (1u << n); N++) {
            int bad = 0;
            for (int a = 0; a < n && !bad; a++) if (N >> a & 1)
                for (int b = a + 1; b < n && !bad; b++) if ((N >> b & 1) && !(adj[a] >> b & 1))
                    if (adj[a] & adj[b] & ~N) bad = 1;
            if (!bad) v++;
        }
        int t; for (t = 0; t < na; t++) if (avals[t] == naut) break;
        if (t == na) { if (na == MAXA) return 2; avals[na] = naut; na++; }
        vsum[t] += v; acnt[t]++;
    }
    for (int t = 0; t < na; t++)
        printf("%llu %llu %llu\n", (unsigned long long)avals[t], (unsigned long long)vsum[t], (unsigned long long)acnt[t]);
    return 0;
}
