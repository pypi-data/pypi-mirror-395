"""
CSV and JSON importer for sqtab.

This module provides basic CSV import functionality. JSON support will be
added in a future commit.
"""

import csv
import json
from typing import Optional
from sqtab.db import get_conn


def import_file(path: str, table: str) -> Optional[int]:
    """
    Import a CSV or JSON file into the specified SQLite table.

    Parameters
    ----------
    path : str
        Path to the input CSV or JSON file.
    table : str
        Name of the SQLite table to import data into.

    Returns
    -------
    Optional[int]
        Number of rows imported, or None if no rows were processed.
    """
    path = str(path)
    path_lower = path.lower()

    if path_lower.endswith(".csv"):
        return _import_csv(path, table)

    if path_lower.endswith(".json"):
        return _import_json(path, table)

    raise ValueError("Only CSV and JSON import are supported at the moment.")


def _import_csv(path: str, table: str) -> int:
    """
    Import data from a CSV file into a SQLite table.

    Performs:
    - column name normalization
    - per-column type inference (INTEGER, REAL, TEXT)
    - row value type inference via infer_type()
    """

    conn = get_conn()
    cur = conn.cursor()

    # Read CSV
    with open_with_bom(path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Strip BOM if present in header (e.g. "﻿id" → "id")
    if rows and list(rows[0].keys()):
        cleaned_rows = []
        for row in rows:
            new_row = {}
            for k, v in row.items():
                clean_key = k.lstrip("\ufeff")  # remove BOM char if present
                new_row[clean_key] = v
            cleaned_rows.append(new_row)
        rows = cleaned_rows

    if not rows:
        return 0

    # Extract original column names from the CSV
    raw_columns = list(rows[0].keys())

    # Normalize column names
    columns = [normalize_column(c) for c in raw_columns]

    # Collect values column-by-column for type inference
    column_values = {col: [] for col in columns}

    for row in rows:
        for raw_col, norm_col in zip(raw_columns, columns):
            column_values[norm_col].append(row[raw_col])

    # Infer type for each column (INTEGER, REAL, TEXT)
    column_types = {
        col: infer_column_type(vals)
        for col, vals in column_values.items()
    }

    # Build CREATE TABLE statement
    col_defs = ", ".join([f'"{col}" {column_types[col]}' for col in columns])
    placeholders = ", ".join(["?"] * len(columns))

    # Create table if not exists
    cur.execute(f'CREATE TABLE IF NOT EXISTS "{table}" ({col_defs})')

    # Insert rows using infer_type on each cell
    for row in rows:
        values = []
        for raw_col in raw_columns:
            v = row[raw_col]
            values.append(infer_type(v))
        cur.execute(
            f'INSERT INTO "{table}" VALUES ({placeholders})',
            values
        )

    conn.commit()
    conn.close()
    return len(rows)



def _import_json(path: str, table: str) -> int:
    """
    Import data from a JSON file into a SQLite table.

    The JSON file must contain either:
    - a list of objects (recommended), or
    - a single object (will be wrapped into a list)

    Returns
    -------
    int
        Number of rows imported.
    """
    conn = get_conn()
    cur = conn.cursor()

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        # Single object → wrap into a list
        rows = [data]
    elif isinstance(data, list):
        rows = data
    else:
        raise ValueError("Invalid JSON format. Expected object or list of objects.")

    if not rows:
        return 0

    columns = rows[0].keys()
    col_list = ", ".join([f'"{col}"' for col in columns])
    placeholders = ", ".join(["?"] * len(columns))

    # Create table if needed
    cur.execute(f'CREATE TABLE IF NOT EXISTS "{table}" ({col_list})')

    # Insert rows
    for row in rows:
        values = list(row.values())
        cur.execute(
            f'INSERT INTO "{table}" VALUES ({placeholders})',
            values
        )

    conn.commit()
    conn.close()
    return len(rows)


def open_with_bom(path: str):
    """Open a file with automatic BOM detection and removal."""
    with open(path, "rb") as f:
        raw = f.read(4)

    # UTF-8 BOM
    if raw.startswith(b"\xef\xbb\xbf"):
        return open(path, encoding="utf-8-sig")

    # UTF-16 LE BOM
    if raw.startswith(b"\xff\xfe"):
        return open(path, encoding="utf-16-le")

    # UTF-16 BE BOM
    if raw.startswith(b"\xfe\xff"):
        return open(path, encoding="utf-16-be")

    # Fallback: UTF-8
    return open(path, encoding="utf-8")


def infer_type(value: str):
    value = value.strip()

    if value == "":
        return None

    # int
    if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
        return int(value)

    # float
    try:
        return float(value)
    except ValueError:
        pass

    # boolean
    lower = value.lower()
    if lower in ("true", "false"):
        return lower == "true"

    return value  # leave as string

def infer_column_type(values):
    """
    Infer SQLite column type (INTEGER, REAL, TEXT)
    based on all values in the column.
    """

    # Remove empty strings
    non_empty = [v for v in values if v != ""]

    if not non_empty:
        return "TEXT"  # all empty → TEXT

    # Try INTEGER
    try:
        for v in non_empty:
            int(v)
        return "INTEGER"
    except ValueError:
        pass

    # Try REAL
    try:
        for v in non_empty:
            float(v)
        return "REAL"
    except ValueError:
        pass

    # Try BOOLEAN
    bool_set = {"true", "false", "True", "False"}
    if all(v in bool_set for v in non_empty):
        return "TEXT"

    # Otherwise TEXT
    return "TEXT"

def normalize_column(col: str) -> str:
    return col.strip().replace(" ", "_").lower()

