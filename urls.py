from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from restaurant import views as restaurant_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # For Allauth URLs
    path('', include('restaurant.urls')),  # Include restaurant URLs
    path('my-bookings/', restaurant_views.my_bookings, name='booking_list'),
    path(
        'my-bookings/<int:booking_id>/',
        restaurant_views.delete_booking,
        name='booking_detail'
    ),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
