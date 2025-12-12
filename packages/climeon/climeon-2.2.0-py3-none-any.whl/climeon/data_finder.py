"""Data finding utilities

All data finding functions return generators, meaning that data is loaded
lazily.
"""

# External modules
import pandas as pd

# Climeon modules
try:
    from .api import analytics, logfile, blackbox, parse_dates, pandas_interval, \
        parse_interval, SQL_INTERVALS, MAX_RESULTS
    from . import filters
except ImportError:
    # Expected import error during autosummary documentation import
    from api import analytics, logfile, blackbox, parse_dates, pandas_interval, \
        parse_interval, SQL_INTERVALS, MAX_RESULTS
    import filters

def data(module_id, date_from, date_to, variables, aggregation=None,
         interval=None, allow_logfile=True):
    """Fetches data at requested resolution, falls back on logfile and blackbox if needed."""
    # pylint: disable=too-many-arguments,too-many-positional-arguments
    date_from, date_to = parse_dates(date_from, date_to)
    interval = interval or parse_interval(date_from, date_to)
    df = analytics(module_id, date_from, date_to, variables, aggregation, interval)
    seconds = (date_to - date_from).seconds
    ok_freq = not df.empty and _ok_freq(df.index.freq, interval)
    if not allow_logfile or ok_freq or seconds > MAX_RESULTS*10:
        return df
    # Resolution not high enough
    var = list(set(variables))
    if df.empty or df.index.freq != "1s":
        # Fallback on logfile
        df = logfile(module_id, date_from, date_to, var)
    # Improve with blackbox data if available
    if interval == "PT100MS":
        df_bb = blackbox(module_id, date_from, date_to, var)
        df = pd.concat([df, df_bb])
        df = df[~df.index.duplicated(keep="last")]
        df = df.sort_index()
    if df is None:
        return df
    return df[date_from:date_to]

def finder(module_id, date_from, date_to, variables, func, time_before=None,
           time_after=None, min_duration=None, interval="PT1S",
           allow_logfile=True, max_results=MAX_RESULTS):
    """Finds all data where func is True by looking at low and high res data.

    Parameters:
        module_id (str): Module ID e.g. "0104000002".
        date_from (str, datetime): Datetime to start looking from.
        date_to (str, datetime): Datetime to look until.
        variables (list): Variables to get.
        func (function): Function that takes a dataframe and returns a
                         boolean series and the variables it needs.
        time_before (str): Amount of time to include before event. Can be negative.
                           Defaults to 0.
        time_after (str): Amount of time to include after event. Can be negative.
                          Defaults to 0.
        min_duration (str): Minimum duration of event to consider it.
        interval (str): Interval to settle for when looking for events.
        allow_logfile (bool): Indicates if logfile should be used to get
                              required resolution for data.
    """
    # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
    time_before = _parse_time(time_before)
    time_after = _parse_time(time_after)
    min_duration = _parse_time(min_duration)
    date_from, date_to = parse_dates(date_from, date_to)
    _, var = func(pd.DataFrame())
    var = list(set(var))*2
    agg = ["min"] * (len(var)//2) + ["max"] * (len(var)//2)
    all_var = list(set(var + variables))
    default_interval = parse_interval(date_from, date_to, max_results=max_results)
    # Don't allow blackbox data when just searching for events.
    # If blackbox is needed it will be fetched later before yielding
    search_interval = "PT1S" if default_interval == "PT100MS" else default_interval
    df = data(module_id, date_from, date_to, var, agg, search_interval, allow_logfile)
    if df is None:
        return
    f, _ = func(df)
    if df.empty or not any(f):
        return
    intervals = list(SQL_INTERVALS.keys())
    freq_ok = _ok_freq(df.index.freq, interval) or search_interval == "PT1S"
    # Try one interval deeper next time
    next_interval = intervals[max(0, intervals.index(default_interval)-1)]
    if _parse_freq(next_interval) < _parse_freq(interval):
        # Avoid going deeper than requested
        next_interval = interval
    timedelta_req = pd.Timedelta(seconds=max_results-1)*SQL_INTERVALS[next_interval]
    t1 = f.idxmax()
    freq = df.index.freq or pd.Timedelta(seconds=1)
    while any(f[t1:]):
        max_ts = min(t1 + timedelta_req, pd.Timestamp(date_to) + freq).astimezone(t1.tzinfo)
        if not any(f[t1:max_ts].astype(int).diff() == -1):
            # No falling edge detected, might as well take max allowed
            t2 = max_ts
        else:
            last_false = f[t1:max_ts].idxmin()
            last_full = f[t1:last_false][::-1].idxmax()
            t2 = last_full + freq
        if (t1 - time_before) >= (t2 + time_after) or (t2 - t1) < min_duration:
            # No way to fit this period, skip it
            pass
        elif freq_ok or (t1 == date_from and t2 == date_to):
            # Arrived at acceptable interval, yield results
            #
            # If (t1 == date_from and t2 == date_to), that means there is a
            # recursion error: the same data was requested twice. Either we
            # could raise an exception, or we just yield results.
            #
            df_h = data(module_id, t1-time_before, t2+time_after, all_var, None, interval)
            f_h, _ = func(df_h)
            if not df_h[f_h].empty:
                # Make sure we dont accidentally steal neighboring events
                f_h[:t1-pd.Timedelta(seconds=1)] = False
                f_h[t2+pd.Timedelta(seconds=1):] = False
                df_h = df_h[variables]
                # Split the data into segments
                yield from split_df(df_h, f_h, time_before, time_after, min_duration)
        else:
            # Look deeper
            yield from finder(module_id, t1, t2, variables, func, time_before,
                              time_after, min_duration, interval)
        if f[t2:].empty:
            break
        t1 = f[t2:].idxmax()

def split_df(df, f, before, after, duration):
    """Split dataframe into segments where f is True."""
    if df.empty or not any(f):
        return
    i = f.idxmax()
    i_max = f[::-1].idxmax()
    while any(f[i:]):
        if all(f[i:]):
            i2 = i_max
        else:
            i = f[i:].idxmax()
            i2 = f[i:].idxmin()
        if (i - before) < (i2 + after) and (i2 - i) > duration:
            yield df[i-before:i2+after]
        if i == i2:
            break
        i = i2

def _ok_freq(freq, interval):
    """Check if a given frequency is acceptable for an interval."""
    if freq is None and interval == "PT100MS":
        return True
    if freq is None:
        return False
    return freq <= _parse_freq(interval)

def _parse_time(time_str):
    time = pd.Timedelta(time_str)
    if not pd.isna(time):
        return time
    return pd.Timedelta(seconds=0)

def _parse_freq(interval):
    return pd.Timedelta(pandas_interval(interval))

def running(module_id, date_from, date_to, variables, **kwargs):
    """Find data from when module was running.

    Parameters:
        module_id (str): Module ID e.g. "0104000002".
        date_from (str, datetime): Datetime to start looking from.
        date_to (str, datetime): Datetime to look until.
        variables (list): Variables to get.
        time_before (str): Amount of time to include before module was running.
                           Can be negative. Defaults to 0.
        time_after (str): Amount of time to include after module stopped running.
                          Can be negative. Defaults to 0.
        interval (str): Interval to settle for when looking for running data.

    Returns:
        DataFrame: An iterator of dataframes when the module was running.
    """
    yield from finder(module_id, date_from, date_to, variables, filters.running, **kwargs)

def starting(module_id, date_from, date_to, variables, **kwargs):
    """Find data from when module was starting.

    Parameters:
        module_id (str): Module ID e.g. "0104000002".
        date_from (str, datetime): Datetime to start looking from.
        date_to (str, datetime): Datetime to look until.
        variables (list): Variables to get.
        time_before (str): Amount of time to include before module initiated start.
                           Can be negative. Defaults to 0.
        time_after (str): Amount of time to include after module completed start.
                          Can be negative. Defaults to 0.

    Returns:
        DataFrame: An iterator of dataframes when the module was starting.
    """
    yield from finder(module_id, date_from, date_to, variables, filters.starting, **kwargs)

def stopping(module_id, date_from, date_to, variables, **kwargs):
    """Find data from when module was stopping.

    Parameters:
        module_id (str): Module ID e.g. "0104000002".
        date_from (str, datetime): Datetime to start looking from.
        date_to (str, datetime): Datetime to look until.
        variables (list): Variables to get.
        time_before (str): Amount of time to include before module initiated stop.
                           Can be negative. Defaults to 0s.
        time_after (str): Amount of time to include after module completed stop.
                          Can be negative. Defaults to 0s.
        stop_type (str): Stop type to look for. Can be any of
                         ``normal``, ``quick``, ``oil``, or ``emergency``.
                         Defaults to all.

    Returns:
        DataFrame: An iterator of dataframes when the module was stopping.
    """
    stop_type = kwargs.pop("stop_type", None)
    stop_substates = {
        "normal": [0, 1, 2, 3, 4, 5, 6, 7, 8],
        "quick": [100, 101, 102],
        "oil": [200, 201, 202],
        "emergency": [250, 251, 252],
    }
    def func(d):
        stop = filters.stopping(d)
        if not stop_type:
            return stop, ["State [-]"]
        var = ["State [-]", "Substate [-]"]
        return stop & filters.where(d, {"Substate [-]": stop_substates[stop_type]}), var
    yield from finder(module_id, date_from, date_to, variables, func, **kwargs)

def alarm(module_id, date_from, date_to, variables, **kwargs):
    """Find data from when module tripped on an alarm.

    Parameters:
        module_id (str): Module ID e.g. "0104000002".
        date_from (str, datetime): Datetime to start looking from.
        date_to (str, datetime): Datetime to look until.
        variables (list): Variables to get.
        time_before (str): Amount of time to include before trip.
                           Can be negative. Defaults to 10 minutes.
        time_after (str): Amount of time to include after trip.
                          Can be negative. Defaults to 10 minutes.
        states (list): Module states to include. Defaults to running and starting.
                       None to include all states.
        alarm_code (int, list): Alarm code(s) to look for.
                                Defaults to all alarms.

    Returns:
        DataFrame: An iterator of dataframes when the module tripped.
    """
    states = kwargs.pop("states", [3, 4]) * 3
    alarm_code = kwargs.pop("alarm_code", None)
    def func(d):
        # Find out if data before the alarm matches request
        d1 = d.shift(1).bfill()
        c1 = {"AlarmCode [-]": 0}
        if states:
            c1["State [-]"] = states
        f1, var = filters.where(d1, c1)
        if d.empty:
            return f1, var
        # Find out if alarm code matches request
        if alarm_code:
            c = {"AlarmCode [-]": alarm_code}
        else:
            c = {"AlarmCode [-]": [1, 99999]}
        fa, _ = filters.where(d, c)
        f = f1 & fa
        return f | f.shift(-1).ffill(), var
    # Update defaults
    kwargs["time_before"] = kwargs.pop("time_before", "10min")
    kwargs["time_after"] = kwargs.pop("time_after", "10min")
    kwargs["interval"] = kwargs.pop("interval", "PT100MS")
    yield from finder(module_id, date_from, date_to, variables, func, **kwargs)

def steady_state(module_id, date_from, date_to, variables, window="5min", limit=None):
    """Find data from when module ran at steady state.

    Steady state is defined as when the module is running and the
    standard deviation of the input and output hot/cold water, power output
    and pump speed are below a certain limit.

    Parameters:
        module_id (str): Module ID e.g. "0104000002".
        date_from (str, datetime): Datetime to start looking from.
        date_to (str, datetime): Datetime to look until.
        variables (list): Variables to get.
        window (str): Window length. Defaults to 5 minutes.
        limit (dict): Variables and their allowed standard deviation within
                      window length.

    Returns:
        DataFrame: An iterator of dataframes when the module ran at steady state.
    """
    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def func(d):
        return filters.steady(d, window, limit)
    yield from finder(module_id, date_from, date_to, variables, func)
