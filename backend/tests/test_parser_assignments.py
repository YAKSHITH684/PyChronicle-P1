import unittest
from pychronicle.ast_engine.parser import parse_source

class ParserAssignmentTests(unittest.TestCase):
    def test_simple_assignment_is_detected(self):
        assignments = parse_source("value = 42")
        self.assertEqual(assignments[0].name, "value")

if __name__ == "__main__":
    unittest.main()
