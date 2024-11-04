from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from bets.models import Bet

User = get_user_model()

class AnalyticsWithResultsViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create some bets for the user
        Bet.objects.create(bet_owner=self.user, result='Win', stake=100, odds=1.5)
        Bet.objects.create(bet_owner=self.user, result='Lose', stake=50, odds=2.0)
        Bet.objects.create(bet_owner=self.user, result='Pending', stake=30, odds=1.0)

    def test_post_with_filters(self):
        response = self.client.post(reverse('analytics_results'), {
            'type-filter': 'category-all',
            'result-filter': 'category-all',
            'tag-filter': '',
            'dateOption': 'all',  # Use 'all' to check without date filters
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('user_bets', response.context)
        self.assertEqual(response.context['bet_count'], 3)  # All bets
        self.assertEqual(response.context['bets_won_count'], 1)  # 1 win
        self.assertEqual(response.context['bets_lost_count'], 1)  # 1 loss
        self.assertEqual(response.context['bets_pending_count'], 1)  # 1 pending

    def test_post_with_custom_date_filter(self):
        response = self.client.post(reverse('analytics_results'), {
            'type-filter': 'category-all',
            'result-filter': 'category-all',
            'tag-filter': '',
            'dateOption': 'custom',
            'filterDateStart': '2020-01-01',  # Use appropriate date format
            'filterDateEnd': '2052-12-31',
        })

        # Assuming all created bets fall within the date range
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['bet_count'], 3)  # Still 3 bets


    def test_invalid_filters(self):
        response = self.client.post(reverse('analytics_results'), {
            'type-filter': 'invalid-category',
            'result-filter': 'invalid-result',
            'tag-filter': '',
            'dateOption': 'all',
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('user_bets', response.context)
        # Depending on how your filter logic is set, you may expect certain outcomes