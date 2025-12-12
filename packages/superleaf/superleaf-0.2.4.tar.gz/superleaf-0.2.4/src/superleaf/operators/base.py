from abc import ABCMeta, abstractmethod
from typing import Any, Callable

from superleaf.operators.wrappers import with_fallback


class Operator(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, arg: Any) -> Any:
        pass

    def __rshift__(self, right: "Operator") -> "_PipedOperator":
        return _PipedOperator(self, right)


class _PipedOperator(Operator):
    def __init__(self, left: Operator, right: Operator):
        self._left = left
        self._right = right

    def __call__(self, arg: Any) -> Any:
        return self._right(self._left(arg))


class FunctionOperator(Operator):
    def __init__(self, f: Callable):
        self._fun = f

    def __call__(self, arg: Any) -> Any:
        return self._fun(arg)


class BooleanOperator(Operator, metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, arg: Any) -> bool:
        pass

    def __or__(self, right: "BooleanOperator") -> "BooleanOperator":
        return _OrBoolOp(self, right)

    def __and__(self, right: "BooleanOperator") -> "BooleanOperator":
        return _AndBoolOp(self, right)

    def __invert__(self) -> "BooleanOperator":
        return _NotBoolOp(self)


class BooleanFunctionOperator(BooleanOperator):
    def __init__(self, f: Callable[[Any], bool]) -> None:
        self._fun = f

    def __call__(self, arg: Any) -> bool:
        result = self._fun(arg)
        try:
            return bool(result)
        except ValueError:
            return result.astype(bool)


class _BinaryBoolOp(BooleanOperator, metaclass=ABCMeta):
    def __init__(self, left: BooleanOperator, right: BooleanOperator):
        self._left = left
        self._right = right


class _OrBoolOp(_BinaryBoolOp):
    def __call__(self, arg: Any) -> bool:
        return self._left(arg) | self._right(arg)


class _AndBoolOp(_BinaryBoolOp):
    def __call__(self, arg: Any) -> bool:
        return self._left(arg) & self._right(arg)


class _NotBoolOp(BooleanOperator):
    def __init__(self, op: BooleanOperator):
        self._op = op

    def __call__(self, arg: Any) -> bool:
        return not self._op(arg)


def operator(f, exceptions=None, fallback=None) -> FunctionOperator:
    if exceptions is not None:
        f = with_fallback(f, fallback=fallback, exceptions=exceptions)
    return FunctionOperator(f)


def bool_operator(f, exceptions=None, fallback=False) -> BooleanFunctionOperator:
    if exceptions is not None:
        if not isinstance(fallback, bool):
            raise TypeError("fallback value must be of type ``bool``")
        f = with_fallback(f, fallback=fallback, exceptions=exceptions)
    return BooleanFunctionOperator(f)
