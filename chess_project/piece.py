# Les pieces du jeu : une classe mere Piece et 6 sous-classes


class Piece:
    def __init__(self, position, color):
        self.position = position
        self.color = color   # 0 = blanc, 1 = noir

    def isValidMove(self, newPosition, board):
        # methode redefinie dans chaque sous-classe
        return True

    def __str__(self):
        return "?"


class King(Piece):
    def isValidMove(self, newPosition, board):
        dc = abs(ord(newPosition.column) - ord(self.position.column))
        dr = abs(newPosition.row - self.position.row)
        return (dc + dr > 0) and dc <= 1 and dr <= 1

    def __str__(self):
        return "K"


class Queen(Piece):
    def isValidMove(self, newPosition, board):
        dc = abs(ord(newPosition.column) - ord(self.position.column))
        dr = abs(newPosition.row - self.position.row)
        return (dc == 0 or dr == 0 or dc == dr) and (dc + dr > 0)

    def __str__(self):
        return "Q"


class Bishop(Piece):
    def isValidMove(self, newPosition, board):
        dc = abs(ord(newPosition.column) - ord(self.position.column))
        dr = abs(newPosition.row - self.position.row)
        return dc == dr and dc > 0

    def __str__(self):
        return "B"


class Knight(Piece):
    def isValidMove(self, newPosition, board):
        dc = abs(ord(newPosition.column) - ord(self.position.column))
        dr = abs(newPosition.row - self.position.row)
        return (dc == 1 and dr == 2) or (dc == 2 and dr == 1)

    def __str__(self):
        return "N"


class Rook(Piece):
    def isValidMove(self, newPosition, board):
        meme_col = newPosition.column == self.position.column
        meme_row = newPosition.row == self.position.row
        return meme_col != meme_row  # exactement un des deux

    def __str__(self):
        return "R"


class Pawn(Piece):
    def isValidMove(self, newPosition, board):
        direction = 1 if self.color == 0 else -1
        rangee_init = 2 if self.color == 0 else 7
        if newPosition.column != self.position.column:
            return False
        delta = newPosition.row - self.position.row
        # avance d'une case, ou de deux cases depuis la position initiale
        return delta == direction or (delta == 2 * direction
                                       and self.position.row == rangee_init)

    def __str__(self):
        return "P"
