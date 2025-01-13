from django.contrib import admin
from django.urls import path, include
from django.urls import get_resolver

print("=== Registered URLs ===")
print(get_resolver().url_patterns)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # For authentication URLs
    path('', include('restaurants.urls')),  # Include restaurant URLs
    path('bookings/', include('booking.urls')),  # Include booking URLs
]