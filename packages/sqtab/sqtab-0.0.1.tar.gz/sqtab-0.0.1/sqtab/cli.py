"""
CLI interface for sqtab.

Defines the public command-line interface using Typer.
Commands are currently skeletons and will be implemented in future commits.
"""

import os
import sqlite3
import typer

from datetime import datetime
from rich.console import Console
from rich.table import Table
from pathlib import Path
from sqtab.importer import import_file
from sqtab.exporter import export_csv, export_json
from sqtab.analyzer import analyze_table
from sqtab.logger import log
from sqtab.db import DB_PATH, get_conn

app = typer.Typer(help="sqtab - Minimal CLI for tabular data (CSV/JSON + SQLite).")

console = Console()

EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)

@app.command()
def version():
    """
    Show the current sqtab version.
    """
    typer.echo("sqtab version 0.0.1")


@app.command("import")
def import_command(path: str, table: str):
    """
    Import a CSV or JSON file into a SQLite table.
    (Skeleton implementation.)
    """
    result = import_file(path, table)
    log(f"Import called for path={path}, table={table}")
    typer.echo(f"Import command executed (rows imported: {result}).")



@app.command("export")
def export_cmd(table: str, path: str = None):
    """
    Export a SQLite table to CSV or JSON. (CSV implemented)
    """
    # If no output path is provided, generate one automatically.
    if path is None:
        path = EXPORT_DIR / f"{table}.csv"
    else:
        path = Path(path)

    lower = str(path).lower()

    if lower.endswith(".csv"):
        rows = export_csv(table, path)
        print(f"Exported {rows} rows to {path}.")
        return

    if lower.endswith(".json"):
        rows = export_json(table, path)
        print(f"Exported {rows} rows to {path}.")
        return

    print("Unsupported export format. Use .csv or .json.")


@app.command("sql")
def sql_command(query: str):
    """
    Execute a raw SQL query on the SQLite database.

    - For SELECT-like statements, prints a formatted table of results.
    - For modification statements (INSERT/UPDATE/DELETE/etc.), prints affected row count.
    """
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute(query)
        stripped = query.strip().lower()

        if stripped.startswith("select"):
            rows = cur.fetchall()

            if not rows:
                typer.echo("No rows returned.")
            else:
                headers = [col[0] for col in cur.description]

                table = Table(show_header=True, header_style="bold")
                for h in headers:
                    table.add_column(h)

                for row in rows:
                    table.add_row(*[str(value) for value in row])

                console.print(table)
        else:
            conn.commit()
            affected = cur.rowcount
            typer.echo(f"Query executed. Rows affected: {affected}")

        log(f"SQL executed successfully: {query}")

    except sqlite3.Error as exc:
        log(f"SQL error for query={query!r}: {exc}")
        typer.echo(f"Error executing SQL: {exc}")
        raise typer.Exit(code=1)
    finally:
        conn.close()


@app.command("tables")
def tables_command(schema: bool = typer.Option(False, "--schema", help="Show table schemas.")):
    """
    List all tables in the SQLite database.
    Use --schema to include column definitions.
    """

    conn = get_conn()
    cur = conn.cursor()

    # Get all table names
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [row[0] for row in cur.fetchall()]

    if not tables:
        typer.echo("No tables found.")
        return

    if not schema:
        # Just list table names
        for t in tables:
            typer.echo(t)
        return

    # Show schema (column definitions)
    for t in tables:
        cur.execute(f'PRAGMA table_info("{t}")')
        cols = cur.fetchall()  # cid, name, type, notnull, dflt, pk

        col_defs = ", ".join([f'{c[1]} {c[2] or "TEXT"}' for c in cols])

        typer.echo(f"{t} ({col_defs})")

    conn.close()



@app.command("analyze")
def analyze_cmd(table: str):
    """
    Analyze a SQLite table and output structural information.
    (AI integration will be added later.)
    """
    try:
        summary = analyze_table(table)
    except ValueError as exc:
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=1)

    console.print(f"[bold]Table:[/bold] {summary['table']}")
    console.print(f"[bold]Rows:[/bold] {summary['rows']}")
    console.print(f"[bold]Columns:[/bold] {summary['column_count']}")

    # Pretty print column structure
    from rich.table import Table as RichTable
    col_table = RichTable(show_header=True, header_style="bold")
    col_table.add_column("Name")
    col_table.add_column("Type")
    col_table.add_column("Not Null")
    col_table.add_column("Primary Key")

    for col in summary["columns"]:
        col_table.add_row(
            col["name"],
            col["type"],
            str(col["not_null"]),
            str(col["primary_key"]),
        )

    console.print(col_table)

    log(f"Analyzed table {table}.")

    # AI placeholder
    console.print(
        "[green]\nAI analysis not implemented yet — summary prepared.[/green]"
    )

@app.command("info")
def info_command():
    """
    Show information about the SQLite database: size, tables, and SQLite version.
    """

    # If database doesn't exist
    if not os.path.exists(DB_PATH):
        typer.echo("Database file does not exist.")
        return

    # Basic file stats
    size_bytes = os.path.getsize(DB_PATH)
    size_kb = size_bytes / 1024
    mtime = datetime.fromtimestamp(os.path.getmtime(DB_PATH))

    # SQLite version
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("select sqlite_version();")
    version = cur.fetchone()[0]

    # Tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [t[0] for t in cur.fetchall()]

    # Print database info
    console.print(f"[bold]Database:[/bold] {DB_PATH}")
    console.print(f"[bold]Size:[/bold] {size_kb:.2f} KB")
    console.print(f"[bold]SQLite version:[/bold] {version}")
    console.print(f"[bold]Last modified:[/bold] {mtime}")

    if not tables:
        console.print("\n[bold]Tables:[/bold] None")
        conn.close()
        return

    # Table with row counts
    table_view = Table(title="Tables", show_header=True, header_style="bold")
    table_view.add_column("Table")
    table_view.add_column("Rows", justify="right")

    for t in tables:
        cur.execute(f'SELECT COUNT(*) FROM "{t}"')
        row_count = cur.fetchone()[0]
        table_view.add_row(t, str(row_count))

    console.print()
    console.print(table_view)

    conn.close()



@app.command("reset")
def reset_command(hard: bool = typer.Option(False, "--hard", help="Delete sqtab.db file instead of dropping tables.")):
    """
    Reset the database.

    Default: remove all tables (soft reset).
    --hard : delete the sqtab.db file entirely (Windows-safe).
    """

    # HARD RESET ============================================================================
    if hard:
        if not os.path.exists(DB_PATH):
            typer.echo("Database file does not exist.")
            return

        temp_name = DB_PATH.with_suffix(".db.old")

        # 1) Rename the file first (Windows allows renaming locked files)
        try:
            os.replace(DB_PATH, temp_name)
        except Exception as e:
            typer.echo(f"Failed to rename database file: {e}")
            return

        # 2) Delete the renamed file in a new process
        import subprocess, sys

        cmd = f"import os; os.remove(r'{temp_name}')"
        result = subprocess.run([sys.executable, "-c", cmd], capture_output=True, text=True)

        if result.returncode != 0:
            typer.echo("Database renamed but deletion failed:")
            typer.echo(result.stderr)
            return

        log("Database hard reset (file deleted).")
        typer.echo("sqtab.db hard reset complete.")
        return

    # SOFT RESET ============================================================================
    conn = get_conn()
    cur = conn.cursor()

    # Fetch all table names
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()

    if not tables:
        typer.echo("No tables to drop.")
        return

    # Drop tables one by one
    for (table_name,) in tables:
        cur.execute(f'DROP TABLE IF EXISTS "{table_name}"')

    conn.commit()
    conn.close()

    log("Database soft reset (tables dropped).")
    typer.echo("All tables dropped (soft reset).")


