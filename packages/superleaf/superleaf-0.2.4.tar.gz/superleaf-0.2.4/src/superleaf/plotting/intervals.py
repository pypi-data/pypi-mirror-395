from dataclasses import astuple, dataclass
from itertools import repeat
from typing import Any, List
from warnings import warn

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


@dataclass
class StateInterval:
    start: Any
    end: Any
    state: Any

    def __iter__(self):
        return iter(astuple(self))


def _get_intervals_from_series(states, t=None) -> List[StateInterval]:
    if isinstance(states, pd.Series):
        if t is None:
            t = states.index
        ss = states.values
    else:
        if t is None:
            t = np.arange(len(states))
        ss = np.asarray(states)
    distinct_states = np.unique(ss)
    if (len(distinct_states) / len(states)) > 0.5:
        warn("Many distinct states, series variable may be continuous.")
    transitions = np.flatnonzero(np.diff(ss))
    # try:
    t_trans = np.mean(np.vstack([t[transitions], t[transitions + 1]]), axis=0)
    # except:  # I'm not sure why I did this, can't seem to find the failure cases now...
    #     t_trans = t_vec[transitions+1]

    intervals = []
    for i in range(len(t_trans) + 1):
        if i == 0:
            t1 = t[0]
        else:
            t1 = t_trans[i-1]
        if i == (len(t_trans)):
            t2 = t[-1]
            s = ss[-1]
        else:
            s = ss[transitions[i]]
            t2 = t_trans[i]
        intervals.append(StateInterval(t1, t2, s))
    return intervals


def _get_intervals_from_tuples(interval_tuples, states=None) -> List[StateInterval]:
    first_tup = interval_tuples[0]
    if len(first_tup) == 3:
        array = np.array(interval_tuples)
        idxs = [0, 1, 2]
        if states is not None:
            state_idx = states
        else:
            state_idx = 2
        if state_idx not in idxs:
            raise ValueError(f"States index not a valid value: {state_idx}")
        intvl_idxs = [idx for idx in idxs if idx != state_idx]
        intervals = zip(array[:, intvl_idxs[0]].astype(int), array[:, intvl_idxs[1]].astype(int))
        states = array[:, state_idx]
    elif len(first_tup) == 2:
        try:
            if len(first_tup[0]) == 2:
                intervals = [tup[0] for tup in first_tup]
                states = [tup[1] for tup in first_tup]
            elif len(first_tup[1]) == 2:
                intervals = [tup[1] for tup in first_tup]
                states = [tup[0] for tup in first_tup]
            else:
                intervals = interval_tuples
        except TypeError:
            intervals = interval_tuples
            if (
                    states is None
                    or isinstance(states, str)
                    or (hasattr(states, "__len__") and len(states) != len(intervals))
            ):
                states = repeat(states)
    else:
        raise ValueError("Interval tuples should each be either length 2 or 3")
    return [StateInterval(start, end, state) for (start, end), state in zip(intervals, states)]


def _get_intervals_from_vars(starts, ends, states=None) -> List[StateInterval]:
    if states is None:
        states = repeat(None)
    return [StateInterval(start, end, state) for start, end, state in zip(starts, ends, states)]


def _get_intervals_from_df(
    df: pd.DataFrame,
    start_col="start",
    end_col="end",
    state_col="state",
) -> List[StateInterval]:
    return _get_intervals_from_tuples(df[[start_col, end_col]].values, states=df[state_col])


def shade_intervals(
    intervals_or_states=None,
    t=None,
    colors=None,
    alpha=0.3,
    labels=True,
    shade_nan=None,
    ax=None,
    xlim=None,
    ylim=None,
    starts=None,
    ends=None,
    states=None,
):
    if colors is not None and len(intervals_or_states) == len(colors) and len(colors) in (3, 4):
        try:
            c = mpl.colors.to_rgb(colors)
            colors = [c for _ in range(len(intervals_or_states))]
        except ValueError:
            pass

    if intervals_or_states is None:
        intervals = _get_intervals_from_vars(starts=starts, ends=ends, states=states)
    elif isinstance(intervals_or_states, pd.DataFrame):
        col_args = {}
        if starts:
            col_args["start_col"] = starts
        if ends:
            col_args["end_col"] = ends
        if states:
            col_args["state_col"] = states
        intervals = _get_intervals_from_df(intervals_or_states, **col_args)
    elif not isinstance(intervals_or_states[0], StateInterval) and len(intervals_or_states[0]) in (2, 3):
        intervals = _get_intervals_from_tuples(intervals_or_states, states=states)
    elif isinstance(intervals_or_states, pd.Series):
        intervals = _get_intervals_from_series(intervals_or_states, t=t)
        distinct_states = np.unique(intervals_or_states)
        if (len(distinct_states) / len(states)) > 0.5:
            warn("Many distinct states, series variable may be continuous.")
    else:
        raise ValueError("Cannot parse intervals/states argument(s)")

    if len(set([intvl.state for intvl in intervals])) == 1:
        shade_nan = True

    if colors is None:
        distinct_states = np.unique([intvl.state for intvl in intervals])
        cmap = mpl.cm.get_cmap('Paired', len(distinct_states))
        colors = {
            s: c[:3]
            for s, c in zip(distinct_states,
                            [cmap(i/(len(distinct_states)-1)) for i in range(len(distinct_states))])
        }

    if isinstance(colors, dict):
        colors = [colors.get(intvl.state) for intvl in intervals]

    if ax is None:
        ax = plt.gca()

    labeled = []
    objects = []
    for (start, end, state), color in zip(intervals, colors):
        if pd.isna(state) and not shade_nan:
            continue
        if isinstance(labels, dict):
            label = labels.get(state)
        elif labels and state not in labeled:
            label = state
        else:
            label = None
        if label:
            labeled.append(label)
        objects.append(ax.axvspan(start, end, color=color, alpha=alpha, label=label))

    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)

    return objects
