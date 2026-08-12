import unittest
from pychronicle.tracer.execution_tracer import _values_equal

class TracerValueTests(unittest.TestCase):
    def test_equal_scalars_compare_true(self):
        self.assertTrue(_values_equal(5, 5))

if __name__ == "__main__":
    unittest.main()
