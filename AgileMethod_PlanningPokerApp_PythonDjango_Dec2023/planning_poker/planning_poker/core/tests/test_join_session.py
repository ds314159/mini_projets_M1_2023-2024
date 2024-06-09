# Fichier: test_poker.py
import unittest

from django.conf import settings
from django.contrib.auth.models import User

from planning_poker.core.models import PokerSession, Participant


class TestPokerSession(unittest.TestCase):

    def test_join_poker_session(self):
        # Rejoindre une nouvelle session de poker
        poker_session = PokerSession.objects.last()
        user = User.objects.last()
        participant = Participant.objects.get(user=user, poker_session=poker_session)

        self.assertTrue(Participant.objects.filter(user=user, poker_session=poker_session).exists())


if __name__ == '__main__':
    unittest.main()
