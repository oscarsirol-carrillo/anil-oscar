# Guide de démarrage rapide

> Pour lancer le jeu en moins de 30 secondes.

## Prérequis

- Python 3.10 ou supérieur (vérifier avec `python --version`)
- Aucune bibliothèque externe à installer (uniquement la stdlib)

## Installation

1. Dézipper le projet où vous voulez
2. Ouvrir un terminal dans le dossier `chess_project/`

```bash
cd chess_project
```

## Lancer une partie

```bash
python main.py
```

Au démarrage, le menu apparaît :
```
=========================================
        JEU D'ECHECS - ISEP I1
=========================================
  1. Nouvelle partie
  2. Charger une partie sauvegardee
  3. Quitter
```

Tapez `1` puis entrée pour démarrer une nouvelle partie.

## Saisir les noms

```
=== Initialisation des joueurs ===
Nom du joueur Blanc (ou 'AI' pour ordinateur) : Alice
Nom du joueur Noir (ou 'AI' pour ordinateur) : Bob
```

- Pour jouer contre l'ordinateur, tapez `AI` à la place d'un nom.
- Pour un match IA contre IA, mettre `AI` aux deux.

## Jouer un coup

Format : `<lettre><case_départ> <lettre><case_arrivée>`

Exemples valides au début :
- `Pe2 Pe4` : avance le pion roi de deux cases
- `Pd2 Pd4` : avance le pion dame de deux cases
- `Nb1 Nc3` : sort le cavalier blanc
- `Ng1 Nf3` : sort l'autre cavalier blanc

Lettres des pièces :

| Lettre | Pièce       | Anglais  |
|--------|-------------|----------|
| K      | Roi         | King     |
| Q      | Reine       | Queen    |
| B      | Fou         | Bishop   |
| N      | Cavalier    | kNight   |
| R      | Tour        | Rook     |
| P      | Pion        | Pawn     |

> Le **N** vient de "kNight" car le **K** est déjà pris par le Roi (King).

## Commandes spéciales pendant la partie

| Commande | Action                                |
|----------|---------------------------------------|
| `SAVE`   | Sauvegarder la partie dans un fichier |
| `QUIT`   | Abandonner et quitter                 |

## Lire l'échiquier

```
    a   b   c   d   e   f   g   h
  +---+---+---+---+---+---+---+---+
8 | r | n | b | q | k | b | n | r | 8     <- pièces noires (minuscules)
  +---+---+---+---+---+---+---+---+
7 | p | p | p | p | p | p | p | p | 7     <- pions noirs
  +---+---+---+---+---+---+---+---+
6 |   |   |   |   |   |   |   |   | 6
  +---+---+---+---+---+---+---+---+
5 |   |   |   |   |   |   |   |   | 5
  +---+---+---+---+---+---+---+---+
4 |   |   |   |   |   |   |   |   | 4
  +---+---+---+---+---+---+---+---+
3 |   |   |   |   |   |   |   |   | 3
  +---+---+---+---+---+---+---+---+
2 | P | P | P | P | P | P | P | P | 2     <- pions blancs
  +---+---+---+---+---+---+---+---+
1 | R | N | B | Q | K | B | N | R | 1     <- pièces blanches (majuscules)
  +---+---+---+---+---+---+---+---+
    a   b   c   d   e   f   g   h
```

- **Majuscules** = pièces blanches
- **minuscules** = pièces noires
- Les Blancs commencent toujours.

## Lancer les tests unitaires

```bash
python -m unittest discover -s tests -v
```

Résultat attendu : `Ran 52 tests in 0.0XXs - OK`

## Messages d'erreur courants

| Message                                    | Cause                                         |
|--------------------------------------------|-----------------------------------------------|
| `Coup mal forme`                           | Format incorrect (manque espace, lettre, etc.) |
| `Aucune piece a la case eXY`               | La case de départ est vide                   |
| `La piece en e2 est un P, pas un N`        | Mauvaise lettre de pièce                     |
| `Cette piece appartient a l'adversaire`    | Vous essayez de jouer une pièce ennemie      |
| `Deplacement non conforme aux regles`      | La pièce ne peut pas se déplacer ainsi       |
| `Ce coup laisserait votre Roi en echec`    | Coup interdit qui exposerait votre roi       |

## Mat du berger - démonstration

Pour démontrer rapidement la détection d'échec et mat :

```
Blanc : Pe2 Pe4
Noir  : Pe7 Pe5
Blanc : Bf1 Bc4
Noir  : Nb8 Nc6
Blanc : Qd1 Qh5
Noir  : Ng8 Nf6
Blanc : Qh5 Qf7      <- mat en 4 coups
```

Vous verrez s'afficher : `=== ECHEC ET MAT ! Blanc gagne ! ===`
