/*
 * e585.c -- Erdos problem 585: graphs with no two edge-disjoint cycles
 * on the same vertex set.
 *
 * A simple graph G is "good" if there is no vertex set S (|S| >= 3) such
 * that G[S] contains two edge-disjoint Hamiltonian cycles.  The property
 * is closed under deleting edges and vertices.
 *
 * Modes (input: graph6 on stdin, one graph per line):
 *   e585 check [-g] [-b] [-q] [-l]
 *       default: one line per graph: "iyi=<0|1> kenar=<m>" and, for a bad
 *       graph, a witness "S=... C1=... C2=..." (two edge-disjoint
 *       Hamiltonian cycles of G[S]).
 *       -g  print only the graph6 strings of good graphs (filter)
 *       -b  print only the graph6 strings of bad graphs (filter)
 *       -q  no per-graph output; summary only (stderr)
 *       -c  certificate: for each BAD graph one line "graph6 S C1 C2"
 *           (checkable by sertifika_dogrula.py without this program)
 *       -l  only test sets S containing the last vertex n-1 (sound only if
 *           G - (n-1) is known to be good; used by the extension ladder)
 *   e585 extend M
 *       input: good graphs on n-1 vertices.  For each one, add a vertex v
 *       with every neighbourhood N such that the new graph has >= M edges
 *       and v has minimum degree in it; output (graph6) the new graphs that
 *       are good.  Output is NOT isomorphism-reduced (pipe through
 *       nauty-labelg | sort -u).
 *
 * Algorithm for one set S: only sets in which every vertex has >= 4
 * neighbours inside S can carry two edge-disjoint Hamiltonian cycles,
 * and we restrict to subsets of the 4-core of G.  For such S we enumerate
 * Hamiltonian cycles C1 of G[S] (each undirected cycle once) and, for each,
 * test whether G[S] - E(C1) is Hamiltonian on S.
 *
 * Summary on stderr: "graphs=<N> good=<N> bad=<N>".
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 32
typedef uint32_t set;

static int n;
static set adj[MAXN];

static int pc(set x) { return __builtin_popcount(x); }

static int read_g6(const char *s) {
    const unsigned char *p = (const unsigned char *)s;
    if (*p == '>') { /* header >>graph6<< */
        p += 10;
    }
    if (*p < 63 || *p > 126) return -1;
    n = *p++ - 63;
    if (n > MAXN - 1) return -1;
    for (int i = 0; i < n; i++) adj[i] = 0;
    int k = 0, bits = 0, val = 0;
    for (int j = 1; j < n; j++)
        for (int i = 0; i < j; i++) {
            if (bits == 0) {
                if (*p < 63 || *p > 126) return -1;
                val = *p++ - 63;
                bits = 6;
            }
            bits--;
            if ((val >> bits) & 1) { adj[i] |= 1u << j; adj[j] |= 1u << i; }
            k++;
        }
    return n;
}

static void write_g6(int nn, const set *a, FILE *f) {
    char buf[256];
    int pos = 0, bits = 0, val = 0;
    buf[pos++] = (char)(63 + nn);
    for (int j = 1; j < nn; j++)
        for (int i = 0; i < j; i++) {
            val = (val << 1) | ((a[i] >> j) & 1);
            if (++bits == 6) { buf[pos++] = (char)(63 + val); bits = 0; val = 0; }
        }
    if (bits) { val <<= (6 - bits); buf[pos++] = (char)(63 + val); }
    buf[pos] = 0;
    fputs(buf, f);
    fputc('\n', f);
}

static int edges(void) {
    int m = 0;
    for (int i = 0; i < n; i++) m += pc(adj[i]);
    return m / 2;
}

/* ---- Hamiltonian cycle search ---- */
static set S_cur;          /* vertex set */
static int S_size, s0;     /* size, start vertex (min of S) */
static set h2[MAXN];       /* adjacency for the second search */
static int path1[MAXN], path2[MAXN];
static int found;

static int ham2(int cur, set vis, int depth) {
    if (depth == S_size) return (h2[cur] >> s0) & 1;
    set cand = h2[cur] & S_cur & ~vis;
    while (cand) {
        int v = __builtin_ctz(cand); cand &= cand - 1;
        path2[depth] = v;
        if (ham2(v, vis | (1u << v), depth + 1)) return 1;
    }
    return 0;
}

static int ham1(int cur, set vis, int depth) {
    if (depth == S_size) {
        if (!((adj[cur] >> s0) & 1)) return 0;
        if (path1[1] > path1[S_size - 1]) return 0; /* each cycle once */
        /* remove C1 edges, test Hamiltonicity of the rest */
        for (int i = 0; i < n; i++) h2[i] = adj[i] & S_cur;
        for (int i = 0; i < S_size; i++) {
            int a = path1[i], b = path1[(i + 1) % S_size];
            h2[a] &= ~(1u << b); h2[b] &= ~(1u << a);
        }
        path2[0] = s0;
        if (ham2(s0, 1u << s0, 1)) { found = 1; return 1; }
        return 0;
    }
    set cand = adj[cur] & S_cur & ~vis;
    while (cand) {
        int v = __builtin_ctz(cand); cand &= cand - 1;
        path1[depth] = v;
        if (ham1(v, vis | (1u << v), depth + 1)) return 1;
    }
    return 0;
}

static int test_set(set S) {
    S_cur = S; S_size = pc(S); s0 = __builtin_ctz(S);
    found = 0;
    path1[0] = s0;
    ham1(s0, 1u << s0, 1);
    return found;
}

/* 4-core of the vertex set T */
static set core4(set T) {
    int changed = 1;
    while (changed) {
        changed = 0;
        for (int v = 0; v < n; v++)
            if (((T >> v) & 1) && pc(adj[v] & T) < 4) { T &= ~(1u << v); changed = 1; }
    }
    return T;
}

static set wit_S;
/* returns 1 if good; on bad, wit_S/path1/path2 hold a witness */
static int is_good(int lastonly) {
    set all = (n == 32) ? 0xffffffffu : ((1u << n) - 1);
    set C = core4(all);
    if (pc(C) < 5) return 1;
    if (lastonly && !((C >> (n - 1)) & 1)) return 1;
    /* enumerate subsets S of C, |S| >= 5 */
    set S = 0;
    do {
        S = (S - C) & C; /* next subset of C */
        if (pc(S) < 5) continue;
        if (lastonly && !((S >> (n - 1)) & 1)) continue;
        int ok = 1, e2 = 0;
        for (set t = S; t; t &= t - 1) {
            int v = __builtin_ctz(t), d = pc(adj[v] & S);
            if (d < 4) { ok = 0; break; }
            e2 += d;
        }
        if (!ok || e2 / 2 < 2 * pc(S)) continue;
        if (test_set(S)) { wit_S = S; return 0; }
    } while (S != C);
    return 1;
}

static void print_witness(FILE *f) {
    fprintf(f, " S=");
    int first = 1;
    for (int v = 0; v < n; v++)
        if ((wit_S >> v) & 1) { fprintf(f, first ? "%d" : ",%d", v); first = 0; }
    fprintf(f, " C1=");
    for (int i = 0; i < S_size; i++) fprintf(f, "%d-", path1[i]);
    fprintf(f, "%d C2=", path1[0]);
    for (int i = 0; i < S_size; i++) fprintf(f, "%d-", path2[i]);
    fprintf(f, "%d", path2[0]);
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: e585 check [-g|-b|-q] [-l] | e585 extend M\n"); return 2; }
    static char line[4096];
    long long ng = 0, ngood = 0, nbad = 0;
    if (!strcmp(argv[1], "check")) {
        int mode = 0, lastonly = 0; /* 0 lines, 1 good filter, 2 bad filter, 3 quiet */
        for (int i = 2; i < argc; i++) {
            if (!strcmp(argv[i], "-g")) mode = 1;
            else if (!strcmp(argv[i], "-b")) mode = 2;
            else if (!strcmp(argv[i], "-q")) mode = 3;
            else if (!strcmp(argv[i], "-c")) mode = 4;
            else if (!strcmp(argv[i], "-l")) lastonly = 1;
            else { fprintf(stderr, "bad option %s\n", argv[i]); return 2; }
        }
        while (fgets(line, sizeof line, stdin)) {
            line[strcspn(line, "\r\n")] = 0;
            if (!line[0]) continue;
            if (read_g6(line) < 0) { fprintf(stderr, "bad graph6: %s\n", line); return 1; }
            ng++;
            int g = is_good(lastonly);
            if (g) ngood++; else nbad++;
            if (mode == 0) {
                printf("iyi=%d kenar=%d", g, edges());
                if (!g) print_witness(stdout);
                printf("\n");
            } else if (mode == 1 && g) puts(line);
            else if (mode == 2 && !g) puts(line);
            else if (mode == 4 && !g) { fputs(line, stdout); print_witness(stdout); putchar('\n'); }
        }
    } else if (!strcmp(argv[1], "extend")) {
        if (argc < 3) return 2;
        int M = atoi(argv[2]);
        while (fgets(line, sizeof line, stdin)) {
            line[strcspn(line, "\r\n")] = 0;
            if (!line[0]) continue;
            if (read_g6(line) < 0) { fprintf(stderr, "bad graph6: %s\n", line); return 1; }
            int n0 = n, m0 = edges();
            set base[MAXN];
            memcpy(base, adj, sizeof base);
            for (set N = 0; N < (1u << n0); N++) {
                int d = pc(N);
                if (m0 + d < M) continue;
                int ok = 1;
                for (int u = 0; u < n0; u++)
                    if (pc(base[u]) + ((N >> u) & 1) < d) { ok = 0; break; }
                if (!ok) continue;
                n = n0 + 1;
                for (int u = 0; u < n0; u++) adj[u] = base[u] | (((N >> u) & 1) ? (1u << n0) : 0);
                adj[n0] = N;
                ng++;
                if (is_good(1)) { ngood++; write_g6(n, adj, stdout); } else nbad++;
            }
        }
    } else { fprintf(stderr, "unknown mode\n"); return 2; }
    fprintf(stderr, "graphs=%lld good=%lld bad=%lld\n", ng, ngood, nbad);
    return 0;
}
