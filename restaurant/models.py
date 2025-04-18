from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.exceptions import ValidationError


# Restaurant Model
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    opening_time = models.TimeField(
        default=datetime.strptime('09:00', '%H:%M').time()
    )
    closing_time = models.TimeField(
        default=datetime.strptime('22:00', '%H:%M').time()
    )
    capacity = models.IntegerField(default=50)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name


# Table Model
class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    table_number = models.IntegerField()
    capacity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['restaurant', 'table_number']

    def clean(self):
        if self.capacity <= 0:
            raise ValidationError('Table capacity must be greater than 0.')
        
        # Check for duplicate table numbers within the same restaurant
        if Table.objects.filter(
            restaurant=self.restaurant,
            table_number=self.table_number
        ).exclude(id=self.id).exists():
            raise ValidationError(
                f'Table number {self.table_number} already exists for this restaurant.'
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.restaurant.name} - Table {self.table_number} "
            f"(Seats {self.capacity})"
        )


# TimeSlot Model
class TimeSlot(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.start_time} to {self.end_time}"


# Booking Model
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )  # Optional table assignment
    time_slot = models.ForeignKey(
        TimeSlot,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )  # Optional time slot
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"Booking for {self.user.username} at {self.restaurant.name} "
            f"on {self.date} at {self.time}"
        )

    class Meta:
        ordering = ['-date', '-time']  # Orders bookings by date and time


# MenuItem Model
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def clean(self):
        if self.price is not None and self.price < 0:
            raise ValidationError('Price cannot be negative.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - ${self.price}"


class Contact(models.Model):
    """Model for storing contact form submissions."""
    STATUS_CHOICES = [
        ('unread', 'Unread'),
        ('read', 'Read'),
        ('replied', 'Replied'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='unread'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contact from {self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']
