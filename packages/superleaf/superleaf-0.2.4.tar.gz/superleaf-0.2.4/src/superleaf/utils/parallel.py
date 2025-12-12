import argparse
import math
import os
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count, Manager, current_process, shared_memory
from multiprocessing.managers import SharedMemoryManager
from threading import Thread, Event
from typing import Optional, Self

from multiprocess import Pool
import numpy as np
import pandas as pd
import pyarrow as pa
from pyarrow import ipc
from tqdm import tqdm

from .hashing import get_hash_string


def _chunkify(lst, n_chunks, enumerated=True):
    """Split list lst into n_chunks roughly equal chunks."""
    chunk_size = math.ceil(len(lst) / n_chunks)
    if enumerated:
        lst = list(enumerate(lst))
    return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]


def _progress_updater(counter, total, pbar, stop_event, poll_interval=0.1):
    """Periodically poll the shared counter and update tqdm progress bar."""
    last = 0
    while last < total and not stop_event.is_set():
        current = counter.value
        if current > last:
            pbar.update(current - last)
            last = current
        time.sleep(poll_interval)


def _run_thread_pool(func, iterable, star=False, update_func=None, n_workers=4):
    """Run tasks in a ThreadPoolExecutor with optional update callback."""
    results = []
    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        if star:
            futures = [executor.submit(func, *item) for item in iterable]
        else:
            futures = [executor.submit(func, item) for item in iterable]
        try:
            for fut in as_completed(futures):
                results.append(fut.result())
                if update_func is not None:
                    update_func()  # call the update function per task
        except KeyboardInterrupt:
            # Cancel pending tasks and shutdown executor
            for fut in futures:
                fut.cancel()
            executor.shutdown(wait=False)
            raise
    return results


def _process_worker(func, enumerated_items, star, counter, lock, nthreads_per_process, verbose=False):
    """Worker function that creates its own thread pool for a chunk of items.
       Each completed task increments the shared counter.
    """
    def thread_func(idx_item):
        idx, item = idx_item
        if star:
            result = func(*item)
        else:
            result = func(item)
        with lock:
            counter.value += 1
        return idx, result

    if verbose:
        print(f"Starting {current_process()} process worker with {nthreads_per_process} threads.")
    with ThreadPoolExecutor(max_workers=nthreads_per_process) as thread_executor:
        return list(thread_executor.map(thread_func, enumerated_items))


def parmap(func, iterable, star=False, mode="process", n_workers=None, nthreads_per_process=None, pbar_desc=None,
           verbose=False):
    """
    Apply ``func`` to every item in ``iterable``.

    mode:
      - "thread": use ThreadPoolExecutor with n_workers.
      - "process": use ProcessPoolExecutor; each process runs a ThreadPoolExecutor of size nthreads_per_process.

    A tqdm progress bar shows overall progress.
    """
    if n_workers is None or n_workers == 0:
        n_workers = 1
    elif n_workers < 0:
        n_workers = cpu_count() + 1 + n_workers

    if nthreads_per_process is None or nthreads_per_process == 0:
        nthreads_per_process = 1

    if nthreads_per_process > 1 and mode == "thread":
        raise ValueError("nthreads_per_process > 1 is not supported in thread mode.")

    if n_workers > 1 and mode == "process" and 'get_ipython' in globals():
        # In Jupyter Notebook, use a different method to avoid issues with multiprocessing.
        mode = "notebook"
        if verbose:
            print("Switching to 'notebook' mode for parallel processing.")

    if verbose:
        print(f"Using {n_workers} workers and {nthreads_per_process} threads per process.")

    if not hasattr(iterable, '__len__'):
        iterable = list(iterable)
    total = len(iterable)
    if total == 0:
        return []
    results = []

    if mode == "thread":
        with tqdm(total=total, desc=pbar_desc) as pbar:
            def update():
                pbar.update(1)
            try:
                results = _run_thread_pool(func, iterable, star=star, update_func=update, n_workers=n_workers)
            except KeyboardInterrupt:
                print("KeyboardInterrupt detected in thread mode; exiting gracefully.")
                raise

    elif mode == "process":
        manager = Manager()
        counter = manager.Value('i', 0)
        lock = manager.Lock()
        chunks = _chunkify(iterable, n_workers)
        stop_event = Event()

        with tqdm(total=total, desc=pbar_desc) as pbar:
            updater = Thread(target=_progress_updater, args=(counter, total, pbar, stop_event))
            updater.daemon = True  # Ensure it doesn't block process exit.
            updater.start()

            try:
                with ProcessPoolExecutor(max_workers=n_workers) as proc_executor:
                    futures = [
                        proc_executor.submit(
                            _process_worker, func, chunk, star, counter, lock, nthreads_per_process, verbose)
                        for chunk in chunks
                    ]
                    for future in as_completed(futures):
                        results.extend(future.result())
                # Results may not be in the original order, sort them using the indices with which they were returned
                results.sort(key=lambda x: x[0])  # Sort by the original index
                _, results = zip(*results)  # Unzip the results to get the values only
            except KeyboardInterrupt:
                print("KeyboardInterrupt detected in process mode; cancelling tasks...")
                stop_event.set()  # Signal the updater thread to stop.
                # Attempt to cancel pending futures.
                for future in futures:
                    future.cancel()
                # Shutdown the executor without waiting.
                proc_executor.shutdown(wait=False)
                raise
            finally:
                stop_event.set()  # Ensure the updater thread exits.
                updater.join(timeout=1)  # Wait briefly for it to finish.
    elif mode == "notebook":
        with Pool(n_workers) as p:
            results = p.map(func, iterable, chunksize=32)
        if verbose:
            print('done.')
    else:
        raise ValueError("mode must be either 'thread' or 'process'")

    return results


class SharedMemoryContainer(ABC):
    """Abstract base class for shared memory containers."""

    @classmethod
    @abstractmethod
    def create(cls, *args, **kwargs) -> Self:
        pass

    @abstractmethod
    def load(self):
        """Load the data from shared memory."""
        pass

    @abstractmethod
    def close(self) -> Self:
        """Close the shared memory."""
        pass

    @abstractmethod
    def unlink(self) -> Self:
        """Unlink the shared memory."""
        pass

    @property
    @abstractmethod
    def metadata(self) -> dict:
        pass

    @classmethod
    @abstractmethod
    def from_metadata(cls, metadata: dict) -> Self:
        pass


class SharedMemoryArray(SharedMemoryContainer):
    def __init__(self, shared_mem: shared_memory.SharedMemory, shape: tuple, dtype):
        self.shared_mem = shared_mem
        self.shape = tuple(shape)
        self.dtype = np.dtype(dtype)

    @classmethod
    def create(cls, array: np.ndarray, smm: Optional[SharedMemoryManager] = None) -> Self:
        if smm:
            shared_mem = smm.SharedMemory(size=array.nbytes)
        else:
            shared_mem = shared_memory.SharedMemory(create=True, size=array.nbytes)
        shared_array = np.ndarray(array.shape, dtype=array.dtype, buffer=shared_mem.buf)
        np.copyto(shared_array, array)
        return cls(shared_mem, array.shape, array.dtype)

    @classmethod
    def create_empty(cls, shape: tuple, dtype, smm: Optional[SharedMemoryManager] = None) -> Self:
        size = np.prod(shape) * np.dtype(dtype).itemsize
        if smm:
            shared_mem = smm.SharedMemory(size=size)
        else:
            shared_mem = shared_memory.SharedMemory(size=size)
        return cls(shared_mem, shape, dtype)

    def load(self) -> np.ndarray:
        return np.ndarray(self.shape, dtype=self.dtype, buffer=self.shared_mem.buf)

    def close(self) -> Self:
        self.shared_mem.close()
        return self

    def unlink(self) -> Self:
        self.shared_mem.unlink()
        return self

    @property
    def metadata(self) -> dict:
        return {'name': self.shared_mem.name, 'shape': self.shape, 'dtype': str(self.dtype)}

    @classmethod
    def from_metadata(cls, metadata: dict) -> Self:
        shared_mem = shared_memory.SharedMemory(name=metadata['name'])
        return cls(shared_mem, metadata['shape'], metadata['dtype'])


class SharedMemoryList(SharedMemoryContainer):
    def __init__(self, shared_mem: shared_memory.ShareableList):
        self.shared_mem = shared_mem

    @classmethod
    def create(cls, array: list, smm: Optional[SharedMemoryManager] = None) -> Self:
        if smm:
            shared_mem = smm.ShareableList(array)
        else:
            shared_mem = shared_memory.ShareableList(array)
        return cls(shared_mem)

    def load(self) -> list:
        return list(self.shared_mem)

    def close(self) -> Self:
        self.shared_mem.shm.close()
        return self

    def unlink(self) -> Self:
        self.shared_mem.shm.unlink()
        return self

    @property
    def metadata(self) -> dict:
        return {'name': self.shared_mem.shm.name}

    @classmethod
    def from_metadata(cls, metadata: dict) -> Self:
        shared_mem = shared_memory.ShareableList(name=metadata['name'])
        return cls(shared_mem)


class PyArrowData(SharedMemoryContainer):
    """Abstract base class for PyArrow data containers."""
    def __init__(self, path: str):
        self.path = path

    @staticmethod
    def _check_path(path: Optional[str] = None, dir: Optional[str] = None, overwrite=False):
        if path is None:
            path = get_hash_string(time.time_ns(), length=8) + ".arrow"
        elif not os.path.splitext(path)[1]:
            path += ".arrow"

        if dir is not None:
            path = os.path.join(dir, path)

        if os.path.exists(path):
            if not overwrite:
                raise FileExistsError(f"File {path} already exists. Use overwrite=True to overwrite.")
            else:
                print(f"Overwriting existing file at {path}")
        else:
            print(f"Creating pyarrow file at {path}")
        path_dir = os.path.dirname(path)
        if path_dir:
            os.makedirs(path_dir, exist_ok=True)
        return path

    @classmethod
    @abstractmethod
    def create(cls, data, path: Optional[str] = None, dir: Optional[str] = None, overwrite: bool = False) -> Self:
        pass

    @abstractmethod
    def load(self):
        """Load the data from the file."""
        pass

    def close(self) -> Self:
        return self

    def unlink(self) -> Self:
        return self

    @property
    def metadata(self) -> dict:
        return {'path': self.path}

    @classmethod
    def from_metadata(cls, metadata: dict) -> Self:
        path = metadata['path']
        if not os.path.exists(path):
            raise FileNotFoundError(f"File {path} does not exist.")
        return cls(path)


class PyArrowDataFrame(PyArrowData):
    @classmethod
    def create(
            cls, df: pd.DataFrame, path: Optional[str] = None, dir: Optional[str] = None, overwrite: bool = False
    ) -> Self:
        path = cls._check_path(path, dir, overwrite)
        table = pa.Table.from_pandas(df)
        with pa.OSFile(path, 'wb') as sink:
            with ipc.new_file(sink, table.schema) as writer:
                writer.write_table(table)
        return cls(path)

    def load(self) -> pd.DataFrame:
        with pa.memory_map(self.path, 'rb') as source:
            return ipc.RecordBatchFileReader(source).read_pandas()


class PyArrowArray(PyArrowDataFrame):
    @classmethod
    def create(
            cls, array: np.ndarray, path: Optional[str] = None, dir: Optional[str] = None, overwrite: bool = False
    ) -> Self:
        if array.ndim > 2:
            raise NotImplementedError("Only arrays with <=2 dimensions are supported.")
        if array.ndim == 1:
            array = array[:, np.newaxis]
        df = pd.DataFrame({str(i): array[:, i] for i in range(array.shape[1])})
        return super().create(df, path=path, dir=dir, overwrite=overwrite)

    def load(self) -> np.ndarray:
        df = super().load()
        return df.values


class SharedDataDict(SharedMemoryContainer):
    def __init__(self, data: dict[str, SharedMemoryContainer]):
        self.data = data

    @classmethod
    def create(cls, data: dict[str, SharedMemoryContainer]) -> Self:
        return cls(data)

    def load(self) -> dict:
        return {k: v.load() for k, v in self.data.items()}

    def close(self) -> Self:
        for v in self.data.values():
            v.close()
        return self

    def unlink(self) -> Self:
        for v in self.data.values():
            v.unlink()
        return self

    @property
    def metadata(self) -> dict:
        metadata = {}
        for k, v in self.data.items():
            metadata[k] = {'class': v.__class__.__name__, 'meta': v.metadata}
        return metadata

    @classmethod
    def from_metadata(cls, metadata: dict) -> Self:
        data = {}
        for name, info in metadata.items():
            type_ = eval(info['class'])
            meta = info['meta']
            data[name] = type_.from_metadata(meta)
        return cls(data)


# -----------------------
# Example usage:

if __name__ == '__main__':
    def example_task(x, y):
        time.sleep(0.1)  # Simulate work
        return x * y

    parser = argparse.ArgumentParser(description="Example usage of parmap")
    parser.add_argument('-n', type=int, default=100)
    args = parser.parse_args()

    xy = list(zip(range(args.n), range(1, 1 + args.n)))

    # try:
    #     print("Running with single worker and thread")
    #     serial_results = parmap(example_task, xy, star=True)
    #     print(f"Serial results: {serial_results[:5]}...")
    # except KeyboardInterrupt:
    #     print("Execution interrupted in thread mode.")

    try:
        print("Running with ThreadPoolExecutor")
        thread_results = parmap(example_task, xy, star=True, mode="thread", n_workers=4)
        print(f"Thread results: {thread_results[:5]}...")
    except KeyboardInterrupt:
        print("Execution interrupted in thread mode.")

    try:
        print("Running with ProcessPoolExecutor and per-process ThreadPoolExecutor")
        process_results = parmap(example_task, xy, star=True, mode="process", n_workers=4, nthreads_per_process=2)
        print(f"Process results: {process_results[:5]}...")
    except KeyboardInterrupt:
        print("Execution interrupted in process mode.")
