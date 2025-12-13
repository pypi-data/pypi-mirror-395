import unittest
from typer.testing import CliRunner
from sqtab.cli import app
from sqtab.db import get_conn

runner = CliRunner()


class TestAnalyzeCommand(unittest.TestCase):

    TABLE = "analyze_test"

    def setUp(self):
        conn = get_conn()
        conn.execute(f'''
            CREATE TABLE IF NOT EXISTS "{self.TABLE}" (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER
            );
        ''')
        conn.commit()

        conn.execute(
            f'INSERT INTO "{self.TABLE}" (id, name, age) VALUES (1, "Ana", 30)'
        )
        conn.execute(
            f'INSERT INTO "{self.TABLE}" (id, name, age) VALUES (2, "Marko", 25)'
        )
        conn.commit()
        conn.close()

    def tearDown(self):
        conn = get_conn()
        conn.execute(f'DROP TABLE IF EXISTS "{self.TABLE}"')
        conn.commit()
        conn.close()

    def test_analyze_output(self):
        result = runner.invoke(app, ["analyze", self.TABLE])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Rows:", result.stdout)
        self.assertIn("Columns:", result.stdout)
        self.assertIn("id", result.stdout)
        self.assertIn("name", result.stdout)
        self.assertIn("age", result.stdout)
