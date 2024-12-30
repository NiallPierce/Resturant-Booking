from django.db import models

# Create your models here.
# Model for Restaurant
class Restaurant(models.Model):
    name = models.CharField(max_length=100)  # Name of the restaurant
    address = models.TextField()  # Address of the restaurant
    contact_number = models.CharField(max_length=15)  # Contact phone number for the restaurant
    opening_hours = models.CharField(max_length=100)  # Opening hours (e.g., "Mon-Fri: 9 AM - 9 PM")

    def __str__(self):
        return self.name  # String representation of the restaurant

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to Django's built-in User model
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Booking for {self.user.username} on {self.date} at {self.time}"

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - ${self.price}"