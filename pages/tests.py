from django.test import SimpleTestCase
from django.urls import reverse

# We import SimpleTestCase as the homepage does not rely on the database.
# If it did indeed rely on the database (like the Bet History page does), we would use TestCase instead.
class HomePageTests(SimpleTestCase):
    def test_url_exists_at_correct_location_homepageview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_homepage_view(self):
        response = self.client.get(reverse("home_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home_page.html")

class AboutPageTests(SimpleTestCase):
    def test_url_exists_at_correct_location_aboutpageview(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)
    
    def test_homepage_view(self):
        response = self.client.get(reverse("about_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about_page.html")
