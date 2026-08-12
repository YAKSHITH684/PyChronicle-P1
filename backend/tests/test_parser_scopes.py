import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pychronicle.ast_engine.parser import parse_source

class ParserScopeTests(unittest.TestCase):
    def test_function_assignment_keeps_scope(self):
        assignments = parse_source("def work():\n    total = 3\n")
        self.assertEqual(assignments[0].scope, "work")

if __name__ == "__main__":
    unittest.main()
