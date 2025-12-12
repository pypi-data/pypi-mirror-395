import itertools
import multiprocessing
import time

import h5py
import numpy
import pytest
from silx.io import h5py_utils

from ..data.hdf5 import dataset_writer


@pytest.mark.parametrize("npoints", (1, 3, 1000))
@pytest.mark.parametrize("flush_period", (None, 0.1))
@pytest.mark.parametrize("known_npoints", (True, False))
def test_dataset_writer(tmpdir, npoints, flush_period, known_npoints):
    expected = list()
    filename = str(tmpdir / "test.h5")
    if flush_period is None:
        sleep_time = None
    else:
        sleep_time = flush_period + 0.1
    isleep = npoints // 3

    kwargs = {"flush_period": flush_period}
    if known_npoints:
        kwargs["npoints"] = npoints

    with h5py.File(filename, mode="w") as f:
        with dataset_writer.DatasetWriter(f, "data", **kwargs) as writer:
            for ipoint in range(npoints):
                data = numpy.random.random((10, 20))
                writer.add_point(data)
                expected.append(data)
                if sleep_time and ipoint == isleep:
                    time.sleep(sleep_time)

    with h5py.File(filename, mode="r") as f:
        data = f["data"][()]
    numpy.testing.assert_allclose(data, expected)


@pytest.mark.parametrize("nstack", (1, 4))
@pytest.mark.parametrize("npoints", (1, 3, 1000))
@pytest.mark.parametrize("flush_period", (None, 0.1))
@pytest.mark.parametrize("known_npoints", (True, False))
@pytest.mark.parametrize("known_nstack", (True, False))
@pytest.mark.parametrize("append_stacks_in_parallel", (True, False))
def test_stack_dataset_writer(
    tmpdir,
    nstack,
    npoints,
    flush_period,
    known_npoints,
    known_nstack,
    append_stacks_in_parallel,
):
    expected = [list() for _ in range(nstack)]
    filename = str(tmpdir / "test.h5")
    if flush_period is None:
        sleep_time = None
    else:
        sleep_time = flush_period + 0.1
    isleep = (nstack * npoints) // 3

    kwargs = {"flush_period": flush_period}
    if known_npoints:
        kwargs["npoints"] = npoints
    if known_nstack:
        kwargs["nstack"] = nstack

    if append_stacks_in_parallel:
        itpoints = itertools.product(range(npoints), range(nstack))
    else:
        itpoints = itertools.product(range(nstack), range(npoints))

    with h5py.File(filename, mode="w") as f:
        with dataset_writer.StackDatasetWriter(f, "data", **kwargs) as writer:
            for tpl in itpoints:
                if append_stacks_in_parallel:
                    ipoint, istack = tpl
                else:
                    istack, ipoint = tpl
                data = numpy.random.random((10, 20))
                writer.add_point(data, istack)
                expected[istack].append(data)
                if sleep_time and (ipoint * nstack + istack) == isleep:
                    time.sleep(sleep_time)

    with h5py.File(filename, mode="r") as f:
        data = f["data"][()]
    numpy.testing.assert_allclose(data, expected)


def test_concurrent_reader(tmpdir):
    npoints = 50
    hdf5_filename = str(tmpdir / "test.h5")
    read_timestamps = str(tmpdir / "read_timestamps.log")
    write_timestamps = str(tmpdir / "write_timestamps.log")
    dataset_name = "data"

    # Run read loop in a sub-process
    start_event = multiprocessing.Event()
    reader_process = multiprocessing.Process(
        target=_read_hdf5_file,
        args=(hdf5_filename, dataset_name, npoints, read_timestamps, start_event),
    )
    reader_process.start()

    assert start_event.wait(timeout=10)

    # Run write loop
    try:
        _write_hdf5_file(hdf5_filename, dataset_name, npoints, write_timestamps)
    except Exception:
        reader_process.terminate()
        raise

    # Wait for read loop to finish
    try:
        reader_process.join(timeout=10)
        if reader_process.exitcode is None:
            raise TimeoutError("Reader process did not terminate within the timeout.")
        elif reader_process.exitcode != 0:
            raise RuntimeError(
                f"Reader process terminated with exit code {reader_process.exitcode}."
            )
    except Exception:
        reader_process.terminate()
        raise

    # Check that reading and writing happened concurrently
    with open(read_timestamps, "r") as eventfile:
        read_events = [int(line.strip()) for line in eventfile.readlines()]
    with open(write_timestamps, "r") as eventfile:
        write_events = [int(line.strip()) for line in eventfile.readlines()]

    assert len(read_events) == npoints
    assert len(write_events) == npoints

    all_events = sorted(read_events + write_events)
    assert (
        read_events != all_events[: len(read_events)]
    ), "reads and writes are not interleaved"


class _DatasetWriter(dataset_writer.DatasetWriter):
    """Testing concurrent reading and writing always ends up
    being flaky. So we introduce a sleep after flushing
    to give the reader plenty of time to fetch new data.
    """

    def _flush_hdf5(self) -> None:
        print("flush")
        super()._flush_hdf5()
        time.sleep(0.2)


def _write_hdf5_file(hdf5_filename, dataset_name, npoints, event_filename):
    data = numpy.zeros((500, 500), dtype=numpy.int64)
    with open(event_filename, "a") as eventfile:
        with h5py.File(hdf5_filename, mode="w") as h5file:
            with _DatasetWriter(h5file, dataset_name) as writer:
                for i in range(npoints):
                    writer.add_point(data)
                    eventfile.write(f"{time.perf_counter_ns()}\n")
                    print(f"write {i}")


def _read_hdf5_file(hdf5_filename, dataset_name, npoints, event_filename, start_event):
    i = 0
    with open(event_filename, "a") as eventfile:
        start_event.set()
        while i < npoints:
            for _ in _iter_data(hdf5_filename, dataset_name):
                eventfile.write(f"{time.perf_counter_ns()}\n")
                print(f"read {i}")
                i += 1


@h5py_utils.retry()
def _iter_data(hdf5_filename, dataset_name, start_index=0):
    with h5py_utils.File(hdf5_filename) as h5file:
        for _ in h5file[dataset_name][start_index:], start_index:
            yield None
