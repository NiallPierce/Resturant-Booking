from django.test import TestCase
from django.contrib.auth.models import User
from .models import Restaurant, Table, TimeSlot
from .forms import BookingForm
from django.utils import timezone
from datetime import datetime, timedelta


class BookingFormTest(TestCase):
    def setUp(self):
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
            'time': datetime.strptime('23:00', '%H:%M').time(),  # Outside opening hours
            'number_of_guests': 2,
            'table': self.table.id,
            'time_slot': self.time_slot.id
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('time', form.errors) 