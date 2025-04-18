from django.test import TestCase
from django.contrib.auth.models import User
from .models import Restaurant, Table, TimeSlot, MenuItem
from .forms import BookingForm
from django.utils import timezone
from datetime import datetime, timedelta
from restaurant.forms import (
    UserRegistrationForm,
    MenuItemForm,
    ContactForm
)
from django.urls import reverse


class BookingFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            is_staff=True
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

    def test_valid_booking_form(self):
        form_data = {
            'date': timezone.now().date() + timedelta(days=1),
            'time': datetime.strptime('13:00', '%H:%M').time(),
            'number_of_guests': 2,
            'special_requests': 'Window seat please',
            'table': self.table.id,
            'time_slot': self.time_slot.id
        }
        form = BookingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_booking_form_with_past_date(self):
        form_data = {
            'date': timezone.now().date() - timedelta(days=1),
            'time': datetime.strptime('13:00', '%H:%M').time(),
            'number_of_guests': 2,
            'table': self.table.id,
            'time_slot': self.time_slot.id
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

    def test_booking_form_with_too_many_guests(self):
        form_data = {
            'date': timezone.now().date() + timedelta(days=1),
            'time': datetime.strptime('13:00', '%H:%M').time(),
            'number_of_guests': 10,  # More than table capacity
            'table': self.table.id,
            'time_slot': self.time_slot.id
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('number_of_guests', form.errors)

    def test_booking_form_without_required_fields(self):
        form_data = {
            'date': timezone.now().date() + timedelta(days=1),
            'time': datetime.strptime('13:00', '%H:%M').time(),
            # Missing number_of_guests
            'table': self.table.id,
            'time_slot': self.time_slot.id
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('number_of_guests', form.errors)

    def test_booking_form_with_invalid_time(self):
        form_data = {
            'date': timezone.now().date() + timedelta(days=1),
            'time': datetime.strptime('23:00', '%H:%M').time(),
            'number_of_guests': 2,
            'special_requests': 'Window seat please',
            'table': self.table.id,
            'time_slot': self.time_slot.id
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('time', form.errors)

    def test_booking_form_valid(self):
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        form_data = {
            'date': tomorrow.date().isoformat(),
            'time': '12:00',
            'number_of_guests': 4,
            'special_requests': 'Test request',
            'table': self.table.id,
            'time_slot': self.time_slot.id
        }
        form = BookingForm(data=form_data)
        self.assertTrue(form.is_valid())


class FormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            is_staff=True
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

    def test_user_registration_form_valid(self):
        form_data = {
            'username': 'newtestuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = UserRegistrationForm(data=form_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_user_registration_form_invalid(self):
        form_data = {
            'username': '',
            'email': 'invalid-email',
            'password1': 'short',
            'password2': 'different'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password2', form.errors)

    def test_booking_form_valid(self):
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        form_data = {
            'date': tomorrow.date().isoformat(),
            'time': '12:00',
            'number_of_guests': 4,
            'special_requests': 'Test request',
            'table': self.table.id,
            'time_slot': self.time_slot.id
        }
        form = BookingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_booking_form_invalid(self):
        form_data = {
            'date': '2020-01-01',
            'time': '23:00',
            'number_of_guests': 0,
            'special_requests': 'x' * 501
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
        self.assertIn('time', form.errors)
        self.assertIn('number_of_guests', form.errors)
        self.assertIn('special_requests', form.errors)

    def test_menu_item_form_valid(self):
        form_data = {
            'name': 'Test Item',
            'description': 'Test Description',
            'price': '9.99'
        }
        form = MenuItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_menu_item_form_invalid(self):
        form_data = {
            'name': '',
            'description': '',
            'price': '-1.00'
        }
        form = MenuItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('description', form.errors)
        self.assertIn('price', form.errors)

    def test_contact_form_valid(self):
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test message'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contact_form_validation(self):
        form = ContactForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('subject', form.errors)
        self.assertIn('message', form.errors)

    def test_menu_item_creation(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse(
                'add_menu_item',
                kwargs={'restaurant_id': self.restaurant.id}
            ),
            {
                'name': 'Test Item',
                'description': 'Test Description',
                'price': '10.00',
                'category': 'MAIN'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            MenuItem.objects.filter(
                restaurant=self.restaurant,
                name='Test Item'
            ).exists()
        )
