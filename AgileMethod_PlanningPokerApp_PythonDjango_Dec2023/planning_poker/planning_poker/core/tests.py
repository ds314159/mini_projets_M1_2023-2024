from django.test import TestCase, Client
from django.urls import reverse
from planning_poker.users.models import User
from planning_poker.core.models import PokerSession, Participant
from django.conf import settings


class PlanningPokerTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.players = 1
        # self.poker_session_id = 1
        self.back_log_file = settings.MEDIA_ROOT + '/files/backlog.json'
        # self.poker_session = PokerSession.objects.create(
        #     players=self.players,
        #     owner=self.user,
        #     product_backlog_file=settings.MEDIA_ROOT + '/files/backlog.json'
        # )
        self.join_poker_session_url = reverse('core:join_poker_session')

    def create_poker_session(self):
        poker_session, created = PokerSession.objects.get_or_create(
            players=self.players,
            owner=self.user,
            product_backlog_file=self.back_log_file
        )

        self.assertTrue(created)

    def test_join_poker_session(self):
        # Données à envoyer via POST
        poker_session, created = PokerSession.objects.get_or_create(
            players=self.players,
            owner=self.user,
            product_backlog_file=self.back_log_file
        )
        data = {'session_id': poker_session.pk}

        # Simule un POST request pour rejoindre la session de poker
        response = self.client.post(self.join_poker_session_url, data)

        # Vérifier la redirection
        self.assertEqual(response.status_code, 302)

        # Vérifier que l'utilisateur a été ajouté en tant que participant
        self.assertEqual(poker_session.participants.count(), 1)
        self.assertTrue(poker_session.participants.filter(user=self.user).exists())

    def test_join_full_poker_session(self):
        poker_session, created = PokerSession.objects.get_or_create(
            players=self.players,
            owner=self.user,
            product_backlog_file=self.back_log_file
        )
        # Ajouter des participants à la session jusqu'à atteindre la limite
        for i in range(poker_session.players):
            user = User.objects.create_user(username=f'user{i}', password='12345')
            Participant.objects.create(poker_session=poker_session, user=user)

        # Tenter de rejoindre une session complète
        data = {'session_id': poker_session.pk}
        response = self.client.post(self.join_poker_session_url, data)

        # Vérifier que le nombre de participants n'a pas changé
        self.assertEqual(poker_session.participants.count(), poker_session.players)

    # def test_vote_poker_session(self):
    #     # Créer une session de poker
    #
    #     poker_session, created = PokerSession.objects.get_or_create(
    #         players=self.players,
    #         owner=self.user,
    #         product_backlog_file=self.back_log_file
    #     )
    #     # Rejoindre la session de poker
    #     self.client.post(self.join_poker_session_url, {'session_id': poker_session.pk})
    #
    #     # Voter pour une fonctionnalité
    #     vote_url = reverse('core:vote', kwargs={'poker_session_id': poker_session.pk, 'card': '100'})
    #     response = self.client.get(vote_url)
    #
    #     # Vérifier la redirection
    #     self.assertEqual(response.status_code, 302)
    #
    #     # Vérifier que le vote a été pris en compte
    #     participant = Participant.objects.get(poker_session=poker_session, user=self.user)
    #     self.assertTrue(participant.votes.filter(vote=100).exists())
