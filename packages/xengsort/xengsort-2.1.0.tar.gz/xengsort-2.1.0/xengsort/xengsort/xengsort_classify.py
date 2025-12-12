"""
xengsort_classify:
Xenograft classification
by Jens Zentgraf & Sven Rahmann, 2019--2023
"""

import datetime
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor, as_completed
from math import ceil
from pathlib import Path


import numpy as np
from numba import njit, uint32, uint64, int64
from ..io.hashio import load_hash
from ..kmers import compile_kmer_processor, compile_positional_kmer_processor
from ..io.generalio import InputFileHandler, OutputFileHandler
from ..io.fastqio import fastq_chunks, fastq_chunks_paired
from ..lowlevel.bitarray import bitarray
from ..dnaencode import (
    quick_dna_to_2bits,
    twobits_to_dna_inplace,
    compile_twobit_to_codes,
    compile_quick_dna_to_2bits,
    _TABLE_DNA_TO_2BITS)
from ..lowlevel import debug
from ..mask import create_mask


# ####### Classification methods ######
def compile_count_based_classification(params):
    Mh_factor = params.get("Mh", 4)
    Mh_min = params.get("Mh_min", 3)
    Mg_factor = params.get("Mg", 4)
    Mg_min = params.get("Mg_min", 3)
    Mb_factor = params.get("Mb", 5)
    Mb_min = params.get("Mb_min", 3)
    Mn_factor = params.get("Mn", 4)
    Mn_min = params.get("Mn_min", 3)
    Ag = params.get("Ag", 3)
    Ah = params.get("Ah", 3)
    nothing = params.get("nothing", 0)
    few = params.get("few", 6)

    @njit(nogil=True, locals=dict(
        gscore=uint32, hscore=uint32, nkmers=uint32))
    def classify_xengsort(counts):
        # counts = [neither, host, graft, both, NA, weakhost, weakgraft, both]
        # returns: 0=host, 1=graft, 2=ambiguous, 3=both, 4=neither.
        nkmers = 0
        for i in counts:
            nkmers += i
        if nkmers == 0:
            return 2  # no k-meres -> ambiguous
        insubstantial = max(uint32(nkmers // 20), 1)
        Mh = uint32(max(uint32(nkmers // Mh_factor), Mh_min))
        Mg = uint32(max(uint32(nkmers // Mg_factor), Mg_min))
        Mb = uint32(max(uint32(nkmers // Mb_factor), Mb_min))
        Mn = uint32(max(uint32((nkmers * 3) // 4 + 1), Mn_min))

        hscore = counts[1] + counts[5] // 2
        gscore = counts[2] + counts[6] // 2

        # no host
        if counts[1] + counts[5] == nothing:  # no host
            if gscore >= Ag:
                return 1  # graft
            if counts[3] + counts[7] >= Mb:  # both
                return 3  # both
            if counts[0] >= Mn:  # neither (was: > nkmers*3 // 4)
                return 4  # neither

        # host, but no graft
        elif counts[2] + counts[6] == nothing:  # no graft
            if hscore >= Ah:
                return 0  # host
            if counts[3] + counts[7] >= Mb:  # both
                return 3  # both
            if counts[0] >= Mn:  # neither
                return 4  # neither

        # some real graft, few weak host, no real host:
        if counts[2] >= few and counts[5] <= few and counts[1] == nothing:
            return 1  # graft
        # some real host, few weak graft, no real graft:
        if counts[1] >= few and counts[6] <= few and counts[2] == nothing:
            return 0  # host

        # substantial graft, insubstantial real host, a little weak host compared to graft:
        if counts[2] + counts[6] >= Mg and counts[1] <= insubstantial and counts[5] < gscore:
            return 1  # graft
        # substantial host, insubstantial real graft, a little weak graft compared to host:
        if counts[1] + counts[5] >= Mh and counts[2] <= insubstantial and counts[6] < hscore:
            return 0  # host
        if counts[3] + counts[7] >= Mb and gscore <= insubstantial and hscore <= insubstantial:  # both
            return 3  # both
        if counts[0] >= Mn:
            return 4  # neither
        return 2  # ambiguous
    return classify_xengsort


def compile_coverage_based_classification(cov, mask, params):
    # count_based_classification = compile_count_based_classification(params)
    k = mask.k
    W = mask.w
    popcount = cov.popcount
    score_return_map = np.array([0, 1, 3, 4], dtype=np.uint8)
    ret_host = 0
    ret_graft = 1
    ret_amb = 2
    ret_both = 3
    ret_neither = 4

    # define default params:
    p = dict()
    p.update(params)

    # coverage based parameters
    min_size = p["min_size"]
    weak_scale = eval(p["weak_scale"]) if isinstance(p["weak_scale"], str) else p["weak_scale"]
    T1_min = eval(p["T1_min"]) if isinstance(p["T1_min"], str) else p["T1_min"]
    T1_max = eval(p["T1_max"]) if isinstance(p["T1_max"], str) else p["T1_max"]
    T1_strong = eval(p["T1_strong"]) if isinstance(p["T1_strong"], str) else p["T1_strong"]
    T2 = eval(p["T2"]) if isinstance(p["T2"], str) else p["T2"]
    T3 = eval(p["T3"]) if isinstance(p["T3"], str) else p["T3"]
    T3_score = eval(p["T3_score"]) if isinstance(p["T3_score"], str) else p["T3_score"]
    T4 = eval(p["T4"]) if isinstance(p["T4"], str) else p["T4"]
    T5 = eval(p["T5"]) if isinstance(p["T5"], str) else p["T5"]
    T5_gap = eval(p["T5_gap"]) if isinstance(p["T5_gap"], str) else p["T5_gap"]
    T5_both_h_g = eval(p["T5_both_h_g"]) if isinstance(p["T5_both_h_g"], str) else p["T5_both_h_g"]
    T6 = eval(p["T6"]) if isinstance(p["T6"], str) else p["T6"]
    T7 = eval(p["T7"]) if isinstance(p["T7"], str) else p["T7"]
    T7_h_g = eval(p["T7_h_g"]) if isinstance(p["T7_h_g"], str) else p["T7_h_g"]
    T8 = eval(p["T8"]) if isinstance(p["T8"], str) else p["T8"]
    T9_gap = eval(p["T9_gap"]) if isinstance(p["T9_gap"], str) else p["T9_gap"]

    @njit(nogil=True)
    def classify_xengsort_cov(counts, neither, stronghost, stronggraft, both, weakhost, weakgraft, weakboth, size):
        # number of bases covered by k-mers of each class

        # no k-mers
        if size <= W + min_size:
            return ret_amb

        neitherBits = popcount(neither, 0, len(neither) * 64)
        strongHostBits = popcount(stronghost, 0, len(stronghost) * 64)
        strongGraftBits = popcount(stronggraft, 0, len(stronggraft) * 64)
        np.bitwise_or(both, weakboth, both)
        bothBits = popcount(both, 0, len(both) * 64)
        weakHostBits = popcount(weakhost, 0, len(weakhost) * 64)
        weakGraftBits = popcount(weakgraft, 0, len(weakgraft) * 64)

        fhost = strongHostBits
        f_weak_host = popcount(np.bitwise_xor(np.bitwise_or(stronghost, weakhost), stronghost), 0, len(stronghost) * 64)
        fgraft = strongGraftBits
        f_weak_graft = popcount(np.bitwise_xor(np.bitwise_or(stronggraft, weakgraft), stronggraft), 0, len(stronggraft) * 64)
        scores = np.zeros(4, dtype=np.float64)
        scores[0] = score_host = np.float64((fhost + f_weak_host * weak_scale) / size)
        scores[1] = score_graft = np.float64((fgraft + f_weak_graft * weak_scale) / size)
        scores[2] = score_both = np.float64((bothBits) / size)
        s_w_host = np.bitwise_or(stronghost, weakhost)
        s_w_graft = np.bitwise_or(stronggraft, weakgraft)
        s_w_both = both
        s_w_host_graft = np.bitwise_or(s_w_host, s_w_graft)
        s_w_host_both = np.bitwise_or(s_w_host, s_w_both)
        s_w_graft_both = np.bitwise_or(s_w_graft, s_w_both)
        s_w_host_graft_both = np.bitwise_or(s_w_host_graft, s_w_both)
        scores[3] = score_neither = np.float64((size - popcount(s_w_host_graft_both, 0, len(s_w_host_graft_both) * 64)) / size)

        # ############### first classify ##########
        # return: 0:host, 1:graft, 2:ambiguous, 3:both, 4:neither

        # No host
        if strongHostBits == 0 and weakHostBits <= W + 2:
            if score_graft >= T1_min:
                return ret_graft
            if score_both >= T1_min:
                return ret_both
            if score_neither >= T1_min:
                return ret_neither

        # No graft
        if strongGraftBits == 0 and weakGraftBits <= W + 2:
            if score_host >= T1_min:
                return ret_host
            if score_both >= T1_min:
                return ret_both
            if score_neither >= T1_min:
                return ret_neither

        # Both
        if score_both > T2 and strongHostBits == 0 and strongGraftBits == 0:
            return ret_both

        # check neither
        if neitherBits >= size * T3 and score_neither >= T3_score:
            return ret_neither

        # Host and graft
        if score_host >= T4 and score_graft >= T4:
            return ret_amb

        order = scores.argsort()

        # if most bits in both are set and no strong host or graft
        if order[3] == 2 and strongHostBits == 0 and strongGraftBits == 0 and\
           score_host < 0.1 and score_graft < 0.1:
            return ret_both

        # ################ GAP ##########################
        # high first score and big gap to the second score

        if scores[order[3]] >= T5 and scores[order[3]] - T5_gap >= scores[order[2]]:
            if order[3] == 0 or order[3] == 1:  # host/graft
                return score_return_map[order[3]]
            # first both, second host/graft
            if order[3] == 2:
                if (order[2] == 0 or order[2] == 1) and scores[order[2]] >= T5_both_h_g:
                    return score_return_map[order[2]]
                else:
                    return score_return_map[order[3]]

        # first is host/graft, second is both
        if (order[3] == 0 or order[3] == 1) and \
             scores[order[3]] >= T6 and\
             order[2] == 2:
            return score_return_map[order[3]]

        # first is both; second is not neither
        if order[3] == 2 and not order[2] == 3:
            if scores[order[3]] >= T7 and scores[order[2]] >= T7_h_g:
                # return 0
                return score_return_map[order[2]]
            else:
                return score_return_map[order[3]]

        # first neither
        if (order[3] == 3):
            if scores[order[2]] >= T8:
                return score_return_map[order[2]]
            else:
                return score_return_map[order[3]]

        if order[3] == 0 and strongHostBits > (W - 1) + 3 and strongGraftBits == 0:
            both_weak_host = np.bitwise_or(both, weakhost)
            weak_graft_bases = popcount(np.bitwise_and(np.invert(both_weak_host), weakgraft), 0, len(weakgraft) * 64)
            if weak_graft_bases < 3:
                return ret_host

        if order[3] == 1 and strongGraftBits > (W - 1) + 3 and strongHostBits == 0:
            both_weak_graft = np.bitwise_or(both, weakgraft)
            weak_host_bases = popcount(np.bitwise_and(np.invert(both_weak_graft), weakhost), 0, len(weakhost) * 64)
            if weak_host_bases < 3:
                return ret_graft

        return ret_amb

    return classify_xengsort_cov


def compile_get_kmer_values(mask, rcmode, h, buckets, count=True, ba=None):
    # tmask: mask in tuple form
    get_value = h.get_value
    get_bf1, get_bf2, get_bf3 = h.private.get_bf
    prefetch = h.private.prefetch_bucket
    get_subtable_subkey = h.private.get_subtable_subkey_from_key
    get_value_from_subtable_subkey = h.private.get_value_from_st_sk

    W = mask.w
    k = mask.k
    tmask = mask.tuple
    if count is False or ba is not None:
        assert count is False
        assert ba is not None
        mask = 0
        for i in tmask:
            mask += 2**i

        set_value_at = ba.set

    @njit(nogil=True,
        locals=dict(code=uint64, subkey=uint64, subtable=uint64, value=uint64))
    def count_values(ht, code, counts):
        subtable, subkey = get_subtable_subkey(code)
        if buckets == 1:
            prefetch(ht, subtable, get_bf2(subkey)[0])
        if buckets == 2:
            prefetch(ht, subtable, get_bf2(subkey)[0])
            prefetch(ht, subtable, get_bf3(subkey)[0])
        value = get_value_from_subtable_subkey(ht, subtable, subkey)  # value is 0 if code is not a key in the hash table
        counts[value] += 1
        return False # we never fail!

    @njit(nogil=True, locals=dict())
    def get_coverage(ht, code, pos, cov):
        counts = cov[0]
        cov = cov[1:]
        subtable, subkey = get_subtable_subkey(code)
        if buckets == 1:
            prefetch(ht, subtable, get_bf2(subkey)[0])
        if buckets == 2:
            prefetch(ht, subtable, get_bf2(subkey)[0])
            prefetch(ht, subtable, get_bf3(subkey)[0])
        value = get_value_from_subtable_subkey(ht, subtable, subkey)
        assert value != 4
        set_value_at(cov[value], pos, mask, W)
        counts[value] += 1
        return False # we never fail!

    # because the supplied function 'count_values' has ONE extra parameter (counts),
    # the generated function process_kmers also gets ONE extra parameter (counts)!
    if count:
        k, process_kmers = compile_kmer_processor(tmask, count_values, rcmode=rcmode)
    else:
        k, process_kmers = compile_positional_kmer_processor(tmask, get_coverage, rcmode=rcmode)

    @njit(nogil=True)
    def classify_read(ht, seq, values):
        process_kmers(ht, seq, 0, len(seq), values)

    return classify_read


def compile_classify_read_from_fastq(
        mode, mask, rcmode, bits, path, h, threads, pairs,
        bufsize=2**23, chunkreads=(2**23) // 200, quick=False,
        filt=False, count=False, prefetchlevel=0, params=dict(),
        compression="gz", show_progress=False):


    if compression != "none":
        compression = "." + compression
    else:
        compression = ""

    bitarrays = list(tuple(None for i in range(8)) for i in range(threads))
    ba = None
    count_kmers = True

    if mode == "count":
        debugprint0("- Using count based classification mode")
        classify = compile_count_based_classification(params)
    elif mode == "coverage":
        debugprint0("- using coverage based classification mode")
        count_kmers = False
        ba = bitarray(200)
        bitarrays = list(tuple(np.zeros(30, dtype=np.uint64) for i in range(8)) for i in range(threads))
        classify = compile_coverage_based_classification(ba, mask, params)
    elif mode == "quick":
        debugprint0("- using quick classification mode")
        assert False
    elif mode == 'bisulfite':
        debugprint0("- Using count based classification mode for bisulfite sequencing data")
        classify = compile_count_based_classification(params)
        ct_table = _TABLE_DNA_TO_2BITS.copy()
        ct_table[99] = 3
        ct_table[67] = 3
        quick_dna_to_2bits_ct = compile_quick_dna_to_2bits(ct_table)

        ga_table = _TABLE_DNA_TO_2BITS.copy()
        ga_table[103] = 0
        ga_table[71] = 0
        quick_dna_to_2bits_ga = compile_quick_dna_to_2bits(ga_table)
    else:
        raise ValueError(f"Unknown mode '{mode}'")

    get_kmer_values = compile_get_kmer_values(mask, rcmode, h, prefetchlevel, count_kmers, ba)
    _, twobit_to_code = compile_twobit_to_codes(mask, rcmode)

    get_value = h.get_value
    k, w = mask.k, mask.w



    @njit(nogil=True, locals=dict(
        third_kmer=uint64, third=uint64,
        thirdlast_kmer=uint64, thirdlast=uint64))
    def get_classification(ht, sq, kcount):
        quick_dna_to_2bits(sq)
        if quick:
            # get 2 k-mers (3rd and 3rd-last)
            third_kmer = twobit_to_code(sq, 2)
            thirdlast_kmer = twobit_to_code(sq, len(sq) - w - 2)
            # look up values of both k-mers, ignore weak status (good thing?!)
            third = get_value(ht, third_kmer) & uint64(3)
            thirdlast = get_value(ht, thirdlast_kmer) & uint64(3)
            if third == thirdlast and third != 3 and third != 0:
                return (third - 1)  # 2 -> 1,  1 -> 0
        kcount[:] = 0
        get_kmer_values(ht, sq, kcount)
        return classify(kcount)

    @njit(nogil=True, locals=dict(
        third_kmer1=uint64, third_sq1=uint64,
        third_kmer2=uint64, third_sq2=uint64,
        thirdlast_kmer1=uint64, thirdlast_sq1=uint64,
        thirdlast_kmer2=uint64, thirdlast_sq2=uint64))
    def get_paired_classification(ht, sq1, sq2, kcount):
        quick_dna_to_2bits(sq1)
        quick_dna_to_2bits(sq2)
        if quick:
            # get 4 k-mers (3rd and 3rd-last of both sequences)
            third_kmer1 = twobit_to_code(sq1, 2)
            thirdlast_kmer1 = twobit_to_code(sq1, len(sq1) - w - 2)
            third_kmer2 = twobit_to_code(sq2, 2)
            thirdlast_kmer2 = twobit_to_code(sq2, len(sq2) - w - 2)
            # look up values of all 4 k-mers, ignore weak status (good thing?!)
            third_sq1 = get_value(ht, third_kmer1) & uint64(3)
            thirdlast_sq1 = get_value(ht, thirdlast_kmer1) & uint64(3)
            third_sq2 = get_value(ht, third_kmer2) & uint64(3)
            thirdlast_sq2 = get_value(ht, thirdlast_kmer2) & uint64(3)
            if (third_sq1 == thirdlast_sq1 and third_sq1 == third_sq2 and third_sq1 == thirdlast_sq2) \
               and (third_sq1 != 3 and third_sq1 != 0):
                return (third_sq1 - 1)
        kcount[:] = 0
        get_kmer_values(ht, sq1, kcount)  # adds to kcount
        get_kmer_values(ht, sq2, kcount)  # adds to kcount
        return classify(kcount)

    @njit(nogil=True, locals=dict(
        third_kmer=uint64, third=uint64,
        thirdlast_kmer=uint64, thirdlast=uint64))
    def get_bisulfite_classification(ht, sq, kcount):
        # if quick:
        #     # get 2 k-mers (3rd and 3rd-last)
        #     third_kmer = twobit_to_code(sq, 2)
        #     thirdlast_kmer = twobit_to_code(sq, len(sq) - w - 2)
        #     # look up values of both k-mers, ignore weak status (good thing?!)
        #     third = get_value(ht, third_kmer) & uint64(3)
        #     thirdlast = get_value(ht, thirdlast_kmer) & uint64(3)
        #     if third == thirdlast and third != 3 and third != 0:
        #         return (third - 1)  # 2 -> 1,  1 -> 0
        get_kmer_values(ht, sq, kcount)
        return -1

    @njit(nogil=True)
    def classify_kmers_chunkwise(threadid, buf, linemarks, ht,
         ba_neither=None, ba_stronghost=None, ba_stronggraft=None, ba_both=None,
         ba_weakhost=None, ba_weakgraft=None, ba_weakboth=None):

        n = linemarks.shape[0]
        classifications = np.zeros(n, dtype=np.uint8)
        counts = np.zeros(8, dtype=np.uint32)
        if mode == "coverage":
            for i in range(n):
                counts[:] = 0
                # rest all bitarrays
                ba_neither.fill(0)
                ba_stronghost.fill(0)
                ba_stronggraft.fill(0)
                ba_both.fill(0)
                ba_weakhost.fill(0)
                ba_weakgraft.fill(0)
                ba_weakboth.fill(0)

                # get sequence
                sq = buf[linemarks[i, 0]:linemarks[i, 1]]

                # check if bitarray is big enoguh for the sequence
                seq_size = int(ceil(len(sq) / 64))
                if seq_size > ba_neither.size:
                    debugprint1("# increase array size to", seq_size, "sequence length=", len(sq))
                    # increase size buffer 1
                    ba_neither = np.zeros(seq_size, dtype=uint64)
                    ba_stronghost = np.zeros(seq_size, dtype=uint64)
                    ba_stronggraft = np.zeros(seq_size, dtype=uint64)
                    ba_both = np.zeros(seq_size, dtype=uint64)
                    ba_weakhost = np.zeros(seq_size, dtype=uint64)
                    ba_weakgraft = np.zeros(seq_size, dtype=uint64)
                    ba_weakboth = np.zeros(seq_size, dtype=uint64)

                 # tranlate seuqences to two bit encoding
                quick_dna_to_2bits(sq)

                # get values for each k-mer
                get_kmer_values(ht, sq, (counts, ba_neither, ba_stronghost, ba_stronggraft, ba_both,
                    ba_neither, ba_weakhost, ba_weakgraft, ba_weakboth))

                # classify the read based on the values
                classifications[i] = classify(counts, ba_neither, ba_stronghost, ba_stronggraft, ba_both,
                    ba_weakhost, ba_weakgraft, ba_weakboth, len(sq))

                # tranlaste the two bit encoding back
                twobits_to_dna_inplace(buf, linemarks[i, 0], linemarks[i, 1])

        elif mode == "count":
            for i in range(n):
                sq = buf[linemarks[i, 0]:linemarks[i, 1]]
                classifications[i] = get_classification(ht, sq, counts)
                twobits_to_dna_inplace(buf, linemarks[i, 0], linemarks[i, 1])
        elif mode == "bisulfite":
            local_seq = np.empty(250, dtype=np.uint8)
            for i in range(n):
                seq_len = linemarks[i, 1] - linemarks[i, 0]

                if seq_len > local_seq.size:
                    debugprint2('WGBS, local sequence length increased to ', seq_len * 2)
                    local_seq = np.empty(seq_len * 2, dtype=np.uint8)

                counts[:] = 0
                # C -> T
                local_seq[:seq_len] = buf[linemarks[i, 0]:linemarks[i, 1]]
                quick_dna_to_2bits_ct(local_seq[:seq_len])
                get_bisulfite_classification(ht, local_seq[:seq_len], counts)

                # G -> A
                local_seq[:seq_len] = buf[linemarks[i, 0]:linemarks[i, 1]]
                quick_dna_to_2bits_ga(local_seq[:seq_len])
                get_bisulfite_classification(ht, local_seq[:seq_len], counts)
                r1_clasification = classify(counts)
                classifications[i] = r1_clasification

        else:
            raise ValueError(f"Classification method {mode} is not supported.")

        return threadid, (classifications, linemarks)

    @njit(nogil=True)
    def classify_paired_kmers_chunkwise(threadid, buf, linemarks, buf1, linemarks1, ht,
         ba_neither=None, ba_stronghost=None, ba_stronggraft=None, ba_both=None,
         ba_weakhost=None, ba_weakgraft=None, ba_weakboth=None):
        n = linemarks.shape[0]
        classifications = np.zeros(n, dtype=np.uint8)
        counts = np.zeros(8, dtype=np.uint32)
        if mode == "coverage":
            for i in range(n):
                counts[:] = 0
                # rest all bitarrays
                ba_neither.fill(0)
                ba_stronghost.fill(0)
                ba_stronggraft.fill(0)
                ba_both.fill(0)
                ba_weakhost.fill(0)
                ba_weakgraft.fill(0)
                ba_weakboth.fill(0)

                # get both sequences
                sq1 = buf[linemarks[i, 0]:linemarks[i, 1]]
                sq2 = buf1[linemarks1[i, 0]:linemarks1[i, 1]]

                # check if bitarrays are big enough for both sequences
                seq1_size = int(ceil(len(sq1) / 64))
                seq2_size = int(ceil(len(sq2) / 64))
                if seq1_size + seq2_size > ba_neither.size:
                    debugprint1("# increase array size to", seq1_size + seq2_size)
                    # increase size buffer 1
                    ba_neither = np.zeros(seq1_size + seq2_size, dtype=uint64)
                    ba_stronghost = np.zeros(seq1_size + seq2_size, dtype=uint64)
                    ba_stronggraft = np.zeros(seq1_size + seq2_size, dtype=uint64)
                    ba_both = np.zeros(seq1_size + seq2_size, dtype=uint64)
                    ba_weakhost = np.zeros(seq1_size + seq2_size, dtype=uint64)
                    ba_weakgraft = np.zeros(seq1_size + seq2_size, dtype=uint64)
                    ba_weakboth = np.zeros(seq1_size + seq2_size, dtype=uint64)

                # tranlate seuqences to two bit encoding
                quick_dna_to_2bits(sq1)
                quick_dna_to_2bits(sq2)

                # get values for each k-mer
                get_kmer_values(ht, sq1, (counts, ba_neither, ba_stronghost, ba_stronggraft, ba_both,
                    ba_neither, ba_weakhost, ba_weakgraft, ba_weakboth))

                get_kmer_values(ht, sq2, (counts, ba_neither[seq1_size:], ba_stronghost[seq1_size:],
                    ba_stronggraft[seq1_size:], ba_both[seq1_size:], ba_neither[seq1_size:],
                    ba_weakhost[seq1_size:], ba_weakgraft[seq1_size:], ba_weakboth[seq1_size:]))

                # classify the read based on the values
                classifications[i] = classify(counts, ba_neither, ba_stronghost, ba_stronggraft, ba_both,
                    ba_weakhost, ba_weakgraft, ba_weakboth, len(sq1) + len(sq2))

                # tranlaste the two bit encoding back
                twobits_to_dna_inplace(buf, linemarks[i, 0], linemarks[i, 1])
                twobits_to_dna_inplace(buf1, linemarks1[i, 0], linemarks1[i, 1])
        elif mode == "count":
            for i in range(n):
                sq1 = buf[linemarks[i, 0]:linemarks[i, 1]]
                sq2 = buf1[linemarks1[i, 0]:linemarks1[i, 1]]
                classifications[i] = get_paired_classification(ht, sq1, sq2, counts)
                twobits_to_dna_inplace(buf, linemarks[i, 0], linemarks[i, 1])
                twobits_to_dna_inplace(buf1, linemarks1[i, 0], linemarks1[i, 1])
        elif mode == "bisulfite":

            local_seq = np.empty(250, dtype=np.uint8)
            for i in range(n):
                seq_len = linemarks[i, 1] - linemarks[i, 0]
                seq_len1 = linemarks1[i, 1] - linemarks1[i, 0]

                max_seq_len = max(seq_len, seq_len1)
                if max_seq_len > local_seq.size:
                    debugprint2('WGBS, local sequence length increased to ', max_seq_len * 2)
                    local_seq = np.empty(max_seq_len * 2, dtype=np.uint8)

                # R1
                counts[:] = 0
                # C -> T
                local_seq[:seq_len] = buf[linemarks[i, 0]:linemarks[i, 1]]
                quick_dna_to_2bits_ct(local_seq[:seq_len])
                q1 = get_bisulfite_classification(ht, local_seq[:seq_len], counts)
                # G -> A
                local_seq[:seq_len] = buf[linemarks[i, 0]:linemarks[i, 1]]
                quick_dna_to_2bits_ct(local_seq[:seq_len])
                q2 = get_bisulfite_classification(ht, local_seq[:seq_len], counts)
                r1_clasification = classify(counts)

                # R2
                counts[:] = 0
                # C -> T
                local_seq[:seq_len1] = buf1[linemarks1[i, 0]:linemarks1[i, 1]]
                quick_dna_to_2bits_ga(local_seq[:seq_len1])
                get_bisulfite_classification(ht, local_seq[:seq_len1], counts)

                # G -> A
                local_seq[:seq_len1] = buf1[linemarks1[i, 0]:linemarks1[i, 1]]
                quick_dna_to_2bits_ga(local_seq[:seq_len1])
                get_bisulfite_classification(ht, local_seq[:seq_len1], counts)
                r2_clasification = classify(counts)

                if r1_clasification == r2_clasification:
                    classifications[i] = r1_clasification
                else:
                    classifications[i] = 2  # ambiguous
        else:
            raise ValueError(f"{mode} is not a supported classification mode")

        return threadid, (classifications, linemarks, linemarks1)

    @njit(nogil=True)
    def get_borders(linemarks, threads):
        n = linemarks.shape[0]
        perthread = (n + (threads - 1)) // threads
        borders = np.empty(threads + 1, dtype=uint32)
        for i in range(threads):
            borders[i] = min(i * perthread, n)
        borders[threads] = n
        return borders

    class dummy_contextmgr():
        """a context manager that does nothing at all"""
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def write(*_):
            pass

        def flush(*_):
            pass

    @contextmanager
    def cond_contextmgr(name, suffix, count, filt):
        if count and filt:
            raise ValueError("ERROR: cannot use both --count and --filter option at the same time.")
        if count:
            yield dummy_contextmgr()
        elif filt:
            if "graft" in suffix:
                with OutputFileHandler(name + suffix) as outfile:
                    yield outfile.file
            else:
                yield dummy_contextmgr()
        else:
            with OutputFileHandler(name + suffix) as outfile:
                yield outfile.file

    def classify_read_from_fastq_paired(fastqs, pairs, ht):
        counts = [0, 0, 0, 0, 0]  # host, graft, amb., both, neither
        nprocessed = 0
        with cond_contextmgr(path, f"-host.1.fq{compression}", count, filt) as host1, \
             cond_contextmgr(path, f"-host.2.fq{compression}", count, filt) as host2, \
             cond_contextmgr(path, f"-graft.1.fq{compression}", count, filt) as graft1, \
             cond_contextmgr(path, f"-graft.2.fq{compression}", count, filt) as graft2, \
             cond_contextmgr(path, f"-ambiguous.1.fq{compression}", count, filt) as ambiguous1, \
             cond_contextmgr(path, f"-ambiguous.2.fq{compression}", count, filt) as ambiguous2, \
             cond_contextmgr(path, f"-both.1.fq{compression}", count, filt) as both1, \
             cond_contextmgr(path, f"-both.2.fq{compression}", count, filt) as both2, \
             cond_contextmgr(path, f"-neither.1.fq{compression}", count, filt) as neither1, \
             cond_contextmgr(path, f"-neither.2.fq{compression}", count, filt) as neither2:
            streams = ((host1, host2), (graft1, graft2), (ambiguous1, ambiguous2), (both1, both2), (neither1, neither2))

            with ThreadPoolExecutor(max_workers=threads) as executor:
                for fastq1, fastq2 in zip(fastqs, pairs):
                    with InputFileHandler(fastq1) as fq, \
                         InputFileHandler(fastq2) as fp:
                        for chunk in fastq_chunks_paired((fq, fp), bufsize=bufsize * threads, maxreads=chunkreads * threads):
                            if show_progress:
                                debugprint0(f"Processed {nprocessed} reads", end="\r")
                            # c0 buffer of first fastq file
                            # c1 linemarks for the first fastq file
                            # c2 buffer of the second fastq file
                            # c3 linemarks of the second fastq file
                            c0, c1, c2, c3 = chunk
                            borders = get_borders(c1, threads)  # the number of sequences in c1 and c3 is equal
                            futures = [executor.submit(
                                classify_paired_kmers_chunkwise, i, c0, c1[borders[i]:borders[i + 1]],
                                c2, c3[borders[i]:borders[i + 1]], ht,
                                bitarrays[i][0], bitarrays[i][1], bitarrays[i][2], bitarrays[i][3],
                                bitarrays[i][4], bitarrays[i][5], bitarrays[i][6])
                                for i in range(threads)]
                            for fut in as_completed(futures):
                                threadid, (classifications, linemarks, linemarks2) = fut.result()
                                # bitarrays[t] = n_bitarrays
                                start_write = datetime.datetime.now()
                                if count:
                                    for seq in range(linemarks.shape[0]):
                                        cl = classifications[seq]
                                        counts[cl] += 1
                                elif filt:
                                    for seq in range(linemarks.shape[0]):
                                        cl = classifications[seq]
                                        counts[cl] += 1
                                        if cl == 1:  # graft
                                            lms1, lms2 = linemarks[seq], linemarks2[seq]
                                            streams[cl][0].write(c0[lms1[2]:lms1[3]])
                                            streams[cl][1].write(c2[lms2[2]:lms2[3]])
                                else:
                                    for seq in range(linemarks.shape[0]):
                                        cl = classifications[seq]
                                        counts[cl] += 1
                                        lms1, lms2 = linemarks[seq], linemarks2[seq]
                                        streams[cl][0].write(c0[lms1[2]:lms1[3]])
                                        streams[cl][1].write(c2[lms2[2]:lms2[3]])
                            nprocessed += len(c1)
                    # all chunks processed
            if show_progress:
                debugprint0(f"Processed {nprocessed} reads")
            # ThreadPool closed
            for s in streams:
                s[0].flush()
                s[1].flush()
            return counts

    def classify_read_from_fastq_single(fastqs, ht):
        counts = [0, 0, 0, 0, 0]
        nprocessed = 0
        with cond_contextmgr(path, f"-host.fq{compression}", count, filt) as host, \
             cond_contextmgr(path, f"-graft.fq{compression}", count, filt) as graft, \
             cond_contextmgr(path, f"-ambiguous.fq{compression}", count, filt) as ambiguous, \
             cond_contextmgr(path, f"-both.fq{compression}", count, filt) as both, \
             cond_contextmgr(path, f"-neither.fq{compression}", count, filt) as neither:
            streams = (host, graft, ambiguous, both, neither)

            running_jobs = []
            with ThreadPoolExecutor(max_workers=threads) as executor:
                for fastq in fastqs:
                    with InputFileHandler(fastq) as fq:
                        for chunk in fastq_chunks(fq, bufsize=bufsize * threads, maxreads=chunkreads * threads):
                            if show_progress:
                                debugprint0(f"Processed {nprocessed} reads of {fastq}", end="\r")
                            # c0 = buffer
                            # c1 = linemarks
                            c0, c1 = chunk
                            borders = get_borders(c1, threads)
                            futures = [executor.submit(
                                classify_kmers_chunkwise, i, c0, c1[borders[i]:borders[i + 1]], ht,
                                bitarrays[i][0], bitarrays[i][1], bitarrays[i][2], bitarrays[i][3],
                                bitarrays[i][4], bitarrays[i][5], bitarrays[i][6])
                                for i in range(threads)]
                            for fut in as_completed(futures):
                                threadid, (classifications, linemarks) = fut.result()
                                if count:
                                    for seq in range(linemarks.shape[0]):
                                        cl = classifications[seq]
                                        counts[cl] += 1
                                elif filt:
                                    for seq in range(linemarks.shape[0]):
                                        cl = classifications[seq]
                                        counts[cl] += 1
                                        if cl == 1:  # graft
                                            lms = linemarks[seq]
                                            streams[cl].write(c0[lms[2]:lms[3]])
                                else:
                                    for seq in range(linemarks.shape[0]):
                                        cl = classifications[seq]
                                        counts[cl] += 1
                                        lms = linemarks[seq]
                                        streams[cl].write(c0[lms[2]:lms[3]])

                            nprocessed += len(c1)
                # all chunks processed
            # ThreadPool closed
            if show_progress:
                debugprint0(f"Processed {nprocessed} reads of {fastq}")
            for s in streams:
                s.flush()
        return counts

    classify_read_from_fastq = (
        classify_read_from_fastq_paired if pairs
        else classify_read_from_fastq_single)
    return classify_read_from_fastq


def print_class_stats(prefix, stats):
    classes = ["host", "graft", "ambiguous", "both", "neither"]

    percentages = [i / sum(stats) * 100 for i in stats]
    str_counts = "\t".join(str(i) for i in stats)
    ndigits = max(map(lambda x: len(str(x)), stats))

    print("\n## Classification Statistics")
    print("\n```")
    print("prefix\thost\tgraft\tambiguous\tboth\tneither")
    print(f"{prefix}\t{str_counts}")
    print("```\n")
    print("```")
    print(f"| prefix    | {prefix} ")
    for i in range(len(classes)):
        print(f"| {classes[i]:9s} | {stats[i]:{ndigits}d} | {percentages[i]:5.2f}% |")
    print("```")
    print()


def main(args):
    """main method for classifying reads"""
    global debugprint0, debugprint1, debugprint2
    global timestamp0, timestamp1, timestamp2
    debugprint0, debugprint1, debugprint2 = debug.debugprint
    timestamp0, timestamp1, timestamp2 = debug.timestamp

    starttime = timestamp0(msg="\n# Xengsort classify")
    debugprint0("\n- (c) 2019-2023 by Sven Rahmann, Jens Zentgraf, Algorithmic Bioinformatics, Saarland University")
    debugprint0("- Licensed under the MIT License")

    # Load hash table (index)
    h, values, infotup = load_hash(args.index, shared_memory=args.shared)
    (hashinfo, valueinfo, optinfo, appinfo) = infotup
    bits = values.bits
    mask = create_mask(appinfo['mask'])
    k, tmask = mask.k, mask.tuple
    assert k == appinfo['k']
    rcmode = appinfo.get('rcmode', values.RCMODE)
    if rcmode is None:
        rcmode = values.RCMODE
    if not isinstance(rcmode, str):
        rcmode = rcmode.decode("ASCII")
    chunksize = int(args.chunksize * 2**20)
    chunkreads = args.chunkreads or (chunksize // 200)

    # classify reads from either FASTQ or FASTA files
    timestamp1(msg='- Begin classification')
    debugprint1(f"- mask: {k=}, w={tmask[-1]+1}, tuple={tmask}")

    # See if FASTQ was given
    quick = False
    mode = args.classification
    if mode == "quick":
        mode = "count"
        quick = True
    if 'bisulfite' in appinfo:
        if appinfo['bisulfite']:
            debugprint0('- The provided index is build for WGBS analysis.\n The classification mode will be switched to bisulfite.')
            mode = 'bisulfite'
    if mode == 'bisulfite':
        params = args["params_" + 'count']
        params = args["params_" + 'bisulfite']
    else:
        params = args["params_" + mode]
    if not args.fastq:
        # NO --fastq given, nothing to do
        debugprint0("- No FASTQ files to classify. Nothing to do. Have a good day.")
        exit(17)

    # check if same number of fastq files are provided for paired end reads
    paired = False
    if args.pairs:
        if len(args.fastq) != len(args.pairs):
            raise ValueError("- Different number of files in --fastq and --pairs")
        paired = True

    if args.prefix is None:
        if len(args.fastq) > 1:
            raise ValueError("- Please provide an output name using --out or -o")
        args.prefix = Path(args.fastq[0]).stem
        if args.prefix.endswith(("fq", "fastq")):
            args.prefix = Path(args.prefix).stem

    if args.prefix.endswith("/"):
        fastqname = Path(args.fastq[0]).stem
        if fastqname.endswith(("fq", "fastq")):
            args.prefix = args.prefix + Path(fastqname).stem
        if len(args.fastq) > 1:
            debugprint0("- Warning: No output file name specified.")
            debugprint0(f"  The output will be saved in {args.prefix}")

    # compile classification method
    classify_read_from_fastq = compile_classify_read_from_fastq(
        mode, mask, rcmode, bits,
        args.prefix, h, args.threads, paired,
        bufsize=chunksize, chunkreads=chunkreads, quick=quick,
        filt=args.filter, count=args.count, prefetchlevel=args.prefetchlevel,
        params=params, compression=args.compression,
        show_progress=args.progress)

    if paired:
        counts = classify_read_from_fastq(args.fastq, args.pairs, h.hashtable)
    else:
        counts = classify_read_from_fastq(args.fastq, h.hashtable)
    print_class_stats(args.prefix, counts)

    debugprint0("## Running time statistics\n")
    timestamp0(starttime, msg="- Running time")
    timestamp0(starttime, msg="- Running time", minutes=True)
    timestamp0(msg="- Done.")
