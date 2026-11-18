# TP — Qualité du code et tests unitaires (SonarQube + pytest)

Module : Déploiement des Systèmes Intelligents
Projet SonarQube Cloud : **Credit Quality** (`HAMZA-eELATIFI_DEPLOIMENT-APP-INTELLEGENT-SONAR-QUBE-TP-2`)

## Structure du projet

```
.
├── credit.py                  # code corrigé
├── sonar-project.properties   # configuration SonarScanner
├── pytest.ini                 # configuration pytest
└── tests/
    └── test_credit.py         # tests unitaires
```

---

## Exercice 1 — Analyse de la qualité avec SonarQube

### Outils
- **SonarQube Cloud** : analyse centralisée (profil Python *Sonar way comprehensive*)
- **SonarScanner CLI 8.4** : lancement de l'analyse
- **SonarQube for IDE** : analyse dans VS Code (mode connecté)

### Problèmes du code initial

| Problème | Ligne(s) | Détecté par SonarCloud ? |
|---|---|---|
| Paramètre `age` inutilisé (python:S1172) | 5, 19 | ✅ Oui (Code Smell, Major) |
| Imports `os` et `math` inutilisés | 1, 2 | ❌ Non (règle absente du profil) |
| Fonction `calculate_risk2` copie exacte de `calculate_risk` | 19-30 | ❌ Non (bloc sous le seuil de duplication) |
| `else` inutile après `return`, seuils « magiques » 0.6 / 0.3 | 11-16 | ❌ Non |

> Avec le profil par défaut *Sonar way core*, SonarCloud n'a détecté **aucun** problème.
> Il a fallu passer au profil *Sonar way comprehensive* pour voir les 2 Code Smells.
> **0 problème ne signifie pas que le code est parfait** : seules les règles actives sont vérifiées.

### Corrections apportées
1. Suppression des imports inutilisés `os` et `math`.
2. Suppression du paramètre inutilisé `age`.
3. Suppression de la fonction dupliquée `calculate_risk2`.
4. Remplacement des valeurs 0.6 / 0.3 par des constantes nommées.
5. Suppression des `elif` / `else` inutiles après `return`.
6. Ajout d'une docstring.
7. Envoi du rapport de couverture pytest à SonarCloud (`coverage.xml`).

### Tableau de comparaison

| Indicateur | Avant | Après |
|---|---|---|
| Problèmes de fiabilité | 0 (A) | 0 (A) |
| Problèmes de sécurité | 0 (A) | 0 (A) |
| Problèmes de maintenabilité | 2 (A) | **0 (A)** |
| Duplication | 0,0 % | 0,0 % |
| Couverture | 0,0 % | **100 %** |
| Lignes de code | 22 | 11 |
| Quality Gate | Passed | **Passed** ✅ |

### Réponses aux questions

**1. Quelle différence existe-t-il entre un Bug et un Code Smell ?**
Un **Bug** est une erreur qui provoque (ou provoquera) un comportement incorrect à l'exécution : division par zéro, variable non définie, condition toujours fausse… Un **Code Smell** est un défaut de conception ou de lisibilité : le programme fonctionne, mais le code est plus difficile à comprendre, à modifier et à maintenir (code dupliqué, paramètre inutilisé, fonction trop longue…). Le bug concerne la **fiabilité**, le Code Smell la **maintenabilité**.

**2. Pourquoi la duplication du code augmente-t-elle les coûts de maintenance ?**
Chaque modification (correction de bug, changement de règle métier) doit être répétée dans toutes les copies. Il est facile d'en oublier une, ce qui crée des comportements incohérents. Le code est aussi plus long à lire, à tester et à relire. Ici, changer le seuil 0.6 aurait demandé deux modifications au lieu d'une.

**3. Quel est le rôle du Quality Gate ?**
C'est un ensemble de conditions (pas de nouveau bug, couverture minimale, duplication maximale…) qui donne un verdict **Passed / Failed** sur le projet. Il sert de « barrière » : dans une chaîne CI/CD, un Quality Gate en échec peut bloquer la fusion ou le déploiement d'un code de mauvaise qualité.

**4. Quelle différence existe-t-il entre SonarScanner CLI et SonarQube for IDE ?**
- **SonarScanner CLI** analyse **tout le projet** et envoie les résultats au serveur SonarQube Cloud : historique, métriques, Quality Gate, partage avec l'équipe. Il est utilisé manuellement ou dans la CI.
- **SonarQube for IDE** analyse **en temps réel** le fichier ouvert dans l'éditeur, pendant l'écriture du code, sans rien envoyer. Il donne un retour immédiat au développeur. En mode connecté, il utilise les mêmes règles que le projet Cloud.

**5. Pourquoi faut-il relancer l'analyse après correction ?**
Pour **vérifier** que les corrections suppriment bien les problèmes sans en introduire de nouveaux, mettre à jour les métriques et le Quality Gate sur SonarCloud, et garder une trace de l'évolution de la qualité (comparaison avant / après).

---

## Exercice 2 — Tests unitaires avec pytest

### Installation et exécution

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install pytest pytest-cov
python -m pytest -v
python -m pytest --cov=credit --cov-report=term-missing
python -m pytest --cov=credit --cov-report=html   # rapport dans htmlcov/index.html
```

### Tests réalisés (8 tests, tous PASSED)

| Partie | Test | Entrée (revenu, dette) | Attendu |
|---|---|---|---|
| A | `test_high_risk` | 1000, 700 | HIGH |
| A | `test_medium_risk` | 1000, 400 | MEDIUM |
| A | `test_low_risk` | 1000, 100 | LOW |
| B | `test_income_zero` | 0, 500 | -1 |
| B | `test_income_negative` | -1000, 500 | -1 |
| B | `test_debt_zero` | 1000, 0 | LOW |
| B | `test_ratio_exactly_0_3` | 1000, 300 | LOW |
| B | `test_ratio_exactly_0_6` | 1000, 600 | MEDIUM |

> Après suppression du paramètre `age` (inutilisé), les appels passent de `calculate_risk(1000, 700, 30)` à `calculate_risk(1000, 700)`.

### Partie C — Détection d'erreurs

En remplaçant `if ratio > 0.6:` par `if ratio > 0.8:` :

```
FAILED tests/test_credit.py::test_high_risk - AssertionError: assert 'MEDIUM' == 'HIGH'
1 failed, 7 passed
```

1. **Test qui échoue** : `test_high_risk`.
2. **Pourquoi** : le ratio vaut 700 / 1000 = 0,7. Avec le seuil 0,8, la condition `0.7 > 0.8` est fausse, donc la fonction retourne `MEDIUM` au lieu de `HIGH`. Les autres tests passent encore car leurs ratios (0,4 ; 0,1 ; 0,3 ; 0,6…) donnent le même résultat avec les deux seuils. Cela montre l'intérêt d'avoir des tests proches des seuils.
3. **Correction** : remise de la condition à `0.6`.
4. **Relance** : 8 tests PASSED.

### Couverture

| | Avant correction | Après correction |
|---|---|---|
| Couverture | 60 % (lignes 20-30 non couvertes : `calculate_risk2` jamais appelée) | **100 %** |

### Réponses aux questions

**1. Quel est le rôle de l'instruction `assert` ?**
Elle vérifie qu'une condition est vraie (par exemple `result == "HIGH"`). Si elle est fausse, elle lève une `AssertionError` et pytest marque le test comme échoué, en affichant la valeur obtenue et la valeur attendue.

**2. Quelle différence existe-t-il entre PASS et FAIL ?**
**PASS** : toutes les assertions du test sont vraies, le résultat obtenu correspond au résultat attendu. **FAIL** : au moins une assertion est fausse (ou une exception inattendue est levée), le comportement du code ne correspond pas à ce qui est attendu.

**3. Pourquoi faut-il tester les valeurs limites ?**
Les erreurs se cachent souvent aux frontières : `>` au lieu de `>=`, division par zéro, valeur négative… Tester exactement 0,3 et 0,6, ou un revenu nul, vérifie que le comportement aux seuils est bien celui voulu et protège contre les régressions.

**4. Une couverture de 100 % garantit-elle l'absence de bugs ?**
**Non.** La couverture indique seulement que chaque ligne a été **exécutée**, pas qu'elle a été **vérifiée** correctement. Un test sans assertion pertinente, un cas oublié (ex. dette négative) ou une erreur de spécification peuvent laisser passer des bugs même à 100 %.

**5. Quelle différence existe-t-il entre pytest et SonarQube ?**
- **pytest** fait de l'**analyse dynamique** : il **exécute** le code et vérifie que les résultats sont corrects (comportement fonctionnel).
- **SonarQube** fait de l'**analyse statique** : il **lit** le code sans l'exécuter et détecte les bugs potentiels, Code Smells, failles de sécurité et duplications (qualité du code).

Les deux sont complémentaires : SonarQube peut d'ailleurs afficher la couverture mesurée par pytest.

---

## Captures d'écran

À ajouter dans le dossier `captures/` :
- SonarCloud avant correction
- SonarCloud après correction
- Problèmes dans VS Code (SonarQube for IDE)
- Exécution des tests pytest
- Rapport de couverture (`htmlcov/index.html`)
