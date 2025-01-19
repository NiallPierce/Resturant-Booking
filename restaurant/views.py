from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
from .models import Restaurant, MenuItem, Booking
from django import forms
from .forms import UserRegistrationForm

def restaurant_list(request):
    print("\n=== Restaurant List View Debug ===")
    print(f"Request Path: {request.path}")
    print(f"Request Method: {request.method}")
    print(f"Content Type: {request.content_type}")

    restaurants = Restaurant.objects.all()
    print(f"Found {restaurants.count()} restaurants in database")
    if restaurants.exists():
        print("Restaurant names:")
        for r in restaurants:
            print(f"- {r.name}")
    else:
        print("No restaurants found in database")

    print("Attempting to render template: restaurant_list.html")
    print("=== End Debug ===\n")

    return render(request, 'restaurant/restaurant_list.html', {'restaurants': restaurants})

# Add new BookingForm class
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time', 'number_of_guests', 'special_requests']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
# Add restaurant detail view
def restaurant_detail(request, restaurant_id):
    print("\n=== Restaurant Detail View Debug ===")
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    print(f"Showing details for restaurant: {restaurant.name}")
    print(f"Found {menu_items.count()} menu items")
    print("=== End Debug ===\n")
    return render(request, 'restaurant/restaurant_detail.html', {
        'restaurant': restaurant,
        'menu_items': menu_items
    })

def register(request):
    # Initialize form variable outside the if block
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')

    return render(request, 'registration/register.html', {'form': form})

# Add booking view
@login_required
def book_restaurant(request, restaurant_id):
    print("\n=== Restaurant Booking View Debug ===")
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    print(f"Processing booking for restaurant: {restaurant.name}")
    
    if request.method == 'POST':
        print("Processing POST request with booking data")
        form = BookingForm(request.POST)
        if form.is_valid():
            print("Form is valid - creating booking")
            booking = form.save(commit=False)
            booking.user = request.user
            booking.restaurant = restaurant
            booking.save()
            print(f"Booking created for user: {request.user.username}")
            return redirect('restaurant_list')  # create a confirmation view
        else:
            print("Form validation failed")
            print(f"Form errors: {form.errors}")
    else:
        print("Displaying empty booking form")
        form = BookingForm()
    
    print("=== End Debug ===\n")
    return render(request, 'restaurant/booking_form.html', {
        'form': form,
        'restaurant': restaurant
    })