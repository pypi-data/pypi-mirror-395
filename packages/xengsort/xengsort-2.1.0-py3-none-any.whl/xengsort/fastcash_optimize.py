import datetime
# from pprint import pprint
from math import log, ceil

import numpy as np
from numba import njit, uint64, int64, uint32, uint8, boolean
from importlib import import_module

from .lowlevel import debug
from .lowlevel.bitarray import bitarray
from .lowlevel.intbitarray import intbitarray, IntBitArray
from .io.hashio import save_hash, load_hash
from .mask import create_mask
from .subtable_hashfunctions import compile_get_subtable_subkey_from_key, compile_get_bucket_fpr_from_subkey
from .srhash import get_nbuckets
from .mathutils import bitsfor
from concurrent.futures import ThreadPoolExecutor, wait
from .srhash import print_statistics
from .optilp import optimize_ilp


def show_memory(*arrays, names=None):
    total = 0
    if names is None:
        names = [f"array{i}" for i in range(1, len(arrays) + 1)]
    for a, name in zip(arrays, names):
        if a is None:
            continue
        if isinstance(a, np.ndarray):
            size = a.size
            b = a.nbytes
            dtype = str(a.dtype)
        elif isinstance(a, IntBitArray):
            size = a.size
            b = a.capacity_bytes
            dtype = f'bits{a.width}'
        elif isinstance(a, StructBitArray):
            size = a.size
            b = a.capacity_bytes
            w = str(tuple(a.widths)).replace(" ", "")
            dtype = f'bits{a.width}{w}'
        else:
            raise RuntimeError(f"unknown array type '{type(a)}'")
        print(f"{name}: {size} x {dtype} = {b/1E6:.3f} MBytes = {b/1E9:.3f} GBytes")
        total += b
    print(f"TOTAL: {total/1E6:.3f} MBytes = {total/1E9:.3f} GBytes")


def compile_calc_subkeys(keys, subkeys, subtables, nkeys, get_st_sk):
    get_key = keys.get
    set_sk = subkeys.set
    set_st = subtables.set

    @njit(nogil=True, locals=dict(st=uint64, sk=uint64))
    def calc_subkeys(akey, ask, ast, st_size):
        for i in range(nkeys):
            st, sk = get_st_sk(get_key(akey, i))
            set_sk(ask, i, sk)
            set_st(ast, i, st)
            st_size[st] += 1

    return calc_subkeys


def compile_split_bitarrays(subkeys, subtables, nkeys):
    get_key = subkeys.get
    set_key = subkeys.set
    get_st = subtables.get

    @njit(nogil=True, locals=dict())
    def split_bitarrays(ask, ast, st_keys):
        pos = np.zeros(len(st_keys), dtype=np.int64)
        for i in range(nkeys):
            key = get_key(ask, i)
            st = get_st(ast, i)
            set_key(st_keys[st], pos[st], key)
            pos[st] += 1
    return split_bitarrays


@debug.deprecated
def compile_merge_choices(choices, subtables, nkeys):
    get_choice = choices.get
    set_choice = choices.set
    get_st = subtables.get

    def merge_choices(achoices, subtable_choices, asubtables):
        pos = np.zeros(nkeys, dtype=np.int64)
        for i in range(nkeys):
            st = get_st(asubtables, i)
            c = get_choice(subtable_choices[st], pos[st])
            pos[st] += 1
            set_choice(achoices, i, c)

    return merge_choices


def check_choices(get_c, ac, get_k, ak, get_bfs, nkeys, nbuckets, bucketsize):
    fill = np.zeros(nbuckets, dtype=np.uint8)
    for i in range(nkeys):
        sk = get_k(ak, i)
        c = get_c(ac, i) - 1
        p, _ = get_bfs[c](sk)
        fill[p] += 1
    assert (fill <= bucketsize).all()


def optimize(nkmers_tuple, bucketsize, bucketcount, hfs, kmer_bitarrays, threads):
    print("Start creating arrays")
    nsubtables = len(nkmers_tuple)
    get_kmer = kmer_bitarrays[0].get
    set_kmer = kmer_bitarrays[0].set

    bucket_fill_tuple = [intbitarray(bucketcount, np.ceil(np.log2(bucketsize + 1))) for _ in range(nsubtables)]
    getbucketfill = bucket_fill_tuple[0].get
    setbucketfill = bucket_fill_tuple[0].set

    hf1 = hfs[0]
    hf2 = hfs[1]
    hf3 = hfs[2]

    ukmerr = [intbitarray(nkmers, 2) for nkmers in nkmers_tuple]
    get_bits_at = ukmerr[0].get  # (array, startbit, nbits=1)
    set_bits_at = ukmerr[0].set

    visited_kmer_tuple = [bitarray(nkmers) for nkmers in nkmers_tuple]
    is_active = is_visited = visited_kmer_tuple[0].get
    set_active = set_visited = visited_kmer_tuple[0].set

    prev_bucket_tuple = [intbitarray(nkmers, 2) for nkmers in nkmers_tuple]
    get_prev_bucket = prev_bucket_tuple[0].get
    set_prev_bucket = prev_bucket_tuple[0].set

    @njit(nogil=True)
    def calcStats(ukmer, pF, nkmers):
        val = 0
        choiceStat = np.zeros(3, dtype=np.uint64)
        for i in range(nkmers):
            choice = int(get_bits_at(ukmer, i))
            val += choice
            choiceStat[choice - 1] += 1
        bucketFillStat = np.zeros(bucketsize + 1, dtype=np.uint64)
        for i in range(bucketcount):
            bucketFillStat[getbucketfill(pF, i)] += 1

        debugprint0("costs:", val, val / nkmers)
        debugprint0("choice Stat:")
        debugprint0("1: ", choiceStat[0])
        debugprint0("2: ", choiceStat[1])
        debugprint0("3: ", choiceStat[2])
        debugprint0("bucket fill:")
        for i, j in enumerate(bucketFillStat):
            debugprint0(i, ": ", j)

    @njit(nogil=True, )
    def checkL(T_starts, T_i, T_j, ukmer, get, set, nkmers, bucketcount):
        for i in range(0, T_starts[-1]):
            if T_i[i] != np.iinfo(uint64).max:
                choice = int(get(ukmer, T_i[i] * 2, 2))
                hf = int(get(T_j, i * 2, 2))
                # assert(choice != hf)

    @njit(nogil=True, locals=dict(kmer=uint64, i=int64,
          choice=uint8, h1=uint64, h2=uint64, h3=uint64))
    def build_T_arrays(nkmers,  # number of k-mers
                       kmers,  # compressed array of k-mer codes
                       bucketcount,  # number of buckets
                       ukmer,  # hf that is used used to assign a k-mer
                       T_starts,  # Array of all indices at which a bucket starts
                       T_i,
                       T_j,
                       ):
        """
        T_starts: index at which each bucket i starts in T_i and T_j
        T_i: stores the index of the k-mer in the compressed k-mer set (kmers)
        T_j: stores the hash function which is used to assign kmers[T_i[i]] to the current bucket

        We compute for each bucket which elements can be assigned to this bucket but currently are assigned to another bucket or not assigned at all.
        This is split in two phases:
        1: Get the number of elements that can be assigned to each bucket but currently are not. This is stored in mFill
        2: For each bucket i store in T_starts at which position it starts in T_j and T_i
        3: Update T_j and T_i using T_starts
        """
        set = T_j_set
        get = T_j_get

        # For each bucket get the number of elements that can be assigned to the bucket but currently are not
        # If for one element multiple hash function point to the same bucket only count one
        mFill = np.zeros(bucketcount, dtype=np.uint64)
        for i in range(nkmers):
            choice = int(get_bits_at(ukmer, i))
            h1 = hf1(int(get_kmer(kmers, i)))[0]
            h2 = hf2(int(get_kmer(kmers, i)))[0]
            h3 = hf3(int(get_kmer(kmers, i)))[0]
            if choice == 0:
                mFill[h1] += 1
                if h2 != h1:
                    mFill[h2] += 1
                if h3 != h1 and h3 != h2:
                    mFill[h3] += 1
            elif choice == 1:
                if h2 != h1:
                    mFill[h2] += 1
                if h3 != h2 and h3 != h1:
                    mFill[h3] += 1
            elif choice == 2:
                # We do not need to check if h1 == h2 because we only did the initialization.
                # if h1==h2 the choice would be 1.
                mFill[h1] += 1
                if h3 != h1 and h3 != h2:
                    mFill[h3] += 1
            elif choice == 3:
                # This should not happen.
                # At this point all inserted elements used the first or second hash function.
                # We only run the init() function.
                raise RuntimeError("Error in build_T_arrays, choice cannot be 3")

            else:
                assert False, "choice must be in [0...3] "

        # store all indices where a new bucket begins
        for i in range(1, bucketcount + 1):
            T_starts_set(T_starts, i, T_starts_get(T_starts, (i - 1)) + mFill[i - 1])

        # Update T_i and T_j with for each bucket

        pFill = np.zeros(bucketcount, dtype=np.uint32)
        # pFill = mFill
        for i in range(nkmers):
            h1 = hf1(int(get_kmer(kmers, i)))[0]
            h2 = hf2(int(get_kmer(kmers, i)))[0]
            h3 = hf3(int(get_kmer(kmers, i)))[0]
            choice = int(get_bits_at(ukmer, i))
            if choice == 0:
                T_i_set(T_i, (T_starts_get(T_starts, h1) + pFill[h1]), i)
                set(T_j, (T_starts_get(T_starts, h1) + pFill[h1]), 1)
                pFill[h1] += 1

                if h2 != h1:
                    T_i_set(T_i, (T_starts_get(T_starts, h2) + pFill[h2]), i)
                    set(T_j, (T_starts_get(T_starts, h2) + pFill[h2]), 2)
                    pFill[h2] += 1
                if h3 != h1 and h3 != h2:
                    T_i_set(T_i, T_starts_get(T_starts, h3) + pFill[h3], i)
                    set(T_j, (T_starts_get(T_starts, h3) + pFill[h3]), 3)
                    pFill[h3] += 1

            elif choice == 1:
                if h2 != h1:
                    T_i_set(T_i, (T_starts_get(T_starts, h2) + pFill[h2]), i)
                    set(T_j, (T_starts_get(T_starts, h2) + pFill[h2]), 2)
                    pFill[h2] += 1

                if h3 != h2 and h3 != h1:
                    T_i_set(T_i, (T_starts_get(T_starts, h3) + pFill[h3]), i)
                    set(T_j, (T_starts_get(T_starts, h3) + pFill[h3]), 3)
                    pFill[h3] += 1

            elif choice == 2:
                T_i_set(T_i, (T_starts_get(T_starts, h1) + pFill[h1]), i)
                set(T_j, (T_starts_get(T_starts, h1) + pFill[h1]), 1)
                pFill[h1] += 1

                if h3 != h1 and h3 != h2:
                    T_i_set(T_i, (T_starts_get(T_starts, h3) + pFill[h3]), i)
                    set(T_j, (T_starts_get(T_starts, h3) + pFill[h3]), 3)
                    pFill[h3] += 1

            elif int(get_bits_at(ukmer, i)) == 3:
                # This should not happen.
                # At this point all inserted elements use the first or second hash function.
                # We only run the init() function.
                raise RuntimeError("Error in build_T_arrays, choice cannot be 3")

    @njit(nogil=True, locals=dict(bucket=uint64, bucketFill=uint8))
    def _init(pF, bucketcount, bucketsize, ukmer, kmers, nkmers):
        # Initialization passes:
        # Insert as many elements as possible only using the first and second hash functions without moving elements.

        # Insert as many elements as possible using only the first hash function
        for i in range(nkmers):
            bucket = hf1(int(get_kmer(kmers, i)))[0]
            bucketFill = getbucketfill(pF, bucket)
            if bucketFill != bucketsize:
                setbucketfill(pF, bucket, bucketFill + 1)
                set_bits_at(ukmer, i, 1)

        count = 0
        # Insert as many of the remaining elements as possible only using the second hashfunction
        for i in range(nkmers):
            if int(get_bits_at(ukmer, i)) == 0:
                bucket = hf2(int(get_kmer(kmers, i)))[0]
                bucketFill = getbucketfill(pF, bucket)
                if bucketFill != bucketsize:
                    setbucketfill(pF, bucket, bucketFill + 1)
                    set_bits_at(ukmer, i, 2)
                else:
                    count += 1

        debugprint2("Number of not inserted k-mers after initialization:", count)
        return count

    @njit(nogil=True, locals=dict(node=uint64, bucket_choice=uint64, pbucket=uint64, bucketFill=uint64, choice=uint64))
    def alternatePaths(prev_kmer, prev_bucket, ukmer, pF, bucketcost, visitedKmer, kmers, nkmers, T_starts, T_j, T_i):
        count = 0
        """
        Iterate over all k-mers; if a k-mer is not assigned insert it following the calculated way
        """

        for skmer in range(nkmers):
            if int(get_bits_at(ukmer, skmer)) != 0:
                continue

            visited = False
            node = skmer
            while node != nkmers + 1:
                if int(is_visited(visitedKmer, node)):
                    visited = True
                    break

                bucket_choice = int(get_prev_bucket(prev_bucket, node))
                if bucket_choice == 1:
                    pbucket = hf1(int(get_kmer(kmers, node)))[0]
                elif bucket_choice == 2:
                    pbucket = hf2(int(get_kmer(kmers, node)))[0]
                elif bucket_choice == 3:
                    pbucket = hf3(int(get_kmer(kmers, node)))[0]

                if prev_kmer_get(prev_kmer, pbucket) == nkmers + 1:
                    if getbucketfill(pF, pbucket) == bucketsize:
                        visited = True
                        break
                node = prev_kmer_get(prev_kmer, pbucket)

            if visited:
                continue

            count += 1
            node = skmer
            while node != np.iinfo(np.uint32).max:
                set_visited(visitedKmer, node, 1)

                bucket_choice = int(get_prev_bucket(prev_bucket, node))

                if bucket_choice == 1:
                    set_bits_at(ukmer, node, 1)
                    pbucket = hf1(int(get_kmer(kmers, node)))[0]
                elif bucket_choice == 2:
                    set_bits_at(ukmer, node, 2)
                    pbucket = hf2(int(get_kmer(kmers, node)))[0]
                elif bucket_choice == 3:
                    set_bits_at(ukmer, node, 3)
                    pbucket = hf3(int(get_kmer(kmers, node)))[0]
                else:
                    assert False

                bucketFill = getbucketfill(pF, pbucket)
                if bucketFill != bucketsize:
                    for i in range(T_starts_get(T_starts, pbucket), T_starts_get(T_starts, pbucket + 1)):
                        if T_i_get(T_i, i) == node:
                            setbucketfill(pF, pbucket, bucketFill + 1)
                            T_i_set(T_i, i, nkmers + 1)
                            T_j_set(T_j, i, 0)
                            break
                    break

                for i in range(T_starts_get(T_starts, pbucket), T_starts_get(T_starts, pbucket + 1)):
                    if T_i_get(T_i, i) == node:
                        T_i_set(T_i, i, prev_kmer_get(prev_kmer, pbucket))
                        choice = int(get_bits_at(ukmer, prev_kmer_get(prev_kmer, pbucket)))
                        T_j_set(T_j, i, choice)
                        break

                node = prev_kmer_get(prev_kmer, pbucket)

        return count

    @njit(nogil=True, locals=dict(i=int64, changes=boolean, kmer=uint32, bucket=uint32,
          choice=uint8, hashfunc=uint8, prevbucket=uint64))
    def findPaths(T_i, T_starts, T_j, bucketcost, bucketcount, prev_bucket, prev_kmer, ukmer, activebucket, pF, kmers, nkmers):
        """
        Calculate all path beginning at empty buckets.
        """

        for i in range(bucketcount):
            val = getbucketfill(pF, i)
            if val < bucketsize:
                bucketcost[i] = 0
                set_active(activebucket, i, 1)

        changes = True
        count = 0
        # TODO can we replace this with a heap/queue or something?
        # It takes a while to check all buckets in every while iteration

        while changes:
            changes = False
            for bucket in range(bucketcount):
                if int(is_active(activebucket, bucket)) == 0:
                    continue

                set_active(activebucket, bucket, 0)
                count += 1
                for i in range(T_starts_get(T_starts, bucket), T_starts_get(T_starts, bucket + 1)):
                    kmer = T_i_get(T_i, i)

                    if kmer == nkmers + 1:
                        continue

                    hashfunc = int(T_j_get(T_j, i))
                    choice = int(get_bits_at(ukmer, kmer))

                    if choice == 0:
                        if int(get_prev_bucket(prev_bucket, kmer)) == 0:
                            set_prev_bucket(prev_bucket, kmer, hashfunc)
                        else:
                            prevbucketHashfunc = int(get_prev_bucket(prev_bucket, kmer))
                            if prevbucketHashfunc == 1:
                                prevbucket = hf1(int(get_kmer(kmers, kmer)))[0]
                            elif prevbucketHashfunc == 2:
                                prevbucket = hf2(int(get_kmer(kmers, kmer)))[0]
                            elif prevbucketHashfunc == 3:
                                prevbucket = hf3(int(get_kmer(kmers, kmer)))[0]
                            if bucketcost[bucket] + hashfunc < bucketcost[prevbucket] + prevbucketHashfunc:
                                set_prev_bucket(prev_bucket, kmer, hashfunc)
                        continue
                    elif choice == 1:
                        choicebucket = hf1(int(get_kmer(kmers, kmer)))[0]
                    elif choice == 2:
                        choicebucket = hf2(int(get_kmer(kmers, kmer)))[0]
                    elif choice == 3:
                        choicebucket = hf3(int(get_kmer(kmers, kmer)))[0]
                    else:
                        assert False, "No valid choice"

                    if bucketcost[choicebucket] <= bucketcost[bucket] - choice + hashfunc:
                        continue

                    set_prev_bucket(prev_bucket, kmer, hashfunc)

                    set_active(activebucket, choicebucket, 1)
                    bucketcost[choicebucket] = bucketcost[bucket] - choice + hashfunc
                    prev_kmer_set(prev_kmer, choicebucket, kmer)
                    changes = True

        debugprint2("Number of updates in bucketcost: ", count)

    @njit(nogil=True)
    def startPasses(pF, n_unassigned_kmers, bucketcount, prev_kmer, bucketcost, bucketsize, ukmer, visitedKmer, activebucket, kmers, nkmers, prev_bucket, T_starts, T_i, T_j):
        passes = 1
        while n_unassigned_kmers > 0:
            debugprint2("pass: ", passes)
            debugprint2("Computing minimum cost paths")
            findPaths(T_i, T_starts, T_j, bucketcost, bucketcount, prev_bucket, prev_kmer, ukmer, activebucket, pF, kmers, nkmers)
            debugprint2("Moving and inserting elements")
            # checkL(T_starts, T_i, T_j, ukmer, get_bits_at, set_bits_at, nkmers, bucketcount)
            insertedKmer = alternatePaths(prev_kmer, prev_bucket, ukmer, pF, bucketcost, visitedKmer, kmers, nkmers, T_starts, T_j, T_i)
            debugprint2("Number of inserted k-mers:", insertedKmer)
            # checkL(T_starts, T_i, T_j, ukmer, get_bits_at, set_bits_at, nkmers, bucketcount)
            n_unassigned_kmers -= insertedKmer
            debugprint2("Number of open k-mers:", n_unassigned_kmers)
            bucketcost.fill(np.iinfo(np.int16).max)
            prev_kmer.fill(np.iinfo(np.uint32).max)

            for i in range(nkmers):
                set_visited(visitedKmer, i, 0)
                set_prev_bucket(prev_bucket, i, 0)
            for i in range(bucketcount + 1):
                prev_kmer_set(prev_kmer, i, nkmers + 1)
            if insertedKmer == 0:
                raise RuntimeError("Problem is unsolvable with the given parameters.")
            passes += 1

    @njit(nogil=True, locals=dict())
    def init_prev_kmers(prev_kmer, nkmers):
        for i in range(bucketcount + 1):
            prev_kmer_set(prev_kmer, i, nkmers + 1)

    max_kmerbits = max(int(np.ceil(np.log2(nkmers + 1))) for nkmers in nkmers_tuple)
    prev_kmerr = [intbitarray(bucketcount, max_kmerbits) for st in range(nsubtables)]
    prev_kmer_set = prev_kmerr[0].set
    prev_kmer_get = prev_kmerr[0].get

    bucketcost = np.full((nsubtables, bucketcount), np.iinfo(np.int16).max, dtype=np.int16)

    @njit(nogil=True, locals=dict())
    def run(nkmers, kmers, ukmer, T_starts, T_i, T_j, pF, prev_kmer, bucketcost, visitedKmer, activebucket, prev_bucket, n_unassigned_kmers):
        build_T_arrays(nkmers, kmers, bucketcount, ukmer, T_starts, T_i, T_j)
        startPasses(pF, n_unassigned_kmers, bucketcount, prev_kmer, bucketcost, bucketsize, ukmer, visitedKmer, activebucket, kmers, nkmers, prev_bucket, T_starts, T_i, T_j)

    print("Start thread pool")
    beg = datetime.datetime.now()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(
            init_prev_kmers, prev_kmerr[st].array, nkmers_tuple[st])
            for st in range(nsubtables)]
        wait(futures)

        n_unassigned_kmers = []
        debugprint0("Start initialization")
        futures = [executor.submit(
            _init, bucket_fill_tuple[st].array, bucketcount, bucketsize, ukmerr[st].array, kmer_bitarrays[st].array, nkmers_tuple[st])
            for st in range(nsubtables)]
        wait(futures)
        for i in range(nsubtables):
            n_unassigned_kmers.append(futures[i].result())

        debugprint1("Compute T array")
        tisize_tuple = [n_unassigned_kmers[st] * 3 + (nkmers_tuple[st] - n_unassigned_kmers[st]) * 2 for st in range(nsubtables)]
        # define T_starts
        # Index in the T arrays at which a bucket begins

        # We need the same setter for all subtables
        max_tisize = max(tisize_tuple)
        T_starts_tuple = [intbitarray(bucketcount + 1, np.ceil(np.log2(max_tisize))) for st in range(nsubtables)]
        # T_starts = T_starts_tuple.array
        T_starts_get = T_starts_tuple[0].get
        T_starts_set = T_starts_tuple[0].set

        # TODO merge T_i and T_j and use max_kmerbits + 2 bits?
        # define T_i
        # T_i stores the index of a k-mer the can
        T_i_tuple = [intbitarray(tisize, max_kmerbits) for tisize in tisize_tuple]
        # T_i = T_i_tuple.array
        T_i_get = T_i_tuple[0].get
        T_i_set = T_i_tuple[0].set

        # define Tj
        # Defines for each bucket which hash function is used to assign the k-mer in T_i to this bucket
        T_j_tuple = [intbitarray(tisize, 2) for tisize in tisize_tuple]
        # T_j = T_j_tuple.array
        T_j_get = T_j_tuple[0].get
        T_j_set = T_j_tuple[0].set

        debugprint0("Start passes.")
        futures = [executor.submit(
            run, nkmers_tuple[st], kmer_bitarrays[st].array, ukmerr[st].array, T_starts_tuple[st].array, T_i_tuple[st].array, T_j_tuple[st].array,
            bucket_fill_tuple[st].array, prev_kmerr[st].array, bucketcost[st], visited_kmer_tuple[st].array, visited_kmer_tuple[st].array,
            prev_bucket_tuple[st].array, n_unassigned_kmers[st])
            for st in range(nsubtables)]

    end = datetime.datetime.now()
    debugprint1("Time to calculate an optimal assignment:")
    debugprint1((end - beg).total_seconds())

    # for st in range(nsubtables):
    #     debugprint1(f"'{datetime.datetime.now()}': Calculate statistics")
    #     calcStats(ukmerr[st].array, bucket_fill_tuple[st].array, nkmers_tuple[st])

    #     debugprint1(f"'{datetime.datetime.now()}': Calculate memory usage")
    #     show_memory(kmer_bitarrays[st].array, ukmerr[st].array, bucket_fill_tuple[st].array, T_starts_tuple[st].array, T_i_tuple[st].array, T_j_tuple[st].array, prev_kmerr[st].array, prev_bucket_tuple[st].array, visited_kmer_tuple[st].array, names="elements assignments bucketfill Tstarts Ti Tj bucket_cost prev_element prev_bucket emba".split())
    return ukmerr


def compile_subkey_arrays(h, subtable_keys, subtable_values, subtable_fill, nsubtables, get_subtable_subkey_from_key, threads, recompute=False):
    # TODO return function
    nbuckets = h.nbuckets
    bucketsize = h.bucketsize
    is_slot_empty_at = h.private.is_slot_empty_at
    get_item_at = h.private.get_item_at
    get_subkey_from_bucket_signature = h.private.get_subkey_from_bucket_signature

    set_key = subtable_keys[0].set
    set_value = subtable_values[0].set
    if recompute:
        get_key_from_subtable_subkey = h.private.get_key_from_subtable_subkey
        old_subtables = h.subtables

        @njit(nogil=True, locals=dict(sig=uint64, subkey=uint64, key=uint64,
              new_subtable=uint64, new_subkey=uint64, value=uint64))
        def fill_array(ht, st_key, st_value, st_fill):
            for st in range(old_subtables):
                for bucket in range(nbuckets):
                    for slot in range(bucketsize):
                        if is_slot_empty_at(ht, st, bucket, slot):
                            break
                        sig, value = get_item_at(ht, st, bucket, slot)
                        subkey = get_subkey_from_bucket_signature(bucket, sig)
                        key = get_key_from_subtable_subkey(st, subkey)
                        new_subtable, new_subkey = get_subtable_subkey_from_key(key)
                        set_key(st_key[new_subtable], st_fill[new_subtable], new_subkey)
                        set_value(st_value[new_subtable], st_fill[new_subtable], value)
                        st_fill[new_subtable] += 1

        fill_array(h.hashtable, tuple(subtable_keys[st].array for st in range(nsubtables)), tuple(subtable_values[st].array for st in range(nsubtables)), subtable_fill)

    else:

        @njit(nogil=True, locals=dict(sig=uint64, subkey=uint64, value=uint64))
        def fill_array(ht, st, st_key, st_value, st_fill):
            for bucket in range(nbuckets):
                for slot in range(bucketsize):
                    if is_slot_empty_at(ht, st, bucket, slot):
                        break
                    sig, value = get_item_at(ht, st, bucket, slot)
                    subkey = get_subkey_from_bucket_signature(bucket, sig)
                    set_key(st_key, st_fill[st], subkey)
                    set_value(st_value, st_fill[st], value)
                    st_fill[st] += 1

        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(
                fill_array, h.hashtable, st, subtable_keys[st].array, subtable_values[st].array, subtable_fill)
                for st in range(nsubtables)]
        wait(futures)


def fill_hash_table(h, st_keys, st_values, st_choices, st_fill):

    assert len(st_keys) == len(st_values) == len(st_choices)
    get_key = st_keys[0].get
    get_value = st_values[0].get
    get_choice = st_choices[0].get

    bucketsize = h.bucketsize
    set_item_at = h.private.set_item_at
    is_slot_empty_at = h.private.is_slot_empty_at
    get_bucket_signature = h.private.get_bs
    get_bucket_signature1 = get_bucket_signature[0]
    get_bucket_signature2 = get_bucket_signature[1]
    get_bucket_signature3 = get_bucket_signature[2]

    @njit(nogil=True, locals=dict(subkey=uint64, value=uint64, choice=uint64,
        sig=uint64, fpr=uint64, bucket=uint64))
    def fill_hash(ht, st, st_keys, st_values, st_choices, st_fill):
        for pos in range(st_fill):
            subkey = get_key(st_keys, pos)
            value = get_value(st_values, pos)
            choice = get_choice(st_choices, pos)

            if choice == 1:
                bucket, sig = get_bucket_signature1(subkey)
            elif choice == 2:
                bucket, sig = get_bucket_signature2(subkey)
            elif choice == 3:
                bucket, sig = get_bucket_signature3(subkey)
            else:
                raise RuntimeError("invalid choice")

            for slot in range(bucketsize):
                if is_slot_empty_at(ht, st, bucket, slot):
                    set_item_at(ht, st, bucket, slot, sig, value)
                    break
            else:
                raise RuntimeError("No empty slot in this bucket. This should not happen.")

    for st in range(h.subtables):
        fill_hash(h.hashtable, st, st_keys[st].array, st_values[st].array, st_choices[st].array, st_fill[st])


# main #########################################
def main(args):
    """main method for calculating an optimal hash assignment"""
    # needs: args.index (str),
    # optional: args.value (int)

    global debugprint0, debugprint1, debugprint2
    global timestamp0, timestamp1, timestamp2
    debugprint0, debugprint1, debugprint2 = debug.debugprint
    timestamp0, timestamp1, timestamp2 = debug.timestamp

    starttime = timestamp0(msg=f"\n# Optimizing index {args.index}")

    # load index
    h, values, infotup = load_hash(args.index)
    (hashinfo, valueinfo, optinfo, appinfo) = infotup

    debugprint1("\n- Extracting infos existing index")
    universe = int(hashinfo["universe"])
    debugprint1(f"- {universe=}")

    # get infos to init new bitarrays
    mask = create_mask(appinfo["mask"])
    debugprint1(f"- {mask.tuple=}")
    nkeys = h.count_items(h.hashtable, njit(nogil=True)(lambda x, y: True))
    fill = nkeys / h.n
    debugprint1(f"- {nkeys=} of n={h.n}")
    debugprint1(f"- {fill=:.3f}")

    valuebits = bitsfor(hashinfo["nvalues"])
    debugprint1(f"- {valueinfo=}")
    debugprint1(f"- {values=}")
    debugprint1(f"- {values.NVALUES=}")
    debugprint1(f"- {hashinfo['nvalues']=}")
    debugprint1(f"- {valuebits=} (from hashinfo['nvalues'])")

    recompute_subkey = False
    # check if new number of subtables is defined
    nsubtables = hashinfo['subtables']
    if args.subtables and args.subtables != nsubtables:
        recompute_subkey = True
        nsubtables = args.subtables

    # update bucket size
    bucketsize = int(args.bucketsize) if args.bucketsize else int(hashinfo['bucketsize'])

    # if a new fill level is provided we need a new number of buckets
    if args.fill:
        fill = args.fill

    if args.fill or args.subtables or args.bucketsize:
        nbuckets = get_nbuckets(ceil(nkeys / nsubtables), bucketsize, fill)
    else:
        nbuckets = hashinfo["nbuckets"]

    rcmode = appinfo['rcmode']
    if not isinstance(rcmode, str):
        rcmode = rcmode.decode()

    # check if new hash functions are defined
    hashfuncs = hashinfo['hashfuncs']
    if args.hashfunctions:
        recompute_subkey = True
        hashfuncs = args.hashfunctions
    if not isinstance(hashfuncs, str):
        hashfuncs = hashfuncs.decode()

    # get hash functions
    hf_string = hashfuncs.split(":")
    get_subtable_subkey_from_key = compile_get_subtable_subkey_from_key(hf_string[0], universe, nsubtables)[0]
    get_bucket_fpr1 = compile_get_bucket_fpr_from_subkey(hf_string[1], universe, nbuckets, nsubtables)[0]  # nsubtables to update the universe for each subtable
    get_bucket_fpr2 = compile_get_bucket_fpr_from_subkey(hf_string[2], universe, nbuckets, nsubtables)[0]  # nsubtables to update the universe for each subtable
    get_bucket_fpr3 = compile_get_bucket_fpr_from_subkey(hf_string[3], universe, nbuckets, nsubtables)[0]  # nsubtables to update the universe for each subtable
    get_bf = (get_bucket_fpr1, get_bucket_fpr2, get_bucket_fpr3)

    beg = timestamp0(msg="- build new int bit arrays")

    subtable_size = nbuckets * bucketsize
    sub_universe = universe // (4**(int(log(nsubtables, 4))))
    subkey_bits = bitsfor(sub_universe)

    debugprint1("- DEBUG: Calculating subkeys")
    subtable_keys = tuple(intbitarray(subtable_size, subkey_bits) for i in range(nsubtables))
    subtable_values = tuple(intbitarray(subtable_size, valuebits) for i in range(nsubtables))
    subtable_fill = np.zeros(nsubtables, dtype=np.uint64)
    compile_subkey_arrays(h, subtable_keys, subtable_values, subtable_fill, nsubtables, get_subtable_subkey_from_key, args.threads, recompute=recompute_subkey)
    keys_size = sum(i.capacity for i in subtable_keys)
    debugprint0(f"- Codes array: Size is {(keys_size/2**30):.3f} GB (GB = 2**30 bytes).")
    start_opimization = timestamp0(msg="\n# Start optimization")

    choices = optimize(subtable_fill, bucketsize, nbuckets, get_bf, subtable_keys, args.threads)
    if args.check:
        optimize_ilp(subtable_keys, subtable_fill, bucketsize, nbuckets, get_bf, choices)

    timestamp0(msg=f"Full time to calculate an optimal assignment for {nsubtables} subtables: ", previous=start_opimization)

    # build hash table
    hashtype = hashinfo["hashtype"]
    hashmodule = import_module(".hash_" + hashtype, __package__)
    build_hash = hashmodule.build_hash
    aligned = bool(hashinfo['aligned'])
    shortcutbits = int(hashinfo['shortcutbits'])
    maxwalk = 3
    debugprint1(f"- DEBUG: {values.NVALUES=}")
    h = build_hash(universe, (nbuckets * bucketsize * nsubtables), nsubtables, bucketsize,
        hashfuncs, values.NVALUES, values.update,
        aligned=aligned, maxwalk=maxwalk, shortcutbits=shortcutbits)
    debugprint1(f"- DEBUG: {h.nvalues=}")
    fill_hash_table(h, subtable_keys, subtable_values, choices, subtable_fill)
    debugprint1(f"- DEBUG: {h.nvalues=}")
    print_statistics(h, level="summary", show_values=2)

    optinfo = dict(walkseed="0", maxwalk=0, maxfailures=0)
    appinfo = dict(rcmode=rcmode, mask=mask.tuple, k=mask.k)
    save_hash(args.optindex, h, valueinfo, optinfo, appinfo)
