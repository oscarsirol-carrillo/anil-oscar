# Document de specifications - Projet Jeu d'echecs

> Document a deposer sur Moodle avant la seance 3 (2 a 4 pages).

## 1. Schema des classes (UML)

### Vue d'ensemble

```
                 +------------+
                 |  Position  |
                 +------------+
                 | _column    |
                 | _row       |
                 +------------+
                 | __str__()  |
                 | from_string() (classmethod)
                 | column_index()
                 +------------+

                       ^
                       | (utilisee par)
                       |
                 +-----+------+
                 |   Piece    | <<abstract>>
                 +------------+
                 | _position  |
                 | _color     |
                 +------------+
                 | isValidMove() <<abstract>>
                 | __str__()     <<abstract>>
                 | _path_is_clear()
                 | _can_land_on()
                 +------------+
                       ^
   _________ _________ | _________ _________
   |       |       |       |       |       |
+---+ +-----+ +------+ +------+ +----+ +----+
|King| |Queen| |Bishop| |Knight| |Rook| |Pawn|
+---+ +-----+ +------+ +------+ +----+ +----+
| str: K  Q       B        N       R     P

                  +----------+
                  |  Board   |
                  +----------+
                  | _pieces : dict{Position: Piece}
                  | _captured : list[Piece]
                  +----------+
                  | getPiece(position)
                  | getPosition(piece)
                  | movePiece(from, to)
                  | findKing(color)
                  +----------+

                  +----------+
                  |  Player  |
                  +----------+
                  | _name    |
                  | _color   |
                  +----------+
                  | askMove(board)
                  +----+-----+
                       ^
                       |
                  +----+-----+
                  | AIPlayer |
                  +----------+
                  | askMove(board) (redefini)
                  +----------+

                  +-----------+
                  |   Chess   |
                  +-----------+
                  | _board : Board
                  | _players : list[Player]
                  | _currentPlayer : Player
                  | _history : list[str]
                  +-----------+
                  | initPlayers()
                  | displayBoard()
                  | isValidMove(move)
                  | updateBoard(move)
                  | switchPlayer()
                  | isCheckMate()
                  | is_in_check(color)
                  | play()
                  +-----------+
```

### Choix de conception

- `Position` est **immuable** : ses attributs sont en lecture seule via `@property`.
  Cela permet de l'utiliser comme cle de dictionnaire (avec `__hash__` et `__eq__`).
- `Piece` est une **classe abstraite** (module `abc`) : on ne peut pas l'instancier
  directement. Chaque sous-classe **doit** implementer `isValidMove` et `__str__`.
- `Board` utilise un **dictionnaire** `{Position : Piece}` plutot qu'une matrice 8x8.
  Avantage : pas de cases `None` a parcourir, acces direct via la cle.
- `AIPlayer` herite de `Player` et **redefinit** seulement `askMove` (polymorphisme).
- `Chess` orchestre la partie et est seul responsable de la **validation globale**
  (echec, echec et mat, format des coups).

## 2. Organisation envisagee

### Repartition des taches

Chaque membre de l'equipe implementera au minimum le deplacement d'une piece :

| Membre | Piece | Tache associee                |
|--------|-------|-------------------------------|
| 1      | Pawn  | Avance + capture diagonale + premiere avancee de 2 cases |
| 2      | Knight| Mouvement en L + saute par-dessus |
| 3      | Bishop| Diagonales + chemin libre        |
| 4      | Rook + Queen + King | Lignes droites + combinaisons |

Le travail commun (Position, Board, Chess, Player, save) sera realise en
sous-equipes de 2 personnes en pair-programming.

### Outils utilises

- **GitHub** pour le partage du code et la traçabilite des modifications
  (`main` proteged, branches `feature/<nom>`).
- **Discord** ou groupe WhatsApp pour la communication rapide.
- **Trello / GitHub Projects** pour le suivi des tâches.
- **Python 3.10+** et **unittest** pour les tests.

### Chef de projet

Un chef de projet **tournant** par seance, charge de :
- verifier que les taches avancent comme prevu ;
- identifier les blocages ;
- relancer ceux qui sont en retard ;
- merger les pull requests sur `main` apres revue d'un autre membre.

### Rythme

| Seance | Objectif                                              |
|--------|-------------------------------------------------------|
| 1      | Analyse, constitution de l'equipe                     |
| 2      | Specifications (ce document), reunion de demarrage    |
| 3      | Implementation des classes communes + tests unitaires |
| 4      | Integration : main.py + Chess.play() fonctionnel      |
| 5      | Code complexe : isCheckMate, AI, isValidMove complet  |
| 6      | Finalisation, chasse aux bugs, revue de code          |
| 7      | Preparation de la soutenance, revue de code           |
| 8      | Soutenance finale                                     |

## 3. Ameliorations envisagees

Pour gagner les 3,5 points d'amelioration, l'equipe vise les ameliorations
suivantes (par ordre de priorite croissant) :

### Priorite 1 - Detection complete d'echec et mat

Le cahier des charges autorise une version simple de `isCheckMate` qui retourne
toujours `False`. Nous implementerons la version complete :
- detection du roi en echec (`is_in_check`) ;
- interdiction des coups qui laisseraient son propre roi en echec ;
- detection du mat : roi en echec + aucun coup legal possible.

### Priorite 2 - IA jouant des coups legaux

Au lieu de generer une chaine aleatoire (qui sera quasi toujours invalide),
notre `AIPlayer` parcourt ses pieces et trouve un coup conforme aux regles
via `piece.isValidMove(...)`. Cela permet de jouer une vraie partie homme/IA.

### Priorite 3 - Deplacements speciaux

Si le temps le permet, ajout d'au moins une regle speciale :
- **Promotion du pion** (la plus simple) : un pion qui atteint la derniere
  rangee est automatiquement transforme en reine.
- **Roque** (plus complexe) : necessite de memoriser si le roi/les tours ont
  deja bouge.

### Priorite 4 - Interface

Possibilite d'ajouter une interface graphique (`tkinter`) si l'avancement le
permet. Le mode texte restera disponible.

### Priorite 5 - Persistance

- Sauvegarde au format **JSON** (vu en cours 5) avec horodatage
- Possibilite de garder un **historique multi-parties** dans un dossier dedie

## 4. Structures de donnees

Conformement au cahier des charges :

- **Liste** : au moins 3 listes utilisees
  - `Chess._players` : les deux joueurs
  - `Chess._history` : historique des coups
  - `Board._captured` : pieces capturees

- **Dictionnaire** : au moins 2 dictionnaires utilises
  - `Board._pieces` : `{Position: Piece}` -> represente l'etat de l'echiquier
  - `save_manager.PIECE_CLASSES` : `{lettre: classe}` -> deserialisation JSON

Chaque membre de l'equipe doit pouvoir expliquer pourquoi ces structures ont
ete choisies et leur comportement (ajout, recherche, suppression, parcours).
