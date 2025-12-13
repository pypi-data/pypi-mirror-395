"""
Analyzer module for sqtab.

Provides AI-assisted analysis of SQLite tables. This module will later use
OpenAI models to examine table structure, sample rows, and generate insights
about the dataset.

This is the initial skeleton; full implementation will follow.
"""
from pathlib import Path
from typing import List
from sqtab.db import get_conn
from openai import OpenAI

SYSTEM_PROMPT = """
You are an expert data analyst. 
Provide accurate, structured, concise analysis.
Do not hallucinate.
Only comment on columns and rows provided.
Output must follow tasks and rules strictly.
"""

from .prompt_utils import (
    load_prompt_template,
    schema_to_markdown,
    samples_to_markdown,
    validate_list,
)
from sqtab.config import require_api_key, get_ai_model, get_debug, is_ai_available

def analyze_table(table: str) -> dict:
    """
    Analyze a SQLite table and return structure + sample rows.
    """

    conn = get_conn()
    cur = conn.cursor()

    # table existence check
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
        (table,)
    )
    if not cur.fetchone():
        raise ValueError(f"Table '{table}' does not exist.")

    # --- 1) Schema ---
    cur.execute(f'PRAGMA table_info("{table}")')
    columns_info = cur.fetchall()

    schema = []
    for cid, name, col_type, notnull, dflt, pk in columns_info:
        schema.append({
            "name": name,
            "type": col_type or "UNKNOWN",
            "not_null": bool(notnull),
            "primary_key": bool(pk)
        })

    # --- 2) Row count ---
    cur.execute(f'SELECT COUNT(*) FROM "{table}"')
    row_count = cur.fetchone()[0]

    # --- 3) Sample rows (first 5) ---
    cur.execute(f'SELECT * FROM "{table}" LIMIT 5')
    rows = cur.fetchall()

    samples = [
        {col["name"]: row[i] for i, col in enumerate(schema)}
        for row in rows
    ]

    conn.close()

    return {
        "table": table,
        "row_count": row_count,
        "column_count": len(schema),
        "schema": schema,
        "samples": samples,
    }


def run_ai_analysis(table: str, info: dict, tasks: List[str], rules: List[str]) -> str:
    """
    Perform AI analysis using prompt templates, markdown formatting,
    and validated tasks/rules.
    """
    api_key = require_api_key()
    client = OpenAI(api_key=api_key)
    model = get_ai_model()

    # Debug output
    if get_debug():
        import sys
        print(f"[sqtab] Using AI model: {model}", file=sys.stderr)

    # Validate inputs
    tasks = validate_list("Tasks", tasks)
    rules = validate_list("Rules", rules)

    # Load prompt template
    template_path = Path(__file__).parent / "prompts" / "default.md"
    template = load_prompt_template(template_path)

    # Prepare variables
    schema_md = schema_to_markdown(info["schema"])
    samples_md = samples_to_markdown(info["samples"])

    context = {
        "table": table,
        "schema": schema_md,
        "samples": samples_md,
        "tasks": "\n".join(f"- {t}" for t in tasks),
        "rules": "\n".join(f"- {r}" for r in rules),
    }

    # Fill template
    user_prompt = template.substitute(**context)
    print(f"[sqtab] Using AI model: {model}")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
    )

    return response.choices[0].message.content.strip()
