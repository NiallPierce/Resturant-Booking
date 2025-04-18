from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Restaurant, MenuItem, Booking, Contact
from .forms import UserRegistrationForm, BookingForm, MenuItemForm, ContactForm


def restaurant_list(request):
    """View to display a list of all restaurants."""
    restaurants = Restaurant.objects.all()
    return render(
        request,
        'restaurant/restaurant_list.html',
        {'restaurants': restaurants}
    )


def staff_required(view_func):
    """Decorator to ensure the user is a staff member."""
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        if not request.user.is_staff:
            messages.error(
                request,
                'You do not have permission to access this page.'
            )
            return redirect('restaurant_list')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def contact(request):
    """View for submitting contact form."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request,
                    'Thank you for your message! We will get back to you soon.'
                )
                return redirect('contact_success')
            except Exception as e:
                messages.error(
                    request,
                    'An error occurred while submitting your message. '
                    'Please try again later.'
                )
                print(f"Contact submission error: {str(e)}")
        else:
            messages.error(
                request,
                'Please correct the errors in the form below.'
            )
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.title()}: {error}")
    else:
        form = ContactForm()
    return render(
        request,
        'restaurant/contact.html',
        {'form': form}
    )


@login_required
def my_bookings(request):
    """View for displaying user's bookings."""
    bookings = Booking.objects.filter(
        user=request.user
    ).order_by('-date', '-time')
    return render(
        request,
        'restaurant/my_bookings.html',
        {'bookings': bookings}
    )


@login_required
def delete_booking(request, booking_id):
    """Delete a booking"""
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.user != request.user:
        return HttpResponseForbidden(
            "You don't have permission to delete this booking"
        )
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Your booking has been cancelled')
        return redirect('my_bookings')
    return render(
        request,
        'restaurant/delete_booking.html',
        {'booking': booking}
    )


def logout_view(request):
    """View for logging out users."""
    logout(request)
    return redirect('restaurant_list')


def restaurant_detail(request, restaurant_id):
    """View for displaying restaurant details."""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    return render(
        request,
        'restaurant/restaurant_detail.html',
        {
            'restaurant': restaurant,
            'menu_items': menu_items
        }
    )


def register(request):
    """View for user registration."""
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request,
                f'Account created for {username}! You can now log in.'
            )
            return redirect('login')

    return render(
        request,
        'account/register.html',
        {'form': form}
    )


@login_required
def book_restaurant(request, restaurant_id):
    """View for making a restaurant booking."""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.restaurant = restaurant
            booking.save()
            messages.success(
                request,
                'Your booking has been created successfully!'
            )
            return redirect('my_bookings')
    else:
        form = BookingForm()
    return render(
        request,
        'restaurant/booking_form.html',
        {'form': form, 'restaurant': restaurant}
    )


@login_required
def edit_booking(request, booking_id):
    """View for editing a booking."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your booking has been updated successfully!'
            )
            return redirect('my_bookings')
    else:
        form = BookingForm(instance=booking)
    return render(
        request,
        'restaurant/booking_form.html',
        {'form': form}
    )


@login_required
def manage_menu(request, restaurant_id):
    """View for managing restaurant menu items."""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if not request.user.is_staff:
        return HttpResponseForbidden()
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    return render(
        request,
        'restaurant/manage_menu.html',
        {'restaurant': restaurant, 'menu_items': menu_items}
    )


@login_required
def add_menu_item(request, restaurant_id):
    """View for adding a menu item."""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant = restaurant
            menu_item.save()
            messages.success(request, 'Menu item added successfully!')
            return redirect('manage_menu', restaurant_id=restaurant_id)
    else:
        form = MenuItemForm()
    return render(
        request,
        'restaurant/menu_item_form.html',
        {'form': form, 'restaurant': restaurant}
    )


@login_required
def edit_menu_item(request, menu_item_id):
    """View for editing a menu item."""
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=menu_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item updated successfully!')
            return redirect(
                'manage_menu',
                restaurant_id=menu_item.restaurant.id
            )
    else:
        form = MenuItemForm(instance=menu_item)
    return render(
        request,
        'restaurant/menu_item_form.html',
        {
            'form': form,
            'menu_item': menu_item,
            'restaurant': menu_item.restaurant
        }
    )


@login_required
def delete_menu_item(request, menu_item_id):
    """View for deleting a menu item."""
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if request.method == 'POST':
        restaurant_id = menu_item.restaurant.id
        menu_item.delete()
        messages.success(request, 'Menu item deleted successfully!')
        return redirect('manage_menu', restaurant_id=restaurant_id)
    return render(
        request,
        'restaurant/delete_menu_item.html',
        {'menu_item': menu_item}
    )


@login_required
def contact_messages(request):
    """View for displaying contact messages."""
    if not request.user.is_staff:
        return HttpResponseForbidden()
    contacts = Contact.objects.all().order_by('-created_at')
    return render(
        request,
        'restaurant/contact_messages.html',
        {'contacts': contacts}
    )


@login_required
def view_contact(request, contact_id):
    """View for displaying contact message details."""
    if not request.user.is_staff:
        return HttpResponseForbidden()
    contact = get_object_or_404(Contact, id=contact_id)
    return render(
        request,
        'restaurant/view_contact.html',
        {'contact': contact}
    )


@login_required
def update_contact_status(request, contact_id):
    """View for updating contact message status."""
    if not request.user.is_staff:
        return HttpResponseForbidden()
    contact = get_object_or_404(Contact, id=contact_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Contact.STATUS_CHOICES):
            contact.status = new_status
            contact.save()
            messages.success(request, 'Contact status updated successfully.')
        else:
            messages.error(request, 'Invalid status selected.')
    return redirect('view_contact', contact_id=contact_id)


@login_required
def delete_contact(request, contact_id):
    """View for deleting a contact message."""
    if not request.user.is_staff:
        return HttpResponseForbidden()
    contact = get_object_or_404(Contact, id=contact_id)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact message deleted successfully.')
        return redirect('contact_messages')
    return render(
        request,
        'restaurant/delete_contact.html',
        {'contact': contact}
    )


def contact_success(request):
    """View for displaying contact form submission success."""
    return render(request, 'restaurant/contact_success.html')
