from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("Hello, world!")

# Model for Restaurant
class Restaurant(models.Model):
    name = models.CharField(max_length=100)  # Name of the restaurant
    address = models.TextField()  # Address of the restaurant
    contact_number = models.CharField(max_length=15)  # Contact phone number for the restaurant
    opening_hours = models.CharField(max_length=100)  # Opening hours (e.g., "Mon-Fri: 9 AM - 9 PM")

    def __str__(self):
        return self.name  # String representation of the restaurant