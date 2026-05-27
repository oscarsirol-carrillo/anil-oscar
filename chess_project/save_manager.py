# Sauvegarde et restauration de la partie dans un fichier JSON

import json
from position import Position
from piece import King, Queen, Bishop, Knight, Rook, Pawn
from player import Player, AIPlayer

# dictionnaire qui associe la lettre a la classe
CLASSES = {"K": King, "Q": Queen, "B": Bishop, "N": Knight, "R": Rook, "P": Pawn}


def save_game(chess, filename):
    data = {
        "players": [[p.name, p.color, isinstance(p, AIPlayer)] for p in chess.players],
        "current": chess.players.index(chess.currentPlayer),
        "pieces": [[str(p), p.color, str(pos)] for pos, p in chess.board.pieces.items()],
    }
    with open(filename, "w") as f:
        json.dump(data, f)


def load_game(filename):
    from chess import Chess
    with open(filename, "r") as f:
        data = json.load(f)
    chess = Chess()
    chess.players = []
    for nom, color, is_ai in data["players"]:
        chess.players.append(AIPlayer(nom, color) if is_ai else Player(nom, color))
    chess.currentPlayer = chess.players[data["current"]]
    chess.board.pieces = {}
    for lettre, color, pos_str in data["pieces"]:
        pos = Position(pos_str[0], int(pos_str[1]))
        chess.board.pieces[pos] = CLASSES[lettre](pos, color)
    return chess
