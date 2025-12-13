#ifndef CMAPPY_H
#define CMAPPY_H

#include <stdlib.h>
#include <string.h>
#include <zlib.h>
#include "minimap.h"
#include "kseq.h"
#include "ksw2.h"

#include <stdint.h>

#include <ctype.h>
#include <stdio.h>

/* Define BAM op codes if htslib headers aren’t included earlier. */
#ifndef BAM_CMATCH
#define BAM_CMATCH      0
#define BAM_CINS        1
#define BAM_CDEL        2
#define BAM_CREF_SKIP   3
#define BAM_CSOFT_CLIP  4
#define BAM_CHARD_CLIP  5
#define BAM_CPAD        6
#define BAM_CEQUAL      7
#define BAM_CDIFF       8
#define BAM_CBACK       9
#endif
KSEQ_DECLARE(gzFile)










/* ---------- String builder ----------------------------------------------- */

typedef struct {
    char *data;
    size_t len;
    size_t cap;
} StrBuf;

static void fatal_oom(void) {
    fprintf(stderr, "Error: out of memory\n");
    exit(EXIT_FAILURE);
}

static void sb_init(StrBuf *sb) {
    sb->cap = 128;
    sb->len = 0;
    sb->data = (char *)malloc(sb->cap);
    if (!sb->data) fatal_oom();
    sb->data[0] = '\0';
}

static void sb_reserve(StrBuf *sb, size_t extra) {
    /* Prevent overflow before computing `needed = len + extra + 1`. */
    if (extra >= SIZE_MAX - sb->len) {
        fatal_oom();
    }
    size_t needed = sb->len + extra + 1;
    if (needed <= sb->cap) return;

    size_t new_cap = sb->cap ? sb->cap : 128;
    while (new_cap < needed) {
        if (new_cap > SIZE_MAX / 2) {
            fatal_oom();
        }
        new_cap *= 2;
    }

    char *tmp = (char *)realloc(sb->data, new_cap);
    if (!tmp) fatal_oom();
    sb->data = tmp;
    sb->cap = new_cap;
}

static void sb_append_char(StrBuf *sb, char c) {
    sb_reserve(sb, 1);
    sb->data[sb->len++] = c;
    sb->data[sb->len] = '\0';
}

static void sb_append_str(StrBuf *sb, const char *s) {
    size_t slen = strlen(s);
    sb_reserve(sb, slen);
    memcpy(sb->data + sb->len, s, slen);
    sb->len += slen;
    sb->data[sb->len] = '\0';
}

static void sb_append_size_t(StrBuf *sb, size_t value) {
    char buf[64];
    snprintf(buf, sizeof(buf), "%zu", value);
    sb_append_str(sb, buf);
}

static void sb_append_lowercase(StrBuf *sb, const char *s, size_t n) {
    sb_reserve(sb, n);
    for (size_t i = 0; i < n; ++i) {
        sb->data[sb->len++] = (char)tolower((unsigned char)s[i]);
    }
    sb->data[sb->len] = '\0';
}

static void sb_append_uppercase(StrBuf *sb, const char *s, size_t n) {
    sb_reserve(sb, n);
    for (size_t i = 0; i < n; ++i) {
        sb->data[sb->len++] = (char)toupper((unsigned char)s[i]);
    }
    sb->data[sb->len] = '\0';
}

static char *sb_detach(StrBuf *sb) {
    char *result = sb->data;
    sb->data = NULL;
    sb->len = sb->cap = 0;
    return result;
}

static void sb_free(StrBuf *sb) {
    if (sb->data) {
        free(sb->data);
        sb->data = NULL;
        sb->len = sb->cap = 0;
    }
}

/* ---------- Builder state ------------------------------------------------ */

typedef struct {
    int enabled;
    int initialized;
    size_t match_count;
    StrBuf buf;
} MDState;

typedef struct {
    int enabled;
    int initialized;
    size_t match_count;
    StrBuf buf;
} CSSState;

typedef struct {
    int enabled;
    int initialized;
    int in_match;
    StrBuf buf;
} CSLState;

static void md_state_init(MDState *state, int enabled) {
    state->enabled = enabled ? 1 : 0;
    state->initialized = 0;
    state->match_count = 0;
    if (state->enabled) {
        sb_init(&state->buf);
        state->initialized = 1;
    } else {
        state->buf.data = NULL;
        state->buf.len = state->buf.cap = 0;
    }
}

static void css_state_init(CSSState *state, int enabled) {
    state->enabled = enabled ? 1 : 0;
    state->initialized = 0;
    state->match_count = 0;
    if (state->enabled) {
        sb_init(&state->buf);
        state->initialized = 1;
    } else {
        state->buf.data = NULL;
        state->buf.len = state->buf.cap = 0;
    }
}

static void csl_state_init(CSLState *state, int enabled) {
    state->enabled = enabled ? 1 : 0;
    state->initialized = 0;
    state->in_match = 0;
    if (state->enabled) {
        sb_init(&state->buf);
        state->initialized = 1;
    } else {
        state->buf.data = NULL;
        state->buf.len = state->buf.cap = 0;
    }
}

static void md_emit_count(MDState *state) {
    if (!state->enabled) return;
    sb_append_size_t(&state->buf, state->match_count);
    state->match_count = 0;
}

static void css_flush_matches(CSSState *state) {
    if (!state->enabled || state->match_count == 0) return;
    sb_append_char(&state->buf, ':');
    sb_append_size_t(&state->buf, state->match_count);
    state->match_count = 0;
}

static void csl_end_match(CSLState *state) {
    if (!state->enabled) return;
    if (state->in_match) {
        state->in_match = 0;
    }
}

/* ---------- Match-block processor --------------------------------------- */

typedef enum {
    BLOCK_TYPE_M,
    BLOCK_TYPE_EQ,
    BLOCK_TYPE_X
} BlockType;

static int process_match_block(
    char op_char,
    BlockType block_type,
    size_t count,
    const char *ref,
    size_t ref_len,
    size_t *ref_idx,
    const char *query,
    size_t query_len,
    size_t *query_idx,
    MDState *md,
    CSSState *css,
    CSLState *csl,
    size_t *nm_count) {

    for (size_t i = 0; i < count; ++i) {
        if (*ref_idx >= ref_len) {
            fprintf(stderr,
                    "Error: reference exhausted while processing '%c'.\n",
                    op_char);
            return -1;
        }
        if (*query_idx >= query_len) {
            fprintf(stderr,
                    "Error: query exhausted while processing '%c'.\n",
                    op_char);
            return -1;
        }

        char ref_base = ref[*ref_idx];
        char qry_base = query[*query_idx];
        int actual_equal =
            (toupper((unsigned char)ref_base) ==
             toupper((unsigned char)qry_base)) ? 1 : 0;
        int is_match;

        if (block_type == BLOCK_TYPE_EQ) {
            if (!actual_equal) {
                fprintf(stderr,
                        "Error: '=' op mismatch at ref index %zu.\n",
                        *ref_idx);
                return -1;
            }
            is_match = 1;
        } else if (block_type == BLOCK_TYPE_X) {
            if (actual_equal) {
                fprintf(stderr,
                        "Error: 'X' op has identical bases at ref index %zu.\n",
                        *ref_idx);
                return -1;
            }
            is_match = 0;
        } else {
            is_match = actual_equal;
        }

        if (!actual_equal && nm_count) {
            if (*nm_count == SIZE_MAX) {
                fprintf(stderr, "Error: NM count overflow.\n");
                return -1;
            }
            (*nm_count)++;
        }

        if (is_match) {
            if (md->enabled) {
                if (md->match_count == SIZE_MAX) {
                    fprintf(stderr, "Error: MD match count overflow.\n");
                    return -1;
                }
                md->match_count++;
            }
            if (css->enabled) {
                if (css->match_count == SIZE_MAX) {
                    fprintf(stderr, "Error: CS match count overflow.\n");
                    return -1;
                }
                css->match_count++;
            }
            if (csl->enabled) {
                if (!csl->in_match) {
                    sb_append_char(&csl->buf, '=');
                    csl->in_match = 1;
                }
                sb_append_char(&csl->buf,
                               (char)tolower((unsigned char)ref_base));
            }
        } else {
            if (md->enabled) {
                md_emit_count(md);
                sb_append_char(&md->buf,
                               (char)toupper((unsigned char)ref_base));
            }
            if (css->enabled) {
                css_flush_matches(css);
                sb_append_char(&css->buf, '*');
                sb_append_char(&css->buf,
                               (char)tolower((unsigned char)ref_base));
                sb_append_char(&css->buf,
                               (char)tolower((unsigned char)qry_base));
            }
            if (csl->enabled) {
                csl_end_match(csl);
                sb_append_char(&csl->buf, '*');
                sb_append_char(&csl->buf,
                               (char)tolower((unsigned char)ref_base));
                sb_append_char(&csl->buf,
                               (char)tolower((unsigned char)qry_base));
            }
        }

        (*ref_idx)++;
        (*query_idx)++;
    }

    return 0;
}

/* ---------- Core builder ------------------------------------------------- */

static int build_tags(const char *cigar,
                      const char *ref,
                      const char *query,
                      int want_md,
                      int want_css_short,
                      int want_css_long,
                      char **md_out,
                      char **cs_short_out,
                      char **cs_long_out,
                      size_t *nm_out) {
    if (want_md && md_out == NULL) {
        fprintf(stderr, "Error: want_md requested but md_out is NULL.\n");
        return -1;
    }
    if (want_css_short && cs_short_out == NULL) {
        fprintf(stderr,
                "Error: want_css_short requested but cs_short_out is NULL.\n");
        return -1;
    }
    if (want_css_long && cs_long_out == NULL) {
        fprintf(stderr,
                "Error: want_css_long requested but cs_long_out is NULL.\n");
        return -1;
    }

    size_t ref_len = strlen(ref);
    size_t query_len = strlen(query);
    size_t ref_idx = 0;
    size_t query_idx = 0;
    size_t nm_count = 0;

    if (md_out) *md_out = NULL;
    if (cs_short_out) *cs_short_out = NULL;
    if (cs_long_out) *cs_long_out = NULL;
    if (nm_out) *nm_out = 0;

    if (cigar == NULL || cigar[0] == '\0') {
        fprintf(stderr, "Error: empty CIGAR string.\n");
        return -1;
    }

    MDState md = {0};
    CSSState css = {0};
    CSLState csl = {0};

    md_state_init(&md, want_md);
    css_state_init(&css, want_css_short);
    csl_state_init(&csl, want_css_long);

    const char *p = cigar;
    while (*p) {
        if (!isdigit((unsigned char)*p)) {
            fprintf(stderr, "Error: invalid CIGAR at '%s'.\n", p);
            goto error;
        }
        size_t count = 0;
        while (isdigit((unsigned char)*p)) {
            int digit = *p - '0';
            if (count > (SIZE_MAX - (size_t)digit) / 10) {
                fprintf(stderr, "Error: CIGAR count overflow.\n");
                goto error;
            }
            count = count * 10 + (size_t)digit;
            ++p;
        }
        if (count == 0 || *p == '\0') {
            fprintf(stderr, "Error: malformed CIGAR run.\n");
            goto error;
        }

        char op = *p++;
        switch (op) {
            case 'M':
                if (process_match_block('M', BLOCK_TYPE_M, count, ref,
                                        ref_len, &ref_idx, query, query_len,
                                        &query_idx, &md, &css, &csl,
                                        &nm_count) != 0) {
                    goto error;
                }
                break;
            case '=':
                if (process_match_block('=', BLOCK_TYPE_EQ, count, ref,
                                        ref_len, &ref_idx, query, query_len,
                                        &query_idx, &md, &css, &csl,
                                        &nm_count) != 0) {
                    goto error;
                }
                break;
            case 'X':
                if (process_match_block('X', BLOCK_TYPE_X, count, ref,
                                        ref_len, &ref_idx, query, query_len,
                                        &query_idx, &md, &css, &csl,
                                        &nm_count) != 0) {
                    goto error;
                }
                break;
            case 'I':
                if (query_idx > query_len || count > query_len - query_idx) {
                    fprintf(stderr,
                            "Error: query shorter than CIGAR 'I' span.\n");
                    goto error;
                }
                if (count > SIZE_MAX - nm_count) {
                    fprintf(stderr, "Error: NM count overflow.\n");
                    goto error;
                }
                nm_count += count;
                if (css.enabled) {
                    css_flush_matches(&css);
                    sb_append_char(&css.buf, '+');
                    sb_append_lowercase(&css.buf, query + query_idx, count);
                }
                if (csl.enabled) {
                    csl_end_match(&csl);
                    sb_append_char(&csl.buf, '+');
                    sb_append_lowercase(&csl.buf, query + query_idx, count);
                }
                query_idx += count;
                break;
            case 'D':
                if (ref_idx > ref_len || count > ref_len - ref_idx) {
                    fprintf(stderr,
                            "Error: reference shorter than CIGAR 'D' span.\n");
                    goto error;
                }
                if (count > SIZE_MAX - nm_count) {
                    fprintf(stderr, "Error: NM count overflow.\n");
                    goto error;
                }
                nm_count += count;
                if (md.enabled) {
                    md_emit_count(&md);
                    sb_append_char(&md.buf, '^');
                    sb_append_uppercase(&md.buf, ref + ref_idx, count);
                }
                if (css.enabled) {
                    css_flush_matches(&css);
                    sb_append_char(&css.buf, '-');
                    sb_append_lowercase(&css.buf, ref + ref_idx, count);
                }
                if (csl.enabled) {
                    csl_end_match(&csl);
                    sb_append_char(&csl.buf, '-');
                    sb_append_lowercase(&csl.buf, ref + ref_idx, count);
                }
                ref_idx += count;
                break;
            case 'N':
                if (ref_idx > ref_len || count > ref_len - ref_idx) {
                    fprintf(stderr,
                            "Error: reference shorter than CIGAR 'N' span.\n");
                    goto error;
                }
                if (count > SIZE_MAX - nm_count) {
                    fprintf(stderr, "Error: NM count overflow.\n");
                    goto error;
                }
                nm_count += count;
                if (md.enabled) {
                    md_emit_count(&md);
                    sb_append_char(&md.buf, '^');
                    sb_append_uppercase(&md.buf, ref + ref_idx, count);
                }
                if (css.enabled) {
                    css_flush_matches(&css);
                    sb_append_char(&css.buf, '~');
                    sb_append_size_t(&css.buf, count);
                }
                if (csl.enabled) {
                    csl_end_match(&csl);
                    sb_append_char(&csl.buf, '~');
                    sb_append_size_t(&csl.buf, count);
                }
                ref_idx += count;
                break;
            case 'S':
                if (query_idx > query_len || count > query_len - query_idx) {
                    fprintf(stderr,
                            "Error: query shorter than CIGAR 'S' span.\n");
                    goto error;
                }
                query_idx += count;
                break;
            case 'H':
            case 'P':
                break;
            default:
                fprintf(stderr, "Error: unsupported CIGAR op '%c'.\n", op);
                goto error;
        }
    }

    if (ref_idx != ref_len) {
        fprintf(stderr,
                "Error: reference length mismatch (consumed %zu of %zu).\n",
                ref_idx, ref_len);
        goto error;
    }
    if (query_idx != query_len) {
        fprintf(stderr,
                "Error: query length mismatch (consumed %zu of %zu).\n",
                query_idx, query_len);
        goto error;
    }

    if (want_md) {
        md_emit_count(&md);
        *md_out = sb_detach(&md.buf);
        md.initialized = 0;
    }
    if (want_css_short) {
        css_flush_matches(&css);
        *cs_short_out = sb_detach(&css.buf);
        css.initialized = 0;
    }
    if (want_css_long) {
        csl_end_match(&csl);
        *cs_long_out = sb_detach(&csl.buf);
        csl.initialized = 0;
    }
    if (nm_out) {
        *nm_out = nm_count;
    }

    if (md.initialized) sb_free(&md.buf);
    if (css.initialized) sb_free(&css.buf);
    if (csl.initialized) sb_free(&csl.buf);
    return 0;

error:
    if (md.initialized) sb_free(&md.buf);
    if (css.initialized) sb_free(&css.buf);
    if (csl.initialized) sb_free(&csl.buf);
    return -1;
}

    
    
typedef struct {
    const char *ctg;
    int32_t ctg_start, ctg_end;
    int32_t qry_start, qry_end;
    int32_t blen, mlen, NM, ctg_len;
    uint8_t mapq, is_primary;
    int8_t strand, trans_strand;
    int32_t seg_id;
    int32_t n_cigar32;
    uint32_t *cigar32;
} mm_hitpy_t;

static inline void mm_reg2hitpy(const mm_idx_t *mi, mm_reg1_t *r, mm_hitpy_t *h)
{
    h->ctg = mi->seq[r->rid].name;
    h->ctg_len = mi->seq[r->rid].len;
    h->ctg_start = r->rs, h->ctg_end = r->re;
    h->qry_start = r->qs, h->qry_end = r->qe;
    h->strand = r->rev? -1 : 1;
    h->mapq = r->mapq;
    h->mlen = r->mlen;
    h->blen = r->blen;
    h->NM = r->blen - r->mlen + r->p->n_ambi;
    h->trans_strand = r->p->trans_strand == 1? 1 : r->p->trans_strand == 2? -1 : 0;
    h->is_primary = (r->id == r->parent);
    h->seg_id = r->seg_id;
    h->n_cigar32 = r->p->n_cigar;
    h->cigar32 = r->p->cigar;
}

static inline void mm_free_reg1(mm_reg1_t *r)
{
    free(r->p);
}

static inline kseq_t *mm_fastx_open(const char *fn)
{
    gzFile fp;
    fp = fn && strcmp(fn, "-") != 0? gzopen(fn, "r") : gzdopen(fileno(stdin), "r");
    return kseq_init(fp);
}

static inline void mm_fastx_close(kseq_t *ks)
{
    gzFile fp;
    fp = ks->f->f;
    kseq_destroy(ks);
    gzclose(fp);
}

static inline int mm_verbose_level(int v)
{
    if (v >= 0) mm_verbose = v;
    return mm_verbose;
}

static inline void mm_reset_timer(void)
{
    extern double realtime(void);
    mm_realtime0 = realtime();
}

extern unsigned char seq_comp_table[256];
static inline s_mm128_t *mm_map_aux(const mm_idx_t *mi, const char *seq1, const char *seq2, int *n_regs, mm_tbuf_t *b, const mm_mapopt_t *opt, int *n_aa)
{
    mm_reg1_t *r;
    s_mm128_t *aa;

    Py_BEGIN_ALLOW_THREADS

    int qlen=strlen(seq1);   
    aa = mm_map_frag_(mi, 1, &qlen, &seq1, n_regs, &r, b, opt, NULL, n_aa);


    Py_END_ALLOW_THREADS
    return aa;
}


static uint32_t *mappy_convert_to_eqx(const uint32_t *cigar,
                                      int n_cigar,
                                      const uint8_t *target,
                                      const uint8_t *query,
                                      int tl,
                                      int ql,
                                      int *n_out)
{
    if (n_cigar <= 0 || !cigar || !target || !query) {
        *n_out = 0;
        return NULL;
    }

    /* Worst case: every base inside an M becomes its own op. */
    int max_ops = ql + n_cigar + 8;
    if (max_ops < n_cigar) max_ops = n_cigar + 8;

    uint32_t *buf = (uint32_t *)malloc((size_t)max_ops * sizeof(uint32_t));
    if (!buf) {
        *n_out = 0;
        return NULL;
    }

    int qpos = 0;
    int tpos = 0;
    int out_n = 0;

    for (int i = 0; i < n_cigar; ++i) {
        const uint32_t entry = cigar[i];
        const int len = (int)(entry >> 4);
        const int op = (int)(entry & 0xF);

        switch (op) {
        case BAM_CMATCH: {
            int run_len = 0;
            int cur_op = -1;

            for (int k = 0; k < len; ++k) {
                if (qpos >= ql || tpos >= tl) {
                    free(buf);
                    *n_out = 0;
                    return NULL;
                }
                const int next_op = (query[qpos] == target[tpos]) ? BAM_CEQUAL : BAM_CDIFF;

                if (next_op == cur_op) {
                    ++run_len;
                } else {
                    if (run_len > 0) {
                        buf[out_n++] = (uint32_t)((run_len << 4) | cur_op);
                    }
                    cur_op = next_op;
                    run_len = 1;
                }
                ++qpos;
                ++tpos;
            }
            if (run_len > 0) {
                buf[out_n++] = (uint32_t)((run_len << 4) | cur_op);
            }
            break;
        }

        case BAM_CEQUAL:
        case BAM_CDIFF:
            if (qpos + len > ql || tpos + len > tl) {
                free(buf);
                *n_out = 0;
                return NULL;
            }
            buf[out_n++] = entry;
            qpos += len;
            tpos += len;
            break;

        case BAM_CINS:
        case BAM_CSOFT_CLIP:
            if (qpos + len > ql) {
                free(buf);
                *n_out = 0;
                return NULL;
            }
            buf[out_n++] = entry;
            qpos += len;
            break;

        case BAM_CDEL:
        case BAM_CREF_SKIP:
            if (tpos + len > tl) {
                free(buf);
                *n_out = 0;
                return NULL;
            }
            buf[out_n++] = entry;
            tpos += len;
            break;

        case BAM_CHARD_CLIP:
        case BAM_CPAD:
        case BAM_CBACK:
        default:
            buf[out_n++] = entry; /* No coordinate movement. */
            break;
        }
    }

    /* Optionally shrink to fit. */
    //uint32_t *tight = (uint32_t *)realloc(buf, (size_t)out_n * sizeof(uint32_t));
    //if (tight) buf = tight;

    *n_out = out_n;
    return buf;
}

static inline uint32_t *mappy_k_cigar(const uint8_t *target,
                                      const uint8_t *query,
                                      int *n_cigarcode,
                                      int *zdropped,
                                      int *max_q,
                                      int *max_t,
                                      int match,
                                      int mismatch,
                                      int gap_open_1,
                                      int gap_extend_1,
                                      int gap_open_2,
                                      int gap_extend_2,
                                      int bw,
                                      int zdropvalue,
                                      int *delcount,
                                      int *inscount,
                                      int eqx)
{
    int i;
    const int a = match;
    const int b = mismatch;
    extern unsigned char seq_nt4_table[256];
    int8_t mat[25] = {
        a, b, b, b, 0,
        b, a, b, b, 0,
        b, b, a, b, 0,
        b, b, b, a, 0,
        0, 0, 0, 0, 0
    };
    const int tl = (int)strlen((const char *)target);
    const int ql = (int)strlen((const char *)query);
    uint8_t *ts = NULL;
    uint8_t *qs = NULL;
    ksw_extz_t ez;

    memset(&ez, 0, sizeof(ksw_extz_t));
    *n_cigarcode = 0;

    ts = (uint8_t *)malloc((size_t)tl);
    qs = (uint8_t *)malloc((size_t)ql);
    if (!ts || !qs) {
        free(ts);
        free(qs);
        return NULL;
    }

    for (i = 0; i < tl; ++i) ts[i] = seq_nt4_table[target[i]];
    for (i = 0; i < ql; ++i) qs[i] = seq_nt4_table[query[i]];

    ksw_extd2_sse(0, ql, qs, tl, ts, 5, mat,
                  gap_open_1, gap_extend_1,
                  gap_open_2, gap_extend_2,
                  bw, zdropvalue, 0, 0, &ez);

    uint32_t *result = ez.cigar;

    if (eqx && ez.n_cigar > 0 && result) {
        int new_n = ez.n_cigar;
        uint32_t *converted = mappy_convert_to_eqx(result, ez.n_cigar,
                                                   target, query, tl, ql, &new_n);
        if (converted) {
            free(result);
            result = converted;
            ez.n_cigar = new_n;
        }
    }

    *n_cigarcode = ez.n_cigar;
    *zdropped = ez.zdropped;
    *max_q = ez.max_q;
    *max_t = ez.max_t;

    free(ts);
    free(qs);

    /* Caller is still responsible for freeing the returned CIGAR. */
    return result;
}



static inline void mm_kfree(void *km, void *ptr)
{
    kfree(km, ptr);
}

static inline char *mappy_revcomp(int len, const uint8_t *seq)
{
    int i;
    char *rev;
    rev = (char*)malloc(len + 1);
    for (i = 0; i < len; ++i)
        rev[len - i - 1] = seq_comp_table[seq[i]];
    rev[len] = 0;
    return rev;
}

static char *mappy_fetch_seq(const mm_idx_t *mi, const char *name, int st, int en, int *len)
{
    int i, rid;
    char *s;
    *len = 0;
    rid = mm_idx_name2id(mi, name);
    if (rid < 0) return 0;
    if ((uint32_t)st >= mi->seq[rid].len || st >= en) return 0;
    if (en < 0 || (uint32_t)en > mi->seq[rid].len)
        en = mi->seq[rid].len;
    s = (char*)malloc(en - st + 1);
    *len = mm_idx_getseq(mi, rid, st, en, (uint8_t*)s);
    for (i = 0; i < *len; ++i)
        s[i] = "ACGTN"[(uint8_t)s[i]];
    s[*len] = 0;
    return s;
}

static mm_idx_t *mappy_idx_seq(int w, int k, int is_hpc, int bucket_bits, const char *seq, int len)
{
    const char *fake_name = "N/A";
    char *s;
    mm_idx_t *mi;
    s = (char*)calloc(len + 1, 1);
    memcpy(s, seq, len);
    mi = mm_idx_str(w, k, is_hpc, bucket_bits, 1, (const char**)&s, (const char**)&fake_name);
    free(s);
    return mi;
}

#endif
