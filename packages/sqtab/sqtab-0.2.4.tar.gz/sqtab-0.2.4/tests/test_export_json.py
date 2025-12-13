import unittest
import json
from pathlib import Path
from sqtab.importer import import_file
from sqtab.exporter import export_json
from sqtab.db import get_conn


class TestJSONExport(unittest.TestCase):

    TABLE = "test_json_export"
    OUTFILE = Path("tests/out_export.json")

    def tearDown(self):
        """Clean up test table and output file."""
        conn = get_conn()
        conn.execute(f'DROP TABLE IF EXISTS "{self.TABLE}"')
        conn.commit()
        conn.close()

        if self.OUTFILE.exists():
            self.OUTFILE.unlink()

    def test_json_export(self):
        sample_json = Path("tests/samples/sample.json")

        import_file(sample_json, self.TABLE)

        rows = export_json(self.TABLE, self.OUTFILE)
        self.assertEqual(rows, 2)

        # Load exported JSON
        with open(self.OUTFILE, encoding="utf-8") as f:
            data = json.load(f)

        expected = [
            {"id": 1, "name": "Ana", "age": 30},
            {"id": 2, "name": "Marko", "age": 25}
        ]

        self.assertEqual(data, expected)
