from rich.table import Table
from rich.console import Console
from sqtab.db import get_conn

def head_table(table: str, limit: int = 10):
    conn = get_conn()
    cur = conn.cursor()

    # fetch columns
    cur.execute(f'PRAGMA table_info("{table}")')
    columns = [c[1] for c in cur.fetchall()]

    # fetch rows
    cur.execute(f'SELECT * FROM "{table}" LIMIT ?', (limit,))
    rows = cur.fetchall()

    conn.close()

    # render
    console = Console()
    t = Table(*columns)

    for row in rows:
        t.add_row(*[str(v) for v in row])

    console.print(t)
