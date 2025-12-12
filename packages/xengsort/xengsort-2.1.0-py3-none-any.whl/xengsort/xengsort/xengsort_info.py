"""
xengsort/xengsort.py:
Collect and print information on a hash table stored on disk.
"""

from numba import njit

from ..lowlevel import debug
from ..srhash import print_statistics
from ..io.hashio import load_hash, dump_to_datafiles


def print_dict(d, title=None):
    if title is not None:
        print(f"\n### {title}")
    for key, value in d.items():
        print(f"- {key}: {value}")


def print_values(values, valuetup, title=None):
    if title is not None:
        print(f"\n### {title}")
    print(f"- value set specification: {valuetup}")
    print(f"- value set name: {values.NAME}")
    print(f"- value set nvalues: {values.NVALUES}")


def compile_filter_function(expr):
    if expr is not None:
        f = eval(f'lambda key, choice, value: ({expr})')
    else:
        f = (lambda key, choice, value: True)
    ff = njit(nogil=True)(f)
    return ff


def dump_dna_to_text(h, nvalues, infotup, prefix, packed, filterfunc):
    fname = prefix + ".dna.txt"
    raise NotImplementedError(f"DNA text dump not implemented yet. {fname=}")


def main(args):
    global debugprint0, debugprint1, debugprint2
    global timestamp0, timestamp1, timestamp2
    debugprint0, debugprint1, debugprint2 = debug.debugprint
    timestamp0, timestamp1, timestamp2 = debug.timestamp
    starttime = timestamp0(msg="\n# fastcash info")

    h, values, infotup = load_hash(args.hashname)
    (hashinfo, valueinfo, optinfo, appinfo) = infotup
    print_dict(hashinfo, "Hash table properties")
    print_dict(optinfo)
    print_dict(appinfo)
    print_values(values, valueinfo, "Value set properties")
    SV = {'all': values.NVALUES, 'none': False}
    sv = args.showvalues
    sv = SV[sv] if sv in SV else int(sv)
    print("!!!", sv)
    print_statistics(h, level=args.statistics, show_values=sv)

    # dump data if requested
    fmt = args.format  # native, packed, text/txt, dna
    anyformat = (fmt is not None)
    prefix = args.outprefix
    nvalues = values.NVALUES
    filterfunc = compile_filter_function(args.filter)
    if (prefix is None) and anyformat:
        prefix = args.hashname
    if prefix is not None:
        startout = timestamp0(msg="\n## Data Output")
        if fmt == "dna":
            written = dump_dna_to_text(h, nvalues, infotup, prefix, filterfunc)
        else:
            if fmt is None:
                fmt = "native"
            elif fmt == "txt":
                fmt = "text"
            written = dump_to_datafiles(h, nvalues, infotup, prefix, fmt, filterfunc)
        debugprint0(f"- wrote {written} items")
        timestamp0(startout, msg="- done writing data; writing time")

    # that's it; successfully exit the program
    timestamp0(starttime, msg="- DONE; total time")
