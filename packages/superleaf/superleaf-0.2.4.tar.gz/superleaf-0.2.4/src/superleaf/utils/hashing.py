import hashlib
from collections.abc import Iterable


def _quoted(s: str):
    if not isinstance(s, str):
        raise TypeError('Input must be type str')
    if not any(c in s for c in ['"', "'"]):
        return f"'{s}'"
    else:
        return s


class HashStringGenerator:
    def __init__(self, algo=None, length=None):
        if algo is not None:
            if isinstance(algo, str):
                algo = getattr(hashlib, algo)
        else:
            if length is not None:
                algo = hashlib.shake_128  # variable length
            else:
                algo = hashlib.sha1
        self._algo = algo
        self._length = length
        self._values = []

    def new(self) -> 'HashStringGenerator':
        return type(self)(algo=self._algo, length=self._length)

    def fork(self) -> 'HashStringGenerator':
        new = self.new()
        new._values = self._values.copy()
        return new

    def _validate(self):
        self._algo()  # Make sure hasher can be initialized

    def _add_values(self, values) -> None:
        if isinstance(values, str) or not isinstance(values, Iterable):
            values = [values]
        for value in values:
            if value is not None:
                if isinstance(value, str):
                    str_val = _quoted(value)
                else:
                    str_val = str(value)
                self._values.append(str_val.encode())

    def __call__(self, *values) -> 'HashStringGenerator':
        for value in values:
            self._add_values(value)
        return self

    def to_str(self, length=None) -> str:
        if length is None:
            length = self._length
        hasher = self._algo()
        for value in self._values:
            hasher.update(value)
        if length is not None:
            try:
                s = hasher.hexdigest(length)
            except TypeError:
                s = hasher.hexdigest()
            if len(s) < length:
                raise ValueError(
                    f'requested hash string length ({length}) is longer than {type(hasher).__name__} hex strings')
            else:
                return s[:length]
        else:
            return hasher.hexdigest()

    def __repr__(self) -> str:
        return self.to_str()


def get_hash_string(values, algo=None, length=None) -> str:
    return str(HashStringGenerator(algo=algo, length=length)(values))
