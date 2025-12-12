"""
fastcash/kmers.py

Compiler functions for k-mer processors

"""

from numba import njit, int64, uint64, uint8
import numpy as np

from .dnaencode import compile_revcomp_and_canonical_code as compile_revcomp_and_canonical_code_old
from .dnaencode_fast import compile_revcomp_and_canonical_code as compile_revcomp_and_canonical_code_new
from .lowlevel import debug
from .lowlevel.llvm import compile_popcount, compile_cttz


def compile_kmer_iterator(shp, rcmode="f", new_encoding=False):
    """
    Return (k, iterator),
    where k is the k-mer length and
    iterator is a compiled k-mer iterator (generator function)
    for the given input shape 'shp' , which can be
    - an integer k for a contiguous shape,
    - or a tuple of growing indices, where k is the length of the tuple,
    and for the given rcmode (from {"both", "f", "r", min", "max"})
    """
    debugprint0, debugprint1, debugprint2 = debug.debugprint

    both = (rcmode == "both")
    if isinstance(shp, int):
        # special case: contiguous k-shape
        k = shp
        shp = None
    elif isinstance(shp, tuple):
        k = len(shp)
        if shp == tuple(range(k)):
            shp = None  # back to special case
    else:
        raise TypeError(f"shape shp={shp} must be int or k-tuple, but is {type(shp)}.")
    if k < 1 or k > 32:
        raise ValueError(f"only 1<= k <= 32 is supported, but k={k}.")
    codemask = uint64(4**(k - 1) - 1)
    revcomp, ccode = compile_revcomp_and_canonical_code_new(k, rcmode) if new_encoding else compile_revcomp_and_canonical_code_old(k, rcmode)

    if shp is None:
        # special case: contiguous k-mer
        debugprint0(f"- Processing contiguous {k}-mers.")

        @njit(nogil=True, locals=dict(
            code=uint64, endpoint=int64, i=int64, j=int64, c=uint64))
        def kmers(seq, start, end):
            endpoint = end - (k - 1)
            valid = False
            i = start
            while i < endpoint:
                if not valid:
                    code = 0
                    for j in range(k):
                        c = seq[i + j]
                        if c > 3:
                            i += j + 1  # skip invalid
                            break
                        code = (code << 2) | c
                    else:  # no break
                        valid = True
                    if not valid:
                        continue  # with while
                else:  # was valid, we have an old code
                    c = seq[i + k - 1]
                    if c > 3:
                        valid = False
                        i += k  # skip invalid
                        continue  # with while
                    code = ((code & codemask) << 2) | c
                # at this point, we have a valid code
                if both:
                    yield code
                    yield revcomp(code)
                else:
                    yield ccode(code)
                i += 1
            pass  # all done here
    else:
        # general shape: k:int and shp:tuple are set
        debugprint0(f"- Processing gapped {k}-mers: {shp}.")

        @njit(nogil=True, locals=dict(
            code=uint64, startpoint=int64, i=int64, j=int64, c=uint64))
        def kmers(seq, start, end):
            startpoints = (end - start) - shp[k - 1]
            for i in range(start, start + startpoints):
                code = 0
                for j in shp:
                    c = seq[i + j]
                    if c > 3:
                        break
                    code = (code << 2) + c
                else:  # no break
                    if both:
                        yield code
                        yield revcomp(code)
                    else:
                        yield ccode(code)
            # all done here

    return k, kmers


def compile_kmer_subarray_iterator(k):
    """
    UNTESTED!

    Return a pair (k, kmers),
    where kmers is a compiled k-subarray iterator (generator function)
    for the given value of k,
    which yields each (valid) contiguous sub-array of a sequence.
    """
    # TODO: improve efficiency (rolling)
    @njit(nogil=True, locals=dict(
        code=uint64, startpoint=int64, i=int64, j=int64, c=uint64))
    def kmers(seq, start, end):
        startpoints = (end - start) - (k - 1)
        for i in range(start, start + startpoints):
            for j in range(k):
                c = seq[i + j]
                if c > 3:
                    break
                else:  # no break
                    yield seq[i:(i + k)]  # should be a view
            # all done here
    return k, kmers


####################################################################
# Efficient k-mer processor for arbitrary shapes
# with function injection

def compile_kmer_processor(shp, func, rcmode="f", new_encoding=False):
    """
    Return (k, processor),
    where k is the k-mer length and
    processor is a compiled k-mer processor.

    The compiled k-mer processor executes a function 'func'
    for each valid k-mer of for the given shape 'shp', which can be
    - an integer k for a contiguous shape,
    - or a tuple of growing indices, where k is the length of the tuple.

    Signature of func must be as follows:
    def func(hashtable, kmercode, param1, param2, param3, ...):
        ...
        return boolean(failure)
    Parameters param1, ... can be an arbitrary number of arrays.

    The given 'rcmode' must be from {"both", "f", "r", min", "max"}
    and specifies how to deal with reverse complementarity.
    """
    debugprint0, debugprint1, debugprint2 = debug.debugprint

    both = (rcmode == "both")
    if isinstance(shp, int):
        # special case: contiguous k-shape
        k = shp
        shp = None
    elif isinstance(shp, tuple):
        k = len(shp)
        if shp == tuple(range(k)):
            shp = None  # back to special case
    else:
        raise TypeError(f"shape shp={shp} must be int or k-tuple, but is {type(shp)}.")
    if k < 1 or k > 32:
        raise ValueError(f"only 1<=k<=32 is supported, but k={k}.")
    codemask = uint64(4**(k - 1) - 1)
    revcomp, ccode = compile_revcomp_and_canonical_code_new(k, rcmode) if new_encoding else compile_revcomp_and_canonical_code_old(k, rcmode)

    if shp is None:
        # special case: contiguous k-mer
        debugprint0(f"- Processing contiguous {k}-mers.")

        @njit(nogil=True, locals=dict(
            code=uint64, endpoint=int64, i=int64, j=int64, c=uint64))
        def processor(ht, seq, start, end, *parameters):
            endpoint = end - (k - 1)
            valid = failed = False
            i = start
            while i < endpoint:
                if not valid:
                    code = 0
                    for j in range(k):
                        c = seq[i + j]
                        if c > 3:
                            i += j + 1  # skip invalid
                            break
                        code = (code << 2) | c
                    else:  # no break
                        valid = True
                    if not valid:
                        continue  # with while
                else:  # was valid, we have an old code
                    c = seq[i + k - 1]
                    if c > 3:
                        valid = False
                        i += k  # skip invalid
                        continue  # with while
                    code = ((code & codemask) << 2) | c
                # at this point, we have a valid code
                if both:
                    failed = func(ht, code, *parameters)
                    failed |= func(ht, revcomp(code), *parameters)
                else:
                    failed = func(ht, ccode(code), *parameters)
                i += 1
                if failed is True:
                    break
            pass  # all done here; end of def kmers(...).
    else:
        # general shape: k:int and shp:tuple are given
        debugprint0(f"- Processing gapped {k}-mers: {shp}.")

        @njit(nogil=True, locals=dict(
                code=uint64, startpoint=int64, i=int64, j=int64, c=uint64))
        def processor(ht, seq, start, end, *parameters):
            startpoints = (end - start) - shp[k-1]
            failed = False
            for i in range(start, start+startpoints):
                code = 0
                for j in shp:
                    c = seq[i+j]
                    if c > 3:
                        break
                    code = uint64(code << 2) + uint64(c)
                else:  # no break
                    if both:
                        failed  = func(ht, code, *parameters)
                        failed |= func(ht, revcomp(code), *parameters)
                    else:
                        failed = func(ht, ccode(code), *parameters)
                if failed is True: break
            pass  # all done here

    return k, processor


def compile_positional_kmer_processor(shp, func, rcmode="f", new_encoding=False):
    """
    like compile_kmer_processor, but also uses the current k-mer start position
    as an additional argument to func:
        func(hashtable, kmercode, position, *parameters)
    """
    debugprint0, debugprint1, debugprint2 = debug.debugprint
    both = (rcmode == "both")
    if isinstance(shp, int):
        # special case: contiguous k-shape
        k = shp
        shp = None
    elif isinstance(shp, tuple):
        k = len(shp)
        if shp == tuple(range(k)): shp = None  # back to special case
    else:
        raise TypeError(f"shape shp={shp} must be int or k-tuple, but is {type(shp)}.")
    if k < 1 or k > 32:
        raise ValueError(f"only 1<=k<=32 is supported, but k={k}.")
    codemask = uint64(4**(k-1) - 1)
    revcomp, ccode = compile_revcomp_and_canonical_code_new(k, rcmode) if new_encoding else compile_revcomp_and_canonical_code_old(k, rcmode)

    if shp is None:
        # special case: contiguous k-mer
        debugprint0(f"- Processing contiguous {k}-mers.")

        @njit(nogil=True, locals=dict(
                code=uint64, endpoint=int64, i=int64, j=int64, c=uint64))
        def processor(ht, seq, start, end, *parameters):
            endpoint = end - (k-1)
            valid = failed = False
            i = start
            while i < endpoint:
                if not valid:
                    code = 0
                    for j in range(k):
                        c = seq[i+j]
                        if c > 3:
                            i += j + 1  # skip invalid
                            break
                        code = (code << 2) | c
                    else:  # no break
                        valid = True
                    if not valid: continue  # with while
                else:  # was valid, we have an old code
                    c = seq[i+k-1]
                    if c > 3:
                        valid = False
                        i += k  # skip invalid
                        continue  # with while
                    code = ((code & codemask) << 2) | c
                # at this point, we have a valid code
                if both:
                    failed  = func(ht, code, i, *parameters)
                    failed |= func(ht, revcomp(code), i, *parameters)
                else:
                    failed = func(ht, ccode(code), i, *parameters)
                i += 1
                if failed is True: break
            pass  # all done here; end of def kmers(...).
    else:
        # general shape: k:int and shp:tuple are given
        debugprint0(f"- Processing gapped {k}-mers: {shp}.")

        @njit(nogil=True, locals=dict(
                code=uint64, startpoint=int64, i=int64, j=int64, c=uint64))
        def processor(ht, seq, start, end, *parameters):
            startpoints = (end - start) - shp[k-1]
            failed = False
            for i in range(start, start+startpoints):
                code = 0
                for j in shp:
                    c = seq[i+j]
                    if c > 3:
                        break
                    code = uint64(code << 2) + uint64(c)
                else:  # no break
                    if both:
                        failed  = func(ht, code, i, *parameters)
                        failed |= func(ht, revcomp(code), i, *parameters)
                    else:
                        failed = func(ht, ccode(code), i, *parameters)
                if failed is True: break
            pass  # all done here

    return k, processor

def compile_positional_translated_kmer_processor(shp, func, rcmode="f", new_encoding=False):
    """
    like compile_positional_kmer_processor, but also translates C->T and G->A and
    only inserts the each k-mer once
        func(hashtable, kmercode, position, *parameters)
    """
    # TODO: probably not working for new encoding
    assert not new_encoding

    debugprint0, debugprint1, debugprint2 = debug.debugprint
    both = (rcmode == "both")
    if isinstance(shp, int):
        # special case: contiguous k-shape
        k = shp
        shp = None
    elif isinstance(shp, tuple):
        k = len(shp)
        if shp == tuple(range(k)): shp = None  # back to special case
    else:
        raise TypeError(f"shape shp={shp} must be int or k-tuple, but is {type(shp)}.")
    if k < 1 or k > 32:
        raise ValueError(f"only 1<=k<=32 is supported, but k={k}.")
    codemask = uint64(4**(k-1) - 1)
    revcomp, ccode = compile_revcomp_and_canonical_code_new(k, rcmode) if new_encoding else compile_revcomp_and_canonical_code_old(k, rcmode)

    if shp is None:
        # special case: contiguous k-mer
        debugprint0(f"- Processing contiguous {k}-mers.")

        @njit(nogil=True, locals=dict(
                code=uint64, code_ct=uint64, code_ga=uint64,
                canoncial_code=uint64, canoncial_code_ct=uint64, canoncial_code_ga=uint64,
                endpoint=int64, i=int64, j=int64, c=uint64))
        def processor(ht, seq, start, end, *parameters):
            endpoint = end - (k - 1)
            valid = failed = False
            i = start
            while i < endpoint:
                if not valid:
                    code = 0
                    code_ct = 0
                    code_ga = 0
                    for j in range(k):
                        c = seq[i + j]
                        if c > 3:
                            i += j + 1  # skip invalid
                            break
                        code = (code << 2) | c
                        if c == 1:
                            code_ct = (code_ct << 2) | 3
                            code_ga = (code_ga << 2) | c
                        elif c == 2:
                            code_ct = (code_ct << 2) | c
                            code_ga = (code_ga << 2) | 0
                        else:
                            code_ct = (code_ct << 2) | c
                            code_ga = (code_ga << 2) | c

                    else:  # no break
                        valid = True
                    if not valid: continue  # with while
                else:  # was valid, we have an old code
                    c = seq[i + k - 1]
                    if c > 3:
                        valid = False
                        i += k  # skip invalid
                        continue  # with while
                    code = ((code & codemask) << 2) | c
                    if c == 1:
                        code_ct = ((code_ct & codemask) << 2) | 3
                        code_ga = ((code_ga & codemask) << 2) | c
                    elif c == 2:
                        code_ct = ((code_ct & codemask) << 2) | c
                        code_ga = ((code_ga & codemask) << 2) | 0
                    else:
                        code_ct = ((code_ct & codemask) << 2) | c
                        code_ga = ((code_ga & codemask) << 2) | c
                # at this point, we have a valid code
                if both:
                    failed = func(ht, code, i, *parameters)
                    failed |= func(ht, revcomp(code), i, *parameters)
                    if ccode(code_ct) != ccode(code):
                        failed |= func(ht, code_ct, i, *parameters)
                        failed |= func(ht, revcomp(code_ct), i, *parameters)
                    if ccode(code_ga) != ccode(code) and ccode(code_ga) != ccode(code_ct):
                        failed |= func(ht, code_ga, i, *parameters)
                        failed |= func(ht, revcomp(code_ga), i, *parameters)
                else:
                    canoncial_code = ccode(code)
                    canoncial_code_ct = ccode(code_ct)
                    canoncial_code_ga = ccode(code_ga)
                    failed = func(ht, canoncial_code, i, *parameters)
                    if canoncial_code_ct != canoncial_code:
                        failed |= func(ht, canoncial_code_ct, i, *parameters)
                    if canoncial_code_ga != canoncial_code and canoncial_code_ga != canoncial_code_ct:
                        failed |= func(ht, canoncial_code_ga, i, *parameters)
                i += 1
                if failed is True: break
            pass  # all done here; end of def kmers(...).
    else:
        # general shape: k:int and shp:tuple are given
        debugprint0(f"- Processing gapped {k}-mers: {shp}.")

        @njit(nogil=True, locals=dict(
              code=uint64, startpoint=int64, i=int64, j=int64, c=uint64))
        def processor(ht, seq, start, end, *parameters):
            startpoints = (end - start) - shp[k - 1]
            failed = False
            for i in range(start, start+startpoints):
                code = 0
                code_ct = 0
                code_ga = 0
                for j in shp:
                    c = seq[i+j]
                    if c > 3:
                        break
                    code = uint64(code << 2) + uint64(c)
                    if c == 1:
                        code_ct = (code_ct << 2) | 3
                        code_ga = (code_ga << 2) | c
                    elif c == 2:
                        code_ct = (code_ct << 2) | c
                        code_ga = (code_ga << 2) | 0
                else:  # no break
                    if both:
                        failed = func(ht, code, i, *parameters)
                        failed |= func(ht, revcomp(code), i, *parameters)
                        if ccode(code_ct) != ccode(code):
                            failed |= func(ht, code_ct, i, *parameters)
                            failed |= func(ht, revcomp(code_ct), i, *parameters)
                        if ccode(code_ga) != ccode(code) and ccode(code_ga) != ccode(code_ct):
                            failed |= func(ht, code_ga, i, *parameters)
                            failed |= func(ht, revcomp(code_ga), i, *parameters)
                    else:
                        canoncial_code = ccode(code)
                        canoncial_code_ct = ccode(code_ct)
                        canoncial_code_ga = ccode(code_ga)
                        failed = func(ht, canoncial_code, i, *parameters)
                        if canoncial_code_ct != canoncial_code:
                            failed |= func(ht, canoncial_code_ct, i, *parameters)
                        if canoncial_code_ga != canoncial_code and canoncial_code_ga != canoncial_code_ct:
                            failed |= func(ht, canoncial_code_ga, i, *parameters)
                if failed is True: break
            pass  # all done here

    return k, processor


# Iterative spaced seed hashing (doi: 10.1007/978-3-030-20242-2_18, reversed order compared to paper)

def compile_positional_kmer_processor_issh(shp, func, rcmode="f", new_encoding=False):
    """
    like compile_kmer_processor, but also uses the current k-mer start position
    as an additional argument to func:
        func(hashtable, kmercode, position, *parameters)
    """
    both = (rcmode == "both")
    k = len(shp)
    if k < 1 or k > 32:
        raise ValueError(f"only 1<=k<=32 is supported, but k={k}.")
    revcomp, ccode = compile_revcomp_and_canonical_code_new(k, rcmode) if new_encoding else compile_revcomp_and_canonical_code_old(k, rcmode)
    popcnt = compile_popcount('uint64')
    cttz = compile_cttz('uint64')

    weight, width = uint64(len(shp)), uint64(max(shp) + 1)
    sig_mask = 0
    m = np.zeros(width, dtype=np.uint64)
    for i in shp:
        sig_mask |= 1 << (width - i - 1)
    sig_mask = uint64(sig_mask)

    for i in range(width - 1):
        m[i + 1] = m[i] + (sig_mask >> (width - i - 1) & 1)

    C = np.zeros((width, width), dtype=np.uint64)
    masks = np.zeros((width, width), dtype=np.uint64)
    for g in range(width):
        for j in range(width - 1):
            for k in shp:
                if k + j < width and (sig_mask >> (width - (k + j) - 1) & 1) == 1 and m[k] == m[k + j] - m[j] + m[g]:
                    C[g, j] |= 1 << (width - k - 1)
                    masks[g, j] |= (3 << 2 * (weight - m[k + j] - 1))

    @njit(nogil=True, locals=dict(best=uint64, best_i=uint64, best_j=uint64, use=uint64))
    def find_best_prev(s, to_cover):
        best = 0
        best_i, best_j = 0, 1
        for z in range(0, s - 1):
            for k in range(1, s):
                use = popcnt(to_cover & C[z, k])
                if use > best:
                    best = use
                    best_i, best_j = z, k
        return best_i, best_j

    @njit(nogil=True, locals=dict(mask=uint64, n_ones=uint64, positions=uint64, n_ones_new=uint64))
    def compute_shift(g, k):
        mask = masks[g, k]
        n_ones = cttz(mask) // 2
        positions = width - shp[weight - n_ones - 1] - 1 + k
        n_ones_new = popcnt(sig_mask & (2**positions - 1))
        return 2 * (n_ones_new - n_ones)

    steps = []
    last = 0
    # new position does not need to be covered
    to_cover = sig_mask & ~uint64(1)
    while to_cover != 0:
        g, k = find_best_prev(width - 1, to_cover)
        shift = compute_shift(g, k)
        remove = to_cover & C[g, k]
        to_cover &= ~remove
        steps.append([k, shift, masks[g, k]])
        last = max(last, k)
    steps = np.array(steps, dtype=np.uint64)

    @njit(nogil=True, locals=dict(code=uint64, shift=uint64, k=uint64, mask=uint64, contained_ns=uint64, c=uint8))
    def issh_processor_fast(ht, seq, start, end, *parameters):
        if (end - start) < (width - 1):
            return
        hashes = np.zeros(last, dtype=np.uint64)
        # compute history
        end_naive = min(start + last, end)
        for i in range(start, end_naive):
            contained_ns = 0
            code = 0
            for j in shp:
                c = seq[i + j]
                contained_ns |= (c > 3)
                code = (code << 2) | min(uint64(c), uint64(3))
            hashes[i] = code
            if not contained_ns:
                if both:
                    failed = func(ht, code, i, *parameters)
                    failed |= func(ht, revcomp(code), i, *parameters)
                else:
                    failed = func(ht, ccode(code), i, *parameters)
                if failed is True:
                    return

        # necessary to check for Ns in first window
        contained_ns = 0
        for i in range(width):
            contained_ns = (contained_ns << 1) | (seq[start + last + i] > 3)
        contained_ns = contained_ns >> 1

        # compute gapped k-mers iteratively based on previous gapped k-mers
        for i in range(start + last, (end - start) - (width - 1)):
            contained_ns = contained_ns << 1
            code = 0
            for k, shift, mask in steps:
                code |= (hashes[(i - k) % last] & mask) << shift
            c = seq[i + width - 1]
            contained_ns |= c > 3
            code |= min(uint64(c), uint64(3))

            hashes[i % last] = code
            if not contained_ns & sig_mask:
                if both:
                    failed = func(ht, code, i, *parameters)
                    failed |= func(ht, revcomp(code), i, *parameters)
                else:
                    failed = func(ht, ccode(code), i, *parameters)
                if failed is True:
                    return
    return k, issh_processor_fast
