# Programme principal

import os
from chess import Chess
from save_manager import load_game


def main():
    print("=== JEU D'ECHECS ===")
    print("1. Nouvelle partie")
    print("2. Charger une partie")
    choix = input("Votre choix : ").strip()

    if choix == "2" and os.path.exists("partie.json"):
        chess = load_game("partie.json")
        print("partie chargee")
    else:
        chess = Chess()

    chess.play()


if __name__ == "__main__":
    main()
