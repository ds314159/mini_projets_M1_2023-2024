# Fichier: test_poker.py
import unittest

from django.conf import settings

from planning_poker.core.models import PokerSession


class TestPokerSession(unittest.TestCase):

    def test_create_poker_session(self):
        # Créer une nouvelle session de poker
        session, _ = PokerSession.objects.create(players=4, owner_id='kimmy', mode="strict", product_backlog_file=settings.MEDIA_ROOT + "/files/backlog.json")

        # Vérifier que la session a été ajoutée à la base de données
        self.assertTrue(PokerSession.objects.filter(players=4, owner_id='kimmy', mode="strict").exists())
        self.assertEqual(session.players, 4)
        self.assertEqual(session.owner_id, 'kimmy')


if __name__ == '__main__':
    unittest.main()
