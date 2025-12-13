import unittest
from sqtab.importer import normalize_column


class TestColumnNormalization(unittest.TestCase):

    def test_trim_lower(self):
        self.assertEqual(normalize_column(" Name "), "name")

    def test_spaces_to_underscores(self):
        self.assertEqual(normalize_column("First Name"), "first_name")
