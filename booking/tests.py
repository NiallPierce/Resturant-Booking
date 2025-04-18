from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from restaurant.models import Restaurant, Booking, Table, TimeSlot
from datetime import datetime, timedelta


class MainProjectTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            address="123 Test Street",
            opening_time=datetime.strptime('09:00', '%H:%M').time(),
            closing_time=datetime.strptime('22:00', '%H:%M').time(),
            contact_number='1234567890',
            email='restaurant@test.com'
        )
        self.table = Table.objects.create(
            restaurant=self.restaurant,
            table_number=1,
            capacity=4,
            is_active=True
        )
        self.time_slot = TimeSlot.objects.create(
            restaurant=self.restaurant,
            start_time=datetime.strptime('12:00', '%H:%M').time(),
            end_time=datetime.strptime('14:00', '%H:%M').time(),
            is_available=True
        )
        self.booking = Booking.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            date=datetime.now().date() + timedelta(days=1),
            time=datetime.now().time(),
            number_of_guests=2
        )

    def test_booking_list_redirect(self):
        """Test that booking_list redirects to my_bookings."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('booking_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/my_bookings.html')

    def test_booking_list_unauthenticated(self):
        """Test that booking_list requires authentication."""
        response = self.client.get(reverse('booking_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_booking_detail_authenticated(self):
        """Test booking_detail view for authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('booking_detail', args=[self.booking.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/delete_booking.html')
        self.assertEqual(response.context['booking'], self.booking)

    def test_booking_detail_unauthorized(self):
        """Test booking_detail view for unauthorized user."""
        User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(
            reverse('booking_detail', args=[self.booking.id])
        )
        self.assertEqual(response.status_code, 403)

    def test_booking_detail_unauthenticated(self):
        """Test booking_detail view for unauthenticated user."""
        response = self.client.get(
            reverse('booking_detail', args=[self.booking.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_booking_detail_not_found(self):
        """Test booking_detail view for non-existent booking."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('booking_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_main_urls(self):
        """Test main project URL patterns."""
        # Test admin URL
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)  # Redirects to login
        # Test accounts URLs (Allauth)
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        # Test restaurant URLs
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/restaurant_list.html')

    def test_static_files_in_development(self):
        """Test static files serving in development mode."""
        # This test assumes DEBUG=True in settings
        # Create a test static file
        import os
        from django.conf import settings
        # Create test static directory if it doesn't exist
        test_static_dir = os.path.join(settings.STATIC_ROOT, 'test')
        os.makedirs(test_static_dir, exist_ok=True)
        # Create a test file
        test_file_path = os.path.join(test_static_dir, 'test.txt')
        with open(test_file_path, 'w') as f:
            f.write('Test content')
        # Check if the file is served
        response = self.client.get('/static/test/test.txt')
        self.assertEqual(response.status_code, 200)
        # Handle WhiteNoiseFileResponse
        if hasattr(response, 'streaming_content'):
            content = b''.join(response.streaming_content)
        else:
            content = response.content
        self.assertEqual(content.decode(), 'Test content')
        # Clean up
        os.remove(test_file_path)
        os.rmdir(test_static_dir)
