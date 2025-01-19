from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking
from datetime import datetime, time, timedelta

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time', 'number_of_guests', 'special_requests']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'class': 'form-control',
                }
            ),
            'time': forms.TimeInput(
                attrs={
                    'type': 'time', 
                    'class': 'form-control',
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
                }
            ),
        }