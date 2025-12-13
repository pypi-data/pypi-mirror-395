"""
Exporter module for sqtab.

Provides utilities for exporting SQLite tables to CSV or JSON files.
"""

import csv
from pathlib import Path
from sqtab.db import get_conn
import json


def export_csv(table: str, path: str | Path) -> int:
    """
    Export a SQLite table into a CSV file.

    Parameters
    ----------
    table : str
        Name of the SQLite table to export.
    path : str | Path
        Output file path for the CSV file.

    Returns
    -------
    int
        Number of exported rows.
    """
    path = Path(path)

    conn = get_conn()
    cur = conn.cursor()

    # Fetch all rows
    result = cur.execute(f'SELECT * FROM "{table}"')
    rows = result.fetchall()

    if not rows:
        # still produce an empty file with header if table exists
        headers = [col[0] for col in result.description]
        _write_csv(path, headers, [])
        conn.close()
        return 0

    headers = [col[0] for col in result.description]

    _write_csv(path, headers, rows)

    conn.close()

    return len(rows)


def _write_csv(path: Path, headers: list[str], rows: list[tuple]):
    """Helper to write CSV file."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def export_json(table: str, path: str | Path) -> int:
    """
    Export a SQLite table into a JSON file.

    Parameters
    ----------
    table : str
        Name of the SQLite table to export.
    path : str | Path
        Output file path.

    Returns
    -------
    int
        Number of exported rows.
    """
    path = Path(path)

    conn = get_conn()
    cur = conn.cursor()

    result = cur.execute(f'SELECT * FROM "{table}"')
    rows = result.fetchall()

    if not rows:
        data = []
    else:
        columns = [col[0] for col in result.description]
        data = [dict(zip(columns, row)) for row in rows]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    conn.close()
    return len(rows)
