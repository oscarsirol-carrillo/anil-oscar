# Explication détaillée du code - Pour la soutenance

> Ce document explique le code fichier par fichier pour permettre à chaque
> membre de l'équipe de comprendre le projet en entier (revue de code individuelle).

## Table des matières

1. [position.py](#1-positionpy) - Représentation d'une case
2. [piece.py](#2-piecepy) - La hiérarchie des pièces
3. [board.py](#3-boardpy) - L'échiquier
4. [player.py](#4-playerpy) - Joueurs humain et IA
5. [chess.py](#5-chesspy) - Le moteur du jeu
6. [save_manager.py](#6-save_managerpy) - Sauvegarde JSON
7. [main.py](#7-mainpy) - Programme principal

---

## 1. `position.py`

### À quoi sert cette classe ?

`Position` représente une case de l'échiquier (par exemple `"e1"` pour la case
du Roi blanc). Elle stocke deux informations :
- `_column` : un caractère entre `'a'` et `'h'`
- `_row` : un entier entre 1 et 8

### Concepts du cours utilisés

- **Encapsulation** : les attributs sont préfixés par `_` (convention "privé").
  L'accès se fait via `@property` (getters), donc on ne peut pas les modifier
  par accident. Vu dans la fiche POO §2.
- **Validation à la création** : le constructeur lève une `ValueError` si
  la colonne ou la rangée est invalide. Vu dans le cours 5 (Exceptions).
- **Méthode spéciale `__str__`** : permet de faire `print(p)` qui affiche `"e1"`.
- **Méthode spéciale `__eq__` et `__hash__`** : permet d'utiliser une `Position`
  comme clé de dictionnaire (essentiel pour `Board`).
- **`@classmethod`** : `from_string("e2")` est un **constructeur alternatif**
  (vu dans la fiche POO §3).

### Question piège possible

> "Pourquoi avoir besoin de `__hash__` ?"
> Réponse : pour pouvoir utiliser une `Position` comme clé dans le
> dictionnaire `_pieces` du `Board`. Python a besoin de hacher la clé.

---

## 2. `piece.py`

### Architecture

Une classe abstraite **`Piece`** et 6 sous-classes concrètes :

```
Piece (ABC)
 ├── King   ("K")
 ├── Queen  ("Q")
 ├── Bishop ("B")
 ├── Knight ("N")
 ├── Rook   ("R")
 └── Pawn   ("P")
```

### Concepts du cours utilisés

- **Classe abstraite** (`from abc import ABC, abstractmethod`).
  `Piece` hérite de `ABC` et ses méthodes `isValidMove` et `__str__` sont
  marquées `@abstractmethod`. **Impossible d'instancier `Piece` directement** :
  on doit créer un `King`, un `Pawn`, etc.
- **Héritage** : chaque sous-classe fait `class King(Piece):`.
- **Polymorphisme** : `piece.isValidMove(pos, board)` appelle automatiquement
  la bonne version (King, Pawn...) selon le type réel de l'objet.
- **Encapsulation** : `_position` et `_color` sont protégés ; accès via
  `@property` ; `position` a un `@setter` qui valide la nouvelle valeur.

### Méthodes protégées partagées

Pour éviter la duplication, deux méthodes utilitaires sont définies dans
`Piece` et utilisées par les sous-classes :

- `_path_is_clear(newPosition, board)` : parcourt les cases entre départ
  et arrivée pour vérifier qu'aucune pièce ne bloque (utilisé par `Queen`,
  `Bishop`, `Rook`). Le `Knight` ne l'utilise pas car il saute.
- `_can_land_on(newPosition, board)` : retourne `True` si la case est vide
  ou contient une pièce adverse.

### Détail du Pion (le plus complexe)

```python
def isValidMove(self, newPosition, board):
    dc = newPosition.column_index() - self._position.column_index()
    dr = newPosition.row - self._position.row
    direction = 1 if self._color == Piece.BLANC else -1
    rangee_initiale = 2 if self._color == Piece.BLANC else 7
    cible = board.getPiece(newPosition)

    if dc == 0:                              # avance tout droit
        if cible is not None:
            return False                     # case occupée
        if dr == direction:
            return True                      # avance d'une case
        if self._position.row == rangee_initiale and dr == 2 * direction:
            intermediaire = Position(self._position.column,
                                      self._position.row + direction)
            if board.getPiece(intermediaire) is None:
                return True                  # avance de deux cases initial
        return False

    if abs(dc) == 1 and dr == direction:     # capture diagonale
        if cible is not None and cible.color != self._color:
            return True
    return False
```

Trois règles à retenir pour le pion :
1. Avance tout droit d'**une** case si la case est vide.
2. Avance de **deux** cases depuis sa position initiale (rangée 2 pour blanc, 7 pour noir).
3. Capture en **diagonale** uniquement.

### Détail du Cavalier (le plus particulier)

Le cavalier est la seule pièce qui peut **sauter** par-dessus les autres.
Il se déplace en "L" : 2 cases dans une direction + 1 case perpendiculaire.

```python
if not ((dc == 2 and dr == 1) or (dc == 1 and dr == 2)):
    return False
```

C'est pour ça qu'on n'appelle **pas** `_path_is_clear` pour le cavalier.

---

## 3. `board.py`

### À quoi sert cette classe ?

`Board` représente l'échiquier. Au lieu d'utiliser une matrice 8×8 (liste
de listes), on utilise un **dictionnaire** :

```python
self._pieces = { Position("a", 1): Rook(...), Position("b", 1): Knight(...), ... }
```

### Pourquoi un dictionnaire ?

- **Accès direct** en O(1) : `board.getPiece(Position("e", 4))` est immédiat.
- **Pas de gaspillage** : on ne stocke que les cases occupées (max 32 sur 64).
- **Parcours facile** des pièces présentes via `.values()`.

C'est le **dictionnaire requis** par le cahier des charges.

### Listes utilisées

- `_captured` : pièces capturées au fil de la partie.
  C'est l'une des **listes requises** par le cahier des charges.

### Méthodes principales

- `getPiece(position)` : retourne la pièce ou `None`.
- `getPosition(piece)` : retourne la position ou `None` (pièce capturée).
- `movePiece(from_pos, to_pos)` : déplace et retourne la pièce capturée éventuelle.
- `findKing(color)` : trouve le roi (utile pour la détection d'échec).

---

## 4. `player.py`

### Hiérarchie

```
Player
 └── AIPlayer (hérite et redéfinit askMove)
```

### Concepts du cours utilisés

- **Héritage simple** : `class AIPlayer(Player):`.
- **Appel du constructeur parent** : `super().__init__(name, color)`.
- **Polymorphisme** : `askMove(board)` a deux comportements différents
  selon que c'est un humain ou une IA, mais on l'appelle de la même façon.

### Comment l'IA joue ?

```python
def askMove(self, board):
    mes_pieces = board.getAllPieces(self._color)
    random.shuffle(mes_pieces)
    for piece in mes_pieces:
        cases = [(c, r) for c in "abcdefgh" for r in range(1, 9)]
        random.shuffle(cases)
        for col, row in cases:
            new_pos = Position(col, row)
            if piece.isValidMove(new_pos, board):
                return f"{piece}{piece.position} {piece}{new_pos}"
    return "QUIT"
```

L'IA :
1. Récupère toutes ses pièces (filtrées par couleur).
2. Mélange l'ordre pour ne pas être prévisible.
3. Pour chaque pièce, essaie aléatoirement toutes les cases.
4. Dès qu'elle trouve un coup conforme aux règles, elle le joue.

---

## 5. `chess.py`

C'est la classe **chef d'orchestre**. Elle a 3 attributs :

```python
self._board = Board()                   # l'échiquier
self._players = []                      # la liste des joueurs (REQUISE)
self._currentPlayer = None              # qui joue maintenant
self._history = []                      # historique des coups (autre liste)
```

### Boucle principale : `play()`

Implémentation conforme au pseudo-code du sujet :

```
Initialisation des joueurs
Tant qu'il n'y a pas d'echec et mat :
    Afficher l'etat courant du plateau de jeu
    Tant que le mouvement n'est pas valide :
        Demander au joueur courant de bouger une piece
    Mettre a jour l'echiquier avec le mouvement valide
    Basculer vers l'autre joueur
```

### Détection d'échec et de mat (amélioration)

```python
def is_in_check(self, color):
    roi = self._board.findKing(color)
    adversaire = Piece.NOIR if color == Piece.BLANC else Piece.BLANC
    return self._is_square_attacked(roi.position, adversaire)

def isCheckMate(self):
    couleur = self._currentPlayer.color
    if not self.is_in_check(couleur):
        return False                        # pas en échec donc pas mat
    # Pour chaque pièce, on cherche un coup qui sort de l'échec
    for piece in self._board.getAllPieces(couleur):
        for col in "abcdefgh":
            for row in range(1, 9):
                cible = Position(col, row)
                if piece.isValidMove(cible, self._board):
                    if not self._move_leaves_king_in_check(piece, piece.position, cible):
                        return False        # un coup sauve le roi
    return True                             # aucun coup ne sauve = mat
```

L'astuce : `_move_leaves_king_in_check` **simule** le coup, vérifie si le roi
serait en échec, puis **annule** le coup. Cela évite de modifier l'état réel.

### Parsing des coups

`_parse_move("Pe2 Pe4")` découpe :
- `"Pe2"` → lettre `'P'`, position `e2`
- `"Pe4"` → lettre `'P'`, position `e4`

Les **exceptions** sont utilisées (cours 5) pour signaler les formats invalides.

---

## 6. `save_manager.py`

### Format JSON utilisé (cours 5)

```json
{
  "version": "1.0",
  "players": [
    {"name": "Alice", "color": 0, "is_ai": false},
    {"name": "Bob",   "color": 1, "is_ai": false}
  ],
  "currentPlayerIndex": 0,
  "pieces": [
    {"type": "R", "color": 0, "position": "a1"},
    {"type": "P", "color": 0, "position": "e4"},
    ...
  ],
  "captured": [],
  "history": ["Pe2 Pe4", "Pe7 Pe5"]
}
```

### Pourquoi JSON et pas CSV ?

- Les pièces ne sont pas un simple tableau : on a un dictionnaire imbriqué.
- JSON gère naturellement les structures composées (listes ET dicts).
- Plus lisible quand on ouvre le fichier dans un éditeur.

### Le dictionnaire `PIECE_CLASSES`

```python
PIECE_CLASSES = {
    "K": King, "Q": Queen, "B": Bishop,
    "N": Knight, "R": Rook, "P": Pawn,
}
```

Permet de retrouver la classe Python à partir de la lettre stockée dans le JSON.
C'est le **second dictionnaire** du projet.

---

## 7. `main.py`

Point d'entrée du programme. Affiche un menu, propose nouvelle partie ou
chargement, puis appelle `chess.play()`.

Les **exceptions** sont attrapées pour gérer proprement :
- `KeyboardInterrupt` : Ctrl+C de l'utilisateur
- `OSError`, `KeyError`, `ValueError` : fichier de sauvegarde invalide

---

## Questions classiques de la soutenance

### "Pourquoi une classe abstraite ?"

Parce que `Piece` ne représente pas une pièce concrète : on ne peut pas
poser "une pièce" sur le plateau, c'est forcément un roi, un pion, etc.
`@abstractmethod` **force** chaque sous-classe à implémenter `isValidMove`,
sinon Python refuse de créer l'objet.

### "Comment fonctionne le polymorphisme ici ?"

Dans `Chess.isValidMove`, on appelle simplement :
```python
piece.isValidMove(pos_a, self._board)
```
Sans savoir si `piece` est un `Pawn`, un `Knight` ou autre. Python choisit
automatiquement la méthode `isValidMove` de la **classe réelle** de l'objet.
C'est ce qui évite des dizaines de `if/elif` dans `Chess`.

### "Comment garantit-on l'immutabilité d'une Position ?"

- Pas de `@setter` sur `column` ni `row`.
- Attributs préfixés par `_` (convention).
- Pas de méthode qui modifie l'instance.

### "Pourquoi le dictionnaire `_pieces` au lieu d'une matrice 8x8 ?"

Trois raisons :
1. **Performance** : accès en O(1) au lieu de calculer l'index.
2. **Lisibilité** : `board.getPiece(Position("e", 4))` est plus clair que `board[3][4]`.
3. **Mémoire** : on ne stocke que les cases occupées.

### "Comment teste-t-on un mat ?"

Voir `tests/test_chess.py` : on joue la séquence du **mat du berger** :
```
Pe2 Pe4, Pe7 Pe5, Bf1 Bc4, Nb8 Nc6, Qd1 Qh5, Ng8 Nf6, Qh5 Qf7
```
Puis on vérifie `chess.isCheckMate() == True`.

### "Comment gère-t-on un coup qui mettrait son propre roi en échec ?"

Méthode `_move_leaves_king_in_check` :
1. On applique le coup temporairement.
2. On vérifie si notre roi est en échec.
3. On annule le coup.
4. Si oui → coup interdit, on ne le joue pas.

### "Pourquoi avoir séparé le code en plusieurs fichiers ?"

- **Lisibilité** : un fichier = une responsabilité.
- **Travail d'équipe** : moins de conflits Git si chacun travaille sur un fichier.
- **Tests** : on peut tester `position.py` indépendamment de `chess.py`.
- C'est ce que recommande le cours (rappel : importer plutôt que copier-coller).
