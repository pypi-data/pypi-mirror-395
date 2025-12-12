"""
xengsort_weak.py:
Mark weak k-mers.efficiently.
Weak k-mers are k-mers that have a Hamming distance 1 neighbor
in the other species.
"""

import numpy as np
from numba import njit, uint64, uint32, int64
from concurrent.futures import ThreadPoolExecutor, wait

from ..dnaencode import compile_revcomp_and_canonical_code
from ..lowlevel import debug  # The debug module with globals!


"""
Terminology:

Group: k-mers that start with a (short) common prefix
    of length group_prefix_length (0, 1 or 2).
    During marking weak k-mers, 
    a single group is kept in an in-memory array at the same time.

Section: a group is divided into several sections;
    each section is examined by one of several threads.
    If we have 9 threads, we should have 9 equally sized sections.
    Section borders must also be block borders.

Block: set of k-mers that share a (long) common prefix
    of length 'block_prefix_length' (approx. 2k/3).
    We look for HD-1 pairs of k-mers only inside blocks.
    One section consists of many blocks.

Part (of a k-mer): Approximately 1/3 of a k-mer.
    We partition a k-mer into 3 parts 
    to efficiently find its HD 1 neighbors.
    The first part (prefix) and last part (suffix) have equal length.
    The middle part may be 1 character longer or shorter, 
    depending on k mod 3.
"""


@njit(nogil=True, locals=dict(
    elem1=uint64, elem2=uint64, h=uint64, mask=uint64, onebit=uint32))
def have_hamming_dist_one(elem1, elem2):
    """
    Return True iff DNAHammingDistance(elem1, elem2) <= 1.
    elem1, elem2 must be 2-bit encoded DNA k-mers.
    """
    mask = uint64(6148914691236517205)  # Mask 0b_01...01010101
    h = elem1 ^ elem2
    h = (h | (h >> 1)) & mask
    onebit = (h & uint64(h - 1)) == uint64(0)
    return onebit


def compile_mark_weak_kmers_in_suffix(
        block_prefix_length,
        k, 
        WEAKMASK,
        VALUEBITS
        ):
    """
    Compile and return a function 'mark_weak_kmers_in_suffix(codes)'
    that examines a sorted array of aggregated k-mer encodings and values
    and decides which k-mers are weak.
    Array 'codes' stores both kmer codes and values: [kmercode|value]
    The number of bits for the value is VALUEBITS.

    prefix_length: Configure search for HD 1 neighbors only in blocks
        where the prefix of this length is constant
    k: the k-mer size (must be >= prefix_length)
    WEAKMASK: bit mask with a single 1-bit that marks weak k-mers
    VALUEBITS: number of bits to store values
    """
    if k <= block_prefix_length:
        raise ValueError(f"k={k} <= {block_prefix_length}=block_prefix_length")
    suffix_bits = 2*k - 2*block_prefix_length + VALUEBITS
    VALUEMASK = uint64(2 ** VALUEBITS - 1)
    SPECIESMASK = uint64(3)  # specific to xengsort

    @njit(nogil=True,  locals=dict(
            ncodes=int64, start=int64, end=int64,
            pos=int64, pos2=int64,
            prefix=uint64,
            element=uint64, value=uint64,
            sec_element=uint64, sec_value=uint64)
         )
    def mark_weak_kmers_in_suffix(codes):
        ncodes = codes.size
        start = end = 0
        while start < ncodes - 1:  # nothing to do if start == ncodes-1
            prefix = codes[start] >> suffix_bits
            # assert end == start
            while (end < ncodes) and (prefix == uint64(codes[end] >> suffix_bits)):
                end += 1
            for pos in range(start, end):
                value = codes[pos] & VALUEMASK
                element = codes[pos] >> VALUEBITS
                found = False
                for pos2 in range(pos+1, end):
                    # Check wether both elements are host or graft
                    sec_value = codes[pos2] & VALUEMASK
                    if ((value & SPECIESMASK) == (sec_value & SPECIESMASK)): continue
                    sec_element = codes[pos2] >> VALUEBITS
                    if have_hamming_dist_one(element, sec_element):
                        found = True
                        codes[pos2] |= WEAKMASK
                if found:
                    codes[pos] |= WEAKMASK
            start = end
    return mark_weak_kmers_in_suffix


def compile_swap_kmer_parts(partlengths, valuebits):
    pl, il, sl = partlengths
    if pl != sl:
        raise ValueError(f"unsymmetric k-mer part lengths {partlengths}")
    ibl, sbl = sl, il
    valuemask = uint64(2 ** valuebits - 1)
    suffix_mask = (4**sl - 1)
    infix_mask = (4**il -1) << (2*sl)
    prefix_mask = (4**pl - 1) << (2*(sl+il))
    SM = uint64(suffix_mask << valuebits)
    IM = uint64(infix_mask << valuebits)
    PM = uint64(prefix_mask << valuebits)
    suffix_back_mask = (4**il - 1)
    infix_back_mask = (4**sl -1) << (2*il)
    SBM = uint64(suffix_back_mask << valuebits)
    IBM = uint64(infix_back_mask << valuebits)

    @njit(nogil=True, locals=dict(
        pos=int64, code=uint64)
        )
    def move_middle_part_right(codes):
        for pos in range(len(codes)):
            code = codes[pos]
            codes[pos] = (code & PM) | (code & valuemask)\
                       | ((code & SM) << (2*il))\
                       | ((code & IM) >> (2*sl))

    @njit(nogil=True, locals=dict(
        pos=int64, code=uint64)
        )
    def build_original_kmer(codes):
        for pos in range(len(codes)):
            code = codes[pos]
            codes[pos] = (code & PM) | (code & valuemask)\
                       | ((code & SBM) << (2*ibl))\
                       | ((code & IBM) >> (2*sbl))

    return move_middle_part_right, build_original_kmer



def compile_grouping_functions(
        h,
        k,
        group_prefix_length,
        nextchars,
        rcmode,
        weakmask,
        valuebits):
    """
    Compile a function 'update_hashtable(ht, codes)'
    that updates the hashtable ht with the weak bit information
    from the array codes[:] where the weak bits have been set.

    Compile a function get_groupsizes(ht)
    that computes and returns an array
    groupsizes[subtable, group_prefix, nextbase]
    with the group size (number of k-mers) for a given combination
    of subtable, group prefix (in 0:4**group_prefix_length),
    and next basepair (in 0:4).

    ...
    """
    if group_prefix_length + nextchars >= k//3:
        raise ValueError("group_prefix_length or nextchars too large: "
            f"{group_prefix_length=}, {nextchars=}, but {k//3=}")
    rc, cc = compile_revcomp_and_canonical_code(k, rcmode)
    subtables = h.subtables
    nbuckets = h.nbuckets
    bucketsize = h.bucketsize
    get_signature_at = h.private.get_signature_at
    get_value_at = h.private.get_value_at
    get_key_sig = h.private.get_subkey_from_bucket_signature# TODO: Does this work using subtables?
    is_slot_empty_at = h.private.is_slot_empty_at
    get_subtable_subkey = h.private.get_subtable_subkey_from_key
    update_item = h.private.update_ssk
    get_key_from_sub_subkey = h.private.get_key_from_subtable_subkey
    shift = 2 * (k - group_prefix_length)
    ngroups = 4 ** group_prefix_length
    nnext = 4 ** nextchars
    nextshift = shift - 2*nextchars
    nextmask = uint64(nnext - 1)
    if nextshift <= 0:
        raise ValueError("group_prefix_length or nextchars too large: "
            f"{group_prefix_length=}, {nextchars=}, but {k//3=}, {shift=}, {nextshift=}")
    valuemask = uint64(2**valuebits - 1)
    do_rev = k % 2 == 1  # standard case shortcut
    maybe_rev = k % 2 == 0  # needs add'l check

    @njit(nogil=True, locals=dict(
        code=uint64, cv=uint64, nweak=int64))
    def update_hashtable(ht, codes):
        nweak = 0
        for cv in codes:
            if cv & weakmask == 0: continue
            code = cv >> valuebits
            st, subkey = get_subtable_subkey(cc(code))
            status, result = update_item(ht, st, subkey, 0) # 0 indicates weak bits in value set
            assert status & 128 != 0
            nweak += 1
        return nweak

    @njit(nogil=True, locals=dict(
        st=uint64, p=uint64, s=uint64, sig=uint64,
        subkey=uint64, key=uint64, rev_key=uint64,
        prefix=uint64, nxt=uint64))
    def count_in_subtable(ht, groupsizes, st):
        for p in range(nbuckets):
            for s in range(bucketsize):
                if is_slot_empty_at(ht, st, p, s):
                    break
                sig = get_signature_at(ht, st, p, s)
                subkey = get_key_sig(p, sig)
                key = get_key_from_sub_subkey(st, subkey)
                rev_key = rc(key)
                # count
                prefix = (key >> shift)
                nxt = (key >> nextshift) & nextmask
                groupsizes[prefix, nxt] += 1
                if do_rev or (maybe_rev and key != rev_key):
                    prefix = (rev_key >> shift)
                    nxt = (rev_key >> nextshift) & nextmask
                    groupsizes[prefix, nxt] += 1

    @njit(nogil=True, locals=dict(
        p=uint64, s=uint64, sig=uint64, value=uint64, keyval=uint64,
        key=uint64, subkey=uint64, rev_key=uint64, prefix=uint64, nxt=uint64))
    def extract_from_subtable(ht, st, prefix, group_next_position, codes):
        for p in range(nbuckets):
            for s in range(bucketsize):
                if is_slot_empty_at(ht, st, p, s):
                    break
                value = get_value_at(ht, st, p, s)
                sig = get_signature_at(ht, st, p, s)
                subkey = get_key_sig(p, sig)
                key = get_key_from_sub_subkey(st, subkey)
                rev_key = rc(key)
                # insert into codes table
                if (key >> shift) == prefix:
                    nxt = (key >> nextshift) & nextmask
                    keyval = (key << valuebits) | (value & valuemask)
                    codes[group_next_position[nxt]] = keyval
                    group_next_position[nxt] += 1
                if (do_rev or (maybe_rev and key != rev_key)) and (rev_key >> shift) == prefix:
                    nxt = (rev_key >> nextshift) & nextmask
                    keyval = (rev_key << valuebits) | (value & valuemask)
                    codes[group_next_position[nxt]] = keyval
                    group_next_position[nxt] += 1

    return update_hashtable, count_in_subtable, extract_from_subtable


# adapter function for sort
# Note: this is pure Python/numpy, called in ThreadPool.
# Can they actually run in parallel?
def my_sort(codes):
    codes.sort(kind='quicksort')


@njit(nogil=True)
def get_section_borders(codes, mask, borders):
    #borders = np.empty(threads+1, dtype=np.int64)
    ncodes = codes.size
    threads = borders.size - 1
    for i in range(threads):
        borders[i] = (ncodes*i) // threads
    borders[threads] = ncodes
    for i in range(1, threads):
        while (borders[i]+1 < ncodes) and (
            (codes[borders[i]] & mask) == (codes[borders[i]+1] & mask)):
                borders[i] += 1
        borders[i] += 1  # first element of new block


# calculate weak k-mers ###############################
def calculate_weak_set(
        h, k,
        group_prefix_length,
        nextchars, *,
        rcmode="max",
        threads=None,
        WEAKMASK=uint64(4),
        VALUEBITS=4):
    # typical: k=25, group_prefix_length=0..2, nextchars=1..2, rcmode="max"

    debugprint0, debugprint1, debugprint2 = debug.debugprint
    timestamp0, timestamp1, timestamp2 = debug.timestamp

    subtables = h.subtables
    ht = h.hashtable
    if threads is None:
        threads = subtables
    #threads = max(threads, subtables)  # threads < subtables not recommended but possible
    nnext = 4 ** nextchars

    update_hashtable, count_in_subtable, build_group \
        = compile_grouping_functions(
            h, k, group_prefix_length, nextchars, rcmode, WEAKMASK, VALUEBITS)

    kthird = k // 3
    partlengths = [kthird] * 3  # prefix (0), infix (1), suffix (2)
    sbl = 3 * kthird
    if sbl == k-1:
        partlengths[1] += 1
    elif sbl == k-2:
        partlengths[0] += 1
        partlengths[2] += 1
    assert sum(partlengths) == k
    block_prefix_length = partlengths[0] + partlengths[1]
    m_block_prefix_length = partlengths[0] + partlengths[1] // 2 + partlengths[2]

    mark_weak_kmers_in_suffix = compile_mark_weak_kmers_in_suffix(block_prefix_length, k, WEAKMASK, VALUEBITS)
    mark_weak_kmers_in_middle = compile_mark_weak_kmers_in_suffix(m_block_prefix_length, k, WEAKMASK, VALUEBITS)
    swap_right, swap_back = compile_swap_kmer_parts(partlengths, VALUEBITS)

    with ThreadPoolExecutor(max_workers=1+threads) as executor:
        # Count k-mers for each combination of (subtable, prefix, nextchars)
        time_start_groupsizes = timestamp1(msg=f"- Begin counting group sizes with {threads} threads")
        gs = [np.zeros((4**group_prefix_length, nnext), dtype=np.int64) for st in range(subtables)]
        debugprint2(f"- groupsize array: {len(gs)} subtables x {gs[0].shape}")
        futures = [ executor.submit(count_in_subtable, ht, gs[st], st)
                    for st in range(subtables) ]
        wait(futures)
        gs = np.array(gs)  # turn list of 2D arrays into 3D array gs[subtable, prefix, nxt]
        groupsizes = np.sum(gs, axis=(0,2))
        gssum = np.sum(groupsizes)
        debugprint2(f"- Group sizes: {groupsizes.shape} -- sum {gssum} -- {groupsizes}")
        timestamp1(time_start_groupsizes, msg="- Time for counting group sizes")
        if gssum == 0:
            raise ValueError("ERROR: no groups!")

        bigcodes = np.empty(np.amax(groupsizes), dtype=np.uint64)
        section_borders = np.empty(threads+1, dtype=np.int64)
        for prefix in range(len(groupsizes)):
            time_start_prefixgroup = timestamp1(msg=f"\n- Counting and building k-mer group with {prefix=}:")
            ncodes = groupsizes[prefix]
            codes = bigcodes[:ncodes]  # a view!
            start_next = np.cumsum(np.sum(gs[:,prefix,:], axis=0))
            start_next[1:] = start_next[:-1]
            start_next[0] = 0
            futures = []
            start_st = np.cumsum(gs[:, prefix, :], axis=0)
            start_st[1:, :] = start_st[:-1,:]
            start_st[0,:] = 0
            starts = np.array([
                [start_next[n]+start_st[st][n] for n in range(nnext)] 
                for st in range(subtables)])
            for st in range(subtables):
                assert starts[st].size == nnext
                futures.append(executor.submit(
                    build_group, ht, st, prefix, starts[st], codes))
            wait(futures)
            time_start_sort1 = timestamp2(time_start_prefixgroup, msg=f"- Time to extract k-mer group with {prefix=}")
            sb = np.append(start_next, ncodes) # TODO -- what?
            assert sb.size == nnext + 1
            futures = [
               executor.submit(my_sort, codes[sb[i]:sb[i+1]])
               for i in range(nnext) ]
            wait(futures)
            time_start_mark1 = timestamp2(time_start_sort1, msg=f"- Time to sort k-mer group with {prefix=}")
            block_prefix_bits = partlengths[0] + partlengths[1]
            block_prefix_shift = 2*partlengths[2] + VALUEBITS
            block_prefix_mask = uint64((4**block_prefix_bits - 1) << block_prefix_shift)
            get_section_borders(codes, block_prefix_mask, section_borders)
            debugprint2(f"- Section borders: {section_borders.tolist()}")
            debugprint2(f"- Group size: {groupsizes[prefix]}")
            futures = [
               executor.submit(
                   mark_weak_kmers_in_suffix,
                   codes[section_borders[i]:section_borders[i+1]]
                   ) for i in range(threads) ]
            wait(futures)

            time_start_swap1 = timestamp2(time_start_mark1, msg=f"- Time to mark weak k-mers from suffixes")
            futures = [
               executor.submit(swap_right, codes[section_borders[i]:section_borders[i+1]])
               for i in range(threads) ]
            wait(futures)
            time_start_sort2 = timestamp2(time_start_swap1, msg=f"- Time to bit-swap k-mers")

            # Re-sort after bit-swap
            block_prefix_bits = partlengths[0]
            block_prefix_shift = 2 * (partlengths[1] + partlengths[2]) + VALUEBITS
            block_prefix_mask = uint64((4**block_prefix_bits - 1) << block_prefix_shift)
            get_section_borders(codes, block_prefix_mask, section_borders)
            futures = [
               executor.submit(my_sort, codes[section_borders[i]:section_borders[i+1]])
               for i in range(threads) ]
            wait(futures)
            time_start_mark2 = timestamp2(time_start_sort2, msg=f"- Time to re-sort after bit-swap")

            # Define sections, mark k-mers (from middle part)
            block_prefix_bits = partlengths[0] + partlengths[2]
            block_prefix_shift = 2*partlengths[1] + VALUEBITS
            block_prefix_mask = uint64((4**block_prefix_bits - 1) << block_prefix_shift)
            get_section_borders(codes, block_prefix_mask, section_borders)
            debugprint2(f"- New section borders: {section_borders.tolist()}")
            debugprint2(f"- New group size: {groupsizes[prefix]}")
            futures = [
                executor.submit(
                    mark_weak_kmers_in_middle,
                    codes[section_borders[i]:section_borders[i+1]]
                ) for i in range(threads) ]
            wait(futures)
            time_start_swap2 = timestamp2(time_start_mark2, msg="- Time to mark weak k-mers from middle part")

            # Bit-swap k-mers back
            futures = [
               executor.submit(swap_back, codes[section_borders[i]:section_borders[i+1]])
               for i in range(threads) ]
            wait(futures)
            time_start_update = timestamp2(time_start_swap2, msg="- Time to bit-swap k-mers back")

            # Update hash table
            weak_kmers = update_hashtable(ht, codes)
            timestamp2(time_start_update, msg="- Time to update hash table")
            timestamp1(time_start_prefixgroup, msg=f"- Group time for k-mer group with {prefix=}")
    pass
    # That's all, folks. It ends here.
