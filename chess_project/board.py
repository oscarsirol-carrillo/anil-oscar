# Classe Board : l'echiquier 8x8

from position import Position
from piece import King, Queen, Bishop, Knight, Rook, Pawn


class Board:
    def __init__(self):
        # le dictionnaire qui stocke les pieces : { Position : Piece }
        self.pieces = {}
        ordre = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i, col in enumerate("abcdefgh"):
            self.pieces[Position(col, 1)] = ordre[i](Position(col, 1), 0)
            self.pieces[Position(col, 2)] = Pawn(Position(col, 2), 0)
            self.pieces[Position(col, 7)] = Pawn(Position(col, 7), 1)
            self.pieces[Position(col, 8)] = ordre[i](Position(col, 8), 1)

    def getPiece(self, position):
        return self.pieces.get(position)

    def getPosition(self, piece):
        for pos, p in self.pieces.items():
            if p is piece:
                return pos
        return None
