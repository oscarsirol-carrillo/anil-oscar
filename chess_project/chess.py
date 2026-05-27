# Classe Chess : gere la partie

from board import Board
from player import Player, AIPlayer
from position import Position


class Chess:
    def __init__(self):
        self.board = Board()
        self.players = []        # la liste de 2 joueurs
        self.currentPlayer = None

    def initPlayers(self):
        nom1 = input("Nom joueur blanc (ou 'AI') : ").strip() or "Blanc"
        nom2 = input("Nom joueur noir (ou 'AI') : ").strip() or "Noir"
        j1 = AIPlayer(nom1, 0) if nom1 == "AI" else Player(nom1, 0)
        j2 = AIPlayer(nom2, 1) if nom2 == "AI" else Player(nom2, 1)
        self.players = [j1, j2]
        self.currentPlayer = j1

    def displayBoard(self):
        for row in range(8, 0, -1):
            ligne = str(row) + " "
            for col in "abcdefgh":
                p = self.board.getPiece(Position(col, row))
                if p is None:
                    ligne += ". "
                elif p.color == 0:
                    ligne += str(p) + " "
                else:
                    ligne += str(p).lower() + " "
            print(ligne)
        print("  a b c d e f g h")

    def isValidMove(self, move):
        try:
            d, a = move.split()
            from_pos = Position(d[1], int(d[2]))
            to_pos = Position(a[1], int(a[2]))
            piece = self.board.getPiece(from_pos)
            if piece is None or piece.color != self.currentPlayer.color:
                return False
            cible = self.board.getPiece(to_pos)
            if cible is not None and cible.color == self.currentPlayer.color:
                return False
            return piece.isValidMove(to_pos, self.board)
        except (ValueError, IndexError):
            return False

    def updateBoard(self, move):
        d, a = move.split()
        from_pos = Position(d[1], int(d[2]))
        to_pos = Position(a[1], int(a[2]))
        piece = self.board.pieces.pop(from_pos)
        self.board.pieces[to_pos] = piece
        piece.position = to_pos

    def switchPlayer(self):
        i = self.players.index(self.currentPlayer)
        self.currentPlayer = self.players[1 - i]

    def isCheckMate(self):
        # premiere version : retourne toujours False
        return False

    def play(self):
        self.initPlayers()
        while not self.isCheckMate():
            self.displayBoard()
            move = self.currentPlayer.askMove()
            if move == "QUIT":
                return
            if move == "SAVE":
                from save_manager import save_game
                save_game(self, "partie.json")
                print("partie sauvegardee")
                continue
            if self.isValidMove(move):
                self.updateBoard(move)
                self.switchPlayer()
            else:
                print("coup invalide")
