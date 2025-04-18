from django.test import TestCase
from .models import Restaurant, TimeSlot, Booking, MenuItem, Table
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from .forms import BookingForm


class RestaurantModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            address="123 Test Street",
            description="A test restaurant",
            opening_time=datetime.strptime('09:00', '%H:%M').time(),
            closing_time=datetime.strptime('22:00', '%H:%M').time(),
            capacity=50,
            contact_number="123-456-7890",
            email="test@example.com"
        )

    def test_restaurant_creation(self):
        self.assertEqual(self.restaurant.name, "Test Restaurant")
        self.assertEqual(self.restaurant.address, "123 Test Street")
        self.assertEqual(self.restaurant.description, "A test restaurant")
        self.assertEqual(
            self.restaurant.opening_time,
            datetime.strptime('09:00', '%H:%M').time()
        )
        self.assertEqual(
            self.restaurant.closing_time,
            datetime.strptime('22:00', '%H:%M').time()
        )
        self.assertEqual(self.restaurant.capacity, 50)
        self.assertEqual(self.restaurant.contact_number, "123-456-7890")
        self.assertEqual(self.restaurant.email, "test@example.com")


class TimeSlotModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            address="123 Test Street",
            opening_time=datetime.strptime('09:00', '%H:%M').time(),
            closing_time=datetime.strptime('22:00', '%H:%M').time(),
        )
        self.time_slot = TimeSlot.objects.create(
            restaurant=self.restaurant,
            start_time=datetime.strptime('12:00', '%H:%M').time(),
            end_time=datetime.strptime('14:00', '%H:%M').time(),
            is_available=True
        )

    def test_time_slot_creation(self):
        self.assertEqual(self.time_slot.restaurant, self.restaurant)
        self.assertEqual(
            self.time_slot.start_time,
            datetime.strptime('12:00', '%H:%M').time()
        )
        self.assertEqual(
            self.time_slot.end_time,
            datetime.strptime('14:00', '%H:%M').time()
        )
        self.assertTrue(self.time_slot.is_available)


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
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
        self.booking = Booking.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            table=self.table,
            time_slot=self.time_slot,
            date=timezone.now().date(),
            time=timezone.now().time(),
            number_of_guests=2,
            special_requests="None",
            status="pending"
        )

    def test_booking_creation(self):
        self.assertEqual(self.booking.user, self.user)
        self.assertEqual(self.booking.restaurant, self.restaurant)
        self.assertEqual(self.booking.table, self.table)
        self.assertEqual(self.booking.time_slot, self.time_slot)
        self.assertEqual(self.booking.number_of_guests, 2)
        self.assertEqual(self.booking.special_requests, "None")
        self.assertEqual(self.booking.status, "pending")

    def test_booking_form_validation(self):
        """Test booking form validation"""
        form_data = {
            'date': timezone.now().date() + timedelta(days=1),
            'time': datetime.strptime('12:00', '%H:%M').time(),
            'number_of_guests': 4,
            'special_requests': 'Test request'
        }
        
        # Test valid form
        form = BookingForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Test invalid number of guests
        form_data['number_of_guests'] = 0
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('number_of_guests', form.errors)
        
        form_data['number_of_guests'] = 9
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('number_of_guests', form.errors)
        
        # Test past date
        form_data['number_of_guests'] = 4
        form_data['date'] = timezone.now().date() - timedelta(days=1)
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
        
        # Test invalid time


class MenuItemModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            address="123 Test Street",
            opening_time=datetime.strptime('09:00', '%H:%M').time(),
            closing_time=datetime.strptime('22:00', '%H:%M').time(),
        )
        self.menu_item = MenuItem.objects.create(
            name="Test Item",
            description="A test menu item",
            price=Decimal("10.99"),
            restaurant=self.restaurant
        )

    def test_menu_item_creation(self):
        self.assertEqual(self.menu_item.name, "Test Item")
        self.assertEqual(self.menu_item.description, "A test menu item")
        self.assertEqual(self.menu_item.price, Decimal("10.99"))
        self.assertEqual(self.menu_item.restaurant, self.restaurant)
