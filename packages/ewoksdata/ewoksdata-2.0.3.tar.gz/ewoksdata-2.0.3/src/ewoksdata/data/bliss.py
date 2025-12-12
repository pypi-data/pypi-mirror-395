"""Utilities for reading Bliss scan data from HDF5/Nexus files
or from memory (Redis or device servers).
"""

import logging
import os
import sys
import time
from numbers import Integral
from numbers import Number
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

import h5py
import hdf5plugin  # noqa: F401 - needed for transparent compression handling
import numpy
from numpy.typing import ArrayLike
from silx.io import h5py_utils
from silx.io.url import DataUrl
from silx.io.utils import get_data as silx_get_data
from silx.utils import retry as retrymod

from . import hdf5
from . import nexus
from . import url
from .blissdata import BUFFER_IN_MEMORY_DEFAULT
from .blissdata import dynamic_hdf5
from .blissdata import iter_bliss_scan_data_from_memory
from .blissdata import iter_bliss_scan_data_from_memory_slice  # noqa: F401
from .blissdata import last_lima_image  # noqa: F401
from .contextiterator import contextiterator

logger = logging.getLogger(__name__)


def get_data(
    data: Union[str, DataUrl, ArrayLike, Number],
    retry_timeout: Optional[float] = None,
    retry_period: Optional[float] = None,
    **hdf5_options: Any,
) -> Union[numpy.ndarray, Number, Sequence]:
    """
    Retrieve numerical data from a data source and return it as a NumPy array or scalar.

    This function accepts various data representations, including data URLs,
    array-like objects, and scalar numbers. The data source may not be
    immediately available so a retry mechanism is used.

    :param data: The input data source. May be:
        - A string or :class:`DataUrl` referencing a dataset (e.g., HDF5),
        - An array-like object convertible to a NumPy array,
        - A scalar numerical value.
    :param retry_timeout: Maximum time in seconds to wait for the data to become
        available. If ``None`` (default), no timeout is applied.
    :param retry_period: Interval in seconds between availability checks when
        retrying. If ``None`` (default), a period of 0.1 seconds is used.
    :param hdf5_options: Additional keyword arguments forwarded to
        :class:`silx.io.h5py_utils.File` when opening HDF5 resources.

    :returns: The resolved data. Array-like inputs are returned as NumPy arrays,
        while scalar inputs are returned as numbers.

    :raises TimeoutError: If the data does not become available within ``retry_timeout``.
    :raises ValueError: If the input type is unsupported or the data cannot be resolved.
    """
    if isinstance(data, (str, DataUrl)):
        data_url = url.as_dataurl(data)
        filename, h5path, idx = url.h5dataset_url_parse(data_url)

        _wait_for_file(filename, retry_timeout=retry_timeout, retry_period=retry_period)

        if _is_hdf5_filename(filename):
            return _get_hdf5_data(
                filename,
                h5path,
                idx=idx,
                retry_timeout=retry_timeout,
                retry_period=retry_period,
                **hdf5_options,
            )

        if not data_url.scheme():
            for scheme in ("fabio", "silx"):
                if sys.platform == "win32":
                    new_data_url = url.as_dataurl(f"{scheme}:///{data}")
                else:
                    new_data_url = url.as_dataurl(f"{scheme}://{data}")
                if new_data_url.is_valid():
                    data_url = new_data_url
                    break

        return silx_get_data(data_url)

    if isinstance(data, (Sequence, Number, numpy.ndarray)):
        return data

    raise TypeError(f"Unsupported data type: {type(data)!r}")


def _wait_for_file(
    filename: str,
    retry_timeout: Optional[float] = None,
    retry_period: Optional[float] = None,
    **_,
) -> None:
    if retry_period is None:
        retry_period = 0.1
    t0 = time.time()
    while True:
        if os.path.exists(filename):
            return
        if retry_timeout is not None:
            if (time.time() - t0) > retry_timeout:
                raise TimeoutError(
                    f"File {filename} is not created within {retry_timeout} sec"
                )
        time.sleep(retry_period)


def _is_hdf5_filename(filename: str) -> bool:
    _, ext = os.path.splitext(filename)
    return ext in (".h5", ".hdf5", ".nx", ".nxs", ".nexus")


def get_image(
    data: Union[str, DataUrl, ArrayLike, Number], **hdf5_options: Any
) -> numpy.ndarray:
    """
    Return a NumPy array or a scalar from *data*.

    Retry options, such as `retry_timeout` and `retry_period` are forwarded to the internal HDF5 data reader.

    :param data: Either a data-URL, an array-like object or a scalar number.
    :param hdf5_options: Additional options forwarded to :class:`silx.io.h5py_utils.File`.
    :return: A 2-D image.
    """
    data = get_data(data, **hdf5_options)
    return numpy.atleast_2d(numpy.squeeze(data))


@h5py_utils.retry()
def _get_hdf5_data(
    filename: str,
    h5path: str,
    idx: Optional[Tuple[int, ...]] = None,
    **hdf5_options: Any,
) -> numpy.ndarray:
    """
    Read a slice of a dataset inside an HDF5 / Nexus file.

    :param filename: Path to the HDF5 / Nexus file.
    :param h5path: Internal path to the dataset (e.g. ``/entry/data``).
    :param idx: Optional index or slice tuple used to read a subset of the dataset.
    :param **hdf5_options: Additional options forwarded to :class:`silx.io.h5py_utils.File`.
    :return: The requested slice.
    """
    with hdf5.h5context(filename, h5path, **hdf5_options) as dset:
        if _is_bliss_file(dset):
            # ``end_time`` is added by the Bliss writer when the scan is
            # finished.  If it is missing we wait for the file to be
            # completed.
            if "end_time" not in nexus.get_nxentry(dset):
                raise retrymod.RetryError("Bliss file not yet complete")
        if idx is None:
            idx = tuple()
        return dset[idx]


@contextiterator
def iter_bliss_scan_data_from_hdf5(
    filename: str,
    scan_nr: Integral,
    subscan: Optional[Integral] = None,
    lima_names: Optional[List[str]] = None,
    counter_names: Optional[List[str]] = None,
    retry_timeout: Optional[float] = None,
    retry_period: Optional[float] = None,
    **hdf5_options: Any,
) -> Iterator[Dict[str, Any]]:
    """
    Iterate over the data of a single Bliss scan stored in an HDF5 file.

    :param filename: Bliss dataset filename (HDF5 / Nexus).
    :param scan_nr: Scan number inside the file.
    :param lima_names: List of LIMA detector names.
    :param counter_names: List of non-LIMA counter names.
    :param subscan: Sub-scan number (e.g. ``10.2`` -> ``scan_nr=10`` and ``subscan=2``).
    :param retry_timeout: Timeout for the retry mechanism.
    :param retry_period: Interval between retries.
    :param **hdf5_options: Additional options forwarded to :class:`blissdata.h5api.dynamic_hdf5.File`.
    :yields: Mapping ``detector_name -> value`` for the each scan point.
    """
    if not subscan:
        subscan = 1
    lima_names = lima_names or []
    counter_names = counter_names or []

    with dynamic_hdf5.File(
        filename,
        lima_names=lima_names,
        retry_timeout=retry_timeout,
        retry_period=retry_period,
        **hdf5_options,
    ) as root:
        scan = root[f"{scan_nr}.{subscan}"]
        # assert _is_bliss_file(scan), "Not a Bliss dataset file"
        measurement = scan["measurement"]
        instrument = scan["instrument"]

        datasets: Dict[str, Any] = {name: measurement[name] for name in counter_names}
        for name in lima_names:
            datasets[name] = instrument[f"{name}/data"]

        names = list(datasets.keys())
        for values in zip(*datasets.values()):
            yield dict(zip(names, values))


@contextiterator
def iter_bliss_data(
    filename: str,
    scan_nr: Integral,
    subscan: Optional[Integral] = None,
    scan_key: Optional[str] = None,
    lima_names: Optional[List[str]] = None,
    counter_names: Optional[List[str]] = None,
    start_index: Optional[int] = None,
    retry_timeout: Optional[float] = None,
    retry_period: Optional[float] = None,
    buffer_in_memory: bool = BUFFER_IN_MEMORY_DEFAULT,
    **options: Any,
) -> Iterator[Tuple[int, Dict[str, Any]]]:
    """
    Iterate over a Bliss scan and also return the scan-point index.

    :param filename: Bliss dataset filename.
    :param scan_nr: Scan number inside the dataset.
    :param subscan: Sub-scan number (e.g. ``10.2`` -> ``scan_nr=10`` and ``subscan=2``).
    :param scan_key: Identifier of a scan for blissdata. Iterate scan data from blissdata-cache.
    :param lima_names: List of LIMA detector names.
    :param counter_names: List of non-LIMA counter names.
    :param start_index: First point to yield (default ``0`` -> all points).
    :param retry_timeout: Timeout for the retry mechanism.
    :param retry_period: Interval between retries.
    :param buffer_in_memory: Blissdata buffering in memory. Only applies when `scan_key` is provided.
                             Use only when you have enough memory or the data processing can keep up with the scan.
    :param **hdf5_options: Additional options forwarded to :class:`blissdata.h5api.dynamic_hdf5.File`.
    :yields: ``(point_index, data_dict)`` where ``point_index`` is the zero-based
             scan-point number and ``data_dict`` maps detector names to values.
    """
    start_index = 0 if start_index is None else start_index

    for idx, data in enumerate(
        iter_bliss_scan_data(
            filename,
            scan_nr,
            subscan=subscan,
            scan_key=scan_key,
            lima_names=lima_names,
            counter_names=counter_names,
            retry_timeout=retry_timeout,
            retry_period=retry_period,
            buffer_in_memory=buffer_in_memory,
            **options,
        )
    ):
        if idx >= start_index:
            yield idx, data


@contextiterator
def iter_bliss_scan_data(
    filename: str,
    scan_nr: Integral,
    subscan: Optional[Integral] = None,
    scan_key: Optional[str] = None,
    lima_names: Optional[List[str]] = None,
    counter_names: Optional[List[str]] = None,
    retry_timeout: Optional[float] = None,
    retry_period: Optional[float] = None,
    buffer_in_memory: bool = BUFFER_IN_MEMORY_DEFAULT,
    **hdf5_options: Any,
) -> Iterator[Dict[str, Any]]:
    """
    Yield the data of a Bliss scan either from an HDF5 file or from memory (Redis or device servers).

    :param filename: Path to the HDF5 / Nexus file (ignored when *scan_key* is supplied).
    :param scan_nr: Scan number inside the file.
    :param subscan: Sub-scan number (e.g. ``10.2`` -> ``scan_nr=10`` and ``subscan=2``).
    :param scan_key: Identifier of a scan for blissdata. Iterate scan data from blissdata-cache.
    :param lima_names: List of LIMA detector names.
    :param counter_names: List of non-LIMA counter names.
    :param retry_timeout: Timeout for the retry mechanism.
    :param retry_period: Interval between retries.
    :param buffer_in_memory: Blissdata buffering in memory. Only applies when `scan_key` is provided.
                             Use only when you have enough memory or the data processing can keep up with the scan.
    :param **hdf5_options: Additional options forwarded to :class:`blissdata.h5api.dynamic_hdf5.File`.
    :yields: Mapping ``detector_name -> value`` for each scan point.
    """
    if scan_key:
        yield from iter_bliss_scan_data_from_memory(
            scan_key,
            lima_names=lima_names,
            counter_names=counter_names,
            retry_timeout=retry_timeout,
            retry_period=retry_period,
            buffer_in_memory=buffer_in_memory,
        )
    else:
        yield from iter_bliss_scan_data_from_hdf5(
            filename,
            scan_nr,
            lima_names=lima_names,
            counter_names=counter_names,
            subscan=subscan,
            retry_timeout=retry_timeout,
            retry_period=retry_period,
            **hdf5_options,
        )


def _is_bliss_file(h5item: Union[h5py.Dataset, h5py.Group]) -> bool:
    """
    Return ``True`` if *h5item* belongs to a Bliss-generated file.

    :param h5item: HDF5 dataset or group.
    :return: ``True`` when the file attributes indicate a Bliss creator/publisher.
    """
    attrs = h5item.file.attrs
    creator = attrs.get("creator", "").lower()
    publisher = attrs.get("publisher", "").lower()
    return creator in _BLISS_PUBLISHERS or publisher in _BLISS_PUBLISHERS


_BLISS_PUBLISHERS = ("bliss", "blissdata")
