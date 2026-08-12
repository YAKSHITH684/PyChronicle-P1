import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pychronicle.ast_engine.parser import parse_source

class ParserAnnotationTests(unittest.TestCase):
    def test_annotation_is_preserved(self):
        assignments = parse_source("name: str = 'py'")
        self.assertEqual(assignments[0].annotation, "str")

if __name__ == "__main__":
    unittest.main()
