"""
lowlevel/packedarray.py:
implementation of a tightly packed integer array.
Values can range from 0 to M (including M).
Additions are silently capped at M, subtractions at 0.

For each individual value of M, we find the best way
of arranging the values, so as few bits as possible are wasted.
"""

from math import ceil, log2
from collections import namedtuple

from numba import njit, int64, uint64

from . import debug
from .intbitarray import intbitarray


PackedArray = namedtuple("PackedArray", [
    "size",
    "maximum",  # maximum stored value (values are 0 .. maximum)
    "group_size",  # number of values in a group (k)
    "group_bits",  # number of bits in a group: 2**group_bits >= n**k
    "loss",  # lost bits per element
    "ngroups",  # number of value groups, so ngroups * group_size >= size
    "total_bits_lost",
    "array",
    "get_group",
    "set_group",
    "get",
    "set",
    "inc",
    "dec",
    "is_equal",
    ])


PINF = float("inf")  # positive infinity (float)
NINF = -PINF  # negative infinity (float)


def _packing(n):
    """
    For given n, find the best number of bits (nb <= 64) and k
    to store a k-tuple of an n-element set {0, ..., n - 1}.

    For every k = 1, 2, ..., find the smallest number B(k) of bits
    that will hold n**k values, i.e., 2**B >= n**k,
    so B(k) = int(ceil(k * log2(n))) for as long as B(k) <= 64.
    Then compute the bit loss per element
    loss(k) = (B(k) - k * log2(n)) / k  =  B(k)/k - log2(n)
    and find the smallest k that minimizes the loss.
    Return the optimal (k, B(k), loss(k))
    """
    logn = log2(n)
    k, bestk = 1, 0
    bestloss = 99.9
    while True:
        B = int(ceil(k * logn))
        if B > 64:
            break
        loss = B / k - logn
        if loss < bestloss:
            bestloss = loss
            bestk = k
        if bestloss <= 0.0:
            break
        k += 1
    B = int(ceil(bestk * logn))
    return (bestk, B, bestloss)


_PACKING_CACHE = {0: (2**64, NINF, 0.0), 1: (2**64, 0, 0.0)}


def packedarray(size, maximum, *, _cache=_PACKING_CACHE):
    """
    Initialize and return an array of 'size' (unsigned) integers,
    each of which can be in the range 0 .. maximum (inclusive).

    For example packedarray(100, 9) is an array of 100 integers,
    each of which can take 10 different values (0 .. 9).


    Provide get and set methods to read and wite
    each width-bit word in the array.
    The width is fixed at creation time and cannot be changed.
    If more flexibility is required, use a bitarray.

    If width is in {1, 2, 4, 8, 16, 32, 64},
    optimized access functions are used,
    as no width-bit word can span two different uint64s.
    Other widths may be slower due to the involved bit shifting.

    """
    if not isinstance(maximum, int) or maximum <= 0 or maximum >= 2**64:
        raise ValueError(f"packedarray: {maximum=} must be between 1 and 2**64 - 1.")
    debugprint0, debugprint1, debugprint2 = debug.debugprint
    # compute group_size: number of values in a group
    # compute group_bits: number of bits in a group
    # compute loss: number of lost bits per element
    # compute total_bits_lost: total number of lost bits
    n = maximum + 1  # number of distinct values: 0 .. maximum
    if n in _cache:
        group_size, group_bits, loss = _cache[n]
    else:
        group_size, group_bits, loss = _cache[n] = _packing(n)
    debugprint2(f"- packedarray: {maximum=}, {n=}, {group_size=}, {group_bits=}, {loss=:.5f} bits/element")
    ngroups = int(ceil(size / group_size))
    nuint64 = int(ceil(ngroups * group_bits / 64))
    total_bits_needed = nuint64 * 64
    total_bits_lost = total_bits_needed - size * log2(n)
    debugprint1(f"  - {size=} => {ngroups=}, total loss: {total_bits_lost/8/1024:.3f} KiB")
    iba = intbitarray(ngroups, group_bits, alignment=64)
    get_group = iba.get
    set_group = iba.set
    is_equal = iba.is_equal
    divs = tuple(uint64(n**j) for j in range(group_size))
    debugprint2(f"  - {divs=}")

    @njit(nogil=True, locals=dict(
        group=int64, j=int64, gv=uint64, div=uint64, value=uint64))
    def get(a, i):
        """return the i-th integer from a[:]"""
        group = i // group_size
        j = i % group_size
        gv = get_group(a, group)
        div = divs[j]
        value = uint64(gv // div) % uint64(n)
        return value

    @njit(nogil=True, locals=dict(
        group=int64, j=int64, gv=uint64, div=uint64, oldvalue=uint64, value=uint64, chg=int64))
    def set(a, i, value):
        """set the 'i'-th word of 'a' to 'value'"""
        group = i // group_size
        j = i % group_size
        gv = get_group(a, group)
        div = divs[j]
        oldvalue = uint64(gv // div) % uint64(n)
        # print(i, group, j, oldvalue, value, gv)
        gv -= uint64(div * oldvalue)
        # print("   ", gv)
        delta = uint64(div * uint64(value))
        gv += delta
        # print("   ", div, delta, gv)
        set_group(a, group, gv)

    @njit(nogil=True, locals=dict(
        group=int64, j=int64, gv=uint64, oldvalue=uint64, value=uint64))
    def increment(a, i, delta=int64(1)):
        """increment the 'i'-th value of array 'a' by 'delta'"""
        group = i // group_size
        j = i % group_size
        div = uint64(n**j)
        gv = get_group(a, group)
        oldvalue = uint64(gv // div) % uint64(n)
        value = uint64(max(0, min(maximum, int64(oldvalue) + int64(delta))))
        gv += div * uint64(value - oldvalue)
        set_group(a, group, gv)

    @njit(nogil=True)
    def decrement(a, i, delta=1):
        """decrement the 'i'-th value of array 'a' by 'delta'"""
        increment(a, i, int64(-delta))

    array = iba.array
    p = PackedArray(
        size=size,
        maximum=maximum,
        group_size=group_size,
        group_bits=group_bits,
        loss=loss,
        ngroups=ngroups,
        total_bits_lost=total_bits_lost,
        array=array,
        get_group=get_group,
        set_group=set_group,
        get=get,
        set=set,
        inc=increment,
        dec=decrement,
        is_equal=is_equal,
        )
    return p
