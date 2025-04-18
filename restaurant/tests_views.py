from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Restaurant, Booking, TimeSlot, Table
from django.utils import timezone
from datetime import datetime, timedelta


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            address="123 Test Street",
            opening_time=datetime.strptime('09:00', '%H:%M').time(),
            closing_time=datetime.strptime('22:00', '%H:%M').time(),
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

    def test_restaurant_list_view(self):
        response = self.client.get(reverse('restaurant_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/restaurant_list.html')
        self.assertContains(response, self.restaurant.name)

    def test_restaurant_detail_view(self):
        response = self.client.get(reverse('restaurant_detail', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/restaurant_detail.html')
        self.assertContains(response, self.restaurant.name)

    def test_booking_create_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('book_restaurant', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/booking_form.html')

    def test_booking_create_view_unauthenticated(self):
        response = self.client.get(reverse('book_restaurant', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        self.assertRedirects(response, f'/accounts/login/?next=/restaurant/{self.restaurant.id}/book/')

    def test_my_bookings_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/my_bookings.html')

    def test_my_bookings_view_unauthenticated(self):
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_booking_update_view(self):
        self.client.login(username='testuser', password='testpass123')
        booking = Booking.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            table=self.table,
            time_slot=self.time_slot,
            date=timezone.now().date(),
            time=timezone.now().time(),
            number_of_guests=2
        )
        response = self.client.get(reverse('edit_booking', args=[booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/edit_booking.html')

    def test_booking_delete_view(self):
        self.client.login(username='testuser', password='testpass123')
        booking = Booking.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            table=self.table,
            time_slot=self.time_slot,
            date=timezone.now().date(),
            time=timezone.now().time(),
            number_of_guests=2
        )
        response = self.client.get(reverse('delete_booking', args=[booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/delete_booking.html') 