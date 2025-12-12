import time
import datetime
import types
from typing import Optional

def now_utc() -> datetime.datetime:
    """Get the current time in UTC timezone.

    Returns:
        The current datetime in UTC.
    """
    return datetime.datetime.now(datetime.timezone.utc)

def timestamp() -> int:
    """Get the current Unix timestamp.

    Returns:
        The current time as an integer Unix timestamp (seconds since epoch).
    """
    return int(time.time())

def format_time(dt: datetime.datetime, fmt: str="%Y-%m-%d %H:%M:%S") -> str:
    """Format a datetime object as a string.

    Args:
        dt: The datetime object to format.
        fmt: The format string (default: "%Y-%m-%d %H:%M:%S").

    Returns:
        The formatted datetime string.
    """
    return dt.strftime(fmt)

def parse_datetime(value: str) -> datetime.datetime:
    """Parse a datetime string to a datetime object.

    Tries ISO format first, then falls back to common format (YYYY-MM-DD HH:MM:SS).

    Args:
        value: The datetime string to parse.

    Returns:
        The parsed datetime object.

    Raises:
        ValueError: If the string cannot be parsed as a datetime.
    """
    # Try to parse with common ISO format first
    try:
        return datetime.datetime.fromisoformat(value)
    except ValueError:
        # fallback: try common format
        return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

def time_ago(dt: datetime.datetime) -> str:
    """Format a datetime as a human-readable relative time string.

    Args:
        dt: The datetime to format (naive datetimes are assumed to be UTC).

    Returns:
        A human-readable string like "5 minutes ago" or "2 days ago".
    """
    now = now_utc()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    delta = now - dt
    seconds = int(delta.total_seconds())

    intervals = (
        ("year", 31536000),
        ("month", 2592000),
        ("week", 604800),
        ("day", 86400),
        ("hour", 3600),
        ("minute", 60),
        ("second", 1),
    )

    for name, count in intervals:
        value = seconds // count
        if value:
            return f"{value} {name}{'s' if value != 1 else ''} ago"
    return "just now"

def sleep_until(target_time: datetime.datetime) -> None:
    """Sleep until a target time is reached.

    Args:
        target_time: The target datetime to sleep until (naive datetimes are assumed to be UTC).
    """
    if target_time.tzinfo is None:
        target_time = target_time.replace(tzinfo=datetime.timezone.utc)
    while True:
        now = now_utc()
        delta = (target_time - now).total_seconds()
        if delta <= 0:
            break
        time.sleep(min(delta, 1))  # sleep in 1-second chunks

class Timer:
    """Context manager for measuring elapsed time.

    Usage:
        with Timer() as timer:
            # code to measure
            pass
        print(timer.elapsed())  # elapsed time in seconds
    """
    def __init__(self):
        """Initialize the timer."""
        self._start = None
        self._end = None

    def __enter__(self):
        """Start the timer when entering the context.

        Returns:
            The Timer instance for use with the 'as' clause.
        """
        self._start = time.perf_counter()
        return self  # allows using `as t`

    def __exit__(self, exc_type: Optional[type[BaseException]],
                    exc_val: Optional[BaseException],
                    exc_tb: Optional[types.TracebackType]) -> None:
        """Stop the timer when exiting the context."""
        self._end = time.perf_counter()

    def elapsed(self) -> float:
        """Get the elapsed time in seconds.

        Returns:
            The elapsed time in seconds. If the timer is still running,
            returns the current duration since start.
        """
        if self._start is None:
            return 0.0
        end_time = self._end if self._end is not None else time.perf_counter()
        return end_time - self._start
