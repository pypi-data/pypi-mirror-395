import unittest
from typer.testing import CliRunner
from sqtab.cli import app
from sqtab.db import get_conn

runner = CliRunner()


class TestSQLCommand(unittest.TestCase):

    TABLE = "sql_test_table"

    def tearDown(self):
        """Drop test table after each test."""
        conn = get_conn()
        conn.execute(f'DROP TABLE IF EXISTS "{self.TABLE}"')
        conn.commit()
        conn.close()

    def test_select_nonexistent_table(self):
        result = runner.invoke(app, ["sql", "SELECT * FROM does_not_exist;"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("no such table", result.stdout.lower())

    def test_create_table(self):
        result = runner.invoke(app, [
            "sql",
            f'CREATE TABLE IF NOT EXISTS {self.TABLE} (id INTEGER);'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Rows affected", result.stdout)

    def test_insert_and_select(self):
        # Create table
        runner.invoke(app, [
            "sql",
            f'CREATE TABLE IF NOT EXISTS {self.TABLE} (id INTEGER, name TEXT);'
        ])

        # Insert
        insert_result = runner.invoke(app, [
            "sql",
            f"INSERT INTO {self.TABLE} (id, name) VALUES (1, 'X');"
        ])
        self.assertEqual(insert_result.exit_code, 0)

        # Select
        select_result = runner.invoke(app, [
            "sql",
            f"SELECT * FROM {self.TABLE};"
        ])
        self.assertEqual(select_result.exit_code, 0)
        self.assertIn("id", select_result.stdout)     # header
        self.assertIn("X", select_result.stdout)      # row
