import unittest
from pychronicle.ast_engine.parser import parse_source

class ParserAugmentedTests(unittest.TestCase):
    def test_augmented_assignment_is_marked(self):
        assignments = parse_source("count = 1\ncount += 2")
        self.assertTrue(assignments[-1].is_augmented)

if __name__ == "__main__":
    unittest.main()
