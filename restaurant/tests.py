from django.test import TestCase, Client
from .models import Restaurant, TimeSlot, Booking, MenuItem, Table, Contact
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from .forms import BookingForm
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib import messages


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

    def test_restaurant_str_method(self):
        self.assertEqual(str(self.restaurant), "Test Restaurant")


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

    def test_time_slot_str_method(self):
        expected = f"{self.restaurant.name} - {self.time_slot.start_time} to {self.time_slot.end_time}"
        self.assertEqual(str(self.time_slot), expected)

    def test_time_slot_availability(self):
        self.time_slot.is_available = False
        self.time_slot.save()
        self.assertFalse(self.time_slot.is_available)


class TableModelTest(TestCase):
    def setUp(self):
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

    def test_table_creation(self):
        self.assertEqual(self.table.restaurant, self.restaurant)
        self.assertEqual(self.table.table_number, 1)
        self.assertEqual(self.table.capacity, 4)
        self.assertTrue(self.table.is_active)

    def test_table_str_method(self):
        expected = f"{self.restaurant.name} - Table {self.table.table_number} (Seats {self.table.capacity})"
        self.assertEqual(str(self.table), expected)

    def test_table_activation(self):
        self.table.is_active = False
        self.table.save()
        self.assertFalse(self.table.is_active)

    def test_table_capacity_validation(self):
        # Test valid capacity
        valid_table = Table(
            restaurant=self.restaurant,
            table_number=2,
            capacity=6,
            is_active=True
        )
        valid_table.full_clean()  # Should not raise an error

        # Test invalid capacity (negative)
        invalid_table = Table(
            restaurant=self.restaurant,
            table_number=3,
            capacity=-2,
            is_active=True
        )
        with self.assertRaises(ValidationError):
            invalid_table.full_clean()

    def test_table_number_uniqueness(self):
        # Create another table with the same number
        duplicate_table = Table(
            restaurant=self.restaurant,
            table_number=1,  # Same as self.table
            capacity=4,
            is_active=True
        )
        with self.assertRaises(ValidationError):
            duplicate_table.full_clean()

    def test_table_restaurant_cascade_delete(self):
        # Test that tables are deleted when their restaurant is deleted
        table_id = self.table.id
        self.restaurant.delete()
        with self.assertRaises(Table.DoesNotExist):
            Table.objects.get(id=table_id)


class BookingModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com"
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
        # Create a table for testing
        table = Table.objects.create(
            restaurant=self.restaurant,
            table_number=2,  # Changed from 1 to 2 to avoid conflict
            capacity=4,
            is_active=True
        )
        
        form_data = {
            'date': timezone.now().date() + timedelta(days=1),
            'time': datetime.strptime('12:00', '%H:%M').time(),
            'number_of_guests': 4,
            'special_requests': 'Test request',
            'table': table.id
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
        form_data['date'] = timezone.now().date() + timedelta(days=1)
        form_data['time'] = datetime.strptime('23:00', '%H:%M').time()
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('time', form.errors)

    def test_booking_str_method(self):
        expected = f"Booking for {self.user.username} at {self.restaurant.name} on {self.booking.date} at {self.booking.time}"
        self.assertEqual(str(self.booking), expected)

    def test_user_login(self):
        response = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(response)

    def test_user_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.logout()
        self.assertEqual(response, None)

    def test_restaurant_list_view(self):
        response = self.client.get(reverse('restaurant_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/restaurant_list.html')

    def test_restaurant_detail_view(self):
        response = self.client.get(reverse('restaurant_detail', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/restaurant_detail.html')

    def test_booking_create_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('book_restaurant', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/booking_form.html')

    def test_booking_form_edge_cases(self):
        # Test empty form
        form = BookingForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
        self.assertIn('time', form.errors)
        self.assertIn('number_of_guests', form.errors)

        # Test form with missing fields
        form_data = {
            'date': timezone.now().date() + timedelta(days=1),
            'time': datetime.strptime('12:00', '%H:%M').time(),
            'number_of_guests': 4,
            'special_requests': 'Test request',
            'table': self.table.id
        }
        
        partial_data = form_data.copy()
        del partial_data['date']
        form = BookingForm(data=partial_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

        # Test maximum guests
        form_data['number_of_guests'] = 11
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('number_of_guests', form.errors)


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
            description="Test Description",
            price=Decimal('10.99'),
            restaurant=self.restaurant
        )

    def test_menu_item_creation(self):
        self.assertEqual(self.menu_item.name, "Test Item")
        self.assertEqual(self.menu_item.description, "Test Description")
        self.assertEqual(self.menu_item.price, Decimal('10.99'))
        self.assertEqual(self.menu_item.restaurant, self.restaurant)

    def test_menu_item_str_method(self):
        self.assertEqual(str(self.menu_item), "Test Item - $10.99")

    def test_menu_item_price_validation(self):
        # Test creating a menu item with valid price
        valid_item = MenuItem(
            name="Valid Item",
            description="Valid Description",
            price=Decimal('15.99'),
            restaurant=self.restaurant
        )
        valid_item.full_clean()  # Should not raise an error

        # Test creating a menu item with negative price
        invalid_item = MenuItem(
            name="Invalid Item",
            description="Invalid Description",
            price=Decimal('-5.99'),
            restaurant=self.restaurant
        )
        with self.assertRaises(ValidationError):
            invalid_item.full_clean()


class ContactModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name="Test User",
            email="test@example.com",
            subject="Test Subject",
            message="Test message content",
            status="unread"
        )

    def test_contact_creation(self):
        self.assertEqual(self.contact.name, "Test User")
        self.assertEqual(self.contact.email, "test@example.com")
        self.assertEqual(self.contact.subject, "Test Subject")
        self.assertEqual(self.contact.message, "Test message content")
        self.assertEqual(self.contact.status, "unread")
        self.assertIsNotNone(self.contact.created_at)
        self.assertIsNotNone(self.contact.updated_at)

    def test_contact_str_method(self):
        expected = f"Contact from {self.contact.name} - {self.contact.subject}"
        self.assertEqual(str(self.contact), expected)

    def test_contact_status_choices(self):
        valid_statuses = ['unread', 'read', 'replied']
        for status in valid_statuses:
            self.contact.status = status
            self.contact.save()
            self.assertEqual(self.contact.status, status)

    def test_contact_ordering(self):
        # Create another contact with a later timestamp
        later_contact = Contact.objects.create(
            name="Later User",
            email="later@example.com",
            subject="Later Subject",
            message="Later message"
        )
        
        # Get all contacts ordered by created_at
        contacts = Contact.objects.all()
        
        # The later contact should be first due to ordering
        self.assertEqual(contacts[0], later_contact)
        self.assertEqual(contacts[1], self.contact)


class ContactViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.contact_url = reverse('contact')
        self.valid_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content'
        }

    def test_contact_page_loads(self):
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/contact.html')
        self.assertIn('form', response.context)

    def test_contact_form_submission(self):
        response = self.client.post(self.contact_url, self.valid_data)
        self.assertEqual(response.status_code, 302)  # Should redirect after successful submission
        self.assertEqual(Contact.objects.count(), 1)
        
        contact = Contact.objects.first()
        self.assertEqual(contact.name, self.valid_data['name'])
        self.assertEqual(contact.email, self.valid_data['email'])
        self.assertEqual(contact.subject, self.valid_data['subject'])
        self.assertEqual(contact.message, self.valid_data['message'])
        self.assertEqual(contact.status, 'unread')

    def test_contact_form_invalid_data(self):
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'invalid-email'  # Invalid email format
        
        response = self.client.post(self.contact_url, invalid_data)
        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        self.assertEqual(Contact.objects.count(), 0)  # No contact should be created
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'][0], 'Enter a valid email address.')

    def test_contact_form_missing_fields(self):
        # Test with missing required fields
        for field in ['name', 'email', 'subject', 'message']:
            data = self.valid_data.copy()
            del data[field]
            
            response = self.client.post(self.contact_url, data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Contact.objects.count(), 0)
            form = response.context['form']
            self.assertFalse(form.is_valid())
            self.assertIn(field, form.errors)
            self.assertEqual(form.errors[field][0], 'This field is required.')


class BookingViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com"
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
        self.booking = Booking.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            table=self.table,
            date=timezone.now().date() + timedelta(days=1),
            time=datetime.strptime('12:00', '%H:%M').time(),
            number_of_guests=2,
            special_requests="Test request",
            status="pending"
        )

    def test_my_bookings_view(self):
        # Test unauthenticated access
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

        # Test authenticated access
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/my_bookings.html')
        self.assertIn('bookings', response.context)
        self.assertEqual(len(response.context['bookings']), 1)
        self.assertEqual(response.context['bookings'][0], self.booking)

    def test_cancel_booking_view(self):
        self.client.login(username='testuser', password='testpassword')
        
        # Test GET request
        response = self.client.get(reverse('cancel_booking', args=[self.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/delete_booking.html')
        self.assertIn('booking', response.context)
        self.assertEqual(response.context['booking'], self.booking)

        # Test POST request
        response = self.client.post(reverse('cancel_booking', args=[self.booking.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect to my_bookings
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'cancelled')

    def test_edit_booking_view(self):
        self.client.login(username='testuser', password='testpassword')
        
        # Test GET request
        response = self.client.get(reverse('edit_booking', args=[self.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/edit_booking.html')
        self.assertIn('form', response.context)
        self.assertIn('booking', response.context)
        self.assertEqual(response.context['booking'], self.booking)

        # Test POST request with valid data
        new_date = timezone.now().date() + timedelta(days=2)
        new_time = datetime.strptime('14:00', '%H:%M').time()
        form_data = {
            'date': new_date,
            'time': new_time,
            'number_of_guests': 3,
            'special_requests': 'Updated request'
        }
        response = self.client.post(reverse('edit_booking', args=[self.booking.id]), form_data)
        self.assertEqual(response.status_code, 302)  # Should redirect to my_bookings
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.date, new_date)
        self.assertEqual(self.booking.time, new_time)
        self.assertEqual(self.booking.number_of_guests, 3)
        self.assertEqual(self.booking.special_requests, 'Updated request')

    def test_delete_booking_view(self):
        self.client.login(username='testuser', password='testpassword')
        
        # Test GET request
        response = self.client.get(reverse('delete_booking', args=[self.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/delete_booking.html')
        self.assertIn('booking', response.context)
        self.assertEqual(response.context['booking'], self.booking)

        # Test POST request
        response = self.client.post(reverse('delete_booking', args=[self.booking.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect to my_bookings
        with self.assertRaises(Booking.DoesNotExist):
            Booking.objects.get(id=self.booking.id)

    def test_booking_unauthorized_access(self):
        # Create another user
        other_user = User.objects.create_user(
            username="otheruser",
            password="otherpassword"
        )
        self.client.login(username='otheruser', password='otherpassword')

        # Test accessing other user's booking
        response = self.client.get(reverse('edit_booking', args=[self.booking.id]))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('delete_booking', args=[self.booking.id]))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('cancel_booking', args=[self.booking.id]))
        self.assertEqual(response.status_code, 404)


class MenuViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com"
        )
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            address="123 Test Street",
            opening_time=datetime.strptime('09:00', '%H:%M').time(),
            closing_time=datetime.strptime('22:00', '%H:%M').time(),
        )
        self.menu_item = MenuItem.objects.create(
            name="Test Item",
            description="Test Description",
            price=Decimal('10.99'),
            restaurant=self.restaurant
        )

    def test_manage_menu_view(self):
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.get(reverse('manage_menu', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/manage_menu.html')
        self.assertIn('restaurant', response.context)
        self.assertIn('menu_items', response.context)
        self.assertEqual(response.context['restaurant'], self.restaurant)
        self.assertEqual(len(response.context['menu_items']), 1)
        self.assertEqual(response.context['menu_items'][0], self.menu_item)

    def test_add_menu_item_view(self):
        self.client.login(username='testuser', password='testpassword')
        
        # Test GET request
        response = self.client.get(reverse('add_menu_item', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/add_menu_item.html')
        self.assertIn('form', response.context)
        self.assertIn('restaurant', response.context)
        self.assertEqual(response.context['restaurant'], self.restaurant)

        # Test POST request with valid data
        form_data = {
            'name': 'New Item',
            'description': 'New Description',
            'price': '15.99'
        }
        response = self.client.post(reverse('add_menu_item', args=[self.restaurant.id]), form_data)
        self.assertEqual(response.status_code, 302)  # Should redirect to manage_menu
        self.assertEqual(MenuItem.objects.count(), 2)
        new_item = MenuItem.objects.latest('id')
        self.assertEqual(new_item.name, 'New Item')
        self.assertEqual(new_item.description, 'New Description')
        self.assertEqual(new_item.price, Decimal('15.99'))
        self.assertEqual(new_item.restaurant, self.restaurant)

    def test_edit_menu_item_view(self):
        self.client.login(username='testuser', password='testpassword')
        
        # Test GET request
        response = self.client.get(reverse('edit_menu_item', args=[self.menu_item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/edit_menu_item.html')
        self.assertIn('form', response.context)
        self.assertIn('menu_item', response.context)
        self.assertEqual(response.context['menu_item'], self.menu_item)

        # Test POST request with valid data
        form_data = {
            'name': 'Updated Item',
            'description': 'Updated Description',
            'price': '12.99'
        }
        response = self.client.post(reverse('edit_menu_item', args=[self.menu_item.id]), form_data)
        self.assertEqual(response.status_code, 302)  # Should redirect to manage_menu
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.name, 'Updated Item')
        self.assertEqual(self.menu_item.description, 'Updated Description')
        self.assertEqual(self.menu_item.price, Decimal('12.99'))

    def test_delete_menu_item_view(self):
        self.client.login(username='testuser', password='testpassword')
        
        # Test GET request
        response = self.client.get(reverse('delete_menu_item', args=[self.menu_item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/delete_menu_item.html')
        self.assertIn('menu_item', response.context)
        self.assertEqual(response.context['menu_item'], self.menu_item)

        # Test POST request
        response = self.client.post(reverse('delete_menu_item', args=[self.menu_item.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect to manage_menu
        with self.assertRaises(MenuItem.DoesNotExist):
            MenuItem.objects.get(id=self.menu_item.id)

    def test_menu_item_validation(self):
        self.client.login(username='testuser', password='testpassword')
        
        # Test negative price
        form_data = {
            'name': 'Invalid Item',
            'description': 'Invalid Description',
            'price': '-5.99'
        }
        response = self.client.post(reverse('add_menu_item', args=[self.restaurant.id]), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIn('price', response.context['form'].errors)

        # Test missing required fields
        form_data = {
            'name': '',
            'description': '',
            'price': '10.99'  # Provide a valid price
        }
        response = self.client.post(reverse('add_menu_item', args=[self.restaurant.id]), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIn('name', response.context['form'].errors)
        self.assertIn('description', response.context['form'].errors)

        # Test valid data
        form_data = {
            'name': 'Valid Item',
            'description': 'Valid Description',
            'price': '10.99'
        }
        response = self.client.post(reverse('add_menu_item', args=[self.restaurant.id]), form_data)
        self.assertEqual(response.status_code, 302)  # Should redirect on success


class ContactAdminViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
            is_staff=True  # Make user a staff member
        )
        self.contact = Contact.objects.create(
            name="Test User",
            email="test@example.com",
            subject="Test Subject",
            message="Test message content",
            status="unread"
        )

    def test_contact_messages_view(self):
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.get(reverse('contact_messages'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/contact_messages.html')
        self.assertIn('contacts', response.context)
        self.assertEqual(len(response.context['contacts']), 1)
        self.assertEqual(response.context['contacts'][0], self.contact)

    def test_view_contact_view(self):
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.get(reverse('view_contact', args=[self.contact.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/view_contact.html')
        self.assertIn('contact', response.context)
        self.assertEqual(response.context['contact'], self.contact)

    def test_update_contact_status_view(self):
        self.client.login(username='testuser', password='testpassword')
        
        # Test updating to 'read' status
        response = self.client.post(
            reverse('update_contact_status', args=[self.contact.id]),
            {'status': 'read'}
        )
        self.assertEqual(response.status_code, 302)  # Should redirect to contact_messages
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.status, 'read')

        # Test updating to 'replied' status
        response = self.client.post(
            reverse('update_contact_status', args=[self.contact.id]),
            {'status': 'replied'}
        )
        self.assertEqual(response.status_code, 302)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.status, 'replied')

        # Test invalid status
        response = self.client.post(
            reverse('update_contact_status', args=[self.contact.id]),
            {'status': 'invalid'}
        )
        self.assertEqual(response.status_code, 302)  # Should redirect to contact_messages
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.status, 'replied')  # Status should remain unchanged

    def test_delete_contact_view(self):
        self.client.login(username='testuser', password='testpassword')
        
        # Test GET request
        response = self.client.get(reverse('delete_contact', args=[self.contact.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/delete_contact.html')
        self.assertIn('contact', response.context)
        self.assertEqual(response.context['contact'], self.contact)

        # Test POST request
        response = self.client.post(reverse('delete_contact', args=[self.contact.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect to contact_messages
        with self.assertRaises(Contact.DoesNotExist):
            Contact.objects.get(id=self.contact.id)

    def test_contact_admin_unauthorized_access(self):
        # Test unauthenticated access
        for view_name in ['contact_messages', 'view_contact', 'update_contact_status', 'delete_contact']:
            if view_name == 'contact_messages':
                response = self.client.get(reverse(view_name))
            else:
                response = self.client.get(reverse(view_name, args=[self.contact.id]))
            self.assertEqual(response.status_code, 302)  # Should redirect to login
