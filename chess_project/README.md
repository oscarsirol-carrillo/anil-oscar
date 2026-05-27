# Jeu d'echecs Python - ISEP I1 (2025/2026)

Implementation en Python d'un jeu d'echecs en mode texte, respectant le
cahier des charges du projet et utilisant l'approche orientee objet vue en cours.

## Documentation

| Document                  | Pour qui ?         | Contenu                                          |
|---------------------------|--------------------|--------------------------------------------------|
| [README.md](README.md)    | Tout le monde      | Vue d'ensemble (ce fichier)                      |
| [GUIDE_DEMARRAGE.md](GUIDE_DEMARRAGE.md) | Utilisateur | Comment installer et jouer en 30 secondes |
| [EXPLICATION_CODE.md](EXPLICATION_CODE.md) | Soutenance | Detail du code fichier par fichier         |
| [SPECIFICATIONS.md](SPECIFICATIONS.md) | Enseignant     | Document de specifications (UML, organisation)  |
| [tests/README.md](tests/README.md) | Developpeur     | Comment lancer et lire les tests                |

## Structure du projet

```
chess_project/
├── position.py          # Classe Position (case de l'echiquier)
├── piece.py             # Classe abstraite Piece + 6 sous-classes
├── board.py             # Classe Board (echiquier 8x8)
├── player.py            # Classes Player et AIPlayer
├── chess.py             # Classe Chess (orchestration de la partie)
├── save_manager.py      # Sauvegarde/restauration JSON
├── main.py              # Programme principal
├── tests/               # Tests unitaires unittest (52 tests)
│   ├── test_position.py
│   ├── test_piece.py
│   ├── test_board.py
│   ├── test_chess.py
│   └── README.md
├── README.md            # Ce fichier
├── GUIDE_DEMARRAGE.md   # Guide d'utilisation rapide
├── EXPLICATION_CODE.md  # Detail du code (soutenance)
├── SPECIFICATIONS.md    # Specifications (livrable seance 2)
└── .gitignore           # Fichiers ignores par Git
```

## Demarrage rapide

```bash
cd chess_project
python main.py
```

Voir [GUIDE_DEMARRAGE.md](GUIDE_DEMARRAGE.md) pour les details.

## Diagramme de classes (UML simplifie)

```
              ┌──────────┐
              │  Piece   │  (abstraite, hérite de ABC)
              ├──────────┤
              │ position │
              │ color    │
              ├──────────┤
              │ isValidMove() ──── méthode abstraite
              │ __str__()     ──── méthode abstraite
              └────┬─────┘
                   │
   ┌──────┬───────┼───────┬───────┬──────┐
   │      │       │       │       │      │
 King   Queen  Bishop  Knight   Rook   Pawn

┌───────┐         ┌───────────┐        ┌────────┐
│ Board │◄───────►│   Chess   │◄──────►│ Player │
├───────┤         ├───────────┤        ├────────┤
│ pieces│         │ board     │        │ name   │
└───────┘         │ players[] │        │ color  │
                  │ currentPlayer       └────┬───┘
                  └───────────┘             ▲
                                            │ (héritage)
                                       ┌────┴─────┐
                                       │ AIPlayer │
                                       └──────────┘
```

## Notions du cours utilisees

| Cours                       | Application dans le projet                                |
|-----------------------------|-----------------------------------------------------------|
| 1. Bases (variables, boucles) | Boucles `for`/`while` dans `play()`, `displayBoard()`   |
| 2. Types composes           | Liste `players`, liste `_history`, dictionnaire `_pieces` |
| 3. Fonctions                | Methodes avec parametres et valeurs par defaut            |
| 4. Exceptions et fichiers   | `try/except`, `with open(...)`, module `json`             |
| 5. POO - Classes            | 9 classes (Position, Piece, 6 pieces, Board, Player...)   |
| 5. POO - Encapsulation      | `@property`, `@setter`, attributs `_proteges`             |
| 5. POO - Heritage           | `AIPlayer(Player)`, `Pawn(Piece)`, `super().__init__()`   |
| 5. POO - Polymorphisme      | `piece.isValidMove(...)` appelle la bonne sous-classe     |
| 5. POO - Classe abstraite   | `Piece(ABC)` + `@abstractmethod`                          |

## Conformite au cahier des charges

| Exigence du sujet                              | Realise |
|------------------------------------------------|---------|
| Classe `Position` avec `column`, `row`, `__str__` | OK   |
| Classe abstraite `Piece`                       | OK      |
| 6 sous-classes : King, Queen, Bishop, Knight, Rook, Pawn | OK |
| Methode `isValidMove(newPosition, board)` pour chaque piece | OK |
| `__str__` retournant K, Q, B, N, R, P          | OK      |
| Classe `Board` avec `getPiece`, `getPosition`, init | OK  |
| Classe `Player` avec `name`, `color`, `askMove` | OK     |
| Classe `AIPlayer` heritant de `Player`         | OK      |
| Classe `Chess` avec `play()`, `initPlayers()`, `displayBoard()`, `isValidMove(move)`, `updateBoard(move)`, `switchPlayer()`, `isCheckMate()` | OK |
| Utilisation d'au moins une liste                | OK (3) |
| Utilisation d'au moins un dictionnaire          | OK (2) |
| Sauvegarde/restauration dans un fichier         | OK (JSON) |
| Tests unitaires (`unittest`)                    | OK (52 tests) |
| Imports entre fichiers (pas de copier-coller)   | OK     |

## Ameliorations implementees (3,5 pts bonus)

1. **Detection complete d'echec et de mat** (au lieu de toujours `False`).
2. **Interdiction des coups qui laisseraient le roi en echec**.
3. **IA jouant des coups legaux** (pas seulement aleatoires).
4. **Affichage des pieces capturees** apres chaque coup.
5. **Sauvegarde JSON versionnee** avec metadonnees completes.

## Lancer les tests unitaires

```bash
python -m unittest discover -s tests -v
```

Resultat attendu : `Ran 52 tests in 0.0XXs - OK`

## Equipe

A completer avec les noms des membres et la repartition des pieces :

| Membre   | Piece implementee | Fichier      |
|----------|-------------------|--------------|
| Membre 1 | Pion (Pawn)       | `piece.py`   |
| Membre 2 | Cavalier (Knight) | `piece.py`   |
| Membre 3 | Fou (Bishop)      | `piece.py`   |
| Membre 4 | Tour/Reine/Roi    | `piece.py`   |

Travail commun : Position, Board, Player, Chess, save_manager, tests, docs.
