# **Documentation des Modèles et Vues**

## Modèles (`models.py`)

### PokerSession

Un modèle représentant une session de scrum poker.

#### Attributs

- `players` : Nombre de participants à la session.
- `owner` : Utilisateur propriétaire de la session.
- `feature_field_name` : Nom du champ désignant les fonctionnalités.
- `product_backlog` : Backlog produit.
- `product_backlog_file` : Fichier de backlog produit.
- `mode` : Mode de la session.
- `status` : Statut de la session.
- `created_at` : Date de création.
- `result_file` : Fichier de résultat de la session.

#### Méthodes

- `get_result_file` : URL du fichier de résultat.
- `get_result_file_name` : Nom du fichier de résultat.
- `can_start` : Vérifie si la session peut commencer.
- `tours_reverse` : Retourne les tours en ordre inverse.
- `gen_features` : Génère des fonctionnalités à partir du backlog.
- `get_next_feature` : Récupère la prochaine fonctionnalité à voter.
- `get_previous_features` : Récupère les fonctionnalités votées.
- `update_status` : Met à jour le statut de la session.
- `save` : Sauvegarde le modèle.

### Feature

Représente une fonctionnalité dans une session de planning poker.

#### Attributs

- `poker_session` : Session de poker associée.
- `title` : Titre de la fonctionnalité.
- `description` : Description.
- `story_points` : Difficulté estimée.
- `voted` : Indique si un vote a été effectué.

#### Méthodes

- `tours_reverse`, `is_consensus`, `is_completed`, `is_validated`, `is_started`, `check_votes`, `get_next_feature`, `get_previous_features`, `get_last_tour`, `set_next_tour`.

### Participant

Représente un participant à une session de planning poker.

#### Attributs

- `poker_session` : Session de poker associée.
- `user` : Utilisateur participant.

#### Méthodes

- `__str__` : Retourne le nom d'utilisateur du participant.

### Vote

Modèle de vote dans une session de planning poker.

#### Attributs

- `poker_session`, `feature`, `voter`, `vote`, `tour`, `cafe`, `interro`.

#### Méthodes

- `__str__` : Représentation en chaîne du vote.

### Tour

Représente un tour dans une session de planning poker.

#### Attributs

- `poker_session`, `feature`, `designation`.

#### Méthodes

- `save` : Logique métier du tour.

### Messages

Modèle de message dans une session de planning poker.

#### Attributs

- `poker_session`, `sender`, `message`, `created_at`.

#### Méthodes

- `__str__` : Extrait du message.

## Vues (`views.py`)

La documentation des vues est générée automatiquement à partir des docstrings des fonctions et est en anglais pour des raisons d'accèsibilité.

### home

Rendu de la page d'accueil pour l'utilisateur connecté.

```python
@login_required
def home(request):
    """
    Affiche la page d'accueil pour l'utilisateur connecté.

    Paramètres :
        request (HttpRequest) : L'objet de requête HTTP.

    Retourne :
        HttpResponse : La page d'accueil rendue.

    Raise :
        None """
```

### create_session

```python
@require_POST
@login_required
def create_poker_session(request):
    """
    Crée une session de poker.

    Cette fonction est responsable de la création d'une session de poker en fonction des données fournies dans la requête.
    Elle effectue les étapes suivantes :
    1. Valide les données fournies dans la requête.
    2. Si les données sont valides, elle crée une nouvelle session de poker avec l'utilisateur actuel comme propriétaire.
    3. Génère les caractéristiques pour la session de poker créée.
    4. Crée un participant pour l'utilisateur actuel dans la session de poker.
    5. Affiche un message de succès ou d'erreur en utilisant sweetify.toast.
    6. Redirige l'utilisateur vers la page d'accueil.

    Paramètres :
    - request : L'objet de requête HTTP contenant les données pour la création de la session de poker.

    Retourne :
    - Une réponse de redirection vers la page d'accueil.

    Raise :
    - N/A (Non Applicable)
    """

```

### poker_session

```python
def poker_session(request, pk):
    """
    Récupère une session de poker en utilisant la clé primaire fournie et effectue diverses opérations dessus.

    Arguments :
        request : L'objet de requête HTTP.
        pk : La clé primaire de la session de poker à récupérer.

    Retourne :
        Un template HTML rendu avec la session de poker, ses caractéristiques et ses participants.
    """


```

### join_poker_session

```python
@require_POST
def join_poker_session(request):
    """
    Rejoint une session de poker.

    Arguments :
        request (HttpRequest) : L'objet de requête HTTP.

    Retourne :
        HttpResponseRedirect : Une redirection vers la page de la session de poker.
    """


```
