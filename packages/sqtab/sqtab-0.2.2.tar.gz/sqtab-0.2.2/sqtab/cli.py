"""
CLI interface for sqtab.

Defines the public command-line interface using Typer.
Commands are currently skeletons and will be implemented in future commits.
"""

import os
import sqlite3
from importlib.metadata import version as get_version, PackageNotFoundError
from typing import List, Optional

import typer

from datetime import datetime
from rich.console import Console
from rich.table import Table
from pathlib import Path
from sqtab.importer import import_file
from sqtab.exporter import export_csv, export_json
from sqtab.analyzer import analyze_table, run_ai_analysis
from sqtab.logger import log
from sqtab.db import DB_PATH, get_conn
from sqtab.ai_sql import generate_sql_from_nl
from dotenv import load_dotenv

def init_env():
    """Load environment variables for sqtab from expected locations."""

    # 1) Local project .env (preferred)
    local_env = Path.cwd() / ".env"
    if local_env.exists():
        load_dotenv(local_env)
        return

    # 2) User home .env (fallback)
    home_env = Path.home() / ".env"
    if home_env.exists():
        load_dotenv(home_env)
        return

    # 3) ~/.sqtab/.env (global sqtab config)
    sqtab_env = Path.home() / ".sqtab" / ".env"
    if sqtab_env.exists():
        load_dotenv(sqtab_env)
        return

# Load variables on module import
init_env()

app = typer.Typer(help="sqtab - Minimal CLI for tabular data (CSV/JSON + SQLite).")
console = Console()

EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)

@app.command()
def version():
    """
    Show the current sqtab version.
    """
    print(get_version("sqtab"))
    try:
        v = get_version("sqtab")
        typer.echo(f"sqtab version {v}")
    except PackageNotFoundError:
        typer.echo("sqtab version unknown (package not found)")


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

@app.command("sql-ai")
def sql_ai(
    question: str = typer.Argument(..., help="Natural language query"),
    execute: bool = typer.Option(True, "--exec/--no-exec", help="Execute the generated SQL")
):
    """
    Generate SQL from a natural-language question using AI.
    Example: sqtab sql-ai "show users older than 30"
    """
    sql = generate_sql_from_nl(question)
    console = Console()
    console.print("[bold cyan]Generated SQL:[/]")
    console.print(sql)

    if not execute:
        return

    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
    except Exception as e:
        console.print(f"[red]Error executing SQL: {e}[/red]")
        return

    # Pretty print results
    if rows:
        columns = [desc[0] for desc in cur.description]
        table = Table(*columns)
        for row in rows:
            table.add_row(*[str(x) for x in row])
        console.print(table)
    else:
        console.print("[yellow]No results.[/yellow]")


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


@app.command()
def head(table: str, n: int = 10):
    """Show first N rows of a table."""
    from .head import head_table
    head_table(table, n)


@app.command()
def describe(table: str):
    """Describe table structure."""
    from .describe import describe_table
    describe_table(table)


@app.command("analyze")
def analyze_command(
    table: str,
    ai: bool = typer.Option(False, "--ai", help="Enable AI-based analysis"),
    task: List[str] = typer.Option(None, "--task", help="Custom analysis tasks (can be repeated)"),
    rule: List[str] = typer.Option(None, "--rule", help="Custom AI rules (can be repeated)"),
    tasks_file: Optional[Path] = typer.Option(None, "--tasks-file", help="File containing tasks"),
    rules_file: Optional[Path] = typer.Option(None, "--rules-file", help="File containing rules"),
):
    """
    Analyze a table. With --ai, run AI-based interpretation with optional custom tasks & rules.
    """
    info = analyze_table(table)

    console = Console()
    console.print(f"Table: {table}")
    console.print(f"Rows: {info['row_count']}")
    console.print(f"Columns: {len(info['schema'])}")

    # Schema table output
    schema_table = Table("Name", "Type", "Not Null", "Primary Key")
    for col in info["schema"]:
        schema_table.add_row(
            col["name"],
            col["type"],
            str(col["not_null"]),
            str(col["primary_key"]),
        )
    console.print(schema_table)

    # Samples preview (max 5)
    console.print("\nSample rows (max 5):")
    for row in info["samples"][:5]:
        console.print(row)

    if not ai:
        console.print("\nAI analysis not requested. Use --ai to enable.")
        return

    # ---- Prepare AI tasks ----
    tasks = list(task or [])

    if tasks_file:
        if tasks_file.exists():
            with open(tasks_file, "r", encoding="utf-8") as f:
                tasks.extend([line.strip() for line in f.readlines() if line.strip()])
        else:
            console.print(f"[red]Tasks file not found: {tasks_file}[/red]")

    # ---- Prepare AI rules ----
    rules = list(rule or [])

    if rules_file:
        if rules_file.exists():
            with open(rules_file, "r", encoding="utf-8") as f:
                rules.extend([line.strip() for line in f.readlines() if line.strip()])
        else:
            console.print(f"[red]Rules file not found: {rules_file}[/red]")

    # If user provided nothing → use defaults
    if not tasks:
        tasks = [
            "Describe the purpose of the table.",
            "Interpret column meanings.",
            "Identify potential data quality issues.",
            "Suggest useful analytical SQL queries."
        ]

    if not rules:
        rules = [
            "Write answers in Markdown.",
            "Be precise and structured.",
        ]

    # ---- Run AI ----
    console.print("\nRunning AI analysis...\n")

    ai_result = run_ai_analysis(table, info, tasks=tasks, rules=rules)
    console.print(ai_result)



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


