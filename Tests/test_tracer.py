"""
Unit tests for tracer package.
"""

import os
import unittest

from pychronicle.tracer.execution_tracer import ExecutionTracer


TEST_DB = "test_tracer.db"


class TracerTests(unittest.TestCase):

    def setUp(self):

        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

        self.tracer = ExecutionTracer(TEST_DB)

    def tearDown(self):

        self.tracer.close()

        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_trace(self):

        self.tracer.trace(
            "score",
            95,
            1,
        )

        history = self.tracer.history()

        self.assertEqual(len(history), 1)

        self.assertEqual(
            history[0]["variable_name"],
            "score"
        )

    def test_delta_tracking(self):

        self.tracer.trace("x", 10, 1)

        self.tracer.trace("x", 20, 2)

        delta = self.tracer.delta_history()

        self.assertEqual(len(delta), 2)

        self.assertEqual(
            delta[1]["old_value"],
            10
        )

        self.assertEqual(
            delta[1]["new_value"],
            20
        )

    def test_multiple_variables(self):

        self.tracer.trace("a", 1, 1)

        self.tracer.trace("b", 2, 2)

        self.tracer.trace("c", 3, 3)

        history = self.tracer.history()

        self.assertEqual(len(history), 3)

    def test_clear(self):

        self.tracer.trace("x", 10, 1)

        self.tracer.clear()

        self.assertEqual(
            len(self.tracer.history()),
            0
        )

        self.assertEqual(
            len(self.tracer.delta_history()),
            0
        )


if __name__ == "__main__":

    unittest.main()