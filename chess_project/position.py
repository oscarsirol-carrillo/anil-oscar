# Classe Position : une case de l'echiquier (ex: "e2")


class Position:
    def __init__(self, column, row):
        self.column = column  # une lettre de "a" a "h"
        self.row = row        # un entier de 1 a 8

    def __str__(self):
        return self.column + str(self.row)

    def __eq__(self, other):
        return self.column == other.column and self.row == other.row

    def __hash__(self):
        # necessaire pour utiliser Position comme cle de dictionnaire
        return hash((self.column, self.row))
