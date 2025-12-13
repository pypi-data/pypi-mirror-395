"""
Database connection utilities for sqtab.
"""

import sqlite3
from pathlib import Path

# Default SQLite database file used by sqtab.
DB_PATH = Path("sqtab.db")


def get_conn() -> sqlite3.Connection:
    """
    Return a new SQLite connection using the default database file.
    The database file will be created automatically if it does not exist.
    """
    return sqlite3.connect(DB_PATH)
