from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Bet
import uuid


class BetModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.bet = Bet.objects.create(
            bet_owner=self.user,
            site="Test Site",
            pick="Test Pick",
            stake=100.00,
            odds=1.50,
            bet_type="Spread",
            result="Win",
        )

    def test_bet_creation(self):
        self.assertEqual(self.bet.pick, "Test Pick")
        self.assertEqual(self.bet.stake, 100.00)
        self.assertEqual(self.bet.odds, 1.50)
        self.assertEqual(self.bet.result, "Win")

    def test_bet_payout(self):
        self.assertEqual(
            self.bet.payout, 150.00
        )  # Assuming bet_payout function returns stake * odds for 'Pending'


class BetViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.client.login(username="testuser", password="password")
        self.bet = Bet.objects.create(
            bet_owner=self.user,
            site="Test Site",
            pick="Test Pick",
            stake=100.00,
            odds=1.50,
            bet_type="Spread",
            result="Pending",
        )

    def test_bet_history_view(self):
        response = self.client.get(reverse("bet_history"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Pick")

    def test_new_bet_view(self):
        response = self.client.post(
            reverse("new_bet"),
            {
                "site": "New Site",
                "pick": "New Pick",
                "stake": 200.00,
                "odds": 2.00,
                "bet_type": "Moneyline",
                "result": "Pending",
            },
        )
        self.assertEqual(
            response.status_code, 302
        )  # Redirect after successful creation
        self.assertEqual(Bet.objects.last().pick, "New Pick")

    def test_update_bet_view(self):
        response = self.client.post(
            reverse("update_bet", args=[self.bet.id]),
            {
                "site": "Updated Site",
                "pick": "Updated Pick",
                "stake": 150.00,
                "odds": 1.75,
                "bet_type": "Spread",
                "result": "Win",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.bet.refresh_from_db()
        self.assertEqual(self.bet.pick, "Updated Pick")
        self.assertEqual(self.bet.stake, 150.00)
        self.assertEqual(self.bet.odds, 1.75)
        self.assertEqual(self.bet.result, "Win")

    def test_delete_bet_view(self):
        response = self.client.delete(reverse("delete_bet", args=[self.bet.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Bet.objects.filter(id=self.bet.id).exists())
