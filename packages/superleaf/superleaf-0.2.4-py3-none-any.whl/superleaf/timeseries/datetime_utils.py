from datetime import datetime, time, timedelta
import pytz
from typing import Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
import pendulum
from pendulum.exceptions import ParserError
from pendulum.tz.exceptions import InvalidTimezone

from superleaf.stats.circular import circmean


_SECONDS_YEAR_2020 = int(pendulum.DateTime(2020, 1, 1).timestamp())


def to_datetime(dt, tz=None) -> pendulum.DateTime:
    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=pytz.UTC)
    elif isinstance(dt, str):
        try:
            dt = pendulum.parse(dt)
        except ParserError as err:
            dt_parts, tz_str = dt.split()[:-1], dt.split()[-1]
            if dt_parts:
                try:
                    dtz = pendulum.timezone(tz_str)
                except InvalidTimezone:
                    raise err
                dt = pendulum.parse(' '.join(dt_parts), tz=dtz)
            else:
                raise err
    elif isinstance(dt, (int, float, np.int_, np.float64)):
        if (dt / _SECONDS_YEAR_2020) > 1e2:
            dt /= 1e9
        dt = pendulum.from_timestamp(dt, tz='UTC')
    else:
        raise NotImplementedError(f"datetime conversion not implemented for type {type(dt).__name__}")
    if isinstance(tz, str):
        tz = pendulum.timezone(tz)
    if tz is not None:
        dt = dt.astimezone(tz)
    return dt


def as_dict(dt) -> Dict[str, int]:
    units = ['year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond']
    if isinstance(dt, time):
        units = units[3:]
    return {unit: getattr(dt, unit) for unit in units}


def to_date(dt, tz=None, end_of_day=False) -> datetime:
    try:
        if end_of_day:
            return to_datetime(dt, tz=tz).replace(hour=23, minute=59, second=59, microsecond=999999)
        else:
            return to_datetime(dt, tz=tz).replace(hour=0, minute=0, second=0, microsecond=0)
    except (AttributeError, ValueError):
        return dt


def get_date_range(start, end=None, tz=None, fmt=None):
    # Similar to pandas.date_range (though less powerful), but can return formatted strings instead
    start = to_date(start, tz=tz)
    end = to_date(end or pendulum.now(), tz=tz)
    dates = [start]
    while dates[-1] < end:
        dates.append(dates[-1].add(days=1))
    if fmt:
        if '%' in fmt:
            dates = list(map(lambda dt: dt.strftime(fmt), dates))
        else:
            dates = list(map(lambda dt: dt.format(fmt), dates))
    return dates


def get_datetime_range(start, end, delta=None, inclusive=False, **timedelta_kwargs) -> List[datetime]:
    if inclusive:
        def keep_going(t):
            return t <= end
    else:
        def keep_going(t):
            return t < end

    start = to_datetime(start)
    end = to_datetime(end)
    if delta is None:
        delta = timedelta(**timedelta_kwargs)
    dts = []
    current = start
    while keep_going(current):
        dts.append(current)
        current += delta
    return dts


def get_hours_minutes_seconds(time_1, time_2=None) -> Tuple[int, int, float]:
    if isinstance(time_1, timedelta):
        delta = time_1
    elif time_2 is None:
        raise ValueError('Either a timedelta or two datetimes are required as input')
    elif time_2 > time_1:
        delta = time_2 - time_1
    else:
        delta = time_1 - time_2
    total_seconds = delta.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = total_seconds % 60
    return hours, minutes, seconds


def nearly_simultaneous(t1, t2, epsilon_seconds) -> bool:
    if isinstance(t1, time) and isinstance(t2, time):
        dt1 = datetime(1970, 1, 1, **as_dict(t1))
        dt2 = datetime(1970, 1, 1, **as_dict(t2))
    elif isinstance(t1, time):
        dt2 = to_datetime(t2)
        t1_dict = as_dict(dt2)
        t1_dict.update(as_dict(t1))
        dt1 = datetime(**t1_dict)
    elif isinstance(t2, time):
        dt1 = to_datetime(t1)
        t2_dict = as_dict(dt1)
        t2_dict.update(as_dict(t2))
        dt2 = datetime(**t2_dict)
    else:
        dt1 = to_datetime(t1)
        dt2 = to_datetime(t2)
    return abs((dt1 - dt2).total_seconds()) <= epsilon_seconds


def to_period(period_or_start, end=None, **delta_kwargs) -> pendulum.Interval:
    if isinstance(period_or_start, pendulum.Interval):
        return period_or_start
    else:
        if hasattr(period_or_start, 'start') and hasattr(period_or_start, 'end'):
            start = period_or_start.start
            end = period_or_start.end
        elif isinstance(period_or_start, tuple) and len(period_or_start) == 2:
            start, end = period_or_start
        elif end is None and len(delta_kwargs) == 0:
            raise NotImplementedError(f"Unsure how to parse start and end from {period_or_start}")
        else:
            start = period_or_start
        start = to_datetime(start)
        if end is None:
            end = start.add(**delta_kwargs)
        else:
            end = to_datetime(end)
        if start > end:
            raise ValueError(f"Start ({start}) is after end ({end})")
        return pendulum.interval(start, end)


def to_seconds_in_day(timestamps, local=False) -> np.ndarray:
    def _via_pandas():
        times = pd.to_datetime(timestamps, utc=(not local))
        if not hasattr(times, '__len__'):
            times = [times]
        if not isinstance(times, pd.DatetimeIndex):
            if not isinstance(times, pd.Series):
                times = pd.Series(times)
            times = pd.DatetimeIndex(times.map(lambda t: t.replace(tzinfo=None)))
        times = times.tz_localize(None).astype('datetime64[ns]')
        return (times.hour * 3600 + times.minute * 60 + times.second + times.microsecond / 1e6).values

    def _brute_force():
        h_m_s_us = []
        for t in timestamps:
            t = to_datetime(t)
            h_m_s_us.append([t.hour, t.minute, t.second, t.microsecond])
        h_m_s_us = np.array(h_m_s_us)
        return h_m_s_us[:, 0] * 3600 + h_m_s_us[:, 1] * 60 + h_m_s_us[:, 2] + h_m_s_us[:, 3] / 1e6

    try:
        return _via_pandas()
    except Exception as e:
        try:
            return _brute_force()
        except Exception:
            raise e


def midpoint(dt1, dt2) -> datetime:
    dt1 = to_datetime(dt1)
    dt2 = to_datetime(dt2)
    return dt1 + (dt2 - dt1) / 2


def seconds_in_day(timestamps, local=False) -> np.ndarray:
    def _via_pandas():
        times = pd.to_datetime(timestamps, utc=(not local))
        if not hasattr(times, '__len__'):
            times = [times]
        if not isinstance(times, pd.DatetimeIndex):
            if not isinstance(times, pd.Series):
                times = pd.Series(times)
            times = pd.DatetimeIndex(times.map(lambda t: t.replace(tzinfo=None)))
        times = times.tz_localize(None).astype('datetime64[ns]')
        return (times.hour * 3600 + times.minute * 60 + times.second + times.microsecond / 1e6).values

    def _brute_force():
        h_m_s_us = []
        for t in timestamps:
            t = to_datetime(t)
            h_m_s_us.append([t.hour, t.minute, t.second, t.microsecond])
        h_m_s_us = np.array(h_m_s_us)
        return h_m_s_us[:, 0] * 3600 + h_m_s_us[:, 1] * 60 + h_m_s_us[:, 2] + h_m_s_us[:, 3] / 1e6

    try:
        return _via_pandas()
    except Exception as e:
        try:
            return _brute_force()
        except Exception:
            raise e


def mean_time(timestamps, weights=None, local=False, nan_policy='propagate') -> time:
    seconds = seconds_in_day(timestamps, local=local)
    mean_seconds = circmean(seconds, weights=weights, high=(24 * 60 * 60), nan_policy=nan_policy)
    return pd.Timestamp(mean_seconds * 1e9).time()


def times_to_radians(timestamps, local=False) -> np.ndarray:
    return seconds_in_day(timestamps, local=local) / (24 * 60 * 60) * 2 * np.pi


def get_first_time_in_interval(t: time, start: Union[datetime, Sequence[datetime]], end: Optional[datetime] = None
                               ) -> Optional[datetime]:
    if isinstance(t, str):
        t = pendulum.parse(t, exact=True)
    if end is None and not isinstance(start, str) and hasattr(start, '__len__'):
        start, end = start
    start = to_datetime(start)
    if end is not None:
        end = to_datetime(end)
    d = start.date()
    dt = datetime(d.year, d.month, d.day, t.hour, t.minute, t.second, t.microsecond, tzinfo=start.tzinfo)
    if dt < start:
        d += timedelta(days=1)
        dt = datetime(d.year, d.month, d.day, t.hour, t.minute, t.second, t.microsecond, tzinfo=start.tzinfo)
    if end is not None and dt > end:
        dt = None
    return dt
