import logging
from numbers import Number
from typing import Any
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional

from blissdata.data.events.lima import ImageNotSaved
from blissdata.data.node import get_node
from numpy.typing import ArrayLike
from silx.utils import retry as retrymod

logger = logging.getLogger(__name__)


def iter_bliss_scan_data_from_memory(
    db_name: str,
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

    scan_node = _get_node(
        db_name, "scan", retry_timeout=retry_timeout, retry_period=retry_period
    )
    indices = {name: 0 for name in lima_names + counter_names}
    buffers = {name: list() for name in lima_names + counter_names}
    if not buffers:
        return

    lima_acq_nb = dict()
    for event_type, node, event_data in scan_node.walk_events():
        if node.type == "lima":
            name = node.db_name.split(":")[-2]
            if name not in lima_names:
                continue
            dataview = _get_lima_dataview(
                node,
                indices[name],
                retry_timeout=retry_timeout,
                retry_period=retry_period,
            )
            current_lima_acq_nb = dataview.status_event.status["lima_acq_nb"]
            first_lima_acq_nb = lima_acq_nb.setdefault(name, current_lima_acq_nb)
            if first_lima_acq_nb != current_lima_acq_nb:
                logger.warning("lima is already acquiring the next scan")
                continue
            try:
                data = list(dataview)
            except ImageNotSaved:
                logger.warning(
                    "cannot read lima data from file because images are not being saved"
                )
                continue
            except Exception as e:
                logger.warning("cannot read lima data (%s)", str(e))
                continue
            indices[name] += len(data)
            buffers[name].extend(data)
        elif node.type == "channel":
            name = node.db_name.split(":")[-1]
            if name not in counter_names:
                continue
            if event_data:
                data = event_data.data
            else:
                data = node.get_as_array(indices[name], -1)
            indices[name] += len(data)
            buffers[name].extend(data)
        nyield = min(len(v) for v in buffers.values())
        if nyield:
            for i in range(nyield):
                yield {name: values[i] for name, values in buffers.items()}
            buffers = {name: values[nyield:] for name, values in buffers.items()}
        if event_type == event_type.END_SCAN:
            break


def last_lima_image(db_name: str) -> ArrayLike:
    """Get last lima image from memory"""
    node = _get_node(db_name, "lima")
    node.from_stream = True
    dataview = node.get(-1)
    try:
        image = dataview.get_last_live_image()
    except AttributeError:
        image = None
    if image is None or image.data is None:
        raise RuntimeError("Cannot get last image from lima")
    return image.data


@retrymod.retry()
def _get_node(db_name: str, node_type: str):
    node = get_node(db_name)
    if node is None:
        raise retrymod.RetryError(f"Redis node {db_name} does not exist")
    if node.type != node_type:
        raise RuntimeError(f"Not a Redis {node_type} node")
    return node


@retrymod.retry()
def _get_lima_dataview(node, start_index: int):
    dataview = node.get(start_index, -1)
    try:
        if dataview.status_event.proxy is None:
            raise retrymod.RetryError("Lima proxy not known (yet)")
    except Exception:
        raise retrymod.RetryError("Lima proxy not known (yet)")
    return dataview
