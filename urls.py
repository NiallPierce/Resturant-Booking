from django.contrib import admin
from django.urls import path, include
from django.urls import get_resolver
print("=== Registered URLs ===")
print(get_resolver().url_patterns)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('restaurants.urls')),  # Include restaurant URLs
    path('bookings/', include('booking.urls')),  # Include booking URLs (no need to import views directly)
    
]