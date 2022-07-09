"""
Test for the django admin modifications
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django admin"""

    # this setup is creating 1. a client, 2. an admin user, 3. a user
    # this is used below in the test_users_list method
    def setUp(self):
        """Create user and client"""
        # here so we can make requests through it? think self(testcase)
        # then client then
        # force login is the function to test login functionality as an admin
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )

    # reinforcement -- whenever you see self as a param in a method..
    # it's the class being passed in
    def test_users_list(self):
        """Test that users are listed on the page"""
        # used to pull url for change list 'reverse admin urls'
        # in django documentation
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
