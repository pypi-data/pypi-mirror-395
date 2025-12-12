import time
from typing import List
from typing import Optional

import h5py
import numpy
from numpy.typing import ArrayLike

from .config import guess_dataset_config
from .types import StrictPositiveIntegral


class _DatasetWriterBase:
    def __init__(
        self,
        parent: h5py.Group,
        name: str,
        attrs: Optional[dict] = None,
        flush_period: Optional[float] = None,
    ) -> None:
        self._file = parent.file
        self._parent = parent
        self._name = name
        self._attrs = attrs
        self._dataset_name = f"{parent.name}/{name}"
        self._dataset = None
        self._flush_period = flush_period
        self._last_flush = None

    @property
    def dataset_name(self) -> str:
        return self._dataset_name

    def __enter__(self) -> "_DatasetWriterBase":
        return self

    def __exit__(self, *args) -> None:
        self.flush_buffer()

    @property
    def dataset(self) -> Optional[h5py.Dataset]:
        return self._dataset

    def _create_dataset(self, first_data_point: numpy.ndarray) -> h5py.Dataset:
        raise NotImplementedError

    def flush_buffer(self, align: bool = False) -> bool:
        raise NotImplementedError

    def _flush_time_expired(self) -> bool:
        if self._flush_period is None:
            return False
        if self._last_flush is None:
            self._last_flush = time.time()
            return False
        return (time.time() - self._last_flush) >= self._flush_period

    def _flush_hdf5(self) -> None:
        """Explicit HDF5 flush for non-locking readers."""
        self._file.flush()


class DatasetWriter(_DatasetWriterBase):
    """Append arrays of the same shape to a new HDF5 dataset in a sequential manner.

    Instead of creating a dataset with the :code:`h5py` API

    .. code-block::python

        h5group["mydataset"] = [[1,2,3], [4,5,6], [7,8,9]]

    it can be done like this

    .. code-block::python

        with DatasetWriter(h5group, "mydataset") as writer:
            writer.add_point([1,2,3])
            writer.add_points([[4,5,6], [7,8,9]])

    Chunk size determination, chunk-aligned writing, compression and flushing is handled.
    """

    def __init__(
        self,
        parent: h5py.Group,
        name: str,
        npoints: Optional[StrictPositiveIntegral] = None,
        attrs: Optional[dict] = None,
        flush_period: Optional[float] = None,
        overwrite: bool = False,
    ) -> None:
        super().__init__(parent, name, attrs=attrs, flush_period=flush_period)
        self._npoints = npoints
        self._overwrite = overwrite
        self._chunked: bool = False
        self._npoints_added: int = 0

        self._buffer: List[ArrayLike] = list()
        self._chunk_size: int = 0
        self._flushed_size: int = 0

    def _create_dataset(self, first_data_point: numpy.ndarray) -> h5py.Dataset:
        scan_shape = (self._npoints,)
        detector_shape = first_data_point.shape
        dtype = first_data_point.dtype
        if self._npoints is None:
            max_shape = scan_shape + detector_shape
            shape = (1,) + first_data_point.shape
        else:
            max_shape = None
            shape = scan_shape + first_data_point.shape

        options = guess_dataset_config(
            scan_shape, detector_shape, dtype=dtype, max_shape=max_shape
        )
        options["shape"] = shape
        options["dtype"] = dtype
        options["fillvalue"] = numpy.nan  # converts to 0 for integers
        if max_shape:
            options["maxshape"] = max_shape
        if options["chunks"]:
            self._chunked = True
            self._chunk_size = options["chunks"][0]
        if self._overwrite and self._name in self._parent:
            del self._parent[self._name]
        dset = self._parent.create_dataset(self._name, **options)
        if self._attrs:
            dset.attrs.update(self._attrs)
        return dset

    @property
    def npoints_added(self) -> int:
        return self._npoints_added

    def add_point(self, data: ArrayLike) -> bool:
        """Append one array to the dataset."""
        if self._dataset is None:
            self._dataset = self._create_dataset(data)
        self._buffer.append(data)
        self._npoints_added += 1
        return self.flush_buffer(align=True)

    def add_points(self, data: ArrayLike) -> bool:
        """Append several arrays at once to the dataset."""
        if self._dataset is None:
            self._dataset = self._create_dataset(data[0])
        self._buffer.extend(data)
        self._npoints_added += len(data)
        return self.flush_buffer(align=True)

    def flush_buffer(self, align: bool = False) -> bool:
        # Determine how many points to flush
        chunk_size = len(self._buffer)

        if self._flush_time_expired():
            flush_size = chunk_size
        elif align and self._chunked:
            n = chunk_size + (self._flushed_size % self._chunk_size)
            flush_size = n // self._chunk_size * self._chunk_size
            flush_size = min(flush_size, chunk_size)
        else:
            flush_size = chunk_size

        if flush_size == 0:
            return False

        # Enlarge the dataset when needed
        nalloc = self._dataset.shape[0]
        istart = self._flushed_size
        flushed_size = istart + flush_size
        if self._chunked and flushed_size > nalloc:
            self._dataset.resize(flushed_size, axis=0)

        # Copy data from buffer to HDF5
        self._dataset[istart : istart + flush_size] = self._buffer[:flush_size]

        # Remove copied data from buffer
        self._buffer = self._buffer[flush_size:]
        self._flushed_size = flushed_size

        self._flush_hdf5()
        self._last_flush = time.time()
        return True


class StackDatasetWriter(_DatasetWriterBase):
    """Append arrays of the same shape to each item of a new HDF5 dataset
    in a sequential manner per item. So each item of the HDF5 dataset is a
    stack to which we can append data in a sequential manner.

    Instead of creating a dataset with the :code:`h5py` API

    .. code-block::python

        stack0 = [[1,2,3], [4,5,6], [7,8,9]]
        stack1 = [[10,11,12], [13,14,15], [16,17,18]]
        h5group["mydataset"] = [stack0, stack1]

    it can be done like this

    .. code-block::python

        with StackDatasetWriter(h5group, "mydataset") as writer:
            writer.add_point([1,2,3], 0)
            writer.add_point([10,11,12], 1)
            writer.add_points([[13,14,15], [16,17,18]], 1)
            writer.add_points([[4,5,6], [7,8,9]], 0)

    Chunk size determination, chunk-aligned writing, compression and flushing is handled.
    """

    def __init__(
        self,
        parent: h5py.Group,
        name: str,
        npoints: Optional[StrictPositiveIntegral] = None,
        nstack: Optional[StrictPositiveIntegral] = None,
        attrs: Optional[dict] = None,
        flush_period: Optional[float] = None,
    ) -> None:
        super().__init__(parent, name, attrs=attrs, flush_period=flush_period)
        self._npoints = npoints
        self._chunked: bool = False
        self._nstack = nstack

        self._buffers: List[List[ArrayLike]] = list()
        self._chunk_size: ArrayLike = numpy.zeros(2, dtype=int)
        self._flushed_size_dim1: ArrayLike = numpy.array(list(), dtype=int)

    def _create_dataset(
        self, first_data_point: numpy.ndarray, stack_index: int
    ) -> h5py.Dataset:
        scan_shape = (self._nstack, self._npoints)
        detector_shape = first_data_point.shape
        dtype = first_data_point.dtype
        if self._npoints is None or self._nstack is None:
            max_shape = scan_shape + detector_shape
            shape = (stack_index + 1, 1) + first_data_point.shape
        else:
            max_shape = None
            shape = scan_shape + first_data_point.shape

        options = guess_dataset_config(
            scan_shape, detector_shape, dtype=dtype, max_shape=max_shape
        )
        options["shape"] = shape
        options["dtype"] = dtype
        options["fillvalue"] = numpy.nan  # converts to 0 for integers
        if max_shape:
            options["maxshape"] = max_shape
        if options["chunks"]:
            self._chunked = True
            self._chunk_size = numpy.array(options["chunks"][:2], dtype=int)
        dset = self._parent.create_dataset(self._name, **options)
        if self._attrs:
            dset.attrs.update(self._attrs)
        return dset

    def _get_buffer(self, stack_index: int) -> List[ArrayLike]:
        # Add stack buffers when needed
        for _ in range(max(stack_index - len(self._buffers) + 1, 0)):
            self._buffers.append(list())
            self._flushed_size_dim1 = numpy.append(self._flushed_size_dim1, 0)
        return self._buffers[stack_index]

    def add_point(self, data: ArrayLike, stack_index: int) -> bool:
        """Append one array to one stack of the dataset."""
        if self._dataset is None:
            self._dataset = self._create_dataset(data, stack_index)
        buffer = self._get_buffer(stack_index)
        buffer.append(data)
        return self.flush_buffer(align=True)

    def add_points(self, data: ArrayLike, stack_index: int) -> bool:
        """Append several arrays at once to one stack of the dataset."""
        if self._dataset is None:
            self._dataset = self._create_dataset(data[0], stack_index)
        buffer = self._get_buffer(stack_index)
        buffer.extend(data)
        return self.flush_buffer(align=True)

    def flush_buffer(self, align: bool = False) -> bool:
        # Determine how many points to flush for each buffer in the stack
        chunk_sizes = numpy.array([len(buffer) for buffer in self._buffers])
        flushed_size_dim1 = self._flushed_size_dim1
        size_dim0 = len(chunk_sizes)
        assert size_dim0 == len(
            flushed_size_dim1
        ), "Number of buffers and number of flushed dim1 points must be the same"

        chunk_size_dim0, chunk_size_dim1 = self._chunk_size[:2]
        if chunk_size_dim0 == 0:
            chunk_size_dim0 = size_dim0

        if self._flush_time_expired():
            flush_sizes = chunk_sizes
        elif align and self._chunked:
            size_dim0 = size_dim0 // chunk_size_dim0 * chunk_size_dim0
            chunk_sizes = chunk_sizes[:size_dim0]
            flushed_size_dim1 = flushed_size_dim1[:size_dim0]
            if size_dim0:
                n1 = chunk_sizes + (flushed_size_dim1 % chunk_size_dim1)
                flush_sizes = n1 // chunk_size_dim1 * chunk_size_dim1
                flush_sizes = numpy.minimum(flush_sizes, chunk_sizes)
                for i0_chunk0 in range(0, size_dim0, chunk_size_dim0):
                    flush_sizes[i0_chunk0 : i0_chunk0 + chunk_size_dim0] = min(
                        flush_sizes[i0_chunk0 : i0_chunk0 + chunk_size_dim0]
                    )
            else:
                flush_sizes = list()
        else:
            flush_sizes = chunk_sizes

        if not any(flush_sizes):
            return False

        # Enlarge the dataset when needed
        nalloc = self._dataset.shape[:2]
        istart_dim1 = flushed_size_dim1
        flushed_size_dim1 = istart_dim1 + flush_sizes
        nalloc_new = numpy.array([size_dim0, max(flushed_size_dim1)])
        if self._chunked and any(nalloc_new > nalloc):
            for axis, n in enumerate(nalloc_new):
                self._dataset.resize(n, axis=axis)

        # Copy data from buffer to HDF5
        for i0_chunk0 in range(0, size_dim0, chunk_size_dim0):
            idx_dim0 = slice(i0_chunk0, i0_chunk0 + chunk_size_dim0)
            buffers = self._buffers[idx_dim0]

            flush_sizes_dim1 = flush_sizes[idx_dim0]
            non_ragged_buffers = len(set(flush_sizes_dim1)) == 1

            istart0_dim1 = istart_dim1[idx_dim0]
            non_ragged_destination = len(set(istart0_dim1)) == 1

            if non_ragged_destination and non_ragged_buffers:
                data = [buffer[: flush_sizes_dim1[0]] for buffer in buffers]
                idx_dim1 = slice(istart0_dim1[0], istart0_dim1[0] + flush_sizes_dim1[0])
                self._dataset[idx_dim0, idx_dim1] = data
            else:
                for buffer, i_dim0, istart_dim1, i_flush_size_dim1 in zip(
                    buffers,
                    range(i0_chunk0, i0_chunk0 + chunk_size_dim0),
                    istart0_dim1,
                    flush_sizes_dim1,
                ):
                    self._dataset[
                        i_dim0, istart_dim1 : istart_dim1 + i_flush_size_dim1, ...
                    ] = buffer[:i_flush_size_dim1]

        # Remove copied data from buffer
        for i0 in range(size_dim0):
            self._buffers[i0] = self._buffers[i0][flush_sizes[i0] :]
            self._flushed_size_dim1[i0] = flushed_size_dim1[i0]

        self._flush_hdf5()
        self._last_flush = time.time()
        return True
