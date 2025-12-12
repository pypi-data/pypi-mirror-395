from typing import Iterable, Optional

import numpy as np
import scipy.stats

_NotSpecified = object()


def _notna(x):
    return x is not None and x == x


class CountStat:
    def __init__(
            self,
            count: int | Iterable[bool],
            total: Optional[int] = _NotSpecified,
            expected=None, name=None,
            fractional=False,
    ):
        if total is _NotSpecified:
            try:
                count_bools = np.asarray(count, dtype=bool)
                if not (np.asarray(count) == count_bools).all():
                    raise
                count = count_bools.sum()
                total = len(count_bools)
            except Exception:
                raise ValueError("If total is not provided, count must be an iterable of booleans.")
        else:
            try:
                int(count)
            except Exception:
                raise ValueError("Count must be an integer if total is provided.")
            if _notna(total):
                try:
                    int(total)
                except Exception:
                    raise ValueError("Total must be an integer if it is provided.")
        if fractional:
            self.count = count
            self.total = total
        else:
            if _notna(count) and int(count) != count:
                raise ValueError(f"Non-integer count: {count}")
            if _notna(total) and int(total) != total:
                raise ValueError(f"Non-integer total: {total}")
            self.count = int(count) if _notna(count) else np.nan
            self.total = int(total) if _notna(total) else np.nan
        if expected is not None:
            if expected < 1:
                self.expected = CountStat(expected * total, total, fractional=True)
            else:
                self.expected = CountStat(expected, total)
        else:
            self.expected = None
        self.name = name

    @property
    def fraction(self):
        if self.total == 0:
            return np.nan
        else:
            return self.count / self.total

    @property
    def percent(self):
        return 100 * self.fraction

    def asdict(self):
        return {attr: getattr(self, attr) for attr in ('name', 'count', 'total')}

    @property
    def chi2_pval(self):
        if self.expected:
            obs = [self.count, self.total - self.count]
            exp = [self.expected.count, self.expected.total - self.expected.count]
            return scipy.stats.chisquare(obs, exp)[1]

    def __repr__(self):
        s = f"{self.name}: " if self.name else ""
        s += f"{self.count} of {self.total} = {self.percent:.1f}%"
        if self.expected:
            if int(self.expected.count) == self.expected.count:
                exp_str = str(int(self.expected.count))
            else:
                exp_str = f"{self.expected.count:.1f}"
            exp_pct = self.expected.percent
            if int(exp_pct) == exp_pct:
                exp_pct = str(int(exp_pct))
            else:
                exp_pct = f"{exp_pct:.1f}"
            s += f" (expected {exp_pct}% = {exp_str}, p = {self.chi2_pval:.3f})"
        return s

    def copy(self, **kwargs):
        attr_dict = self.asdict()
        attr_dict.update(kwargs)
        return CountStat(**attr_dict)

    @classmethod
    def nan(cls, name=None):
        return cls(np.nan, np.nan, name=name)

    def __add__(self, other: 'CountStat'):
        return CountStat(self.count + other.count, self.total + other.total,
                         f"{self.name} + {other.name}" if self.name and other.name else None)
