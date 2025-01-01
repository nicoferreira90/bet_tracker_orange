from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Bet
from bets.analytics import bet_payout
from tags.models import Tag


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
        expected_payout = bet_payout(self.bet.stake, self.bet.odds, self.bet.result)
        self.assertEqual(self.bet.payout, expected_payout)


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
        )  # Redirect after successful creation of new bet

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


class BetTagIntegrationTest(TestCase):
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
        self.tag = Tag.objects.create(
            label="Test Tag", description="Test Description", tag_owner=self.user
        )

    def test_add_tag_to_bet(self):
        self.tag.associated_bets.add(self.bet)
        self.assertIn(self.bet, self.tag.associated_bets.all())
        self.assertIn(self.tag, self.bet.tags.all())

    def test_remove_tag_from_bet(self):
        self.tag.associated_bets.add(self.bet)
        self.tag.associated_bets.remove(self.bet)
        self.assertNotIn(self.bet, self.tag.associated_bets.all())
        self.assertNotIn(self.tag, self.bet.tags.all())

    def test_view_add_tag_to_bet(self):
        response = self.client.post(
            reverse("add_associated_tag", args=[self.bet.id]),
            {"tag-select": self.tag.label},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.bet, self.tag.associated_bets.all())
        self.assertIn(self.tag, self.bet.tags.all())

    def test_view_remove_tag_from_bet(self):
        self.tag.associated_bets.add(self.bet)
        response = self.client.post(
            reverse("remove_associated_tag", args=[self.bet.id]),
            {"bet-id": self.bet.id, "tag-id": self.tag.id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.bet, self.tag.associated_bets.all())
        self.assertNotIn(self.tag, self.bet.tags.all())
