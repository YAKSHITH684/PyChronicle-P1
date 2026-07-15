"""
Unit tests for parser.py
"""

import unittest

from pychronicle.ast_engine.parser import parse_source


class ParserTests(unittest.TestCase):

    def test_simple_assignment(self):

        source = """

x = 10
y = 20
z = x + y

"""

        result = parse_source(source)

        self.assertEqual(len(result), 3)

        self.assertEqual(result[0].name, "x")

        self.assertEqual(result[1].name, "y")

        self.assertEqual(result[2].name, "z")

    def test_augmented_assignment(self):

        source = """

count = 1
count += 5

"""

        result = parse_source(source)

        self.assertEqual(len(result), 2)

        self.assertTrue(result[1].is_augmented)

    def test_tuple_assignment(self):

        source = """

a, b = (1, 2)

"""

        result = parse_source(source)

        self.assertEqual(len(result), 2)

        self.assertEqual(result[0].name, "a")

        self.assertEqual(result[1].name, "b")

    def test_annotation(self):

        source = """

age: int = 20

"""

        result = parse_source(source)

        self.assertEqual(result[0].annotation, "int")

    def test_scope(self):

        source = """

def demo():

    x = 5

"""

        result = parse_source(source)

        self.assertEqual(result[0].scope, "demo")


if __name__ == "__main__":

    unittest.main()