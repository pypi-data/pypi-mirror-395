# sqtab

sqtab is a minimalist command-line tool for working with tabular data using SQLite.  
It provides a simple workflow for importing CSV/JSON files, inspecting table structures, executing SQL queries, and exporting results.  
The goal is to offer a small, dependency-light utility that is easy to integrate into scripts and data pipelines.

---

## Installation

```bash
git clone https://github.com/gojankovic/sqtab
cd sqtab
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -e .
```

This installs the `sqtab` command inside your virtual environment.

---

## Basic Usage

### Import CSV or JSON into a table

```bash
sqtab import data.csv users
sqtab import data.json users
```

### Analyze table structure

```bash
sqtab analyze users
```

### List tables

```bash
sqtab tables
sqtab tables --schema
```

### Execute SQL

```bash
sqtab sql "SELECT * FROM users;"
```

### Export tables

```bash
sqtab export users output.csv
sqtab export users output.json
```

### Database information

```bash
sqtab info
```

### Reset database

Soft reset (drops all tables):

```bash
sqtab reset
```

Hard reset (delete the database file):

```bash
sqtab reset --hard
```

---

## Command Reference

The full list of commands is always available through:

```bash
sqtab --help
sqtab <command> --help
```

Examples:

```bash
sqtab import --help
sqtab sql --help
sqtab tables --help
```

Each command provides clear parameter descriptions and available options.

---

## License

MIT License © 2025 Goran Janković
