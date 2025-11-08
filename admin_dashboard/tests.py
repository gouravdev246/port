from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_view_success(self):
        response = self.client.post(reverse('admin_dashboard:login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin_dashboard:dashboard'))

    def test_login_view_failure(self):
        response = self.client.post(reverse('admin_dashboard:login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')

    def test_password_reset(self):
        response = self.client.get(reverse('admin_dashboard:password_reset'))
        self.assertEqual(response.status_code, 200)
