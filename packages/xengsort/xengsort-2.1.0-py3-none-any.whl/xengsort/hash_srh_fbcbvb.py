"""
hash_rh_fbcbvb:
a hash table based on robin hood hashing,
bucket layout is (low) ... [shortcutbits][slot]+ ... (high),
where slot is  (low) ... [signature value] ...     (high),
where signature is (low) [fingerprint choice] .....(high).
signature as bitmask: ccffffffffffffff (choice is at HIGH bits!)

This layout allows fast access because bits are separated.
It is memory-efficient if the number of values is a power of 2,
or just a little less.
"""

# fastpark count --fastq <(zcat data/ecoli.fq.gz) --subtables 0 -n 2262962 -k 25 -o test_s9.h5 --fill 0.9 --type rh_fbcbvb
from math import log

import numpy as np
from numpy.random import randint
from numba import njit, uint64, int64, uint32, int32, boolean, void

from .mathutils import bitsfor, xbitsfor, nextpower
from .lowlevel.bitarray import bitarray
from .lowlevel.intbitarray import intbitarray
# from .hashfunctions import get_hashfunctions
from .subtable_hashfunctions import (
    get_hashfunctions,
    hashfunc_tuple_from_str,
    compile_get_subtable_subkey_from_key,
    )
from .srhash import (
    create_SRHash,
    check_bits,
    get_nbuckets,
    get_nfingerprints,
    compile_get_subkey_from_bucket_signature,
    compile_get_subkey_choice_from_bucket_signature,
    compile_get_bucketstatus_v,
    )
from .lowlevel import debug  # the global debugging functions


def build_hash(universe, n, subtables, bucketsize, # _ for subtables
        hashfunc_str, nvalues, update_value, *,
        aligned=False, nfingerprints=-1, init=True,
        maxwalk=500, shortcutbits=0, prefetch=False, force_h0=None):
    """
    Allocate an array and compile access methods for a hash table.
    Return an SRHash object with the hash information.
    """

    # Get debug printing functions
    debugprint0, debugprint1, debugprint2 = debug.debugprint


    # Basic properties
    hashtype = "rh_fbcbvb"
    choices = 1
    psl = 7  # probe sequence lengths
    base = 1
    nbuckets = get_nbuckets(n // subtables, bucketsize)
    sub_universe = universe // (4**(int(log(subtables, 4))))
    nfingerprints = get_nfingerprints(nfingerprints, sub_universe, nbuckets)
    fprbits, ffprbits = xbitsfor(nfingerprints)

    pslbits = bitsfor(psl)
    sigbits = fprbits + pslbits
    valuebits = bitsfor(nvalues)
    check_bits(sigbits, "signataure")
    check_bits(valuebits, "value")
    if shortcutbits < 0 or shortcutbits > 2:
        print(f"# warning: illegal number {shortcutbits} of shortcutbits, using 0.")
        shortcutbits = 0

    fprmask = uint64(2**fprbits - 1)
    pslmask = uint64(2**pslbits - 1)
    sigmask = uint64(2**sigbits - 1)  # fpr + psl, no values
    slotbits = sigbits + valuebits  # sigbits: bitsfor(fpr x psl)
    neededbits = slotbits * bucketsize + shortcutbits  # specific
    bucketsizebits = nextpower(neededbits)  if aligned else neededbits
    subtablebits = int((nbuckets + psl) * bucketsizebits)
    subtablebits = (subtablebits // 512 + 1) * 512
    tablebits = subtablebits * subtables

    fprloss = bucketsize * nbuckets * (fprbits-ffprbits) / 2**23  # in MB

    # allocate the underlying array
    if init == True:
        hasharray = bitarray(tablebits, alignment=64)  # (#bits, #bytes)
        print(f"# allocated {hasharray.array.dtype} hash table of shape {hasharray.array.shape}")
    else:
        hasharray = bitarray(0)
    hashtable = hasharray.array  # the raw bit array
    get_bits_at = hasharray.get  # (array, startbit, nbits=1)
    set_bits_at = hasharray.set  # (array, startbit, value, nbits=1)
    hprefetch = hasharray.prefetch
    
    if hashfunc_str == "random" or hashfunc_str == "default":
        if force_h0 is not None:
            firsthashfunc = force_h0
        else:
            firsthashfunc = hashfunc_tuple_from_str(
                hashfunc_str, number=1, mod_value=subtables)[0]
    else:
        firsthashfunc, hashfunc_str = hashfunc_str.split(":", 1)
    get_subtable_subkey_from_key, get_key_from_subtable_subkey \
        = compile_get_subtable_subkey_from_key(firsthashfunc, universe, subtables)

    hashfuncs, get_bf, get_subkey, get_subtable_bucket_fpr, get_key_from_subtale_bucket_fpr \
        = get_hashfunctions(firsthashfunc, hashfunc_str, choices, universe, nbuckets, subtables)

    debugprint1(
        f"- fingerprintbits: {ffprbits} -> {fprbits}; loss={fprloss:.1f} MB\n"
        f"- nbuckets={nbuckets}, slots={bucketsize*nbuckets}, n={n} per subtable\n"
        f"- bits per slot: {slotbits}; per bucket: {neededbits} -> {bucketsizebits}\n"
        f"- subtable bits: {subtablebits};  ({subtablebits/2**23:.1f} MiB, {subtablebits/2**33:.3f} GiB) x {subtables} subtables\n"
        f"- table bits: {tablebits};  MB: {tablebits/2**23:.1f};  GB: {tablebits/2**33:.3f}\n"
        f"- shortcutbits: {shortcutbits}\n"
        f"- final hash functions: {hashfuncs}",
    )
    get_bs = compile_getps_from_getpf(get_bf[0], 1, fprbits)

    @njit(nogil=True, inline='always', locals=dict(
        bucket=int64, startbit=uint64))
    def prefetch_bucket(table, bucket):
        startbit = bucket * bucketsizebits
        hprefetch(table, startbit)

    # Define private low-level hash table accssor methods
    @njit(nogil=True, locals=dict(
            bucket=int64, startbit=int64, v=uint64))
    def get_shortcutbits_at(table, subtable, bucket):
        """Return the shortcut bits at the given bucket."""
        if shortcutbits == 0:
            return uint64(3)
        startbit = subtable * subtablebits + bucket * bucketsizebits
        v = get_bits_at(table, startbit, shortcutbits)
        return v

    @njit(nogil=True,  locals=dict(
            bucket=int64, slot=uint64, startbit=int64, v=uint64))
    def get_value_at(table, subtable, bucket, slot):
        """Return the value at the given bucket and slot."""
        if valuebits == 0: return 0
        startbit = subtable * subtablebits + bucket * bucketsizebits + slot * slotbits + shortcutbits + sigbits
        v = get_bits_at(table, startbit, valuebits)
        return v

    @njit(nogil=True, locals=dict(
            bucket=int64, slot=uint64, startbit=int64, c=uint64))
    def get_probebits_at(table, subtable, bucket, slot):
        """Return the probe value at the given bucket and slot."""
        startbit = subtable * subtablebits + bucket * bucketsizebits + slot * slotbits + shortcutbits + fprbits
        c = get_bits_at(table, startbit, pslbits)
        return c

    @njit(nogil=True,  locals=dict(
            bucket=int64, slot=uint64, startbit=int64, sig=uint64))
    def get_signature_at(table, subtable, bucket, slot):
        """Return the signature (probe, fingerprint) at the given bucket and slot."""
        startbit = subtable * subtablebits + bucket * bucketsizebits + slot * slotbits + shortcutbits
        sig = get_bits_at(table, startbit, sigbits)
        return sig

    @njit(nogil=True, locals=dict(
            bucket=int64, slot=uint64, startbit=int64, sig=uint64, v=uint64))
    def get_item_at(table, subtable, bucket, slot):
        """Return the signature (probe, fingerprint) at the given bucket and slot."""
        startbit = subtable * subtablebits + bucket * bucketsizebits + slot * slotbits + shortcutbits
        sig = get_bits_at(table, startbit, sigbits)
        if valuebits > 0:
            v = get_bits_at(table, startbit+sigbits, valuebits)
            return (sig, v)
        return (sig, uint64(0))


    @njit(nogil=True, inline='always', locals=dict(
            sig=uint64, c=uint64, fpr=uint64))
    def signature_to_probe_fingerprint(sig):
        """Return (probe, fingerprint) from signature"""
        fpr = sig & fprmask
        c = (sig >> uint64(fprbits)) & pslmask
        return (c, fpr)

    @njit(nogil=True, inline='always', locals=dict(
            sig=uint64, probe=uint64, fpr=uint64))
    def signature_from_probe_fingerprint(probe, fpr):
        """Return signature from (probe, fingerprints)"""
        sig = (probe << uint64(fprbits)) | fpr
        return sig

    @njit(nogil=True, locals=dict(
            bucket=int64, bit=uint64, startbit=uint64))
    def set_shortcutbit_at(table, subtable, bucket, bit):
        """Set the shortcut bits at the given bucket."""
        if shortcutbits == 0: return
        # assert 1 <= bit <= shortcutbits
        startbit = subtable * subtablebits + bucket * bucketsizebits + bit - 1
        set_bits_at(table, startbit, 1, 1)  # set exactly one bit to 1

    @njit(nogil=True, locals=dict(
            bucket=int64, slot=int64, sig=uint64))
    def set_signature_at(table, subtable, bucket, slot, sig):
        """Set the signature at the given bucket and slot."""
        startbit = subtable * subtablebits + bucket * bucketsizebits + slot * slotbits + shortcutbits
        set_bits_at(table, startbit, sig, sigbits)
    
    @njit(nogil=True, locals=dict(
            bucket=int64, slot=int64, value=int64))
    def set_value_at(table, subtable, bucket, slot, value):
        if valuebits == 0: return
        """Set the value at the given bucket and slot."""
        startbit = subtable * subtablebits + bucket * bucketsizebits + slot * slotbits + sigbits + shortcutbits
        set_bits_at(table, startbit, value, valuebits)

    @njit(nogil=True, locals=dict(
            bucket=int64, slot=int64, sig=uint64, value=uint64))
    def set_item_at(table, subtable, bucket, slot, sig, value):
        startbit = subtable * subtablebits + bucket * bucketsizebits + slot * slotbits + shortcutbits
        set_bits_at(table, startbit, sig, sigbits)
        if valuebits == 0: return
        set_bits_at(table, startbit+sigbits, value, valuebits)


    # define the is_slot_empty_at function
    @njit(nogil=True, inline='always', locals=dict(b=boolean))
    def is_slot_empty_at(table, subtable, bucket, slot):
        """Return whether a given slot is empty (check by psl value)"""
        c = get_probebits_at(table, subtable, bucket, slot)
        b = (c == 0)
        return b

    # define the _find_signature_at function
    @njit(nogil=True, inline="always", locals=dict(
            bucket=uint64, fpr=uint64, probe=uint64,
            query=uint64, slot=int64, v=uint64, s=uint64))
    def _find_signature_at(table, subtable, bucket, query):
        """
        Attempt to locate signature on a bucket,
        assuming probe == 0 indicates an empty space.
        Return (int64, uint64):
        Return (slot, value) if the signature 'query' was found,
            where 0 <= slot < bucketsize.
        Return (-1, fill) if the signature was not found,
            where fill >= 0 is the number of slots already filled.
        """
        for slot in range(bucketsize):
            s = get_signature_at(table, subtable, bucket, slot)
            if s == query:
                v = get_value_at(table, subtable, bucket, slot)
                return (slot, v)
            c, _ = signature_to_probe_fingerprint(s)
            if c == 0:
                return (int64(-1), uint64(slot))  # free slot, only valid if tight!
        return (int64(-1), uint64(bucketsize))

    # define the update/store/overwrite functions

    update, update_ssk \
        = compile_update_by_randomwalk(bucketsize, psl,
            get_bs, get_signature_at, get_value_at,
            get_item_at, set_item_at, set_value_at,
            prefetch_bucket,signature_to_probe_fingerprint,
            signature_from_probe_fingerprint,
            is_slot_empty_at, nbuckets,
            update_value=update_value, overwrite=False,
            allow_new=True, allow_existing=True,
            maxwalk=maxwalk, prefetch=prefetch)

    update_existing, update_existing_ssk \
        = compile_update_by_randomwalk(bucketsize, psl,
            get_bs, get_signature_at, get_value_at,
            get_item_at, set_item_at, set_value_at,
            prefetch_bucket,signature_to_probe_fingerprint,
            signature_from_probe_fingerprint,
            is_slot_empty_at, nbuckets,
            update_value=update_value, overwrite=False,
            allow_new=False, allow_existing=True,
            maxwalk=maxwalk, prefetch=prefetch)

    store_new, store_new_ssk \
        = compile_update_by_randomwalk(bucketsize, psl,
            get_bs, get_signature_at, get_value_at,
            get_item_at, set_item_at, set_value_at,
            prefetch_bucket,signature_to_probe_fingerprint,
            signature_from_probe_fingerprint,
            is_slot_empty_at, nbuckets,
            update_value=None, overwrite=True,
            allow_new=True, allow_existing=False,
            maxwalk=maxwalk, prefetch=prefetch)

    overwrite, overwrite_ssk \
        = compile_update_by_randomwalk(bucketsize, psl,
            get_bs, get_signature_at, get_value_at,
            get_item_at, set_item_at, set_value_at,
            prefetch_bucket,signature_to_probe_fingerprint,
            signature_from_probe_fingerprint,
            is_slot_empty_at, nbuckets,
            update_value=update_value, overwrite=True,
            allow_new=True, allow_existing=True,
            maxwalk=maxwalk, prefetch=prefetch)

    overwrite_existing, overwrite_existing_ssk \
        = compile_update_by_randomwalk(bucketsize, psl,
            get_bs, get_signature_at, get_value_at,
            get_item_at, set_item_at, set_value_at,
            prefetch_bucket,signature_to_probe_fingerprint,
            signature_from_probe_fingerprint,
            is_slot_empty_at, nbuckets,
            update_value=update_value, overwrite=True,
            allow_new=False, allow_existing=True,
            maxwalk=maxwalk, prefetch=prefetch)


    # define the "reading" functions find_index, get_value, etc.

    @njit(nogil=True, locals=dict(
            subkey=uint64, default=uint64, NOTFOUND=uint64,
            bucket1=uint64, sig1=uint64, slot1=int64, val1=uint64,
            bucket2=uint64, sig2=uint64, slot2=int64, val2=uint64,
            bucket3=uint64, sig3=uint64, slot3=int64, val3=uint64,
            bucketbits=uint32, check2=uint32, check3=uint32))
    def find_index(table, subtable, subkey, default=uint64(-1)):
        """
        Return uint64: the linear table index the given subkey,
        or the default if the subkey is not present.
        """
        NOTFOUND = uint64(default)
        bucket1, sig1 = get_bs1(subkey)
        (slot1, val1) = _find_signature_at(table, subtable, bucket1, sig1)
        if slot1 >= 0: return uint64(uint64(bucket1 * bucketsize) + slot1)
        if val1 < bucketsize: return NOTFOUND
        # test for shortcut
        bucketbits = get_shortcutbits_at(table, subtable, bucket1)  # returns all bits set if bits==0
        if not bucketbits: return NOTFOUND
        check2 = bucketbits & 1
        check3 = bucketbits & 2 if shortcutbits >= 2 else 1

        if check2:
            bucket2, sig2 = get_bs2(subkey)
            (slot2, val2) = _find_signature_at(table, subtable, bucket2, sig2)
            if slot2 >= 0: return uint64(uint64(bucket2 * bucketsize) + slot2)
            if val2 < bucketsize: return NOTFOUND
            # test for shortcuts
            if shortcutbits != 0:
                bucketbits = get_shortcutbits_at(table, subtable, bucket2)
                if shortcutbits == 1:
                    check3 = bucketbits  # 1 or 0
                else:
                    check3 &= bucketbits & 2

        # try the third choice only if necessary
        if not check3: return NOTFOUND
        bucket3, sig3 = get_bs3(subkey)
        (slot3, val3) = _find_signature_at(table, subtable, bucket3, sig3)
        if slot3 >= 0: return uint64(uint64(bucket3 * bucketsize) + slot3)
        return NOTFOUND


    @njit(nogil=True, locals=dict(
            key=uint64, default=uint64, NOTFOUND=uint64,
            bucket1=uint64, sig1=uint64, slot1=int64, val1=uint64,
            bucket2=uint64, sig2=uint64, slot2=int64, val2=uint64,
            bucket3=uint64, sig3=uint64, slot3=int64, val3=uint64,
            bucketbits=uint32, check2=uint32, check3=uint32))
    def get_value_from_st_sk(table, subtable, subkey, default=uint64(0)):
        """
        Return uint64: the value for the given subkey,
        or the default if the subkey is not present.
        """
        NOTFOUND = uint64(default)
        bucket1, sig1 = get_bs1(subkey)
        (slot1, val1) = _find_signature_at(table, subtable, bucket1, sig1)
        if slot1 >= 0: return val1
        if val1 < bucketsize: return NOTFOUND
        # test for shortcut
        bucketbits = get_shortcutbits_at(table, bucket1)  # returns all bits set if bits==0
        if not bucketbits: return NOTFOUND
        check2 = bucketbits & 1
        check3 = bucketbits & 2 if shortcutbits >= 2 else 1

        if check2:
            bucket2, sig2 = get_bs2(subkey)
            (slot2, val2) = _find_signature_at(table, subtable, bucket2, sig2)
            if slot2 >= 0: return val2
            if val2 < bucketsize: return NOTFOUND
            # test for shortcuts
            if shortcutbits != 0:
                bucketbits = get_shortcutbits_at(table, subtable, bucket2)
                if shortcutbits == 1:
                    check3 = bucketbits  # 1 or 0
                else:
                    check3 &= bucketbits & 2

        # try the third choice only if necessary
        if not check3: return NOTFOUND
        bucket3, sig3 = get_bs3(subkey)
        (slot3, val3) = _find_signature_at(table, subtable, bucket3, sig3)
        if slot3 >= 0: return val3
        return NOTFOUND


    @njit(nogil=True, locals=dict(
            key=uint64, default=uint64,
            bucket1=uint64, sig1=uint64, slot1=int64, val1=uint64,
            bucket2=uint64, sig2=uint64, slot2=int64, val2=uint64,
            bucket3=uint64, sig3=uint64, slot3=int64, val3=uint64,
            bucketbits=uint32, check2=uint32, check3=uint32))
    def get_value_and_choice_from_st_sk(table, subtable, subkey, default=uint64(0)):
        """
        Return (value, choice) for given key,
        where value is uint64 and choice is in {1,2,3} if key was found,
        but value=default and choice=0 if key was not found.
        """
        NOTFOUND = (uint64(default), uint32(0))
        bucket1, sig1 = get_bs1(key)
        (slot1, val1) = _find_signature_at(table, subtable, bucket1, sig1)
        if slot1 >= 0: return (val1, uint32(1))
        if val1 < bucketsize: return NOTFOUND
        # test for shortcut
        bucketbits = get_shortcutbits_at(table, subtable, bucket1)  # returns all bits set if bits==0
        if not bucketbits: return NOTFOUND
        check2 = bucketbits & 1
        check3 = bucketbits & 2 if shortcutbits >= 2 else 1

        if check2:
            bucket2, sig2 = get_bs2(key)
            (slot2, val2) = _find_signature_at(table, subtable, bucket2, sig2)
            if slot2 >= 0: return (val2, uint32(2))
            if val2 < bucketsize: return NOTFOUND
            # test for shortcuts
            if shortcutbits != 0:
                bucketbits = get_shortcutbits_at(table, subtable, bucket2)
                if shortcutbits == 1:
                    check3 = bucketbits  # 1 or 0
                else:
                    check3 &= bucketbits & 2

        # try the third choice only if necessary
        if not check3: return NOTFOUND
        bucket3, sig3 = get_bs3(key)
        (slot3, val3) = _find_signature_at(table, subtable, bucket3, sig3)
        if slot3 >= 0: return (val3, uint32(3))
        return NOTFOUND

    @njit(nogil=True)
    def get_value_and_choice(table, key):
        st, sk = get_subtable_subkey_from_key(key)
        return get_value_and_choice_from_st_sk(table, st, sk)

    @njit(nogil=True)
    def get_value(table, key):
        st, sk = get_subtable_subkey_from_key(key)
        return get_value_from_st_sk(table, st, sk)


    @njit(nogil=True, locals=dict(
            bucket=uint64, slot=int64, v=uint64, sig=uint64, c=uint64,
            f=uint64, key=uint64, p=uint64, s=int64, fill=uint64))
    def is_tight(ht):
        """
        Return (0,0) if hash is tight, or problem (key, choice).
        In the latter case, it means that there is an empty slot
        for key 'key' on bucket choice 'choice', although key is
        stored at a higher choice.
        """

        # Todo check all subtables?
        for bucket in range(nbuckets):
            for slot in range(bucketsize):
                sig = get_signature_at(ht, bucket, slot)
                (c, f) = signature_to_choice_fingerprint(sig)  # should be in 0,1,2,3.
                if c <= 1: continue
                # c >= 2
                key = get_key2(bucket, f)
                p, s = get_bs1(key)
                (slot, val) = _find_signature_at(ht, p, s)
                if slot >= 0 or val != bucketsize:
                    return (uint64(key), 1)  # empty slot on 1st choice
                if c >= 3:
                    key = get_key3(bucket, f)
                    p, s = get_bs2(key)
                    (slot, val) = _find_signature_at(ht, p, s)
                    if slot >= 0 or val != bucketsize:
                        return (uint64(key), 2)  # empty slot on 2nd choice
                if c >= 4:
                    return (uint64(key), 9)  # should never happen, c=1,2,3.
        # all done, no problems
        return (0, 0)

    @njit(nogil=True, locals=dict(counter=uint64))
    def count_items(ht, filter_func):
        """
        ht: uint64[:]  # the hash table
        filter_func(key: uint64, value: uint64) -> bool  # function
        Return number of items satisfying the filter function (uint64).
        """

        # todo fix get_subkey_from_bucket_signature
        counter = 0
        for st in range(subtables):
            for p in range(nbuckets):
                for s in range(bucketsize):
                    if is_slot_empty_at(ht, st, p, s):  continue
                    sig = get_signature_at(ht, st, p, s)
                    value = get_value_at(ht, st, p, s)
                    key = get_subkey_from_bucket_signature(p, sig)
                    if filter_func(key, value):
                        counter += 1
        return counter

    @njit(nogil=True, locals=dict(pos=uint64))
    def get_items(ht, filter_func, buffer):
        """
        ht: uint64[:]  # the hash table
        filter_func: bool(key(uint64), value(uint64))
        buffer: buffer to store keys (filled till full)
        Return the number of items satisfying the filter function.
        """

        # todo fix get_subkey_from_bucket_signature
        B = buffer.size
        pos = 0
        for p in range(nbuckets):
            for s in range(bucketsize):
                if is_slot_empty_at(ht, p, s):  continue
                sig = get_signature_at(ht, p, s)
                value = get_value_at(ht, p, s)
                key = get_subkey_from_bucket_signature(p, sig)
                if filter_func(key, value):
                    if pos < B:
                        buffer[pos] = key
                    pos += 1
        return pos

    # define the occupancy computation function
    # get_statistics = compile_get_statistics("c", subtables,
    #     choices, nbuckets+choices, bucketsize, nvalues, shortcutbits,
    #     get_value_at, get_signature_at,
    #     signature_to_choice_fingerprint, get_shortcutbits_at)


    # define the compute_shortcut_bits fuction,
    # depending on the number of shortcutbits
    if shortcutbits == 0:
        @njit
        def compute_shortcut_bits(table):
            pass
    elif shortcutbits == 1:
        @njit
        def compute_shortcut_bits(table):
            for bucket in range(nbuckets):
                for slot in range(bucketsize):
                    if is_slot_empty_at(table, bucket, slot):
                        continue
                    key, c = get_subkey_choice_from_bucket_signature(
                        bucket, get_signature_at(table, bucket, slot))
                    assert c >= 1
                    if c == 1: continue  # first choice: nothing to do
                    # treat c >= 2
                    firstbucket, _ = get_bf1(key)
                    set_shortcutbit_at(table, firstbucket, 1)
                    if c >= 3:
                        secbucket, _ = get_bf2(key)
                        set_shortcutbit_at(table, secbucket, 1)
    elif shortcutbits == 2:
        @njit
        def compute_shortcut_bits(table):
            for bucket in range(nbuckets):
                for slot in range(bucketsize):
                    if is_slot_empty_at(table, bucket, slot):
                        continue
                    key, c = get_subkey_choice_from_bucket_signature(
                        bucket, get_signature_at(table, bucket, slot))
                    assert c >= 1
                    if c == 1:
                        continue
                    if c == 2:
                        firstbucket, _ = get_bf1(key)
                        set_shortcutbit_at(table, firstbucket, 1)
                        continue
                    # now c == 3:
                    firstbucket, _ = get_bf1(key)
                    set_shortcutbit_at(table, firstbucket, 2)
                    secbucket, _ = get_bf2(key)
                    set_shortcutbit_at(table, secbucket, 2)
    else:
        raise ValueError(f"illegal number of shortcutbits: {shortcutbits}")

    # all methods are defined; return the hash object

    # rename some functions
    get_choicebits_at = get_probebits_at
    signature_to_choice_fingerprint = signature_to_probe_fingerprint
    signature_from_choice_fingerprint = signature_from_probe_fingerprint
    get_subkey_from_bucket_signature = None  # Todo
    get_subkey_choice_from_bucket_signature = None  # Todo
    return create_SRHash(locals())


#######################################################################


def compile_getps_from_getpf(get_bfx, choice, fprbits):
    @njit(nogil=True, inline='always', locals=dict(
            p=uint64, f=uint64, sig=uint64))
    def get_bsx(code):
        (p, f) = get_bfx(code)
        sig = uint64((choice << uint64(fprbits)) | f)
        return (p, sig)
    return get_bsx


def compile_update_by_randomwalk(bucketsize, psl,
            get_bs, get_signature_at, get_value_at,
            get_item_at, set_item_at,
            set_value_at,
            prefetch_bucket,
            signature_to_probe_fingerprint,
            signature_from_probe_fingerprint,
            is_slot_empty_at, nbuckets,
            *,
            update_value=None, overwrite=False,
            allow_new=False, allow_existing=False,
            maxwalk=1000, prefetch=False):
    """return a function that stores or modifies an item"""

    if (update_value is None or overwrite) and allow_existing:
        update_value = njit(
            nogil=True, locals=dict(old=uint64, new=uint64)
            )(lambda old, new: new)
    if not allow_existing:
        update_value = njit(
            nogil=True, locals=dict(old=uint64, new=uint64)
            )(lambda old, new: old)

    @njit(nogil=True, locals=dict(
            key=uint64, value=uint64, v=uint64,
            bucket1=uint64, sig1=uint64, slot1=int64, val1=uint64,
            bucket2=uint64, sig2=uint64, slot2=int64, val2=uint64,
            bucket3=uint64, sig3=uint64, slot3=int64, val3=uint64,
            fc=uint64, fpr=uint64, probe=uint64, p=uint64, bucket=uint64, psl=uint64,
            oldbucket=uint64, lastlocation=uint64, steps=uint64, min_probe=uint64,
            xsig=uint64, xval=uint64))
    def update_ssk(table, subtable, subkey, value):
        """
        Attempt to store given key with given value in hash table.
        If the key exists, the existing value may be updated or overwritten,
        or nothing may happen, depending on how this function was compiled.
        If the key does not exist, it is stored with the provided value,
        or nothing may happen, depending on how this function was compiled.

        Returns (status: int32, result: uint64).

        status: if status == 0, the subkey was not found,
            and, if allow_new=True, it could not be inserted either.
            If (status & 127 =: c) != 0, the subkey exists or was inserted w/ probing sequence length psl.
            If (status & 128 != 0), the subkey was aleady present.

        result: If the subkey was already present (status & 128 != 0),
            and result is the new value that was stored.
            Otherwise, result is the walk length needed
            to store the new subkey, value pair.
        """
        oldbucket = uint64(-1)
        lastlocation = uint64(-1)
        steps = 0
        bucket, sig = get_bs(subkey)
        probe, fpr = signature_to_probe_fingerprint(sig)
        assert probe == 1 # 0 is a special value that indicates that the slot is empty
        # sig = signature_from_probe_fingerprint(probe, fpr)

        # nbuckets + lps since we have a buffer of psl at the end of the subtable
        while steps <= maxwalk and bucket < nbuckets+psl:

            sig = signature_from_probe_fingerprint(probe, fpr)
            # check each slot on bucket
            min_slot = -1
            min_probe = 8  # todo is this psl + 1?
            # check all slots on bucket
            for slot in range(bucketsize):
                steps += 1
                # found an empty slot; insert element
                if is_slot_empty_at(table, subtable, bucket, slot):
                    set_item_at(table, subtable, bucket, slot, sig, value)
                    return (int32(1), steps)

                c_sig = get_signature_at(table, subtable, bucket, slot)
                c_probe, c_fpr = signature_to_probe_fingerprint(sig)
                # found element; Update value
                if c_sig == sig:
                    val = get_value_at(table, subtable, bucket, slot)
                    v = update_value(val, value)
                    if v != val: set_value_at(table, subtable, bucket, slot, v)
                    return (int32(128|1), steps)

                # check if there exists an element assigned to this bucket with a lower psl
                if c_probe < probe and c_probe < min_probe:
                    min_slot = slot
                    min_probe = c_probe

            # Element is not in this bucket and there is no empty slot

            # can we swap the current element with one with a lower psl?
            # on the current bucket was at least one element with a lower psl
            if min_slot != -1:
                new_sig, new_val = get_item_at(table, subtable, bucket, min_slot)
                set_item_at(table, subtable, bucket, min_slot, sig, value)
                p, fpr = signature_to_probe_fingerprint(new_sig)
                if p != min_probe:
                    print(p, min_probe)
                    assert p == min_probe
                probe = min_probe

            # increase psl and check next bucket
            bucket += 1
            probe += 1

            if probe > psl:
                print("min_probe: ", min_probe)
                break
                # we reached the maximum psl

        # maxwalk step exceeded;
        # We could not take enough from the rich. :(
        print("steps: ", steps)
        return (int32(0), steps)

    @njit(nogil=True, locals=dict(
        subtable=uint64, subkey=uint64))
    def update(table, key, value):
        subtable, subkey = get_subtable_subkey_from_key(key)
        return update_ssk(table, subtable, subkey, value)

    return update, update_ssk


#######################################################################
## Module-level functions
#######################################################################
## define the fill_from_dump function

def fill_from_arrays(h, k, nkmers, codes, achoices, values):
    nbuckets = h.nbuckets
    bucketsize = h.bucketsize
    (get_bf1, get_bf2, get_bf3) = h.private.get_bf
    set_signature_at = h.private.set_signature_at
    set_value_at = h.private.set_value_at
    is_slot_empty_at = h.private.is_slot_empty_at
    signature_from_choice_fingerprint = h.private.signature_from_choice_fingerprint
    choices = intbitarray(nkmers, 2, init=achoices)
    acodes = codes.array
    avalues = values.array
    get_code = codes.get
    get_value = values.get
    get_choice = choices.get

    @njit(nogil=True, locals=dict(choice=uint64))
    def _insert_elements(ht):
        total = 0
        for i in range(nkmers):
            total += 1
            code = get_code(acodes, i)
            value = get_value(avalues, i)
            choice = get_choice(achoices, i)
            assert choice >= 1
            if choice == 1:
                bucket, fpr = get_bf1(code)
            elif choice == 2:
                bucket, fpr = get_bf2(code)
            elif choice == 3:
                bucket, fpr = get_bf3(code)
            else:
                assert False
            for slot in range(bucketsize):
                if is_slot_empty_at(ht, bucket, slot): break
            else:
                assert False
            sig =  signature_from_choice_fingerprint(choice, fpr)
            set_signature_at(ht, bucket, slot, sig)
            set_value_at(ht, bucket, slot, value)
        return total

    total = _insert_elements(h.hashtable)
    walklength = np.zeros(h.maxwalk+5, dtype=np.uint64)
    walklength[0] = total
    return (total, 0, walklength)


def compile_calc_shortcut_bits_old(h): #TODO Remove?
    choices = len(h.get_bf)
    if choices != 3:
        raise ValueError("shortcut bits only implemented for 3 hash functions")
    bits = h.shortcutbits  # 0, 1 or 2
    is_slot_empty_at = h.is_slot_empty_at
    signature_parts = h.signature_parts
    get_signature_at = h.get_signature_at
    set_shortcutbit_at = h.set_shortcutbit_at
    (get_bf1, get_bf2, get_bf3) = h.get_bf
    get_key_choice_from_signature = h.get_key_choice_from_signature
    nbuckets = h.nbuckets
    bucketsize = h.bucketsize

    if bits < 0 or bits > 2: 
        print("# WARNING: Illegal number of shortcut bits; using 0")
        bits = 0

    if bits == 0:
        @njit
        def calc_shortcut_bits(table):
            pass
        return calc_shortcut_bits

    if bits == 1:
        @njit
        def calc_shortcut_bits(table):
            for bucket in range(nbuckets):
                for slot in range(bucketsize):
                    if is_slot_empty_at(table, bucket, slot):
                        continue
                    key, c = get_key_choice_from_signature(
                        bucket, get_signature_at(table, bucket, slot))
                    assert c >= 1
                    if c == 1: continue  # first choice: nothing to do
                    # treat c >= 2
                    firstbucket, _ = get_bf1(key)
                    set_shortcutbit_at(table, firstbucket, 1)
                    if c >= 3:
                        secbucket, _ = get_bf2(key)
                        set_shortcutbit_at(table, secbucket, 1)
        return calc_shortcut_bits
    
    # bits == 2
    @njit
    def calc_shortcut_bits(table):
        for bucket in range(nbuckets):
            for slot in range(bucketsize):
                if is_slot_empty_at(table, bucket, slot):
                    continue
                key, c = get_key_choice_from_signature(
                    bucket, get_signature_at(table, bucket, slot))
                assert c >= 1
                if c == 1:
                    continue
                if c == 2:
                    firstbucket, _ = get_bf1(key)
                    set_shortcutbit_at(table, firstbucket, 1)
                    continue
                # now c == 3:
                firstbucket, _ = get_bf1(key)
                set_shortcutbit_at(table, firstbucket, 2)
                secbucket, _ = get_bf2(key)
                set_shortcutbit_at(table, secbucket, 2)
    return calc_shortcut_bits

# 0: 2765848
# 1: 2237435 (98.872%)
# 2: 23878 (1.055%)
# 3: 1493 (0.066%)
# 4: 132 (0.006%)
# 5: 15 (0.001%)
# 6: 8 (0.000%)
# 7: 1 (0.000%)
