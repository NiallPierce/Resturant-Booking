from django.shortcuts import render
from .models import Restaurant
from django import forms

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