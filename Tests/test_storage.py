"""
Unit tests for storage/database.py
"""

import os
import unittest

from pychronicle.storage.database import TraceDatabase


TEST_DB = "test_pychronicle.db"


class StorageTests(unittest.TestCase):

    def setUp(self):

        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        self.db = TraceDatabase(TEST_DB)

    def tearDown(self):

        self.db.close()

        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_insert_variable(self):

        self.db.insert_variable(
            "x",
            10,
            1,
            "global"
        )

        rows = self.db.get_history()

        self.assertEqual(len(rows), 1)

        self.assertEqual(
            rows[0]["variable_name"],
            "x"
        )

        self.assertEqual(
            rows[0]["variable_value"],
            "10"
        )

    def test_multiple_records(self):

        self.db.insert_variable("a", 1, 1)

        self.db.insert_variable("b", 2, 2)

        self.db.insert_variable("c", 3, 3)

        rows = self.db.get_history()

        self.assertEqual(len(rows), 3)

    def test_filter_history(self):

        self.db.insert_variable("x", 10, 1)

        self.db.insert_variable("y", 20, 2)

        self.db.insert_variable("x", 30, 3)

        rows = self.db.get_history("x")

        self.assertEqual(len(rows), 2)

    def test_clear_database(self):

        self.db.insert_variable("x", 10, 1)

        self.db.insert_variable("y", 20, 2)

        self.db.clear()

        rows = self.db.get_history()

        self.assertEqual(len(rows), 0)


if __name__ == "__main__":

    unittest.main()