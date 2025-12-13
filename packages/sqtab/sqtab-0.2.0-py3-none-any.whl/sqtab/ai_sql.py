import os
import json
import re
from textwrap import dedent
from openai import OpenAI
from pygments.lexers import sql

from sqtab.db import get_conn
from sqtab.prompt_utils import get_ai_model


def _get_schema() -> dict:
    """Return a dict with all SQLite table schemas."""
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cur.fetchall()]

    schema = {}

    for table in tables:
        cur.execute(f"PRAGMA table_info('{table}')")
        cols = cur.fetchall()
        schema[table] = [
            {"name": c[1], "type": c[2], "not_null": bool(c[3]), "pk": bool(c[5])}
            for c in cols
        ]

    conn.close()
    return schema


def generate_sql_from_nl(question: str) -> str:
    """Convert natural-language question into a valid SQLite SQL query."""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    client = OpenAI(api_key=api_key)
    schema = _get_schema()

    prompt = dedent(f"""
    You are a senior SQL engineer. Generate a valid SQLite SQL query.

    RULES:
    - Output SQL only, no explanation.
    - Use correct table and column names.
    - Do not invent tables or columns.
    - Use simple SQLite syntax that works everywhere.
    - If ambiguous, choose the most reasonable interpretation.

    SCHEMA:
    {json.dumps(schema, indent=2)}

    USER QUESTION:
    "{question}"

    Return only SQL:
    """)

    model = get_ai_model()
    print(f"[sqtab] Using AI model: {model}")

    res = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    sql = res.choices[0].message.content.strip()

    return clean_sql(sql)


def clean_sql(sql: str) -> str:
    """
    Extract pure SQL from model output.
    Handles ```sql blocks, ``` blocks, markdown, comments, and noise.
    """

    # If there is a code block, extract content inside it
    block_match = re.search(r"```(?:sql)?\s*(.*?)\s*```", sql, flags=re.DOTALL | re.IGNORECASE)
    if block_match:
        sql = block_match.group(1)

    # Remove backticks in case the model used inline code formatting
    sql = sql.replace("`", "")

    # Remove "sql:" prefix or similar noise
    sql = re.sub(r"(?i)^sql\s*:\s*", "", sql).strip()

    # Remove any comments the model might add (e.g. -- explanation)
    sql = re.sub(r"--.*", "", sql)

    # Remove empty lines
    sql = "\n".join(line for line in sql.splitlines() if line.strip())

    return sql.strip()

