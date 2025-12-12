import itertools
from typing import Generic, Iterable, Iterator, Self, TypeVar

T = TypeVar('T')


class OrderedSet(Generic[T]):
    """Similar interface to the native set class, but with item order maintained, and expanded functionality, including
    addition and summation. Implemented by storing the set items as keys in an internal dict."""

    def __init__(self, items: Iterable[T] = None):
        self._dict: dict[T, None] = dict(zip(items, itertools.repeat(None))) if items is not None else {}

    @property
    def _items(self) -> list[T]:
        return list(self._dict.keys())

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)

    def copy(self) -> Self:
        return self.__class__(self._items)

    def union(self, other: Iterable[T]) -> Self:
        return self.__class__(itertools.chain(self, other))

    def add(self, item: T) -> Self:
        self._dict[item] = None

    def intersection(self, other: Iterable[T]) -> Self:
        return self.__class__(filter(lambda x: x in other, self))

    def __add__(self, other: Iterable[T]) -> Self:
        return self.__class__(self.union(other))

    def __radd__(self, other: Iterable[T]) -> Self:
        if other == 0:
            return self
        else:
            if not isinstance(other, type(self)):
                other = type(self)(other)
            return other + self

    def __iadd__(self, other: Iterable[T]) -> Self:
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        self._dict.update(other._dict)
        return self

    def __sub__(self, other: Iterable[T]) -> Self:
        return self.__class__(filter(lambda x: x not in other, self))

    def __isub__(self, other: Iterable[T]) -> Self:
        if not isinstance(other, self.__class__):
            other = self.__class__(other)
        for item in other:
            if item in self:
                self._dict.pop(item)
        return self

    def __contains__(self, item: T) -> bool:
        return item in self._dict

    def __eq__(self, other: Self | set[T]) -> Self:
        if isinstance(other, set):
            return set(self._items) == other
        elif isinstance(other, OrderedSet):
            return self._dict == other._dict
        else:
            return False

    def __repr__(self) -> str:
        return "{" + ", ".join([item.__repr__() for item in self._items]) + "}"

    def __len__(self) -> int:
        return len(self._dict)

    def __getitem__(self, item: int) -> T:
        return self._items[item]
