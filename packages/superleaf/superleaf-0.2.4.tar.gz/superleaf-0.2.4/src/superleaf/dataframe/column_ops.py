from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Iterable, Optional, Union

import pandas as pd


class ColOp(metaclass=ABCMeta):
    """Abstract base class for column operations on pandas DataFrames.

    Subclasses implement transformations or evaluations that produce pandas Series or scalar
    results when applied to DataFrames. Supports chaining and combining using logical and
    arithmetic operators.

    Operators defined on this class:
    ``|`` (bitwise or), ``&`` (bitwise and), ``~`` (bitwise not), ``==`` (equal to), ``!=`` (not equal to),
    ``<`` (less than), ``<=`` (less than or equal to), ``>`` (greater than), ``>=`` (greater than or equal to),
    ``+`` (addition), ``-`` (subtraction), ``*`` (multiplication), ``/`` (division), ``^`` (power)
    """

    @abstractmethod
    def __call__(self, df: pd.DataFrame) -> Union[pd.Series, Any]:
        """Evaluate the operation on the DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame on which to apply the operation.

        Returns
        -------
        Union[pd.Series, Any]
            The resulting pandas Series or scalar value produced by this operation.
        """
        pass

    def __or__(self, right: "ColOp") -> "ColOp":
        return _OrOp(self, right)

    def __and__(self, right: "ColOp") -> "ColOp":
        return _AndOp(self, right)

    def __invert__(self) -> "ColOp":
        return _NotOp(self)

    def __eq__(self, value: Any) -> "ColOp":
        return _EqOp(self, value)

    def __ne__(self, value: Any) -> "ColOp":
        return _NotOp(self == value)

    def __lt__(self, value: Any) -> "ColOp":
        return _LtOp(self, value)

    def __le__(self, value: Any) -> "ColOp":
        return _LeOp(self, value)

    def __gt__(self, value: Any) -> "ColOp":
        return _GtOp(self, value)

    def __ge__(self, value: Any) -> "ColOp":
        return _GeOp(self, value)

    def __add__(self, right: "ColOp") -> "ColOp":
        return _AddOp(self, right)

    def __sub__(self, right: "ColOp") -> "ColOp":
        return _SubtractOp(self, right)

    def __mul__(self, right: "ColOp") -> "ColOp":
        return _MultiplyOp(self, right)

    def __truediv__(self, right: "ColOp") -> "ColOp":
        return _DivideOp(self, right)

    def __pow__(self, right: "ColOp") -> "ColOp":
        return _PowOp(self, right)

    def apply(self, f: Callable[[pd.Series], pd.Series]) -> "ColOp":
        """Apply a transformation function to the result of this operation.

        Parameters
        ----------
        f : callable
            A function that takes a pandas Series and returns a transformed Series.

        Returns
        -------
        ColOp
            A new ColOp representing the application of ``f`` to this operation’s output.
        """
        return _ColApplyOp(self, f)

    def map(self, f: Callable[[Any], Any]) -> "ColOp":
        """Map a function over each element of the Series produced by this operation.

        Parameters
        ----------
        f : callable
            A function applied element-wise to each value in the Series.

        Returns
        -------
        ColOp
            A new ColOp representing the mapped operation.
        """
        return _ColMapOp(self, f)

    def isin(self, values: Iterable[Any]) -> "ColOp":
        """Test whether each element of the Series is in the given values.

        Parameters
        ----------
        values : iterable
            A collection of values to test membership against.

        Returns
        -------
        ColOp
            A new ColOp that yields a boolean Series.
        """
        if isinstance(values, ColOp):
            combined_vals = self.to_list() + values.to_list()
            return combined_vals.map(lambda x: x[0] in x[1])
        else:
            return self.apply(lambda s: s.isin(values))

    def contains(self, value: Any) -> "ColOp":
        """Test whether each element of the Series contains the specified value.

        Parameters
        ----------
        value : Any
            Value to search for within each element.

        Returns
        -------
        ColOp
            A new ColOp that yields a boolean Series.
        """
        return self.map(lambda x: value in x)

    def startswith(self, value: str) -> "ColOp":
        """Test whether each element of the Series starts with the specified substring.

        Parameters
        ----------
        value : str
            Substring to check at the start of each element.

        Returns
        -------
        ColOp
            A new ColOp that yields a boolean Series.
        """
        value = str(value)
        return self.map(lambda x: str(x).startswith(value))

    def endswith(self, value: str) -> "ColOp":
        """Test whether each element of the Series starts with the specified substring.

        Parameters
        ----------
        value : str
            Substring to check at the start of each element.

        Returns
        -------
        ColOp
            A new ColOp that yields a boolean Series.
        """
        value = str(value)
        return self.map(lambda x: str(x).endswith(value))

    def startswith_one_of(self, value: Iterable[str]) -> "ColOp":
        """Test whether each element of the Series starts with the specified substring.

        Parameters
        ----------
        value : str
            Substring to check at the start of each element.

        Returns
        -------
        ColOp
            A new ColOp that yields a boolean Series.
        """
        if isinstance(value, str) or not isinstance(value, Iterable):
            value = [str(value)]
        else:
            value = [str(v) for v in value]
        return self.map(lambda x: any(str(x).startswith(s) for s in value))

    def endswith_one_of(self, value: str) -> "ColOp":
        """Test whether each element of the Series starts with the specified substring.

        Parameters
        ----------
        value : str
            Substring to check at the start of each element.

        Returns
        -------
        ColOp
            A new ColOp that yields a boolean Series.
        """
        if isinstance(value, str) or not isinstance(value, Iterable):
            value = [str(value)]
        else:
            value = [str(v) for v in value]
        return self.map(lambda x: any(str(x).endswith(s) for s in value))

    def notna(self) -> "ColOp":
        """Test for non-missing values in the Series.

        Returns
        -------
        ColOp
            A new ColOp yielding a boolean Series where True indicates non-null values.
        """
        return self.apply(lambda s: s.notna())

    def isna(self) -> "ColOp":
        """Test for missing values in the Series.

        Returns
        -------
        ColOp
            A new ColOp yielding a boolean Series where True indicates null values.
        """
        return self.apply(lambda s: s.isna())

    def astype(self, type_) -> "ColOp":
        """Cast the Series to a specified dtype.

        Parameters
        ----------
        type_ : type or str
            The target data type for the Series.

        Returns
        -------
        ColOp
            A new ColOp representing the cast operation.
        """
        return self.apply(lambda s: s.astype(type_))

    def to_list(self) -> "ColOp":
        """Wrap each element in the Series into a single-element list.

        Returns
        -------
        ColOp
            A new ColOp that converts each scalar to a list containing that value.
        """
        return self.map(lambda x: [x])


class Index(ColOp):
    """Represent the index of a pandas DataFrame.

    Parameters
    ----------
    None

    Examples
    --------
    >>> idx = Index()
    >>> idx(df)
    DatetimeIndex([...])
    """
    def __call__(self, df: pd.DataFrame) -> pd.Index:
        return df.index


class Col(ColOp):
    """Represent a named column in a DataFrame.

    Parameters
    ----------
    name : str, optional
        Column name to select. If None, selects the entire DataFrame.

    Examples
    --------
    >>> col = Col('column_name')
    >>> col(df)
    0    ...
    Name: column_name, dtype: dtype
    """
    def __init__(self, name: Optional[str]):
        self._name = name

    def __call__(self, df: pd.DataFrame) -> pd.Series:
        if self._name is None:
            return df.iloc[:]
        else:
            return df[self._name]


class Values(Col):
    """Represent the values of a pandas Series.

    Notes
    -----
    This raises a TypeError if called on a DataFrame instead of a Series.

    Examples
    --------
    >>> values = Values()
    >>> values(series)
    array([...])
    """
    def __init__(self):
        super().__init__(None)

    def __call__(self, s: pd.Series) -> pd.Series:
        if isinstance(s, pd.DataFrame):
            raise TypeError("Values can only be called on a Series")
        return s.iloc[:]


class _LiteralOp(ColOp):
    def __init__(self, value: Any) -> None:
        self._value = value

    def __call__(self, df: pd.DataFrame) -> Any:
        return self._value


class _ComparisonOp(ColOp):
    def __init__(self, col: ColOp, value: Union[ColOp, Any]) -> None:
        self._col = col
        if isinstance(value, ColOp):
            self._value = value
        else:
            self._value = _LiteralOp(value)


class _EqOp(_ComparisonOp):
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        return self._col(df) == self._value(df)


class _LtOp(_ComparisonOp):
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        return self._col(df) < self._value(df)


class _LeOp(_ComparisonOp):
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        return self._col(df) <= self._value(df)


class _GtOp(_ComparisonOp):
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        return self._col(df) > self._value(df)


class _GeOp(_ComparisonOp):
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        return self._col(df) >= self._value(df)


class _BinaryOp(ColOp):
    def __init__(self, left: Union[ColOp, Any], right: Union[ColOp, Any]) -> None:
        if isinstance(left, ColOp):
            self._left = left
        else:
            self._left = _LiteralOp(left)
        if isinstance(right, ColOp):
            self._right = right
        else:
            self._right = _LiteralOp(right)


class _OrOp(_BinaryOp):
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        return self._left(df) | self._right(df)


class _AndOp(_BinaryOp):
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        return self._left(df) & self._right(df)


class _AddOp(_BinaryOp):
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        return self._left(df) + self._right(df)


class _SubtractOp(_BinaryOp):
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        return self._left(df) - self._right(df)


class _MultiplyOp(_BinaryOp):
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        return self._left(df) * self._right(df)


class _DivideOp(_BinaryOp):
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        return self._left(df) / self._right(df)


class _PowOp(_BinaryOp):
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        return self._left(df) ** self._right(df)


class _NotOp(ColOp):
    def __init__(self, col: ColOp) -> None:
        self._col = col

    def __call__(self, df: pd.DataFrame) -> pd.Series:
        return ~self._col(df)


class _ColApplyOp(ColOp):
    def __init__(self, col: ColOp, f: Callable[[pd.Series], pd.Series]) -> None:
        self._col = col
        self._fun = f

    def __call__(self, df: pd.DataFrame) -> pd.Series:
        return self._fun(self._col(df))


class _ColMapOp(ColOp):
    def __init__(self, col: ColOp, f: Callable[[Any], Any]) -> None:
        self._col = col
        self._fun = f

    def __call__(self, df: pd.DataFrame) -> pd.Series:
        return self._col(df).map(self._fun)
