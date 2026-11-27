/* Sanity check for small n: enumerate all 2^C(n,2) edge sets as plain bitmasks,
 * test all C(n,4) vertex subsets. Usage: s1_bruteforce_small NMAX (NMAX <= 7). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int main(int argc, char **argv) {
    int NMAX = argc > 1 ? atoi(argv[1]) : 6;
    for (int n = 1; n <= NMAX; n++) {
        int E = n * (n - 1) / 2, ei[64], ej[64], e = 0;
        for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) { ei[e] = i; ej[e] = j; e++; }
        unsigned long long count = 0;
        for (uint64_t m = 0; m < (1ull << E); m++) {
            uint32_t adj[16] = {0};
            for (int t = 0; t < E; t++) if (m >> t & 1) { adj[ei[t]] |= 1u << ej[t]; adj[ej[t]] |= 1u << ei[t]; }
            int bad = 0;
            for (int a = 0; a < n && !bad; a++) for (int b = a + 1; b < n && !bad; b++)
            for (int c = b + 1; c < n && !bad; c++) for (int d = c + 1; d < n && !bad; d++) {
                uint32_t S = (1u<<a)|(1u<<b)|(1u<<c)|(1u<<d);
                int ea = __builtin_popcount(adj[a]&S), eb = __builtin_popcount(adj[b]&S);
                int ec = __builtin_popcount(adj[c]&S), ed = __builtin_popcount(adj[d]&S);
                if (ea == 2 && eb == 2 && ec == 2 && ed == 2) bad = 1;
            }
            if (!bad) count++;
        }
        printf("%d %llu\n", n, count);
    }
    return 0;
}
