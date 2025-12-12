import pickle  # for binary files
from os import stat as osstat
from importlib import import_module

import numpy as np

from ..lowlevel import debug
from .hashio import write_array
from ..fastcash_xor import build_from_save

_ATTRS_TO_SAVE = "universe nsubfilter hashfuncs m fprbits valuebits mem_bytes".split()
_ATTR_PAIRS = [((name if '=' not in name else name.split("=")[0]), (name if '=' not in name else name.split("=")[1])) for name in _ATTRS_TO_SAVE]


def load_array_into(fname, arr, *, check=None, allow_short=False):
    # Return whether we made a check.
    # (If we make a check at it fails, it will raise RuntimeError)
    dtype, size = arr.dtype, arr.size
    fsize = osstat(fname).st_size  # file size in bytes
    assert fsize % 8 == 0
    n_uint16 = fsize // 2
    if dtype != np.uint16:
        raise RuntimeError(f"- ERROR: xorio.load_array_into: Provided array's {dtype=:_} does not match uint16")
    if (size > n_uint16) or ((not allow_short) and size != n_uint16):
        raise RuntimeError(f"- ERROR: xorio.load_array_into: Provided array's {size=:_} does not match file's {n_uint16=:_}")
    with open(fname, "rb") as fin:
        fin.readinto(arr.view(np.uint16))
    if check is not None:
        checksum = int(arr[:256].sum())
        if checksum != check:
            raise RuntimeError(f"- ERROR: xorio.load_array_into: {checksum=} does not match expected {check}")
        else:
            return True
    return False


def save_filter(outname, fltr, valueinfo, optinfo=dict(), appinfo=dict(), *, _pairs=_ATTR_PAIRS):
    """
    Save the xor filter array fltr.array in `{outname}.hash` (array only)
    and `{outname}.info` (dicts with information)
    """
    timestamp0, timestamp1, timestamp2 = debug.timestamp
    debugprint0, debugprint1, debugprint2 = debug.debugprint
    startout = timestamp0(msg="\n## Output")
    if outname.casefold() in ("/dev/null", "null", "none"):
        debugprint0(f"- not writing special null output file '{outname}'")
        return None
    debugprint0(f"- writing output files '{outname}.hash', '{outname}.info'...")
    filterinfo = {name: getattr(fltr, hname) for (name, hname) in _pairs}
    obj = (filterinfo, valueinfo, optinfo, appinfo)
    pickle.dumps(obj)  # test whether this works before writing huge hash table
    checksum = write_array(f"{outname}.hash", fltr.array)
    filterinfo['checksum'] = checksum
    with open(f"{outname}.info", "wb") as fout:
        pickle.dump(obj, fout)
    timestamp0(startout, msg="- writing output: wall time")
    return checksum


def load_filter(filename, *, shared_memory=False, info_only=False):
    debugprint0, debugprint1, debugprint2 = debug.debugprint
    timestamp0, timestamp1, timestamp2 = debug.timestamp
    if not info_only:
        startload = timestamp0(msg="\n## Loading XOR filter")
        debugprint0(f"- filter files '{filename}.info', '{filename}.hash'...")

    with open(f"{filename}.info", "rb") as finfo:
        infotup = pickle.load(finfo)
    if info_only:
        return None, None, infotup
    (filterinfo, valueinfo, optinfo, appinfo) = infotup

    debugprint1(f"- Importing value set {valueinfo}.")
    vmodule = import_module(f"..values.{valueinfo[0]}", __package__)
    values = vmodule.initialize(*(valueinfo[1:]))

    universe = filterinfo['universe']
    hashfuncs = filterinfo['hashfuncs']
    if isinstance(hashfuncs, bytes):
        filterinfo['hashfuncs'] = hashfuncs = hashfuncs.decode("ASCII")
        debugprint0("- WARNING: Converting hashfuncs from bytes to str")
    m = filterinfo['m']
    nsubfilter = filterinfo['nsubfilter']
    fprbits = filterinfo['fprbits']
    valuebits = filterinfo['valuebits']
    checksum = filterinfo['checksum']

    fltr = build_from_save(universe, hashfuncs, m, nsubfilter, fprbits, valuebits)
    checked = load_array_into(f"{filename}.hash", fltr.array, check=checksum)
    if checked:
        debugprint2(f"- Checksum {checksum} successfully verified. Nice.")

    timestamp0(startload, msg="- Time to load")
    return fltr, values, (filterinfo, valueinfo, optinfo, appinfo)
