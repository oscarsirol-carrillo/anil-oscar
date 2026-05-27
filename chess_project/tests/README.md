# Tests unitaires

Tests écrits avec le framework `unittest` (intégré à Python, vu en cours 5).

## Lancer tous les tests

Depuis le dossier `chess_project/` :

```bash
python -m unittest discover -s tests -v
```

Résultat attendu :
```
Ran 52 tests in 0.0XXs

OK
```

## Lancer un seul fichier de tests

```bash
python -m unittest tests.test_position -v
python -m unittest tests.test_piece -v
python -m unittest tests.test_board -v
python -m unittest tests.test_chess -v
```

## Lancer un seul test précis

```bash
python -m unittest tests.test_chess.TestChessEchecEtMat.test_mat_du_berger -v
```

## Couverture des tests

| Fichier         | Tests | Ce qui est vérifié                                  |
|-----------------|-------|-----------------------------------------------------|
| `test_position` | 9     | Création, validation, égalité, hachage, `from_string` |
| `test_piece`    | 18    | Lettres des pièces, déplacements légaux/illégaux des 6 pièces |
| `test_board`    | 12    | Initialisation, getPiece/getPosition, déplacement, capture |
| `test_chess`    | 13    | Parsing, validation des coups, switch player, mat, sauvegarde JSON |
| **Total**       | **52** |                                                    |

## Pourquoi des tests unitaires ?

1. **Détecter les régressions** : si un membre de l'équipe modifie `Pawn`,
   les tests existants détectent immédiatement les casses.
2. **Documentation vivante** : un test montre comment utiliser la classe.
3. **Travail en parallèle** : on peut tester `Position` sans avoir besoin
   du `Board` ni du `Chess` (intégration plus tard).
4. **Confiance** : 52 tests qui passent → la base est solide.

## Tests les plus importants à expliquer en soutenance

### `test_position.test_hashable`

Vérifie qu'on peut utiliser une `Position` comme clé de dictionnaire.
C'est ce qui permet à `Board._pieces` de fonctionner.

### `test_piece.test_cavalier_saute_pieces`

Vérifie que le cavalier sort en `c3` même avec tous les pions devant lui.
Démontre la règle spécifique du cavalier.

### `test_chess.test_mat_du_berger`

Joue 7 coups d'une vraie partie qui se termine par un mat. Vérifie que
`isCheckMate()` retourne bien `True` à la fin. C'est le test le plus
"impressionnant" car il valide presque toute la chaîne logique.

### `test_chess.test_save_and_load`

Joue 2 coups, sauvegarde dans un fichier JSON, recharge, vérifie que
l'état est correctement restauré. Valide la persistance.

## Conventions utilisées

- Chaque classe de test commence par `Test...`
- Chaque méthode de test commence par `test_...`
- `setUp()` est appelée avant chaque test (initialisation fraîche)
- Assertions principales :
  - `assertEqual(a, b)` : vérifie `a == b`
  - `assertTrue(x)` : vérifie que `x` est vrai
  - `assertFalse(x)` : vérifie que `x` est faux
  - `assertIsNone(x)` : vérifie que `x is None`
  - `assertRaises(Erreur)` : vérifie qu'une exception est levée
