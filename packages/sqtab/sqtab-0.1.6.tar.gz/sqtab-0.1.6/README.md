# sqtab

**sqtab** is a minimal command-line toolkit for working with tabular data
(CSV / JSON) using SQLite as a lightweight local database layer.

It is designed for developers, data analysts, and engineers who need a fast,
clean way to explore or transform structured data without setting up a full
database environment.

sqtab provides:

- importing CSV or JSON into SQLite tables  
- schema inspection  
- running ad-hoc SQL queries  
- exporting tables back to CSV or JSON  
- AI-assisted table analysis (customizable with tasks and rules)

---

## Installation

```
pip install sqtab
```

Requires **Python 3.10+**.

---

## Quick Start

### Import CSV or JSON

```
sqtab import data.csv users
```

### Inspect table schema

```
sqtab tables --schema
```

### Run SQL queries

```
sqtab sql "SELECT * FROM users;"
```

### Export a table

```
sqtab export users users.csv
```

### Reset the local SQLite database

```
sqtab reset
```

For all commands:

```
sqtab --help
```

---

## AI-Assisted Analysis

sqtab can analyze table structure and data using an AI model (OpenAI API).

### Basic usage

```
sqtab analyze users --ai
```

### Custom tasks and rules

You can define exactly what the AI should do:

```
sqtab analyze users --ai \
    --task "Identify data issues" \
    --task "Suggest useful SQL queries" \
    --rule "Be concise"
```

### Load tasks and rules from files

```
sqtab analyze users --ai --tasks-file tasks.txt --rules-file rules.txt
```

Requires environment variable or `.env` file:

```
OPENAI_API_KEY=your-key-here
```

---

## Project Status

sqtab is in early active development (0.x releases).  
The CLI is stable; features may expand based on feedback.

Contributions, issues, and suggestions are welcome.

GitHub repository:  
https://github.com/gojankovic/sqtab

---

## License

MIT License © 2025 Goran Janković
