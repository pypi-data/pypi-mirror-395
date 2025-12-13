import sqlite3
from sqtab.head import head_table
from sqtab.db import DB_PATH
from io import StringIO
from rich.console import Console


def setup_test_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("""
        CREATE TABLE users (
            id INTEGER,
            name TEXT,
            age INTEGER
        )
    """)
    cur.executemany(
        "INSERT INTO users (id, name, age) VALUES (?, ?, ?)",
        [
            (1, "Ana", 30),
            (2, "Marko", 25),
            (3, "Ivana", 28),
        ],
    )
    conn.commit()
    conn.close()


def test_head_outputs_first_n_rows(monkeypatch):
    setup_test_db()

    # Capture rich console output
    buffer = StringIO()
    monkeypatch.setattr(Console, "print", lambda self, x: buffer.write(str(x)))

    head_table("users", limit=2)

    output = buffer.getvalue()

    assert "Ana" in output
    assert "Marko" in output
    assert "Ivana" not in output  # limited to first 2 rows
