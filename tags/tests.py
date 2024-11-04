from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.urls import reverse
from .models import Tag
from django.contrib.auth import get_user_model

User = get_user_model()

class TagViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_create_tag(self):
        response = self.client.post(reverse('new_tag'), {
            'label': 'Test Tag',
            'description': 'This is a test tag.'
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.assertTrue(Tag.objects.filter(label='Test Tag').exists())
        tag = Tag.objects.get(label='Test Tag')
        self.assertEqual(tag.tag_owner, self.user)

class TagModificationTests(TestCase):

    def setUp(self):
        # Create two users
        self.owner = User.objects.create_user(username='owner', password='ownerpassword')
        self.non_owner = User.objects.create_user(username='non_owner', password='nonownerpassword')
        
        # Create a tag owned by the owner
        self.tag = Tag.objects.create(label='Owner Tag', tag_owner=self.owner)

    def test_update_tag_unauthorized_user(self):
        # Log in as a non-owner
        self.client.login(username='non_owner', password='nonownerpassword')
        
        # Attempt to update the tag
        response = self.client.post(reverse('update_tag', args=[self.tag.pk]), {
            'label': 'New Label',
            'description': 'Updated description.'
        })
        
        # Check that the response is a redirect (forbidden)
        self.assertEqual(response.status_code, 403)  # Expect a forbidden status
        self.tag.refresh_from_db()  # Refresh to get the latest data
        self.assertEqual(self.tag.label, 'Owner Tag')  # Ensure the tag was not updated

    def test_delete_tag_unauthorized_user(self):
        # Log in as a non-owner
        self.client.login(username='non_owner', password='nonownerpassword')
        
        # Attempt to delete the tag
        response = self.client.post(reverse('delete_tag', args=[self.tag.pk]))
        
        # Check that the response is a redirect (forbidden)
        self.assertEqual(response.status_code, 403)  # Expect a forbidden status
        self.assertTrue(Tag.objects.filter(pk=self.tag.pk).exists())  # Ensure the tag
    
    def test_update_tag_page_unauthorized_user(self):
        # Log in as a non-owner
        self.client.login(username='non_owner', password='nonownerpassword')

        # Attempt to access the update tag page
        response = self.client.get(reverse('update_tag', args=[self.tag.pk]))
        self.assertEqual(response.status_code, 403)  # Expect a forbidden status

    def test_delete_tag_page_unauthorized_user(self):
        # Log in as a non-owner
        self.client.login(username='non_owner', password='nonownerpassword')

        # Attempt to access the delete tag page
        response = self.client.get(reverse('delete_tag', args=[self.tag.pk]))
        self.assertEqual(response.status_code, 403)  # Expect a forbidden status