import logging
import sys
import time
from collections import Counter
from collections.abc import Iterator
from importlib.metadata import version
from typing import Any
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional
from typing import Tuple

import numpy
from blissdata.beacon.data import BeaconData
from blissdata.redis_engine.scan import ScanState
from blissdata.redis_engine.store import DataStore
from numpy.typing import ArrayLike
from packaging.version import Version

_BLISSDATA_VERSION = Version(version("blissdata"))
if _BLISSDATA_VERSION >= Version("2.3.0"):
    from blissdata.exceptions import EndOfStream
    from blissdata.exceptions import IndexNoMoreThereError
    from blissdata.exceptions import IndexNotYetThereError
    from blissdata.exceptions import IndexWontBeThereError
    from blissdata.streams import CursorGroup
else:
    from blissdata.redis_engine.exceptions import EndOfStream
    from blissdata.redis_engine.exceptions import IndexNoMoreThereError
    from blissdata.redis_engine.exceptions import IndexNotYetThereError
    from blissdata.redis_engine.exceptions import IndexWontBeThereError
    from blissdata.streams.base import CursorGroup

logger = logging.getLogger(__name__)

INFINITY = sys.maxsize


def _get_data_store() -> None:
    redis_url = BeaconData().get_redis_data_db()
    return DataStore(redis_url)


def iter_bliss_scan_data_from_memory(
    scan_key: str,
    lima_names: Optional[List[str]] = None,
    counter_names: Optional[List[str]] = None,
    retry_timeout: Optional[float] = None,
    retry_period: Optional[float] = None,
    buffer_in_memory: bool = False,
) -> Generator[Dict[str, Any], None, None]:
    if lima_names is None:
        lima_names = list()
    if counter_names is None:
        counter_names = list()

    streams = _get_streams(scan_key, lima_names, counter_names)
    if not streams:
        return

    cursor = CursorGroup(list(streams.values()))
    cursor_timeout = retry_period or 0
    ctr_names = lima_names + counter_names
    data_buffers = {ctr_name: _DataBuffer() for ctr_name in ctr_names}
    stream_to_ctr_names = {
        stream.name: ctr_name for ctr_name, stream in streams.items()
    }

    while True:
        try:
            views = cursor.read(timeout=cursor_timeout)
        except EndOfStream:
            # No more data - stop the generator
            progress = [
                f"{ctr_name}: {data_buffer.progress}"
                for ctr_name, data_buffer in data_buffers.items()
            ]
            logger.info("Data progress on exit:\n %s", "\n".join(progress))
            for ctr_name, data_buffer in data_buffers.items():
                if data_buffer.length_left:
                    logger.warning(
                        "Data points for counter %r: %s",
                        ctr_name,
                        data_buffer.progress,
                    )
            break

        for stream, view in views.items():
            ctr_name = stream_to_ctr_names[stream.name]
            data_buffers[ctr_name].append_view(view)

        if buffer_in_memory:
            for data_buffer in data_buffers.values():
                data_buffer.buffer_in_memory()

        while True:
            try:
                ctr_values = [
                    next(data_buffer) for data_buffer in data_buffers.values()
                ]
            except StopIteration:
                # One of the buffers ran out of data
                break

            yield dict(zip(ctr_names, ctr_values))


class _DataBuffer(Iterator):
    """Data iterator with view and data buffering for a single counter."""

    def __init__(self):
        self._views = []
        self._view_lengths = []
        self._first_view_index = 0
        self._buffer = []
        self._total_length = 0
        self._total_yielded = 0

    @property
    def length_left(self) -> int:
        return self._total_length - self._total_yielded

    @property
    def progress(self) -> str:
        return f"{self._total_yielded}/{self._total_length}"

    def buffer_in_memory(self) -> None:
        """Buffer and clear all view objects."""
        if not self._views:
            return
        starts = [0] * len(self._views)
        starts[0] = self._first_view_index
        for view, start in zip(self._views, starts):
            self._buffer.extend(view.get_data(start=start, stop=None))
        self._views.clear()
        self._view_lengths.clear()
        self._first_view_index = 0

    def append_view(self, view) -> None:
        """Append view object when not empty."""
        view_length = len(view)
        if view_length:
            self._views.append(view)
            self._view_lengths.append(view_length)
            self._total_length += view_length

    def __iter__(self) -> "_DataBuffer":
        return self

    def __next__(self):
        """Return next scan data point for this counter."""
        if self._buffer:
            return self._buffer.pop(0)

        if len(self._views) == 0:
            raise StopIteration

        view = self._views[0]
        start = self._first_view_index

        self._total_yielded += 1
        self._first_view_index += 1

        if self._first_view_index == self._view_lengths[0]:
            self._views.pop(0)
            self._view_lengths.pop(0)
            self._first_view_index = 0

        data = view.get_data(start=start, stop=start + 1)
        return data[0]


def last_lima_image(scan_key: str, lima_name: str) -> ArrayLike:
    """Get last lima image from memory"""
    streams = _get_streams(scan_key, [lima_name], [])
    stream = list(streams.values())[0]
    return stream.get_last_live_image().array


def _get_streams(
    scan_key: str,
    lima_names: List[str],
    counter_names: List[str],
):
    data_store = _get_data_store()
    scan = data_store.load_scan(scan_key)

    while scan.state < ScanState.PREPARED:
        scan.update()

    streams = dict()

    for name, stream in scan.streams.items():
        if (
            stream.event_stream.encoding["type"] == "json"
            and "lima" in stream.info["format"]
        ):
            if name.split(":")[-2] in lima_names:
                streams[name.split(":")[-2]] = stream

        elif name.split(":")[-1] in counter_names:
            streams[name.split(":")[-1]] = stream

    nnames = len(lima_names) + len(counter_names)
    nstreams = len(streams)
    if nnames != nstreams:
        logger.warning("asked for %d names but got %s streams", nnames, nstreams)
        return dict()

    return streams


def iter_bliss_scan_data_from_memory_slice(
    scan_key: str,
    lima_names: List[str],
    counter_names: List[str],
    slice_range: Optional[Tuple[int, int]] = None,
    retry_timeout: Optional[float] = None,
    retry_period: Optional[float] = None,
    yield_timeout: Optional[float] = None,
    max_slicing_size: Optional[float] = None,
    verbose: Optional[bool] = False,
):
    """Iterates over the data from a Bliss scan, slicing the streams associated to a lima detector or a counter between specific indexes of the scan (optional)

    :param str scan_key: key of the Bliss scan (e.g. "esrf:scan:XXXX")
    :param list lima_names: names of lima detectors
    :param list counter_names: names of non-lima detectors (you need to provide at least one)
    :param tuple slice_range: two elements which define the limits of the iteration along the scan. If None, it iterates along the whole scan
    :param float retry_timeout: timeout when it cannot access the data for `retry_timeout` seconds
    :param float retry_period: interval in seconds between data access retries
    :param float yield_timeout: timeout to stop slicing the stream and yield the buffered data
    :param float max_slicing_size: maximum size of frames to be sliced out of the stream in one single iteration. If None, it will slice all the available data in the stream
    :yields dict: data
    """
    streams = _get_streams(scan_key, lima_names, counter_names)
    if not streams:
        return

    if slice_range is None:
        slice_range = (0, INFINITY)

    if yield_timeout is None:
        yield_timeout = 0.01

    buffers_count = Counter({counter: slice_range[0] for counter in streams.keys()})

    # Read and yield continuously
    stream_on = True

    incoming_buffers = {stream_name: [] for stream_name in streams.keys()}
    non_yielded_buffers = {stream_name: [] for stream_name in streams.keys()}

    restart_buffer = time.perf_counter()
    while stream_on:

        # While loop will stop unless one single stream is successfully sliced
        stream_on = False

        for stream_name, stream in streams.items():
            try:
                # Stop condition for limited slices
                if (
                    slice_range[1] is not INFINITY
                    and buffers_count[stream_name] >= slice_range[1]
                ):
                    continue

                # Test first index, (slicing between limits do not fall into Error)
                _ = stream[buffers_count[stream_name]]
                if max_slicing_size is None:
                    stream_data = stream[buffers_count[stream_name] : slice_range[1]]
                else:
                    stream_data = stream[
                        buffers_count[stream_name] : min(
                            slice_range[1],
                            buffers_count[stream_name] + max_slicing_size,
                        )
                    ]
                incoming_buffers[stream_name] = stream_data
                buffers_count[stream_name] += len(stream_data)
                stream_on = True

            except IndexNotYetThereError:
                stream_on = True
            except IndexWontBeThereError:
                pass
            except IndexNoMoreThereError:
                pass
            except EndOfStream:
                pass
            except RuntimeError:
                pass

            for stream_name in incoming_buffers.keys():
                if len(incoming_buffers[stream_name]) > 0:
                    if len(non_yielded_buffers[stream_name]) == 0:
                        non_yielded_buffers[stream_name] = numpy.array(
                            incoming_buffers[stream_name]
                        )
                    else:
                        non_yielded_buffers[stream_name] = numpy.concatenate(
                            (
                                non_yielded_buffers[stream_name],
                                incoming_buffers[stream_name],
                            )
                        )
                    incoming_buffers[stream_name] = []

        if not stream_on or ((time.perf_counter() - restart_buffer) > yield_timeout):

            frames_to_yield = min(
                [len(value) for value in non_yielded_buffers.values()]
            )

            if frames_to_yield > 0:
                if verbose:
                    for stream_name, stream_buffer in non_yielded_buffers.items():
                        print(
                            f"After slicing the stream: {stream_name} buffer contains {len(stream_buffer)} items"
                        )

                # Yield point by point
                for index in range(frames_to_yield):
                    yield {
                        stream_name: stream_buffer[index]
                        for stream_name, stream_buffer in non_yielded_buffers.items()
                    }

                # Save the non-yielded points for the next iteration
                for stream_name in non_yielded_buffers.keys():
                    non_yielded_buffers[stream_name] = non_yielded_buffers[stream_name][
                        frames_to_yield:
                    ]

                if verbose:
                    for stream_name, stream_buffer in non_yielded_buffers.items():
                        print(
                            f"After yielding: {stream_name} buffer contains {len(stream_buffer)} non-yielded items"
                        )

            restart_buffer = time.perf_counter()
