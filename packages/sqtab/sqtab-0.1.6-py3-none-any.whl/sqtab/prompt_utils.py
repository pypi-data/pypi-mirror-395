from string import Template
from typing import List
from pathlib import Path


def load_prompt_template(path: Path) -> Template:
    return Template(path.read_text(encoding="utf-8"))


def schema_to_markdown(schema: List[dict]) -> str:
    if not schema:
        return "(no columns)"

    header = "| name | type | not_null | primary_key |"
    sep    = "|------|------|----------|-------------|"
    rows = [
        f"| {c['name']} | {c['type']} | {c['not_null']} | {c['primary_key']} |"
        for c in schema
    ]
    return "\n".join([header, sep, *rows])


def samples_to_markdown(samples: List[dict]) -> str:
    if not samples:
        return "(no sample rows)"

    samples = samples[:10]
    cols = samples[0].keys()

    header = "| " + " | ".join(cols) + " |"
    sep    = "| " + " | ".join("---" for _ in cols) + " |"

    rows = []
    for row in samples:
        values = [str(row[col]) for col in cols]
        rows.append("| " + " | ".join(values) + " |")

    return "\n".join([header, sep, *rows])


def validate_list(name: str, items: List[str]) -> List[str]:
    if not items:
        return []
    cleaned = [i.strip() for i in items if i.strip()]
    if not cleaned:
        raise ValueError(f"{name} must contain at least one non-empty item.")
    return cleaned
