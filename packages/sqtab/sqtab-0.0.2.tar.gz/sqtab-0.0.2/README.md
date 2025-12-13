# sqtab

Minimal command-line toolkit for working with tabular data (CSV / JSON) using SQLite.

sqtab allows you to:

- import CSV or JSON into a SQLite table  
- run SQL queries  
- inspect table schemas  
- export tables to CSV  
- analyze tables (AI-assisted analysis coming soon)

---

## Installation

Install using pip:

```bash
pip install sqtab
```

Requires Python 3.10+.

---

## Basic Usage

### Import CSV or JSON

```bash
sqtab import data.csv users
```

### View table schema

```bash
sqtab tables --schema
```

### Run SQL queries

```bash
sqtab sql "SELECT * FROM users;"
```

### Export a table to CSV

```bash
sqtab export users users_export.csv
```

### Reset the database

```bash
sqtab reset
```

For a full list of commands:

```bash
sqtab --help
```

---

## Project Status

sqtab is in early development (0.x releases).  
Feedback and contributions are welcome.

Source code:  
https://github.com/gojankovic/sqtab


## License

MIT License © 2025 Goran Janković
