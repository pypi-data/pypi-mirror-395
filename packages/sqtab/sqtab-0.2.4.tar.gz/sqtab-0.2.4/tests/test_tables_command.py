import unittest
from typer.testing import CliRunner
from sqtab.cli import app
from sqtab.db import get_conn

runner = CliRunner()


class TestTablesCommand(unittest.TestCase):

    TABLE = "test_tables"

    def setUp(self):
        conn = get_conn()
        conn.execute(f'CREATE TABLE IF NOT EXISTS "{self.TABLE}" (id INTEGER)')
        conn.commit()
        conn.close()

    def tearDown(self):
        conn = get_conn()
        conn.execute(f'DROP TABLE IF EXISTS "{self.TABLE}"')
        conn.commit()
        conn.close()

    def test_tables_lists_created_table(self):
        result = runner.invoke(app, ["tables"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(self.TABLE, result.stdout)
