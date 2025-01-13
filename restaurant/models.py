from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Restaurant Model
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    opening_time = models.TimeField(default=datetime.strptime('09:00', '%H:%M').time())
    closing_time = models.TimeField(default=datetime.strptime('22:00', '%H:%M').time())
    capacity = models.IntegerField(default=50)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()

    def str(self):
        return self.name

# Table Model
class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    table_number = models.IntegerField()
    capacity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def str(self):
        return f"{self.restaurant.name} - Table {self.table_number} (Seats {self.capacity})"

#TimeSlot Model
class TimeSlot(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    def str(self):
        return f"{self.restaurant.name} - {self.start_time} to {self.end_time}"

#Booking Model
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True, blank=True)  # Optional table assignment
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, null=True, blank=True)  # Optional time slot
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def str(self):
        return f"Booking for {self.user.username} at {self.restaurant.name} on {self.date} at {self.time}"

    class Meta:
        ordering = ['-date', '-time']  # Orders bookings by date and time, most recent first

#MenuItem Model
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - ${self.price}"