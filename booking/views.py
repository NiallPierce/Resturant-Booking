from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from restaurant.models import Booking

@login_required
def booking_list(request):
    """View for listing user's bookings."""
    return redirect('my_bookings')  # Redirect to the existing my_bookings view

@login_required
def booking_detail(request, booking_id):
    """View for showing booking details."""
    booking = Booking.objects.get(id=booking_id, user=request.user)
    return render(request, 'restaurant/delete_booking.html', {'booking': booking}) 