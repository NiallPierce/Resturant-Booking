from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, Table, MenuItem, Contact
from datetime import datetime, time, timedelta
from django.utils import timezone


class UserRegistrationForm(UserCreationForm):
    """Custom form for user registration."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class BookingForm(forms.ModelForm):
    """Model form for creating/editing bookings."""
    class Meta:
        model = Booking
        fields = ['date', 'time', 'number_of_guests', 'special_requests', 'table']

        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'min': timezone.now().date().isoformat(),
                }
            ),
            'time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                    'min': '09:00',
                    'max': '22:00',
                }
            ),
            'number_of_guests': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '1',
                    'max': '8',
                }
            ),
            'special_requests': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'maxlength': '500',
                }
            ),
            'table': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

    def clean_number_of_guests(self):
        guests = self.cleaned_data.get('number_of_guests')
        if guests is None:
            raise forms.ValidationError("Please specify the number of guests.")
        if guests < 1:
            raise forms.ValidationError("Number of guests must be at least 1.")
        if guests > 8:
            raise forms.ValidationError("Number of guests cannot exceed 8.")
        return guests

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date is None:
            raise forms.ValidationError("Please select a date.")
        if date < timezone.now().date():
            raise forms.ValidationError("You cannot book a table for a past date.")
        return date

    def clean_time(self):
        time = self.cleaned_data.get('time')
        if time is None:
            raise forms.ValidationError("Please select a time.")
        opening_time = datetime.strptime('09:00', '%H:%M').time()
        closing_time = datetime.strptime('22:00', '%H:%M').time()
        if time < opening_time:
            raise forms.ValidationError(f"Booking time must be after {opening_time.strftime('%I:%M %p')}.")
        if time > closing_time:
            raise forms.ValidationError(f"Booking time must be before {closing_time.strftime('%I:%M %p')}.")
        return time

    def clean_table(self):
        table = self.cleaned_data.get('table')
        number_of_guests = self.cleaned_data.get('number_of_guests')
        
        if table is None:
            raise forms.ValidationError("Please select a table.")
        if number_of_guests and number_of_guests > table.capacity:
            raise forms.ValidationError(
                f"Selected table can only accommodate {table.capacity} guests. "
                f"Please select a different table or reduce the number of guests."
            )
        return table

    def clean_special_requests(self):
        special_requests = self.cleaned_data.get('special_requests', '')
        if len(special_requests) > 500:
            raise forms.ValidationError("Special requests cannot exceed 500 characters.")
        return special_requests


class MenuItemForm(forms.ModelForm):
    """Model form for creating/editing menu items."""
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'maxlength': '100',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'maxlength': '500',
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0.01',
                    'step': '0.01',
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Menu item name is required.")
        if len(name) > 100:
            raise forms.ValidationError("Menu item name cannot exceed 100 characters.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise forms.ValidationError("Menu item description is required.")
        if len(description) > 500:
            raise forms.ValidationError("Menu item description cannot exceed 500 characters.")
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            raise forms.ValidationError("Price is required.")
        if price <= 0:
            raise forms.ValidationError("Price must be greater than 0.")
        return price


class ContactForm(forms.ModelForm):
    """Model form for contact submissions."""
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'maxlength': '100',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'subject': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'maxlength': '200',
                }
            ),
            'message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'maxlength': '1000',
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Name is required.")
        if len(name) > 100:
            raise forms.ValidationError("Name cannot exceed 100 characters.")
        return name

    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        if not subject:
            raise forms.ValidationError("Subject is required.")
        if len(subject) > 200:
            raise forms.ValidationError("Subject cannot exceed 200 characters.")
        return subject

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if not message:
            raise forms.ValidationError("Message is required.")
        if len(message) > 1000:
            raise forms.ValidationError("Message cannot exceed 1000 characters.")
        return message
