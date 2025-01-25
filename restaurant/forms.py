from django import forms  # Imports the forms module from Django
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User  # Imports the User model
from .models import Booking  
from datetime import datetime, time, timedelta  

class UserRegistrationForm(UserCreationForm):
    # Defines a custom form for user registration, inheriting from Django's UserCreationForm
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        # Meta class to configure form details
        model = User  # Specifies the model this form is associated with
        fields = ['username', 'email', 'password1', 'password2']
        # Specifies the model fields that will be included in this form

class BookingForm(forms.ModelForm):
    # Defines a model form for creating/editing bookings
    class Meta:
        # Meta class for BookingForm
        model = Booking  # Specifies the Booking model is associated with this form
        fields = ['date', 'time', 'number_of_guests', 'special_requests']
        # Specifies the model fields that should be part of this form

        widgets = {
        # Define custom widgets for each of the form fields
            'date': forms.DateInput(
                attrs={
                 'type': 'date',
                 'class': 'form-control',
                }
            ),
          # Date field with type set to 'date' to get a date picker, styled with Bootstrap class
            'time': forms.TimeInput(
                attrs={
                 'type': 'time',
                'class': 'form-control',
                }
            ),
          # Time field with type 'time' for a time picker, styled with Bootstrap class
            'number_of_guests': forms.NumberInput(
                attrs={
                 'class': 'form-control',
                 'min': '1',
                 'max': '8',
                 }
            ),
           # Number of guests field, restricting it to a minimum of one and maximum of 8, styled with Bootstrap class
            'special_requests': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    }
                ),
          # Text area for special requests, styled with Bootstrap class, set to 3 rows
        }