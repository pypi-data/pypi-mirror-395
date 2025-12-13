import unittest
from sqtab.importer import infer_type


class TestTypeInference(unittest.TestCase):

    def test_int(self):
        self.assertEqual(infer_type("42"), 42)

    def test_float(self):
        self.assertEqual(infer_type("3.14"), 3.14)

    def test_bool(self):
        self.assertTrue(infer_type("true"))
        self.assertFalse(infer_type("false"))

    def test_empty(self):
        self.assertIsNone(infer_type(""))

    def test_string(self):
        self.assertEqual(infer_type("hello"), "hello")
