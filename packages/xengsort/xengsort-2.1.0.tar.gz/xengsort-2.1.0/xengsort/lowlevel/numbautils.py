"""
Provide a function that returns a stringified return type
for a numba function, like 'uint64' or 'none'.

Usage:

from testutils import numba_return_type_str

# Let f be some numba function (i.e., Dispatcher object).
assert numba_return_type_str(f) == 'uint64'
"""


def numba_return_type_dict(f):
    return {sig: code.signature.return_type for sig, code in f.overloads.items()}
    # type(code.signature) == <class 'numba.core.typing.templates.Signature'>
    # type(sig) == tuple


def numba_return_type_str(f):
    s = set(numba_return_type_dict(f).values())
    rt = "|".join(sorted(map(str, s)))
    if len(rt) == 0:
        rt = 'none'
    return rt
