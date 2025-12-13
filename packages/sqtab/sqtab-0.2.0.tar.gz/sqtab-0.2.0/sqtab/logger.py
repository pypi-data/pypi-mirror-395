"""
Logger module for sqtab.

Provides a simple logging utility for recording sqtab operations.
Logs will be appended to a local file named '.sqtab.log'.

This is the initial skeleton; more advanced logging features may be added later.
"""

from datetime import datetime
from pathlib import Path

LOG_PATH = Path(".sqtab.log")


def log(message: str) -> None:
    """
    Append a log message to the local sqtab log file.

    Parameters
    ----------
    message : str
        The message to record in the log file.

    Notes
    -----
    - Logging is minimal for now.
    - Messages are timestamped using local time.
    - Future improvements may include log levels, rotation, or configuration.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # TODO: expand logging capabilities in future commits.
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
