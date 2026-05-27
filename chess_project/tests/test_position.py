# Tests de la classe Position

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from position import Position


class TestPosition(unittest.TestCase):
    def test_creation(self):
        p = Position("e", 1)
        self.assertEqual(p.column, "e")
        self.assertEqual(p.row, 1)

    def test_str(self):
        self.assertEqual(str(Position("e", 1)), "e1")

    def test_egalite(self):
        self.assertEqual(Position("a", 1), Position("a", 1))
        self.assertNotEqual(Position("a", 1), Position("a", 2))

    def test_hashable(self):
        d = {Position("a", 1): "tour"}
        self.assertEqual(d[Position("a", 1)], "tour")


if __name__ == "__main__":
    unittest.main()
