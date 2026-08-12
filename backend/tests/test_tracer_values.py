import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pychronicle.tracer.execution_tracer import _values_equal

class TracerValueTests(unittest.TestCase):
    def test_equal_scalars_compare_true(self):
        self.assertTrue(_values_equal(5, 5))

if __name__ == "__main__":
    unittest.main()
