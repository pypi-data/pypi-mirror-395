from rich.table import Table
from rich.console import Console
from .db import get_conn

def describe_table(table: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(f'PRAGMA table_info("{table}")')
    rows = cur.fetchall()
    conn.close()

    console = Console()
    t = Table("Column", "Type", "Not Null", "PK", "Default")

    for cid, name, col_type, notnull, dflt, pk in rows:
        t.add_row(name, col_type, str(bool(notnull)), str(bool(pk)), str(dflt))

    console.print(t)
