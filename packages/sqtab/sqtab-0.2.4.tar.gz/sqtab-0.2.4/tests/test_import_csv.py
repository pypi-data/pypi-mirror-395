import unittest
from pathlib import Path
from sqtab.importer import import_file
from sqtab.db import get_conn


class TestCSVImport(unittest.TestCase):

    TABLE = "test_users"

    def tearDown(self):
        """Clean up only the table created by this test."""
        conn = get_conn()
        conn.execute(f'DROP TABLE IF EXISTS "{self.TABLE}"')
        conn.commit()
        conn.close()

    def test_import_csv(self):
        sample_path = Path("tests/samples/sample.csv")

        # Import into isolated test table
        rows = import_file(sample_path, self.TABLE)
        self.assertEqual(rows, 3)

        conn = get_conn()
        data = conn.execute(f'SELECT * FROM "{self.TABLE}" ORDER BY id').fetchall()
        conn.close()

        expected = [
            (1, "Ana", 30),
            (2, "Marko", 25),
            (3, 'Ivana', 28)
        ]

        self.assertEqual(data, expected)
