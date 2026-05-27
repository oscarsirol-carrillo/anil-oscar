# Tests de la partie d'echecs

import sys, os, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from chess import Chess
from player import Player
from position import Position
from save_manager import save_game, load_game


class TestChess(unittest.TestCase):
    def setUp(self):
        self.chess = Chess()
        self.chess.players = [Player("Blanc", 0), Player("Noir", 1)]
        self.chess.currentPlayer = self.chess.players[0]

    def test_coup_valide(self):
        self.assertTrue(self.chess.isValidMove("Pe2 Pe4"))

    def test_coup_invalide(self):
        self.assertFalse(self.chess.isValidMove("Pe2 Pe5"))

    def test_jouer_un_coup(self):
        self.chess.updateBoard("Pe2 Pe4")
        self.assertIsNotNone(self.chess.board.getPiece(Position("e", 4)))
        self.assertIsNone(self.chess.board.getPiece(Position("e", 2)))

    def test_switch_player(self):
        ancien = self.chess.currentPlayer
        self.chess.switchPlayer()
        self.assertIsNot(self.chess.currentPlayer, ancien)

    def test_sauvegarde(self):
        self.chess.updateBoard("Pe2 Pe4")
        f = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        f.close()
        try:
            save_game(self.chess, f.name)
            recharge = load_game(f.name)
            self.assertEqual(len(recharge.players), 2)
            self.assertIsNotNone(recharge.board.getPiece(Position("e", 4)))
        finally:
            os.unlink(f.name)


if __name__ == "__main__":
    unittest.main()
