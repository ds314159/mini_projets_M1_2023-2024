import json
from django.utils import timezone
from django.db import models

from django.conf import settings

from django.utils.translation import gettext_lazy as _


# Create your models here.
class PokerSession(models.Model):
    """
    Un modèle représentant une session de poker pour la planification et l'estimation agile.

    Attributs :
        SESSION_MODE (enum): Une énumération pour les modes de session, avec les options 'STRICT' et 'MEDIUM'.
        SESSION_STATUS (enum): Une énumération pour les statuts de la session, avec les options 'CREATED', 'STARTED' et 'FINISHED'.
        players (IntegerField): Le nombre de participants à la session.
        owner (ForeignKey): Référence à l'utilisateur propriétaire de la session.
        feature_field_name (CharField): Le nom du champ dans le backlog qui désigne les fonctionnalités.
        product_backlog (TextField): Le backlog produit sous format texte.
        product_backlog_file (FileField): Un champ de téléchargement de fichier pour le backlog produit.
        mode (CharField): Le mode de la session, choisi parmi les options de SESSION_MODE.
        status (CharField): Le statut actuel de la session, choisi parmi les options de SESSION_STATUS.
        created_at (DateTimeField): La date et l'heure de création de la session, définies automatiquement.
        result_file (FileField): Un champ facultatif pour télécharger le fichier de résultat de la session.

    Méthodes :
        get_result_file: Retourne l'URL du fichier de résultat, si disponible.
        get_result_file_name: Retourne le nom du fichier de résultat, si disponible.
        can_start: Vérifie si la session peut commencer en fonction du nombre de participants.
        tours_reverse: Retourne les objets 'tours' associés dans l'ordre inverse.
        gen_features: Génère des objets de fonctionnalité à partir du fichier de backlog produit.
        get_next_feature: Récupère la prochaine fonctionnalité qui n'a pas encore été votée.
        get_previous_features: Récupère les fonctionnalités qui ont déjà été votées.
        update_status: Met à jour le statut de la session en fonction des fonctionnalités restantes.
        save: Méthode save surchargée pour charger le backlog produit à partir d'un fichier avant de sauvegarder.
    """

    class SESSION_MODE(models.TextChoices):
        STRICT = "strict", _("Strict")
        MEDIUM = "medium", _("Moyenne")
        # MEDIAN = "median", _("Median")

    class SESSION_STATUS(models.TextChoices):
        CREATED = "created", _("Créée")
        STARTED = "started", _("Commencée")
        FINISHED = "finished", _("Terminée")

    players = models.IntegerField(default=1, verbose_name="Participants")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="poker_sessions")
    feature_field_name = models.CharField(max_length=50, default="items", verbose_name="Nom du champ des features")
    product_backlog = models.TextField()
    product_backlog_file = models.FileField(upload_to="files", verbose_name="Fichier du backlog")
    mode = models.CharField(max_length=10, choices=SESSION_MODE.choices, default=SESSION_MODE.STRICT)
    status = models.CharField(max_length=10, choices=SESSION_STATUS.choices, default=SESSION_STATUS.CREATED)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    result_file = models.FileField(upload_to="files", verbose_name="Fichier du résultat", null=True, blank=True)

    @property
    def get_result_file(self):
        return self.result_file.url if self.result_file else ""

    @property
    def get_result_file_name(self):
        return self.result_file.name if self.result_file else ""

    @property
    def can_start(self):
        return self.participants.count() == self.players

    def tours_reverse(self):
        return self.tours.all().order_by("-pk")

    def gen_features(self):
        _features = json.load(self.product_backlog_file)
        Feature.objects.bulk_create(
            [
                Feature(
                    poker_session=self,
                    title=item["name"],
                    description=item["description"],
                )
                for item in _features[self.feature_field_name]
            ]
        )
        return _features[self.feature_field_name]

    @property
    def get_next_feature(self):
        return self.features.filter(voted=False).first()

    def get_previous_features(self):
        return self.features.filter(voted=True)

    def update_status(self):
        if self.features.filter(voted=False).exists() and self.get_next_feature:
            self.status = self.SESSION_STATUS.CREATED
        else:
            self.status = self.SESSION_STATUS.FINISHED
        self.save()

    def save(
        self,
        *args,
        **kwargs,
    ):

        self.product_backlog = json.load(self.product_backlog_file)
        super().save(*args, **kwargs)


class Feature(models.Model):
    """
        Un modèle représentant une fonctionnalité (feature) dans une session de poker pour la planification agile.

        Attributs :
            poker_session (ForeignKey): Référence à la session de poker à laquelle appartient cette fonctionnalité.
            title (CharField): Le titre de la fonctionnalité.
            description (TextField): La description de la fonctionnalité.
            story_points (IntegerField): Les points d'histoire estimés pour la fonctionnalité.
            voted (BooleanField): Un indicateur pour savoir si un vote a été effectué pour cette fonctionnalité.

        Méthodes :
            __str__: Retourne le titre de la fonctionnalité.
            tours_reverse: Retourne les objets 'tours' associés dans l'ordre inverse.
            is_consensus: Vérifie s'il y a consensus dans les votes du dernier tour.
            is_completed: Vérifie si tous les participants ont voté pour le dernier tour.
            is_validated: Vérifie si la fonctionnalité est validée (consensus et complétude).
            is_started: Vérifie si au moins un vote a été effectué pour cette fonctionnalité.
            check_votes: Vérifie les votes selon le mode de la session de poker.
            get_next_feature: Récupère la prochaine fonctionnalité non votée dans la session.
            get_previous_features: Récupère les fonctionnalités précédemment votées dans la session.
            get_last_tour: Récupère le dernier tour de votes pour cette fonctionnalité.
            set_next_tour: Crée et sauvegarde un nouveau tour de vote pour cette fonctionnalité.
        """

    poker_session = models.ForeignKey(PokerSession, on_delete=models.CASCADE, related_name="features")
    title = models.CharField(max_length=100)
    description = models.TextField(default="")
    story_points = models.IntegerField(default=0)
    voted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def tours_reverse(self):
        return self.tours.all().order_by("-pk")

    @property
    def is_consensus(self):
        return len(set(self.get_last_tour.votes.values_list("vote", flat=True)) if self.get_last_tour else []) == 1

    # check if all participants have voted
    @property
    def is_completed(self):
        return len(self.get_last_tour.votes.all() if self.get_last_tour else []) == len(
            self.poker_session.participants.all())

    @property
    def is_validated(self):
        return self.is_consensus and self.is_completed

    @property
    def is_started(self):
        return self.votes.all().exists()

    def check_votes(self, mode):
        vote_count = len(self.votes.all()) == len(self.poker_session.participants.all())
        if mode == PokerSession.SESSION_MODE.STRICT:
            return

    def get_next_feature(self):
        return self.poker_session.features.filter(voted=False).first()

    def get_previous_features(self):
        return self.poker_session.features.filter(voted=True)

    @property
    def get_last_tour(self):
        return self.tours.last()

    def set_next_tour(self):
        # breakpoint()
        tour = Tour.objects.create(poker_session=self.poker_session, feature=self,
                                   designation=self.get_last_tour.designation + 1)
        tour.save()
        return tour


class Participant(models.Model):
    """
        Un modèle représentant un participant à une session de poker agile.

        Cette classe crée une relation entre une session de poker (`PokerSession`) et un utilisateur (`user`),
        permettant de suivre quels utilisateurs participent à quelles sessions de poker.

        Attributs :
            poker_session (ForeignKey): Référence à la session de poker à laquelle le participant est lié.
            user (ForeignKey): Référence à l'utilisateur qui est le participant.

        Meta :
            unique_together: Assure qu'une paire (poker_session, user) soit unique dans la base de données,
                             évitant ainsi les doublons de participants dans une même session.

        Méthodes :
            __str__: Retourne le nom d'utilisateur du participant.
        """

    class Meta:
        unique_together = ("poker_session", "user")

    poker_session = models.ForeignKey(PokerSession, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="participants")

    def __str__(self):
        return self.user.username


class Vote(models.Model):
    """
        Un modèle représentant un vote dans une session de poker agile.

        Ce modèle permet de capturer les détails d'un vote effectué par un participant sur une fonctionnalité
        spécifique lors d'un tour donné dans une session de poker.

        Attributs :
            poker_session (ForeignKey): Référence à la session de poker à laquelle le vote est associé.
            feature (ForeignKey): Référence à la fonctionnalité pour laquelle le vote est effectué.
            voter (ForeignKey): Référence au participant qui effectue le vote.
            vote (IntegerField): La valeur du vote.
            tour (ForeignKey): Référence au tour spécifique de la session de poker durant lequel le vote est effectué.
            cafe (BooleanField): Indicateur si le vote est un vote 'café' (pause ou besoin de réflexion supplémentaire).
            interro (BooleanField): Indicateur si le vote est un vote 'interrogation' (incertitude ou question).

        Méthodes :
            __str__: Retourne une représentation en chaîne du vote, typiquement le nom du participant et la valeur du vote.
    """

    poker_session = models.ForeignKey(PokerSession, on_delete=models.CASCADE, related_name="votes")
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name="votes")
    voter = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="votes")
    vote = models.IntegerField()
    tour = models.ForeignKey("Tour", on_delete=models.CASCADE, related_name="votes")
    cafe = models.BooleanField(default=False)
    interro = models.BooleanField(default=False)


class Tour(models.Model):
    """
        Un modèle représentant un tour dans une session de poker agile.

        Ce modèle est utilisé pour suivre les différents tours de votes qui ont lieu pour chaque fonctionnalité
        au sein d'une session de poker. Chaque tour peut avoir plusieurs votes associés à différentes fonctionnalités.

        Attributs :
            poker_session (ForeignKey): Référence à la session de poker à laquelle le tour est associé.
            feature (ForeignKey): Référence à la fonctionnalité pour laquelle le tour est effectué.
            designation (IntegerField): Un numéro de séquence pour le tour, par défaut à 1.

        Méthodes :
            save: Surcharge de la méthode save pour assurer la logique métier spécifique au tour.
    """

    poker_session = models.ForeignKey(PokerSession, on_delete=models.CASCADE, related_name="tours")
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name="tours")
    designation = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        # breakpoint()
        _votes = Vote.objects.filter(tour=self).count()
        if _votes > 0 and _votes != self.poker_session.players:
            return
        self.designation = len(Tour.objects.filter(feature=self.feature).all()) + 1
        return super().save(*args, **kwargs)


class Messages(models.Model):
    """
        Un modèle représentant un message dans une session de poker agile.

        Ce modèle est utilisé pour stocker les messages envoyés par les participants pendant une session de poker.
        Il permet une communication entre les participants dans le contexte de la session.

        Attributs :
            poker_session (ForeignKey): Référence à la session de poker à laquelle le message est associé.
            sender (ForeignKey): Référence au participant qui a envoyé le message.
            message (TextField): Le contenu du message.
            created_at (DateTimeField): La date et l'heure de création du message, définies automatiquement.

        Méthodes :
            __str__: Retourne un extrait du message pour une représentation en chaîne.
    """

    poker_session = models.ForeignKey(PokerSession, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="messages")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
