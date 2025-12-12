import logging
import sys
import time
from collections import Counter
from numbers import Number
from typing import Any
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional
from typing import Tuple

import numpy
from blissdata.beacon.data import BeaconData
from blissdata.lima.client import lima_client_factory
from blissdata.redis_engine.exceptions import EndOfStream
from blissdata.redis_engine.exceptions import IndexNoMoreThereError
from blissdata.redis_engine.exceptions import IndexNotYetThereError
from blissdata.redis_engine.exceptions import IndexWontBeThereError
from blissdata.redis_engine.scan import Scan
from blissdata.redis_engine.scan import ScanState
from blissdata.redis_engine.store import DataStore
from blissdata.redis_engine.stream import StreamingClient
from numpy.typing import ArrayLike

try:
    from blissdata.stream import LimaStream
except ImportError:
    from blissdata.streams.lima_stream import LimaStream


logger = logging.getLogger(__name__)

INFINITY = sys.maxsize


def _get_data_store() -> None:
    redis_url = BeaconData().get_redis_data_db()
    return DataStore(redis_url)


def iter_bliss_scan_data_from_memory(
    scan_key: str,
    lima_names: Optional[List[str]] = None,
    counter_names: Optional[List[str]] = None,
    retry_timeout: Optional[Number] = None,
    retry_period: Optional[Number] = None,
    buffer_in_memory: bool = True,
) -> Generator[Dict[str, Any], None, None]:
    if not buffer_in_memory:
        raise NotImplementedError("Requires blissdata>=2.0.0rc1")
    if lima_names is None:
        lima_names = list()
    if counter_names is None:
        counter_names = list()

    data_store = _get_data_store()
    scan = data_store.load_scan(scan_key, scan_cls=Scan)
    buffers = {name: list() for name in lima_names + counter_names}
    if not buffers:
        return

    while scan.state < ScanState.PREPARED:
        scan.update()

    lima_streams = dict()
    lima_clients = dict()
    counter_streams = dict()
    for name, stream in scan.streams.items():
        if stream.encoding["type"] == "json" and "lima" in stream.info["format"]:
            if name.split(":")[-2] in lima_names:
                lima_streams[name] = stream
                lima_clients[name] = lima_client_factory(data_store, stream.info)
        elif name.split(":")[-1] in counter_names:
            counter_streams[name] = stream

    client = StreamingClient({**lima_streams, **counter_streams})
    client_timeout = retry_period or 0
    lima_buffer_count = Counter()

    while True:
        try:
            output = client.read(timeout=client_timeout)
        except EndOfStream:
            break
        for stream, (_, payload) in output.items():
            name_parts = stream.name.split(":")
            if stream.name in lima_streams:
                # payload is a sequence of JSON statuses
                ctr_name = name_parts[-2]
                last_status = payload[-1]
                lima_client = lima_clients[stream.name]
                lima_client.update(**last_status)
                n_already_read = lima_buffer_count[ctr_name]
                try:
                    data = lima_client[n_already_read:]
                except IndexNoMoreThereError:
                    continue
                buffers[ctr_name].extend(data)
                lima_buffer_count[ctr_name] += len(data)
            else:
                # payload is a sequence of data points (0D, 1D, 2D)
                ctr_name = name_parts[-1]
                buffers[ctr_name].extend(payload)

        nyield = min(len(v) for v in buffers.values())
        if nyield:
            for i in range(nyield):
                yield {name: values[i] for name, values in buffers.items()}
            buffers = {name: values[nyield:] for name, values in buffers.items()}


def last_lima_image(channel_info: dict) -> ArrayLike:
    """Get last lima image from memory"""
    data_store = _get_data_store()
    lima_client = lima_client_factory(data_store, channel_info)
    return lima_client.get_last_live_image().array


def _get_streams(
    scan_key: str,
    lima_names: List[str],
    counter_names: List[str],
):
    data_store = _get_data_store()
    scan = data_store.load_scan(scan_key, scan_cls=Scan)

    while scan.state < ScanState.PREPARED:
        scan.update()

    lima_streams = dict()
    counter_streams = dict()

    for name, stream in scan.streams.items():
        if stream.encoding["type"] == "json" and "lima" in stream.info["format"]:
            if name.split(":")[-2] in lima_names:
                lima_streams[name.split(":")[-2]] = LimaStream(stream)

        elif name.split(":")[-1] in counter_names:
            counter_streams[name.split(":")[-1]] = stream

    return lima_streams, counter_streams


def iter_bliss_scan_data_from_memory_slice(
    scan_key: str,
    lima_names: List[str],
    counter_names: List[str],
    slice_range: Optional[Tuple[int, int]] = None,
    retry_timeout: Optional[Number] = None,
    retry_period: Optional[Number] = None,
    yield_timeout: Optional[Number] = None,
    max_slicing_size: Optional[Number] = None,
    verbose: Optional[bool] = False,
):
    """Iterates over the data from a Bliss scan, slicing the streams associated to a lima detector or a counter between specific indexes of the scan (optional)

    :param str scan_key: key of the Bliss scan (e.g. "esrf:scan:XXXX")
    :param list lima_names: names of lima detectors
    :param list counter_names: names of non-lima detectors (you need to provide at least one)
    :param tuple slice_range: two elements which define the limits of the iteration along the scan. If None, it iterates along the whole scan
    :param Number retry_timeout: timeout when it cannot access the data for `retry_timeout` seconds
    :param Number retry_period: interval in seconds between data access retries
    :param Number yield_timeout: timeout to stop slicing the stream and yield the buffered data
    :param Number max_slicing_size: maximum size of frames to be sliced out of the stream in one single iteration. If None, it will slice all the available data in the stream
    :yields dict: data
    """
    lima_streams, counter_streams = _get_streams(scan_key, lima_names, counter_names)

    all_streams = {**lima_streams, **counter_streams}
    if not all_streams:
        logger.warning("There is no stream to slice")
        return

    if slice_range is None:
        slice_range = (0, INFINITY)

    if retry_period is None:
        retry_period = 1

    if yield_timeout is None:
        yield_timeout = 0.01

    buffers_count = Counter({counter: slice_range[0] for counter in all_streams.keys()})

    # Read and yield continuously
    stream_on = True

    incoming_buffers = {stream_name: [] for stream_name in all_streams.keys()}
    non_yielded_buffers = {stream_name: [] for stream_name in all_streams.keys()}

    restart_buffer = time.perf_counter()
    while stream_on:

        # While loop will stop unless one single stream is successfully sliced
        stream_on = False

        for stream_name, stream in all_streams.items():
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
