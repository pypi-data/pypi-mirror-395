"""
Analyzer module for sqtab.

Provides AI-assisted analysis of SQLite tables. This module will later use
OpenAI models to examine table structure, sample rows, and generate insights
about the dataset.

This is the initial skeleton; full implementation will follow.
"""

from sqtab.db import get_conn


def analyze_table(table: str) -> dict:
    """
    Analyze a SQLite table and return its structure and summary statistics.

    This does NOT call any AI model yet — only prepares the data structure.
    """

    conn = get_conn()
    cur = conn.cursor()

    # Check table existence
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
        (table,)
    )
    exists = cur.fetchone()
    if not exists:
        raise ValueError(f"Table '{table}' does not exist.")

    # 1) Read table structure
    cur.execute(f'PRAGMA table_info("{table}")')
    columns_info = cur.fetchall()  # cid, name, type, notnull, dflt_value, pk

    columns = []
    for cid, name, col_type, notnull, dflt, pk in columns_info:
        columns.append({
            "name": name,
            "type": col_type or "UNKNOWN",
            "not_null": bool(notnull),
            "primary_key": bool(pk)
        })

    # 2) Count rows
    cur.execute(f'SELECT COUNT(*) FROM "{table}"')
    row_count = cur.fetchone()[0]

    # 3) Collect basic stats preview
    summary = {
        "table": table,
        "rows": row_count,
        "column_count": len(columns),
        "columns": columns,
    }

    conn.close()
    return summary
