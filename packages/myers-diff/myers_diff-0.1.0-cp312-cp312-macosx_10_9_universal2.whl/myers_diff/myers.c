#include "myers.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

static inline unsigned long hash_str(const char *s) {
    unsigned long h = 0;
    while (*s) h = h * 31 + (unsigned char)*s++;
    return h;
}

int myers_distance(const char **a, int n, const char **b, int m) {
    if (!n) return m;
    if (!m) return n;
    unsigned long *ha = malloc(n * sizeof(unsigned long));
    unsigned long *hb = malloc(m * sizeof(unsigned long));
    for (int i = 0; i < n; i++) ha[i] = hash_str(a[i]);
    for (int i = 0; i < m; i++) hb[i] = hash_str(b[i]);
    int pf = 0, sf = 0;
    while (pf < n && pf < m && ha[pf] == hb[pf]) pf++;
    while (sf < n - pf && sf < m - pf && ha[n-1-sf] == hb[m-1-sf]) sf++;
    int la = n - pf - sf, lb = m - pf - sf;
    if (!la) { free(ha); free(hb); return lb; }
    if (!lb) { free(ha); free(hb); return la; }
    unsigned long *pa = ha + pf, *pb = hb + pf;
    int *curr = malloc((lb + 1) * sizeof(int));
    int *prev = malloc((lb + 1) * sizeof(int));
    for (int j = 0; j <= lb; j++) prev[j] = j;
    for (int i = 1; i <= la; i++) {
        curr[0] = i;
        unsigned long hai = pa[i - 1];
        for (int j = 1; j <= lb; j++) {
            if (hai == pb[j - 1]) curr[j] = prev[j - 1];
            else curr[j] = 1 + (prev[j] < curr[j - 1] ? prev[j] : curr[j - 1]);
        }
        int *tmp = prev; prev = curr; curr = tmp;
    }
    int dist = prev[lb];
    free(curr); free(prev); free(ha); free(hb);
    return dist;
}

EditScript *myers_diff(const char **a, int n, const char **b, int m, int max_d) {
    EditScript *s = malloc(sizeof(EditScript));
    s->ops = NULL; s->count = 0; s->capacity = 0; s->exceeded = 0;
    if (!n && !m) return s;
    if (!n) {
        if (max_d >= 0 && m > max_d) { s->exceeded = 1; return s; }
        s->capacity = m; s->ops = malloc(m * sizeof(EditOperation));
        for (int i = 0; i < m; i++) s->ops[s->count++] = (EditOperation){OP_INSERT, i, b[i]};
        return s;
    }
    if (!m) {
        if (max_d >= 0 && n > max_d) { s->exceeded = 1; return s; }
        s->capacity = n; s->ops = malloc(n * sizeof(EditOperation));
        for (int i = 0; i < n; i++) s->ops[s->count++] = (EditOperation){OP_DELETE, i, a[i]};
        return s;
    }
    unsigned long *ha = malloc(n * sizeof(unsigned long));
    unsigned long *hb = malloc(m * sizeof(unsigned long));
    for (int i = 0; i < n; i++) ha[i] = hash_str(a[i]);
    for (int i = 0; i < m; i++) hb[i] = hash_str(b[i]);
    int pf = 0, sf = 0;
    while (pf < n && pf < m && ha[pf] == hb[pf]) pf++;
    while (sf < n - pf && sf < m - pf && ha[n-1-sf] == hb[m-1-sf]) sf++;
    int sa = pf, sb = pf, la = n - pf - sf, lb = m - pf - sf;
    if (!la && !lb) { free(ha); free(hb); return s; }
    if (!la) {
        if (max_d >= 0 && lb > max_d) { s->exceeded = 1; free(ha); free(hb); return s; }
        s->capacity = lb; s->ops = malloc(lb * sizeof(EditOperation));
        for (int i = 0; i < lb; i++) s->ops[s->count++] = (EditOperation){OP_INSERT, sb + i, b[sb + i]};
        free(ha); free(hb); return s;
    }
    if (!lb) {
        if (max_d >= 0 && la > max_d) { s->exceeded = 1; free(ha); free(hb); return s; }
        s->capacity = la; s->ops = malloc(la * sizeof(EditOperation));
        for (int i = 0; i < la; i++) s->ops[s->count++] = (EditOperation){OP_DELETE, sa + i, a[sa + i]};
        free(ha); free(hb); return s;
    }
    unsigned long *pa = ha + sa, *pb = hb + sb;
    int full_max_d = la + lb;
    int limit_d = (max_d >= 0 && max_d < full_max_d) ? max_d : full_max_d;
    int vs = 2 * full_max_d + 1, off = full_max_d;
    int *v = malloc(vs * sizeof(int));
    size_t trsz = 0;
    for (int d = 0; d <= limit_d; d++) trsz += 2 * d + 1;
    int *tr = malloc(trsz * sizeof(int));
    size_t toff = 0;
    for (int i = 0; i < vs; i++) v[i] = -1;
    v[off + 1] = 0;
    int fd = -1;
    for (int d = 0; d <= limit_d; d++) {
        int w = 2 * d + 1;
        memcpy(tr + toff, v + off - d, w * sizeof(int));
        toff += w;
        for (int k = -d; k <= d; k += 2) {
            int x = (k == -d || (k != d && v[off+k-1] < v[off+k+1])) ? v[off+k+1] : v[off+k-1] + 1;
            int y = x - k;
            while (x < la && y < lb && pa[x] == pb[y]) { x++; y++; }
            v[off + k] = x;
            if (x >= la && y >= lb) { fd = d; goto found; }
        }
    }
    s->exceeded = 1;
    free(v); free(tr); free(ha); free(hb);
    return s;
found:
    if (fd >= 0) {
        s->capacity = fd; s->ops = malloc(fd * sizeof(EditOperation));
        size_t ti = toff;
        int x = la, y = lb;
        for (int d = fd; d > 0; d--) {
            int w = 2 * d + 1;
            ti -= w;
            int *pv = tr + ti;
            int k = x - y;
            int vkm1 = (k - 1 >= -d) ? pv[d + k - 1] : -2;
            int vkp1 = (k + 1 <= d) ? pv[d + k + 1] : -2;
            int pk = (k == -d || (k != d && vkm1 < vkp1)) ? k + 1 : k - 1;
            int px = pv[d + pk], py = px - pk;
            while (x > px && y > py) { x--; y--; }
            if (x == px && y > py) { y--; s->ops[s->count].type = OP_INSERT; s->ops[s->count].index = sb + y; s->ops[s->count++].line = b[sb + y]; }
            else if (y == py && x > px) { x--; s->ops[s->count].type = OP_DELETE; s->ops[s->count].index = sa + x; s->ops[s->count++].line = a[sa + x]; }
            x = px; y = py;
        }
        for (int i = 0, j = s->count - 1; i < j; i++, j--) { EditOperation t = s->ops[i]; s->ops[i] = s->ops[j]; s->ops[j] = t; }
    }
    free(v); free(tr); free(ha); free(hb);
    return s;
}

void free_edit_script(EditScript *s) { if (s) { free(s->ops); free(s); } }

void print_edit_script(EditScript *s) {
    printf("Edit operations (%d total):\n", s->count);
    for (int i = 0; i < s->count; i++)
        printf("  %s [%d]: \"%s\"\n", s->ops[i].type == OP_DELETE ? "DELETE" : "INSERT", s->ops[i].index, s->ops[i].line);
}
