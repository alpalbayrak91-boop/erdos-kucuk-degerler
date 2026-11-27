/* Reads graph6 lines on stdin, writes those with no induced C4 to stdout.
 * Used by method B (geng | s1_filter | countg --a). n <= 16.              */
#include <stdio.h>
#include <string.h>
#include <stdint.h>
int main(void) {
    char line[256];
    while (fgets(line, sizeof line, stdin)) {
        if (line[0] == '>') continue;
        int n = line[0] - 63;
        uint32_t adj[16] = {0};
        int bit = 0; const char *p = line + 1;
        for (int j = 1; j < n; j++) for (int i = 0; i < j; i++) {
            int v = (p[bit / 6] - 63) >> (5 - bit % 6) & 1; bit++;
            if (v) { adj[i] |= 1u << j; adj[j] |= 1u << i; }
        }
        int bad = 0;
        for (int a = 0; a < n && !bad; a++) for (int b = a + 1; b < n && !bad; b++)
        for (int c = b + 1; c < n && !bad; c++) for (int d = c + 1; d < n && !bad; d++) {
            uint32_t S = (1u<<a)|(1u<<b)|(1u<<c)|(1u<<d);
            if (__builtin_popcount(adj[a]&S) == 2 && __builtin_popcount(adj[b]&S) == 2 &&
                __builtin_popcount(adj[c]&S) == 2 && __builtin_popcount(adj[d]&S) == 2) bad = 1;
        }
        if (!bad) fputs(line, stdout);
    }
    return 0;
}
