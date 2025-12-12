import os
from contextlib import contextmanager
from typing import Iterator
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import h5py
from silx.io import h5py_utils

from .url import DataUrl
from .url import as_dataurl


def ensure_nxclass(group: h5py.Group) -> None:
    """
    Ensure the HDF5 group has an appropriate ``NX_class`` attribute.

    The attribute is assigned based on the group's depth in the hierarchy:
      * Root group (``/``): ``NXroot``
      * First-level group: ``NXentry``
      * Deeper groups: ``NXcollection``

    :param group: The HDF5 group to update.
    :type group: h5py.Group
    """
    if group.attrs.get("NX_class"):
        return
    groups = [s for s in group.name.split("/") if s]
    n = len(groups)
    if n == 0:
        group.attrs["NX_class"] = "NXroot"
    elif n == 1:
        group.attrs["NX_class"] = "NXentry"
    else:
        group.attrs["NX_class"] = "NXcollection"


def select_default_plot(nxdata: h5py.Group) -> None:
    """
    Set the default NXdata group for visualization in the parent hierarchy.

    The function walks up the group tree and sets the ``default`` attribute
    in each parent to point to the given NXdata group.

    :param nxdata: An HDF5 group representing an NXdata node.
    :type nxdata: h5py.Group
    """
    parent = nxdata.parent
    for name in nxdata.name.split("/")[::-1]:
        if not name:
            continue
        parent.attrs["default"] = name
        parent = parent.parent


def create_url(url: str, overwrite: bool = False, **open_options) -> DataUrl:
    """
    Create (or ensure the existence of) an HDF5 group specified by a URL.

    :param url: The HDF5 URL (e.g. ``path/to/file.h5::/entry/data``).
    :param overwrite: If True, overwrite the final group if it exists.
                      If False, reuse existing groups. Default is False.
    :param open_options: Additional options passed to ``h5py.File``.
    :return: A DataUrl object pointing to the created or existing group.
    """
    url = as_dataurl(url)
    filename = url.file_path()
    data_path = url.data_path() or "/"
    dirname = os.path.dirname(filename)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    _ = open_options.setdefault("mode", "a")
    with h5py_utils.open_item(filename, "/", **open_options) as parent:
        h5item, _ = _create_h5group(parent, data_path, overwrite=overwrite)
        return as_dataurl(f"{filename}::{h5item.name}")


def get_nxentry(h5item: Union[h5py.Dataset, h5py.Group]) -> h5py.Group:
    """
    Return the top-level NXentry group containing the given HDF5 item.

    :param h5item: An HDF5 dataset or group.
    :return: The NXentry group containing ``h5item``.
    :raises ValueError: If the item does not belong to an NXentry hierarchy.
    """
    parts = [s for s in h5item.name.split("/") if s]
    if parts:
        return h5item.file[parts[0]]
    raise ValueError("HDF5 item must be part of an NXentry")


@contextmanager
def create_nexus_group(
    url: Union[str, DataUrl],
    retry_timeout=None,
    retry_period=None,
    default_levels: Optional[Sequence[str]] = None,
    **open_options,
) -> Iterator[Tuple[h5py.Group, bool]]:
    """
    Context manager to create or access an HDF5 group specified by a URL.

    The data path inside HDF5 is ensured to have at least ``default_levels`` levels.

    :param url: The HDF5 URL (e.g. ``path/to/file.h5::/entry/data``).
    :param retry_timeout: Maximum time in seconds to retry opening the file.
    :param retry_period: Time in seconds between retries.
    :param default_levels: Minimum path hierarchy touse when missing. Default is ``["/", "results"]``.
    :param open_options: Additional options passed to ``h5py.File``.
    :yields: Tuple of (HDF5 group, already_existed flag).
    """
    url = as_dataurl(url)
    filename = url.file_path()
    itemname = url.data_path() or "/"
    dirname = os.path.dirname(filename)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    open_options.setdefault("mode", "a")
    with h5py_utils.open_item(
        filename,
        "/",
        retry_timeout=retry_timeout,
        retry_period=retry_period,
        **open_options,
    ) as root:
        yield _create_h5group(root, itemname, default_levels=default_levels)


def _create_h5group(
    parent: h5py.Group,
    data_path: str,
    default_levels: Optional[Sequence[str]] = None,
    overwrite: bool = False,
) -> Tuple[h5py.Group, bool]:
    """
    Create or retrieve an HDF5 group under a given parent.

    Ensures that intermediate groups exist, optionally enforcing a minimum
    depth using ``default_levels``.

    Missing ``NX_class`` attributes are automatically created on all levels.
    The final group can be replaced if ``overwrite=True``.

    :param parent: Parent group under which the path should be created.
    :param data_path: Group path to create relative to ``parent``.
    :param default_levels: Minimum hierarchy to enforce.
                           If ``data_path`` is shorter, extra levels are added.
    :param overwrite: If True, delete and recreate the final group if it exists.
                      Default is False.
    :return: Tuple of (HDF5 group, already_existed flag).
    """
    # Ensure the data path has at least N levels as defined by ``default_levels``
    groups = [s for s in data_path.split("/") if s]
    if default_levels:
        default_levels = list(default_levels)
    else:
        default_levels = ["results"]
    if len(groups) < len(default_levels):
        groups += default_levels[len(groups) :]

    # Ensure parent groups exist + ensure NX_class
    create = False
    ensure_nxclass(parent)
    for group in groups[:-1]:
        if group in parent:
            parent = parent[group]
        else:
            parent = parent.create_group(group)
            create = True
        ensure_nxclass(parent)

    # Final group: create, overwrite or confirm existence + ensure NX_class
    group = groups[-1]
    if group in parent:
        if overwrite:
            del parent[group]
            parent = parent.create_group(group)
        else:
            parent = parent[group]
    else:
        parent = parent.create_group(group)
        create = True
    ensure_nxclass(parent)

    return parent, not create
