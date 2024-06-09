import unittest

from planning_poker.core.models import PokerSession
from planning_poker.core.views import vote
from planning_poker.users.models import User
from django.http import HttpRequest

from django.test import Client


class CreateSessionTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_vote(self):
        request = HttpRequest()
        # request.user = User.objects.last()
        card = "100"
        poker_session_id = PokerSession.objects.last().pk
        response = vote(request, poker_session_id, card)
        self.assertEqual(response.status_code, 302)  # Check that the response is a redirect


if __name__ == '__main__':
    unittest.main()
