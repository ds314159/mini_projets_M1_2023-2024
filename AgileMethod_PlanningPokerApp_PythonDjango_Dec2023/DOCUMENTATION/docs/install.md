# **Comment installer Planning Poker**

Pour installer Planning Poker, veuillez suivre les instructions ci-dessous.

## Pré-requis

- Installation de Git : [Git](https://git-scm.com/downloads)
- Installation de Python 3.9.6 : [Python](https://www.python.org/downloads/)

## Installation

1. Cloner le projet sur votre machine locale.

``` bash
git clone https://github.com/ds314159/to_success_project.git
```

2. Créer un environnement virtuel.

``` bash
python -m venv venv
```

3. Activer l'environnement virtuel.

``` bash
source venv/bin/activate
```

4. Installer les dépendances.

``` bash
python -m pip install -r requirements/locale.txt
```

ou

``` bash
python -m pip install -r requirements/production.txt
```

en fonction de l'environnement.

5. Lancer le serveur.

``` bash
python manage.py runserver
```
