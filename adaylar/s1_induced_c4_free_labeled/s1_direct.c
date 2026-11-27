/* Method A: direct count of labeled graphs on {0..n-1} with no induced C4.
 * Depth-first over labeled graphs: vertex k chooses its neighbourhood among
 * {0..k-1} (bitmask); every 4-subset containing k is checked when k is added,
 * so each 4-subset is checked exactly once on every root-to-leaf path.
 * A 4-vertex induced subgraph is C4 iff every vertex has degree 2 inside it.
 * Usage: s1_direct NMAX   (prints "n count" for n = 1..NMAX, NMAX <= 9)    */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static int NMAX;
static uint32_t adj[16];
static uint64_t cnt[16];

static int deg_in(int v, uint32_t S) { return __builtin_popcount(adj[v] & S); }

static int has_induced_c4_with(int k) {
    for (int a = 0; a < k; a++)
        for (int b = a + 1; b < k; b++)
            for (int c = b + 1; c < k; c++) {
                uint32_t S = (1u << a) | (1u << b) | (1u << c) | (1u << k);
                if (deg_in(a, S) == 2 && deg_in(b, S) == 2 && deg_in(c, S) == 2 &&
                    deg_in(k, S) == 2)
                    return 1;
            }
    return 0;
}

static void rec(int k) {           /* vertices 0..k-1 placed, graph valid */
    cnt[k]++;
    if (k == NMAX) return;
    for (uint32_t N = 0; N < (1u << k); N++) {
        adj[k] = N;
        for (int i = 0; i < k; i++) if (N >> i & 1) adj[i] |= 1u << k;
        if (!has_induced_c4_with(k)) rec(k + 1);
        for (int i = 0; i < k; i++) adj[i] &= ~(1u << k);
        adj[k] = 0;
    }
}

int main(int argc, char **argv) {
    NMAX = argc > 1 ? atoi(argv[1]) : 7;
    if (NMAX < 1 || NMAX > 9) { fprintf(stderr, "NMAX in 1..9\n"); return 1; }
    rec(0);
    for (int n = 1; n <= NMAX; n++) printf("%d %llu\n", n, (unsigned long long)cnt[n]);
    return 0;
}
