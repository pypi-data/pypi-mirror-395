from typing import Callable, Iterable, List, TypeVar

from superleaf.sequences.serial import filtered, flatten, flat_map as _flat_map_s, groupby, mapped as _mapped_s
try:
    from superleaf.utils.parallel import parmap
except ImportError:
    print("Warning: parallel processing not available, please install parallel requirements. "
          "Falling back to serial processing.")
    parmap = None

T = TypeVar("T")
U = TypeVar("U")


def mapped(f: Callable[[T], U], seq: Iterable[T], parallel=False, workers=None) -> List[U]:
    if parmap is not None and (parallel or (workers is not None and (workers < 0 or workers > 1))):
        if workers is None:
            workers = -1
        return parmap(f, seq, n_workers=workers)
    else:
        return _mapped_s(f, seq)


def flat_map(f: Callable, seq: Iterable, depth=None, drop_null=True, parallel=False, workers=None) -> list:
    if parmap is not None and (parallel or (workers is not None and (workers < 0 or workers > 1))):
        if workers is None:
            workers = -1
        return flatten(parmap(f, seq, n_workers=workers), depth=depth, drop_null=drop_null)
    else:
        return _flat_map_s(f, seq, depth=depth, drop_null=drop_null)
