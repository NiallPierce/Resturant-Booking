from django.test import TestCase, Client
from .models import Restaurant, TimeSlot, Booking, MenuItem, Table, Contact
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta, date
from decimal import Decimal
from .forms import BookingForm
from django.urls import reverse
from django.core.exceptions import ValidationError


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
        expected = (
            f"{self.restaurant.name} - {self.time_slot.start_time} "
            f"to {self.time_slot.end_time}"
        )
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
        expected = (
            f"{self.restaurant.name} - Table {self.table.table_number} "
            f"(Seats {self.table.capacity})"
        )
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
        valid_table.full_clean()

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
        duplicate_table = Table(
            restaurant=self.restaurant,
            table_number=1,
            capacity=4,
            is_active=True
        )
        with self.assertRaises(ValidationError):
            duplicate_table.full_clean()

    def test_table_restaurant_cascade_delete(self):
        table_id = self.table.id
        self.restaurant.delete()
        with self.assertRaises(Table.DoesNotExist):
            Table.objects.get(id=table_id)

    def test_table_validation(self):
        restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='123 Test St',
            contact_number='1234567890',
            email='test@example.com',
            opening_time=datetime.strptime('09:00', '%H:%M').time(),
            closing_time=datetime.strptime('22:00', '%H:%M').time()
        )
        table = Table(
            restaurant=restaurant,
            table_number=1,
            capacity=0,
            is_active=True
        )
        with self.assertRaises(ValidationError):
            table.full_clean()


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
        form_data = {
            'date': timezone.now().date(),
            'time': timezone.now().time(),
            'number_of_guests': 2,
            'special_requests': 'Test request'
        }
        form = BookingForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data['number_of_guests'] = 0
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('number_of_guests', form.errors)

        form_data['number_of_guests'] = 9
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('number_of_guests', form.errors)

    def test_booking_str_method(self):
        self.assertEqual(
            str(self.booking),
            f"Booking for {self.booking.restaurant.name} on "
            f"{self.booking.date}"
        )

    def test_restaurant_list_view(self):
        response = self.client.get(reverse('restaurant_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/restaurant_list.html')

    def test_restaurant_detail_view(self):
        response = self.client.get(
            reverse('restaurant_detail', args=[self.restaurant.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/restaurant_detail.html')

    def test_booking_create_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(
            reverse('book_restaurant', args=[self.restaurant.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/booking_form.html')

    def test_booking_form_edge_cases(self):
        form = BookingForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
        self.assertIn('time', form.errors)
        self.assertIn('number_of_guests', form.errors)

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

        form_data['number_of_guests'] = 11
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('number_of_guests', form.errors)

    def test_booking_validation(self):
        restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='123 Test St',
            contact_number='1234567890',
            opening_time=datetime.strptime('09:00', '%H:%M').time(),
            closing_time=datetime.strptime('22:00', '%H:%M').time()
        )
        table = Table.objects.create(
            restaurant=restaurant,
            table_number=1,
            capacity=4,
            is_active=True
        )
        user = User.objects.create_user(
            username='testuser_booking',
            password='testpass123'
        )
        booking = Booking.objects.create(
            user=user,
            restaurant=restaurant,
            table=table,
            date=date.today(),
            time=datetime.strptime('12:00', '%H:%M').time(),
            number_of_guests=4,
            status='pending'
        )
        self.assertEqual(booking.status, 'pending')

        form_data = {
            'date': date.today(),
            'time': datetime.strptime('12:00', '%H:%M').time(),
            'number_of_guests': 0,
            'table': table.id,
            'special_requests': 'Test request'
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('number_of_guests', form.errors)

    def test_booking_unauthorized_access(self):
        """Test that users cannot access other users' bookings"""
        User.objects.create_user(
            username="otheruser",
            password="otherpassword"
        )
        self.client.login(username='otheruser', password='otherpassword')

        # Test delete booking
        response = self.client.get(
            reverse('delete_booking', args=[self.booking.id])
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_booking_view(self):
        self.client.login(username='testuser', password='testpassword')

        booking_url = reverse('delete_booking', args=[self.booking.id])
        response = self.client.get(booking_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/delete_booking.html')
        self.assertIn('booking', response.context)
        self.assertEqual(response.context['booking'], self.booking)

        response = self.client.post(booking_url)
        self.assertEqual(response.status_code, 302)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'cancelled')

    def test_delete_booking_requires_login(self):
        """Test that deleting a booking requires login"""
        response = self.client.post(
            reverse('delete_booking', args=[self.booking.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/booking/{self.booking.id}/delete/'
        )

    def test_cannot_delete_others_booking(self):
        """Test that a user cannot delete another user's booking"""
        User.objects.create_user(
            username="otheruser",
            password="otherpassword"
        )
        self.client.login(username='otheruser', password='otherpassword')
        response = self.client.post(
            reverse('delete_booking', args=[self.booking.id])
        )
        self.assertEqual(response.status_code, 403)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'pending')

    def test_edit_booking_view(self):
        """Test that users can edit their own bookings"""
        self.client.login(username='testuser', password='testpassword')
        edit_url = reverse('edit_booking', args=[self.booking.id])
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/booking_form.html')
        self.assertIn('form', response.context)
        self.assertEqual(response.context['form'].instance, self.booking)


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
        valid_item = MenuItem(
            name="Valid Item",
            description="Valid Description",
            price=Decimal('15.99'),
            restaurant=self.restaurant
        )
        valid_item.full_clean()

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
        later_contact = Contact.objects.create(
            name="Later User",
            email="later@example.com",
            subject="Later Subject",
            message="Later message"
        )
        contacts = Contact.objects.all()
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
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contact.objects.count(), 1)

        contact = Contact.objects.first()
        self.assertEqual(contact.name, self.valid_data['name'])
        self.assertEqual(contact.email, self.valid_data['email'])
        self.assertEqual(contact.subject, self.valid_data['subject'])
        self.assertEqual(contact.message, self.valid_data['message'])
        self.assertEqual(contact.status, 'unread')

    def test_contact_form_invalid_data(self):
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'invalid-email'
        response = self.client.post(self.contact_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.count(), 0)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(
            form.errors['email'][0],
            'Enter a valid email address.'
        )

    def test_contact_form_missing_fields(self):
        for field in ['name', 'email', 'subject', 'message']:
            data = self.valid_data.copy()
            del data[field]
            response = self.client.post(self.contact_url, data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Contact.objects.count(), 0)
            form = response.context['form']
            self.assertFalse(form.is_valid())
            self.assertIn(field, form.errors)
            self.assertEqual(
                form.errors[field][0],
                'This field is required.'
            )


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
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/my_bookings.html')
        self.assertIn('bookings', response.context)
        self.assertEqual(len(response.context['bookings']), 1)
        self.assertEqual(response.context['bookings'][0], self.booking)

    def test_delete_booking_view(self):
        self.client.login(username='testuser', password='testpassword')

        booking_url = reverse('delete_booking', args=[self.booking.id])
        response = self.client.get(booking_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/delete_booking.html')
        self.assertIn('booking', response.context)
        self.assertEqual(response.context['booking'], self.booking)

        response = self.client.post(booking_url)
        self.assertEqual(response.status_code, 302)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'cancelled')

    def test_edit_booking_view(self):
        """Test that users can edit their own bookings"""
        self.client.login(username='testuser', password='testpassword')
        edit_url = reverse('edit_booking', args=[self.booking.id])
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/booking_form.html')
        self.assertIn('form', response.context)
        self.assertEqual(response.context['form'].instance, self.booking)


class MenuViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
            is_staff=True
        )
        self.client.login(username="testuser", password="testpassword")
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
        """Test that staff can access the menu management page"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(
            reverse('manage_menu', args=[self.restaurant.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/manage_menu.html')
        self.assertIn('restaurant', response.context)
        self.assertIn('menu_items', response.context)
        self.assertEqual(response.context['restaurant'], self.restaurant)
        self.assertEqual(len(response.context['menu_items']), 1)
        self.assertEqual(response.context['menu_items'][0], self.menu_item)

    def test_menu_item_form_view(self):
        response = self.client.get(
            reverse('edit_menu_item', args=[self.menu_item.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/menu_item_form.html')

    def test_edit_menu_item_view(self):
        response = self.client.get(
            reverse('edit_menu_item', args=[self.menu_item.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/menu_item_form.html')

    def test_menu_item_validation(self):
        """Test that menu items require a name and price"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('add_menu_item', args=[self.restaurant.id]),
            {
                'name': '',
                'price': '',
                'description': 'Test description'
            }
        )
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('price', form.errors)
        self.assertEqual(form.errors['name'][0], 'This field is required.')
        self.assertEqual(form.errors['price'][0], 'This field is required.')

    def test_delete_menu_item_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(
            reverse(
                'delete_menu_item',
                args=[self.menu_item.id]
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/delete_menu_item.html')
        self.assertIn('menu_item', response.context)
        self.assertEqual(response.context['menu_item'], self.menu_item)

        response = self.client.post(
            reverse('delete_menu_item', args=[self.menu_item.id])
        )
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(MenuItem.DoesNotExist):
            MenuItem.objects.get(id=self.menu_item.id)


class ContactAdminViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
            is_staff=True
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

        response = self.client.get(
            reverse('view_contact', args=[self.contact.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/view_contact.html')
        self.assertIn('contact', response.context)
        self.assertEqual(response.context['contact'], self.contact)

    def test_update_contact_status_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(
            reverse('update_contact_status', args=[self.contact.id]),
            {'status': 'read'}
        )
        self.assertEqual(response.status_code, 302)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.status, 'read')

        response = self.client.post(
            reverse('update_contact_status', args=[self.contact.id]),
            {'status': 'replied'}
        )
        self.assertEqual(response.status_code, 302)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.status, 'replied')

        response = self.client.post(
            reverse('update_contact_status', args=[self.contact.id]),
            {'status': 'invalid'}
        )
        self.assertEqual(response.status_code, 302)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.status, 'replied')

    def test_delete_contact_view(self):
        self.client.login(username='testuser', password='testpassword')

        delete_url = reverse('delete_contact', args=[self.contact.id])
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/delete_contact.html')
        self.assertIn('contact', response.context)
        self.assertEqual(response.context['contact'], self.contact)

        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Contact.DoesNotExist):
            Contact.objects.get(id=self.contact.id)

    def test_contact_admin_unauthorized_access(self):
        response = self.client.get(reverse('contact_messages'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            '/accounts/login/?next=/contact/messages/'
        )

        contact_url = reverse(
            'view_contact',
            kwargs={'contact_id': self.contact.id}
        )
        response = self.client.get(contact_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/contact/messages/{self.contact.id}/'
        )
