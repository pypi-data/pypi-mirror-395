import unittest
import csv
from pathlib import Path
from sqtab.importer import import_file
from sqtab.exporter import export_csv
from sqtab.db import get_conn


class TestCSVExport(unittest.TestCase):

    TABLE = "test_export"
    OUTFILE = Path("tests/out_export.csv")

    def tearDown(self):
        """Clean up: drop test table and delete output CSV"""
        conn = get_conn()
        conn.execute(f'DROP TABLE IF EXISTS "{self.TABLE}"')
        conn.commit()
        conn.close()

        if self.OUTFILE.exists():
            self.OUTFILE.unlink()

    def test_csv_export(self):
        # 1. Import minimal CSV first
        sample_path = Path("tests/samples/sample.csv")
        import_file(sample_path, self.TABLE)

        # 2. Export the table to a new CSV file
        rows_exported = export_csv(self.TABLE, self.OUTFILE)
        self.assertEqual(rows_exported, 3)

        # 3. Read generated CSV
        with open(self.OUTFILE, encoding="utf-8") as f:
            reader = list(csv.reader(f))

        # Expected: header + two rows
        expected = [
            ["id", "name", "age"],
            ["1", "Ana", "30"],
            ["2", "Marko", "25"],
            ["3", "Ivana", "28"],
        ]

        self.assertEqual(reader, expected)
