from libc.stdint cimport uint8_t, int8_t
from libc.stdlib cimport free
cimport cmappy
import sys

import ctypes
from ctypes import c_char_p, c_int, c_uint32, c_uint8, POINTER
from cpython.unicode cimport PyUnicode_FromString


# BAM op → character mapping
_CIGAR_OPS = "MIDNSHP=XB"

__version__ = '2.28'

cmappy.mm_reset_timer()

cdef class Alignment:
    cdef int _ctg_len, _r_st, _r_en
    cdef int _q_st, _q_en
    cdef int _NM, _mlen, _blen
    cdef int8_t _strand, _trans_strand
    cdef uint8_t _mapq, _is_primary
    cdef int _seg_id
    cdef _ctg, _cigar, _cs, _MD # these are python objects

    def __cinit__(self, ctg, cl, cs, ce, strand, qs, qe, mapq, cigar, is_primary, mlen, blen, NM, trans_strand, seg_id, cs_str, MD_str):
        self._ctg = ctg if isinstance(ctg, str) else ctg.decode()
        self._ctg_len, self._r_st, self._r_en = cl, cs, ce
        self._strand, self._q_st, self._q_en = strand, qs, qe
        self._NM, self._mlen, self._blen = NM, mlen, blen
        self._mapq = mapq
        self._cigar = cigar
        self._is_primary = is_primary
        self._trans_strand = trans_strand
        self._seg_id = seg_id
        self._cs = cs_str
        self._MD = MD_str

    @property
    def ctg(self): return self._ctg

    @property
    def ctg_len(self): return self._ctg_len

    @property
    def r_st(self): return self._r_st

    @property
    def r_en(self): return self._r_en

    @property
    def strand(self): return self._strand

    @property
    def trans_strand(self): return self._trans_strand

    @property
    def blen(self): return self._blen

    @property
    def mlen(self): return self._mlen

    @property
    def NM(self): return self._NM

    @property
    def is_primary(self): return (self._is_primary != 0)

    @property
    def q_st(self): return self._q_st

    @property
    def q_en(self): return self._q_en

    @property
    def mapq(self): return self._mapq

    @property
    def cigar(self): return self._cigar

    @property
    def read_num(self): return self._seg_id + 1

    @property
    def cs(self): return self._cs

    @property
    def MD(self): return self._MD

    @property
    def cigar_str(self):
        return "".join(map(lambda x: str(x[0]) + 'MIDNSHP=XB'[x[1]], self._cigar))

    def __str__(self):
        if self._strand > 0: strand = '+'
        elif self._strand < 0: strand = '-'
        else: strand = '?'
        if self._is_primary != 0: tp = 'tp:A:P'
        else: tp = 'tp:A:S'
        if self._trans_strand > 0: ts = 'ts:A:+'
        elif self._trans_strand < 0: ts = 'ts:A:-'
        else: ts = 'ts:A:.'
        a = [str(self._q_st), str(self._q_en), strand, self._ctg, str(self._ctg_len), str(self._r_st), str(self._r_en),
            str(self._mlen), str(self._blen), str(self._mapq), tp, ts, "cg:Z:" + self.cigar_str]
        if self._cs != "": a.append("cs:Z:" + self._cs)
        if self._MD != "": a.append("MD:Z:" + self._MD)
        return "\t".join(a)

cdef class ThreadBuffer:
    cdef cmappy.mm_tbuf_t *_b

    def __cinit__(self):
        self._b = cmappy.mm_tbuf_init()

    def __dealloc__(self):
        cmappy.mm_tbuf_destroy(self._b)

cdef class Aligner:
    cdef cmappy.mm_idx_t *_idx
    cdef cmappy.mm_idxopt_t idx_opt
    cdef cmappy.mm_mapopt_t map_opt

    def __cinit__(self, fn_idx_in=None, preset=None, k=None, w=None, min_cnt=None, min_chain_score=None, min_dp_score=None, bw=None, bw_long=None, best_n=None, n_threads=3, fn_idx_out=None, max_frag_len=None, extra_flags=None, seq=None, scoring=None):
        self._idx = NULL
        cmappy.mm_set_opt(NULL, &self.idx_opt, &self.map_opt) # set the default options
        if preset is not None:
            cmappy.mm_set_opt(str.encode(preset), &self.idx_opt, &self.map_opt) # apply preset
        self.map_opt.flag |= 4 # always perform alignment
        self.idx_opt.batch_size = 0x7fffffffffffffffL # always build a uni-part index
        if k is not None: self.idx_opt.k = k
        if w is not None: self.idx_opt.w = w
        if min_cnt is not None: self.map_opt.min_cnt = min_cnt
        if min_chain_score is not None: self.map_opt.min_chain_score = min_chain_score
        if min_dp_score is not None: self.map_opt.min_dp_max = min_dp_score
        if bw is not None: self.map_opt.bw = bw
        if bw_long is not None: self.map_opt.bw_long = bw_long
        if best_n is not None: self.map_opt.best_n = best_n
        if max_frag_len is not None: self.map_opt.max_frag_len = max_frag_len
        if extra_flags is not None: self.map_opt.flag |= extra_flags
        if scoring is not None and len(scoring) >= 4:
            self.map_opt.a, self.map_opt.b = scoring[0], scoring[1]
            self.map_opt.q, self.map_opt.e = scoring[2], scoring[3]
            self.map_opt.q2, self.map_opt.e2 = self.map_opt.q, self.map_opt.e
            if len(scoring) >= 6:
                self.map_opt.q2, self.map_opt.e2 = scoring[4], scoring[5]
                if len(scoring) >= 7:
                    self.map_opt.sc_ambi = scoring[6]

        cdef cmappy.mm_idx_reader_t *r;

        if seq is None:
            if fn_idx_out is None:
                r = cmappy.mm_idx_reader_open(str.encode(fn_idx_in), &self.idx_opt, NULL)
            else:
                r = cmappy.mm_idx_reader_open(str.encode(fn_idx_in), &self.idx_opt, str.encode(fn_idx_out))
            if r is not NULL:
                self._idx = cmappy.mm_idx_reader_read(r, n_threads) # NB: ONLY read the first part
                cmappy.mm_idx_reader_close(r)
                cmappy.mm_mapopt_update(&self.map_opt, self._idx)
                cmappy.mm_idx_index_name(self._idx)
        else:
            self._idx = cmappy.mappy_idx_seq(self.idx_opt.w, self.idx_opt.k, self.idx_opt.flag&1, self.idx_opt.bucket_bits, str.encode(seq), len(seq))
            cmappy.mm_mapopt_update(&self.map_opt, self._idx)
            self.map_opt.mid_occ = 1000 # don't filter high-occ seeds

    def __dealloc__(self):
        if self._idx is not NULL:
            cmappy.mm_idx_destroy(self._idx)

    def __bool__(self):
        return (self._idx != NULL)

    def map(self, seq, check_num = 20, mid_occ = -1):
        cdef cmappy.mm_reg1_t *regs
        cdef cmappy.s_mm128_t *aa
        cdef cmappy.mm_hitpy_t h
        cdef ThreadBuffer b
        cdef int n_regs
        cdef void *km
        cdef cmappy.mm_mapopt_t map_opt
        cdef int n_aa = check_num, x_base 
        cdef int kmersize  
        cdef int pstrand = 1
        cdef int nstrand = -1
        cdef int i
        map_opt = self.map_opt   
        if(mid_occ != -1 and mid_occ > 0):
            map_opt.mid_occ = mid_occ
        if self._idx is NULL: return None
        b = ThreadBuffer()
        km = cmappy.mm_tbuf_get_km(b._b)
        _seq = seq if isinstance(seq, bytes) else seq.encode()
        aa = cmappy.mm_map_aux(self._idx, _seq, NULL,  &n_regs, b._b, &map_opt, &n_aa)
        kmersize = int(self._idx.k)
        ee = []
        for i in range(n_aa):
            if(aa[i].x < 0):
                ee.append((aa[i].y, abs(aa[i].x), nstrand, kmersize))
            else:
                ee.append((aa[i].y, aa[i].x, pstrand, kmersize))
        cmappy.mm_kfree(km, aa)
        return ee

    def seq(self, str name, int start=0, int end=0x7fffffff):
        cdef int l
        cdef char *s
        if self._idx == NULL: return
        s = cmappy.mappy_fetch_seq(self._idx, name.encode(), start, end, &l)
        if l == 0: return None
        r = s[:l] if isinstance(s, str) else s[:l].decode()
        free(s)
        return r.upper()

    @property
    def k(self): return self._idx.k

    @property
    def w(self): return self._idx.w

    @property
    def n_seq(self): return self._idx.n_seq

    @property
    def seq_names(self):
        cdef char *p
        if self._idx == NULL: return
        sn = []
        for i in range(self._idx.n_seq):
            p = self._idx.seq[i].name
            s = p if isinstance(p, str) else p.decode()
            sn.append(s)
        return sn

    @property
    def seq_offset(self):
        cdef char *p
        if self._idx == NULL: return
        sn = []
        for i in range(self._idx.n_seq):
            sn.append((self._idx.seq[i].name, self._idx.seq[i].len, self._idx.seq[i].offset))
        return sn

def fastx_read(fn, read_comment=False):
    cdef cmappy.kseq_t *ks
    ks = cmappy.mm_fastx_open(str.encode(fn))
    if ks is NULL: return None
    while cmappy.kseq_read(ks) >= 0:
        if ks.qual.l > 0: qual = ks.qual.s if isinstance(ks.qual.s, str) else ks.qual.s.decode()
        else: qual = None
        name = ks.name.s if isinstance(ks.name.s, str) else ks.name.s.decode()
        seq = ks.seq.s if isinstance(ks.seq.s, str) else ks.seq.s.decode()
        if read_comment:
            if ks.comment.l > 0: comment = ks.comment.s if isinstance(ks.comment.s, str) else ks.comment.s.decode()
            else: comment = None
            yield name, seq, qual, comment
        else:
            yield name, seq, qual
    cmappy.mm_fastx_close(ks)



def _as_c_string(seq):
    """Ensure input is NUL-terminated bytes."""
    if isinstance(seq, str):
        return seq.encode("ascii")
    if isinstance(seq, bytes):
        return seq
    raise TypeError("target/query must be str or bytes")




def k_md_cs(cigar,
            target,
            query,
            want_md,
            want_css_short,
            want_css_long):
    """
    Call cmappy.build_tags and return (MD, cs_short, cs_long) strings.
    Strings are empty when the corresponding flag is False.
    """
    #if(want_md == want_css_short == want_css_long == False):
        #return '', '', ''
    target_c = _as_c_string(target)
    query_c = _as_c_string(query)
    cigar_c = _as_c_string(cigar)

    cdef bint want_md_b = bool(want_md)
    cdef bint want_css_short_b = bool(want_css_short)
    cdef bint want_css_long_b = bool(want_css_long)

    cdef char *md_tag = NULL
    cdef char *cs_short = NULL
    cdef char *cs_long = NULL
    cdef size_t nm_out = 0;
    
    
    cdef int status = cmappy.build_tags(
        cigar_c,
        target_c,
        query_c,
        want_md_b,
        want_css_short_b,
        want_css_long_b,
        &md_tag,
        &cs_short,
        &cs_long,
        &nm_out
    )

    if status != 0:
        if md_tag != NULL:
            free(md_tag)
        if cs_short != NULL:
            free(cs_short)
        if cs_long != NULL:
            free(cs_long)
        raise RuntimeError("cmappy.build_tags failed")

    try:
        if want_md_b:
            if md_tag == NULL:
                raise RuntimeError("cmappy.build_tags returned NULL md_tag")
            md_string = PyUnicode_FromString(md_tag)
        else:
            md_string = ""
        if want_css_short_b:
            if cs_short == NULL:
                raise RuntimeError("cmappy.build_tags returned NULL cs_short")
            cs_short_string = PyUnicode_FromString(cs_short)
        else:
            cs_short_string = ""
        if want_css_long_b:
            if cs_long == NULL:
                raise RuntimeError("cmappy.build_tags returned NULL cs_long")
            cs_long_string = PyUnicode_FromString(cs_long)
        else:
            cs_long_string = ""
        return md_string, cs_short_string, cs_long_string, nm_out
    finally:
        if md_tag != NULL:
            free(md_tag)
        if cs_short != NULL:
            free(cs_short)
        if cs_long != NULL:
            free(cs_long)


def k_cigar(
    target,
    query,
    match=2,
    mismatch=-4,
    gap_open_1=4,
    gap_extend_1=2,
    gap_open_2=24,
    gap_extend_2=1,
    bw=500,
    zdropvalue=400,
    eqx=False,
):
    """
    Call mappy_k_cigar() and return a CIGAR string (optionally with =/X ops).

    Parameters mirror the C function; target/query can be str or bytes.
    """
    #cdef uint32_t *cigarcode;
    cdef int n_cigar = 0, zdropped = 0, max_q = 0, max_t = 0, delcount = 0, inscount = 0
    if(max(len(target), len(query)) > 500000):
        return '', 1, 0, 0, 999, 999

    target_c = _as_c_string(target)
    query_c = _as_c_string(query)


    cigar_ptr = cmappy.mappy_k_cigar(
        target_c,
        query_c,
        (&n_cigar),
        (&zdropped),
        (&max_q),
        (&max_t),
        (match),
        (mismatch),
        (gap_open_1),
        (gap_extend_1),
        (gap_open_2),
        (gap_extend_2),
        (bw),
        (zdropvalue),
        (&delcount),
        (&inscount),
        (1 if eqx else 0),
    )

    try:
        count = n_cigar
        if not cigar_ptr or count == 0:
            return '', 1, 0, 0, 999, 999

        parts = []
        for i in range(count):
            entry = cigar_ptr[i]
            length = entry >> 4
            op = entry & 0xF
            if op >= len(_CIGAR_OPS):
                raise ValueError(f"Unknown CIGAR op code: {op}")
            parts.append(f"{length}{_CIGAR_OPS[op]}")
        return "".join(parts), zdropped, max_q+1, max_t+1, delcount, inscount
    finally:
        if cigar_ptr:
            free(cigar_ptr)

def revcomp(seq):
    l = len(seq)
    bseq = seq if isinstance(seq, bytes) else seq.encode()
    cdef char *s = cmappy.mappy_revcomp(l, bseq)
    r = s[:l] if isinstance(s, str) else s[:l].decode()
    free(s)
    return r

def verbose(v=None):
    if v is None: v = -1
    return cmappy.mm_verbose_level(v)
