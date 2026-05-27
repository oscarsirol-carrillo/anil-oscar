# Classes Player et AIPlayer

import random


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color   # 0 = blanc, 1 = noir

    def askMove(self):
        couleur = "blanc" if self.color == 0 else "noir"
        return input(self.name + " (" + couleur + ") - votre coup (ex: Pe2 Pe4) : ").strip()


class AIPlayer(Player):
    def askMove(self):
        # genere un coup aleatoire (premiere version comme dit le sujet)
        cols = "abcdefgh"
        depart = random.choice(cols) + str(random.randint(1, 8))
        arrivee = random.choice(cols) + str(random.randint(1, 8))
        lettre = random.choice("KQBNRP")
        return lettre + depart + " " + lettre + arrivee
