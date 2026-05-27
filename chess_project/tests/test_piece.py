# Tests des pieces

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from position import Position
from piece import King, Queen, Bishop, Knight, Rook, Pawn


class TestPieces(unittest.TestCase):
    def test_lettres(self):
        p = Position("a", 1)
        self.assertEqual(str(King(p, 0)), "K")
        self.assertEqual(str(Queen(p, 0)), "Q")
        self.assertEqual(str(Bishop(p, 0)), "B")
        self.assertEqual(str(Knight(p, 0)), "N")
        self.assertEqual(str(Rook(p, 0)), "R")
        self.assertEqual(str(Pawn(p, 0)), "P")

    def test_pion_avance(self):
        pion = Pawn(Position("e", 2), 0)
        self.assertTrue(pion.isValidMove(Position("e", 3), None))
        self.assertFalse(pion.isValidMove(Position("e", 1), None))

    def test_cavalier_en_L(self):
        cav = Knight(Position("b", 1), 0)
        self.assertTrue(cav.isValidMove(Position("c", 3), None))
        self.assertFalse(cav.isValidMove(Position("b", 3), None))

    def test_tour_ligne_droite(self):
        tour = Rook(Position("a", 1), 0)
        self.assertTrue(tour.isValidMove(Position("a", 5), None))
        self.assertFalse(tour.isValidMove(Position("b", 2), None))

    def test_fou_diagonale(self):
        fou = Bishop(Position("c", 1), 0)
        self.assertTrue(fou.isValidMove(Position("a", 3), None))
        self.assertFalse(fou.isValidMove(Position("c", 4), None))

    def test_reine(self):
        reine = Queen(Position("d", 1), 0)
        self.assertTrue(reine.isValidMove(Position("d", 5), None))
        self.assertTrue(reine.isValidMove(Position("h", 5), None))
        self.assertFalse(reine.isValidMove(Position("e", 3), None))

    def test_roi_une_case(self):
        roi = King(Position("e", 1), 0)
        self.assertTrue(roi.isValidMove(Position("e", 2), None))
        self.assertFalse(roi.isValidMove(Position("e", 3), None))


if __name__ == "__main__":
    unittest.main()
