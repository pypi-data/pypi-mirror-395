# sqtab

[![PyPI version](https://img.shields.io/pypi/v/sqtab.svg)](https://pypi.org/project/sqtab/)
[![Python Versions](https://img.shields.io/pypi/pyversions/sqtab.svg)](https://pypi.org/project/sqtab/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**sqtab** is a minimalist command-line toolkit with **AI assistance** for working with tabular data  
(CSV / JSON) using **SQLite** as a lightweight local database layer.

It is built for developers, data analysts, and engineers who want a fast and clean workflow
without maintaining a full database runtime.

sqtab provides:

- CSV / JSON → SQLite import  
- schema inspection & table listing  
- ad-hoc SQL execution  
- export to CSV / JSON  
- **AI-assisted SQL generation** (`sqtab sql-ai`)  
- **AI-assisted table analysis** (customizable tasks & rules)  
- optional user-defined AI model via `SQTAB_AI_MODEL`

---

## Installation

```bash
pip install sqtab
```

Requires **Python 3.10+**.

---

## Quick Start

### Import CSV or JSON

```bash
sqtab import data.csv users
```

### Inspect table schema

```bash
sqtab tables --schema
```

### Run SQL queries

```bash
sqtab sql "SELECT * FROM users;"
```

### Export a table

```bash
sqtab export users users.csv
```

### Reset the local SQLite database

```bash
sqtab reset
```

For all commands:

```bash
sqtab --help
```

---

## AI Features

sqtab integrates with OpenAI models to provide intelligent data assistance.
You must set an API key (environment variable or `.env`):

```
OPENAI_API_KEY=your-key-here
```

You may also set a preferred model (optional):

```
SQTAB_AI_MODEL=gpt-4o-mini
```

If not provided, sqtab falls back to a safe default.

---

## 1. AI-Generated SQL (`sql-ai`)

Convert natural-language questions into valid SQLite SQL:

```bash
sqtab sql-ai "show all users older than 30"
```

Example result:

```sql
SELECT * FROM users WHERE age > 30;
```

---

## 2. AI-Assisted Table Analysis (`analyze`)

Analyze structure, sample rows, patterns, anomalies, and more.

### Basic usage

```bash
sqtab analyze users --ai
```

### Custom tasks & rules

```bash
sqtab analyze users --ai \
    --task "Identify anomalies" \
    --task "Suggest indexes" \
    --rule "Be concise"
```

### Load from external files

```bash
sqtab analyze users --ai --tasks-file tasks.txt --rules-file rules.txt
```

---

## Environment Variables

| Variable | Description | Default |
|---------|-------------|---------|
| `OPENAI_API_KEY` | Required for AI features | — |
| `SQTAB_AI_MODEL` | Optional user-preferred model | `gpt-4o-mini` |

---

## Project Status

sqtab is in active early development (**0.x** releases).  
The core CLI is stable, but new AI features are expanding rapidly.

Feedback, ideas, and contributions are welcome.

GitHub repository:  
https://github.com/gojankovic/sqtab

---

## License

MIT License © 2025 Goran Janković
