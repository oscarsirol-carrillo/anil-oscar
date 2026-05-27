# Tests de l'echiquier

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from board import Board
from position import Position
from piece import King, Pawn


class TestBoard(unittest.TestCase):
    def test_nombre_pieces(self):
        b = Board()
        self.assertEqual(len(b.pieces), 32)

    def test_pion_en_e2(self):
        b = Board()
        self.assertIsInstance(b.getPiece(Position("e", 2)), Pawn)

    def test_roi_en_e1(self):
        b = Board()
        self.assertIsInstance(b.getPiece(Position("e", 1)), King)

    def test_case_vide(self):
        b = Board()
        self.assertIsNone(b.getPiece(Position("e", 4)))

    def test_get_position(self):
        b = Board()
        roi = b.getPiece(Position("e", 1))
        self.assertEqual(b.getPosition(roi), Position("e", 1))


if __name__ == "__main__":
    unittest.main()
