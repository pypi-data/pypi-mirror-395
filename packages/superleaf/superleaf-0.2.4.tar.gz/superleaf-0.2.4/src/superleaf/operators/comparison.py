import re
from typing import Any, Callable, Iterable

import pandas as pd

from superleaf.operators.base import bool_operator, BooleanOperator
from superleaf.operators.string import FuzzyMatcher


def _isna(x: Any) -> bool:
    try:
        return x is None or x != x
    except ValueError:
        return False


def _parse_exc_args(*exc_args, **exc_kwargs) -> dict:
    if exc_args:
        fallback = exc_args[0]
        exc_args = exc_args[1:]
        if exc_args:
            exceptions = exc_args[0]
        elif "exceptions" in exc_kwargs:
            exceptions = exc_kwargs["exceptions"]
        else:
            exceptions = Exception
        return {"fallback": fallback, "exceptions": exceptions}
    else:
        return exc_kwargs


def _get_str_op(str_method: Callable[[str, str], bool], value, str_converter=str, raise_type_error=False):
    if raise_type_error:
        def op(s):
            try:
                return str_method(s, value)
            except Exception as e:
                raise TypeError(str(e))
    elif str_converter is not None:
        if not isinstance(value, str):
            value = str_converter(value)

        def convert(s) -> str:
            if isinstance(s, str):
                return s
            else:
                return str_converter(s)

        def op(s):
            return not _isna(s) and str_method(convert(s), value)
    else:
        def op(s):
            return isinstance(s, str) and str_method(s, value)
    return op


def _get_any_op(str_method: Callable[[str, str], bool], values, str_converter=str, raise_type_error=False):
    if isinstance(values, pd.Series):
        values = values.values
    ops = [_get_str_op(str_method, v, str_converter=str_converter, raise_type_error=raise_type_error) for v in values]
    return lambda s: any(op(s) for op in ops)


class ComparisonFunctions:
    @staticmethod
    def eq(value: Any, *exc_args, **exc_kwargs) -> BooleanOperator:
        return bool_operator(lambda x: x == value, **_parse_exc_args(*exc_args, **exc_kwargs))

    @staticmethod
    def ne(value: Any, *exc_args, **exc_kwargs) -> BooleanOperator:
        return bool_operator(lambda x: x != value, **_parse_exc_args(*exc_args, **exc_kwargs))

    @staticmethod
    def lt(value: Any, *exc_args, **exc_kwargs) -> BooleanOperator:
        return bool_operator(lambda x: x < value, **_parse_exc_args(*exc_args, **exc_kwargs))

    @staticmethod
    def le(value: Any, *exc_args, **exc_kwargs) -> BooleanOperator:
        return bool_operator(lambda x: x <= value, **_parse_exc_args(*exc_args, **exc_kwargs))

    @staticmethod
    def gt(value: Any, *exc_args, **exc_kwargs) -> BooleanOperator:
        return bool_operator(lambda x: x > value, **_parse_exc_args(*exc_args, **exc_kwargs))

    @staticmethod
    def ge(value: Any, *exc_args, **exc_kwargs) -> BooleanOperator:
        return bool_operator(lambda x: x >= value, **_parse_exc_args(*exc_args, **exc_kwargs))

    @staticmethod
    def isin(values: Any, *exc_args, **exc_kwargs) -> BooleanOperator:
        if isinstance(values, pd.Series):
            values = values.values
        return bool_operator(lambda x: x in values, **_parse_exc_args(*exc_args, **exc_kwargs))

    @staticmethod
    def contains(value: Any, *exc_args, **exc_kwargs) -> BooleanOperator:
        return bool_operator(lambda x: value in x, **_parse_exc_args(*exc_args, **exc_kwargs))

    @staticmethod
    def contains_all(values: Any, *exc_args, **exc_kwargs) -> BooleanOperator:
        if isinstance(values, str) or not isinstance(values, Iterable):
            values = [values]
        elif isinstance(values, pd.Series):
            values = values.values
        return bool_operator(lambda x: all(v in x for v in values), **_parse_exc_args(*exc_args, **exc_kwargs))

    @staticmethod
    def contains_any(values: Any, *exc_args, **exc_kwargs) -> BooleanOperator:
        if isinstance(values, str) or not isinstance(values, Iterable):
            values = [values]
        elif isinstance(values, pd.Series):
            values = values.values
        return bool_operator(lambda x: any(v in x for v in values), **_parse_exc_args(*exc_args, **exc_kwargs))

    @staticmethod
    def startswith(value: str, *exc_args, str_converter=str, raise_type_error=False, **exc_kwargs) -> BooleanOperator:
        op = _get_str_op(str.startswith, value, str_converter=str_converter, raise_type_error=raise_type_error)
        return bool_operator(op, **_parse_exc_args(*exc_args, **exc_kwargs))

    @staticmethod
    def endswith(value: str, *exc_args, str_converter=str, raise_type_error=False, **exc_kwargs) -> BooleanOperator:
        op = _get_str_op(str.endswith, value, str_converter=str_converter, raise_type_error=raise_type_error)
        return bool_operator(op, **_parse_exc_args(*exc_args, **exc_kwargs))

    @staticmethod
    def startswith_one_of(
            values: Iterable[str], *exc_args, str_converter=str, raise_type_error=False, **exc_kwargs
    ) -> BooleanOperator:
        op = _get_any_op(str.startswith, values, str_converter=str_converter, raise_type_error=raise_type_error)
        return bool_operator(op, **_parse_exc_args(*exc_args, **exc_kwargs))

    @staticmethod
    def endswith_one_of(
            values: Iterable[str], *exc_args, str_converter=str, raise_type_error=False, **exc_kwargs
    ) -> BooleanOperator:
        op = _get_any_op(str.endswith, values, str_converter=str_converter, raise_type_error=raise_type_error)
        return bool_operator(op, **_parse_exc_args(*exc_args, **exc_kwargs))

    @staticmethod
    def matches_regex(
            pattern: str, *exc_args, flags=None, str_converter=str, raise_type_error=False, **exc_kwargs
    ) -> BooleanOperator:
        if flags is not None:
            match_kws = {"flags": flags}
        else:
            match_kws = {}

        def has_match(s, pattern):
            return re.match(pattern, s, **match_kws) is not None

        op = _get_str_op(has_match, pattern, str_converter=str_converter, raise_type_error=raise_type_error)
        return bool_operator(op, **_parse_exc_args(*exc_args, **exc_kwargs))

    @staticmethod
    def fuzzy_match(
            targets: str | Iterable[str],
            *exc_args,
            normalizer: Callable[[str], str] = None,
            substring: bool = False,
            score_threshold: float = 80.0,
            raise_type_error=False,
            **exc_kwargs,
    ) -> BooleanOperator:
        matcher = FuzzyMatcher(targets, normalizer=normalizer, substring=substring)
        return matcher.to_bool_operator(
            score_threshold,
            raise_type_error=raise_type_error,
            **_parse_exc_args(*exc_args, **exc_kwargs),
        )

    isna = bool_operator(_isna)
    notna = ~isna
