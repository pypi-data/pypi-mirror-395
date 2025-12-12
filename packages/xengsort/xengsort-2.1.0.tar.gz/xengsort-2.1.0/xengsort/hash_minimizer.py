"""
hash_minimizer:
a hash table with subtables and three choices,
bucket layout is (low) ... [shortcutbits][slot]+ ... (high),
where slot is  (low) ... [occurrence_counter signature leftbits rightbits value] ...     (high),
where signature is (low) [fingerprint choice] .....(high),
where fingerprint is the quotient of a minimizer.
signature as bitmask: ccffffffffffffff (choice is at HIGH bits!)

This layout allows fast access because bits are separated.
It is memory-efficient if the number of values is a power of 2,
or just a little less.
"""

import numpy as np
from math import log
from numba import njit, uint64, int64, uint32, int32, uint8, boolean

from .lowlevel.bitarray import bitarray
from .lowlevel.llvm import \
    compile_ctlz, compile_cttz, \
    compile_compare_xchange, compile_pause, \
    compile_volatile_load, compile_volatile_store
from .subtable_hashfunctions import get_hashfunctions, build_get_sub_subkey_from_key, parse_names
from .mathutils import bitsfor, xbitsfor
from .dnaencode import compile_revcomp_and_canonical_code
from .skhash import (
    create_SKHash,
    get_nfingerprints,
    get_nbuckets,
    compile_get_subkey_from_bucket_signature,
    compile_get_subkey_choice_from_bucket_signature,
    compile_get_statistics,
    )
from .hash_3c_fbcbvb import build_hash as build_backup_hash


rng = np.random.default_rng()
ctlz = compile_ctlz("uint64")
cttz = compile_cttz("uint64")
cmpxchg = compile_compare_xchange("uint64")
pause = compile_pause()
vload = compile_volatile_load("uint64")
vstore = compile_volatile_store("uint64")


def build_hash(k: int,  # k-mer size
               m: int,  # minimizer size
          rcmode: str,  # rcmode for minimizers
               n: int,  # number of slots over all subtables
       subtables: int,  # number of subtables
        bucketsize: int,
       hashfuncs: tuple[str, str, str, str],
         nvalues: int,
    update_value,
               *,
        aligned=False, nfingerprints=-1,
        maxwalk=500, shortcutbits=0, prefetch=False):
    """
    Allocate an array and compile access methods for a hash table.
    Return an SRHash object with the hash information.
    """

    # calculate the minimizer universe
    universe = 4**m
    sub_universe = universe // (4**(int(log(subtables, 4))))

    # Basic properties
    hashtype = "minimizer"
    choices = 3
    superkmersize = 2 * k - m
    nbuckets = get_nbuckets(n // subtables, bucketsize)
    nfingerprints = get_nfingerprints(nfingerprints, sub_universe, nbuckets)

    """
    Calculate the necessary bits for one slot containing:

    - occurence counter: True if the minimizer occurs more than once (2 bit)
       - 00: occured more than 3 times; look up in extra table needed
       - 01: occured once; stop search
       - 10/11: occured two or three times

    #signature
    - choice bit (2 bits)
    - minimizer: fingerprint of the minimizer

    - incomplete super-k-mer: two bits if the super-k-mer is not complete
      on the left or right side. Unused bits are set to 1 (for the left part
      starting at the most significant bit and for the right part at the least
      significant bit). The first 0 bit indicates the start of the super-k-mer (2 bits)
    - left and right of the super k-mer: store the part on the left and right side
      of the minimizer of one super-k-mer (2*k-m bit)

    - values: one value for each k-mer in a super-k-mer (k-m+1 values for a complete super-k-mer).
      ((k-m+1) * value bits)
    """
    base = 1  # indicates a CHOICE-controlled hash
    minimizerbits, fminimizerbits = xbitsfor(nfingerprints)
    choicebits = bitsfor(choices)
    sigbits = choicebits + minimizerbits
    max_minimizer_occ = 3
    max_minimizer_occ_bits = bitsfor(max_minimizer_occ)
    backupflag_bits = 1
    incomplete_bits = 2
    leftpart_bits = rightpart_bits = 2 * (k - m)
    superkmerbits = backupflag_bits + max_minimizer_occ_bits + choicebits + minimizerbits + incomplete_bits + leftpart_bits + rightpart_bits

    # value bits
    nvalues_per_superkmer = k - m + 1
    vbits = bitsfor(nvalues)  # bits to store the value of one k-mer
    valuebits = vbits * nvalues_per_superkmer  # bits to store one value for each k-mer in a super-k-mer

    minimizermask = uint64(2**minimizerbits - 1)
    choicemask = uint64(2**choicebits - 1)
    sigmask = uint64(2**sigbits - 1)  # fpr + choice, no values
    slotbits = superkmerbits + valuebits
    neededbits = shortcutbits + slotbits * bucketsize
    bucketsizebits = nextpower(neededbits) if aligned else neededbits
    subtablebits = int(nbuckets * bucketsizebits)
    subtablebits = (subtablebits // 512 + 1) * 512
    tablebits = subtablebits * subtables

    fprloss = bucketsize * nbuckets * (minimizerbits - fminimizerbits) / 2**23  # in MB

    # allocate the underlying array
    hasharray = bitarray(tablebits, alignment=64)  # (#bits, #bytes)
    # print(f"# allocated {hasharray.array.dtype} hash table of shape {hasharray.array.shape}")
    hashtable = hasharray.array  # the raw bit array
    get_bits_at = hasharray.get  # (array, startbit, nbits=1)
    set_bits_at = hasharray.set  # (array, startbit, value , nbits=1)
    hprefetch = hasharray.prefetch

    # get the hash functions
    if hashfuncs == "random":
        firsthashfunc = parse_names(hashfuncs, 1)[0]
    else:
        firsthashfunc, hashfuncs = hashfuncs.split(":", 1)
    get_subtable_subkey_from_key, get_key_from_subtable_subkey = build_get_sub_subkey_from_key(firsthashfunc, universe, subtables)
    hashfuncs, get_bf, get_subkey, get_subtable_bucket_fpr, get_key_from_subtale_bucket_fpr = get_hashfunctions(
        firsthashfunc, hashfuncs, choices, universe, nbuckets, subtables)

    # print(f"# fingerprintbits: {fminimizerbits} -> {minimizerbits}; loss={fprloss:.1f} MB")
    # print(f"# nbuckets={nbuckets}, slots={bucketsize*nbuckets}, n={n} per subtable")
    # print(f"# bits per slot: {slotbits}; per bucket: {neededbits} -> {bucketsizebits}")
    # print(f"# subtable bits: {subtablebits};  MB: {subtablebits/2**23:.1f};  GB: {subtablebits/2**33:.3f}")
    # print(f"# table bits: {tablebits};  MB: {tablebits/2**23:.1f};  GB: {tablebits/2**33:.3f}")
    # print(f"# shortcutbits: {shortcutbits}")
    # print(f"# subtable hash function: {firsthashfunc}")
    # print(f"# final hash functions: {hashfuncs}")
    # Build backup table
    # print()
    # print(f"# build backup tabel")
    b_universe = 4**k
    b_n = n // 10
    backuptable = build_backup_hash(b_universe, b_n, 0, bucketsize, ":".join(hashfuncs[1:]), nvalues, update_value, shortcutbits=shortcutbits, prefetch=prefetch)
    backuplock = np.zeros(1, dtype=np.uint64)
    backuplock[0] = uint64(-1)  # -1 not locked
    revcomp, ccode = compile_revcomp_and_canonical_code(k, rcmode)
    # print()
    get_bs = tuple([compile_getps_from_getpf(get_bf[c], c + 1, minimizerbits)
            for c in range(choices)])
    get_bf1, get_bf2, get_bf3 = get_bf
    get_bs1, get_bs2, get_bs3 = get_bs
    get_key1, get_key2, get_key3 = get_subkey

    @njit(nogil=True, inline='always', locals=dict(
        bucket=uint64, startbit=uint64))
    def prefetch_bucket(table, subtable, bucket):
        startbit = subtable * subtablebits + bucket * bucketsizebits
        hprefetch(table, startbit)

    # Define private low-level hash table accssor methods
    # Setter ########
    @njit(nogil=True, locals=dict(
        bucket=uint64, startbit=uint64, v=uint64))
    def get_shortcutbits_at(table, subtable, bucket):
        """Return the shortcut bits at the given bucket."""
        if shortcutbits == 0:
            return uint64(3)
        startbit = subtable * subtablebits + bucket * bucketsizebits
        v = get_bits_at(table, startbit, shortcutbits)
        return v

    @njit(nogil=True, locals=dict(
        bucket=uint64, slot=uint64, startbit=uint64, occ=uint64))
    def get_occbits_at(table, subtable, bucket, slot):
        """
        Get the occurence counter bits at the given bucket and slot
           0: More than 3 times
           1-max_minimizer_occ: Occurs 1 to max_minimizer_occ times
        """
        startbit = subtable * subtablebits + bucket * bucketsizebits + shortcutbits + slot * slotbits + backupflag_bits
        occ = get_bits_at(table, startbit, max_minimizer_occ_bits)
        return occ

    @njit(nogil=True, locals=dict(
        bucket=uint64, slot=uint64, startbit=uint64, flag=uint64))
    def get_backupflag_at(table, subtable, bucket, slot):
        """
        Get the flag if a k-mer with this minimizer is stored in the backup table
        """
        startbit = subtable * subtablebits + bucket * bucketsizebits + shortcutbits + slot * slotbits
        flag = get_bits_at(table, startbit, backupflag_bits)
        return flag

    @njit(nogil=True, locals=dict(
        bucket=uint64, slot=uint64, startbit=uint64, c=uint64))
    def get_choicebits_at(table, subtable, bucket, slot):
        """Return the choice at the given bucket and slot; choices start with 1."""
        startbit = subtable * subtablebits + bucket * bucketsizebits + shortcutbits + slot * slotbits + backupflag_bits + max_minimizer_occ_bits + minimizerbits
        c = get_bits_at(table, startbit, choicebits)
        return c

    @njit(nogil=True, locals=dict(
        subtable=uint64, bucket=uint64, slot=uint64, kmer=uint64, v=uint64))
    def get_value_at(table, subtable:int, bucket:int, slot:int, kmer:int):
        """
        Return the value at the given bucket, slot
        the position of the kmer in the super-k-mer
        """
        if vbits == 0: return 0
        startbit = subtable * subtablebits + bucket * bucketsizebits + shortcutbits + slot * slotbits + superkmerbits + vbits * kmer
        v = get_bits_at(table, startbit, vbits)
        return v

    @njit(nogil=True, locals=dict(
        subtable=uint64, bucket=uint64, slot=uint64, minimizer=uint64))
    def get_minimizer_at(table, subtable:int, bucket:int, slot:int):
        """
            Return the minimizer at the given bucket and slot.
        """
        startbit = subtable * subtablebits + bucket * bucketsizebits + shortcutbits + slot * slotbits + backupflag_bits + max_minimizer_occ_bits + choicebits
        minimizer = get_bits_at(table, startbit, minimizerbits)
        return minimizer

    @njit(nogil=True, locals=dict(
        subtable=uint64, bucket=uint64, slot=uint64, leftpart=uint64, leftsize=uint64,
        is_incomplete=uint8, leading_zeros=uint8))
    def get_leftpart_at(table, subtable:int, bucket:int, slot:int):
        """
            Get the left part of the super-k-mer at the given bucket and slot.
        """
        startbit = subtable * subtablebits + bucket * bucketsizebits + shortcutbits + slot * slotbits + backupflag_bits + max_minimizer_occ_bits + choicebits + minimizerbits + 1
        is_incomplete = get_bits_at(table, startbit - 1, 1)
        leftpart = get_bits_at(table, startbit, leftpart_bits)
        leftsize = k - m
        if is_incomplete:
            leading_zeros = ctlz(leftpart)
            leftsize = 64 - leading_zeros - 1
            leftpart = leftpart ^ (1 << leftsize)
            leftsize /= 2
        return leftpart, leftsize

    @njit(nogil=True, locals=dict(
        subtable=uint64, bucket=uint64, slot=uint64, rightpart=uint64, rightsize=uint64,
        is_incomplete=uint8, leading_zeros=uint8))
    def get_rightpart_at(table, subtable:int, bucket:int, slot:int):
        """
            Get the right part of the super-k-mer at the given bucket and slot.
        """
        startbit = subtable * subtablebits + bucket * bucketsizebits + shortcutbits + slot * slotbits + backupflag_bits + max_minimizer_occ_bits + choicebits + minimizerbits + 1 + leftpart_bits + 1
        is_incomplete = get_bits_at(table, startbit - 1, 1)
        rightpart = get_bits_at(table, startbit, rightpart_bits)
        rightsize = k - m
        if is_incomplete:
            trailing_zeros = cttz(rightpart)
            rightsize = rightpart_bits - trailing_zeros - 1
            rightpart = rightpart >> (trailing_zeros + 1)
            rightsize /= 2

        return rightpart, rightsize

    @njit(nogil=True, locals=dict(
        subtable=uint64, bucket=uint64, slot=uint64, sig=uint64,
        leftsize=uint64, leftpart=uint64, rightsize=uint64, rightpart=uint64))
    def get_item_at(table, subtable:int, bucket:int, slot:int, values):
        sig = get_signature_at(table, subtable, bucket, slot)
        leftpart, leftsize = get_leftpart_at(table, subtable, bucket, slot)
        rightpart, rightsize = get_rightpart_at(table, subtable, bucket, slot)
        start_value = k - m - leftsize
        end_value = rightsize + 1
        # values = np.zeros(max(end_value - start_value, 0), dtype=np.uint64) # TODO Array
        assert len(values) >= end_value - start_value
        for i in range(end_value - start_value):
            values[i] = get_value_at(table, subtable, bucket, slot, start_value+i)
        return sig, leftsize, leftpart, rightsize, rightpart

    @njit(nogil=True, locals=dict(
        bucket=uint64, slot=uint64, startbit=uint64, sig=uint64))
    def get_signature_at(table, subtable, bucket, slot):
        """Return the signature (choice, fingerprint) at the given bucket and slot."""
        startbit = subtable * subtablebits + bucket * bucketsizebits + shortcutbits + slot * slotbits + backupflag_bits + max_minimizer_occ_bits
        sig = get_bits_at(table, startbit, sigbits)
        return sig

    # High level getter #######

    @njit(nogil=True, locals=dict(
        subkey=uint64, subtable=uint64, leftpart=uint64,
        leftsize=uint64, rightpart=uint64, rightsize=uint64,
        default=uint64, NOTFOUND=uint64,
        bucket1=uint64, sig1=uint64, slot1=uint64, val1=uint64,
        bucket2=uint64, sig2=uint64, slot2=uint64, val2=uint64,
        bucket3=uint64, sig3=uint64, slot3=uint64, val3=uint64,
        bucketbits=uint32, check2=uint32, check3=uint32))
    def get_value_from_st_sk(table, subtable, subkey, leftpart, leftsize,
                             rightpart, rightsize, default=uint64(0)):
        """
        Return numpy array of uint64: the value for the given subkey,
        or the default if the subkey is not present.

        We need to check all slots in all possible buckets
        We can stop if:
        - We have found the minimizer exactly as many times as the occ bits indicate
        - One bucket has an empty slot (minimizer is not in the table)
        """
        assert leftsize + rightsize + m >= k  # TODO Remove

        values = np.zeros(leftsize + m + rightsize - k + 1, dtype=np.uint64)  # TODO Creats array
        # TODO support default value
        bucket1, sig1 = get_bs1(subkey)
        maxocc = -1
        occ = -1
        # check all slots in bucket 1
        for slot1 in range(0, bucketsize):
            # If we find an empty slot the minimizer does not exist in the table
            if is_slot_empty_at(table, subtable, bucket, slot1):
                return values
            sig = get_signature_at(table, subtable, bucket, slot1)
            if sig != sig1:
                continue

            # get the stored left and right part
            lp1, ls1 = get_leftpart_at(table, subtable, bucket1, slot1)
            rp1, rs1 = get_rightpart_at(table, subtable, bucket1, slot1)

            # Count how many bases on the left and right are equal
            sls = min(leftsize, ls3)  # smaller left size
            eq_l = cttz(2**(sls*2) | (leftpart ^ lp3))//2

            srs = min(rightsize, rs3)  # smaller right size
            eq_r = ctlz( (1<<(64-srs)) | ((rightpart << (64-rightsize*2)) ^ (rp3 << (64-rs3*2))))//2
            if eq_l + eq_r + m >= k: # we foud at least one k-mer
                nkmers = eq_r + eq_l + m - k + 1
                for i in range(nkmers):
                    kmer_pos = k-m-eq_l + i
                    values[i] = get_value_at(table, subtable, bucket1, slot1, kmer_pos)
                maxocc = get_occbits_at(table, subtable, bucket1, slot1)
                occ += 1
                if occ == maxocc:
                    return values

        # test for shortcut
        bucketbits = get_shortcutbits_at(table, subtable, bucket1)  # returns all bits set if bits==0
        if not bucketbits: return NOTFOUND
        check2 = bucketbits & 1
        check3 = bucketbits & 2 if shortcutbits >= 2 else 1

        if check2:
            bucket2, sig2 = get_bs2(subkey)
            for slot2 in range(0, bucketsize):
                # If we find an empty slot the minimizer does not exist in the table
                if is_slot_empty_at(table, subtable, bucket, slot2):
                    assert False # TODO: This should never happen
                sig = get_signature_at(table, subtable, bucket, slot2)
                if sig != sig2: continue

                # get the stored left and right part
                lp2, ls2 = get_leftpart_at(table, subtable, bucket2, slot2)
                rp2, rs2 = get_rightpart_at(table, subtable, bucket2, slot2)

                # Count how many bases on the left and right are equal
                sls = min(leftsize, ls3) # smaller left size
                eq_l = cttz(2**(sls*2) | (leftpart ^ lp3))//2

                srs = min(rightsize, rs3) # smaller right size
                eq_r = ctlz( (1<<(64-srs)) | ((rightpart << (64-rightsize*2)) ^ (rp3 << (64-rs3*2))))//2

                if eq_l + eq_r + m >= k: # we foud at least one k-mer
                    nkmers = eq_r + eq_l + m - k + 1
                    for i in range(nkmers):
                        kmer_pos = k-m-eq_l + i
                        values[i] = get_value_at(table, subtable, bucket2, slot2, kmer_pos)
                    occ += 1
                    if occ == maxocc:
                        return values

            # test for shortcuts
            if shortcutbits != 0:
                bucketbits = get_shortcutbits_at(table, subtable, bucket2)
                if shortcutbits == 1:
                    check3 = bucketbits  # 1 or 0
                else:
                    check3 &= bucketbits & 2

        if not check3: return values # TODO NOTFOUND default value
        bucket3, sig3 = get_bs3(subkey)
        for slot3 in range(0, bucketsize):
                # If we find an empty slot the minimizer does not exist in the table
                if is_slot_empty_at(table, subtable, bucket, slot3):
                    assert False # TODO: This should never happen
                sig = get_signature_at(table, subtable, bucket, slot3)
                if sig != sig3: continue

                # get the stored left and right part
                lp3, ls3 = get_leftpart_at(table, subtable, bucket3, slot3)
                rp3, rs3 = get_rightpart_at(table, subtable, bucket3, slot3)

                # Count how many bases on the left and right are equal
                sls = min(leftsize, ls3) # smaller left size
                eq_l = cttz(2**(sls*2) | (leftpart ^ lp3))//2

                srs = min(rightsize, rs3) # smaller right size
                eq_r = ctlz( (1<<(64-srs)) | ((rightpart << (64-rightsize*2)) ^ (rp3 << (64-rs3*2))))//2

                if eq_l + eq_r + m >= k: # we foud at least one k-mer
                    nkmers = eq_r + eq_l + m - k + 1
                    for i in range(nkmers):
                        kmer_pos = k-m-eq_l + i
                        values[i] = get_value_at(table, subtable, bucket3, slot3, kmer_pos)
                    occ += 1
                    if occ == maxocc:
                        return values
        if occ < maxocc:
            assert False # Check in second table

        return values # TODO NOTFOUND default value

    ####### Setter ########

    @njit(nogil=True, locals=dict(
        bucket=uint64, startbit=uint64, v=uint64))
    def set_shortcutbits_at(table:int, subtable:int, bucket:int, bit:int):
        """Store the shortcut bits at the given bucket."""
        if shortcutbits == 0: return
        startbit = subtable * subtablebits + bucket * bucketsizebits + bit -1
        set_bits_at(table, startbit, 1, 1) # set exactly one bit to 1


    @njit(nogil=True, locals=dict(
        bucket=uint64, slot=uint64, startbit=uint64, occ=uint64))
    def set_occbits_at(table, subtable, bucket, slot, occ):
        """
           Set the occurence counter bits at the given bucket and slot
           0: More than 3 times
           1-3: Occurs 1-3 times
        """
        startbit = subtable * subtablebits + bucket * bucketsizebits + shortcutbits + slot * slotbits + backupflag_bits
        set_bits_at(table, startbit, occ, max_minimizer_occ_bits)

    @njit(nogil=True, locals=dict(
        bucket=uint64, slot=uint64, startbit=uint64, flag=uint64))
    def set_backupflag_at(table, subtable, bucket, slot, flag):
        """
           Set the flag if a k-mer with this minimizer is stored in the backup table
        """
        startbit = subtable * subtablebits + bucket * bucketsizebits + shortcutbits + slot * slotbits
        set_bits_at(table, startbit, flag, backupflag_bits)

    @njit(nogil=True, locals=dict(
            bucket=uint64, slot=uint64, value=uint64))
    def set_value_at(table, subtable:int, bucket:int, slot:int, kmer:int, value:int):
        """
           Set the value at the given bucket and slot.
           Value is placed after the super-k-mer.
        """
        if valuebits == 0: return
        startbit = subtable * subtablebits + bucket * bucketsizebits + shortcutbits + slot * slotbits + superkmerbits + vbits * kmer
        set_bits_at(table, startbit, value, vbits)

    @njit(nogil=True, locals=dict(
            subtable=uint64, bucket=uint64, slot=uint64, minimizer=uint64))
    def set_minimizer_at(table, subtable:int, bucket:int, slot:int, minimizer:int):
        """
            Set the minimizer at the given bucket and slot.
        """
        startbit = subtable * subtablebits + bucket * bucketsizebits + shortcutbits + slot * slotbits + backupflag_bits + max_minimizer_occ_bits + choicebits
        set_bits_at(table, startbit, minimizer, minimizerbits)

    @njit(nogil=True,  locals=dict(
            bucket=uint64, slot=uint64, startbit=uint64, sig=uint64))
    def set_signature_at(table, subtable, bucket, slot, sig):
        """Set the signature (choice, fingerprint) at the given bucket and slot."""
        startbit = subtable * subtablebits + bucket * bucketsizebits + shortcutbits + slot * slotbits + backupflag_bits + max_minimizer_occ_bits
        set_bits_at(table, startbit, sig, sigbits)

    @njit(nogil=True, locals=dict(
            subtable=uint64, bucket=uint64, slot=uint64, leftpart=uint64, leftsize=uint64))
    def set_leftpart_at(table, subtable:int, bucket:int, slot:int, leftpart:int, leftsize:int):
        """
            Set the left part of the super-k-mer at the given bucket and slot.
            If leftsize is smaller than k-m:
            - Set the incomplete bit for the left part to 1.
            - Set the first bit in the leftpart to 1 that is not used

            Example:
            uint32
            leftsize 7 (14 bit)
            000000000000000001XXXXXXXXXXXXXX
        """
        startbit = subtable * subtablebits + bucket * bucketsizebits + shortcutbits+ slot * slotbits + backupflag_bits + max_minimizer_occ_bits + choicebits + minimizerbits + 1
        if leftsize != k-m:
            leftpart = leftpart | (1 << (leftsize*2))
            set_bits_at(table, startbit-1, 1, 1)
        else:
            set_bits_at(table, startbit-1, 0, 1)
            # set_incomplete(table, subtable, bucket, slot, left=True)
            """ TODO
            we can skip this if we set startbit to startbit-1 and and the most significant bit is 1
            Does not work if the left size needs all 64 bits (32 bps)
            """
        set_bits_at(table, startbit, leftpart, leftpart_bits)

    @njit(nogil=True, locals=dict(
        subtable=uint64, bucket=uint64, slot=uint64, rightpart=uint64, rightsize=uint64))
    def set_rightpart_at(table, subtable:int, bucket:int, slot:int, rightpart:int, rightsize:int):
        """
            Set the right part of the super-k-mer at the given bucket and slot.
            If rightsize is smaller than k-m:
            - Set the incomplete bit for the right part to 1.
            - Set the first bit in the rightpart to 1 that is not used


            Example:
            uint32
            rightsize 7 (14 bit)
            XXXXXXXXXXXXXX100000000000000000
        """
        startbit = subtable * subtablebits + bucket * bucketsizebits + shortcutbits+ slot * slotbits + backupflag_bits + max_minimizer_occ_bits + choicebits + minimizerbits + 1 + leftpart_bits + 1
        if rightsize != k-m:
            rightpart = (rightpart << 1) | 1
            rightpart = rightpart << (2*(k-m-rightsize-1))

            set_bits_at(table, startbit-1, 1, 1)
        else:
            set_bits_at(table, startbit-1, 0, 1)
            # set_incomplete(table, subtable, bucket, slot, left=False)
            """ TODO
            we can skip this if we set startbit to startbit-1 and and the most significant bit is 1
            Does not work if the right size needs all 64 bits (32 bps)
            """
        set_bits_at(table, startbit, rightpart, rightpart_bits)

    @njit(nogil=True, locals=dict(
        subtable=uint64, bucket=uint64, slot=uint64, sig=uint64,
        leftpart=uint64, leftsize=uint64, rightpart=uint64, rightsize=uint64))
    def set_item_at(table, subtable, bucket, slot, sig, leftpart, leftsize, rightpart, rightsize, values):
        set_signature_at(table, subtable, bucket, slot, sig)
        set_leftpart_at(table, subtable, bucket, slot, leftpart, leftsize)
        set_rightpart_at(table, subtable, bucket, slot, rightpart, rightsize)
        for i in range(leftsize+m+rightsize-k+1):
            kmer = k-m-leftsize+i
            set_value_at(table, subtable, bucket, slot, kmer, values[i])



    # Utility functions
    @njit(nogil=True, inline='always', locals=dict(b=boolean))
    def is_slot_empty_at(table, subtable, bucket, slot):
        """Return whether a given slot is empty (check by choice)"""
        c = get_choicebits_at(table, subtable, bucket, slot)
        b = (c == 0)
        return b

    @njit(nogil=True, inline='always', locals=dict(
            sig=uint64, c=uint64, fpr=uint64))
    def signature_to_choice_fingerprint(sig):
        """Return (choice, fingerprint) from signature"""
        fpr = sig & minimizermask
        c = (sig >> uint64(minimizerbits)) & choicemask
        return (c, fpr)

    @njit(nogil=True, inline='always', locals=dict(
            sig=uint64, choice=uint64, fpr=uint64))
    def signature_from_choice_fingerprint(choice, fpr):
        """Return signature from (choice, fingerprints)"""
        sig = (choice << uint64(minimizerbits)) | fpr
        return sig

    # define the get_subkey_from_bucket_signature function
    get_subkey_from_bucket_signature = compile_get_subkey_from_bucket_signature(
        get_subkey, signature_to_choice_fingerprint, base=base)
    get_subkey_choice_from_bucket_signature = compile_get_subkey_choice_from_bucket_signature(
        get_subkey, signature_to_choice_fingerprint, base=base)

    # define the occupancy computation function
    get_statistics = compile_get_statistics(backuptable, "c", k, m, subtables,
        choices, nbuckets, bucketsize, nvalues, shortcutbits,
        get_value_at, get_signature_at,
        signature_to_choice_fingerprint, get_shortcutbits_at)

    update, update_ssk \
        = compile_update_by_randomwalk(k, m, bucketsize, max_minimizer_occ,
            backuptable,
            get_bs, get_item_at, set_occbits_at,
            set_item_at, set_value_at,
            is_slot_empty_at, get_occbits_at,
            get_backupflag_at, set_backupflag_at,
            get_subkey_choice_from_bucket_signature,
            get_subtable_subkey_from_key,
            prefetch_bucket, ccode,
            update_value=update_value, overwrite=False,
            allow_new=True, allow_existing=True,
            maxwalk=maxwalk, prefetch=prefetch)

    return create_SKHash(locals())



######## Move to another file?
def compile_getps_from_getpf(get_bfx, choice, fprbits):
    @njit(nogil=True, inline='always', locals=dict(
            p=uint64, f=uint64, sig=uint64))
    def get_bsx(code):
        (p, f) = get_bfx(code)
        sig = uint64((choice << uint64(fprbits)) | f)
        return (p, sig)
    return get_bsx

def compile_update_by_randomwalk(k, m, bucketsize, max_minimizer_occ,
            backuptable,
            get_bs, get_item_at, set_occbits_at, set_item_at,
            set_value_at, is_slot_empty_at, get_occbits_at,
            get_backupflag_at, set_backupflag_at,
            get_subkey_choice_from_bucket_signature,
            get_subtable_subkey_from_key,
            prefetch_bucket, ccode,
            *,
            update_value=None, overwrite=False,
            allow_new=False, allow_existing=False,
            maxwalk=1000, prefetch=False):
    """return a function that stores or modifies an item"""

    update_backup = backuptable.update
    update_existing_backup = backuptable.update_existing
    choices = len(get_bs)
    assert choices <= 3
    (get_bs1, get_bs2, get_bs3) = get_bs
    LOCATIONS = choices * bucketsize
    if LOCATIONS < 2:
        raise ValueError(f"ERROR: Invalid combination of bucketsize={bucketsize} * choices={choices}")
    # if (update_value is None or overwrite) and allow_existing:
    #     update_value = njit(
    #         nogil=True, locals=dict(old=uint64, new=uint64)
    #         )(lambda old, new: new)
    # if not allow_existing:
    #     update_value = njit(
    #         nogil=True, locals=dict(old=uint64, new=uint64)
    #         )(lambda old, new: old)

    @njit(nogil=True, locals=dict(subkey=uint64, choice=uint64))
    def get_bucket_sig(subkey, choice):
        # we want this: bucket, sig = (get_bs[choice])(subkey)
        # but this does not work
        if choice == 0:
            bucket, sig = get_bs1(subkey)
        elif choice == 1:
            bucket, sig = get_bs2(subkey)
        elif choice == 2:
            bucket, sig = get_bs3(subkey)
        else:
            assert False
        # TODO: remove assert? return (-1), (-1) ?
        return bucket, sig

    @njit(nogil=True,
          locals=dict(minimizer=uint64, leftpart=uint64, leftsize=uint64,
                      rightpart=uint64, rightsize=uint64, subtable=uint64,
                      status=int64, result=uint64))
    def insert_in_backup_table(bt, lock, subtable, minimizer, leftpart, leftsize, rightpart, rightsize, values, found_kmers):
        # Try to lock backup table
        while vload(lock,0) != subtable:
            if vload(lock,0) == uint64(-1):
                if cmpxchg(lock, 0, uint64(-1), subtable):
                    break
            else:
                pause()

        assert vload(lock, 0) == subtable

        for i in range(len(found_kmers)):
            if found_kmers[i] == 0:
                kmer_leftsize = leftsize - i
                kmer_leftpart = (leftpart & (4**(kmer_leftsize)-1)) << 2*(k-kmer_leftsize)
                kmer_rightsize = k-m-kmer_leftsize
                kmer_rightpart = rightpart >> (2*(rightsize-kmer_rightsize))
                kmer_minimizer = minimizer << 2*kmer_rightsize
                kmer = kmer_leftpart | kmer_minimizer | kmer_rightpart
                kmer = ccode(kmer)
                status, result = update_backup(bt, kmer, values[i])
                if status == 0: break
                found_kmers[i] = 1

        assert vload(lock, 0) == subtable
        vstore(lock, 0, uint64(-1))

        return (status, result)

    @njit(nogil=True,
          locals=dict(minimizer=uint64, leftpart=uint64, leftsize=uint64,
                      rightpart=uint64, rightsize=uint64, subtable=uint64,
                      status=int64, result=uint64))
    def update_in_backup_table(bt, lock, subtable, minimizer, leftpart, leftsize, rightpart, rightsize, values, found_kmers):
        # Try to lock backup table
        while vload(lock,0) != subtable:
            if vload(lock,0) == uint64(-1):
                if cmpxchg(lock, 0, uint64(-1), subtable):
                    break
            else:
                pause()

        assert vload(lock, 0) == subtable

        for i in range(len(found_kmers)):
            if found_kmers[i] == 0:
                kmer_leftsize = leftsize - i
                kmer_leftpart = (leftpart & (4**(kmer_leftsize)-1)) << 2*(k-kmer_leftsize)
                kmer_rightsize = k-m-kmer_leftsize
                kmer_rightpart = rightpart >> (2*(rightsize-kmer_rightsize))
                kmer_minimizer = minimizer << 2*kmer_rightsize
                kmer = kmer_leftpart | kmer_minimizer | kmer_rightpart
                kmer = ccode(kmer)
                status, result = update_existing_backup(bt, kmer, values[i])
                if status & 128 != 0:
                    found_kmers[i] = 1
        assert vload(lock, 0) == subtable
        vstore(lock, 0, uint64(-1))
        return (1, 1)

    @njit(nogil=True, locals=dict(
          subtable=uint64,choices=uint64,
          subkey=uint64, leftpart=uint64, leftsize=uint64,
          rightpart=uint64, rightsize=uint64, occ=uint64, btflag=uint64,
          xsubkey=uint64, xleftpart=uint64, xleftsize=uint64,
          xrightpart=uint64, xrightsize=uint64, xocc=uint64,
          stored_subkey=uint64, stored_leftpart=uint64, stored_leftsize=uint64,
          stored_rightpart=uint64, stored_rightsize=uint64, stored_occ=uint64,
          stored_choice=uint64, stored_sig=uint64,
          sig=uint64, bucket=uint64, choice=uint64, lchoice=uint64, slot=uint64,
          steps=uint64, maxwalk=uint64, location=uint64, lastlocation=uint64,
          c=uint64, xbtflag=uint64, stored_btflag=uint64,))
    def random_walk(table, subtable, subkey,
                    leftpart, leftsize, rightpart, rightsize, values, stored_values, xvalues, occ, btflag):
        steps = 0
        lastlocation = uint64(-1)

        xbtflag = btflag
        xsubkey = subkey
        xleftpart = leftpart
        xleftsize = leftsize
        xrightpart = rightpart
        xrightsize = rightsize
        xvalues[:] = values[:]
        xocc = occ

        while steps < maxwalk:
            # We get here iff all buckets are full.
            # Check the next hashfunctions and buckets if a slot is empty
            for choice in range(choices):
                bucket, sig = get_bucket_sig(xsubkey, choice)
                for slot in range(bucketsize):
                    # check if slot is empty
                    if is_slot_empty_at(table, subtable, bucket, slot):
                        #Only insert the super-k-mer if have an empty slot and did not find the minimizer before
                        set_item_at(table, subtable, bucket, slot,
                            sig, xleftpart, xleftsize, xrightpart, xrightsize, xvalues)
                        set_occbits_at(table, subtable, bucket, slot, xocc)
                        set_backupflag_at(table, subtable, bucket, slot, xbtflag)
                        return (int32(128|choice), steps)

            # Pick a random location;
            # store item there and continue with evicted item.
            location = np.random.randint(LOCATIONS)
            while location == lastlocation:
                location = np.random.randint(LOCATIONS)
            lastlocation = location
            slot = location // choices
            c = location % choices
            bucket, sig = get_bucket_sig(xsubkey, c)

            # get stored item
            stored_sig, stored_leftsize, stored_leftpart, stored_rightsize, stored_rightpart = get_item_at(table, subtable, bucket, slot, stored_values)
            stored_subkey, stored_choice = get_subkey_choice_from_bucket_signature(bucket, stored_sig)
            # Original minimizer
            if stored_subkey == subkey:
                continue

            stored_occ = get_occbits_at(table, subtable, bucket, slot)
            stored_btflag = get_backupflag_at(table, subtable, bucket, slot)

            set_item_at(table, subtable, bucket, slot, sig, xleftpart, xleftsize, xrightpart, xrightsize, xvalues)
            set_occbits_at(table, subtable, bucket, slot, xocc)
            set_backupflag_at(table, subtable, bucket, slot, xbtflag)

            xsubkey = stored_subkey
            xleftpart = stored_leftpart
            xleftsize = stored_leftsize
            xrightpart = stored_rightpart
            xrightsize = stored_rightsize
            xvalues[:] = stored_values[:]
            xocc = stored_occ
            xbtflag = stored_btflag

            steps += 1
            # loop again
        return (int32(0), steps)



    @njit(nogil=True,
        locals=dict(sig=uint64, sig1=uint64, startbit=uint64, choice=uint64,
        bucket=uint64, slot=uint64, stored_sig=uint64, stored_leftsize=uint64,
        stored_leftpart=uint64, stored_rightsize=uint64, stored_rightpart=uint64,
        sls=uint64, srs=uint64, eq_l=uint64, eq_r=uint64, kmer_pos=uint64, offset=uint64,
        new_leftsize=uint64, new_leftpart=uint64, new_rightsize=uint64, new_rightpart=uint64,
        lastchoice=uint64, lastbucket=uint64, lastslot=uint64, lastsig=uint64,
        f_leftpart=uint64, f_leftsize=uint64, f_rightpart=uint64, f_rightsize=uint64,
        s_leftpart=uint64, s_leftsize=uint64, s_rightpart=uint64, s_rightsize=uint64,
        occ_value=uint64, max_minimizer_occ=uint64, temp_occ=uint64, btflag=uint64,
        ))
    def update_ssk(table, bt, lock, subtable, flag, minimizer, subkey,
                   leftpart, leftsize, rightpart, rightsize, values):
        assert (not flag) or (leftsize+m+rightsize == k)
        occ_value = uint64(-1)
        btflag = 0
        kmers_in_superkmer = leftsize + m + rightsize - k + 1

        # Problem: many array allocations --> slow !
        # found_kmers can be a bit-vector (uint64).
        found_kmers = np.zeros(kmers_in_superkmer, dtype=np.uint8) # TODO replace with one uint64
        nfound = 0

        # these 7 arrays (in one big one) are a problem.
        # max_minimizer_occ is the maximum possible number of occurrences of the same minimizer in the hash table.
        array = np.zeros((max_minimizer_occ, 7), dtype=np.uint64)
        buckets = array[:, 0]
        slots = array[:, 1]
        sigs = array[:, 2]
        eq_ls = array[:, 3]
        eq_rs = array[:, 4]
        leftextend = array[:, 5]
        rightextend = array[:, 6]
        # buckets = np.zeros(max_minimizer_occ, dtype=np.uint64)
        # slots = np.zeros(max_minimizer_occ, dtype=np.uint64)
        # sigs = np.zeros(max_minimizer_occ, dtype=np.uint64)
        # eq_ls = np.zeros(max_minimizer_occ, dtype=np.uint64)
        # eq_rs = np.zeros(max_minimizer_occ, dtype=np.uint64)
        # leftextend = np.zeros(max_minimizer_occ, dtype=np.uint64)
        # rightextend = np.zeros(max_minimizer_occ, dtype=np.uint64)

        stored_values = np.zeros(k-m+1, dtype=np.uint64)
        rw_values = np.zeros(k-m+1, dtype=np.uint64)

        # save postion of last empty slot
        lastchoice = uint64(-1)
        lastbucket = uint64(-1)
        lastslot = uint64(-1)
        lastsig = uint64(-1)

        # check all possible slots for the minimizer
        stop_search = False

        for choice in range(choices):
            bucket, sig = get_bucket_sig(subkey, choice)
            for slot in range(bucketsize):
                # check if slot is empty
                if is_slot_empty_at(table, subtable, bucket, slot):
                    #Only insert the super-k-mer if have an empty slot and did not find the minimizer before
                    if allow_new and nfound == 0 and not flag:
                        assert occ_value == uint64(-1)
                        set_item_at(table, subtable, bucket, slot,
                            sig, leftpart, leftsize, rightpart, rightsize, values)
                        set_occbits_at(table, subtable, bucket, slot, 1)
                        return (int32(128|choice), 1)
                    # we found an empty slot but we could not insert the new super-k-mer
                    # stop searching for existing minimizer
                    stop_search = True
                    lastchoice = choice
                    lastbucket = bucket
                    lastslot = slot
                    lastsig = sig
                    break

                # search for the signature
                stored_sig, stored_leftsize, stored_leftpart, stored_rightsize, stored_rightpart = get_item_at(table, subtable, bucket, slot, stored_values)
                if stored_sig != sig: continue

                # Get the number of occurences of this minimizer
                # and check if it is stored in the backup table
                occ_value = get_occbits_at(table, subtable, bucket, slot)
                btflag = get_backupflag_at(table, subtable, bucket, slot)

                buckets[nfound] = bucket
                slots[nfound] = slot
                sigs[nfound] = sig

                # Found signature check if we can update k-mers

                ## Calculate the overlap
                # TODO: perhaps cttz and ctlz is not fast?
                sls = min(leftsize, stored_leftsize) # smaller left size
                eq_l = cttz(2**(sls*2) | (leftpart ^ stored_leftpart))//2

                srs = min(rightsize, stored_rightsize) # smaller right size
                eq_r = ctlz( (1<<(64-srs*2-1)) | ((rightpart << (64-rightsize*2)) ^ (stored_rightpart << (64-stored_rightsize*2))))//2

                eq_ls[nfound] = eq_l
                eq_rs[nfound] = eq_r

                #We can only extend this super-k-mer if we have an overlapp of at least k-1
                if eq_l + m + eq_r >= k - 1:
                    leftextend[nfound] = (stored_leftsize < k - m) and (stored_leftsize == eq_l)
                    rightextend[nfound] = (stored_rightsize < k - m) and (stored_rightsize == eq_r)
                covered_kmers = max(eq_l + eq_r + m - k + 1, 0)
                if covered_kmers >= 1: # We can update at least one k-mer
                    # mark found k-mers
                    assert (found_kmers[leftsize-eq_l:leftsize-eq_l+covered_kmers] == 0).all()
                    found_kmers[leftsize-eq_l:leftsize-eq_l+covered_kmers] = 1
                    for i in range(covered_kmers):
                        pos_values = stored_leftsize-eq_l+i
                        val = stored_values[pos_values]
                        v = update_value(val, values[leftsize-eq_l+i])
                        if v != val:
                            set_value_at(table, subtable, bucket, slot, k-m-eq_l+i, v)
                    if sum(found_kmers) == len(found_kmers):
                        return (int32(128|choice), 1)

                nfound += 1

                # if we found the max number of exisiting k-mers
                if nfound == max_minimizer_occ:
                    stop_search = True
                    break

            if stop_search: break

        if flag:
            status_bt, steps_bt = insert_in_backup_table(bt, lock, subtable, minimizer, leftpart, leftsize, rightpart, rightsize, values, found_kmers)
            if status_bt & 128 == 0: return (status_bt, steps_bt)
            if occ_value != uint64(-1):
                if btflag == 0:
                    for i in range(nfound):
                        set_backupflag_at(table, subtable, buckets[i], slots[i], 1)
            else:
                # insert a super-k-mer without left and right part
                if lastchoice != uint64(-1):
                    set_item_at(table, subtable, lastbucket, lastslot, lastsig, 0, 0, 0, 0, values)
                    set_occbits_at(table, subtable, lastbucket, lastslot, 1)
                    set_backupflag_at(table, subtable, lastbucket, lastslot, 1)
                else:
                    status_rw, steps_rw = random_walk(table, subtable, subkey, 0, 0, 0, 0, values, stored_values, rw_values, 1, 1)
                    if status_rw & 128 == 0: return (status_rw, steps_rw)
            return (int32(128 | 4), 1)

        if btflag:
            status, steps = update_in_backup_table(bt, lock, subtable, minimizer, leftpart, leftsize, rightpart, rightsize, values, found_kmers)
            if status == 0: return
            if sum(found_kmers) == len(found_kmers):
                return (int32(128|choice+1), 1)
        # Found all exisiting positions and updated all existing k-mers in this table

        # Check if we can extend one of the existing super-kmers
        # We can do this before checking the second table
        # because we always extend before we use the second table
        # If we can extend, the k-mer is not in the second table

        # new extend approach: check each k-mer/block of not inserted k-mers
        # is one of the stored super-k-mers extendable
        if sum(leftextend) != 0 or sum(rightextend) !=0:
            for start in range(len(found_kmers)):
                if found_kmers[start] == 1: continue
                for end in range(start, len(found_kmers)+1):
                    if found_kmers[end] == 1: break
                # if start < end: continue
                new_leftsize = leftsize - start
                new_leftpart = leftpart & ((4**new_leftsize)-1)
                new_rightsize = k-m-new_leftsize + end - start -1
                new_rightpart = rightpart >> (2*(rightsize-new_rightsize))

                for pos in range(nfound):
                    if new_leftsize + new_rightsize - min(eq_ls[pos], new_leftsize) - min(eq_rs[pos], new_rightsize) != end-start: continue
                    if new_rightsize>eq_rs[pos]:
                        if not rightextend[pos]: continue
                    if new_leftsize>eq_ls[pos]:
                        if not leftextend[pos]: continue
                    stored_sig, stored_leftsize, stored_leftpart, stored_rightsize, stored_rightpart = get_item_at(table, subtable, buckets[pos], slots[pos], stored_values)

                    assert stored_sig == sigs[pos]
                    nstored_values = stored_leftsize+m+stored_rightsize-k+1

                    new_values = rw_values[:end-start + nstored_values] # TODO
                    if new_leftsize < stored_leftsize:
                        new_leftsize = stored_leftsize
                        new_leftpart = stored_leftpart
                        new_values[:nstored_values] = stored_values[:nstored_values]
                        new_values[nstored_values:] = values[start:end]
                    if new_rightsize < stored_rightsize:
                        new_rightsize = stored_rightsize
                        new_rightpart = stored_rightpart
                        new_values[:end-start] = values[start:end]
                        new_values[end-start:end-start+nstored_values] = stored_values[:nstored_values]
                    set_item_at(table, subtable, buckets[pos], slots[pos], sigs[pos], new_leftpart, new_leftsize, new_rightpart, new_rightsize, new_values)
                    if eq_ls[pos] < new_leftsize:
                        eq_ls[pos] = new_leftsize
                        leftextend[pos] = 0
                    if eq_rs[pos] < new_rightsize:
                        eq_rs[pos] = new_rightsize
                        rightextend[pos] = 0
                    assert (found_kmers[start:end] == 0).all()
                    found_kmers[start:end] = 1
                    break
                if sum(found_kmers) == len(found_kmers):
                     return (int32(128|choice+1), 1)


        # All k-mers updated or inserted (extended)?
        if sum(found_kmers) == len(found_kmers):
            return (int32(128|choice+1), 1)

        # not all k-mers found or extended

        # Check if we need to insert/update the remaining k-mers in the second table
        if occ_value == max_minimizer_occ or btflag:
            if not btflag:
                for i in range(nfound):
                    set_backupflag_at(table, subtable, buckets[i], slots[i], 1)
            return insert_in_backup_table(bt, lock, subtable, minimizer, leftpart, leftsize, rightpart, rightsize, values, found_kmers)

        # Minimizer is stored less than max_minimizer_occ times
        # We can insert atleast on new super-k-mmer
        # if no k-mer was updated in the table, insert super-k-mer
        if sum(found_kmers) == 0:
            # We stopped at an empty slot
            if occ_value == uint64(-1):
                occ_value = 1
            else:
                occ_value += 1

            if lastchoice != uint64(-1):
                set_item_at(table, subtable, lastbucket, lastslot, lastsig, leftpart, leftsize, rightpart, rightsize, values)
                set_occbits_at(table, subtable, lastbucket, lastslot, occ_value)
                for i in range(nfound):
                    set_occbits_at(table, subtable, buckets[i], slots[i], occ_value)
                return (int32(128|lastchoice), 1)
            else:
                for i in range(nfound):
                    set_occbits_at(table, subtable, buckets[i], slots[i], occ_value)
                return random_walk(table, subtable, subkey, leftpart, leftsize, rightpart, rightsize, values, stored_values, rw_values, occ_value, btflag)


        else:
            # At least one k-mer was updated, we need to split the remaining super-k-mer
            for start in range(len(found_kmers)):
                if found_kmers[start] == 1: continue
                for end in range(start, len(found_kmers)+1):
                    if found_kmers[end] == 1: break
                inserted = False
                new_leftsize = leftsize - start
                new_leftpart = leftpart & ((4**new_leftsize)-1)
                new_rightsize = k-m-new_leftsize + end - start -1
                new_rightpart = rightpart >> (2*(rightsize-new_rightsize))

                if occ_value == max_minimizer_occ or btflag:
                    if not btflag:
                        for i in range(nfound):
                            set_backupflag_at(table, subtable, buckets[i], slots[i], 1)
                    return insert_in_backup_table(bt, lock, subtable, minimizer, leftpart, leftsize, rightpart, rightsize, values, found_kmers)

                # search for an empty slot
                for choice in range(lastchoice, choices):
                    bucket, sig = get_bucket_sig(subkey, choice)
                    lastchoice = choice
                    for slot in range(bucketsize):
                        if is_slot_empty_at(table, subtable, bucket, slot):
                            occ_value += 1
                            for i in range(nfound):
                                set_occbits_at(table, subtable, buckets[i], slots[i], occ_value)
                            set_item_at(table, subtable, bucket, slot, sig, new_leftpart, new_leftsize, new_rightpart, new_rightsize, values[start:end])
                            set_occbits_at(table, subtable, bucket, slot, occ_value)
                            sigs[nfound] = sig
                            buckets[nfound] = bucket
                            slots[nfound] = slot
                            nfound += 1
                            inserted = True
                            break
                    if inserted == True: break
                else:
                    # If no empty spot do a random walk
                    occ_value += 1
                    for i in range(nfound):
                        set_occbits_at(table, subtable, buckets[i], slots[i], occ_value)
                    status, steps = random_walk(table, subtable, subkey, new_leftpart, new_leftsize, new_rightpart, new_rightsize, values[start:end], stored_values, rw_values, occ_value, btflag)
                    if status == 0: return (int32(0), steps)

                assert (found_kmers[start:end] == 0).all()
                found_kmers[start:end] = 1
                if sum(found_kmers) == len(found_kmers): break

            assert (found_kmers == 1).all()
            return(int32(128|choice), 1)


        return (int32(0), 1)


    @njit(nogil=True, locals=dict(
            subtable=uint64, subkey=uint64))
    def update(table, bt, lock, flag, minimizer, leftpart, leftsize, rightpart, rightsize, values):
        assert leftsize + m + rightsize - k + 1 == len(values)
        subtable, subkey = get_subtable_subkey_from_key(minimizer)
        return update_ssk(table, bt, lock, subtable, flag, minimizer, subkey, leftpart, leftsize, rightpart, rightsize, values)

    return update, update_ssk
