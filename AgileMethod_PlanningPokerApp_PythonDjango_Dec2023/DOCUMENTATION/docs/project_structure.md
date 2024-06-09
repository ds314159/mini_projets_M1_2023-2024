# **Structure du Projet**

Le projet "Planning Poker" est une application organisée de manière à faciliter la compréhension, la maintenance et l'évolution du code. Voici la structure détaillée du projet :

### Fichiers et dossiers à la racine

- **`README.md`** : Fournit un aperçu du projet, des instructions d'installation et d'utilisation.
- **`LICENSE`** : Détaille la licence sous laquelle le projet est distribué.
- **`CONTRIBUTORS.txt`** : Liste des personnes ayant contribué au projet.
- **`manage.py`** : Script utilitaire pour gérer diverses tâches du projet, typique des applications Django.
- **`db.sqlite3`** : La base de données du projet.
- **`pyproject.toml, setup.cfg`** : Fichiers de configuration pour la gestion des dépendances et du projet.
- **`requirements`** : Dossier contenant les fichiers de dépendances Python nécessaires au projet.
- **`config`** : Dossier contenant les fichiers de configuration du projet.
- **`planning_poker`** : Dossier principal contenant le code et la logique métier.
- **`utility`** :   Dossier contenant des scripts ou des utilitaires supplémentaires pour le projet.

- **`locale`** : Dossiers pour les fichiers de localisation, permettant la prise en charge de plusieurs langues.

- **`.editorconfig , .gitattributes , .gitignore , requirements.txt`** : Fichiers de configuration de l'environnement de travail.

## Sous-dossier `planning_poker`

Cette documentation décrit la structure du sous-dossier `planning_poker`, qui fait partie intégrante du projet "Planning Poker".

### Structure Générale

Le sous-dossier suit une structure typique d'une application web, basée sur le framework Django .

#### Fichiers Racine

- **`__init__.py`**: Indique que le dossier est un package Python.
- **`conftest.py`**: Fichier de configuration pour les tests avec pytest.

#### Dossiers de l'Application

1. **`contrib`**: Contient des modules ou packages complémentaires au projet.
2. **`core`**: Le cœur de l'application, incluant la logique métier principale et les modèles.
3. **`users`**: Gère tout ce qui est relatif aux utilisateurs de l'application.
4. **`utils`**: Fonctions utilitaires et helpers utilisés à travers l'application.

#### Ressources et Fichiers Statiques

1. **`media`**: Dossier pour les fichiers médias uploadés ou utilisés dans l'application.

2. **`media/files`**: Dossier pour les backlogs uploadé par les utilisateurs.
3. **`media/backlogs`**: Dossier pour le résultat des backlogs en JSON à chaque fin de partie.
4. **`static`**: Contient les fichiers statiques comme les CSS, JavaScript, et images.
3. **`templates`**: Templates HTML pour la génération des pages web.

#### Dossiers de Cache

- `__pycache__`:
  - Fichiers Python compilés pour améliorer les performances de chargement.
