from collections import defaultdict
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def mapped(f: Callable[[T], U], seq: Iterable[T]) -> list[U]:
    return list(map(f, seq))


def filtered(f: Callable[[T], bool], seq: Iterable[T]) -> list[T]:
    return list(filter(f, seq))


def groupby(f: Callable[[T], U], seq: Iterable[T]) -> dict[U, list[T]]:
    grouped = defaultdict(list)
    for item in seq:
        grouped[f(item)].append(item)
    return dict(grouped)


def flatten(seq: Iterable, depth=None, drop_null=False) -> list:
    if depth == 0:
        return list(seq)
    flattened = []
    for item in seq:
        next_depth = depth - 1 if depth is not None else None
        if isinstance(item, str) or not (hasattr(item, "__len__") or hasattr(item, "__next__")):
            if drop_null and (item is None or item != item):
                continue
            else:
                flattened.append(item)
        else:
            flattened.extend(flatten(item, next_depth, drop_null=drop_null))
    return flattened


def flat_map(f: Callable, seq: Iterable, depth=None, drop_null=True) -> list:
    return flatten(mapped(f, seq), depth=depth, drop_null=drop_null)


def partitioned(f: Callable[[T], bool], seq: Iterable[T]) -> tuple[list[T], ...]:
    true_part, false_part = [], []
    for item in seq:
        if f(item):
            true_part.append(item)
        else:
            false_part.append(item)
    return true_part, false_part
