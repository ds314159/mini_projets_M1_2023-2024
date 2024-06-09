# Planning Poker

Plannig Poker

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: icom-2024
##
##

## Guide d'installations et de lancement :

### installer les pré-requis et lancer l'application Planning Poker

- Nous commençons dans le repertoire "to_success_project", aller dans le repertoire "planning_poker":


              $ cd planning_poker
- Installer les requirements, et un pré-requis django:


              $ pip install -r requirements/local.txt

              $ pip install django-htmx
- Lancer l'application planning poker:
              
      $ python manage.py runserver 2024
- L'application planning poker devra désormais tourner sur l'adresse http indiquée 
sur votre console (adresse locale + numéro canal de type http://127.0.0.1:2024)


### Installer les pré-requis et lancer le site de la documentation

- Ouvrir une autre fenêtre de terminal,  Nous sommes dans "/to_success_project", allons dans le repertoire "DOCUMENTATION":


              $ cd DOCUMENTATION
- Installer mkdocs, ainsi qu'un thème :

              $ pip install mkdocs
              $ pip install mkdocs-material
- Lancer l'application : site statique de documentation :

              $ mkdocs serve 
- Le site de la documentation devrait désormais tourner sur l'adresse locale par défaut de type http://127.0.0.1:8000

##
##


## Visite guidée et tests des fonctionnalités:

L'application planning poker supporte le jeu à plusieurs, je propose ici un itinéraire guidé optimisé afin de présenter les 
fonctionnalités implémentées et tester le jeu.

### Simuler un jeu à plusieurs :
L'application peut tourner avec un seul joueur si la session créée le stipule, mais cela bridera le jeu car la majorité du 
vote est toujours obtenu dès le premier tour.

Le mieux est de simuler un jeu à deux personnes ( à 3 ou plus c'est possible également mais plus compliqué à tester):

- Ouvrir deux navigateurs différents : exemple, chrome et firefox


- Copier-coller l'URL sur laquelle tourne l'application planning poker dans les deux navigateurs, 
adresse visible dans votre console, de type http://127.0.0.1:2024. La page du site planning poker 
s'affichera sur chaque navigateur.


- Dans l'onglet inscription, créer un compte utilisateur différent sur chaque page, quand le compte sera 
créé vous serez connecté. Dans la présentation qui suit, nous appellerons ces deux joueurs user1 et user2
pour plus de clarté.

- Les deux joueurs peuvent revenir à la page d'accueil en appuyant sur l'onglet Accueil. 
Se déconnecter en appuyant sur l'onglet Déconnexion. 
Se reconnecter en allant sur l'onglet Connexion et en utilisant l'identifiant et mot de passe fournis
lors de la création  du compte.


### Créer une partie de planning poker à partir d'un sprint backlog :

Imaginons que la phase de planification d'un sprint a déjà defini les items d'un backlog de sprint. 
Il reste à estimer l'effort requis pour chaque item, alors le scénario suivant se déroule:

- User1 se connecte, et se met à la page d'accueil.


- User1 appuie sur le bouton vert à gauche "créer une partie", l'interface de création de partie s'affiche.


- User1 choisit le fichier de backlog à estimer. Le notre est un fichier json nommé "backlog_a_valider.json" 
qui est dans le dossier '/to_success_project/backlogs_a_valider/'.


- User1 choisit le mode du jeu : Strict ou Moyenne.



- User1 choisit le nombre de participants, dans notre cas 2. Attention le jeu ne pourra se lancer que si le nombre
de joueurs défini lors de la création correspond aux joueurs qui rejoignent la partie.



- La case "nom du champ des features" est défini par défaut sur "items", cela correspond à la clef des fonctionnalités
dans le fichier json. Elle est à laisser telle quelle  tant que le fichier json n'a pas changé de structure.



- User1 appuie sur créer, une partie est créée, elle est listée mais n'est pas encore lancée. On peut visualiser
ses diverses caractéristiques, dont l'Id. Ce numéro d'identification servira à rejoindre la partie pour les joueurs.



### Rejoindre une partie :

Il est possible de rejoindre des parties qui viennent d'être créées ou des parties entamées et non finalisées.
Le numéro d'identification de la partie sert de référence.

- User1 appuie sur rejoindre une partie, une fenêtre l'invite à préciser l'id de la partie concernée, et à valider.


- User2 appuie sur rejoindre une partie, une fenêtre l'invite à préciser l'id de la partie concernée, et à valider.


- Si l'id de la partie n'existe pas, cela provoque une erreur.


### Jouer :

Quand un joueur valide un id de partie valide, la page de la partie du jeu s'affiche pour lui. 
À noter que la page ne sera interactive et que les cartes ne s'afficheront que quand 
tous les joueurs rejoignent la partie. Penser à rafraichir votre page quand l'autre joueur aura rejoint, 
ça lancera le mode interactif.
Maintenant il est possible de commencer à jouer :

- Les fonctionnalités seront présentées successivement, 
il faut valider l'estimation d'une fonctionnalité pour que la suivante s'affiche.


- Le mode Strict et Moyenne sont implémentés, selon les règles vues en cours.


- À l'interruption du jeu (déconnexion, pause, fermeture navigateur, etc.), la partie est sauvegardée,
il est possible de la reprendre en reprenant la voie "rejoindre une partie" et en reprécisant son identifiant.


- La carte café permet de lancer une pause, en invitant les joueurs à s'exprimer entre eux dans le chat. Le jeu reprend
quand les joueurs se remettent à voter.



- Quand une partie est finalisée, c'est-à-dire que toutes les fonctionnalités ont été votées, 
son fichier json est enregistré dans le dossier to_success_project/planning_poker/planning_poker/media/backlogs.


- Il est toujours possible de consulter une partie finie avec son id, mais il est 
impossible d'en modifier les caractéristiques.

##
##
## Tests :


##
### Tests unitaire:
- Exécuter Automatiquement les tests unitaires 

      $ pytest

### Tests de Type:
- Analyser les fichiers Python dans le dossier planning_poker (et ses sous-dossiers) pour vérifier les annotations de type:

      $ mypy planning_poker

### Obtenir des rapports de couverture des tests :

- Exécuter les tests, vérifier la couverture et générer un rapport de couverture en HTML, attention différence de commande OS/Windows:

Sous Mac OS

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Sous Windows

    $ coverage run -m pytest
    $ coverage html
    $ start htmlcov/index.html








