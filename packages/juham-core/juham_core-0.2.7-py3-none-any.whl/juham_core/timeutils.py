"""Time management for Juham framework.
"""

import datetime
import time
from typing import Optional
import pytz


def quantize(quanta: float, value: float) -> float:
    """Quantize the given value.

    Args:
        quanta (float): resolution for quantization
        value (float): value to be quantized

    Returns:
        (float): quantized value

    Example:
    ::

        hour_of_a_day = quantize(3600, epoch_seconds)
    """
    return (value // quanta) * quanta


def epoc2utc(epoch: float) -> str:
    """Converts the given epoch time to UTC time string. All time
    coordinates are represented in UTC time. This allows the time
    coordinate to be mapped to any local time representation without
    ambiguity.

    Args:
        epoch (float) : timestamp in UTC time
        rc (str): time string describing date, time and time zone e.g 2024-07-08T12:10:22Z

    Returns:
        UTC time
    """
    utc_time = datetime.datetime.fromtimestamp(epoch, datetime.timezone.utc)
    utc_timestr = utc_time.strftime("%Y-%m-%dT%H:%M:%S") + "Z"
    return utc_timestr


def timestampstr(ts: float) -> str:
    """Converts the given UTC timestamp to human readable UTC time string of format 'Y-m-d
    H:M:S'.

    Args:
        ts (timestamp):  time stamp to be converted

    Returns:
        rc (string):  human readable date-time string
    """
    dt = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)
    formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


def timestamp() -> float:
    """Returns the current date-time in UTC.

    Returns:
        rc (datetime):  datetime in UTC.
    """
    return datetime.datetime.now(datetime.timezone.utc).timestamp()


def timestamp_hour(ts: float) -> float:
    """Returns the hour in 24h format in UTC.

    Args:
        ts (float): timestamp
    Returns:
        rc (int):  current hour in UTC 0 ...23
    """
    dt = datetime.datetime.fromtimestamp(ts)
    return dt.hour


def timestamp_hour_local(ts: float, timezone: str) -> float:
    """Returns the hour in 24h format in UTC.

    Args:
        ts (float): timestamp
    Returns:
        rc (int):  current hour in UTC 0 ...23
    """
    utc_time = datetime.datetime.fromtimestamp(ts, tz=pytz.utc)

    # Convert to your local timezone (e.g., 'US/Eastern' for Eastern Time)
    local_time = utc_time.astimezone(pytz.timezone(timezone))

    # Get the hour in your local timezone
    return local_time.hour


def is_time_between(
    begin_time: float, end_time: float, check_time: Optional[float] = None
) -> bool:
    """Check if the given time is within the given timeline. All
    timestamps must be in UTC time.

    Args:
        begin_time (float): Beginning of the timeline (Unix timestamp).
        end_time (float): End of the timeline (Unix timestamp).
        check_time (Optional[float]): Time to be checked (Unix timestamp). Defaults to current time.

    Returns:
        bool: True if the time is within the timeline.
    """

    time_to_check: float = check_time if check_time is not None else time.time()
    if begin_time < end_time:
        return begin_time <= time_to_check <= end_time
    else:  # Crosses midnight
        return time_to_check >= begin_time or time_to_check <= end_time


def is_hour_within_schedule(hour: float, start_time: float, stop_time: float) -> bool:
    """
    Check if the given hour is within the scheduled start and stop times.

    :param hour: int, current hour (0-23)
    :param start_time: int, start hour (0-23)
    :param stop_time: int, stop hour (0-23)
    :return: bool, True if the hour is within the schedule, False otherwise
    """
    if start_time < stop_time - 0.01:
        # range does not cross midnight
        return start_time <= hour < stop_time
    elif stop_time < start_time - 0.01:
        # Range crosses midnight
        return hour >= start_time or hour < stop_time
    else:
        # null schedule, consider always in.
        return True



def elapsed_seconds_in_interval(ts_utc: float, interval: int) -> float:
    """
    Compute the elapsed seconds within a given interval.

    Args:
        ts_utc (float): Timestamp in UTC (seconds since epoch)
        interval (int): Interval in seconds (e.g., 3600 for hour, 86400 for day)

    Returns:
        float: Number of seconds elapsed within the interval
    """
    ts = datetime.datetime.fromtimestamp(ts_utc)

    # Compute the start of the interval
    epoch_seconds = ts_utc
    elapsed_in_interval = epoch_seconds % interval

    return elapsed_in_interval


# Convenience wrappers
def elapsed_seconds_in_hour(ts_utc: float) -> float:
    return elapsed_seconds_in_interval(ts_utc, 3600)

def elapsed_seconds_in_day(ts_utc: float) -> float:
    return elapsed_seconds_in_interval(ts_utc, 86400)
