import os
from os import stat as osstat
from os.path import basename
from multiprocessing import resource_tracker
from multiprocessing.shared_memory import SharedMemory

import numpy as np

from ..lowlevel import debug


def create_shared_memory(fpath, fname):
    fpath = fpath + ".hash"
    fsize = osstat(fpath).st_size
    assert fsize % 8 == 0

    with open(fpath, "rb") as hasharray:
        try:
            shm = SharedMemory(name=fname, create=True, size=fsize)
        except FileExistsError:
            return False
        shm_array = np.ndarray(fsize, dtype=np.uint8, buffer=shm.buf)
        hasharray.readinto(shm_array.view(np.uint8))

    resource_tracker.unregister(shm._name, "shared_memory")
    return True


def main(args):
    global debugprint0, debugprint1, debugprint2
    global timestamp0, timestamp1, timestamp2
    debugprint0, debugprint1, debugprint2 = debug.debugprint
    timestamp0, timestamp1, timestamp2 = debug.timestamp


    osname = os.name.lower()
    fpath = args.name
    fname = basename(fpath)
    if osname != 'posix':
        msg = f"OS name '{osname}' not supported yet."
        debugprint0(msg)
        debugprint0(f"Shared object {fname} is not loaded.")
        exit(1)
    debugprint0(f"Creating shared memory object {fname}")
    created = create_shared_memory(fpath, fname)
    if created:
        debugprint0(f"Shared memory with {fname} was created. Please use xengsort remove to delete it!")
    else:
        print(f"Index {fname} is already loaded as shared memory.")


if __name__ == '__main__':
    main()
