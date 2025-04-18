from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib import messages
from .models import Restaurant, MenuItem, Booking, Contact, Table, TimeSlot
from django import forms
from .forms import UserRegistrationForm, BookingForm, MenuItemForm, ContactForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date, datetime
from decimal import Decimal


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time', 'number_of_guests', 'special_requests']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': date.today().strftime('%Y-%m-%d')
            }),
            'time': forms.TimeInput(
                attrs={'type': 'time', 'class': 'form-control'}
            ),
            'number_of_guests': forms.NumberInput(
                attrs={'class': 'form-control', 'min': 1}
            ),
            'special_requests': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }

    def clean_date(self):
        selected_date = self.cleaned_data.get('date')
        if selected_date < date.today():
            raise forms.ValidationError(
                "You cannot select a date in the past."
            )
        return selected_date

    def clean_number_of_guests(self):
        guests = self.cleaned_data.get('number_of_guests')
        if guests < 1:
            raise forms.ValidationError(
                "Number of guests must be at least 1."
            )
        return guests


def staff_required(view_func):
    """Decorator to ensure the user is a staff member."""
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        if not request.user.is_staff:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('restaurant_list')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def restaurant_list(request):
    """View to display a list of all restaurants."""
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

    return render(
        request,
        'restaurant/restaurant_list.html',
        {'restaurants': restaurants}
    )


def contact(request):
    """View for submitting contact form."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                contact = form.save()
                messages.success(
                    request,
                    'Thank you for your message! We will get back to you soon.'
                )
                return redirect('restaurant_list')
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
    bookings = Booking.objects.filter(
        user=request.user
    ).order_by('-date', '-time')
    return render(
        request,
        'restaurant/my_bookings.html',
        {'bookings': bookings}
    )


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Your booking has been cancelled.')
        return redirect('my_bookings')
    
    return render(request, 'restaurant/delete_booking.html', {'booking': booking})


def logout_view(request):
    logout(request)
    return redirect('restaurant_list')


def restaurant_detail(request, restaurant_id):
    print("\n=== Restaurant Detail View Debug ===")
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    print(f"Showing details for restaurant: {restaurant.name}")
    print(f"Found {menu_items.count()} menu items")
    print("=== End Debug ===\n")
    return render(
        request,
        'restaurant/restaurant_detail.html',
        {
            'restaurant': restaurant,
            'menu_items': menu_items
        }
    )


def register(request):
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request,
                f'Account created for {username}! '
                'You can now log in.'
            )
            return redirect('login')

    return render(request, 'account/register.html', {'form': form})


@login_required
def book_restaurant(request, restaurant_id):
    print("\n=== Restaurant Booking View Debug ===")
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    print(f"Processing booking for restaurant: {restaurant.name}")

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                booking = form.save(commit=False)
                booking.user = request.user
                booking.restaurant = restaurant
                booking.status = 'pending'
                booking.save()
                messages.success(
                    request,
                    'Your booking has been submitted successfully! '
                    'We will confirm your reservation shortly.'
                )
                return redirect('my_bookings')
            except Exception as e:
                messages.error(
                    request,
                    'An error occurred while processing your booking. '
                    'Please try again later.'
                )
                print(f"Booking error: {str(e)}")
        else:
            messages.error(
                request,
                'Please correct the errors in the form below.'
            )
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.title()}: {error}")
    else:
        form = BookingForm()
        print("Displaying empty booking form")

    print("=== End Debug ===\n")
    return render(
        request,
        'restaurant/booking_form.html',
        {'form': form, 'restaurant': restaurant}
    )


@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status == 'cancelled':
        messages.error(
            request,
            'Cannot edit a cancelled booking. Please create a new booking instead.'
        )
        return redirect('my_bookings')
    
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            try:
                updated_booking = form.save()
                messages.success(
                    request,
                    'Your booking has been updated successfully!'
                )
                return redirect('my_bookings')
            except Exception as e:
                messages.error(
                    request,
                    'An error occurred while updating your booking. '
                    'Please try again later.'
                )
                print(f"Booking update error: {str(e)}")
        else:
            messages.error(
                request,
                'Please correct the errors in the form below.'
            )
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.title()}: {error}")
    else:
        form = BookingForm(instance=booking)
    
    return render(
        request,
        'restaurant/edit_booking.html',
        {'form': form, 'booking': booking}
    )


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        try:
            booking.delete()
            messages.success(
                request,
                'Your booking has been deleted successfully.'
            )
        except Exception as e:
            messages.error(
                request,
                'An error occurred while deleting your booking. '
                'Please try again later.'
            )
            print(f"Booking deletion error: {str(e)}")
        return redirect('my_bookings')
    
    return render(
        request,
        'restaurant/delete_booking.html',
        {'booking': booking}
    )


@login_required
def manage_menu(request, restaurant_id):
    """View for managing restaurant menu items."""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    
    return render(
        request,
        'restaurant/manage_menu.html',
        {
            'restaurant': restaurant,
            'menu_items': menu_items
        }
    )


@login_required
def add_menu_item(request, restaurant_id):
    """View for adding a new menu item."""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            try:
                menu_item = form.save(commit=False)
                menu_item.restaurant = restaurant
                menu_item.save()
                messages.success(
                    request,
                    'Menu item added successfully!'
                )
                return redirect('manage_menu', restaurant_id=restaurant.id)
            except Exception as e:
                messages.error(
                    request,
                    'An error occurred while adding the menu item. '
                    'Please try again later.'
                )
                print(f"Menu item addition error: {str(e)}")
        else:
            messages.error(
                request,
                'Please correct the errors in the form below.'
            )
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.title()}: {error}")
    else:
        form = MenuItemForm()
    
    return render(
        request,
        'restaurant/add_menu_item.html',
        {
            'form': form,
            'restaurant': restaurant
        }
    )


@login_required
def edit_menu_item(request, menu_item_id):
    """View for editing an existing menu item."""
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=menu_item)
        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request,
                    'Menu item updated successfully!'
                )
                return redirect('manage_menu', restaurant_id=menu_item.restaurant.id)
            except Exception as e:
                messages.error(
                    request,
                    'An error occurred while updating the menu item. '
                    'Please try again later.'
                )
                print(f"Menu item update error: {str(e)}")
        else:
            messages.error(
                request,
                'Please correct the errors in the form below.'
            )
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.title()}: {error}")
    else:
        form = MenuItemForm(instance=menu_item)
    
    return render(
        request,
        'restaurant/edit_menu_item.html',
        {
            'form': form,
            'menu_item': menu_item
        }
    )


@login_required
def delete_menu_item(request, menu_item_id):
    """View for deleting a menu item."""
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    restaurant_id = menu_item.restaurant.id
    
    if request.method == 'POST':
        try:
            menu_item.delete()
            messages.success(
                request,
                'Menu item deleted successfully!'
            )
        except Exception as e:
            messages.error(
                request,
                'An error occurred while deleting the menu item. '
                'Please try again later.'
            )
            print(f"Menu item deletion error: {str(e)}")
        return redirect('manage_menu', restaurant_id=restaurant_id)
    
    return render(
        request,
        'restaurant/delete_menu_item.html',
        {'menu_item': menu_item}
    )


@staff_required
def contact_messages(request):
    """View for admin to see all contact messages."""
    contacts = Contact.objects.all().order_by('-created_at')
    return render(
        request,
        'restaurant/contact_messages.html',
        {'contacts': contacts}
    )


@staff_required
def view_contact(request, contact_id):
    """View for admin to view a specific contact message."""
    contact = get_object_or_404(Contact, id=contact_id)
    if contact.status == 'unread':
        contact.status = 'read'
        contact.save()
    
    return render(
        request,
        'restaurant/view_contact.html',
        {'contact': contact}
    )


@staff_required
def update_contact_status(request, contact_id):
    """View for admin to update contact message status."""
    contact = get_object_or_404(Contact, id=contact_id)
    
    if request.method == 'POST':
        try:
            new_status = request.POST.get('status')
            if new_status in dict(Contact.STATUS_CHOICES):
                contact.status = new_status
                contact.save()
                messages.success(
                    request,
                    'Contact message status updated successfully!'
                )
            else:
                messages.error(
                    request,
                    'Invalid status selected.'
                )
        except Exception as e:
            messages.error(
                request,
                'An error occurred while updating the status. '
                'Please try again later.'
            )
            print(f"Contact status update error: {str(e)}")
    
    return redirect('view_contact', contact_id=contact_id)


@staff_required
def delete_contact(request, contact_id):
    """View for admin to delete a contact message."""
    contact = get_object_or_404(Contact, id=contact_id)
    
    if request.method == 'POST':
        try:
            contact.delete()
            messages.success(
                request,
                'Contact message deleted successfully!'
            )
            return redirect('contact_messages')
        except Exception as e:
            messages.error(
                request,
                'An error occurred while deleting the message. '
                'Please try again later.'
            )
            print(f"Contact deletion error: {str(e)}")
            return redirect('view_contact', contact_id=contact_id)
    
    return render(
        request,
        'restaurant/delete_contact.html',
        {'contact': contact}
    )
