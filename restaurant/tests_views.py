from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Restaurant, Booking, TimeSlot, Table, MenuItem, Contact
from .forms import BookingForm, ContactForm, MenuItemForm
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='staffpassword',
            is_staff=True
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
        self.menu_item = MenuItem.objects.create(
            name='Test Item',
            description='Test Description',
            price=Decimal('9.99'),
            restaurant=self.restaurant
        )
        self.contact = Contact.objects.create(
            name='Test Contact',
            email='contact@test.com',
            subject='Test Subject',
            message='Test Message'
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
        response = self.client.get(reverse('edit_booking', args=[self.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/edit_booking.html')

    def test_booking_delete_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('delete_booking', args=[self.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/delete_booking.html')

    def test_contact_form_submission(self):
        url = reverse('contact')
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test Message'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Contact.objects.filter(email='test@example.com').exists())

    def test_edit_booking(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('edit_booking', args=[self.booking.id])
        data = {
            'date': (datetime.now().date() + timedelta(days=2)).strftime('%Y-%m-%d'),
            'time': '14:00',
            'number_of_guests': 3,
            'special_requests': 'Updated request'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.number_of_guests, 3)

    def test_delete_booking(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('delete_booking', args=[self.booking.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())

    def test_manage_menu(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('manage_menu', args=[self.restaurant.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/manage_menu.html')

    def test_add_menu_item(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('add_menu_item', args=[self.restaurant.id])
        data = {
            'name': 'New Item',
            'description': 'New Description',
            'price': '12.99'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MenuItem.objects.filter(name='New Item').exists())

    def test_edit_menu_item(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('edit_menu_item', args=[self.menu_item.id])
        data = {
            'name': 'Updated Item',
            'description': 'Updated Description',
            'price': '14.99'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.name, 'Updated Item')

    def test_delete_menu_item(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('delete_menu_item', args=[self.menu_item.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(MenuItem.objects.filter(id=self.menu_item.id).exists())

    def test_contact_messages(self):
        self.client.login(username='staffuser', password='staffpassword')
        response = self.client.get(reverse('contact_messages'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/contact_messages.html')
        self.assertContains(response, self.contact.subject)

    def test_view_contact(self):
        self.client.login(username='staffuser', password='staffpassword')
        response = self.client.get(reverse('view_contact', args=[self.contact.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/view_contact.html')
        self.assertContains(response, self.contact.message)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.status, 'read')

    def test_update_contact_status(self):
        self.client.login(username='staffuser', password='staffpassword')
        url = reverse('update_contact_status', args=[self.contact.id])
        response = self.client.post(url, {'status': 'read'})
        self.assertEqual(response.status_code, 302)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.status, 'read')

    def test_delete_contact(self):
        self.client.login(username='staffuser', password='staffpassword')
        url = reverse('delete_contact', args=[self.contact.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Contact.objects.filter(id=self.contact.id).exists())

    def test_booking_form_validation(self):
        """Test booking form validation."""
        form_data = {
            'date': (datetime.now().date() - timedelta(days=1)).strftime('%Y-%m-%d'),
            'time': '12:00',
            'number_of_guests': 0
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
        self.assertIn('number_of_guests', form.errors)

    def test_contact_form_error_handling(self):
        """Test contact form error handling."""
        form_data = {
            'name': '',
            'email': 'invalid-email',
            'subject': '',
            'message': ''
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)

    def test_restaurant_detail_menu_items(self):
        """Test restaurant detail view with menu items."""
        response = self.client.get(reverse('restaurant_detail', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.menu_item.name)
        self.assertContains(response, self.menu_item.description)

    def test_booking_cancellation(self):
        """Test booking cancellation."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('cancel_booking', args=[self.booking.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'cancelled')

    def test_booking_edit_validation(self):
        """Test booking edit validation."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('edit_booking', args=[self.booking.id])
        data = {
            'date': (datetime.now().date() - timedelta(days=1)).strftime('%Y-%m-%d'),
            'time': '12:00',
            'number_of_guests': 0
        }
        form = BookingForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
        self.assertIn('number_of_guests', form.errors)

    def test_menu_management_unauthorized(self):
        """Test menu management unauthorized access."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('manage_menu', args=[self.restaurant.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Should be accessible to all authenticated users

    def test_menu_item_addition_validation(self):
        """Test menu item addition validation."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'name': '',
            'description': '',
            'price': '-10.00'
        }
        form = MenuItemForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('price', form.errors)

    def test_menu_item_edit_validation(self):
        """Test menu item edit validation."""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'name': '',
            'description': '',
            'price': '-10.00'
        }
        form = MenuItemForm(data=data, instance=self.menu_item)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('price', form.errors)

    def test_contact_status_update_error(self):
        """Test contact status update error handling."""
        self.client.login(username='staffuser', password='staffpassword')
        url = reverse('update_contact_status', args=[self.contact.id])
        response = self.client.post(url, {'status': 'invalid_status'})
        self.assertEqual(response.status_code, 302)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.status, 'unread')  # Status should not change

    def test_contact_deletion_error(self):
        """Test contact deletion error handling."""
        self.client.login(username='staffuser', password='staffpassword')
        # Create a new contact
        contact = Contact.objects.create(
            name='Test Contact 2',
            email='contact2@test.com',
            subject='Test Subject 2',
            message='Test Message 2',
            status='invalid_status'
        )
        url = reverse('delete_contact', args=[contact.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        # Contact should be deleted regardless of status
        self.assertFalse(Contact.objects.filter(id=contact.id).exists()) 