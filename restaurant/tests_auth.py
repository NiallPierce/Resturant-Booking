from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        EmailAddress.objects.create(
            user=self.user,
            email='test@example.com',
            primary=True,
            verified=True
        )

    def test_login_view(self):
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_successful_login(self):
        response = self.client.post(reverse('account_login'), {
            'login': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after login
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_failed_login(self):
        response = self.client.post(reverse('account_login'), {
            'login': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Should stay on login page
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('account_logout'))
        self.assertEqual(response.status_code, 302)  # Should redirect to logout page
        response = self.client.get(response.url)  # Follow the redirect
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/restaurant_list.html')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_successful_logout(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('account_logout'))
        self.assertEqual(response.status_code, 302)  # Should redirect after logout
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_registration_view(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')

    def test_successful_registration(self):
        response = self.client.post(reverse('account_signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after registration
        self.assertTrue(get_user_model().objects.filter(username='newuser').exists())

    def test_registration_with_existing_username(self):
        response = self.client.post(reverse('account_signup'), {
            'username': 'testuser',  # Already exists
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertEqual(response.status_code, 200)  # Should stay on registration page
        self.assertFalse(get_user_model().objects.filter(email='newuser@example.com').exists())

    def test_protected_view_access(self):
        # Try to access a protected view without login
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

        # Login and try again
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 200)  # Should be accessible 