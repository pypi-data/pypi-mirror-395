import os
from contextlib import contextmanager
from typing import Optional

from silx.io import h5py_utils


@contextmanager
def h5context(filename: str, h5path: Optional[str] = None, **openargs):
    with h5py_utils.File(filename, **openargs) as f:
        if h5path:
            yield f[h5path]
        else:
            yield f


def h5exists(filename: str, h5path: Optional[str] = None, **openargs) -> bool:
    if not os.path.isfile(filename):
        return False
    with h5py_utils.open_item(filename, "/", **openargs) as f:
        if h5path and h5path != "/":
            return h5path in f
        return True
