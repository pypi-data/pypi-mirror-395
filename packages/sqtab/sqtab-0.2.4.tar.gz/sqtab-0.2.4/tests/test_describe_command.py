import sqlite3
from sqtab.describe import describe_table
from sqtab.db import DB_PATH
from io import StringIO
from rich.console import Console


def setup_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS products")
    cur.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            price REAL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def test_describe_outputs_schema(monkeypatch):
    setup_table()

    buffer = StringIO()
    monkeypatch.setattr(Console, "print", lambda self, x: buffer.write(str(x)))

    describe_table("products")

    output = buffer.getvalue()

    assert "id" in output
    assert "INTEGER" in output
    assert "True" in output  # PK or NOT NULL entries
    assert "title" in output
    assert "price" in output
