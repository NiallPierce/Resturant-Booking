from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from restaurant.models import Restaurant, MenuItem, Contact, Booking, Table
from decimal import Decimal
from datetime import datetime, date


class RestaurantViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            is_staff=True
        )
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='123 Test St',
            description='Test Description',
            opening_time=datetime.strptime('09:00', '%H:%M').time(),
            closing_time=datetime.strptime('22:00', '%H:%M').time(),
            capacity=50,
            contact_number='1234567890',
            email='restaurant@test.com'
        )
        self.table = Table.objects.create(
            restaurant=self.restaurant,
            table_number=1,
            capacity=4,
            is_active=True
        )
        self.menu_item = MenuItem.objects.create(
            name='Test Item',
            description='Test Description',
            price=Decimal('10.99'),
            restaurant=self.restaurant
        )
        self.contact = Contact.objects.create(
            name='Test Contact',
            email='test@example.com',
            subject='Test Subject',
            message='Test Message'
        )

    def test_restaurant_list_view(self):
        response = self.client.get(reverse('restaurant_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/restaurant_list.html')
        self.assertIn('restaurants', response.context)
        self.assertEqual(
            list(response.context['restaurants']),
            [self.restaurant]
        )

    def test_restaurant_detail_view(self):
        response = self.client.get(
            reverse('restaurant_detail', args=[self.restaurant.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/restaurant_detail.html')
        self.assertEqual(response.context['restaurant'], self.restaurant)

    def test_contact_view_get(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/contact.html')
        self.assertIn('form', response.context)

    def test_contact_form_submission(self):
        response = self.client.post(
            reverse('contact'),
            {
                'name': 'Test User',
                'email': 'test@example.com',
                'subject': 'Test Subject',
                'message': 'Test Message'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('contact_success'))

    def test_contact_view_post_invalid(self):
        initial_count = Contact.objects.count()
        data = {
            'name': '',  # Empty name
            'email': 'invalid-email',  # Invalid email format
            'subject': '',  # Empty subject
            'message': ''  # Empty message
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 200)
        # Check that no new objects were created
        self.assertEqual(Contact.objects.count(), initial_count)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)
        self.assertIn('name', response.context['form'].errors)
        self.assertIn('email', response.context['form'].errors)
        self.assertIn('subject', response.context['form'].errors)
        self.assertIn('message', response.context['form'].errors)

    def test_my_bookings_view_unauthenticated(self):
        response = self.client.get(reverse('my_bookings'))
        login_url = reverse('account_login')
        self.assertRedirects(
            response,
            f'{login_url}?next={reverse("my_bookings")}'
        )

    def test_my_bookings_view_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('my_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/my_bookings.html')
        self.assertIn('bookings', response.context)

    def test_manage_menu_view_unauthenticated(self):
        url = reverse('manage_menu', args=[self.restaurant.id])
        response = self.client.get(url)
        login_url = reverse('account_login')
        self.assertRedirects(response, f'{login_url}?next={url}')

    def test_manage_menu_view_authenticated(self):
        self.client.force_login(self.user)
        url = reverse('manage_menu', args=[self.restaurant.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/manage_menu.html')
        self.assertEqual(response.context['restaurant'], self.restaurant)
        self.assertIn('menu_items', response.context)

    def test_add_menu_item_view(self):
        self.client.force_login(self.user)
        url = reverse('add_menu_item', args=[self.restaurant.id])
        data = {
            'name': 'New Item',
            'description': 'New Description',
            'price': '15.99'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MenuItem.objects.count(), 2)
        new_item = MenuItem.objects.latest('id')
        self.assertEqual(new_item.name, data['name'])
        self.assertEqual(new_item.price, Decimal(data['price']))

    def test_edit_menu_item_view(self):
        self.client.force_login(self.user)
        url = reverse('edit_menu_item', args=[self.menu_item.id])
        data = {
            'name': 'Updated Item',
            'description': 'Updated Description',
            'price': '20.99'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.name, data['name'])
        self.assertEqual(self.menu_item.price, Decimal(data['price']))

    def test_delete_menu_item_view(self):
        self.client.force_login(self.user)
        url = reverse('delete_menu_item', args=[self.menu_item.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MenuItem.objects.count(), 0)

    def test_booking_creation(self):
        """Test booking creation."""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse(
                'book_restaurant',
                kwargs={'restaurant_id': self.restaurant.id}
            ),
            {
                'date': date.today(),
                'time': datetime.strptime('12:00', '%H:%M').time(),
                'number_of_guests': 4,
                'table': self.table.id,
                'special_requests': 'Test request'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.count(), 1)
        booking = Booking.objects.first()
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.restaurant, self.restaurant)
        self.assertEqual(booking.number_of_guests, 4)

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

    def test_menu_item_edit_view(self):
        """Test menu item edit view."""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                'edit_menu_item',
                kwargs={'menu_item_id': self.menu_item.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/menu_item_form.html')

    def test_menu_item_delete_view(self):
        """Test menu item delete view."""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                'delete_menu_item',
                kwargs={'menu_item_id': self.menu_item.id}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/delete_menu_item.html')

    def test_contact_messages_view(self):
        """Test contact messages view."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('contact_messages'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/contact_messages.html')

    def test_contact_success_view(self):
        response = self.client.get(reverse('contact_success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/contact_success.html')
