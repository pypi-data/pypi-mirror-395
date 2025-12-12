from datetime import timedelta
from typing import List, Optional, Union

import numpy as np

from superleaf.timeseries.datetime_utils import get_datetime_range, to_datetime
from superleaf.operators.getters import attr_getter

TimeIntervalType = Union["TimeInterval", "TimeIntervals"]


class TimeInterval:
    def __init__(self, start, end=None):
        if end is None:
            if hasattr(start, '__len__') and len(start) == 2:
                start, end = start
            else:
                raise TypeError("TimeInterval requires two values.")
        start = to_datetime(start)
        end = to_datetime(end)
        if end < start:
            raise ValueError("end precedes start")
        elif end == start:
            print("WARNING: start == end")

        self.start = start
        self.end = end

    def copy(self) -> "TimeInterval":
        return TimeInterval(self.start, self.end)

    def delta(self) -> timedelta:
        return self.end - self.start

    def __contains__(self, t):
        t = to_datetime(t)
        return self.start <= t < self.end

    def __eq__(self, other: "TimeInterval") -> bool:
        if isinstance(other, TimeInterval):
            return (other.start == self.start) and (other.end == self.end)
        else:
            return False

    def total_seconds(self) -> float:
        return self.delta().total_seconds()

    def overlap_seconds(self, other: TimeIntervalType) -> float:
        if (self.end < other.start) or (self.start > other.end):
            return 0.0
        elif isinstance(other, TimeInterval):
            overlap = (min(self.end, other.end) - max(self.start, other.start)).total_seconds()
            return max(overlap, 0.0)
        else:
            return sum([self.overlap_seconds(i) for i in other])

    def add_offset(self, delta: timedelta):
        return TimeInterval(self.start + delta, self.end + delta)

    def _intersection_single(self, other: "TimeInterval") -> Optional["TimeInterval"]:
        if self.start < other.start:
            first, second = self, other
        else:
            first, second = other, self
        start = max(first.start, second.start)
        end = min(first.end, second.end)
        if start < end:
            return TimeInterval(start, end)
        else:
            return None

    def intersection(self, other: TimeIntervalType) -> Optional[TimeIntervalType]:
        if isinstance(other, TimeInterval):
            return self._intersection_single(other)

        intersect_intervals = []
        for intvl in other:
            if intvl.start >= self.end:
                break
            else:
                intersect = self._intersection_single(intvl)
                if intersect is not None:
                    intersect_intervals.append(intersect)

        if len(intersect_intervals) == 0:
            return None
        else:
            return TimeIntervals(intersect_intervals).squeeze()

    def union(self, other: TimeIntervalType) -> TimeIntervalType:
        if isinstance(other, TimeInterval):
            intervals = [self] + [other]
            squeeze = True  # If result is single interval, return only an TimeInterval
        else:
            intervals = [self] + other.intervals
            squeeze = False
        consolidated = TimeIntervals(intervals)
        if squeeze:
            consolidated = consolidated.squeeze()
        return consolidated

    def subtract(self, other: TimeIntervalType) -> Optional[TimeIntervalType]:
        intersection = self.intersection(other)
        if isinstance(intersection, TimeInterval):
            intersection = TimeIntervals([intersection])
            squeeze = True  # If result is single interval, return only an TimeInterval
        elif intersection is None:
            return self
        else:
            squeeze = False

        remaining = self.copy()
        subtracted = []
        for intvl in intersection:
            if intvl.start > remaining.start:
                subtracted.append(TimeInterval(remaining.start, intvl.start))
            elif intvl.end < remaining.end:
                remaining.start = intvl.end
        if remaining.start < remaining.end:
            subtracted.append(remaining)

        if len(subtracted) == 0:
            subtracted = None
        elif len(subtracted) == 1:
            subtracted = subtracted[0]
        else:
            subtracted = TimeIntervals(subtracted)
            if squeeze:
                subtracted = subtracted.squeeze()
        return subtracted

    def __sub__(self, other: TimeIntervalType) -> Optional[TimeIntervalType]:
        return self.subtract(other)

    def __repr__(self):
        return f"({self.start} --> {self.end})"

    def split(self, splits_or_timedelta=None, **timedelta_kwargs) -> List["TimeInterval"]:
        if splits_or_timedelta is None and len(timedelta_kwargs) == 0:
            raise ValueError("Either an integer number of splits or a timedelta, or timedelta kwargs, are required to"
                             " split an TimeInterval.")
        elif splits_or_timedelta is None:
            delta = timedelta(**timedelta_kwargs)
            n = int(np.ceil(self.total_seconds() / delta.total_seconds()))
        elif isinstance(splits_or_timedelta, timedelta):
            delta = splits_or_timedelta
            n = int(np.ceil(self.total_seconds() / delta.total_seconds()))
        else:
            delta = timedelta(seconds=(self.total_seconds() / splits_or_timedelta))
            n = int(np.ceil(self.total_seconds() / delta.total_seconds()))
            assert n == splits_or_timedelta

        split_times = get_datetime_range(self.start, self.end, delta, inclusive=True)
        if len(split_times) < n:
            split_times.append(self.end)

        intervals = []
        for i in range(n):
            intervals.append(TimeInterval(split_times[i], split_times[i + 1]))
        return intervals  # Leave as a list, putting into an TimeIntervals instance will rejoin the intervals


class TimeIntervals:
    def __init__(self, intervals: Optional[List[TimeInterval]] = None):
        if intervals is None:
            self.intervals = []
        else:
            if not all(isinstance(i, TimeInterval) for i in intervals):
                raise TypeError(f"All intervals must be of type {TimeInterval.__name__}")
            self.intervals = self.consolidate(intervals)

    @staticmethod
    def consolidate(intervals: List[TimeInterval]) -> List[TimeInterval]:
        if len(intervals) == 0:
            return []
        start_sorted = sorted([i.copy() for i in intervals], key=attr_getter('start'))
        consolidated = [start_sorted[0]]
        for intvl in start_sorted[1:]:
            if intvl.start <= consolidated[-1].end:
                if intvl.end > consolidated[-1].end:
                    consolidated[-1].end = intvl.end
            else:
                consolidated.append(intvl)
        return consolidated

    def copy(self) -> "TimeIntervals":
        return TimeIntervals([i.copy() for i in self])

    @property
    def start(self):
        return self.intervals[0].start

    @property
    def end(self):
        return self.intervals[-1].end

    def total_seconds(self) -> float:
        return sum([intvl.total_seconds() for intvl in self])

    def __iter__(self):
        return iter(self.intervals)

    def __contains__(self, t):
        t = to_datetime(t)
        return any(t in intvl for intvl in self)

    def __eq__(self, other) -> bool:
        if isinstance(other, TimeIntervals):
            return (len(self.intervals) == len(other.intervals)) and all([i1 == i2 for i1, i2 in zip(self, other)])
        else:
            return False

    def overlap_seconds(self, other: TimeIntervalType) -> float:
        if isinstance(other, TimeInterval):
            return other.overlap_seconds(self)
        else:
            if (self.end < other.start) or (self.start > other.end):
                return 0.0
            else:
                return sum([intvl.overlap_seconds(other) for intvl in self])

    def add_offset(self, delta: timedelta):
        return TimeIntervals([intvl.add_offset(delta) for intvl in self])

    def squeeze(self) -> TimeIntervalType:
        if len(self.intervals) == 1:
            return self.intervals[0]
        else:
            return self

    def intersection(self, other: TimeIntervalType) -> Optional[TimeIntervalType]:
        if isinstance(other, TimeInterval):
            return other.intersection(self)

        if self.overlap_seconds(other) == 0.0:
            return None

        intersect_intervals = []
        for intvl in self:
            if intvl.end < other.start:
                break
            intersect = intvl.intersection(other)
            if intersect is not None:
                intersect_intervals.append(intersect)
        intersect_intervals = TimeIntervals(intersect_intervals)

        if len(intersect_intervals.intervals) == 0:
            return None
        else:
            return intersect_intervals

    def union(self, other: TimeIntervalType) -> TimeIntervalType:
        if isinstance(other, TimeInterval):
            other = TimeIntervals([other])
        return TimeIntervals(self.intervals + other.intervals)

    def subtract(self, other: TimeIntervalType) -> Optional[TimeIntervalType]:
        remaining = []
        for intvl in self:
            i_remaining = intvl - other
            if i_remaining is not None:
                remaining.append(i_remaining)
        remaining = TimeIntervals(remaining)
        if len(remaining.intervals) == 0:
            return None
        else:
            return remaining

    def __sub__(self, other: TimeIntervalType) -> Optional[TimeIntervalType]:
        return self.subtract(other)

    def __repr__(self):
        return f"{{{', '.join([f'({intvl.start} --> {intvl.end})' for intvl in self])}}}"
