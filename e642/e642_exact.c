/*
 * Exact canonical-enumeration solver for Erdos Problem #642 (Hamburger-Szegedy):
 *   f(n) = max |E(G)| over simple graphs G on n vertices in which every simple cycle C
 *   has strictly more vertices than chords (equivalently, |E(G[V(C)])| <= 2*|V(C)| - 1).
 *
 * Cross-checks:
 *   - Sanity mode (--test-canon) checks total unlabeled graphs for n = 2..6 against
 *     OEIS A000088: 2, 4, 11, 34, 156.
 *   - Exact enumeration of valid non-isomorphic graphs by (n, m), exploiting the lossless
 *     hereditary minimum-degree bound: if G on n vertices with m edges has min degree delta,
 *     then delta <= floor(2m/n) and G - v is a valid (n-1)-vertex graph with m - delta edges.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#define MAXN 10

typedef struct {
    uint64_t code;
    uint16_t adj[MAXN];
    uint8_t n;
    uint8_t m;
} Graph;

static int has_ham_cycle(const uint16_t local_adj[MAXN], int k) {
    /* Held-Karp bitmask DP starting at vertex 0 */
    int full = (1 << k) - 1;
    uint16_t dp[1 << MAXN];
    memset(dp, 0, (size_t)(1 << k) * sizeof(uint16_t));
    dp[1] = 1;
    for (int mask = 1; mask <= full; mask += 2) {
        uint16_t reach = dp[mask];
        if (!reach) continue;
        uint16_t u_bits = reach;
        while (u_bits) {
            int u = __builtin_ctz(u_bits);
            u_bits &= (uint16_t)(u_bits - 1);
            uint16_t nbrs = local_adj[u] & (uint16_t)(~mask) & (uint16_t)full;
            uint16_t v_bits = nbrs;
            while (v_bits) {
                int v = __builtin_ctz(v_bits);
                v_bits &= (uint16_t)(v_bits - 1);
                dp[mask | (1 << v)] |= (uint16_t)(1 << v);
            }
        }
    }
    return (dp[full] & local_adj[0]) != 0;
}

static int is_valid_with_new_vertex(int n, const uint16_t adj[MAXN]) {
    /* Assumes G - {n-1} is already valid. Checks subsets S of 0..n-1 containing (n-1)
     * with |S| = L >= 5, |E(G[S])| >= 2*L, and every vertex in S having deg_{G[S]} >= 2. */
    int newv = n - 1;
    if (n < 5) return 1;
    if (__builtin_popcount((unsigned)adj[newv]) < 2) return 1;
    int full_sub = 1 << (n - 1);
    for (int mask_prev = 0; mask_prev < full_sub; mask_prev++) {
        int L = __builtin_popcount((unsigned)mask_prev) + 1;
        if (L < 5) continue;
        int smask = mask_prev | (1 << newv);
        int deg_sum = 0;
        int deg_ok = 1;
        int tmp = smask;
        while (tmp) {
            int v = __builtin_ctz(tmp);
            tmp &= tmp - 1;
            int dv = __builtin_popcount((unsigned)(adj[v] & smask));
            if (dv < 2) {
                deg_ok = 0;
                break;
            }
            deg_sum += dv;
        }
        if (!deg_ok) continue;
        int e_cnt = deg_sum / 2;
        if (e_cnt < 2 * L) continue;
        int verts[MAXN];
        int k = 0;
        tmp = smask;
        while (tmp) {
            int v = __builtin_ctz(tmp);
            tmp &= tmp - 1;
            verts[k++] = v;
        }
        uint16_t local_adj[MAXN];
        for (int i = 0; i < k; i++) {
            uint16_t row = 0;
            uint16_t av = adj[verts[i]];
            for (int j = 0; j < k; j++) {
                if ((av >> verts[j]) & 1) row |= (uint16_t)(1 << j);
            }
            local_adj[i] = row;
        }
        if (has_ham_cycle(local_adj, k)) return 0;
    }
    return 1;
}

/* Exact canonicalization by degree+neighbor-degree signature bucketing + branch-and-bound */
typedef struct {
    int n;
    int total_bits;
    const uint16_t *adj;
    uint64_t sig[MAXN];
    int bucket_verts[MAXN][MAXN];
    int bucket_sz[MAXN];
    int pos_bucket[MAXN];
    int perm[MAXN];
    int used_mask;
    uint64_t best_code;
} CanonCtx;

static void canon_dfs(CanonCtx *ctx, int i, uint64_t cur_code) {
    if (i == ctx->n) {
        if (cur_code < ctx->best_code) ctx->best_code = cur_code;
        return;
    }
    int b = ctx->pos_bucket[i];
    int sz = ctx->bucket_sz[b];
    int rem_after = ctx->total_bits - (i * (i + 1)) / 2;
    for (int idx = 0; idx < sz; idx++) {
        int v = ctx->bucket_verts[b][idx];
        if ((ctx->used_mask >> v) & 1) continue;
        ctx->perm[i] = v;
        uint64_t next_code = cur_code;
        int base_bit = ctx->total_bits - 1 - (i * (i - 1)) / 2;
        uint16_t av = ctx->adj[v];
        for (int j = 0; j < i; j++) {
            if ((av >> ctx->perm[j]) & 1) {
                next_code |= (1ULL << (base_bit - j));
            }
        }
        if ((next_code >> rem_after) > (ctx->best_code >> rem_after)) continue;
        ctx->used_mask |= (1 << v);
        canon_dfs(ctx, i + 1, next_code);
        ctx->used_mask &= ~(1 << v);
    }
}

static uint64_t canonical_code(int n, const uint16_t adj[MAXN]) {
    if (n <= 1) return 0ULL;
    CanonCtx ctx;
    ctx.n = n;
    ctx.total_bits = (n * (n - 1)) / 2;
    ctx.adj = adj;
    ctx.used_mask = 0;
    ctx.best_code = UINT64_MAX;

    int deg[MAXN];
    for (int v = 0; v < n; v++) deg[v] = __builtin_popcount((unsigned)adj[v]);
    for (int v = 0; v < n; v++) {
        uint64_t s = ((uint64_t)deg[v]) << 40;
        uint16_t av = adj[v];
        while (av) {
            int u = __builtin_ctz(av);
            av &= (uint16_t)(av - 1);
            s += (1ULL << (4 * deg[u]));
        }
        ctx.sig[v] = s;
    }
    int order[MAXN];
    for (int v = 0; v < n; v++) order[v] = v;
    for (int a = 0; a < n; a++) {
        for (int b = a + 1; b < n; b++) {
            if (ctx.sig[order[b]] < ctx.sig[order[a]]) {
                int t = order[a]; order[a] = order[b]; order[b] = t;
            }
        }
    }
    int nb = 0;
    for (int i = 0; i < n; ) {
        int j = i;
        ctx.bucket_sz[nb] = 0;
        while (j < n && ctx.sig[order[j]] == ctx.sig[order[i]]) {
            ctx.bucket_verts[nb][ctx.bucket_sz[nb]++] = order[j];
            ctx.pos_bucket[j] = nb;
            j++;
        }
        nb++;
        i = j;
    }
    canon_dfs(&ctx, 0, 0ULL);
    return ctx.best_code;
}

/* Open-addressing exact hash set for uint64_t canonical codes */
typedef struct {
    uint64_t *keys;
    uint8_t *used;
    size_t cap;
    size_t count;
} CodeSet;

static void codeset_init(CodeSet *s, size_t init_cap) {
    s->cap = 1;
    while (s->cap < init_cap) s->cap <<= 1;
    s->keys = (uint64_t *)malloc(s->cap * sizeof(uint64_t));
    s->used = (uint8_t *)calloc(s->cap, sizeof(uint8_t));
    s->count = 0;
}

static void codeset_free(CodeSet *s) {
    free(s->keys);
    free(s->used);
}

static inline uint64_t mix64(uint64_t x) {
    x ^= x >> 30; x *= 0xbf58476d1ce4e5b9ULL;
    x ^= x >> 27; x *= 0x94d049bb133111ebULL;
    x ^= x >> 31;
    return x;
}

static int codeset_insert(CodeSet *s, uint64_t key) {
    if ((s->count + 1) * 2 >= s->cap) {
        size_t ncap = s->cap * 2;
        uint64_t *nkeys = (uint64_t *)malloc(ncap * sizeof(uint64_t));
        uint8_t *nused = (uint8_t *)calloc(ncap, sizeof(uint8_t));
        for (size_t i = 0; i < s->cap; i++) {
            if (s->used[i]) {
                size_t idx = (size_t)(mix64(s->keys[i]) & (ncap - 1));
                while (nused[idx]) idx = (idx + 1) & (ncap - 1);
                nused[idx] = 1;
                nkeys[idx] = s->keys[i];
            }
        }
        free(s->keys);
        free(s->used);
        s->keys = nkeys;
        s->used = nused;
        s->cap = ncap;
    }
    size_t idx = (size_t)(mix64(key) & (s->cap - 1));
    while (s->used[idx]) {
        if (s->keys[idx] == key) return 0;
        idx = (idx + 1) & (s->cap - 1);
    }
    s->used[idx] = 1;
    s->keys[idx] = key;
    s->count++;
    return 1;
}

typedef struct {
    Graph *items;
    size_t len;
    size_t cap;
} GraphVec;

static void vec_push(GraphVec *v, const Graph *g) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 64;
        v->items = (Graph *)realloc(v->items, v->cap * sizeof(Graph));
    }
    v->items[v->len++] = *g;
}

static void decode_canon(int n, int m, uint64_t code, Graph *out) {
    memset(out, 0, sizeof(*out));
    out->code = code;
    out->n = (uint8_t)n;
    out->m = (uint8_t)m;
    int total_bits = (n * (n - 1)) / 2;
    for (int i = 1; i < n; i++) {
        int base_bit = total_bits - 1 - (i * (i - 1)) / 2;
        for (int j = 0; j < i; j++) {
            if ((code >> (base_bit - j)) & 1ULL) {
                out->adj[i] |= (uint16_t)(1 << j);
                out->adj[j] |= (uint16_t)(1 << i);
            }
        }
    }
}

static void print_edges(const Graph *g) {
    printf("[");
    int first = 1;
    for (int i = 0; i < g->n; i++) {
        for (int j = i + 1; j < g->n; j++) {
            if ((g->adj[i] >> j) & 1) {
                if (!first) printf(", ");
                printf("[%d, %d]", i, j);
                first = 0;
            }
        }
    }
    printf("]");
}

/* Extend graphs of size (n-1) with m_prev edges by adding vertex (n-1) of degree delta.
 * Enforces min degree >= delta in the resulting n-vertex graph so every G is generated
 * from G - v where v is a minimum-degree vertex of G. */
static void extend_bucket(
    int n,
    int delta,
    const GraphVec *prev_vec,
    CodeSet *seen,
    GraphVec *out_vec,
    int check_property
) {
    int prev_n = n - 1;
    int full = 1 << prev_n;
    for (size_t gi = 0; gi < prev_vec->len; gi++) {
        const Graph *gp = &prev_vec->items[gi];
        int pdeg[MAXN];
        int forced_mask = 0;
        int ok_base = 1;
        for (int u = 0; u < prev_n; u++) {
            pdeg[u] = __builtin_popcount((unsigned)gp->adj[u]);
            if (pdeg[u] < delta - 1) { ok_base = 0; break; }
            if (pdeg[u] == delta - 1) forced_mask |= (1 << u);
        }
        if (!ok_base) continue;
        int fc = __builtin_popcount((unsigned)forced_mask);
        if (fc > delta) continue;

        for (int mask = 0; mask < full; mask++) {
            if ((mask & forced_mask) != forced_mask) continue;
            if (__builtin_popcount((unsigned)mask) != delta) continue;

            uint16_t nadj[MAXN];
            memcpy(nadj, gp->adj, sizeof(nadj));
            nadj[prev_n] = (uint16_t)mask;
            for (int u = 0; u < prev_n; u++) {
                if ((mask >> u) & 1) nadj[u] |= (uint16_t)(1 << prev_n);
            }
            if (check_property && !is_valid_with_new_vertex(n, nadj)) continue;
            uint64_t code = canonical_code(n, nadj);
            if (codeset_insert(seen, code)) {
                Graph ng;
                decode_canon(n, gp->m + delta, code, &ng);
                vec_push(out_vec, &ng);
            }
        }
    }
}

int main(int argc, char **argv) {
    if (argc > 1 && strcmp(argv[1], "--test-canon") == 0) {
        GraphVec layers[7][16];
        memset(layers, 0, sizeof(layers));
        Graph g1; memset(&g1, 0, sizeof(g1)); g1.n = 1;
        vec_push(&layers[1][0], &g1);
        int a000088[] = {1, 1, 2, 4, 11, 34, 156};
        for (int n = 2; n <= 6; n++) {
            size_t tot = 0;
            int max_e = (n * (n - 1)) / 2;
            for (int m = 0; m <= max_e; m++) {
                CodeSet seen;
                codeset_init(&seen, 128);
                int max_d = (2 * m) / n;
                for (int d = 0; d <= max_d; d++) {
                    int mp = m - d;
                    if (mp < 0 || mp > ((n - 1) * (n - 2)) / 2) continue;
                    extend_bucket(n, d, &layers[n - 1][mp], &seen, &layers[n][m], 0);
                }
                tot += layers[n][m].len;
                codeset_free(&seen);
            }
            printf("n=%d unlabeled graphs: %zu (expected A000088: %d)\n", n, tot, a000088[n]);
            if ((int)tot != a000088[n]) return 2;
        }
        return 0;
    }

    int target_n = (argc > 1) ? atoi(argv[1]) : 9;
    if (target_n > 9) target_n = 9;

    /* Compute all valid unlabeled graphs for n <= 7 across all m,
     * m >= 13 for n = 8, and m >= 17 for n = 9.
     * Since for n = 9 and m in [17..22], delta <= floor(2*22/9) = 4, we always have
     * m - delta >= 17 - 4 = 13, so valid[8][13..17] is lossless for n = 9, m >= 17. */
    static GraphVec valid[MAXN + 1][46];
    memset(valid, 0, sizeof(valid));
    int f_exact[MAXN + 1];
    memset(f_exact, 0, sizeof(f_exact));

    Graph g1; memset(&g1, 0, sizeof(g1)); g1.n = 1;
    vec_push(&valid[1][0], &g1);
    f_exact[0] = 0;
    f_exact[1] = 0;

    for (int n = 2; n <= target_n; n++) {
        clock_t t0 = clock();
        int max_e = (n * (n - 1)) / 2;
        int min_m = 0;
        if (n == 8) min_m = 13;
        if (n == 9) min_m = 17;

        if (n <= 7) {
            for (int m = 0; m <= max_e; m++) {
                CodeSet seen;
                codeset_init(&seen, 256);
                int max_d = (2 * m) / n;
                int min_d = m - f_exact[n - 1];
                if (min_d < 0) min_d = 0;
                for (int d = min_d; d <= max_d; d++) {
                    int mp = m - d;
                    if (mp < 0 || mp > f_exact[n - 1]) continue;
                    extend_bucket(n, d, &valid[n - 1][mp], &seen, &valid[n][m], 1);
                }
                if (valid[n][m].len > 0) f_exact[n] = m;
                codeset_free(&seen);
            }
        } else {
            int m_upper = f_exact[n - 1] + (n - 1);
            for (int m = min_m; m <= max_e && m <= m_upper; m++) {
                int max_d = (2 * m) / n;
                int min_d = m - f_exact[n - 1];
                if (min_d < 0) min_d = 0;
                if (min_d > max_d) continue;
                CodeSet seen;
                codeset_init(&seen, 1024);
                for (int d = min_d; d <= max_d; d++) {
                    int mp = m - d;
                    if (mp < 0 || mp > f_exact[n - 1]) continue;
                    if (n == 9 && mp < 13) {
                        fprintf(stderr, "ERROR: needed mp=%d < min_m(8)=13\n", mp);
                        return 3;
                    }
                    extend_bucket(n, d, &valid[n - 1][mp], &seen, &valid[n][m], 1);
                }
                if (valid[n][m].len > 0) f_exact[n] = m;
                codeset_free(&seen);
                printf("  [n=%d m=%d] min_d=%d max_d=%d unique_valid=%zu\n", n, m, min_d, max_d, valid[n][m].len);
                fflush(stdout);
            }
        }
        double dt = (double)(clock() - t0) / CLOCKS_PER_SEC;
        printf("n=%d f_exact=%d (valid_at_f=%zu, time=%.3fs) witness=",
               n, f_exact[n], valid[n][f_exact[n]].len, dt);
        if (valid[n][f_exact[n]].len > 0) print_edges(&valid[n][f_exact[n]].items[0]);
        printf("\n");
        fflush(stdout);
    }
    return 0;
}
